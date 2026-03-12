import subprocess
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
        if self.image_provider and hasattr(self.image_provider, "render"):
            return self.image_provider.render(
                title=title,
                subtitle=subtitle,
                output_path=output_path
            )

        if self.image_provider and hasattr(self.image_provider, "generate_image"):
            return self.image_provider.generate_image(
                prompt=f"{title} -- {subtitle} -- documentary title card for {topic}",
                output_path=output_path
            )

        fallback = TitleCardProvider()
        return fallback.render(
            title=title,
            subtitle=subtitle,
            output_path=output_path
        )

    def _build_scene_video(self, scene_images, output_video: Path):
        clips = []

        for img in scene_images:
            clip = img.with_suffix(".mp4")

            cmd = [
                "ffmpeg",
                "-y",
                "-loop", "1",
                "-i", str(img),
                "-t", "4",
                "-vf", "scale=1280:720",
                "-pix_fmt", "yuv420p",
                str(clip)
            ]

            subprocess.run(
                cmd,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False
            )

            clips.append(clip)

        concat_file = output_video.parent / "concat.txt"

        with open(concat_file, "w", encoding="utf-8") as f:
            for clip in clips:
                f.write(f"file '{clip.resolve()}'\n")

        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", str(concat_file),
                "-c", "copy",
                str(output_video)
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False
        )

    def run(self, topic="The Origin of the Impossible Map"):
        output_root = Path("examples/releases/output")
        output_root.mkdir(parents=True, exist_ok=True)

        script_text = (
            f"Tonight we investigate {topic}. "
            "Researchers recently uncovered evidence that challenges known exploration routes."
        )

        title = self.title_engine.generate(topic)[0]

        # Main frame for thumbnail/upstream export
        image_result = self._render_image(
            title=title["title"],
            subtitle=title["hook"],
            topic=topic,
            output_path=str(output_root / "episode_frame.png")
        )

        # Multi-scene frames for longer video
        scene_images = []
        scene_results = []

        for i in range(1, 4):
            scene_path = output_root / f"scene_{i:02}.png"

            scene_result = self._render_image(
                title=title["title"],
                subtitle=f"Scene {i}",
                topic=topic,
                output_path=str(scene_path)
            )

            scene_images.append(scene_path)
            scene_results.append(scene_result)

        audio_result = self.audio_provider.synthesize(
            text=script_text,
            output_path=str(output_root / "narration.wav")
        )

        self._build_scene_video(
            scene_images=scene_images,
            output_video=output_root / "episode.mp4"
        )

        video_result = {
            "command": ["ffmpeg", "concat-scene-build"],
            "output_path": str(output_root / "episode.mp4"),
            "executed": (output_root / "episode.mp4").exists(),
            "returncode": 0 if (output_root / "episode.mp4").exists() else 1,
            "mode": "scene_concat" if (output_root / "episode.mp4").exists() else "failed",
        }

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
            "scene_results": scene_results,
            "audio_result": audio_result,
            "video_result": video_result,
            "title": title,
            "thumbnail": thumbnail,
            "release_package": release
        }
