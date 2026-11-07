"""解析 EAF 帧动画,把每个表情的首帧导出为 PNG,并拼成一张总览图。
EAF 格式参考 managed_components/espressif__esp_lv_eaf_player/src/esp_eaf_dec.c
"""
import os
import struct
import glob
from PIL import Image, ImageDraw

SRC = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large"
OUT = r"E:\cyberkit\deploy\emote_preview"
os.makedirs(OUT, exist_ok=True)


def parse_eaf_first_frame(path):
    b = open(path, "rb").read()
    magic, frames, _checksum, _len = struct.unpack("<4sIII", b[:16])
    if magic != b"\x89EAF":
        raise ValueError(f"bad magic {magic!r}")
    table = struct.unpack(f"<{frames * 2}I", b[16:16 + frames * 8])
    data_start = 16 + frames * 8
    size, off = table[0], table[1]
    f = b[data_start + off: data_start + off + size]

    # 帧头: "ZZ" + "_S" 标识, 实际字段从 offset 2 起按 esp_eaf_header_parse 读取
    # memcpy(format, f, 2) -> "ZZ"? 解码器接收的是 frame_data+2 (跳过 "ZZ")
    h = f[2:]
    if h[:2] != b"_S":
        raise ValueError(f"bad frame header {f[:4]!r}")
    bit_depth = h[9]
    width, height, blocks, block_height = struct.unpack("<4H", h[10:18])
    block_len = struct.unpack(f"<{blocks}I", h[18:18 + blocks * 4])
    ncolors = 0 if bit_depth == 24 else (1 << bit_depth)
    pal_off = 18 + blocks * 4
    palette = h[pal_off: pal_off + ncolors * 4]
    data_off = pal_off + ncolors * 4

    # 调色板: 每色 4 字节, RGB888 是 [B,G,R,A]
    def rgb(idx):
        c = palette[idx * 4: idx * 4 + 4]
        if len(c) < 3:
            return (0, 0, 0)
        return (c[2], c[1], c[0])

    img = Image.new("RGB", (width, height), (0, 0, 0))
    px = img.load()
    offsets = []
    o = data_off
    for i in range(blocks):
        offsets.append(o)
        o += block_len[i]

    y = 0
    for i in range(blocks):
        blk = h[offsets[i]: offsets[i] + block_len[i]]
        if not blk:
            continue
        enc = blk[0]
        payload = blk[1:]
        rows = block_height
        if i == blocks - 1:
            rows = height - y
        pixels = None
        if enc == 0:  # RLE
            out = bytearray()
            for j in range(0, len(payload) - 1, 2):
                cnt, val = payload[j], payload[j + 1]
                out.extend(bytes([val]) * cnt)
            pixels = bytes(out)
        elif enc == 2:  # JPEG
            import io
            try:
                jim = Image.open(io.BytesIO(payload)).convert("RGB")
                for yy in range(min(rows, jim.height)):
                    for xx in range(min(width, jim.width)):
                        px[xx, y + yy] = jim.getpixel((xx, yy))
                y += rows
                continue
            except Exception:
                pixels = None
        else:
            pixels = None  # Huffman 帧暂不解

        if pixels is None:
            y += rows
            continue
        for row in range(rows):
            for x in range(width):
                pos = row * width + x
                if pos < len(pixels):
                    px[x, y + row] = rgb(pixels[pos])
        y += rows
    return img, dict(frames=frames, size=(width, height), bit_depth=bit_depth,
                     blocks=blocks, enc=[h[offsets[i]] for i in range(blocks)])


results = []
for p in sorted(glob.glob(os.path.join(SRC, "*.eaf"))):
    name = os.path.basename(p)
    try:
        img, info = parse_eaf_first_frame(p)
        out = os.path.join(OUT, name.replace(".eaf", ".png"))
        img.save(out)
        results.append((name, img, info))
        print(f"OK  {name:20} {info['size']} frames={info['frames']} enc={info['enc']}")
    except Exception as e:
        print(f"ERR {name:20} {e}")

# 拼总览图
if results:
    cell_w, cell_h = 160, 200
    cols = 6
    rows = (len(results) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (245, 245, 245))
    d = ImageDraw.Draw(sheet)
    for i, (name, img, info) in enumerate(results):
        x, y = (i % cols) * cell_w, (i // cols) * cell_h
        thumb = img.copy()
        thumb.thumbnail((cell_w - 10, cell_h - 34))
        sheet.paste(thumb, (x + (cell_w - thumb.width) // 2, y + 4))
        d.text((x + 6, y + cell_h - 24), name.replace(".eaf", ""), fill=(20, 20, 20))
    sheet_path = os.path.join(OUT, "ALL_EMOTES.png")
    sheet.save(sheet_path)
    print("\n总览图:", sheet_path)
