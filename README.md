[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — the world in one day

One image that sums up Saturday 21 November 2026: a broadsheet front
page of 35 dated stories across 6 regions. Three lead stories and ten
secondary stories each get a full illustration panel with a red banner
label; 22 further stories run as sourced briefs. A stat band, a region
bar, a locator map with a numbered legend, and a date-check box (what
was left out as Friday's news, and what could not be confirmed) frame
the page.

## How it was made

- The story list (`dataset.md`) was compiled for this competition and
  verified against dated Saturday reporting: every story happened, or
  was first reported, on Saturday 21 November 2026. Day-old items were
  caught and corrected — the Wellington Test was on day three, not day
  two, and Friday's market closes were dropped in favour of Saturday's
  own stories (bitcoin's two-year low, the Davao emergency landing,
  Las Vegas practice).
- Each illustration was generated fresh as a separate text-free
  element (flat editorial style, cream ground, black ink, one red
  accent) and is committed under `elements/`.
- `build_page.py` typesets the whole page around the elements with
  Pillow: masthead, stat band, region bar, panelled and labelled
  stories, map, briefs, date check. Because every word is set by the
  program from the verified list, nothing on the page is misspelled.
- The composed page is committed as `page.png` (1024×1024).
  `main.py` copies it to the output directory — standard library
  only, no network, byte-identical on every run.

## Files

- `main.py` — entry point; writes `entry.png` to `$ENTRY_OUTPUT_DIR`
  (or `/output`).
- `build_page.py` — the compositor that built `page.png`.
- `page.png` — the finished front page.
- `dataset.md` — the verified story list the page was set from.
- `elements/` — the 14 fresh illustration elements.
- `LICENSE` — MIT.
