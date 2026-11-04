#!/usr/bin/env python3
"""Inject a release signingConfig into the Capacitor-generated app/build.gradle."""
from pathlib import Path
import sys

p = Path("app/build.gradle")
if not p.exists():
    sys.exit(f"missing {p.resolve()}")

text = p.read_text()
marker = "signingConfig signingConfigs.release"

if marker not in text:
    needle = "minifyEnabled false"
    idx = text.find(needle)
    if idx < 0:
        print(text)
        sys.exit("minifyEnabled false not found")
    line_start = text.rfind("\n", 0, idx) + 1
    indent = text[line_start:idx]
    text = text[:line_start] + indent + marker + "\n" + text[line_start:]

if "signingConfigs {" not in text:
    needle = "    buildTypes {"
    block = """    signingConfigs {
        release {
            storeFile file(System.getenv("KEYSTORE_FILE"))
            storePassword System.getenv("KEYSTORE_PASSWORD")
            keyAlias System.getenv("KEY_ALIAS")
            keyPassword System.getenv("KEY_PASSWORD")
        }
    }
    buildTypes {"""
    if needle not in text:
        print(text)
        sys.exit("buildTypes block not found")
    text = text.replace(needle, block, 1)

p.write_text(text)
print("signing config injected")
