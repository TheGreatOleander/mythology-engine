# Audio Provider

Mythology Engine v1.8 upgrades the audio provider from a passive scaffold into
a real execution path attempt.

## Command

```bash
mythology --mode manual --action audio-test
```

## Behavior

1. Builds a real Piper command if `piper` is installed
2. Attempts execution using the configured model path
3. Captures stdout/stderr and return code
4. Falls back to a placeholder artifact if the provider is unavailable

## Why it matters

This gives the repo a second concrete execution limb and strengthens the episode pipeline.
