import os, zipfile, hashlib

d = r"E:\cyberkit\releases"
z = os.path.join(d, "v2.0.5.6_CyberVoc-Board-V2_1.zip")
with zipfile.ZipFile(z) as f:
    print("包内文件:", f.namelist())
    f.extract("merged-binary.bin", d)

p = os.path.join(d, "merged-binary.bin")
sz = os.path.getsize(p)
md5 = hashlib.md5(open(p, "rb").read()).hexdigest()
print(f"merged-binary.bin: {sz/1024/1024:.2f} MB  md5={md5}")
