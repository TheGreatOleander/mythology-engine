class OAuthManager:
    def __init__(self, secrets=None):
        self.secrets = secrets or {}

    def status(self):
        return {
            "youtube_configured": bool(self.secrets.get("youtube_client_id")),
            "tiktok_configured": bool(self.secrets.get("tiktok_api_key")),
            "instagram_configured": bool(self.secrets.get("instagram_app_id")),
            "mode": "scaffold"
        }
