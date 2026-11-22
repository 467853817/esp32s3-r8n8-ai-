# bread-compact-wifi-n8r8 板级源码（可改）

本目录是 **ESP32-S3-N8R8** 适配用的板级文件。  
GitHub Actions 编译时会把这里的文件覆盖到官方 `xiaozhi-esp32` v2.5.0 的 `main/boards/bread-compact-wifi/` 再构建。

## 你可以改什么

| 文件 | 用途 |
|------|------|
| `config.h` | **引脚定义**（麦克风 / 功放 / OLED / 按键） |
| `config.json` | Flash 大小、分区表、OLED 分辨率、构建变体名 |
| `compact_wifi_board.cc` | 板级初始化逻辑（显示、按键行为、音频编解码） |

改完后：

1. 提交到 `main`（或在网页上直接编辑保存）
2. 打开 Actions → **Build Xiaozhi for ESP32-S3-N8R8** → Run workflow
3. 下载新的 `merged-binary.bin` 烧录

## 当前默认引脚（与官方 bread-compact-wifi 一致）

- OLED SDA=41 SCL=42
- MIC WS=4 SCK=5 SD=6
- SPK DIN=7 BCLK=15 LRC=16
- BOOT=0，音量±=40/39

改 GPIO 时请避开 **GPIO33–37**（Octal PSRAM 占用）。

## 许可

板级逻辑来源于 [78/xiaozhi-esp32](https://github.com/78/xiaozhi-esp32) v2.5.0，按上游项目许可证使用。
