from pathlib import Path

from publishing.provider_layer.image.title_card_provider import TitleCardProvider
from publishing.provider_layer.audio.piper_provider import PiperProvider
from publishing.provider_layer.video.ffmpeg_provider import FFmpegProvider

from channel.title_engine.title_engine import TitleEngine
from channel.thumbnail_engine.thumbnail_engine import ThumbnailEngine
from channel.release_package.package_builder import ReleasePackageBuilder


class EpisodePipeline:
    def __init__(self, image_provider=None, audio_provider=None, video_provider=None):
        self.image_provider = image_provider
        self.audio_provider = audio_provider or PiperProvider()
        self.video_provider = video_provider or FFmpegProvider()

        self.title_engine = TitleEngine()
        self.thumbnail_engine = ThumbnailEngine()
        self.release_builder = ReleasePackageBuilder()

    def _render_image(self, title: str, subtitle: str, topic: str, output_path: str):
        # Preferred path: providers that implement .render(...)
        if self.image_provider and hasattr(self.image_provider, "render"):
            return self.image_provider.render(
                title=title,
                subtitle=subtitle,
                output_path=output_path
            )

        # Compatibility path: older providers that implement .generate_image(...)
        if self.image_provider and hasattr(self.image_provider, "generate_image"):
            return self.image_provider.generate_image(
                prompt=f"{title} -- {subtitle} -- documentary title card for {topic}",
                output_path=output_path
            )

        # Safe fallback: always produce a real PNG locally
        fallback = TitleCardProvider()
        return fallback.render(
            title=title,
            subtitle=subtitle,
            output_path=output_path
        )

    def run(self, topic="The Origin of the Impossible Map"):
        output_root = Path("examples/releases/output")
        output_root.mkdir(parents=True, exist_ok=True)

        script_text = (
            f"Tonight we investigate {topic}. "
            "Researchers recently uncovered evidence that challenges known exploration routes."
        )

        title = self.title_engine.generate(topic)[0]

        image_result = self._render_image(
            title=title["title"],
            subtitle=title["hook"],
            topic=topic,
            output_path=str(output_root / "episode_frame.png")
        )

        audio_result = self.audio_provider.synthesize(
            text=script_text,
            output_path=str(output_root / "narration.wav")
        )

        video_result = self.video_provider.render_still_video(
            image_path=image_result["output_path"],
            output_path=str(output_root / "episode.mp4"),
            duration=5
        )

        thumbnail = self.thumbnail_engine.generate(title["title"], topic)

        release = self.release_builder.build(
            title=title["title"],
            description=f"A documentary investigation into {topic}.",
            video=video_result["output_path"],
            thumbnail=thumbnail,
            captions=str(output_root / "captions.srt")
        )

        return {
            "topic": topic,
            "script_text": script_text,
            "image_result": image_result,
            "audio_result": audio_result,
            "video_result": video_result,
            "title": title,
            "thumbnail": thumbnail,
            "release_package": release
        }
