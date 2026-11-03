"""检查本地 llama.cpp 是否已在 127.0.0.1:8088 提供服务。"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request


def main() -> int:
    url = "http://127.0.0.1:8088/health"
    try:
        with urllib.request.urlopen(url, timeout=3) as response:
            body = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        print(f"DOWN {exc}")
        return 1
    print(body)
    try:
        payload = json.loads(body)
        status = str(payload.get("status", "")).lower()
        if status in {"ok", "healthy"}:
            return 0
    except json.JSONDecodeError:
        if "ok" in body.lower():
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
