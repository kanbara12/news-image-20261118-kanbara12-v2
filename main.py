#!/usr/bin/env python3
"""news-image-20261118 v2 entrypoint: copy the pre-rendered front page to the
output directory the kit expects. Stdlib only, no network, deterministic.
"""
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    size = os.path.getsize(dst)
    if size > 1024 * 1024:
        print("entry.png exceeds 1 MiB: %d bytes" % size, file=sys.stderr)
        return 1
    print("wrote %s (%d bytes)" % (dst, size))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
