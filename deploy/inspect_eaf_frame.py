import os, struct

p = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large\Happy.eaf"
b = open(p, "rb").read()
magic, frames, unk, data_size = struct.unpack("<4sIII", b[:16])
print("magic:", magic, "frames:", frames, "unk:", hex(unk), "data_size:", data_size)

table = struct.unpack(f"<{frames * 2}I", b[16:16 + frames * 8])
print("帧表前 6 项(size, offset):", [(table[i], table[i+1]) for i in range(0, 12, 2)])
print("帧表最后 2 项:", (table[-2], table[-1]))

data_start = 16 + frames * 8
print("data_start:", data_start, "文件总长:", len(b))
first_size, first_off = table[0], table[1]
frame = b[data_start + first_off: data_start + first_off + first_size]
print("第一帧长度:", len(frame))
print("第一帧前 48 字节 HEX:", frame[:48].hex(" "))
print("第一帧前 48 字节 ASCII:", "".join(chr(c) if 32 <= c < 127 else "." for c in frame[:48]))
