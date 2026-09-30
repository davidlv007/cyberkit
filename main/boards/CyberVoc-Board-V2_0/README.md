# CyberVoc-Board-V2_0

本目录包含 **CyberVoc-Board-V2_0** 的板级实现与配置文件。

## 概览

- **板级目录**：`main/boards/CyberVoc-Board-V2_0/`
- **menuconfig 选项**：`Xiaozhi Assistant` → **Board Type** → `CyberVoc V2.0`（`CONFIG_BOARD_TYPE_CYBERVOC_V2_0`；工程默认板级为 V2_1，编译 V2_0 需手动切换）
- **目标芯片**：ESP32-S3（见 `config.json`）
- **网络能力**：双网络（Wi-Fi / ML307 4G），支持在部分状态下切换网络类型（具体以固件逻辑为准）
- **显示与触摸**：圆形触摸屏（QSPI LCD + CST816S）
- **电源**：PG2(GPIO7) 高电平自锁保持供电，PG1(GPIO16) 为开关机键（按下为低）
- **烧录**：烧录全程需一直按住开关机键，否则中途会断电
- **音频**：ES7210 采集，TDM slot 0 为麦克风、slot 1 为功放回采

> 同系列的 V2_1 在电源方案、引脚和麦克风 slot 上均有差异，见 `main/boards/CyberVoc-Board-V2_1/README.md`。

## 编译（推荐脚本方式）

板级构建参数由本目录的 `config.json` 描述，使用根目录脚本编译：

```bash
python scripts/release.py CyberVoc-Board-V2_0
```

## 关键文件

- `config.h`：引脚映射与硬件参数（例如音频 I2S、I2C、LCD/TP、SD、ML307 等）
- `config.json`：release 脚本构建变体与追加的 `sdkconfig` 片段
- `CyberVoc.cc/.h`：板级初始化与外设驱动集成
- `ui_bridge.*`：LVGL 页面与触摸手势桥接（与 UI 交互相关）

## 参考

- 原理图：`docs/原理图/2.0/`（`V2.0-主控板.pdf`、`V2.0-电源板.pdf`、`V2.0-麦克风板.pdf`）
- 根目录 `README.md`：项目总体说明、编译/烧录流程、License 与上游声明
