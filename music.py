import requests
import time
import requests_cache
from typing import List, Dict, Any

requests_cache.install_cache("deezer_cache", expire_after=86400)

class DeezerAPI:
    BASE_URL = "https://api.deezer.com"

    def __init__(self, delay_between_requests: float = 0.1):
        self.delay = delay_between_requests

    def _get(self, endpoint: str, params: dict = {}) -> Dict[str, Any]:
        """Generic GET request with rate limiting and error handling."""
        time.sleep(self.delay)
        try:
            response = requests.get(f"{self.BASE_URL}/{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching '{endpoint}': {e}")
            return {}

    def get_top_tracks(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get("chart/0/tracks", {"limit": limit}).get("data", [])

    def get_top_albums(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get("chart/0/albums", {"limit": limit}).get("data", [])

    def get_top_artists(self, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get("chart/0/artists", {"limit": limit}).get("data", [])

    def get_artist(self, artist_id: int) -> Dict[str, Any]:
        """Get full artist details (may include genres, fans, etc.)"""
        return self._get(f"artist/{artist_id}")

    def get_artist_top_tracks(self, artist_id: int, limit: int = 1) -> List[Dict[str, Any]]:
        return self._get(f"artist/{artist_id}/top", {"limit": limit}).get("data", [])

    def get_artist_albums(self, artist_id: int, limit: int = 10) -> List[Dict[str, Any]]:
        return self._get(f"artist/{artist_id}/albums", {"limit": limit}).get("data", [])

    def get_album(self, album_id: int) -> Dict[str, Any]:
        return self._get(f"album/{album_id}")

    def get_track(self, track_id: int) -> Dict[str, Any]:
        return self._get(f"track/{track_id}")

    def search_track(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self._get("search/track", {"q": query, "limit": limit}).get("data", [])

    def search_artist(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self._get("search/artist", {"q": query, "limit": limit}).get("data", [])

    def search_album(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        return self._get("search/album", {"q": query, "limit": limit}).get("data", [])
