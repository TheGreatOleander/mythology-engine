from pathlib import Path
import json

DEFAULT_CONFIG = {
    "channel_name": "The Hidden Archive",
    "publish_mode": "manual_first",
    "video_provider": "ffmpeg",
    "audio_provider": "piper",
    "image_provider": "sdxl",
    "primary_platforms": ["youtube", "youtube_shorts", "tiktok", "instagram_reels", "podcast"]
}

DEFAULT_SECRETS = {
    "youtube_client_id": "YOUR_CLIENT_ID",
    "youtube_client_secret": "YOUR_CLIENT_SECRET",
    "tiktok_api_key": "YOUR_TIKTOK_KEY",
    "image_provider_key": "YOUR_IMAGE_PROVIDER_KEY",
    "audio_provider_key": "YOUR_AUDIO_PROVIDER_KEY"
}

def write_config_bundle(config_dir):
    config_dir = Path(config_dir)
    config_dir.mkdir(parents=True, exist_ok=True)

    config_path = config_dir / "studio_config.json"
    secrets_example_path = config_dir / "secrets.example.json"
    notes_path = config_dir / "BOOTSTRAP_NOTES.txt"

    config_path.write_text(json.dumps(DEFAULT_CONFIG, indent=2), encoding="utf-8")
    secrets_example_path.write_text(json.dumps(DEFAULT_SECRETS, indent=2), encoding="utf-8")
    notes_path.write_text(
        "MYTHOLOGY ENGINE BOOTSTRAP\n\n"
        "1. Review studio_config.json\n"
        "2. Copy secrets.example.json to a real secrets file kept out of version control\n"
        "3. Keep publish_mode=manual_first until providers are wired\n"
        "4. Use release_packages/ as the handoff boundary to future systems\n",
        encoding="utf-8"
    )

    return {
        "studio_config": str(config_path),
        "secrets_example": str(secrets_example_path),
        "notes": str(notes_path)
    }
