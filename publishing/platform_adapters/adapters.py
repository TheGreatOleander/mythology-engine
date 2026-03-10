def build_platform_packages(story):
    return {
        "youtube": {"platform": "youtube", "aspect_ratio": "16:9", "title": story["title"]},
        "tiktok": {"platform": "tiktok", "aspect_ratio": "9:16", "title": story["hook"]},
        "instagram_reels": {"platform": "instagram_reels", "aspect_ratio": "9:16", "title": story["hook"]},
        "youtube_shorts": {"platform": "youtube_shorts", "aspect_ratio": "9:16", "title": story["hook"] + " | Shorts"},
        "podcast": {"platform": "podcast", "aspect_ratio": "audio_only", "title": story["title"]}
    }
