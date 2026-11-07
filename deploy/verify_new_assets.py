"""验证编译产物:新表情确实进了 merged-binary,分区未超,模型仍单份"""
import os, json, struct, glob

ROOT = r"E:\cyberkit"
log = os.path.join(ROOT, "release_build.log")
lines = open(log, encoding="utf-8", errors="ignore").read().splitlines()

print("=== 打包日志中的新表情 ===")
hits = [l for l in lines if "emote '" in l and ("smile.eaf" in l or "angry.eaf" in l or "shy.eaf" in l)]
for l in hits[:12]:
    print(" ", l.strip())
print(f"  新表情相关行数: {len(hits)}")

print("\n=== 是否有 MISSING/lack ===")
bad = [l for l in lines if "MISSING" in l or "lack=True" in l]
print("  无" if not bad else "\n".join("  " + b.strip() for b in bad[:10]))

print("\n=== assets 分区大小 ===")
p = os.path.join(ROOT, "build", "expression_assets.bin")
if os.path.exists(p):
    sz = os.path.getsize(p)
    print(f"  expression_assets.bin = {sz/1024:.0f} KB  (分区 5500K, {'OK' if sz <= 5500*1024 else '超限!'})")

print("\n=== 模型分区 ===")
for l in lines:
    if "Recommended model partition" in l:
        print("  " + l.strip())

print("\n=== 发布包 ===")
z = os.path.join(ROOT, "releases", "v2.0.5.6_CyberVoc-Board-V2_1.zip")
if os.path.exists(z):
    print(f"  {os.path.basename(z)}  {os.path.getsize(z)/1024/1024:.2f} MB")

print("\n=== 板级 emote.json 前 5 条 ===")
cfg = json.load(open(os.path.join(ROOT, "main", "boards", "CyberVoc-Board-V2_1",
                                  "assets", "360_360", "emote.json"), encoding="utf-8"))
for e in cfg[:5]:
    print(" ", e)
print(f"  共 {len(cfg)} 条")
