# Providers

Mythology Engine v1.3 adds a provider wiring layer.

## Included scaffolds

- FFmpegProvider
- PiperProvider
- SDXLProvider
- ProviderManager

## Use

Inspect provider readiness:

```bash
mythology --mode manual --action providers
```

## Goal

Keep concrete integrations isolated from the narrative core and studio operator layer.
