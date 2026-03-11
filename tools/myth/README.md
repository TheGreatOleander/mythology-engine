# Myth CLI Menu

This package contains a simple interactive `myth` menu for Termux.

## Files
- `myth` - interactive studio menu
- `README.md`

## Recommended location
Put `myth` in:

`/sdcard/mythology-engine/tools/`

Then symlink it to:

`~/bin/myth`

## Example setup
```bash
mkdir -p /sdcard/mythology-engine/tools
cp myth /sdcard/mythology-engine/tools/myth
chmod +x /sdcard/mythology-engine/tools/myth
ln -s /sdcard/mythology-engine/tools/myth ~/bin/myth
```

## Requirements
These commands should already exist on your PATH:
- `myth-engine`
- `myth-forge`
- `myth-herald`
- `myth-run`
- `myth-run-video`
