# Mythology Engine MASTER REPO

A consolidated standalone repo for the Mythology Engine core.

## Demo
```bash
python runtime/demo_cycle.py
```

## Repo boundary
This repo is the content studio core.

Future separate repos:
- Media PR Engine
- GestureFX Engine


## Studio Layer (v1.1)

The operator layer now lives **inside the same repo**.

Use it to run the engine in different modes:

```bash
python runtime/run_studio.py --mode manual --action full-cycle
python runtime/run_studio.py --mode assisted --action release-package
python runtime/run_studio.py --mode auto --action full-cycle --publish
```

### Run modes

- `manual` — AI prepares assets; human reviews and publishes
- `assisted` — AI prepares assets; human approves major steps
- `auto` — AI attempts end-to-end execution with wired providers

### Actions

- `full-cycle` — run the full production cycle
- `release-package` — build or inspect the release package
- `status` — inspect configuration and provider readiness


## CLI Command Layer (v1.2)

Mythology Engine now includes an installable command-line entrypoint.

### Install locally

```bash
python -m pip install -e .
```

### Use the command

```bash
mythology --mode manual --action full-cycle
mythology --mode manual --action status
mythology --mode assisted --action release-package
mythology --mode auto --action full-cycle --publish
```

### Shortcuts

A `Makefile` is included for convenience:

```bash
make install
make run
make status
make release
make demo
```


## Provider Wiring Layer (v1.3)

Mythology Engine now includes a more explicit provider wiring layer inside the same repo.

### Check provider status

```bash
mythology --mode manual --action providers
```

### Included provider scaffolds

- `ffmpeg` for video assembly
- `piper` for narration / TTS
- `sdxl` for image generation

### Why this matters

This is the step where the system starts moving from a pure framework toward a usable studio runtime.
It gives you a clean place to wire real providers without turning the repo into spaghetti.


## Bootstrap / Install Polish (v1.4)

Mythology Engine now includes a practical bootstrap layer for first-run setup.

### Bootstrap the environment

```bash
python bootstrap/tools/run_bootstrap.py
```

### Termux helper

```bash
bash bootstrap/scripts/setup_termux.sh
```

### What bootstrap does

- checks the environment
- creates runtime folders
- checks base provider readiness
- writes an initial config bundle

This is the step that makes the repo feel much more like a tool you can bring up intentionally instead of a box of sharp parts.\n

## First Real Provider Hookup (v1.5)

Mythology Engine now includes its first more concrete provider execution path.

### Test the FFmpeg provider

```bash
mythology --mode manual --action provider-test
```

This action:

- builds a real FFmpeg command
- attempts execution if FFmpeg is installed
- records command details and output
- falls back to a placeholder artifact if the environment is not ready

This is the first step from provider scaffolding into actual execution.


## Image Provider (v1.6)

The engine now supports a basic image generation provider.

Test:

    mythology --mode manual --action image-test

If an SDXL API is configured a real generation request will be attempted.
Otherwise a placeholder artifact is created so the pipeline continues.


## First True Episode Pipeline (v1.7)

The engine now includes a chained episode pipeline that links image, audio, video,
title, thumbnail, and release-package generation.

### Test the pipeline

```bash
mythology --mode manual --action episode-test
```

### What it does

- generates an image artifact
- generates a narration artifact
- attempts a video artifact
- creates a title
- creates a thumbnail
- builds a release package

This is the first true multi-provider episode path inside the repo.


## Real Audio Provider Execution (v1.8)

The engine now upgrades its audio path from a pure placeholder to a real local execution attempt.

### Test the audio provider

```bash
mythology --mode manual --action audio-test
```

This action:

- builds a real Piper command
- attempts local narration generation if Piper is installed
- captures command output and return code
- falls back to a placeholder narration artifact if the environment is not ready


## Release Review + Publish Layer (v1.9)

Two new commands:

    mythology --action review-release
    mythology --action publish-sim

review-release:
    Inspects artifacts created by the episode pipeline.

publish-sim:
    Builds a publish payload and simulates sending content to platforms.

This prepares the engine for real YouTube / TikTok publishing adapters.


## Platform Adapter Layer (v2.0)

The engine now includes platform-specific adapter scaffolds for:

- YouTube
- TikTok
- Instagram Reels
- Podcast

### Commands

```bash
mythology --action platforms
mythology --action publish-sim
```

### Added pieces

- platform adapter manager
- OAuth scaffold
- scheduler scaffold
- channel brain scaffold

This is the threshold where Mythology Engine starts behaving like a platform runtime.
