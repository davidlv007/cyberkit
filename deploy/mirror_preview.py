"""模拟固件 mirror:auto 的双眼效果,生成最终观感预览"""
import os, struct, glob
from PIL import Image, ImageDraw
from verify_eaf_roundtrip import decode_frame, composite

OUT = r"E:\cyberkit\deploy\emote_preview\new_eaf"
PREV = r"E:\cyberkit\deploy\emote_preview"

cells = []
for p in sorted(glob.glob(os.path.join(OUT, "*.eaf"))):
    name = os.path.basename(p).replace(".eaf", "")
    b = open(p, "rb").read()
    frames = struct.unpack("<I", b[4:8])[0]
    table = struct.unpack(f"<{frames*2}I", b[16:16+frames*8])
    ds = 16 + frames*8
    im = decode_frame(b, frames//2, table, ds)
    rgb = composite(im)
    # 模拟 mirror:auto:水平镜像拼接
    mirrored = rgb.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    both = Image.new("RGB", (rgb.width*2, rgb.height))
    both.paste(rgb, (0, 0))
    both.paste(mirrored, (rgb.width, 0))
    cells.append((name, both))

cw, ch, cols = 260, 180, 4
rows = (len(cells)+cols-1)//cols
sheet = Image.new("RGB", (cols*cw, rows*ch), (240,240,242))
d = ImageDraw.Draw(sheet)
for i, (name, img) in enumerate(cells):
    x, y = (i%cols)*cw, (i//cols)*ch
    t = img.copy(); t.thumbnail((cw-12, ch-38))
    sheet.paste(t, (x+(cw-t.width)//2, y+4))
    d.text((x+8, y+ch-24), name, fill=(15,15,15))
out = os.path.join(PREV, "NEW_EMOTES_MIRRORED.png")
sheet.save(out)
print("双眼效果预览:", out)
