class YouTubeAdapter:
    platform = "youtube"

    def build_payload(self, release_package):
        manifest = release_package.get("manifest", {})
        return {
            "platform": self.platform,
            "title": manifest.get("title"),
            "description": manifest.get("description"),
            "video": manifest.get("video"),
            "thumbnail": manifest.get("thumbnail"),
            "captions": manifest.get("captions"),
            "visibility": "private"
        }

    def simulate_upload(self, payload):
        return {
            "platform": self.platform,
            "status": "simulated",
            "video": payload.get("video"),
            "title": payload.get("title")
        }
