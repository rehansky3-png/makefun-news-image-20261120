#!/usr/bin/env python3
"""Entry point for the make.fun news-image-20261120 round 2 entry.

Copies the bundled front-page image (entry.png, 1024x1024, under
1 MiB) to $MAKEFUN_OUTPUT_DIR (default "out"), validating it is a
real PNG of the right size first. Standard library only, no network.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
    python3 main.py --self-test
"""
import hashlib
import os
import shutil
import sys
import tempfile
from pathlib import Path

ENTRY = Path(__file__).resolve().parent / "entry.png"
MAX_BYTES = 1_048_576
WANT_W, WANT_H = 1024, 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(data):
    """Return (width, height) from PNG bytes, or raise ValueError."""
    if len(data) < 33 or data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic)")
    if data[12:16] != b"IHDR":
        raise ValueError("not a PNG file (missing IHDR)")
    w = int.from_bytes(data[16:20], "big")
    h = int.from_bytes(data[20:24], "big")
    return w, h


def validate(data):
    """Check the bundled image: PNG, 1024x1024, under 1 MiB."""
    if len(data) > MAX_BYTES:
        raise ValueError(f"entry.png is {len(data)} bytes, over 1 MiB")
    w, h = read_png_size(data)
    if (w, h) != (WANT_W, WANT_H):
        raise ValueError(f"entry.png is {w}x{h}, expected 1024x1024")
    return len(data)


def copy_entry(out_dir):
    """Copy entry.png into out_dir, validating first. Returns (path, size)."""
    data = ENTRY.read_bytes()
    size = validate(data)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(ENTRY, dest)
    return dest, size


def self_test():
    """Copy the entry twice into fresh temp dirs; outputs must match."""
    data = ENTRY.read_bytes()
    want = hashlib.sha256(data).hexdigest()
    validate(data)
    digests = []
    with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
        for d in (d1, d2):
            dest, size = copy_entry(d)
            got = hashlib.sha256(dest.read_bytes()).hexdigest()
            digests.append(got)
            print(f"self-test copy -> {dest} ({size} bytes, sha256 {got[:16]}...)")
    if digests[0] != digests[1] or digests[0] != want:
        raise SystemExit("self-test FAILED: outputs differ")
    print("self-test OK: two copies byte-identical, valid 1024x1024 PNG")


def main(argv):
    if "--self-test" in argv:
        self_test()
        return 0
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    dest, size = copy_entry(out_dir)
    print(f"wrote {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
