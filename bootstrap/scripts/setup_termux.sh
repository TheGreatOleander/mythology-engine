#!/data/data/com.termux/files/usr/bin/bash
set -e

pkg update -y
pkg upgrade -y
pkg install -y python git ffmpeg clang make cmake rust termux-tools

python -m pip install --upgrade pip wheel setuptools

echo ""
echo "Base bootstrap dependencies installed."
echo "Run next:"
echo "  python bootstrap/tools/run_bootstrap.py"
echo ""
