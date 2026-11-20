#!/usr/bin/env python3
"""THE WORLD -- Friday 20 November 2026: one image of the day's news.

This program copies the front-page image shipped in this repository
(entry.png) to the output directory as entry.png. It uses only the
Python standard library, reads no network, and is deterministic:
every run writes the same bytes.

Usage:
    mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
"""

import hashlib
import os
import shutil
import struct
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "entry.png")
MAX_BYTES = 1_048_576
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def read_png_size(path):
    """Return (width, height) parsed from a PNG IHDR chunk."""
    with open(path, "rb") as fh:
        head = fh.read(33)
    if len(head) < 33 or head[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file")
    if head[12:16] != b"IHDR":
        raise ValueError("PNG has no IHDR chunk")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def self_test():
    """Copy twice into fresh dirs and check the bytes are identical."""
    digests = []
    for _ in range(2):
        with tempfile.TemporaryDirectory() as tmp:
            os.environ["MAKEFUN_OUTPUT_DIR"] = tmp
            if main() != 0:
                return 1
            with open(os.path.join(tmp, "entry.png"), "rb") as fh:
                digests.append(hashlib.sha256(fh.read()).hexdigest())
    if digests[0] != digests[1]:
        print("self-test FAILED: two runs differ")
        return 1
    print("self-test OK: deterministic, sha256 %s" % digests[0])
    return 0


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dest = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SOURCE, dest)
    size = os.path.getsize(dest)
    if size > MAX_BYTES:
        raise ValueError("entry.png is %d bytes, over the 1 MiB limit" % size)
    width, height = read_png_size(dest)
    if (width, height) != (1024, 1024):
        raise ValueError("entry.png is %dx%d, expected 1024x1024"
                         % (width, height))
    print("wrote %s (%d bytes, %dx%d)" % (dest, size, width, height))
    return 0


if __name__ == "__main__":
    if "--self-test" in sys.argv:
        sys.exit(self_test())
    sys.exit(main())
