"""GIF -> EAF 转换器(适配 CyberVoc V2_1 的 gfx_anim)

EAF 格式(来自 esp_eaf_dec.c / gfx_anim.c):
  文件头 16B: 0x89 'E' 'A' 'F' | frames(u32) | checksum(u32) | table+data 长度(u32)
  帧表: 每帧 (size u32, offset u32), offset 相对于帧数据区起点
  校验和: 从 offset 16 起 stored_len 字节逐字节累加
  帧: "ZZ" + "_S" + version(6B) + bit_depth(1B=8) + w(2) + h(2)
      + blocks(2) + block_height(2) + block_len[blocks](4B each)
      + palette(256*4B, BGRA) + 每块 [encoding(1B=0 RLE) + RLE数据]

默认输出半幅(单眼),配合 layout.json 的 mirror:auto 镜像成双眼。
"""
import os
import struct
import glob
import re
from PIL import Image, ImageDraw

GIF_DIR = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif"
OUT_DIR = r"E:\cyberkit\deploy\emote_preview\new_eaf"
os.makedirs(OUT_DIR, exist_ok=True)

W, H = 125, 160          # 与现有 emoji_large 眼睛帧一致
BLOCK_H = 32             # 与现有一致
FPS = 20
MAX_FRAMES = 100


def build_palette():
    """256 色 BGRA 调色板:0=透明,1=黑,2=白,3..=灰阶"""
    pal = bytearray(256 * 4)
    # 0 透明
    pal[0:4] = bytes([0, 0, 0, 0])
    # 1 黑
    pal[4:8] = bytes([0, 0, 0, 255])
    # 2 白
    pal[8:12] = bytes([255, 255, 255, 255])
    # 3..255 灰阶(BGRA)
    for i in range(3, 256):
        v = min(255, int((i - 3) * 255 / 252))
        pal[i * 4:i * 4 + 4] = bytes([v, v, v, 255])
    return bytes(pal)


PALETTE = build_palette()


def quantize_pixels(rgba):
    """把 RGBA 图转成调色板索引:绿幕/黑底->透明,白->2,其余按亮度灰阶"""
    px = rgba.load()
    out = bytearray(W * H)
    for y in range(H):
        for x in range(W):
            r, g, b, a = px[x, y]
            if a < 32 or (g > 170 and r < 110 and b < 110):
                out[y * W + x] = 0
            elif r > 200 and g > 200 and b > 200:
                out[y * W + x] = 2
            elif r < 40 and g < 40 and b < 40:
                out[y * W + x] = 1
            else:
                lum = int(0.299 * r + 0.587 * g + 0.114 * b)
                out[y * W + x] = min(255, 3 + int(lum * 252 / 255))
    return out


def rle_encode(data):
    """(count, value) 对, count 最大 255"""
    out = bytearray()
    i = 0
    n = len(data)
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
    header += b"ZZ_S"                       # magic(0x5A5A) + format "_S"
    header += b"\x00" * 7                   # 1 保留字节 + 6 字节 version
    header += bytes([8])                    # bit_depth(相对 h=f[2:] 的偏移 9)
    header += struct.pack("<4H", W, H, blocks, BLOCK_H)
    block_lens = []
    body = bytearray()
    for bi in range(blocks):
        y0 = bi * BLOCK_H
        y1 = min(H, y0 + BLOCK_H)
        chunk = pix[y0 * W: y1 * W]
        # 补齐到整块高度,避免解码时行数不足
        if y1 - y0 < BLOCK_H:
            chunk = chunk + bytes(W * (BLOCK_H - (y1 - y0)))
        rle = rle_encode(chunk)
        payload = bytes([0]) + rle          # encoding 0 = RLE
        block_lens.append(len(payload))
        body += payload
    header += struct.pack(f"<{blocks}I", *block_lens)
    header += PALETTE
    return bytes(header) + bytes(body)


def convert(gif_path, name, frame_cap=MAX_FRAMES, half=True):
    im = Image.open(gif_path)
    total = getattr(im, "n_frames", 1)
    step = max(1, total // frame_cap)
    idxs = list(range(0, total, step))[:frame_cap]
    frames = []
    for fi in idxs:
        im.seek(fi)
        rgba = im.convert("RGBA")
        if half:
            # 官方是完整双眼;取左半再缩放到 125x160,交给固件镜像成双眼
            rgba = rgba.crop((0, 0, rgba.width // 2, rgba.height))
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
    import sys
    args = sys.argv[1:]
    target = args[0] if args else "smile"
    for p in sorted(glob.glob(os.path.join(GIF_DIR, "*.gif"))):
        if os.path.basename(p).split("_")[0] != target:
            continue
        path, n, size = convert(p, target)
        print(f"{target}: {n} 帧, {size/1024:.0f} KB -> {path}")
        break
