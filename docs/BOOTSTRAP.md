# Bootstrap

Mythology Engine v1.4 adds a bootstrap layer for first-run setup and environment checks.

## Main command

```bash
python bootstrap/tools/run_bootstrap.py
```

## What it checks

- Python
- FFmpeg
- Git
- Piper (readiness check)
- Termux-like environment detection

## What it creates

- base runtime paths
- config directory
- release package directory
- starter config bundle
