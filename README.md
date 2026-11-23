# The World in One Day — Sunday 22 November 2026

Entry for make.fun bounty **news-image-20261122** — "Sum up 22 November's
world news in one image" ($100, 50 places paid).

## What it is

A dense 1024×1024 broadsheet PNG: masthead with the date **22 NOVEMBER
2026**, three top stories (COP31 collapse, two tankers hit mines at Hormuz,
'El Chapo Isidro' captured), a UTC timeline, and **43 stories** in six
sections — The Gulf & Middle East, Ukraine & Europe, Climate/Markets/US,
Asia & Pacific, Africa & Disasters, Sport & Obituaries — each with its UTC
time, headline, one-line detail and source.

## How it runs

`main.py` (Python 3.13, standard library only) copies the shipped
`entry.png` to `/output/entry.png` (or `$MAKEFUN_OUTPUT_DIR`). The copy is
byte-identical, so both grading runs write the same bytes. No network.

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`gen_image.py` is the build script that drew `entry.png` with Pillow
(DejaVu fonts, fixed layout, no timestamps, no randomness — re-running it
reproduces the same image).

## Sources (all events happened or were first reported 22 Nov 2026)

Researched 23 Nov 2026 from Reuters, AP, AFP, Al Jazeera,
[Daily Summary of World — 22 Nov 2026](https://dailysummaryof.com/world/2026-11-22)
(29 stories, 50 sources),
[Bangladesh Chronicle morning briefing](https://bangladeshchronicle.net/morning-briefing-sunday-november-22-2026/),
LiveScore / FBref (22 Nov 2026 fixtures), and KPFA's 22 Nov evening news.

Top stories: COP31 in Antalya ends with no deal after the EU rejects a
final text omitting fossil fuels (Reuters/AP); two supertankers hit naval
mines east of the Strait of Hormuz (Iran navy / UKMTO); Mexican forces
capture FBI Top-10 fugitive Fausto 'El Chapo Isidro' Meza Flores, 11 killed
in the Sinaloa raid (AP/Reuters). Full per-story sources are printed on the
image itself.

## License

MIT — see LICENSE.
