"""把全幅 360x360 官方表情落地到板级 assets,替换上一版半幅"""
import os, json, shutil

BOARD = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets"
SRC = r"E:\cyberkit\deploy\emote_preview\new_eaf_full"
dst_dir = os.path.join(BOARD, "emoji_large")

# 1) 删除上一版半幅 EAF(半幅文件已无用了,保留会浪费空间但不打包,删除更干净)
half_names = ["angry", "asleep", "badminton", "confident", "cry", "investigate",
              "laugh", "leisure", "mock", "panic", "ponder", "question", "sad",
              "shocked", "shy", "sigh", "smile", "smile_static", "snigger", "yummy"]
removed = 0
for n in half_names:
    p = os.path.join(dst_dir, f"{n}.eaf")
    if os.path.exists(p):
        os.remove(p)
        removed += 1
print(f"已移除上一版半幅 EAF: {removed} 个")

# 2) 复制全幅版
new_files = sorted(f for f in os.listdir(SRC) if f.endswith(".eaf"))
for f in new_files:
    shutil.copy2(os.path.join(SRC, f), os.path.join(dst_dir, f))
print(f"已放入全幅 EAF: {len(new_files)} 个")

# 3) 更新 emote.json:把所有名字映射到全幅版,补上 music/mute/yawn 的使用
#    (MAPPING 与上一版一致,官方表情名不变,只是文件换成了全幅内容)
src_json = os.path.join(BOARD, "360_360", "emote.json")
entries = json.load(open(src_json, encoding="utf-8"))
# 校验:所有 src 必须存在于全幅目录
missing = [e["src"] for e in entries if not os.path.exists(os.path.join(dst_dir, e["src"]))]
if missing:
    print("缺失素材:", missing)
else:
    print("映射核对: 全部 src 存在")

# 4) 汇总
total = sum(os.path.getsize(os.path.join(dst_dir, f)) for f in new_files)
print(f"\n全幅 EAF 总大小: {total/1024/1024:.2f} MB (assets 分区 5500K)")
print(f"emote.json 条目: {len(entries)}")
