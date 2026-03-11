# Studio Layer

The Studio Layer is the operator interface for Mythology Engine.

## Main entrypoint

```bash
python runtime/run_studio.py --mode manual --action full-cycle
```

## Relationship to the core

- `core/` contains the narrative and production brain
- `studio/` contains the operator workflow, mode selection, and provider status logic
