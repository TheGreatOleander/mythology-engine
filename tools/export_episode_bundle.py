import json
from pathlib import Path

ENGINE_OUTPUT = Path("engine_last_run.json")
OUTDIR = Path("/sdcard/mythology-engine/output/episode_bundle")

def main():
    if not ENGINE_OUTPUT.exists():
        print("engine_last_run.json not found")
        return
    data = json.loads(ENGINE_OUTPUT.read_text(encoding="utf-8"))
    episode = data["episode_result"]
    OUTDIR.mkdir(parents=True, exist_ok=True)

    (OUTDIR / "script.txt").write_text(episode["script_text"], encoding="utf-8")

    bundle = {
        "bundle_version": "1.0",
        "project": "mythology-engine",
        "episode_id": "engine_run",
        "title": episode["title"]["title"],
        "topic": episode["topic"],
        "paths": {
            "script": "script.txt",
            "metadata": "metadata.json",
            "scene_prompts": "scene_prompts.json",
            "episode_plan": "episode_plan.json"
        }
    }
    (OUTDIR / "bundle.json").write_text(json.dumps(bundle, indent=2), encoding="utf-8")

    metadata = {"series": "Mythology Engine", "tags": ["engine", "mythology", "story"], "tone": "documentary"}
    (OUTDIR / "metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    scenes = [
        {"scene_id": "scene_01", "prompt": "mysterious archival chamber, impossible map glowing on stone table", "narration": episode["script_text"][:120]},
        {"scene_id": "scene_02", "prompt": "close-up of parchment map with unknown sigils and weathered edges", "narration": "The object appears authentic, but nothing about it should exist."},
        {"scene_id": "scene_03", "prompt": "historian and cartographer studying impossible map under cinematic light", "narration": "Experts disagree about its origin, age, and purpose."}
    ]
    (OUTDIR / "scene_prompts.json").write_text(json.dumps(scenes, indent=2), encoding="utf-8")

    plan = {"hook": episode["title"]["hook"], "beats": ["hook", "investigation", "historical tension", "reveal"], "target_duration_sec": 180}
    (OUTDIR / "episode_plan.json").write_text(json.dumps(plan, indent=2), encoding="utf-8")
    print(f"episode_bundle exported to {OUTDIR}")

if __name__ == "__main__":
    main()
