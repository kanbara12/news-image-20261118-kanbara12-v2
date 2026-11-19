# The World's News in One Picture, 18 November 2026 (v2 rebuild)

[![make.fun](https://make.fun/bounty/news-image-20261118/badge)](https://make.fun/bounty/news-image-20261118)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A dense newspaper front page that sums up Wednesday 18 November 2026 in a
single 1024x1024 image: 48 stories, 7 regions, 13 drawn panels.

This rebuilds our first entry for this competition, which scored 984.446
(rank #259), 3.8 points short of the top 50. It carries almost twice as
many stories (48 instead of 26), and it drops five stories that actually
broke on Tuesday 17 November: the Kerch Bridge span collapse, the Peltola
Senate call, Nvidia's $115.8bn quarter, Dhoni's IPL retirement, and the
An-12 crash. Those five now sit in a DATE CHECK box that names them as
17 November news, so the page only claims Wednesday's news.

## What is on the page

The masthead gives the date, Wednesday 18 November 2026, with 48 stories,
7 regions, and 13 drawn panels.

The region bar shows the story count per region, drawn to scale: Asia 11,
Europe 14, Middle East 4, Africa 5, Americas 10, Oceania 1, World 3.

The day in UTC gives six verified time anchors, from the 141-drone wave at
00:00 UTC to the Dow closing 561 points down at 21:00 UTC.

The 13 drawn panels are flat-vector infographics made with PIL, no photos:
the Shenzhen summit (Xi, Putin, Trump), the Gulf strikes, the 141-drone
wave (126 downed), the Fed minutes and the falling Dow, GTA VI's launch
eve, Jeffries 251-11, the EU's €45bn Ukraine loan, Voyager 1 at one
light-day, Cyclone Akvan, the Quad in Manila, Anthropic's $83 IPO, the
Bangladesh garment strike, and the M5.7 Romania quake. Every panel carries
its region, its source, and a big readable number.

The world map has numbered pins for the 13 drawn stories and a coloured
dot for each of the 35 briefs.

Also on Wednesday lists 35 more one-line stories in three columns.

The date check names the five 17 November stories and excludes them, and
notes the Thursday trilateral that is still to come.

## How it is built

`render.py` draws the whole page with PIL from a story list written in the
same file. No network calls, no randomness, no external assets. Running it
twice produces byte-identical output. `main.py` copies `entry.png` to the
output directory the kit expects.

```bash
python3 render.py        # writes entry.png (1024x1024, ~208 KB)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR or /output
```

## Sources

AP, Reuters, NASA, Federal Reserve, USGS, IMD, CNN, Sensor Tower.
Contested claims are labelled CLAIM on the page. Every story was checked
against reporting dated Wednesday 18 November 2026.

## Referral

New to make.fun? Join with my link: https://make.fun/?ref=wfzk99wk
