class PodcastAdapter:
    platform = "podcast"

    def build_payload(self, release_package):
        manifest = release_package.get("manifest", {})
        return {
            "platform": self.platform,
            "title": manifest.get("title"),
            "description": manifest.get("description"),
            "audio_or_video": manifest.get("video"),
            "cover_art": manifest.get("thumbnail")
        }

    def simulate_upload(self, payload):
        return {
            "platform": self.platform,
            "status": "simulated",
            "asset": payload.get("audio_or_video"),
            "title": payload.get("title")
        }
