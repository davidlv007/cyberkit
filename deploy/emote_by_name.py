"""按 emote.json 的 30 个表情名拼对照图:名字 -> 实际动画画面"""
import os, json
from PIL import Image, ImageDraw

EMOTE_JSON = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\360_360\emote.json"
OUT = r"E:\cyberkit\deploy\emote_preview"
entries = json.load(open(EMOTE_JSON, encoding="utf-8"))

# 已解码出的"最佳帧"图
cw, ch, cols = 190, 170, 5
rows = (len(entries) + cols - 1) // cols
sheet = Image.new("RGB", (cols * cw, rows * ch), (240, 240, 242))
d = ImageDraw.Draw(sheet)

missing = set()
for i, e in enumerate(entries):
    name, src = e["emote"], e["src"]
    x, y = (i % cols) * cw, (i // cols) * ch
    stem = src.replace(".eaf", "")
    f = os.path.join(OUT, f"best_{stem}.png")
    if os.path.exists(f):
        img = Image.open(f).convert("RGB")
        img.thumbnail((cw - 12, ch - 44))
        sheet.paste(img, (x + (cw - img.width) // 2, y + 4))
        label = f"{name}"
        sub = stem
    else:
        d.rectangle([x + 50, y + 30, x + cw - 50, y + ch - 50], fill=(215, 215, 218))
        d.text((x + 58, y + 60), "素材缺失", fill=(180, 40, 40))
        label = name
        sub = src + " (缺)"
        missing.add(src)
    d.text((x + 8, y + ch - 38), label, fill=(15, 15, 15))
    d.text((x + 8, y + ch - 22), sub, fill=(110, 110, 115))

out = os.path.join(OUT, "BY_NAME_30.png")
sheet.save(out)
print("对照图:", out)
print("缺失素材:", sorted(missing))
