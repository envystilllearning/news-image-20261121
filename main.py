#!/usr/bin/env python3
"""Entry point: write the finished front page to the output directory.

The page is composed by build_page.py and committed as page.png.
This program verifies the committed asset, then copies it out —
standard library only, no network, same bytes on every run.
"""
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def main():
    src = os.path.join(HERE, "page.png")
    if not os.path.isfile(src):
        print("error: page.png is missing next to main.py", file=sys.stderr)
        return 1
    with open(src, "rb") as fh:
        header = fh.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        print("error: page.png is not a PNG file", file=sys.stderr)
        return 1

    out_dir = os.environ.get("ENTRY_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")

    # Copy via a temp file in the same directory, then atomically
    # rename it into place so entry.png is never seen half-written.
    fd, tmp = tempfile.mkstemp(dir=out_dir, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "wb") as out, open(src, "rb") as fh:
            shutil.copyfileobj(fh, out)
        size = os.path.getsize(tmp)
        os.replace(tmp, dst)
    except BaseException:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise

    print(size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
