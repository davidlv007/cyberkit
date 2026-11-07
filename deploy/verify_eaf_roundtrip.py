"""闭环验证:用与固件同逻辑的解码器读取新生成的 EAF,并检查校验和"""
import os, struct, glob
from PIL import Image, ImageDraw

OUT = r"E:\cyberkit\deploy\emote_preview\new_eaf"
PREV = r"E:\cyberkit\deploy\emote_preview"
BG = (18, 18, 22, 255)


def decode_frame(b, fi, table, ds):
    size, off = table[fi*2], table[fi*2+1]
    f = b[ds+off: ds+off+size]
    h = f[2:]
    if h[:2] != b"_S":
        raise ValueError("bad frame header")
    bd = h[9]
    w, ht, blocks, bh = struct.unpack("<4H", h[10:18])
    bl = struct.unpack(f"<{blocks}I", h[18:18+blocks*4])
    n = 1 << bd
    pal_off = 18 + blocks*4
    pal = h[pal_off:pal_off+n*4]
    data_off = pal_off + n*4

    img = Image.new("RGBA", (w, ht), (0, 0, 0, 0))
    px = img.load()
    offsets, o = [], data_off
    for i in range(blocks):
        offsets.append(o); o += bl[i]
    y = 0
    for i in range(blocks):
        blk = h[offsets[i]:offsets[i]+bl[i]]
        if not blk:
            continue
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
                        c = pal[idx*4:idx*4+4]
                        a = 0 if c[3] == 0 else 255
                        px[x, y+row] = (c[2], c[1], c[0], a)
        y += rows
    return img


def composite(img):
    bg = Image.new("RGBA", img.size, BG)
    return Image.alpha_composite(bg, img).convert("RGB")


cells = []
for p in sorted(glob.glob(os.path.join(OUT, "*.eaf"))):
    name = os.path.basename(p).replace(".eaf", "")
    b = open(p, "rb").read()
    magic, frames, chk, stored = struct.unpack("<4sIII", b[:16])
    calc = sum(b[16:16+stored]) & 0xFFFFFFFF
    ok_chk = (calc == chk)
    table = struct.unpack(f"<{frames*2}I", b[16:16+frames*8])
    ds = 16 + frames*8
    try:
        im = decode_frame(b, frames//2, table, ds)
        cells.append((name, composite(im)))
        print(f"{name:14} {frames:3d}帧 checksum={'OK' if ok_chk else 'FAIL'} size={im.size} decode=OK")
    except Exception as e:
        print(f"{name:14} {frames:3d}帧 checksum={'OK' if ok_chk else 'FAIL'} decode=FAIL: {e}")

if cells:
    cw, ch, cols = 200, 200, 4
    rows = (len(cells)+cols-1)//cols
    sheet = Image.new("RGB", (cols*cw, rows*ch), (240,240,242))
    d = ImageDraw.Draw(sheet)
    for i, (name, img) in enumerate(cells):
        x, y = (i%cols)*cw, (i//cols)*ch
        t = img.copy(); t.thumbnail((cw-12, ch-40))
        sheet.paste(t, (x+(cw-t.width)//2, y+4))
        d.text((x+8, y+ch-26), name, fill=(15,15,15))
    out = os.path.join(PREV, "NEW_EAF_ROUNDTRIP.png")
    sheet.save(out)
    print("\n解码预览:", out)
