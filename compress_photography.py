#!/usr/bin/env python3
"""
Compress all images in images/PHOTOGRAPHY/ and subfolders:
- Resize to max 3000px width (keep aspect ratio)
- JPEG quality 85%
- Overwrites originals
- Uses PIL/Pillow
"""

import os
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("Pillow is required. Install with: pip install Pillow")
    raise SystemExit(1)

PHOTOGRAPHY_DIR = Path(__file__).resolve().parent / "images" / "PHOTOGRAPHY"
MAX_WIDTH = 3000
JPEG_QUALITY = 85
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".jpe", ".webp"}


def is_image(path: Path) -> bool:
    return path.suffix.lower() in IMAGE_EXTENSIONS


def optimize_image(path: Path) -> bool:
    """Resize (if needed) and compress image; overwrite original. Returns True on success."""
    try:
        with Image.open(path) as im:
            im.load()
            # JPEG needs RGB or L; PNG can keep RGBA
            if im.mode in ("RGBA", "P"):
                background = Image.new("RGB", im.size, (255, 255, 255))
                if im.mode == "P":
                    im = im.convert("RGBA")
                if im.mode == "RGBA":
                    background.paste(im, mask=im.split()[-1])
                    im = background
                else:
                    im = im.convert("RGB")
            elif im.mode not in ("RGB", "L"):
                im = im.convert("RGB")

            width, height = im.size
            if width > MAX_WIDTH:
                ratio = MAX_WIDTH / width
                new_size = (MAX_WIDTH, int(height * ratio))
                im = im.resize(new_size, Image.Resampling.LANCZOS)

            ext = path.suffix.lower()
            if ext in (".jpg", ".jpeg", ".jpe"):
                im.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            elif ext == ".png":
                im.save(path, "PNG", optimize=True)
            elif ext == ".webp":
                im.save(path, "WEBP", quality=JPEG_QUALITY, method=6)
            else:
                im.save(path, "JPEG", quality=JPEG_QUALITY, optimize=True)
            return True
    except Exception as e:
        print(f"  Error: {e}")
        return False


def main():
    if not PHOTOGRAPHY_DIR.is_dir():
        print(f"Directory not found: {PHOTOGRAPHY_DIR}")
        raise SystemExit(1)

    files = sorted(f for f in PHOTOGRAPHY_DIR.rglob("*") if f.is_file() and is_image(f))
    total = len(files)
    if total == 0:
        print("No image files found in", PHOTOGRAPHY_DIR)
        return

    print(f"Found {total} image(s) in {PHOTOGRAPHY_DIR}")
    print(f"Settings: max width={MAX_WIDTH}px, JPEG quality={JPEG_QUALITY}%\n")

    ok = 0
    for i, path in enumerate(files, 1):
        rel = path.relative_to(PHOTOGRAPHY_DIR)
        print(f"[{i}/{total}] {rel} ... ", end="", flush=True)
        if optimize_image(path):
            print("OK")
            ok += 1
        else:
            print("SKIP")

    print(f"\nDone. Processed {ok}/{total} successfully.")


if __name__ == "__main__":
    main()
