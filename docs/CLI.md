# CLI

Mythology Engine v1.2 adds a real command entrypoint.

## Install

```bash
python -m pip install -e .
```

## Commands

### Full cycle

```bash
mythology --mode manual --action full-cycle
```

### Status

```bash
mythology --mode manual --action status
```

### Release package

```bash
mythology --mode assisted --action release-package
```

### Auto publish attempt

```bash
mythology --mode auto --action full-cycle --publish
```
