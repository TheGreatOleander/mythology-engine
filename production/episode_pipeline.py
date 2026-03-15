import subprocess
import sys
import wave
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

    def _log(self, message: str):
        print(message, file=sys.stderr)

    def _render_image(self, title: str, subtitle: str, topic: str, output_path: str):
        self._log(f"[EpisodePipeline] Rendering image -> {output_path}")

        if self.image_provider and hasattr(self.image_provider, "render"):
            result = self.image_provider.render(
                title=title,
                subtitle=subtitle,
                output_path=output_path
            )
            self._log(f"[EpisodePipeline] Image render result: {result}")
            return result

        if self.image_provider and hasattr(self.image_provider, "generate_image"):
            result = self.image_provider.generate_image(
                prompt=f"{title} -- {subtitle} -- documentary title card for {topic}",
                output_path=output_path
            )
            self._log(f"[EpisodePipeline] Image generate result: {result}")
            return result

        fallback = TitleCardProvider()
        result = fallback.render(
            title=title,
            subtitle=subtitle,
            output_path=output_path
        )
        self._log(f"[EpisodePipeline] Fallback image render result: {result}")
        return result

    def _build_scene_video(self, scene_images, output_video: Path):
        self._log(f"[EpisodePipeline] Building silent scene video -> {output_video}")
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

            self._log(f"[EpisodePipeline] Scene clip command: {' '.join(cmd)}")
            proc = subprocess.run(cmd, check=False)
            self._log(f"[EpisodePipeline] Scene clip returncode: {proc.returncode}")
            clips.append(clip)

        concat_file = output_video.parent / "concat.txt"

        with open(concat_file, "w", encoding="utf-8") as f:
            for clip in clips:
                f.write(f"file '{clip.resolve()}'\n")

        cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", str(concat_file),
            "-c", "copy",
            str(output_video)
        ]

        self._log(f"[EpisodePipeline] Concat command: {' '.join(cmd)}")
        proc = subprocess.run(cmd, check=False)
        self._log(f"[EpisodePipeline] Concat returncode: {proc.returncode}")
        self._log(f"[EpisodePipeline] Silent video exists: {output_video.exists()}")

    def _is_valid_wav(self, audio_path: Path) -> bool:
        if not audio_path.exists() or not audio_path.is_file():
            return False
        try:
            with wave.open(str(audio_path), "rb") as wf:
                return wf.getnchannels() > 0 and wf.getframerate() > 0
        except Exception:
            return False

    def _mux_audio_video(self, video_path: Path, audio_path: Path, output_path: Path):
        self._log(f"[EpisodePipeline] Muxing audio + video -> {output_path}")
        self._log(f"[EpisodePipeline] Video exists: {video_path.exists()} ({video_path})")
        self._log(f"[EpisodePipeline] Audio exists: {audio_path.exists()} ({audio_path})")

        if video_path.exists():
            self._log(f"[EpisodePipeline] Video size: {video_path.stat().st_size}")
        if audio_path.exists():
            self._log(f"[EpisodePipeline] Audio size: {audio_path.stat().st_size}")

        if not video_path.exists():
            self._log("[EpisodePipeline] Missing silent video for mux.")
            return {
                "command": ["ffmpeg", "mux-audio-video"],
                "output_path": str(output_path),
                "executed": False,
                "returncode": 1,
                "mode": "missing_video",
            }

        if not self._is_valid_wav(audio_path):
            self._log("[EpisodePipeline] narration.wav is not a valid WAV. Skipping mux.")
            return {
                "command": ["ffmpeg", "mux-audio-video"],
                "output_path": str(output_path),
                "executed": False,
                "returncode": 1,
                "mode": "invalid_audio",
            }

        cmd = [
            "ffmpeg",
            "-y",
            "-i", str(video_path),
            "-i", str(audio_path),
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            str(output_path)
        ]

        self._log(f"[EpisodePipeline] Mux command: {' '.join(cmd)}")
        proc = subprocess.run(cmd, check=False)
        self._log(f"[EpisodePipeline] Mux returncode: {proc.returncode}")
        self._log(f"[EpisodePipeline] Final video exists: {output_path.exists()}")

        return {
            "command": cmd,
            "output_path": str(output_path),
            "executed": output_path.exists() and proc.returncode == 0,
            "returncode": proc.returncode,
            "mode": "muxed" if output_path.exists() and proc.returncode == 0 else "failed",
        }

    def run(self, topic="The Origin of the Impossible Map"):
        output_root = Path("examples/releases/output")
        output_root.mkdir(parents=True, exist_ok=True)

        self._log(f"[EpisodePipeline] Output root: {output_root}")

        script_text = (
            f"Tonight we investigate {topic}. "
            "Researchers recently uncovered evidence that challenges known exploration routes."
        )

        self._log(f"[EpisodePipeline] Script text: {script_text}")

        title = self.title_engine.generate(topic)[0]
        self._log(f"[EpisodePipeline] Title result: {title}")

        image_result = self._render_image(
            title=title["title"],
            subtitle=title["hook"],
            topic=topic,
            output_path=str(output_root / "episode_frame.png")
        )

        scene_subtitles = {
            1: "Discovery of the Map",
            2: "The Impossible Contradiction",
            3: "The Historian's Revelation",
        }

        scene_images = []
        scene_results = []

        for i in range(1, 4):
            scene_path = output_root / f"scene_{i:02}.png"

            scene_result = self._render_image(
                title=title["title"],
                subtitle=scene_subtitles[i],
                topic=topic,
                output_path=str(scene_path)
            )

            scene_images.append(scene_path)
            scene_results.append(scene_result)

        audio_path = output_root / "narration.wav"
        silent_video_path = output_root / "episode_silent.mp4"
        final_video_path = output_root / "episode.mp4"

        self._log(f"[EpisodePipeline] Synthesizing audio -> {audio_path}")
        audio_result = self.audio_provider.synthesize(
            text=script_text,
            output_path=str(audio_path)
        )
        self._log(f"[EpisodePipeline] Audio result: {audio_result}")
        self._log(f"[EpisodePipeline] Valid WAV: {self._is_valid_wav(audio_path)}")

        self._build_scene_video(
            scene_images=scene_images,
            output_video=silent_video_path
        )

        mux_result = self._mux_audio_video(
            video_path=silent_video_path,
            audio_path=audio_path,
            output_path=final_video_path
        )

        if mux_result["executed"]:
            video_result = mux_result
        else:
            video_result = {
                "command": ["ffmpeg", "concat-scene-build"],
                "output_path": str(silent_video_path),
                "executed": silent_video_path.exists(),
                "returncode": 0 if silent_video_path.exists() else 1,
                "mode": "scene_concat" if silent_video_path.exists() else mux_result["mode"],
            }

        self._log(f"[EpisodePipeline] Video result: {video_result}")

        thumbnail = self.thumbnail_engine.generate(title["title"], topic)
        self._log(f"[EpisodePipeline] Thumbnail result: {thumbnail}")

        release = self.release_builder.build(
            title=title["title"],
            description=f"A documentary investigation into {topic}.",
            video=video_result["output_path"],
            thumbnail=thumbnail,
            captions=str(output_root / "captions.srt")
        )

        self._log(f"[EpisodePipeline] Release package: {release}")

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
