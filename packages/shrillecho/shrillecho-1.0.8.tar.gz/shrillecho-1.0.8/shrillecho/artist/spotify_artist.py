import spotipy
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.album_types import ArtistAlbums, SeveralAlbums
from shrillecho.types.artist_types import Artist, SeveralArtists
from shrillecho.types.track_types import SeveralTracks, Track
from shrillecho.utility.general_utility import sp_fetch
from typing import List

class SpotifyArtist:

    @staticmethod
    def get_artist_tracks(sp: SpotifyClient, artist_id: str) -> List[Track]:
        
        """ Given an artist id, return all their songs 

            TODO:
                - Consider removing duplicate using ISRC set
        """
     
        artist_albums: ArtistAlbums = sp.artist_albums(artist_id=artist_id, album_type='album,single')

        tracks_to_fetch = set()
        albums_to_fetch = set()

        for album in artist_albums.items:
            albums_to_fetch.add(album.id)

        chunk_size = 50  
        for i in range(0, len(albums_to_fetch), chunk_size):
            chunk = list(albums_to_fetch)[i:i + chunk_size]
            several_albums: SeveralAlbums = sp.albums(chunk)
            for album in several_albums.albums:
                for track in album.tracks.items:
                    tracks_to_fetch.add(track.id)

        all_fetched_tracks = []
        for i in range(0, len(tracks_to_fetch), chunk_size):
            chunk = list(tracks_to_fetch)[i:i + chunk_size]
            tracks: SeveralTracks = sp.tracks(chunk)
            all_fetched_tracks.extend(tracks.tracks)

        return all_fetched_tracks