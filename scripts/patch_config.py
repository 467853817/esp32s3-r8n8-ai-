#!/usr/bin/env python3
"""Patch bread-compact-wifi config.json for ESP32-S3-N8R8 (8MB Flash)."""
import json
from pathlib import Path

p = Path("main/boards/bread-compact-wifi/config.json")
if not p.exists():
    raise SystemExit(f"ERROR: {p} not found")

cfg = json.loads(p.read_text(encoding="utf-8"))
builds = cfg.get("builds", [])
changed = False

for b in builds:
    if b.get("name") in ("bread-compact-wifi", "bread-compact-wifi-n8r8"):
        b["name"] = "bread-compact-wifi-n8r8"
        b["sdkconfig_append"] = [
            "CONFIG_OLED_SSD1306_128X32=y",
            "CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y",
            'CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions/v2/8m.csv"',
        ]
        changed = True
        print("Patched build:", b["name"])
        print("sdkconfig_append =", b["sdkconfig_append"])
        break

if not changed:
    # fallback: append a new build entry
    builds.append({
        "name": "bread-compact-wifi-n8r8",
        "sdkconfig_append": [
            "CONFIG_OLED_SSD1306_128X32=y",
            "CONFIG_ESPTOOLPY_FLASHSIZE_8MB=y",
            'CONFIG_PARTITION_TABLE_CUSTOM_FILENAME="partitions/v2/8m.csv"',
        ],
    })
    cfg["builds"] = builds
    changed = True
    print("Added new build: bread-compact-wifi-n8r8")

if not changed:
    raise SystemExit("ERROR: failed to patch config.json")

p.write_text(json.dumps(cfg, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")
print("OK: config.json patched for 8MB Flash + 8m partition table")
