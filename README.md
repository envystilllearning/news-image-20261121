[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# Saturday 21 November 2026 — the world in one day

One newspaper front page that sums up Saturday 21 November 2026 in a single
image: 35 stories, each with its source named on the page. Three lead stories
run across the top — the world court's genocide ruling against Myanmar, the
400-drone barrage on Ukraine that put two missiles into Poland, and COP31
running past its deadline with no deal. Ten featured stories follow in a
grid, a dotted world map pins all thirteen featured stories to where they
happened, and 22 briefs fill the rest of the page. A red date-check strip at
the foot separates Saturday's news from Friday's and flags what was still
unconfirmed when the page was drawn.

Every story on the page was checked against reporting dated Saturday
21 November 2026; the full story list and its sources are kept in
`dataset.md`. Two items from earlier drafts were caught and fixed by that
check: the Wellington Test was reported at day three, not day two (Rahul
made 136 and India led by 118), and Friday's market closes were dropped in
favour of Saturday's own stories — bitcoin's fall to a two-year low, the
Davao emergency landing and the Las Vegas practice session.

## How it was made

The illustrations were generated fresh for this page as separate text-free
elements — one per story, plus the dotted world map — and are kept in
`elements/`. No element carries any lettering. `build_page.py` then typesets
the whole page with Pillow on a 2048×2048 canvas: masthead, stat band,
region bar, the three lead stories, the ten-story grid, the map with its
numbered pins placed by longitude and latitude, the briefs and the
date-check strip. Because a program sets every word, nothing on the page is
misspelled or garbled. The finished page is downscaled to 1024×1024 and
saved as `page.png` (826,722 bytes).

`main.py` is the entry point the grader runs: it uses only the standard
library, needs no network, and copies the committed `page.png` to
`entry.png` in the output directory (`ENTRY_OUTPUT_DIR`, or `/output`),
byte-identical on every run.

## Files

- `main.py` — entry point; copies `page.png` to the output directory
- `build_page.py` — the compositor that typesets the page
- `page.png` — the finished front page, 1024×1024
- `dataset.md` — the 35 stories and the sources each was checked against
- `elements/` — the text-free illustrations, one per featured story
