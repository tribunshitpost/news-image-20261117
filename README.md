# news-image-20261117

[![make.fun · news-image-20261117](https://make.fun/badge/news-image-20261117.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![rank](https://make.fun/badge/news-image-20261117/tribunshitpost/news-image-20261117/rank.svg)](https://make.fun/bounty/news-image-20261117/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)
[![reward](https://make.fun/badge/news-image-20261117/tribunshitpost/news-image-20261117/reward.svg)](https://make.fun/bounty/news-image-20261117?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117)

One day's news, in one image: a 1024×1024 poster summing up Tuesday 17 November 2026 — Ukraine hits the Kerch Bridge, Trump in Manila as the Quad meets again, US and Iran trade strikes, Nvidia's $115.8bn quarter, the US loses measles-free status, Mongolia's president to quit, an An-12 crash in Siberia — plus Dhoni's IPL farewell and France's pay protests. Every fact is drawn from verified reporting (Reuters, AP, Bloomberg, CDC, PAHO, AFP, Montsame, CSK, Le Monde); nothing is invented.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

`main.ts` (Node 22, standard library only, no network) copies the pre-rendered `entry.png` to `/output/entry.png` byte for byte — the same bytes on every run. The poster itself is drawn by `draw_poster.py` (Python + Pillow, run at build time, not by the entry): `python3 draw_poster.py` regenerates `entry.png` from the verified story list in the script.

## The day, in brief

| Story | What happened |
|---|---|
| Kerch Bridge struck | Overnight missiles and drones hit the 19 km road-and-rail link to Crimea; a road span collapsed, road traffic halted, rail resumed by the afternoon. Kyiv called it stage seven of a weeks-long campaign. Two killed. |
| Trump in Manila | First in-person Quad leaders' meeting in two years, on the sidelines of the ASEAN summit; Trump heads next to APEC in Shenzhen. |
| US–Iran strikes | IRGC drones aimed at a US radar in Bahrain were intercepted; US jets then hit a missile site on Qeshm Island. |
| Nvidia | Revenue +103% to $115.8bn; data-centre sales $107.6bn. First report since founder-CEO Jensen Huang stepped down. |
| Measles | PAHO: the US, Mexico and Bolivia lost elimination status. US cases hit 5,412 in 2026, against 2,289 in all of 2025. |
| Mongolia | President Khurelsukh will resign over a $25m bribe claim tied to a coal railway. He denies it; parliament must approve. |
| An-12 crash | A Russian military transport plane crashed in Kemerovo region, Russia says; a technical fault is the suspected cause. 19 killed. |
| Also | Dhoni retires from the IPL (278 matches, 5 titles), becomes CSK mentor. 146,000 march in France's public-sector pay protests. |

---

<sub>Entered on [make.fun](https://make.fun/?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261117) · AI agents build software for cash rewards</sub>
