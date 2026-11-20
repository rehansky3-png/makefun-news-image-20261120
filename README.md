# THE WORLD — Friday 20 November 2026

A newspaper front page that sums up the world's news of **Friday 20 November 2026**
in a single 1024×1024 image, built for the make.fun bounty
[`news-image-20261120`](https://make.fun/bounty/news-image-20261120).

## What the image shows

- **Masthead** with the date front and centre: Friday 20 November 2026.
- **Lead story:** the International Court of Justice rules 9–6 that Myanmar
  committed genocide against the Rohingya — the first time the World Court
  has held a state responsible for genocide.
- **The day in figures:** the ICJ's 9–6 vote, Anthropic's record $81.3bn IPO,
  the Nikkei's −4.8% fall, the $48.3bn cost of the Iran war, Kenya clearing
  Ebola in 37 days, and GTA 6's $2.3bn launch.
- **A world map** with 15 numbered dots marking where the day's stories happened,
  from The Hague to Shenzhen, Kyiv to Nairobi.
- **Three illustrated panels:** the Trump–Xi–Putin summit in Shenzhen, the
  fifth straight day of falling markets, and Voyager 1 reaching one light-day
  from Earth.
- **42 more stories** in a tight grid — the Kerch Bridge strikes, the Kyiv
  missile attack, the Houthi missile in Riyadh, COP31, the Nvidia probe,
  the UN secretary-general race, BepiColombo reaching Mercury, and more —
  plus six briefs. 49 stories in total, every one verified against real
  reporting from 20 November 2026.

## How to run

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `out`), checks it is a valid PNG of 1024×1024 pixels and under
1 MiB, and prints its size. It uses only the Python standard library,
needs no network, and is deterministic — two runs write identical bytes:

```sh
python3 main.py --self-test
```

## Sources

Every story on the page was checked against real reporting first published
on 20 November 2026 (BBC, Reuters, AP, The Guardian, and the day's wire
coverage). No story, figure, or quote was invented.

## Files

- `main.py` — the entry program (standard library only).
- `entry.png` — the front-page image (1024×1024 PNG).
- `LICENSE` — MIT.

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rehansky3-png/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rehansky3-png/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
