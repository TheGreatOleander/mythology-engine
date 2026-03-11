import shutil
import subprocess
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
            "capabilities": ["tts_narration", "voice_render"]
        }

    def build_command(self, text, output_path):
        return [
            self.binary,
            "--model", self.model_path,
            "--output_file", str(output_path)
        ], text

    def synthesize(self, text, output_path="examples/releases/output/narration.wav"):
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        result = {
            "provider": self.name,
            "output_path": str(out),
            "executed": False,
            "returncode": None,
            "mode": "placeholder"
        }

        found = shutil.which(self.binary)
        if found is not None:
            cmd, stdin_text = self.build_command(text, out)
            try:
                proc = subprocess.run(
                    cmd,
                    input=stdin_text,
                    capture_output=True,
                    text=True
                )
                result["executed"] = True
                result["returncode"] = proc.returncode
                result["stdout"] = proc.stdout[-1000:]
                result["stderr"] = proc.stderr[-2000:]
                result["mode"] = "provider_exec"
            except Exception as e:
                result["error"] = str(e)

        if not out.exists():
            out.write_text(
                "PIPER PLACEHOLDER\n\n" + text,
                encoding="utf-8"
            )

        return result
