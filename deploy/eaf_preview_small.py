"""解码组件自带 emoji_small 套,与板级 emoji_large 拼对照图"""
import os, sys, glob, struct
from PIL import Image, ImageDraw

sys.path.insert(0, r"E:\cyberkit\deploy")
# 复用 eaf_preview3 的解码函数
import importlib.util
spec = importlib.util.spec_from_file_location("ep3", r"E:\cyberkit\deploy\eaf_preview3.py")

# 直接把解码逻辑拷过来(避免执行模块顶层循环)
BG = (18, 18, 22, 255)

def decode_frame(b, fi, table, ds):
    size, off = table[fi*2], table[fi*2+1]
    f = b[ds+off: ds+off+size]
    h = f[2:]
    if h[:2] != b"_S":
        return None
    bd = h[9]
    w, ht, blocks, bh = struct.unpack("<4H", h[10:18])
    bl = struct.unpack(f"<{blocks}I", h[18:18+blocks*4])
    n = 0 if bd == 24 else (1 << bd)
    pal_off = 18 + blocks*4
    pal = h[pal_off:pal_off+n*4]
    data_off = pal_off + n*4

    def rgb(i):
        c = pal[i*4:i*4+4]
        return (c[2], c[1], c[0]) if len(c) >= 3 else (0, 0, 0)

    img = Image.new("RGBA", (w, ht), (0, 0, 0, 0))
    px = img.load()
    offsets, o = [], data_off
    for i in range(blocks):
        offsets.append(o); o += bl[i]
    y = 0
    for i in range(blocks):
        blk = h[offsets[i]:offsets[i]+bl[i]]
        if not blk: continue
        enc, payload = blk[0], blk[1:]
        rows = bh if i < blocks-1 else ht - y
        if enc == 0:
            out = bytearray()
            for j in range(0, len(payload)-1, 2):
                out.extend(bytes([payload[j+1]]) * payload[j])
            for row in range(rows):
                for x in range(w):
                    pos = row*w + x
                    if pos < len(out):
                        idx = out[pos]
                        r, g, bb = rgb(idx)
                        a = 0 if pal[idx*4+3] == 0 else 255
                        px[x, y+row] = (r, g, bb, a)
        y += rows
    return img

def composite(img):
    bg = Image.new("RGBA", img.size, BG)
    return Image.alpha_composite(bg, img).convert("RGB")

DIRS = [
    ("板级 emoji_large", r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large"),
    ("组件 emoji_small", r"E:\cyberkit\managed_components\espressif2022__esp_emote_assets\emoji_small"),
]
OUT = r"E:\cyberkit\deploy\emote_preview"
os.makedirs(OUT, exist_ok=True)

for label, d in DIRS:
    files = sorted(glob.glob(os.path.join(d, "*.eaf")))
    cells = []
    for p in files:
        name = os.path.basename(p).replace(".eaf", "")
        try:
            b = open(p, "rb").read()
            frames = struct.unpack("<I", b[4:8])[0]
            table = struct.unpack(f"<{frames*2}I", b[16:16+frames*8])
            ds = 16 + frames*8
            im = decode_frame(b, 0, table, ds)
            if im is None: continue
            cells.append((name, composite(im), frames, im.size))
            print(f"OK {label} {name:14} {im.size} {frames}f")
        except Exception as e:
            print(f"ERR {label} {name}: {e}")
    cw, ch, cols = 200, 200, 5
    rows = (len(cells) + cols - 1)//cols
    sheet = Image.new("RGB", (cols*cw, rows*ch), (240,240,242))
    dr = ImageDraw.Draw(sheet)
    for i, (name, img, frames, size) in enumerate(cells):
        x, y = (i%cols)*cw, (i//cols)*ch
        t = img.copy(); t.thumbnail((cw-12, ch-46))
        sheet.paste(t, (x+(cw-t.width)//2, y+4))
        dr.text((x+8, y+ch-38), f"{name} ({frames}f)", fill=(15,15,15))
        dr.text((x+8, y+ch-22), str(size), fill=(110,110,115))
    fn = "SMALL_vs_LARGE.png" if "small" in label.lower() else "LARGE_only.png"
    # 分别输出
    out = os.path.join(OUT, ("SET_emoji_small.png" if "small" in label.lower() else "SET_emoji_large.png"))
    sheet.save(out)
    print("  ->", out)
