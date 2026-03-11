import json
from pathlib import Path
from tools.series_planner import get_next_episode

def main():
    selection = get_next_episode(advance=False)
    Path("series_selection.json").write_text(json.dumps(selection, indent=2), encoding="utf-8")
    print(json.dumps(selection, indent=2))

if __name__ == "__main__":
    main()
