# 赛博喵伴（CyberVoc）ESP32-S3 固件

![CyberVoc](/docs/v0/cybervoc_pretty_bg.png)

本仓库是基于开源项目 [`78/xiaozhi-esp32`](https://github.com/78/xiaozhi-esp32) 的工程框架进行裁剪与二次开发的固件工程，**仅保留并维护**我们自己的硬件板级实现：

- `main/boards/CyberVoc-Board-V1_2`
- `main/boards/CyberVoc-Board-V2_0`
- `main/boards/CyberVoc-Board-V2_1`

如需完整的多开发板支持与更通用的工程能力，请参考上游项目。

---

## 功能概览

- **ESP32-S3** 语音对话固件工程（ESP-IDF）
- 圆形触摸屏 UI（LVGL + `esp_lvgl_adapter`）
- 音频采集/播放、语音唤醒（依赖 `esp-sr`）
-（部分硬件）4G 模组支持与网络切换（板级能力）
- OTA（工程内含压缩 OTA 相关组件与示例/文档）

> 具体功能与交互细节，以板级 README 与代码实现为准。

---

## 支持的硬件

本仓库仅保证以下硬件的可用性：

| 板级 | 目录 | menuconfig 选项（Kconfig 符号） |
|---|---|---|
| **CyberVoc-Board-V1_2** | `main/boards/CyberVoc-Board-V1_2` | `CyberVoc`（`BOARD_TYPE_CYBERVOC`） |
| **CyberVoc-Board-V2_0** | `main/boards/CyberVoc-Board-V2_0` | `CyberVoc V2.0`（`BOARD_TYPE_CYBERVOC_V2_0`） |
| **CyberVoc-Board-V2_1** | `main/boards/CyberVoc-Board-V2_1` | `CyberVoc V2.1`（`BOARD_TYPE_CYBERVOC_V2_1`，**默认板级**） |

### 主要硬件差异

| 项目 | V1_2 | V2_0 | V2_1 |
|---|---|---|---|
| 烧录时是否需按住开关机键 | 不需要 | **需要一直按住** | 不需要 |
| 电源方式 | `POWER_CTRL`(GPIO9) 控制 | PG2(GPIO7) 高电平自锁；PG1(GPIO16) 按键 | 硬件上电；PG1(GPIO40) 长按 1.5s 关机，PG2(GPIO38) 输出 200ms 高脉冲断电 |
| 网络 | Wi-Fi | Wi-Fi / ML307 4G 双网 | Wi-Fi / ML307 4G 双网 |
| 音频采集 | ES7210 + ES8311 | ES7210 麦克风 + 功放回采 | ES7210 麦克风 + 功放回采（麦克风在 TDM slot 2） |
| 姿态传感器 | — | QMI8658 | QMA6100P（I2C 0x12） |
| 说话指示灯 | — | — | GPIO19，低电平点亮 |

> 不确定手上是哪块板时，可先按烧录时是否需要按住开关机键区分 V2_0；V1_2 与 V2_1 再按 PCB 丝印区分。

各板引脚与硬件参数见各自目录下的 `config.h` / `config.json`，详细说明见板级 README。

---

## 固件下载

预编译固件统一放在仓库根目录的 `releases/` 文件夹中。用户如果只需要烧录固件，可以只下载这个文件夹里的对应 `.zip` 文件，不需要下载完整源码。

当前固件包：

- `releases/v2.0.5.6_CyberVoc-Board-V2_0.zip`

V1_2 与 V2_1 暂未提供预编译包，请按下文用发布脚本自行生成。固件包命名规则为 `v<版本号>_<板级名>.zip`，每个 `.zip` 内包含 `merged-binary.bin`，从 `0x0` 地址整体烧录即可：

```bash
python scripts/release.py CyberVoc-Board-V1_2
python scripts/release.py CyberVoc-Board-V2_0
python scripts/release.py CyberVoc-Board-V2_1
```

> 若 `releases/` 下已存在同名 zip，脚本会跳过该板级；需要重新生成时请先删除旧包。

---

## 快速开始（编译 / 烧录）

### 1) 准备 ESP-IDF 环境

- **要求**：ESP-IDF `>= 5.4.0`（详见 `main/idf_component.yml`）
- 建议使用与你当前工程验证一致的版本（例如日志中为 `v5.5.2`）

确保已正确安装并导出环境变量（`idf.py` 可用）。

### 2) 选择目标芯片

```bash
idf.py set-target esp32s3
```

### 3) 按板级编译（推荐）

本仓库的板级构建参数由 `main/boards/<board>/config.json` 描述，使用 `scripts/release.py` 进行自动化构建：

```bash
python scripts/release.py CyberVoc-Board-V1_2
# 或
python scripts/release.py CyberVoc-Board-V2_0
# 或
python scripts/release.py CyberVoc-Board-V2_1
```

脚本会读取 `config.json` 并追加对应的 `sdkconfig` 片段，然后完成构建与打包。

> 注意：脚本会执行 `idf.py set-target` 并**直接改写根目录的 `sdkconfig`**（在末尾追加板级配置）。提交代码前请检查 `sdkconfig` 的改动，避免把某个板级的配置误提交为默认配置。

可用以下命令查看脚本识别到的板级与变体：

```bash
python scripts/release.py --list-boards
```

### 4) 直接使用 idf.py 编译

```bash
idf.py build
```

> 本仓库已包含 `sdkconfig`，默认板级为 **V2_1**（`sdkconfig.defaults` 与 Kconfig 默认值均为 `CONFIG_BOARD_TYPE_CYBERVOC_V2_1`），克隆后直接编译得到的是 V2_1 固件。编译其他板级前请切换板型；编出的始终是 `sdkconfig` 里**当前选中**的板级，可用以下命令确认：
>
> ```bash
> grep "CONFIG_BOARD_TYPE_CYBERVOC" sdkconfig
> ```

如需手动选择板型与 UI 风格，可进入配置菜单：

```bash
idf.py menuconfig
```

然后在 `Xiaozhi Assistant` → **Board Type** 中选择对应板级（选项名见上文“支持的硬件”表格）。

### 5) 烧录与串口监视

```bash
idf.py -p /dev/ttyUSB0 flash monitor
```

- 串口号按实际情况替换（Windows 下为 `COMx`）。
- **V2_0** 烧录全程需按住开关机键，否则烧录中途会断电；V1_2 / V2_1 无需按住。

---

## 常见问题

### 如何从日志判断设备有没有听到说话

对话流程的关键日志如下：

```text
Application: STATE: listening   ← 进入聆听
Application: >> 你在干嘛？        ← 服务器识别到的说话内容
Application: STATE: speaking    ← 服务器开始回复
Application: << 没干嘛呀…         ← 回复文字
```

进入 `listening` 后说话却始终没有 `>>` 日志，说明设备没有采到有效人声或音量过低，应优先检查麦克风的 TDM slot 映射与硬件。

### V2_1 能唤醒但聆听时听不到说话

V2_1 的主麦克风接在 ES7210 的 MIC2（TDM slot 2），与 V2_0 读取的 slot 0 不同。固件已在 `main/audio/codecs/box_audio_codec.cc` 中按板级处理；若修改该文件或移植到新板，请确认麦克风与回采所用的 slot，详见 `main/boards/CyberVoc-Board-V2_1/README.md`。

---

## 目录结构（精简说明）

- `main/`：应用主工程
  - `boards/`：板级实现
    - `CyberVoc-Board-V1_2/`
    - `CyberVoc-Board-V2_0/`
    - `CyberVoc-Board-V2_1/`
    - `common/`：通用板级抽象/复用（WiFi/4G/双网等）
- `components/`：工程依赖组件（含第三方组件与自研组件）
- `docs/`：协议/使用/扩展文档（如 MCP、WebSocket/MQTT 等）
- `scripts/`：构建/资源转换/发布脚本
- `partitions/`：分区表相关

板级说明请优先阅读：

- `main/boards/CyberVoc-Board-V1_2/README.md`
- `main/boards/CyberVoc-Board-V2_0/README.md`
- `main/boards/CyberVoc-Board-V2_1/README.md`
- `docs/custom-board.md`（上游风格的板级扩展说明）

---

## 上游项目与致谢

本工程框架沿用并参考了上游开源项目：

- 上游：[`78/xiaozhi-esp32`](https://github.com/78/xiaozhi-esp32)

我们在此基础上进行了**裁剪**（移除大量上游板级适配）与**板级定制开发**（仅保留 `CyberVoc-Board-V1_2`、`CyberVoc-Board-V2_0` 与 `CyberVoc-Board-V2_1`）。

同时感谢 ESP-IDF、LVGL 及本工程所使用的各组件/库作者与贡献者。

---

## 许可证（License）

本仓库根目录提供 `LICENSE`，当前为 **MIT License**。

> 注意：本仓库包含多个第三方依赖与组件，它们可能具有各自的许可证（例如 `components/` 与部分子目录中存在独立 `LICENSE` 文件）。在二次分发时请一并遵守对应条款。

---

## 贡献（Contributing）

欢迎提交 Issue / PR。为便于维护：

- 仅保证 `CyberVoc-Board-V1_2`、`CyberVoc-Board-V2_0` 与 `CyberVoc-Board-V2_1` 的可用性与回归
- 变更请尽量保持板级差异收敛在各自 `main/boards/<board>/` 目录内
