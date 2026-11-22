# ESP32-S3-N8R8 小智 AI 固件（手机可编译 / 可改源码）

本仓库为 **ESP32-S3-N8R8**（8MB Flash + 8MB Octal PSRAM）提供可直接用手机编译、烧录的小智 AI 固件。

基于官方 [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) **v2.5.0**，板级配置使用 `bread-compact-wifi`（0.91 寸 128×32 SSD1306 OLED），并强制 **8MB 分区表**。

---

## 0. 可修改的板级源码（重点）

适配相关源码已放在仓库内，**可直接改**：

```
boards/bread-compact-wifi-n8r8/
├── config.h                 # 引脚定义（麦克风/功放/OLED/按键）
├── config.json              # 8MB Flash、分区表、构建名
├── compact_wifi_board.cc    # 板级初始化与按键逻辑
└── README.md
```

修改方式（手机也可）：

1. 打开仓库 → 进入 `boards/bread-compact-wifi-n8r8/`
2. 点开 `config.h` 或其它文件 → 铅笔图标编辑 → Commit
3. 到 **Actions** 里重新 **Run workflow**，下载新固件

编译时会把该目录覆盖到上游 `main/boards/bread-compact-wifi/` 再构建。

---

## 1. 硬件确认

| 项目 | 配置 |
|------|------|
| 主控 | ESP32-S3-N8R8（8MB Quad Flash + 8MB Octal PSRAM） |
| OLED | 0.91 寸 128×32 SSD1306，I²C 地址 0x3C |
| 麦克风 | INMP441（I²S） |
| 功放 | MAX98357A（I²S） |
| 分区 | `partitions/v2/8m.csv`（ota 各约 3MB，assets 2MB @ `0x600000`） |
| PSRAM | Octal 80MHz（上游 sdkconfig.defaults.esp32s3 已正确） |

### 接线表

**OLED**
- GND → GND　VCC → 3.3V　SCL → **GPIO42**　SDA → **GPIO41**

**INMP441**
- VDD → 3.3V　GND → GND　WS → **GPIO4**　SCK → **GPIO5**　SD → **GPIO6**　L/R → GND

**MAX98357A**
- VIN → 5V（或模块支持的 3.3V）　GND → GND　DIN → **GPIO7**　BCLK → **GPIO15**　LRC → **GPIO16**

板载 RGB LED = GPIO48，BOOT = GPIO0。引脚已避开 Octal PSRAM 的 GPIO33–37。

---

## 2. 手机编译（GitHub Actions）

1. 打开：https://github.com/467853817/esp32s3-r8n8-ai-
2. **Actions** → **Build Xiaozhi for ESP32-S3-N8R8** → **Run workflow**
3. 约 10–20 分钟后，Artifacts 下载 `xiaozhi-v2.5.0-bread-compact-wifi-n8r8`
4. 解压得到 `merged-binary.bin`

若 Actions 被禁用：Settings → Actions → General → Allow all actions。

---

## 3. 手机烧录主固件（ESPFlash）

1. 芯片 **ESP32-S3**，地址 **0x0**，选 `merged-binary.bin`
2. 进下载模式：按住 **BOOT** → 点 **RST** → 松开 BOOT
3. 烧完按 RST 重启

### 单独烧 assets（唤醒词等，不抹主程序）

- 地址：**`0x600000`**
- 文件：`assets.bin`
- 模式：**Raw Binary / As Raw**
- 不要用 0x0 烧 assets，否则会覆盖主程序

---

## 4. 配网与测试

- 首次启动按提示配网；或连设备热点后按网页提示操作
- 短按 **BOOT** 开始/结束对话
- 需要离线唤醒时，再烧入对应的 `assets.bin` 到 `0x600000`

---

## 5. 失败排查

| 现象 | 处理 |
|------|------|
| Actions 无日志 | 开启仓库 Actions 权限 |
| 编译失败 | 看日志是否成功 Overlay 了 board 文件 |
| 烧录后黑屏 | 重新 BOOT+RST 进下载模式，换 USB 口 |
| OLED 无显示 | 确认 SDA=41 SCL=42 |
| 无声音 | 按接线表重接麦/喇叭；短按 BOOT 再试 |
| assets 烧录报 segment size | 必须用 Raw/As Raw，地址 0x600000 |

---

## 6. 说明

- 完整上游工程仍由 Actions 每次拉取官方 v2.5.0；本仓库只维护 **N8R8 板级覆盖层** 与编译脚本。
- 旧版 `scripts/patch_config.py` 已不再作为主流程（逻辑已固化进 `boards/.../config.json`）。
