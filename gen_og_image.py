"""Generate the social-preview (Open Graph) image: docs/og-image.png (1200x630).
Run: python gen_og_image.py
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 630
BG = (247, 249, 252)
BLUE = (31, 111, 235)
FG = (29, 35, 48)
MUTED = (90, 100, 114)


def font(path_names, size):
    for p in path_names:
        try:
            return ImageFont.truetype(p, size)
        except Exception:
            continue
    return ImageFont.load_default()


bold = lambda s: font([r"C:\Windows\Fonts\segoeuib.ttf", r"C:\Windows\Fonts\arialbd.ttf"], s)
reg = lambda s: font([r"C:\Windows\Fonts\segoeui.ttf", r"C:\Windows\Fonts\arial.ttf"], s)

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# left accent bar
d.rectangle([0, 0, 14, H], fill=BLUE)

# ink-drop emblem (right)
ex, ey, r = 980, 300, 96
d.rounded_rectangle([ex - 150, ey - 150, ex + 150, ey + 150], radius=46, fill=BLUE)
cx, cy = ex, ey + 18
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255))
d.polygon([(cx, cy - 165), (cx - r, cy), (cx + r, cy)], fill=(255, 255, 255))

# text block (left)
x = 70
d.text((x, 96), "Waste Ink Maintenance", font=bold(58), fill=FG)
d.text((x, 162), "Counter Utility", font=bold(58), fill=FG)
d.text((x, 252), "Read & reset waste-ink maintenance counters", font=reg(30), fill=MUTED)
d.text((x, 292), "over USB — after physical pad/tank service.", font=reg(30), fill=MUTED)

for i, line in enumerate(["Open source  ·  Windows  ·  USB  ·  EUPL-1.2",
                          "Not an official Epson product."]):
    d.text((x, 392 + i * 40), line, font=reg(26), fill=MUTED)

os.makedirs("docs", exist_ok=True)
img.save(os.path.join("docs", "og-image.png"))
print("Wrote docs/og-image.png")
