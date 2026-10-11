# ESP32-S3-N8R8 小智 AI 固件（手机可编译）

本仓库专门为 **ESP32-S3-N8R8**（8MB Flash + 8MB Octal PSRAM）制作可直接用手机烧录的小智 AI 固件。

基于官方 [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) **v2.5.0**，板级配置使用 `bread-compact-wifi`（0.91 寸 128×32 SSD1306 OLED），并强制使用 **8MB 分区表**。

---

## 1. 硬件确认（已核对源码）

| 项目 | 配置 |
|------|------|
| 主控 | ESP32-S3-N8R8（8MB Quad Flash + 8MB Octal PSRAM） |
| OLED | 0.91 寸 128×32 SSD1306，I²C 地址 0x3C |
| 麦克风 | INMP441（I²S） |
| 功放 | MAX98357A（I²S） |
| 分区 | `partitions/v2/8m.csv`（ota_0/ota_1 各约 3MB，assets 2MB） |
| PSRAM | Octal 80MHz（上游 `sdkconfig.defaults.esp32s3` 已正确） |

### 接线表（面包板 + 杜邦线）

**OLED**
- GND → GND
- VCC → 3.3V
- SCL → **GPIO42**
- SDA → **GPIO41**

**INMP441 麦克风**
- VDD → 3.3V
- GND → GND
- WS  → **GPIO4**
- SCK → **GPIO5**
- SD  → **GPIO6**
- L/R → GND（左声道）

**MAX98357A 功放 + 喇叭**
- VIN → 5V（或模块支持的 3.3V）
- GND → GND
- DIN → **GPIO7**
- BCLK → **GPIO15**
- LRC → **GPIO16**

板载 RGB LED = GPIO48，BOOT 按钮 = GPIO0。
以上引脚已避开 Octal PSRAM 占用的 GPIO33–37。

---

## 2. 如何用手机编译（GitHub Actions）

1. 打开本仓库页面：https://github.com/467853817/esp32s3-r8n8-ai-
2. 点击上方 **Actions** 标签。
3. 左侧选择 **Build Xiaozhi for ESP32-S3-N8R8**。
4. 右侧点击 **Run workflow** → 选 `main` → 再点绿色 **Run workflow**。
5. 等待约 10–20 分钟（第一次会下载 ESP-IDF 和依赖）。
6. 编译成功后，点进最新一次运行记录 → 最下方 **Artifacts** → 下载 `xiaozhi-v2.5.0-bread-compact-wifi-n8r8`。
7. 解压后得到 `merged-binary.bin`（或 zip 里的同名文件）。

> 如果 Actions 页面提示未启用，请到仓库 **Settings → Actions → General**，选择 **Allow all actions and reusable workflows** 并保存。

---

## 3. 用手机烧录（华为畅享 50 + ESPFlash）

1. 手机安装 **ESPFlash**（你以前给 ESP32-C3 烧过，同一个 App）。
2. 开发板用**支持数据的 USB-C 线**通过 OTG 接到手机。
   - 双 USB-C 板子：先试靠近芯片/天线一侧的口，进不了下载模式就换另一个。
3. 进入下载模式：
   - 按住 **BOOT** 不放 → 点一下 **RST** → 松开 BOOT。
4. 打开 ESPFlash：
   - 芯片选择 **ESP32-S3**
   - 烧录地址填 **0x0**
   - 选择刚才下载的 `merged-binary.bin`
   - 开始烧录。
5. 烧完后按一下 **RST** 重启。

---

## 4. 配网与测试

- 首次启动后，OLED 会显示状态或提示配网。
- 按 **BOOT** 键可进入配网模式（具体提示以固件为准）。
- 连接成功后，按 BOOT 开始对话；触摸/音量按键为可选功能。
- 小智服务端需要设备激活，按固件提示操作即可，不要假设一定是 `192.168.4.1`。

---

## 5. 失败排查

| 现象 | 可能原因 | 处理 |
|------|----------|------|
| Actions 直接失败且没有日志 | 仓库未开启 Actions | Settings → Actions → Allow all actions |
| 编译报分区/Flash 错误 | 补丁没生效 | 看日志是否有 “OK: config.json patched” |
| 烧录后黑屏/重启循环 | 没进下载模式或烧错口 | 重新按 BOOT+RST 进下载模式，换 USB 口 |
| OLED 无显示 | 接线或地址不对 | 确认 SDA=41 SCL=42，地址 0x3C |
| 有画面但无声音 | 音频模块未接或接线错 | 按上面引脚表重接 |
| PSRAM 报错 | 极少见（上游已配 Octal） | 把完整串口日志发出来 |

---

## 6. 重要说明

- 本仓库**只包含** GitHub Actions 工作流和补丁脚本，**不包含**完整源码。每次构建会自动拉取官方 v2.5.0 标签。
- 不要直接使用 16302.com 上的预编译固件，除非确认它使用了 8MB 分区表。
- 本仓库与你的 `ESP32-C3-AutoClicker` 完全独立，互不影响。

编译成功后把 Artifacts 下载链接或截图发给我，我可以继续帮你看日志或调整。
