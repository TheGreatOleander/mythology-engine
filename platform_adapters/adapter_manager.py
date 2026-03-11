from platform_adapters.youtube.youtube_adapter import YouTubeAdapter
from platform_adapters.tiktok.tiktok_adapter import TikTokAdapter
from platform_adapters.instagram.instagram_adapter import InstagramReelsAdapter
from platform_adapters.podcast.podcast_adapter import PodcastAdapter

class PlatformAdapterManager:
    def __init__(self):
        self.adapters = {
            "youtube": YouTubeAdapter(),
            "tiktok": TikTokAdapter(),
            "instagram_reels": InstagramReelsAdapter(),
            "podcast": PodcastAdapter(),
        }

    def list_platforms(self):
        return list(self.adapters.keys())

    def build_all_payloads(self, release_package):
        return {
            name: adapter.build_payload(release_package)
            for name, adapter in self.adapters.items()
        }

    def simulate_all_uploads(self, release_package):
        payloads = self.build_all_payloads(release_package)
        return {
            name: self.adapters[name].simulate_upload(payload)
            for name, payload in payloads.items()
        }
