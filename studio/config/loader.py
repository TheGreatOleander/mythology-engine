import json
from pathlib import Path

def load_json(path: str) -> dict:
    p = Path(path)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

def load_profile(profile_path: str = 'configs/studio_profile.json') -> dict:
    return load_json(profile_path)

def load_secrets(secrets_path: str = 'configs/secrets.json') -> dict:
    return load_json(secrets_path)
