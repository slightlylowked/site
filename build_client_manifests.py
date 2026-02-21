#!/usr/bin/env python3
"""
Scan images/PHOTOGRAPHY/CLIENT/ subfolders and write client-manifests.json
with a list of image filenames per client folder. Run this after adding or
removing photos in any client folder so the photography page can display them.
"""
import json
import os
from pathlib import Path

CLIENT_DIR = Path(__file__).resolve().parent / "images" / "PHOTOGRAPHY" / "CLIENT"
MANIFESTS_PATH = Path(__file__).resolve().parent / "client-manifests.json"
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif", ".webp"}


def main():
    if not CLIENT_DIR.is_dir():
        os.makedirs(CLIENT_DIR, exist_ok=True)
        with open(MANIFESTS_PATH, "w") as f:
            json.dump({}, f, indent=2)
        print("Created", CLIENT_DIR, "and empty", MANIFESTS_PATH)
        return

    manifests = {}
    for subdir in sorted(CLIENT_DIR.iterdir()):
        if not subdir.is_dir():
            continue
        name = subdir.name
        if name.startswith("."):
            continue
        files = []
        for f in sorted(subdir.iterdir()):
            if f.is_file() and f.suffix.lower() in IMAGE_EXTENSIONS:
                files.append(f.name)
        manifests[name] = files

    with open(MANIFESTS_PATH, "w") as f:
        json.dump(manifests, f, indent=2)

    print("Wrote", MANIFESTS_PATH, "with", len(manifests), "client(s).")
    for k, v in manifests.items():
        print("  ", k, "->", len(v), "image(s)")


if __name__ == "__main__":
    main()
