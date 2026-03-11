import os
import platform
import shutil
import sys

def run_environment_check():
    return {
        "platform": platform.platform(),
        "python_version": sys.version.split()[0],
        "is_termux_like": "ANDROID_ROOT" in os.environ or "com.termux" in os.environ.get("PREFIX", ""),
        "binaries": {
            "python": shutil.which("python"),
            "ffmpeg": shutil.which("ffmpeg"),
            "git": shutil.which("git"),
            "bash": shutil.which("bash"),
            "pkg": shutil.which("pkg")
        }
    }
