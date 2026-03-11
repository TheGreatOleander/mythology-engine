#!/data/data/com.termux/files/usr/bin/bash
set -e

export PYTHONUNBUFFERED=1
export TMPDIR="${TMPDIR:-$HOME/.tmp}"
mkdir -p "$TMPDIR"
mkdir -p "$HOME/MythologyStudio/logs"

python "$@" 2>&1 | tee "$HOME/MythologyStudio/logs/bootstrap_last_run.log"
