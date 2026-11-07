"""把新表情包落地到板级 assets(含备份),保持 .bin / listen.eaf 不动"""
import os, json, shutil

BOARD = r"E:\cyberkit\main\boards\CyberVoc-Board-V2_1\assets"
SRC = r"E:\cyberkit\deploy\emote_preview\new_eaf"
BAK = r"E:\cyberkit\deploy\emote_preview\backup_original_assets"

os.makedirs(BAK, exist_ok=True)

# 1) 备份原 emote.json
src_json = os.path.join(BOARD, "360_360", "emote.json")
bak_json = os.path.join(BAK, "emote.json")
if not os.path.exists(bak_json):
    shutil.copy2(src_json, bak_json)
    print("已备份原 emote.json")

# 2) 复制新 EAF 到 emoji_large
dst_dir = os.path.join(BOARD, "emoji_large")
new_files = [f for f in os.listdir(SRC) if f.endswith(".eaf")]
for f in new_files:
    shutil.copy2(os.path.join(SRC, f), os.path.join(dst_dir, f))
print(f"已放入 {len(new_files)} 个新 EAF")

# 3) 写入新映射(补上服务端会下发但原来缺失的 kissy / cool / eat)
entries = json.load(open(os.path.join(SRC, "emote.json"), encoding="utf-8"))
name_to_src = {e["emote"]: e["src"] for e in entries}
extra = {
    "kissy": "shy.eaf",       # 服务端 😘 -> kissy,原来固件没定义
}
for k, v in extra.items():
    if k not in name_to_src:
        entries.append({"emote": k, "src": v, "loop": True, "fps": 20})

with open(src_json, "w", encoding="utf-8") as f:
    json.dump(entries, f, ensure_ascii=False, indent=4)
print(f"新 emote.json: {len(entries)} 条")

# 4) 核对所有 src 都存在,以及服务端 EMOJI_MAP 的名字都有覆盖
missing = [e["src"] for e in entries if not os.path.exists(os.path.join(dst_dir, e["src"]))]
print("缺失素材:", missing if missing else "无")

emoji_map = ["funny", "crying", "angry", "sad", "loving", "surprised", "shocked",
             "thinking", "relaxed", "sleepy", "silly", "confused", "neutral",
             "happy", "laughing", "embarrassed", "winking", "cool", "delicious",
             "kissy", "confident"]
names = {e["emote"] for e in entries}
uncovered = [n for n in emoji_map if n not in names]
print("服务端 EMOJI_MAP 未覆盖:", uncovered if uncovered else "全部覆盖")

# 5) 打印大小变化
old_eaf = ["Happy.eaf", "Sad.eaf", "angry.eaf", "book.eaf", "confused.eaf", "cry.eaf",
           "insert.eaf", "listen.eaf", "look_around.eaf", "look_left.eaf", "look_right.eaf",
           "neutral.eaf", "paishou.eaf", "question.eaf", "shocked.eaf", "sleep.eaf",
           "tried.eaf", "winking.eaf"]
old_size = sum(os.path.getsize(os.path.join(dst_dir, f)) for f in old_eaf if os.path.exists(os.path.join(dst_dir, f)))
new_size = sum(os.path.getsize(os.path.join(dst_dir, f)) for f in new_files)
print(f"\n旧 18 个 EAF: {old_size/1024/1024:.2f} MB")
print(f"新 {len(new_files)} 个 EAF: {new_size/1024/1024:.2f} MB")
print("(旧文件保留在目录但不被打包,可随时回滚)")
