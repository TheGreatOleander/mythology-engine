import shutil

def run_provider_check():
    return {
        "ffmpeg_ready": shutil.which("ffmpeg") is not None,
        "piper_ready": shutil.which("piper") is not None,
        "python_ready": shutil.which("python") is not None,
        "git_ready": shutil.which("git") is not None
    }
