import struct
p = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large\Happy.eaf"
b = open(p, "rb").read()
frames = struct.unpack("<I", b[4:8])[0]
tbl = struct.unpack(f"<{frames*2}I", b[16:16+frames*8])
f = b[16+frames*8+tbl[1] : 16+frames*8+tbl[1]+tbl[0]]
h = f[2:]
bd = h[9]
w, ht, blocks, bh = struct.unpack("<4H", h[10:18])
bl = struct.unpack(f"<{blocks}I", h[18:18+blocks*4])
pal_off = 18 + blocks*4
n = 1 << bd
pal = h[pal_off:pal_off+n*4]
print("bit_depth", bd, "size", (w,ht), "blocks", blocks, "ncolors", n)
print("palette 前 12 色 [B,G,R,A] -> (R,G,B):")
for i in range(12):
    c = pal[i*4:i*4+4]
    print(" ", i, list(c), "->", (c[2], c[1], c[0]))
print("palette 非零色数:", sum(1 for i in range(n) if any(pal[i*4:i*4+3])))
print("block_len:", bl)
