"""批量把官方 23 个 GIF 转成 EAF,并生成新的 emote.json 映射"""
import os, sys, glob, json, re
sys.path.insert(0, r"E:\cyberkit\deploy")
from gif2eaf import convert, GIF_DIR, OUT_DIR

# 现有 30 个表情名 -> 官方 23 个表情的映射
# 依据规范文档的情绪矩阵:积极/消极/中性思考/惊讶反应/社交情境/生理状态
MAPPING = {
    "happy": "smile",
    "laughing": "laugh",
    "funny": "snigger",
    "loving": "shy",
    "embarrassed": "shy",
    "confident": "confident",
    "delicious": "yummy",
    "sad": "sad",
    "crying": "cry",
    "sleepy": "asleep",
    "silly": "mock",
    "angry": "angry",
    "surprised": "shocked",
    "shocked": "panic",
    "thinking": "ponder",
    "winking": "leisure",
    "relaxed": "leisure",
    "confused": "question",
    "neutral": "smile_static",
    "idle": "smile_static",
    "insert": "investigate",
    "look_left": "investigate",
    "look_right": "investigate",
    "look_around": "investigate",
    "question": "question",
    "eat": "yummy",
    "tried": "sigh",
    "book": "ponder",
    "cool": "confident",
    "paishou": "badminton",
}

# GIF 文件名(去掉参数后缀) -> 规范名
gif_files = {}
for p in sorted(glob.glob(os.path.join(GIF_DIR, "*.gif"))):
    fn = os.path.basename(p)
    stem = fn.split("_")[0]
    gif_files[stem] = p
# smile_static 单独对应静态微笑
for p in sorted(glob.glob(os.path.join(GIF_DIR, "*.gif"))):
    if "smile_static" in os.path.basename(p):
        gif_files["smile_static"] = p

# 只转实际被用到的官方表情
needed = sorted(set(MAPPING.values()))
print("需要转换的官方表情:", len(needed), needed)

results = {}
for name in needed:
    if name not in gif_files:
        print(f"  [缺失] {name}")
        continue
    path, n, size = convert(gif_files[name], name)
    results[name] = (n, size)
    print(f"  {name:16} {n:3d} 帧  {size/1024:7.1f} KB")

total = sum(v[1] for v in results.values())
print(f"\n合计: {len(results)} 个 EAF, {total/1024/1024:.2f} MB")

# 生成新的 emote.json:每个名字指向对应 EAF
entries = []
for emote, src in MAPPING.items():
    if src not in results:
        continue
    entries.append({
        "emote": emote,
        "src": f"{src}.eaf",
        "loop": emote not in ("neutral", "idle", "insert", "look_left", "look_right",
                              "look_around", "question", "eat", "tried", "book", "cool", "paishou"),
        "fps": 20,
    })
out_json = os.path.join(OUT_DIR, "emote.json")
with open(out_json, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=4)
print("映射文件:", out_json, f"({len(entries)} 条)")
