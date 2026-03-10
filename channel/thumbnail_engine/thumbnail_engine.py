from pathlib import Path
class ThumbnailEngine:
    def generate(self, title, topic):
        out = Path("examples/releases/output/thumbnail.png")
        out.write_text(f"THUMBNAIL PLACEHOLDER\ntitle={title}\ntopic={topic}", encoding="utf-8")
        return str(out)
