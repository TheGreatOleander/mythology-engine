# First Real Provider Hookup

Mythology Engine v1.5 upgrades the FFmpeg provider from a passive scaffold
into a real command builder and execution path.

## Command

```bash
mythology --mode manual --action provider-test
```

## What it does

- builds a real FFmpeg command
- attempts execution if FFmpeg is installed
- captures stdout/stderr
- writes a fallback placeholder artifact if execution cannot complete

## Why it matters

This is the first point where a provider stops merely describing itself and
starts attempting real work.
