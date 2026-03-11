import json
import os
from pathlib import Path
import urllib.request

class SDXLProvider:
    name = "sdxl"

    def __init__(self, api_url=None, api_key=None):
        self.api_url = api_url or os.environ.get("SDXL_API_URL")
        self.api_key = api_key or os.environ.get("SDXL_API_KEY")

    def status(self):
        return {
            "provider": self.name,
            "api_configured": bool(self.api_url),
            "key_present": bool(self.api_key),
            "capabilities": [
                "thumbnail_generation",
                "scene_generation",
                "social_card_generation"
            ]
        }

    def generate_image(self, prompt, output_path="examples/releases/output/generated_image.png"):
        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        # If API configured attempt request
        if self.api_url and self.api_key:
            payload = json.dumps({
                "prompt": prompt,
                "width": 1024,
                "height": 576
            }).encode()

            req = urllib.request.Request(
                self.api_url,
                data=payload,
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}"
                }
            )

            try:
                with urllib.request.urlopen(req, timeout=60) as resp:
                    data = resp.read()
                    out.write_bytes(data)
                    return {
                        "executed": True,
                        "output_path": str(out),
                        "mode": "api"
                    }
            except Exception as e:
                return {
                    "executed": False,
                    "error": str(e),
                    "fallback": True
                }

        # fallback placeholder
        out.write_text(
            "IMAGE GENERATION PLACEHOLDER\n"
            f"prompt={prompt}\n",
            encoding="utf-8"
        )

        return {
            "executed": False,
            "output_path": str(out),
            "mode": "placeholder"
        }
