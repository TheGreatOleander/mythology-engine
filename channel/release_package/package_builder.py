from pathlib import Path
import json
class ReleasePackageBuilder:
    def build(self, title, description, video, thumbnail, captions):
        root = Path("examples/releases")
        root.mkdir(parents=True, exist_ok=True)
        (root / "teaser_clips").mkdir(parents=True, exist_ok=True)
        (root / "social_images").mkdir(parents=True, exist_ok=True)
        (root / "title.txt").write_text(title, encoding="utf-8")
        (root / "description.txt").write_text(description, encoding="utf-8")
        (root / "transcript.txt").write_text("Transcript placeholder", encoding="utf-8")
        for i in range(1,4):
            (root / "teaser_clips" / f"teaser_clip_{i:02}.mp4").write_text(f"TEASER {i}", encoding="utf-8")
            (root / "social_images" / f"social_card_{i:02}.png").write_text(f"SOCIAL CARD {i}", encoding="utf-8")
        manifest = {"title":title,"description":description,"video":video,"thumbnail":thumbnail,"captions":captions}
        (root / "metadata.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
        return {"package_dir": str(root), "manifest": manifest}
