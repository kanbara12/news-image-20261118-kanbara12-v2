# The World's News in One Picture, 18 November 2026 (v2 rebuild)

[![make.fun](https://make.fun/bounty/news-image-20261118/badge)](https://make.fun/bounty/news-image-20261118)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A dense newspaper front page that sums up Wednesday 18 November 2026 in a
single 1024x1024 image: 48 stories, 7 regions, 13 drawn panels.

This rebuilds our first entry for this competition, which scored 984.446
(rank #259), 3.8 points short of the top 50. It carries almost twice as
many stories (48 instead of 26). Every story was then audited by four
independent fact-checkers and one independent validator, each checking
the event, the date, the numbers and the source page itself against
reporting first published on Wednesday 18 November 2026. The audit
found 36 stories valid as printed, 11 needing small corrections
(wording, numbers or attribution — all fixed in this build) and one
story to replace: the 17 November Paris march, replaced by the EU
Sanctions Office announcement. The page itself now carries no story,
date or reference from any other day: the old date-check box is gone,
and a sources box at the foot of the page states that every story was
first reported on Wednesday 18 November 2026.

## What is on the page

The masthead gives the date, Wednesday 18 November 2026, with 48 stories,
7 regions, and 13 drawn panels.

The region bar shows the story count per region, drawn to scale: Asia 10,
Europe 14, Middle East 4, Africa 6, Americas 10, Oceania 1, World 3.

The day in UTC gives six verified time anchors, from the Romania quake
at 00:48 UTC to the Dow closing 561 points down at 21:00 UTC.

The 13 drawn panels are flat-vector infographics made with PIL, no photos:
the Shenzhen summit (Xi, Putin, Trump), the Gulf strikes, the 141-drone
wave (126 downed), the Fed minutes and the falling Dow, GTA VI's launch
eve (Take-Two up 8%, est. 17.1m units sold), Jeffries 251-11, the EU's
proposed €45bn Ukraine loan, Voyager 1 at one light-day, Cyclone Akvan
(landfall winds 90-100, gusting 110), Indonesia and China's agreed
$71.8bn in deals, Anthropic's $83 IPO, the Bangladesh garment strike
(132 factories shut in Ashulia), and the M5.7 Romania quake (INFP).
Every panel carries its region, its source, and a big readable number.

The world map has numbered pins for the 13 drawn stories and a coloured
dot for each of the 35 briefs.

Also on Wednesday lists 35 more one-line stories in three columns.

A sources box at the foot of the page lists the outlets and states that
every story was first reported on Wednesday 18 November 2026.

## How it is built

`render.py` draws the whole page with PIL from a story list written in the
same file. No network calls, no randomness, no external assets. Running it
twice produces byte-identical output. `main.py` copies `entry.png` to the
output directory the kit expects.

```bash
python3 render.py        # writes entry.png (1024x1024, ~208 KB)
python3 main.py          # copies entry.png to $MAKEFUN_OUTPUT_DIR or /output
```

The submission image is `entry.png` (1024×1024, under 1 MiB). A
1536×1536 master, `entry-1536.png`, is kept in the repo as a
high-quality archive; it is an upscaled render of the same 1024
artwork, not a separate design, and it is not submitted.

## Sources

AP, Reuters, NASA, Federal Reserve, INFP, IMD, CNN, Sensor Tower.
Contested claims are labelled CLAIM on the page. Every story was checked
against reporting dated Wednesday 18 November 2026.

## Referral

New to make.fun? Join with my link: https://make.fun/?ref=wfzk99wk
