#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

failed = []

for png in Path(".").rglob("*.png"):
    # Skip hidden directories (e.g. .git, .github)
    if any(part.startswith(".") for part in png.parts):
        continue
    webp = png.with_suffix(".webp")
    print(f"Converting {png} -> {webp}", flush=True)
    result = subprocess.run(
        [
            "ffmpeg", "-i", str(png),
            "-c:v", "libwebp",
            "-q:v", "100",
            "-compression_level", "6",
            str(webp), "-y",
        ],
        stdin=subprocess.DEVNULL,
    )
    if result.returncode != 0:
        print(f"WARNING: failed to convert {png}", file=sys.stderr, flush=True)
        failed.append(str(png))

if failed:
    print(f"\n{len(failed)} file(s) failed to convert:", file=sys.stderr)
    for f in failed:
        print(f"  {f}", file=sys.stderr)
    sys.exit(1)
