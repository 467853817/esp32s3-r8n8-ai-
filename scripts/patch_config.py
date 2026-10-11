#!/usr/bin/env python3
"""Patch bread-compact-wifi config.json for ESP32-S3-N8R8 (8MB Flash)."""
import json
from pathlib import Path

p = Path("main/boards/bread-compact-wifi/config.json")
if not p.exists():
    raise SystemExit(f"ERROR: {p} not found")

cfg = json.loads(p.read_text(encoding="utf-8"))
changed = False
for b in cfg.get("builds", []):
    if b.get("name") == "bread-compact-wifi":
        b["sdkconfig_append"] = [
            "CONFIG_OLED_SSD1306_128X32=y",
            "CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y",
            'CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions/v2/8m.csv"',
        ]
        changed = True
        print("Patched build:", b["name"])
        print("sdkconfig_append =", b["sdkconfig_append"])

if not changed:
    raise SystemExit("ERROR: bread-compact-wifi build entry not found")

p.write_text(json.dumps(cfg, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
print("OK: config.json patched for 8MB Flash + 8m partition table")
