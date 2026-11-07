"""EAF -> 每个表情挑最清晰的一帧(非透明像素最多) + 可用的 GIF 动图"""
import os, struct, glob
from PIL import Image, ImageDraw

SRC = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large"
OUT = r"E:\cyberkit\deploy\emote_preview"
BG = (18, 18, 22, 255)


def decode_frame(b, fi, table, ds):
    size, off = table[fi * 2], table[fi * 2 + 1]
    f = b[ds + off: ds + off + size]
    h = f[2:]
    if h[:2] != b"_S":
        return None, None
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
                        r, g, bb = rgb(idx)
                        a = 0 if pal[idx * 4 + 3] == 0 else 255
                        px[x, y + row] = (r, g, bb, a)
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
    # 非透明像素数,用于挑"最张开"的帧
    alpha = img.getchannel("A")
    visible = sum(1 for a in alpha.getdata() if a > 0)
    return img, visible


def composite(img):
    bg = Image.new("RGBA", img.size, BG)
    return Image.alpha_composite(bg, img).convert("RGB")


results, gif_ok = [], 0
for p in sorted(glob.glob(os.path.join(SRC, "*.eaf"))):
    name = os.path.basename(p).replace(".eaf", "")
    try:
        b = open(p, "rb").read()
        frames = struct.unpack("<I", b[4:8])[0]
        table = struct.unpack(f"<{frames*2}I", b[16:16 + frames*8])
        ds = 16 + frames * 8

        # 采样最多 24 帧,挑可见像素最多的
        step = max(1, frames // 24)
        samples = list(range(0, frames, step))
        best, best_score, best_i = None, -1, 0
        cache = {}
        for fi in samples:
            im, score = decode_frame(b, fi, table, ds)
            if im is None:
                continue
            cache[fi] = im
            if score > best_score:
                best, best_score, best_i = im, score, fi
        if best is None:
            raise ValueError("无可解码帧")
        comp = composite(best)
        comp.save(os.path.join(OUT, f"best_{name}.png"))
        results.append((name, comp, frames, best_i))
        print(f"OK {name:16} 最佳帧 #{best_i}/{frames} 可见像素 {best_score}")

        # GIF:用已解码的缓存帧
        gifs = [composite(cache[fi]) for fi in sorted(cache)]
        if len(gifs) >= 2:
            gif_path = os.path.join(OUT, f"anim_{name}.gif")
            gifs[0].save(gif_path, save_all=True, append_images=gifs[1:],
                         duration=100, loop=0, optimize=False)
            gif_ok += 1
    except Exception as e:
        print(f"ERR {name}: {e}")

if results:
    cw, ch, cols = 200, 220, 5
    rows = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cw, rows * ch), (238, 238, 240))
    d = ImageDraw.Draw(sheet)
    for i, (name, img, frames, bi) in enumerate(results):
        x, y = (i % cols) * cw, (i // cols) * ch
        t = img.copy()
        t.thumbnail((cw - 12, ch - 40))
        sheet.paste(t, (x + (cw - t.width) // 2, y + 6))
        d.text((x + 8, y + ch - 28), f"{name} ({frames}f)", fill=(15, 15, 15))
    out = os.path.join(OUT, "ALL_EMOTES_BEST.png")
    sheet.save(out)
    print(f"\n总览图: {out}")
    print(f"GIF 动图: {gif_ok} 个")
