import json
import shutil
from pathlib import Path

ENGINE_OUTPUT = Path("engine_last_run.json")
ENGINE_MEDIA_ROOT = Path("examples/releases/output")
OUTDIR = Path("/sdcard/mythology-engine/output/episode_bundle")


def copy_if_exists(src: Path, dst: Path):
    if src.exists() and src.is_file():
        shutil.copy(src, dst)
        return True
    return False


def main():
    if not ENGINE_OUTPUT.exists():
        print("engine_last_run.json not found")
        return

    data = json.loads(ENGINE_OUTPUT.read_text(encoding="utf-8"))
    episode = data["episode_result"]

    OUTDIR.mkdir(parents=True, exist_ok=True)

    # core text/script output
    (OUTDIR / "script.txt").write_text(episode["script_text"], encoding="utf-8")

    # copy real media artifacts if they exist
    copied_frame = copy_if_exists(
        ENGINE_MEDIA_ROOT / "episode_frame.png",
        OUTDIR / "episode_frame.png"
    )

    copied_video = copy_if_exists(
        ENGINE_MEDIA_ROOT / "episode.mp4",
        OUTDIR / "episode.mp4"
    )

    copied_audio = copy_if_exists(
        ENGINE_MEDIA_ROOT / "narration.wav",
        OUTDIR / "narration.wav"
    )

    bundle = {
        "bundle_version": "1.1",
        "project": "mythology-engine",
        "episode_id": "engine_run",
        "title": episode["title"]["title"],
        "topic": episode["topic"],
        "paths": {
            "script": "script.txt",
            "metadata": "metadata.json",
            "scene_prompts": "scene_prompts.json",
            "episode_plan": "episode_plan.json",
            "episode_frame": "episode_frame.png" if copied_frame else None,
            "episode_video": "episode.mp4" if copied_video else None,
            "narration": "narration.wav" if copied_audio else None,
        },
    }

    (OUTDIR / "bundle.json").write_text(
        json.dumps(bundle, indent=2),
        encoding="utf-8"
    )

    metadata = {
        "series": "Mythology Engine",
        "tags": ["engine", "mythology", "story"],
        "tone": "documentary",
        "has_real_frame": copied_frame,
        "has_real_video": copied_video,
        "has_real_audio": copied_audio,
    }

    (OUTDIR / "metadata.json").write_text(
        json.dumps(metadata, indent=2),
        encoding="utf-8"
    )

    scenes = [
        {
            "scene_id": "scene_01",
            "prompt": "mysterious archival chamber, impossible map glowing on stone table",
            "narration": episode["script_text"][:120],
        },
        {
            "scene_id": "scene_02",
            "prompt": "close-up of parchment map with unknown sigils and weathered edges",
            "narration": "The object appears authentic, but nothing about it should exist.",
        },
        {
            "scene_id": "scene_03",
            "prompt": "historian and cartographer studying impossible map under cinematic light",
            "narration": "Experts disagree about its origin, age, and purpose.",
        },
    ]

    (OUTDIR / "scene_prompts.json").write_text(
        json.dumps(scenes, indent=2),
        encoding="utf-8"
    )

    plan = {
        "hook": episode["title"]["hook"],
        "beats": ["hook", "investigation", "historical tension", "reveal"],
        "target_duration_sec": 180,
    }

    (OUTDIR / "episode_plan.json").write_text(
        json.dumps(plan, indent=2),
        encoding="utf-8"
    )

    print(f"episode_bundle exported to {OUTDIR}")
    print(f"  copied frame: {copied_frame}")
    print(f"  copied video: {copied_video}")
    print(f"  copied audio: {copied_audio}")


if __name__ == "__main__":
    main()
