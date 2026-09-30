# CyberVoc-Board-V2_1

本目录包含 **CyberVoc-Board-V2_1** 的板级实现与配置文件。软件功能与 `CyberVoc-Board-V2_0` 一致，硬件引脚与电源方案来自 vocat-3 工程的 `cyber-vocat` 板级。

## 概览

- **板级目录**：`main/boards/CyberVoc-Board-V2_1/`
- **menuconfig 选项**：`Xiaozhi Assistant` → **Board Type** → `CyberVoc V2.1`（`CONFIG_BOARD_TYPE_CYBERVOC_V2_1`，工程默认板级）
- **目标芯片**：ESP32-S3（见 `config.json`）
- **网络能力**：双网络（Wi-Fi / ML307 4G），支持在部分状态下切换网络类型（具体以固件逻辑为准）
- **显示与触摸**：360×360 圆形触摸屏（QSPI ST77916 + CST816S）
- **音频**：ES8311（播放）+ ES7210（采集，麦克风 + 功放回采，支持设备端 AEC）
- **电量计**：BQ27220
- **姿态传感器**：QMA6100P（I2C 0x12，与音频 Codec 共用 I2C 总线），用于摇晃检测
- **说话指示灯**：GPIO19，低电平点亮，仅在设备说话（speaking）状态点亮

## 与 V2_0 的硬件差异

| 项目 | V2_0 | V2_1 |
|---|---|---|
| 开机 | PG2(GPIO7) 高电平自锁 | 硬件上电，无软件开机 |
| 关机键 | PG1(GPIO16)，按下为低 | PG1(GPIO40)，按下为高 |
| 关机方式 | 释放 PG2 自锁 | 长按 1.5s → 显示关机提示 2.5s → PG2(GPIO38) 输出 200ms 高脉冲断电 |
| 烧录 | 需一直按住开关机键 | 无需按住 |
| 姿态传感器 | QMI8658 | QMA6100P |
| 说话指示灯 | 无 | GPIO19 |
| 麦克风所在 TDM slot | slot 0 | **slot 2**（见下文） |
| 引脚 | — | I2S、LCD、SD、ML307、底座 UART、头部触摸等全部重新分配 |

### 电源键行为

- PG2 平时保持低电平；任何时刻输出高电平都会断电，因此 `main.cc` 在启动最早阶段即把 PG2 拉到非激活电平。
- 上电时若一直按着 PG1，需先检测到松开，并经过 3s 忽略窗口和一次空闲松开后，长按才会生效，避免开机按键被误判为关机长按。
- 相关时序参数（`KEY_*`）见 `config.h`。

## 音频通道（ES7210 TDM）

ES7210 以 TDM 输出 4 个 slot，顺序为 MIC1、MIC3、MIC2、MIC4。本板接线如下：

| TDM slot | ES7210 输入 | 原理图网络 | 用途 |
|---|---|---|---|
| slot 0 | MIC1 | `ADC_MIC1` | 麦克风 1（实测几乎收不到人声，未使用） |
| slot 1 | MIC3 | `ADC_MIC3`（功放 OUTP/OUTN 分压） | **AEC 回采参考** |
| slot 2 | MIC2 | `ADC_MIC2` | **麦克风（实际使用）** |
| slot 3 | MIC4 | 未接 | — |

`main/audio/codecs/box_audio_codec.cc` 在 V2_1 的 mic+ref 模式下读取完整 4 个 slot，取 slot 2 作麦克风、slot 1 作回采（常量 `kMrMicTdmSlot` / `kMrRefTdmSlot`）。V2_0 仍读取 slot 0/1。

## 引脚速查

| 功能 | 引脚 |
|---|---|
| I2S | MCLK=GPIO5，BCLK=GPIO15，WS=GPIO7，DIN=GPIO16，DOUT=GPIO6 |
| 功放使能 | GPIO4 |
| Codec / QMA6100P I2C | SDA=GPIO2，SCL=GPIO1 |
| LCD（QSPI） | PCLK=GPIO21，CS=GPIO10，D0=GPIO14，D1=GPIO9，D2=GPIO13，D3=GPIO46，RST=GPIO47，TE=GPIO12，背光=GPIO3 |
| 触摸 CST816S | INT=GPIO11 |
| 电源 | PG1 关机键=GPIO40，PG2 断电控制=GPIO38 |
| 头部触摸 | GPIO20（高电平有效） |
| 说话指示灯 | GPIO19（低电平点亮） |
| SD 卡（1 线） | CLK=GPIO48，CMD=GPIO45，D0=GPIO39 |
| ML307 4G | TX=GPIO8，RX=GPIO18，EN=GPIO17，UART2 |
| 底座 UART | TX=GPIO41，RX=GPIO42，UART1 |

以 `config.h` 为准。

## 编译与烧录

推荐使用根目录脚本编译并打包：

```bash
python scripts/release.py CyberVoc-Board-V2_1
```

或在 menuconfig 中选择 `CyberVoc V2.1` 后直接编译烧录：

```bash
idf.py build
idf.py -p /dev/ttyUSB0 flash monitor
```

## 已知问题

- **MIC1 几乎收不到人声**：原因待硬件确认（焊接、音孔或器件）。目前只用 MIC2 收音，不影响对话。
- **双麦声源定位（DOA）暂不可靠**：DOA 模式会自动挑选能量最大的两个 slot；MIC1 过弱，且播放时回采 slot 1 能量很大，可能被误选。启用前需先修复 MIC1，并将 DOA 固定为 slot 0 与 slot 2。

## 关键文件

- `config.h`：引脚映射与硬件参数（音频 I2S、I2C、LCD/TP、SD、ML307、电源键等）
- `config.json`：release 脚本构建变体与追加的 `sdkconfig` 片段
- `CyberVoc.cc/.h`：板级初始化与外设驱动集成（电源键、QMA6100P、BQ27220、说话指示灯等）
- `ui_bridge.*`：LVGL 页面与触摸手势桥接（与 UI 交互相关）

## 参考

- 根目录 `README.md`：项目总体说明、编译/烧录流程、License 与上游声明
