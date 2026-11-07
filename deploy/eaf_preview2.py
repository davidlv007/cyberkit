"""EAF -> 中间帧总览 + 每个表情的 GIF 动图"""
import os, struct, glob
from PIL import Image, ImageDraw

SRC = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large"
OUT = r"E:\cyberkit\deploy\emote_preview"
os.makedirs(OUT, exist_ok=True)


def decode_frame(b, fi, table, data_start):
    size, off = table[fi * 2], table[fi * 2 + 1]
    f = b[data_start + off: data_start + off + size]
    h = f[2:]
    if h[:2] != b"_S":
        raise ValueError("bad header")
    bd = h[9]
    w, ht, blocks, bh = struct.unpack("<4H", h[10:18])
    bl = struct.unpack(f"<{blocks}I", h[18:18 + blocks * 4])
    n = 0 if bd == 24 else (1 << bd)
    pal_off = 18 + blocks * 4
    pal = h[pal_off:pal_off + n * 4]
    data_off = pal_off + n * 4

    def rgb(i):
        c = pal[i * 4:i * 4 + 4]
        return (c[2], c[1], c[0]) if len(c) >= 3 else (0, 0, 0)

    img = Image.new("RGBA", (w, ht), (0, 0, 0, 0))
    px = img.load()
    offsets, o = [], data_off
    for i in range(blocks):
        offsets.append(o)
        o += bl[i]
    y = 0
    for i in range(blocks):
        blk = h[offsets[i]:offsets[i] + bl[i]]
        if not blk:
            continue
        enc, payload = blk[0], blk[1:]
        rows = bh if i < blocks - 1 else ht - y
        if enc == 0:
            out = bytearray()
            for j in range(0, len(payload) - 1, 2):
                out.extend(bytes([payload[j + 1]]) * payload[j])
            for row in range(rows):
                for x in range(w):
                    pos = row * w + x
                    if pos < len(out):
                        idx = out[pos]
                        r, g, bl_ = rgb(idx)
                        a = 0 if pal[idx * 4 + 3] == 0 else 255
                        px[x, y + row] = (r, g, bl_, a)
        elif enc == 2:
            import io
            try:
                jim = Image.open(io.BytesIO(payload)).convert("RGBA")
                for yy in range(min(rows, jim.height)):
                    for xx in range(min(w, jim.width)):
                        px[xx, y + yy] = jim.getpixel((xx, yy))
            except Exception:
                pass
        y += rows
    return img, (w, ht)


def load_eaf(path):
    b = open(path, "rb").read()
    frames = struct.unpack("<I", b[4:8])[0]
    table = struct.unpack(f"<{frames*2}I", b[16:16 + frames*8])
    return b, frames, table, 16 + frames * 8


results = []
for p in sorted(glob.glob(os.path.join(SRC, "*.eaf"))):
    name = os.path.basename(p).replace(".eaf", "")
    try:
        b, frames, table, ds = load_eaf(p)
        mid, size = decode_frame(b, frames // 2, table, ds)
        # 白底合成(透明处显示深色,模拟屏幕)
        bg = Image.new("RGBA", size, (18, 18, 22, 255))
        comp = Image.alpha_composite(bg, mid).convert("RGB")
        comp.save(os.path.join(OUT, f"mid_{name}.png"))
        results.append((name, comp, frames))
        print(f"OK {name:16} 中间帧 {size}, 共 {frames} 帧")

        # GIF:均匀抽 12 帧
        idxs = sorted(set(round(i * (frames - 1) / 11) for i in range(12)))
        gifs = []
        for fi in idxs:
            im, _ = decode_frame(b, fi, table, ds)
            bgi = Image.new("RGBA", size, (18, 18, 22, 255))
            gifs.append(Image.alpha_composite(bgi, im).convert("RGB"))
        gif_path = os.path.join(OUT, f"anim_{name}.gif")
        gifs[0].save(gif_path, save_all=True, append_images=gifs[1:],
                     duration=80, loop=0, optimize=False)
    except Exception as e:
        print(f"ERR {name}: {e}")

# 中间帧总览
if results:
    cw, ch, cols = 200, 220, 5
    rows = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (238, 238, 240))
    d = ImageDraw.Draw(sheet)
    for i, (name, img, frames) in enumerate(results):
        x, y = (i % cols) * cw, (i // cols) * ch
        t = img.copy()
        t.thumbnail((cw - 12, ch - 40))
        sheet.paste(t, (x + (cw - t.width) // 2, y + 6))
        d.text((x + 8, y + ch - 28), f"{name} ({frames}f)", fill=(15, 15, 15))
    out = os.path.join(OUT, "ALL_EMOTES_MID.png")
    sheet.save(out)
    print("\n中间帧总览:", out)
