#!/usr/bin/env python3
"""Entry point for the news-image-20261121 submission.

Copies the committed front page (page.png, sitting next to this file) to
the grader's output directory as entry.png. Standard library only, no
network, and the copy is byte-identical on every run.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "page.png")
    out_dir = os.environ.get("ENTRY_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print(f"wrote {dst} ({os.path.getsize(dst)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
