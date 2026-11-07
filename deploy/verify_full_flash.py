"""验证:assets 里是全幅 360x360 新表情,然后解压固件"""
import os, zipfile

p = r"E:\cyberkit\build\expression_assets.bin"
b = open(p, "rb").read()
print(f"assets 镜像: {len(b)/1024:.0f} KB (分区 5500K)")

# 全幅文件名应在
for n in ["smile.eaf", "angry.eaf", "shy.eaf", "yummy.eaf", "music.eaf", "mute.eaf", "yawn.eaf"]:
    print(f"  {n:18} {'✓' if n.encode() in b else '✗ 缺失'}")

# 旧半幅不应残留(以内容判断不可行,查文件名即可:文件名与半幅同名,改为检查镜像中 smile.eaf 附近帧头尺寸)
# 直接检查:镜像中是否存在 125x160 的帧头特征无法简单判断,改为核对板级目录
d = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets\emoji_large"
import glob
eafs = glob.glob(os.path.join(d, "*.eaf"))
sizes = {}
for e in eafs:
    bb = open(e, "rb").read()
    frames = struct.unpack("<I", bb[4:8])[0] if False else None
import struct
for e in eafs:
    bb = open(e, "rb").read()
    frames = struct.unpack("<I", bb[4:8])[0]
    # 第二帧帧头里读 width/height
    table = struct.unpack(f"<{frames*2}I", bb[16:16+frames*8])
    ds = 16 + frames*8
    f0 = bb[ds+table[1]: ds+table[1]+table[0]]
    w, h = struct.unpack("<2H", f0[14:18])
    sizes[os.path.basename(e)] = (w, h)

bad = {k: v for k, v in sizes.items() if v != (360, 360) and k != "listen.eaf"}
print("\n板级 emoji_large 帧尺寸检查(应全 360x360,listen 除外):")
print("  全部 OK" if not bad else "  异常: " + str(bad))
print(f"  listen.eaf: {sizes.get('listen.eaf')}")

# 解压固件
d2 = r"E:\cyberkit\releases"
z = os.path.join(d2, "v2.0.5.6_CyberVoc-Board-V2_1.zip")
with zipfile.ZipFile(z) as f:
    f.extract("merged-binary.bin", d2)
mp = os.path.join(d2, "merged-binary.bin")
print(f"\nmerged-binary.bin: {os.path.getsize(mp)/1024/1024:.2f} MB")
