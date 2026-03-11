# First True Episode Pipeline

Mythology Engine v1.7 introduces the first true end-to-end episode pipeline.

## Command

```bash
mythology --mode manual --action episode-test
```

## Flow

1. Generate image artifact
2. Generate narration artifact
3. Build video artifact
4. Generate title
5. Generate thumbnail
6. Build release package

## Why it matters

This is the first point where multiple providers are chained into a single content-production path.
