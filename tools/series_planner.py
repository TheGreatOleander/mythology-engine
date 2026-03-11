import json
from pathlib import Path

SERIES_PATH = Path("configs/series.json")
STATE_PATH = Path("configs/series_state.json")

def _load(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))

def _save(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")

def get_next_episode(advance=False):
    series = _load(SERIES_PATH, {"series_title": "Untitled", "episodes": []})
    state = _load(STATE_PATH, {"series_title": series.get("series_title", "Untitled"), "next_episode_index": 0})
    episodes = series.get("episodes", [])
    if not episodes:
        return {"series_title": series.get("series_title", "Untitled"), "episode_index": None, "topic": "Untitled Episode"}
    idx = max(0, min(int(state.get("next_episode_index", 0)), len(episodes)-1))
    result = {"series_title": series.get("series_title", "Untitled"), "episode_index": idx, "topic": episodes[idx]}
    if advance:
        state["next_episode_index"] = min(idx + 1, len(episodes)-1)
        _save(STATE_PATH, state)
    return result

if __name__ == "__main__":
    print(json.dumps(get_next_episode(False), indent=2))
