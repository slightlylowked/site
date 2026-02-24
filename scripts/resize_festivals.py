#!/usr/bin/env python3
"""Resize and compress images in images/PHOTOGRAPHY/FESTIVALS/ for web.
   Max dimension 1920px, JPEG quality 85. Overwrites originals."""
import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Install Pillow: pip install Pillow", file=sys.stderr)
    sys.exit(1)

FESTIVALS_DIR = Path(__file__).resolve().parent.parent / "images" / "PHOTOGRAPHY" / "FESTIVALS"
MAX_PX = 1920
JPEG_QUALITY = 85

def main():
    if not FESTIVALS_DIR.is_dir():
        print(f"Directory not found: {FESTIVALS_DIR}", file=sys.stderr)
        sys.exit(1)
    count = 0
    for path in sorted(FESTIVALS_DIR.iterdir()):
        if path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
            continue
        try:
            with Image.open(path) as im:
                im.load()
                if im.mode in ("RGBA", "P"):
                    im = im.convert("RGB")
                w, h = im.size
                if max(w, h) <= MAX_PX:
                    continue
                if w >= h:
                    new_w, new_h = MAX_PX, int(h * MAX_PX / w)
                else:
                    new_w, new_h = int(w * MAX_PX / h), MAX_PX
                im = im.resize((new_w, new_h), Image.Resampling.LANCZOS)
                out_path = path.with_suffix(".jpg")
                im.save(out_path, "JPEG", quality=JPEG_QUALITY, optimize=True)
                if out_path != path and path.exists():
                    path.unlink()
            count += 1
            print(path.name)
        except Exception as e:
            print(f"Skip {path.name}: {e}", file=sys.stderr)
    print(f"Processed {count} images.", file=sys.stderr)

if __name__ == "__main__":
    main()
