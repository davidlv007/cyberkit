"""乐鑫官方 Emote Pack:23 个 GIF 表情 -> 总览图"""
import os, glob, re
from PIL import Image, ImageDraw

SRC = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif"
OUT = r"E:\cyberkit\deploy\emote_preview"

cells = []
for p in sorted(glob.glob(os.path.join(SRC, "*.gif"))):
    name = os.path.basename(p).split("_")[0]
    try:
        im = Image.open(p)
        n = getattr(im, "n_frames", 1)
        # 取中间偏后一帧(通常表情最完整)
        im.seek(min(n - 1, max(0, int(n * 0.45))))
        frame = im.convert("RGBA")
        # GIF 用纯绿做透明色键,替换成深色屏幕背景
        px = frame.load()
        for yy in range(frame.height):
            for xx in range(frame.width):
                r, g, b, a = px[xx, yy]
                if g > 200 and r < 80 and b < 80:
                    px[xx, yy] = (18, 18, 22, 255)
        bg = Image.new("RGBA", frame.size, (18, 18, 22, 255))
        frame = Image.alpha_composite(bg, frame).convert("RGB")
        cells.append((name, frame, n, im.size))
        print(f"OK {name:14} {im.size} {n} 帧")
    except Exception as e:
        print(f"ERR {name}: {e}")

cw, ch, cols = 220, 230, 5
rows = (len(cells) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), (242, 242, 245))
d = ImageDraw.Draw(sheet)
for i, (name, img, n, size) in enumerate(cells):
    x, y = (i % cols) * cw, (i // cols) * ch
    t = img.copy()
    t.thumbnail((cw - 14, ch - 46))
    sheet.paste(t, (x + (cw - t.width) // 2, y + 4))
    d.text((x + 8, y + ch - 38), f"{name}", fill=(15, 15, 15))
    d.text((x + 8, y + ch - 22), f"{size[0]}x{size[1]}  {n}f", fill=(110, 110, 115))

out = os.path.join(OUT, "OFFICIAL_23_EMOTES.png")
sheet.save(out)
print("\n官方表情总览:", out)
