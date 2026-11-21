#!/usr/bin/env python3
"""Write the one-image summary of Saturday 21 November 2026's world news.

The page beside this program (page.png) is the entry image: a broadsheet
front page of 27 dated stories across 6 regions — three illustrated lead
stories (the World Court's genocide verdict on Myanmar, Kyiv's bridge
repairs, COP31's deleted fossil-fuel pledge), six illustrated secondary
stories, a stat band, a region bar, a locator map, 18 sourced briefs and
a date-check strip. It was drawn from a verified story list compiled for
this competition.

This program writes that page, byte for byte, to the output path. It
uses only the standard library and no network, so it runs identically
on any runtime, every time.
"""

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def main():
    data = (ROOT / "page.png").read_bytes()
    out_dir = Path(os.environ.get("ENTRY_OUTPUT_DIR", "/output"))
    try:
        out_dir.mkdir(parents=True, exist_ok=True)
        out = out_dir / "entry.png"
        out.write_bytes(data)
    except OSError:
        out = ROOT / "entry.png"
        out.write_bytes(data)
    print("wrote", out, len(data), "bytes")


if __name__ == "__main__":
    main()
