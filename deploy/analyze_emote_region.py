"""分析官方 GIF 帧内容边界:眼睛/图形实际占据的区域,确定裁剪框"""
import os, glob
from PIL import Image

SRC = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif"

for p in sorted(glob.glob(os.path.join(SRC, "*.gif"))):
    name = os.path.basename(p).split("_")[0]
    im = Image.open(p)
    n = getattr(im, "n_frames", 1)
    # 取 3 帧样本(开始/中间/结尾)统计内容边界
    bounds = []
    for fi in [0, n // 2, n - 1]:
        im.seek(fi)
        rgba = im.convert("RGBA")
        px = rgba.load()
        w, h = rgba.size
        minx, miny, maxx, maxy = w, h, 0, 0
        for y in range(0, h, 4):
            for x in range(0, w, 4):
                r, g, b, a = px[x, y]
                if a > 32 and not (g > 170 and r < 110 and b < 110):  # 非透明且非绿幕
                    if x < minx: minx = x
                    if y < miny: miny = y
                    if x > maxx: maxx = x
                    if y > maxy: maxy = y
        if maxx >= minx and maxy >= miny:
            bounds.append((minx, miny, maxx, maxy))
    if bounds:
        # 取并集
        x0 = min(b[0] for b in bounds); y0 = min(b[1] for b in bounds)
        x1 = max(b[2] for b in bounds); y1 = max(b[3] for b in bounds)
        print(f"{name:16} 画布 {w}x{h}  内容框 x[{x0}-{x1}] y[{y0}-{y1}] "
              f"= {x1-x0+1}x{y1-y0+1}  比例 {(y1-y0+1)/(x1-x0+1):.2f}")
