# CyberVoc-Board-V2_1

本目录包含 **CyberVoc-Board-V2_1** 的板级实现与配置文件。软件功能与 `CyberVoc-Board-V2_0` 一致，硬件引脚与电源方案来自 vocat-3 工程的 `cyber-vocat` 板级。

## 概览

- **板级目录**：`main/boards/CyberVoc-Board-V2_1/`
- **目标芯片**：ESP32-S3（见 `config.json`）
- **网络能力**：双网络（Wi-Fi / ML307 4G），支持在部分状态下切换网络类型（具体以固件逻辑为准）
- **显示与触摸**：圆形触摸屏（QSPI LCD + CST816S）
- **姿态传感器**：QMA6100P（I2C 0x12，与音频 Codec 共用 I2C 总线）
- **说话指示灯**：GPIO19，低电平点亮

## 与 V2_0 的硬件差异

- **电源**：无软件开机，上电由硬件完成；PG1(GPIO40) 为关机键（按下为高），长按 1.5s 显示关机提示后，PG2(GPIO38) 输出 200ms 高电平脉冲断电。PG2 平时保持低电平（V2_0 为高电平自锁保持）。
- **烧录**：不需要一直按住开关机按键。
- **引脚**：I2S、LCD、SD、ML307、底座 UART、头部触摸等引脚全部重新分配，详见 `config.h`。
- **麦克风 TDM slot**：ES7210 的 TDM 顺序为 MIC1、MIC3、MIC2、MIC4。本板 MIC1/MIC2 为麦克风，MIC3 为功放输出回采（AEC 参考），MIC4 未用。实测 MIC1（slot 0）几乎收不到人声，因此 `BoxAudioCodec` 在 V2_1 的 mic+ref 模式下读取完整 4 slot，取 slot 2（MIC2）作麦克风、slot 1（MIC3）作回采。

## 编译（推荐脚本方式）

板级构建参数由本目录的 `config.json` 描述，使用根目录脚本编译：

```bash
python scripts/release.py CyberVoc-Board-V2_1
```

## 关键文件

- `config.h`：引脚映射与硬件参数（例如音频 I2S、I2C、LCD/TP、SD、ML307、电源键等）
- `config.json`：release 脚本构建变体与追加的 `sdkconfig` 片段
- `CyberVoc.cc/.h`：板级初始化与外设驱动集成
- `ui_bridge.*`：LVGL 页面与触摸手势桥接（与 UI 交互相关）

## 参考

- 根目录 `README.md`：项目总体说明、编译/烧录流程、License 与上游声明
