"""GIF -> EAF 转换器 v2:完整双眼直出(360x360 全幅,不镜像)
配合固件修改:gfx_anim_set_auto_mirror(..., false) + 居中对齐
"""
import os, sys, struct, glob
from PIL import Image

GIF_DIR = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif"
OUT_DIR = r"E:\cyberkit\deploy\emote_preview\new_eaf_full"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 360, 360
BLOCK_H = 30
FPS = 20
MAX_FRAMES = 100


def build_palette():
    pal = bytearray(256 * 4)
    pal[0:4] = bytes([0, 0, 0, 0])              # 0 透明
    pal[4:8] = bytes([0, 0, 0, 255])            # 1 黑
    pal[8:12] = bytes([255, 255, 255, 255])     # 2 白
    for i in range(3, 256):
        v = min(255, int((i - 3) * 255 / 252))
        pal[i*4:i*4+4] = bytes([v, v, v, 255])  # 灰阶
    return bytes(pal)


PALETTE = build_palette()


def quantize_pixels(rgba):
    px = rgba.load()
    out = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a < 32 or (g > 170 and r < 110 and b < 110):
                out[y*W+x] = 0
            elif r > 200 and g > 200 and b > 200:
                out[y*W+x] = 2
            elif r < 40 and g < 40 and b < 40:
                out[y*W+x] = 1
            else:
                lum = int(0.299*r + 0.587*g + 0.114*b)
                out[y*W+x] = min(255, 3 + int(lum*252/255))
    return out


def rle_encode(data):
    out = bytearray()
    i, n = 0, len(data)
    while i < n:
        v = data[i]
        j = i + 1
        while j < n and data[j] == v and j - i < 255:
            j += 1
        out.append(j - i)
        out.append(v)
        i = j
    return bytes(out)


def build_frame(pix):
    blocks = (H + BLOCK_H - 1) // BLOCK_H
    header = bytearray()
    header += b"ZZ_S"
    header += b"\x00" * 7
    header += bytes([8])
    header += struct.pack("<4H", W, H, blocks, BLOCK_H)
    block_lens = []
    body = bytearray()
    for bi in range(blocks):
        y0 = bi * BLOCK_H
        y1 = min(H, y0 + BLOCK_H)
        chunk = pix[y0*W:y1*W]
        if y1 - y0 < BLOCK_H:
            chunk = chunk + bytes(W * (BLOCK_H - (y1 - y0)))
        rle = rle_encode(chunk)
        payload = bytes([0]) + rle
        block_lens.append(len(payload))
        body += payload
    header += struct.pack(f"<{blocks}I", *block_lens)
    header += PALETTE
    return bytes(header) + bytes(body)


def convert(gif_path, name, frame_cap=MAX_FRAMES):
    im = Image.open(gif_path)
    total = getattr(im, "n_frames", 1)
    step = max(1, total // frame_cap)
    idxs = list(range(0, total, step))[:frame_cap]
    frames = []
    for fi in idxs:
        im.seek(fi)
        rgba = im.convert("RGBA")
        # 完整画面等比缩放到 360x360(官方 848x848 正方形画布)
        rgba = rgba.resize((W, H), Image.Resampling.LANCZOS)
        frames.append(build_frame(quantize_pixels(rgba)))

    n = len(frames)
    table = bytearray()
    data = bytearray()
    for f in frames:
        table += struct.pack("<II", len(f), len(data))
        data += f
    stored = len(table) + len(data)
    chk = sum(table) + sum(data)
    head = struct.pack("<4sIII", b"\x89EAF", n, chk & 0xFFFFFFFF, stored)
    out = head + table + data
    path = os.path.join(OUT_DIR, f"{name}.eaf")
    with open(path, "wb") as fp:
        fp.write(out)
    return path, n, len(out)


if __name__ == "__main__":
    args = sys.argv[1:]
    if args and args[0] == "all":
        names = sorted({os.path.basename(p).split("_")[0] for p in glob.glob(os.path.join(GIF_DIR, "*.gif"))})
        for n in names:
            src = next(p for p in glob.glob(os.path.join(GIF_DIR, "*.gif"))
                       if os.path.basename(p).split("_")[0] == n)
            path, cnt, size = convert(src, n)
            print(f"{n:16} {cnt:3d} 帧 {size/1024:7.1f} KB")
    else:
        target = args[0] if args else "smile"
        for p in sorted(glob.glob(os.path.join(GIF_DIR, "*.gif"))):
            if os.path.basename(p).split("_")[0] == target:
                path, n, size = convert(p, target)
                print(f"{target}: {n} 帧, {size/1024:.0f} KB -> {path}")
                break
