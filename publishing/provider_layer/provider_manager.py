from publishing.provider_layer.video.ffmpeg_provider import FFmpegProvider
from publishing.provider_layer.audio.piper_provider import PiperProvider
from publishing.provider_layer.image.sdxl_provider import SDXLProvider

class ProviderManager:
    def __init__(self):
        self.video = FFmpegProvider()
        self.audio = PiperProvider()
        self.image = SDXLProvider()

    def status(self):
        return {
            "video": self.video.status(),
            "audio": self.audio.status(),
            "image": self.image.status()
        }
