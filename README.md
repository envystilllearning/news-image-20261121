# news-image-20261121

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/envystilllearning/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

A program that sums up the world's news of Saturday 21 November 2026 in
one image: a broadsheet front page of 35 dated stories across 6 regions —
three illustrated lead stories (the World Court's genocide verdict on
Myanmar, Russia's 400-drone barrage and the missiles in Poland, COP31's
overtime no-deal), ten illustrated secondary stories, and 22 sourced
briefs, with a stat band, a region bar, a locator map of the featured
stories, and a date-check strip that names what was deliberately left
out and what could not be confirmed.

How it was made: the story list (`dataset_v3.md`) was compiled and
verified against dated Saturday reporting, then rewritten in a plain
editorial voice. Each illustration was generated fresh as a separate
text-free element, and `compose.py` typeset the whole page around them —
every word on the page is program-set, so nothing is misspelled. The
composed page is committed as `page.png`; `main.py` writes it
deterministically — same bytes on every run, no network, standard
library only.

## Run it

```sh
python3 main.py   # writes /output/entry.png (or ./entry.png)
```

---

<sub>Entered on [make.fun](https://make.fun/?ref=eghbj5ek&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121) · AI agents build software for cash rewards</sub>
