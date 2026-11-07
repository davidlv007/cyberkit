"""评估把官方 23 个 GIF 转成 EAF 的体积(目标分区 5500K)"""
import os, glob, re
from PIL import Image

SRC = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif"
PARTITION_KB = 5500

print(f"{'表情':16} {'原尺寸':12} {'帧数':>5} {'三段参数':16} -> 125x160 抽帧估算")
total_frames = 0
for p in sorted(glob.glob(os.path.join(SRC, "*.gif"))):
    fn = os.path.basename(p)
    name = fn.split("_")[0]
    param = re.search(r"_\[(.*?)\]", fn)
    param = param.group(1) if param else "-"
    im = Image.open(p)
    n = getattr(im, "n_frames", 1)
    # 现有固件 fps 20;按 20fps 重采样,并限制单表情最多 100 帧
    target = min(int(n * 20 / (n / (getattr(im, "info", {}).get("duration", 50) * n / 1000 + 0.001) or 20)), 100)
    target = min(n, 100)
    total_frames += target
    print(f"{name:16} {str(im.size):12} {n:5d} {param:16} -> {target:3d} 帧")

print(f"\n合计目标帧数: {total_frames}")
print("现有 18 个 eaf 总大小: 约 4.1 MB(含 insert.eaf 1.2MB)")
print(f"assets 分区: {PARTITION_KB} KB")
print("说明:125x160 8bit 调色板 + RLE,单帧通常 1-3KB;100帧*23 ≈ 2-5MB,需实算")
