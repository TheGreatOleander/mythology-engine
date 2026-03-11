from pathlib import Path
import os

def build_paths():
    home = Path(os.environ.get("HOME", "."))
    base = home / "MythologyStudio"
    paths = {
        "base_dir": str(base),
        "projects_dir": str(base / "projects"),
        "output_dir": str(base / "output"),
        "models_dir": str(base / "models"),
        "cache_dir": str(base / "cache"),
        "logs_dir": str(base / "logs"),
        "config_dir": str(base / "config"),
        "release_dir": str(base / "release_packages")
    }
    for p in paths.values():
        Path(p).mkdir(parents=True, exist_ok=True)
    return paths
