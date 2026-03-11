# Platform Adapters

v2.0 introduces platform adapter scaffolds for:

- YouTube
- TikTok
- Instagram Reels
- Podcast

## Commands

```bash
mythology --action platforms
mythology --action publish-sim
```

## What they do

- build platform-specific payloads from a release package
- simulate uploads
- expose an OAuth scaffold
- expose a scheduler scaffold
- expose a basic channel brain summary

## Why it matters

This is the threshold where Mythology Engine begins acting like a platform runtime, not just a studio.
