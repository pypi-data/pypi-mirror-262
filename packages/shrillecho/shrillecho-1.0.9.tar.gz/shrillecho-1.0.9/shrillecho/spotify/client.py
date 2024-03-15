import asyncio
from dataclasses import asdict, dataclass
import math
import time
from typing import List, Optional, Type, Union
from annotated_types import T
from fastclasses_json import dataclass_json
import httpx
import json
import os

from shrillecho.auth.local_auth import authenticate_local
from shrillecho.auth.oauth import ClientCredentials, OAuthCredentials
from shrillecho.types.album_types import ArtistAlbums, SeveralAlbums
from shrillecho.types.artist_types import Artist, SeveralArtists
from shrillecho.types.playlist_types import Playlist, PlaylistTrack, PlaylistTracks, SimplifiedPlaylistObject, UserPlaylists
from shrillecho.types.track_types import Recc, SavedTrack, SavedTracks, SeveralTracks, Track
from shrillecho.utility.general_utility import sp_fetch
import spotipy
# from shrillecho.auth.local_auth import authenticate_local
from shrillecho.utility.archive_maybe_delete.old_cache import Cache
from shrillecho.utility.cache import mongo_client, redis_client
import redis

@dataclass
class SpotifyAuthContext:
    client_id: str
    client_secret: str
    scope: str
    redirect_uri: str

