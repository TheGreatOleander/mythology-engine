from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class TitleCardProvider:
    WIDTH = 1280
    HEIGHT = 720

    SCENE_COLORS = [
        (15, 15, 20),   # dark blue-black
        (35, 20, 10),   # sepia
        (10, 30, 25),   # green-black
        (30, 10, 35),   # violet-black
        (20, 20, 45),   # navy
    ]

    def _pick_bg(self, subtitle: str):
        subtitle_l = subtitle.lower()
        if "discovery" in subtitle_l:
            return self.SCENE_COLORS[0]
        if "contradiction" in subtitle_l:
            return self.SCENE_COLORS[1]
        if "revelation" in subtitle_l:
            return self.SCENE_COLORS[2]
        return self.SCENE_COLORS[4]

    def render(self, title: str, subtitle: str, output_path: str):
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        bg = self._pick_bg(subtitle)
        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), bg)
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
            sub_font = ImageFont.truetype("DejaVuSans.ttf", 36)
            small_font = ImageFont.truetype("DejaVuSans.ttf", 24)
        except Exception:
            title_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()
            small_font = ImageFont.load_default()

        draw.rectangle(
            [(40, 40), (self.WIDTH - 40, self.HEIGHT - 40)],
            outline=(180, 180, 180),
            width=3
        )

        subtitle_l = subtitle.lower()

        if "discovery" in subtitle_l:
            scene_label = "DISCOVERY"
            title_pos = (90, 180)
            sub_pos = (90, 300)
        elif "contradiction" in subtitle_l:
            scene_label = "CONTRADICTION"
            title_pos = (90, 260)
            sub_pos = (90, 380)
        elif "revelation" in subtitle_l:
            scene_label = "REVELATION"
            title_pos = (90, 340)
            sub_pos = (90, 460)
        else:
            scene_label = "MYTHOLOGY ENGINE"
            title_pos = (90, 240)
            sub_pos = (90, 360)

        draw.text(
            (90, 90),
            scene_label,
            font=small_font,
            fill=(210, 210, 210)
        )

        draw.text(
            title_pos,
            title,
            font=title_font,
            fill=(245, 245, 245)
        )

        draw.text(
            sub_pos,
            subtitle,
            font=sub_font,
            fill=(190, 190, 190)
        )

        img.save(output)

        return {
            "executed": True,
            "output_path": str(output),
            "mode": "title_card"
        }
