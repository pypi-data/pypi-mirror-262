from typing import List

# Internal
from shrillecho.spotify.client import SpotifyClient
from shrillecho.types.track_types import Track

class SpotifyTrack:


    @staticmethod
    def track_difference(track_list_A: List[Track], track_list_B: List[Track]) -> List[Track]:
        """
            Computes the difference between two lists of tracks.
        """
        metadata_dict: dict = {}
        for track_b in track_list_B:
            key = track_b.name
            if key not in metadata_dict:
                metadata_dict[key] = set()
            metadata_dict[key].add(track_b.external_ids.isrc)
        filtered_a = []
        for track_a in track_list_A:
            if any(track_a.external_ids.isrc in isrc for isrc in metadata_dict.values()):
                continue 
            if track_a.name not in metadata_dict:
                filtered_a.append(track_a)
        return filtered_a
    
    @staticmethod
    def fetch_track_uris(tracks: List[Track]) -> List[str]:
        """
            Given a list of tracks return a list of the uris only
        """
        return [track.uri for track in tracks]
    
    @staticmethod
    async def track_difference_liked(sp: SpotifyClient, playlist_tracks: List[Track]) -> List[Track]:
        
        liked_tracks: List[Track] = await sp.current_user_saved_tracks(batch=True, chunk_size=10)
        
        filtered_tracks: List[Track] = SpotifyTrack.track_difference(playlist_tracks, liked_tracks)

        return filtered_tracks
    