class SpotifyClient:

    SPOTIFY_API = "https://api.spotify.com/v1/"

    def __init__(self, auth=None, auth_flow: Union[OAuthCredentials | ClientCredentials] = None):
        self.auth = auth
        self.auth_flow = auth_flow
        if auth_flow:
            self.access_token = auth_flow.get_access_token()
        else:
            self.access_token = self.auth
        self.temp_spotipy: spotipy.Spotify = spotipy.Spotify(auth=self.access_token)
        self.http_client: httpx.AsyncClient = httpx.AsyncClient
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.batch_errors = 0

    async def _request(self, 
                       method: str, 
                       endpoint: str, 
                       response_type = None,
                       params: Optional[dict] = None, 
                       body: Optional[dict] = None):
        
        if self.auth:
            access_token = self.auth
        elif self.auth_flow:
            access_token = self.auth_flow.get_access_token()
        else:
            raise Exception("No authorization provided to the client")

        headers = {"Authorization" : f"Bearer {access_token}"}
        
        async with self.http_client() as client:
         
            response = await client.request(method, f"{self.SPOTIFY_API}{endpoint}", params=params, headers=headers, json=body)

            if response.status_code > 300:
                raise Exception("Spotify Client Error", response.text)

            if response_type:
                return response_type.from_json(json.dumps(response.json()))
            else:
                return response.json()
        

    async def _async_fetch_urls(self, urls, chunk_size, client, tracks, sp_type):
        def chunks(lst, n):
            for i in range(0, len(lst), n):
                yield lst[i:i + n]

          
        if self.auth:
            access_token = self.auth
        elif self.auth_flow:
            access_token = self.auth_flow.get_access_token()
        else:
            raise Exception("No authorization provided to the client")

        headers = {"Authorization" : f"Bearer {access_token}"}

        for batch in chunks(urls, chunk_size):
            while len(batch) != 0:
                print(f"fetching batch size: {len(batch)}")
                responses = await asyncio.gather(*(client.get(url, headers=headers) for url in batch))
                passed_responses = []
                indices_to_remove = []
                retry = 0
                for idx, r in enumerate(responses):
                    if r.status_code == 200:
                        passed_responses.append(r)
                        indices_to_remove.append(idx)
                        # cache the get response for this URL, for retry purposes , wipe it 
                        # after as we have a complete caching layer, so we dont really want to have this fully caching
                        # always but maybe consider.
                    else:
                        if r.status_code == 429:
                            retry = int(r.headers.get('Retry-After'))
                        else:
                            self.batch_errors += 1 
                            raise Exception("Batch Error, setting batch size to 10")
                if retry != 0:
                    print("rate limit waiting to try again...")
                    await asyncio.sleep(retry)

                batch = [url for idx, url in enumerate(batch) if idx not in indices_to_remove]
                if len(passed_responses) > 0:
                    tracks.extend(sp_fetch(response.json, sp_type) for response in passed_responses)
            
    async def _batch_request(self, ep_path: str, initial_item , sp_type: Type[T], *args, chunk_size=25):
        async with httpx.AsyncClient() as client:
            urls = []
            limit = 50
    
            items: List[sp_type] = [initial_item]
        
            pages = math.ceil(initial_item.total / limit)
        
            for page in range(1, pages):
                urls.append(f"https://api.spotify.com/v1/{ep_path}?limit=50&offset={limit * page}")
                
            try:
                await self._async_fetch_urls(urls, chunk_size, client, items, sp_type)
            except Exception as e:
                 if self.batch_errors > 3:
                      raise Exception("Fatal Error, Batch request failed after 3 retries")
                 items: List[sp_type] = [initial_item]
                 await self._async_fetch_urls(urls=urls, client=client, tracks=items, sp_type=sp_type, chunk_size=10)

            self.batch_errors = 0

            """ sort this out, essentially this batcher is designed for paginated requests
                so we want the items bit all collated into one sequential list
            """
            unpacked_items = []
        
            for chunk in items:
                for cube in chunk.items:
                        unpacked_items.append(cube)


            return unpacked_items

    async def _get(self, endpoint: str, response_type=None, params: Optional[dict]=None):
        print(f'GETTING: {endpoint}')
        return await self._request(method="GET", endpoint=endpoint, params=params, response_type=response_type)
    
    async def _post(self, endpoint: str, body: dict, params: Optional[dict]=None):
        await self._request(method="POST", endpoint=endpoint, params=params, body=body)



    ############# Shrillecho Implemented Methods #############

    async def me(self) -> SavedTracks:
        return await self._get("me")
    
    async def track(self, track: str) -> Track:
        return await self._get(f"tracks/{track}")

    ################## Spotipy Methods ####################

    async def playlist(self, playlist_id: str) -> Playlist:
        pl_id = self.temp_spotipy._get_id("artist", playlist_id)

        async def cache_update_function() -> Playlist:
            return sp_fetch(self.temp_spotipy.playlist, Playlist, pl_id)
        
        cache_response: Artist = await redis_client.cache_query(cache_key=f"playlist_{pl_id}", 
                                        class_type=Playlist, 
                                        cache_update_function=cache_update_function, 
                                        expiry=100)

        return cache_response
    
    async def artist_related_artists(self, artist: str, invalidate_cache=False) -> List[Artist]:

        async def related_artists() -> SeveralArtists:
            return sp_fetch(self.temp_spotipy.artist_related_artists, SeveralArtists, artist)
        
        if invalidate_cache:
            self.redis.delete(f"artist_related_{artist}")

        cache_respnse = await redis_client.cache_query(cache_key=f"artist_related_{artist}", 
                                          cache_update_function=related_artists, 
                                          expiry=3600, 
                                          class_type=SeveralArtists)
        return cache_respnse.artists
    

    async def artist(self, artist_id: str) -> Artist:
        art_id = self.temp_spotipy._get_id("artist", artist_id)

        async def cache_update_function() -> Artist:
            return sp_fetch(self.temp_spotipy.artist, Artist, art_id)
        
        cache_response: Artist = await redis_client.cache_query(cache_key=f"artist_{art_id}", 
                                        class_type=Artist, 
                                        cache_update_function=cache_update_function, 
                                        expiry=100)
        return cache_response


    async def artist_albums(self, artist_id: str, album_type: str):

        return sp_fetch(self.temp_spotipy.artist_albums, ArtistAlbums, artist_id,
                        album_type=album_type)
    
    async def albums(self, albums) -> SeveralAlbums:
        sp_fetch(self.temp_spotipy.albums, SeveralAlbums, albums)
    
    async def tracks(self, tracks) -> SeveralTracks:
        sp_fetch(self.temp_spotipy.tracks, SeveralTracks, tracks)

    async def user_playlist_create(self, user:str , name:str, public: bool):
        return self.temp_spotipy.user_playlist_create(user=user, name=name, public=public)

    async def playlist_add_items(self, playlist_id: str, tracks) -> None:
        self.temp_spotipy.playlist_add_items(playlist_id, tracks)

    async def current_user_unfollow_playlist(self, playlist_uri) -> None:
        self.temp_spotipy.current_user_unfollow_playlist(playlist_uri)

    async def reccomendations(self, limit, seed_artists=None,seed_genres=None,seed_tracks=None,country=None, track_list=True) -> Recc:

        reccs:  Recc = sp_fetch(self.temp_spotipy.recommendations, 
                              Recc, 
                              limit=limit, 
                              seed_tracks=seed_tracks, 
                              seed_artists=seed_artists, seed_genres=seed_genres)
        if track_list:
            return reccs.tracks
    
        return reccs 

    ################### BATCHING METHODS ############################
        
    async def current_user_saved_tracks(self,limit: int = None, 
                                        offset: int = None, batch=False,  chunk_size = 25, invalidate_cache=False, track_list=True) -> List[SavedTrack] | SavedTracks:
        if not batch:
            return await self._get(f"me/tracks?offset={offset}&limit={limit}")
        
        async def batch_request() -> List[SavedTrack]:
            initial_item = await self._get(f"me/tracks?offset={0}&limit={50}", response_type=SavedTracks)
            return await self._batch_request(ep_path="me/tracks", 
                                        initial_item=initial_item,
                                            sp_type=SavedTracks,
                                            chunk_size=chunk_size)
        if invalidate_cache:
            self.redis.delete("my_tracks")


        saved_tracks: List[SavedTrack] = await redis_client.cache_query(cache_key="my_tracks", 
                                          cache_update_function=batch_request, 
                                          expiry=3600, 
                                          class_type=SavedTrack)
        if track_list:
            tracks: List[Track] = []
            for item in saved_tracks:
                tracks.append(item.track)
            return tracks

        return await saved_tracks
    
    async def current_user_saved_playlists(self,limit: int = None, 
                                        offset: int = None,
                                          batch=False,
                                          chunk_size=25, invalidate_cache=False) -> List[SimplifiedPlaylistObject] | UserPlaylists:
        
        cache_key = "my_playlists_new_cache"
        ep = "me/playlists"
        
        if not batch:
            return await self._get(f"{ep}?offset={offset}&limit={limit}", response_type=UserPlaylists)
        
        async def batch_request() -> List[SimplifiedPlaylistObject]:
            initial_item = await self._get(f"{ep}?offset={0}&limit={50}", response_type=UserPlaylists)
            return await self._batch_request(ep_path=ep, 
                                        initial_item=initial_item,
                                            sp_type=UserPlaylists,
                                            chunk_size=chunk_size)
        if invalidate_cache:
            self.redis.delete(cache_key)

        print("############ QUERYING CACHE ###################")
        return await redis_client.cache_query(cache_key=cache_key, 
                                          cache_update_function=batch_request, 
                                          expiry=3600, 
                                          class_type=SimplifiedPlaylistObject)

    async def playlist_tracks(self, playlist_id, limit: int = None, 
                                        offset: int = None,
                                          batch=False,
                                          chunk_size=25, invalidate_cache=False, track_list=True) -> List[PlaylistTrack] | List[Track] | PlaylistTracks:
        if not batch:
            return await self._get(f"playlists/{playlist_id}/tracks?offset={offset}&limit={limit}", response_type=PlaylistTracks)
        
        async def batch_request() -> List[PlaylistTrack]:
            initial_item = await self._get(f"playlists/{playlist_id}/tracks?offset={0}&limit={50}", response_type=PlaylistTracks)
            return await self._batch_request(ep_path=f"playlists/{playlist_id}/tracks", 
                                        initial_item=initial_item,
                                            sp_type=PlaylistTracks,
                                            chunk_size=chunk_size)
        if invalidate_cache:
            self.redis.delete(f"playlist_tracks_{playlist_id}")

        playlist_tracks: List[PlaylistTrack] = await redis_client.cache_query(cache_key=f"playlist_tracks_{playlist_id}", 
                                          cache_update_function=batch_request, 
                                          expiry=3600, 
                                          class_type=PlaylistTrack)
        if track_list:
            tracks: List[Track] = []
            for item in playlist_tracks:
                tracks.append(item.track)
            return tracks
        
        return playlist_tracks