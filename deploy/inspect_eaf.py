import os, struct

p = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large\Happy.eaf"
b = open(p, "rb").read(128)
print("文件大小:", os.path.getsize(p))
print("HEX:", b[:64].hex(" "))
print("ASCII:", "".join(chr(c) if 32 <= c < 127 else "." for c in b[:64]))
print()
print("按 uint32 LE 前 16 个:", struct.unpack("<16I", b[:64]))
