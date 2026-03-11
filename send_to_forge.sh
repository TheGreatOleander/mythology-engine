#!/data/data/com.termux/files/usr/bin/bash

SRC="/sdcard/mythology-engine/output/episode_bundle"
DST="/sdcard/mythology-forge/input/episode_bundle"

rm -rf "$DST"
mkdir -p "$DST"

cp -r "$SRC"/. "$DST"/

echo "Episode bundle sent to Forge"
