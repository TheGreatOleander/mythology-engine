# Image Provider

v1.6 introduces the first functional image provider scaffold.

Command:

    mythology --mode manual --action image-test

Behavior:

1. If an SDXL API is configured the engine attempts a real image generation call.
2. If no API is configured the system writes a placeholder artifact.

This allows development to proceed without requiring GPU models locally.
