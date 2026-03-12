import subprocess
import sys
from pathlib import Path


class FFmpegProvider:
    PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"

    def _is_real_png(self, image_path: Path) -> bool:
        if not image_path.exists() or not image_path.is_file():
            return False

        try:
            with image_path.open("rb") as f:
                sig = f.read(8)
            return sig == self.PNG_SIGNATURE
        except OSError:
            return False

    def render_still_video(self, image_path: str, output_path: str, duration: int = 5):
        image_path_obj = Path(image_path)
        output_path_obj = Path(output_path)

        if not image_path_obj.exists():
            print("Image missing — skipping ffmpeg render.", file=sys.stderr)
            return {
                "command": None,
                "output_path": str(output_path_obj),
                "executed": False,
                "returncode": None,
                "mode": "placeholder_missing_image",
            }

        if not self._is_real_png(image_path_obj):
            print("Image is not a real PNG — skipping ffmpeg render.", file=sys.stderr)
            print(f"Path: {image_path_obj}", file=sys.stderr)
            return {
                "command": None,
                "output_path": str(output_path_obj),
                "executed": False,
                "returncode": None,
                "mode": "placeholder_invalid_png",
            }

        cmd = [
            "ffmpeg",
            "-y",
            "-loop",
            "1",
            "-i",
            str(image_path_obj),
            "-t",
            str(duration),
            "-c:v",
            "libx264",
            "-pix_fmt",
            "yuv420p",
            str(output_path_obj),
        ]

        print("Running ffmpeg render...", file=sys.stderr)
        print("Command:", file=sys.stderr)
        print(" ".join(cmd), file=sys.stderr)
        print("This may take a moment.", file=sys.stderr)
        print("", file=sys.stderr)

        try:
            proc = subprocess.run(cmd, text=True)
        except KeyboardInterrupt:
            print("\nffmpeg render interrupted by user.", file=sys.stderr)
            return {
                "command": cmd,
                "output_path": str(output_path_obj),
                "executed": False,
                "returncode": None,
                "mode": "interrupted",
            }

        return {
            "command": cmd,
            "output_path": str(output_path_obj),
            "executed": proc.returncode == 0,
            "returncode": proc.returncode,
            "mode": "ffmpeg" if proc.returncode == 0 else "failed",
        }
