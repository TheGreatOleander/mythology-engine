from PIL import Image, ImageDraw, ImageFont
from pathlib import Path


class TitleCardProvider:

    WIDTH = 1280
    HEIGHT = 720

    def render(self, title: str, subtitle: str, output_path: str):

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        img = Image.new("RGB", (self.WIDTH, self.HEIGHT), (15, 15, 20))
        draw = ImageDraw.Draw(img)

        try:
            title_font = ImageFont.truetype("DejaVuSans-Bold.ttf", 64)
            sub_font = ImageFont.truetype("DejaVuSans.ttf", 36)
        except:
            title_font = ImageFont.load_default()
            sub_font = ImageFont.load_default()

        title_w, title_h = draw.textbbox((0,0), title, font=title_font)[2:]
        sub_w, sub_h = draw.textbbox((0,0), subtitle, font=sub_font)[2:]

        draw.text(
            ((self.WIDTH - title_w) / 2, self.HEIGHT / 2 - 80),
            title,
            font=title_font,
            fill=(240,240,240)
        )

        draw.text(
            ((self.WIDTH - sub_w) / 2, self.HEIGHT / 2 + 20),
            subtitle,
            font=sub_font,
            fill=(180,180,180)
        )

        img.save(output)

        return {
            "executed": True,
            "output_path": str(output),
            "mode": "title_card"
        }
