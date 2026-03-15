import shutil
import subprocess
import time
import wave
from pathlib import Path


class PiperProvider:
    name = "piper"

    def __init__(self, binary="piper", model_path="models/en_US-lessac-medium.onnx"):
        self.binary = binary
        self.model_path = model_path

    def status(self):
        found = shutil.which(self.binary)
        return {
            "provider": self.name,
            "ready": found is not None,
            "binary": found,
            "model_path": self.model_path,
            "capabilities": ["tts_narration", "voice_render"],
        }

    def build_command(self, text, output_path):
        return [
            self.binary,
            "--model", self.model_path,
            "--output_file", str(output_path),
        ], text

    def _is_valid_wav(self, path: Path) -> bool:
        if not path.exists() or not path.is_file():
            return False
        try:
            with wave.open(str(path), "rb") as wf:
                return wf.getnchannels() > 0 and wf.getframerate() > 0
        except Exception:
            return False

    def _synthesize_with_piper(self, text: str, out: Path):
        cmd, stdin_text = self.build_command(text, out)
        proc = subprocess.run(
            cmd,
            input=stdin_text,
            capture_output=True,
            text=True,
            check=False,
        )
        return {
            "provider": self.name,
            "output_path": str(out),
            "executed": True,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-1000:] if proc.stdout else "",
            "stderr": proc.stderr[-2000:] if proc.stderr else "",
            "mode": "provider_exec" if proc.returncode == 0 else "provider_failed",
        }

    def synthesize(self, text, output_path="examples/releases/output/narration.wav"):
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        if out.exists():
            try:
                out.unlink()
            except Exception:
                pass

        found = shutil.which(self.binary)

        result = {
            "provider": self.name,
            "output_path": str(out),
            "executed": False,
            "returncode": None,
            "mode": "audio_disabled",
            "valid_wav": False,
        }

        if found is None:
            return result

        try:
            result = self._synthesize_with_piper(text, out)
        except Exception as e:
            return {
                "provider": self.name,
                "output_path": str(out),
                "executed": False,
                "returncode": None,
                "mode": "provider_exception",
                "valid_wav": False,
                "error": str(e),
            }

        time.sleep(0.2)

        if self._is_valid_wav(out):
            result["mode"] = "provider_wav"
            result["valid_wav"] = True
            return result

        if out.exists():
            try:
                out.unlink()
            except Exception:
                pass

        result["mode"] = "provider_invalid_wav"
        result["valid_wav"] = False
        return result
