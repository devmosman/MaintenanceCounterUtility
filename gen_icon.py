"""Generate a placeholder application icon (assets/app.ico).

Replace assets/app.ico with your own icon any time, then rebuild — the build and
the window both pick it up automatically. Run: python gen_icon.py
"""
import os
from PIL import Image, ImageDraw

S = 256
img = Image.new("RGBA", (S, S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)

# rounded-square background (brand blue)
d.rounded_rectangle([6, 6, S - 6, S - 6], radius=46, fill=(31, 111, 235, 255))

# white ink drop = triangle (top) + circle (bottom)
cx, r, cy = S // 2, 56, 168
d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 255, 255, 255))
d.polygon([(cx, 56), (cx - r, cy), (cx + r, cy)], fill=(255, 255, 255, 255))
# small "drop highlight"
d.ellipse([cx - 22, cy - 14, cx - 2, cy + 6], fill=(210, 226, 255, 255))

os.makedirs("assets", exist_ok=True)
img.save(os.path.join("assets", "app.ico"),
         sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("Wrote assets/app.ico")
