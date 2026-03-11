import shutil
import subprocess
from pathlib import Path

class FFmpegProvider:
    name = "ffmpeg"

    def __init__(self, binary="ffmpeg"):
        self.binary = binary

    def status(self):
        found = shutil.which(self.binary)
        return {
            "provider": self.name,
            "ready": found is not None,
            "binary": found,
            "capabilities": ["assemble_video", "transcode", "subtitle_burnin", "audio_mux"]
        }

    def build_still_video_command(self, image_path, output_path, duration=5):
        return [
            self.binary,
            "-y",
            "-loop", "1",
            "-i", str(image_path),
            "-t", str(duration),
            "-c:v", "libx264",
            "-pix_fmt", "yuv420p",
            str(output_path)
        ]

    def render_still_video(self, image_path, output_path="examples/releases/output/assembled_video.mp4", duration=5):
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        cmd = self.build_still_video_command(image_path, out, duration=duration)
        result = {
            "command": cmd,
            "output_path": str(out),
            "executed": False,
            "returncode": None
        }

        if shutil.which(self.binary) is not None:
            proc = subprocess.run(cmd, capture_output=True, text=True)
            result["executed"] = True
            result["returncode"] = proc.returncode
            result["stdout"] = proc.stdout[-1000:]
            result["stderr"] = proc.stderr[-2000:]

        if not out.exists():
            out.write_text(
                "FFMPEG REAL HOOKUP PLACEHOLDER\n"
                f"source_image={image_path}\n"
                f"duration={duration}\n",
                encoding="utf-8"
            )

        return result
