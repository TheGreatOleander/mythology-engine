class TikTokAdapter:
    platform = "tiktok"

    def build_payload(self, release_package):
        manifest = release_package.get("manifest", {})
        return {
            "platform": self.platform,
            "caption": manifest.get("title"),
            "video": manifest.get("video"),
            "cover_image": manifest.get("thumbnail"),
            "visibility": "private"
        }

    def simulate_upload(self, payload):
        return {
            "platform": self.platform,
            "status": "simulated",
            "video": payload.get("video"),
            "caption": payload.get("caption")
        }
