#!/usr/bin/env python3
"""Generate the 22 Nov 2026 world-news front page v2 (1024x1024).

Visual-first photo broadsheet: hero photo + two photos + compact story list.
Deterministic: fixed fonts, fixed layout, no timestamps, no randomness.
Run: python3 gen_image.py  -> writes entry.png next to this file.
Stories were researched 23 Nov 2026 from Reuters, AP, AFP, Al Jazeera,
Daily Summary of World (dailysummaryof.com/world/2026-11-22),
Bangladesh Chronicle and LiveScore/FBref. Every event happened or was
first reported on Sunday 22 November 2026 (any time zone).
Photos are AI-generated illustrations of the three lead events.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "v2-assets")


def f_bold(size):
    return ImageFont.truetype(FONT_DIR + "/DejaVuSans-Bold.ttf", size)


def f_reg(size):
    return ImageFont.truetype(FONT_DIR + "/DejaVuSans.ttf", size)


def f_serif_bold(size):
    return ImageFont.truetype(FONT_DIR + "/DejaVuSerif-Bold.ttf", size)


NAVY = (15, 42, 74)
RED = (178, 34, 34)
INK = (20, 20, 20)
GREY = (90, 90, 90)
LIGHT = (242, 244, 247)
CREAM = (253, 246, 227)
RULE = (200, 200, 200)

# (asset file, headline, meta) for the three photo stories
PHOTOS = [
    ("media-generation-cop31-antalya-0-9b982790-1ded-4875-8906-467942232342.webp",
     "COP31 ends with no deal",
     "EU rejects final text without fossil fuels  •  12:00 UTC  •  REUTERS / AP"),
    ("media-generation-hormuz-tankers-0-5590228b-8562-40cd-a0df-57710f6d1365.webp",
     "Two supertankers hit mines at Hormuz",
     "Ships ablaze east of the Strait  •  17:13 UTC  •  DAILY SUMMARY / UKMTO"),
    ("media-generation-sinaloa-raid-0-c170b851-47c7-41dd-9759-af20aa0e97eb.webp",
     "'El Chapo Isidro' captured in Sinaloa",
     "FBI Top-10 fugitive seized; 11 killed in raid  •  AP / REUTERS"),
]

SECTIONS = [
    ("THE GULF & MIDDLE EAST", [
        ("03:24", "Iran strikes Bahrain base", "REUTERS / AFP"),
        ("09:53", "UAE condemns Iran attack on Bahrain", "DAILY SUMMARY"),
        ("13:16", "Saudi intercepts Houthi drone", "DAILY SUMMARY"),
        ("14:20", "Iran unveils dual-missile launcher", "DAILY SUMMARY"),
        ("02:09", "Pezeshkian: 'silent economic war'", "DAILY SUMMARY"),
        ("05:48", "Three killed in Gaza food-aid strike", "DAILY SUMMARY"),
        ("02:14", "Displaced Palestinians protest in Gaza", "DAILY SUMMARY"),
    ]),
    ("UKRAINE & EUROPE", [
        ("22 NOV", "Missile hits Kryvyi Rih; 2 killed", "AP / CNN"),
        ("14:48", "Zelenskyy urges US to release Patriots", "DAILY SUMMARY"),
        ("15:36", "Sea drone hits Russian corvette Merkury", "DAILY SUMMARY"),
        ("22 NOV", "Russian cargo ship Sparta II on fire", "AP / REUTERS"),
        ("06:15", "Finland: war is spilling over", "DAILY SUMMARY"),
        ("09:41", "Europe protests, third straight day", "DAILY SUMMARY"),
        ("10:25", "Ex-Italian police chief found dead", "DAILY SUMMARY"),
    ]),
    ("CLIMATE, MARKETS & THE US", [
        ("22 NOV", "S&P 500 falls 3.7% in a week of rout", "AP"),
        ("22 NOV", "Trump curbs contractors' replies", "AP"),
        ("22 NOV", "US intel chief: Putin 'not a friend'", "REUTERS"),
        ("22 NOV", "Army to detonate lead in Iowa", "REUTERS"),
        ("22 NOV", "Democrats' biggest win since 1992", "DAILY SUMMARY"),
        ("19:16", "Delta flights briefly delayed at Atlanta", "REUTERS"),
        ("00:09", "Teen gamer helps FBI rescue missing girl", "DAILY SUMMARY"),
    ]),
    ("ASIA & PACIFIC", [
        ("04:19", "Candy factory fire kills 3 in Indonesia", "AP / REUTERS"),
        ("22 NOV", "EU-Indonesia sign trade deal", "AP / REUTERS"),
        ("22 NOV", "South Korea minister quits over AI exam", "REUTERS"),
        ("22 NOV", "Nepal PM's first visit to India", "BANGLADESH CHRONICLE"),
        ("22 NOV", "Bangladesh: 773 arrested in Dhaka raids", "BANGLADESH CHRONICLE"),
        ("22 NOV", "Thai court upholds defamation verdict", "AP"),
        ("00:26", "Fred Nile, NSW figure, dies at 92", "DAILY SUMMARY"),
    ]),
    ("AFRICA & DISASTERS", [
        ("15:03", "Sudan drone attacks kill 4 near Khartoum", "DAILY SUMMARY"),
        ("22 NOV", "Nigeria boat capsizes, at least 24 dead", "AP"),
        ("07:36", "Blast at Benghazi naval depot", "DAILY SUMMARY"),
        ("22 NOV", "Unrest hinders DRC Ebola response", "GEOQUEST"),
        ("22 NOV", "Brazil storm kills 3, injures 162", "GEOQUEST"),
        ("02:38", "Lebanon's Aoun demands Israeli pullout", "DAILY SUMMARY"),
    ]),
    ("SPORT & OBITUARIES", [
        ("22 NOV", "Liverpool 4-0 Manchester United", "LIVESCORE / FBREF"),
        ("22 NOV", "Barcelona 3-2 Villarreal in La Liga", "LIVESCORE"),
        ("22 NOV", "Boca win Copa Sudamericana", "LIVESCORE"),
        ("22 NOV", "Georgia, Utah, Notre Dame top 3", "REUTERS / AP"),
        ("22 NOV", "Paolo Bulgari, jeweller, dies at 89", "AP"),
        ("22 NOV", "Phumzile Mlambo-Ngcuka dies at 71", "AP"),
    ]),
]

TIMELINE = [
    ("00:09", "RESCUE"), ("02:09", "ECON WAR"), ("04:19", "FIRE"),
    ("07:47", "SETTLERS"), ("12:00", "COP31"),
    ("14:48", "PATRIOTS"), ("15:36", "MERKURY"),
    ("17:13", "TANKERS"),
]

SHORT = {
    "REUTERS / AP": "RTR/AP", "AP / REUTERS": "AP/RTR", "REUTERS / AFP": "RTR/AFP",
    "DAILY SUMMARY": "DS", "AP / CNN": "AP/CNN", "BANGLADESH CHRONICLE": "B.CHRON.",
    "LIVESCORE / FBREF": "LIVESCORE", "LIVESCORE": "LIVESCORE", "GEOQUEST": "GEOQUEST",
    "AP": "AP", "REUTERS": "RTR",
}

TOTAL_STORIES = 3 + sum(len(items) for _, items in SECTIONS)


def cover_crop(img, tw, th):
    """Center-crop to target aspect, then resize (deterministic)."""
    sw, sh = img.size
    target = tw / th
    if sw / sh > target:
        nw = int(sh * target)
        x0 = (sw - nw) // 2
        img = img.crop((x0, 0, x0 + nw, sh))
    else:
        nh = int(sw / target)
        y0 = (sh - nh) // 2
        img = img.crop((0, y0, sw, y0 + nh))
    return img.resize((tw, th), Image.LANCZOS)


def trunc(draw, text, font, max_w):
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"


def caption_band(d, x, y, w, h, head, meta, head_font, meta_font):
    d.rectangle([x, y, x + w, y + h], fill=(0, 0, 0))
    d.text((x + 10, y + 6), trunc(d, head, head_font, w - 20),
           font=head_font, fill=(255, 255, 255))
    d.text((x + 10, y + 6 + head_font.size + 4), trunc(d, meta, meta_font, w - 20),
           font=meta_font, fill=(200, 210, 225))


def render():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 72], fill=NAVY)
    d.text((24, 8), "THE WORLD IN ONE DAY  •  SUNDAY", font=f_bold(12), fill=(180, 200, 220))
    d.text((24, 24), "22 NOVEMBER 2026", font=f_serif_bold(40), fill=(255, 255, 255))
    d.text((W - 24, 12), "%d STORIES  •  ALL TIMES UTC" % TOTAL_STORIES,
           font=f_bold(13), fill=(255, 210, 90), anchor="ra")
    d.text((W - 24, 34), "PHOTOS: AI ILLUSTRATIONS OF THE DAY'S NEWS",
           font=f_bold(10), fill=(180, 200, 220), anchor="ra")
    d.rectangle([0, 72, W, 76], fill=RED)

    # ---------- hero photo: COP31 ----------
    hero_x, hero_y, hero_w, hero_h = 24, 84, W - 48, 316
    hero = cover_crop(Image.open(os.path.join(ASSETS, PHOTOS[0][0])).convert("RGB"),
                      hero_w, hero_h)
    img.paste(hero, (hero_x, hero_y))
    d.rectangle([hero_x, hero_y, hero_x + hero_w, hero_y + 3], fill=RED)
    caption_band(d, hero_x, hero_y + hero_h - 58, hero_w, 58,
                 PHOTOS[0][1], PHOTOS[0][2], f_bold(24), f_reg(12))

    # ---------- two photos side by side ----------
    sub_y, sub_h, gap = 412, 190, 12
    sub_w = (W - 48 - gap) // 2
    for i in (1, 2):
        x = 24 + (i - 1) * (sub_w + gap)
        photo = cover_crop(Image.open(os.path.join(ASSETS, PHOTOS[i][0])).convert("RGB"),
                           sub_w, sub_h)
        img.paste(photo, (x, sub_y))
        caption_band(d, x, sub_y + sub_h - 48, sub_w, 48,
                     PHOTOS[i][1], PHOTOS[i][2], f_bold(15), f_reg(10))

    # ---------- UTC timeline strip ----------
    ty = 662
    d.rectangle([24, ty, W - 24, ty + 24], fill=CREAM, outline=RULE)
    d.text((32, ty + 6), "UTC TIMELINE", font=f_bold(10), fill=RED)
    seg = (985 - 175) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 175 + seg * i + seg / 2
        d.ellipse([cx - 3, ty + 9, cx + 3, ty + 15], fill=RED)
        d.text((cx, ty + 1), t, font=f_bold(9), fill=INK, anchor="ma")
        d.text((cx, ty + 13), label, font=f_bold(8), fill=GREY, anchor="ma")

    # ---------- compact story list: 3 columns ----------
    body_top = 696
    col_w = (W - 48 - 2 * 16) // 3
    col_x = [24, 24 + col_w + 16, 24 + 2 * (col_w + 16)]
    cols = [[0, 4], [1, 3], [2, 5]]
    for ci, sec_idx in enumerate(cols):
        x = col_x[ci]
        y = body_top
        for si in sec_idx:
            title, items = SECTIONS[si]
            d.rectangle([x, y + 2, x + 10, y + 12], fill=RED)
            d.text((x + 14, y), title, font=f_bold(12), fill=NAVY)
            d.line([x, y + 17, x + col_w, y + 17], fill=NAVY, width=1)
            y += 24
            for (t, head, src) in items:
                line = t + "  " + head + "  [" + SHORT.get(src, src) + "]"
                d.text((x, y), trunc(d, line, f_bold(10), col_w),
                       font=f_bold(10), fill=INK)
                y += 14
            y += 6

    # ---------- footer ----------
    d.line([24, 994, W - 24, 994], fill=NAVY, width=1)
    d.text((W // 2, 999),
           "All events happened or were first reported on Sunday 22 November 2026 (any time zone).",
           font=f_reg(10), fill=GREY, anchor="ma")
    d.text((W // 2, 1011),
           "Sources: Reuters, AP, AFP, Al Jazeera, Daily Summary of World, Bangladesh Chronicle, LiveScore, FBref.",
           font=f_reg(9), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    out = render()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
