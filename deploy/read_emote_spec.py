"""提取官方表情动效系统规范 PDF 的文字,重点找表情清单/矩阵与制作规格"""
import sys
p = r"E:\cyberkit\deploy\emote_preview\emote_spec.pdf"

try:
    from pypdf import PdfReader
    r = PdfReader(p)
    print("页数:", len(r.pages))
    out = []
    for i, page in enumerate(r.pages):
        try:
            t = page.extract_text() or ""
        except Exception as e:
            t = f"[提取失败 {e}]"
        out.append(f"\n===== PAGE {i+1} =====\n{t}")
    txt = "\n".join(out)
    with open(r"E:\cyberkit\deploy\emote_preview\emote_spec.txt", "w", encoding="utf-8") as f:
        f.write(txt)
    print("全文已保存, 字符数:", len(txt))
    print("\n--- 前 3000 字 ---\n")
    print(txt[:3000])
except Exception as e:
    print("pypdf 失败:", e)
    import traceback
    traceback.print_exc()
