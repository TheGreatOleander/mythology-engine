from publishing.provider_layer.provider_manager import ProviderManager

def profile_or_default(profile: dict, key: str, default):
    return profile.get(key, default)

class ProviderRegistry:
    def __init__(self, profile: dict, secrets: dict):
        self.profile = profile
        self.secrets = secrets
        self.manager = ProviderManager()

    def status(self) -> dict:
        return {
            "selected": {
                "video_provider": profile_or_default(self.profile, "video_provider", "ffmpeg"),
                "audio_provider": profile_or_default(self.profile, "audio_provider", "piper"),
                "image_provider": profile_or_default(self.profile, "image_provider", "sdxl"),
                "publish_mode": profile_or_default(self.profile, "publish_mode", "manual_first"),
                "secrets_loaded": bool(self.secrets)
            },
            "available": self.manager.status()
        }
