import os
import sys

root = r"E:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server"
os.chdir(root)
sys.path.insert(0, root)
os.environ["Path"] = r"E:\cyberkit\deploy\xiaozhi-esp32-server\bin;" + os.environ.get("Path", "")

from core.providers.asr.sherpa_onnx_local import is_noise_text

noise = [".", "Yeah.", "The.", "I.", "I", "Um.", "OK.", "", "  ", "...", "Hmm.", "A."]
valid = ["你好喵伴", "讲个笑话", "今天天气怎么样", "播放音乐", "Hello world", "What time is it"]

print("=== 应被拦截(噪声) ===")
for t in noise:
    r = is_noise_text(t)
    print(f"  {t!r:12} -> {'拦截' if r else '放行  <<< 漏网'}")
print("=== 应被放行(正常语句) ===")
for t in valid:
    r = is_noise_text(t)
    print(f"  {t!r:20} -> {'拦截  <<< 误杀' if r else '放行'}")
