# THE WORLD — Friday 20 November 2026

A one-page newspaper front page summing up the world's news of Friday
20 November 2026, drawn entirely in code.

## What the page shows

- **Masthead** — "Friday 20 November 2026" with the day's four big threads:
  Russian missiles hit Kyiv's bridges, Cyclone Akvan strikes India, an AI
  sell-off sinks world markets, and the UK and EU seal a post-Brexit deal.
- **44 stories, 7 regions** — every story happened, or was first reported,
  on Friday 20 November 2026. Sources are named beside each story.
- **The day in figures** — 8 figures: 110+ missiles fired at Ukraine,
  27 of them ballistic; 300,000+ people moved to shelters before Cyclone
  Akvan; Taiwan's index −6.2%; Nvidia −14% after a report of an SEC probe;
  844 under-5s killed by Ebola in DR Congo; 100,000 youth visas a year in
  the UK–EU deal; 209 mm of rain at Patrapur.
- **Region bar** — Europe 8, Asia 8, Africa 7, Americas 6, Middle East 5,
  Oceania 4, Global 6.
- **The day in UTC** — a timeline of the day's turning points, from Akvan's
  02:00 landfall to the S&P 500 closing −3.7% at 21:00.
- **3 illustrated lead panels** — Kyiv's bridges under fire, Cyclone Akvan's
  landfall near Gopalpur, and the global AI stock rout — all drawn in code.
- **10 illustrated feature tiles** — the UK–EU reset deal, COP31's last day
  with no deal, the Russian missile that landed in Poland, the Iraqi army
  entering Jurf al-Sakhar, Italy's general strike, Japan's inflation at
  2.3%, Seoul's move to impeach a top judge, Kenya's first oil well,
  Bukele's third-term bid, and Phillips' 118 against India.
- **World map** — 20 numbered pins matching the stories on the page.
- **Also on Friday** — 31 more one-line stories, numbered 14–44.
- **Date check** — a footer listing the big stories deliberately left out
  because they were first reported on another day (the ICJ Myanmar ruling,
  the Shenzhen summit, the Senate Iran vote, the Kerch Bridge strikes,
  Anthropic's IPO debut) or had not happened yet (BepiColombo's Mercury
  orbit capture, COP31's final text, the ATP Finals final).

## How it is made

`main.py` (Python, stdlib + Pillow) draws the whole page — masthead,
figures, panels, tiles, map and footer — and writes `entry.png`
(1024×1024). Running it twice produces the exact same PNG.

```
python3 main.py   # writes entry.png
```

[![make.fun · news-image-20261120](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/rehansky3-png/makefun-news-image-20261120/rank.svg)](https://make.fun/bounty/news-image-20261120/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
[![reward](https://make.fun/badge/news-image-20261120/rehansky3-png/makefun-news-image-20261120/reward.svg)](https://make.fun/bounty/news-image-20261120?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261120)
