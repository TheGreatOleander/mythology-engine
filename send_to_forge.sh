#!/data/data/com.termux/files/usr/bin/bash
set -e
SRC="/sdcard/mythology-engine/output/episode_bundle"
DST="/sdcard/mythology-forge/input/episode_bundle"
ARCHIVE_ROOT="/sdcard/mythology-engine/output_archive"
TIMESTAMP="$(date '+%Y%m%d_%H%M%S')"
ARCHIVE_DST="$ARCHIVE_ROOT/episode_bundle_$TIMESTAMP"
rm -rf "$DST"; mkdir -p "$DST"; cp -r "$SRC"/. "$DST"/
[ -f "$DST/bundle.json" ] || { echo "Handoff failed"; exit 1; }
mkdir -p "$ARCHIVE_ROOT" "$ARCHIVE_DST"
cp -r "$SRC"/. "$ARCHIVE_DST"/
rm -rf "$SRC"; mkdir -p "$SRC"; touch "$SRC/.gitkeep"
echo "Episode bundle sent to Forge"
echo "Archived to: $ARCHIVE_DST"
