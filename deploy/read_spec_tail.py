p = r"E:\cyberkit\deploy\emote_preview\emote_spec.txt"
t = open(p, encoding="utf-8").read()
i = t.find("===== PAGE 9 =====")
print(t[i:])
