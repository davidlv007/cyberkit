import sys
sys.path.insert(0, r"E:\cyberkit\deploy")
from gif2eaf_full import convert

p = r"E:\cyberkit\deploy\emote_preview\EmotePack\gif\smile_static_[0.5s].gif"
path, n, size = convert(p, "smile_static")
print(f"smile_static: {n} 帧, {size/1024:.1f} KB -> {path}")

# 核对与 smile 的差异(内容应不同:static 是静态款)
import hashlib
a = hashlib.md5(open(path, "rb").read()).hexdigest()[:10]
b = hashlib.md5(open(r"E:\cyberkit\deploy\emote_preview\new_eaf_full\smile.eaf", "rb").read()).hexdigest()[:10]
print(f"smile_static md5={a}  smile md5={b}  {'相同(注意!)' if a == b else '不同 OK'}")
