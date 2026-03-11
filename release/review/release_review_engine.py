from pathlib import Path
import json

class ReleaseReviewEngine:

    def __init__(self, release_dir="examples/releases"):
        self.release_dir = Path(release_dir)

    def inspect(self):

        artifacts = {
            "video": list(self.release_dir.glob("**/*.mp4")),
            "audio": list(self.release_dir.glob("**/*.wav")),
            "images": list(self.release_dir.glob("**/*.png")),
            "thumbnails": list(self.release_dir.glob("**/*thumbnail*")),
            "metadata": list(self.release_dir.glob("**/*.json"))
        }

        summary = {
            k: [str(x) for x in v] for k, v in artifacts.items()
        }

        return {
            "release_dir": str(self.release_dir),
            "artifact_summary": summary,
            "counts": {k: len(v) for k, v in artifacts.items()}
        }
