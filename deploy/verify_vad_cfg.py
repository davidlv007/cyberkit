import os
import sys

root = r"E:\cyberkit\deploy\xiaozhi-esp32-server\main\xiaozhi-server"
os.chdir(root)
sys.path.insert(0, root)

try:
    import asyncio
    import inspect
    from config.config_loader import load_config
    result = load_config()
    cfg = asyncio.run(result) if inspect.iscoroutine(result) else result
except Exception as e:
    print("load_config 调用失败:", e)
    # 回退:手动模拟深合并验证 yaml 内容
    import yaml
    def deep_merge(a, b):
        for k, v in b.items():
            if isinstance(v, dict) and isinstance(a.get(k), dict):
                deep_merge(a[k], v)
            else:
                a[k] = v
        return a
    with open("config.yaml", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    with open(os.path.join("data", ".config.yaml"), encoding="utf-8") as f:
        cfg = deep_merge(cfg, yaml.safe_load(f))

print("VAD.SileroVAD 合并结果:")
for k, v in cfg.get("VAD", {}).get("SileroVAD", {}).items():
    print(f"  {k} = {v}")
print("selected_module.VAD =", cfg.get("selected_module", {}).get("VAD"))
