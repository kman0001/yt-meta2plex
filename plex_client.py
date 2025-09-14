import requests

class PlexClient:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.token = token

    def refresh_metadata(self, library_section="Videos"):
        url = f"{self.base_url}/library/sections/{library_section}/refresh?X-Plex-Token={self.token}"
        try:
            requests.get(url, timeout=5)
            print("[plex] metadata refresh triggered")
        except Exception as e:
            print("[plex] error refreshing metadata:", e)
