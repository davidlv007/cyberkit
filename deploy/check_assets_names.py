"""在生成的 assets 镜像里搜索表情文件名,确认新旧"""
import os
p = r"E:\cyberkit\build\expression_assets.bin"
b = open(p, "rb").read()

new_names = ["smile.eaf", "laugh.eaf", "shy.eaf", "yummy.eaf", "asleep.eaf",
             "investigate.eaf", "panic.eaf", "ponder.eaf", "snigger.eaf"]
old_names = ["Happy.eaf", "Sad.eaf", "insert.eaf", "paishou.eaf",
             "look_around.eaf", "book.eaf", "tried.eaf"]

print("=== 新表情文件名(应存在) ===")
for n in new_names:
    print(f"  {n:22} {'✓' if n.encode() in b else '✗ 缺失'}")
print("=== 旧表情文件名(不应存在) ===")
for n in old_names:
    print(f"  {n:22} {'✗ 仍存在' if n.encode() in b else '✓ 已移除'}")
print("=== 图标/听筒动画(应保留) ===")
for n in ["listen.eaf", "icon_mic.bin", "battery_bg.bin", "icon_wifi"]:
    print(f"  {n:22} {'✓' if n.encode() in b else '✗ 缺失'}")
