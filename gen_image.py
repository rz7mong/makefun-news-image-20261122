#!/usr/bin/env python3
"""Generate the 22 Nov 2026 world-news broadsheet (1024x1024 PNG).

Deterministic: fixed fonts, fixed layout, no timestamps, no randomness.
Run: python3 gen_image.py  -> writes entry.png next to this file.
Stories were researched 23 Nov 2026 from Reuters, AP, AFP, Al Jazeera,
Daily Summary of World (dailysummaryof.com/world/2026-11-22),
Bangladesh Chronicle and LiveScore/FBref. Every event happened or was
first reported on Sunday 22 November 2026 (any time zone).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"

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

# (utc_time, headline, detail, source)
LEADS = [
    ("12:00 UTC", "COP31 ENDS WITH NO DEAL",
     "EU rejects final text that omits fossil fuels; climate talks in Antalya collapse after two weeks.",
     "REUTERS / AP"),
    ("17:13 UTC", "TWO TANKERS HIT MINES AT HORMUZ",
     "Iran's navy says two supertankers struck naval mines and caught fire east of the Strait of Hormuz.",
     "DAILY SUMMARY / UKMTO"),
    ("22 NOV", "'EL CHAPO ISIDRO' CAPTURED",
     "Mexican forces seize FBI Top-10 fugitive Fausto Isidro Meza Flores; 11 killed in the Sinaloa raid.",
     "AP / REUTERS"),
]

SECTIONS = [
    ("THE GULF & MIDDLE EAST", [
        ("03:24", "Iran strikes Bahrain base and factory",
         "Civilian site hit near Manama, 2 hurt; Iran says it hit 2 Patriot radars.", "REUTERS / AFP"),
        ("09:53", "UAE condemns Iran attack on Bahrain",
         "Calls the strikes a violation of Bahrain's sovereignty.", "DAILY SUMMARY"),
        ("13:16", "Saudi intercepts Houthi drone, missile",
         "Houthis claim a strike on the Rabigh refinery on the Red Sea.", "DAILY SUMMARY"),
        ("14:20", "Iran unveils dual-missile launcher",
         "State media shows a new underground 'missile city'.", "DAILY SUMMARY"),
        ("02:09", "Pezeshkian: Iran in 'silent economic war'",
         "US naval blockade hits 130 days as oil exports are squeezed.", "DAILY SUMMARY"),
        ("05:48", "Three killed in Gaza food-aid strike",
         "World Central Kitchen says the vehicle hit was not its team.", "DAILY SUMMARY"),
        ("02:14", "Displaced Palestinians protest in Gaza",
         "350,000 families homeless after 80% of homes were destroyed.", "DAILY SUMMARY"),
    ]),
    ("UKRAINE & EUROPE", [
        ("22 NOV", "Russian missile hits Kryvyi Rih",
         "A boy, 7, and a woman, 20, killed; about 60 wounded.", "AP / CNN"),
        ("14:48", "Zelenskyy urges US to release Patriots",
         "Partners paid; Russia fired 2,700 drones in a week.", "DAILY SUMMARY"),
        ("15:36", "Sea drone hits Russian corvette Merkury",
         "Explosion and fire at the Benghazi naval base in eastern Libya.", "DAILY SUMMARY"),
        ("22 NOV", "Russian cargo ship Sparta II on fire",
         "Burning in the Baltic after a suspected Ukrainian drone strike.", "AP / REUTERS"),
        ("06:15", "Finland: war is spilling over",
         "Helsinki reacts after the Baltic drone strike on the Russian ship.", "DAILY SUMMARY"),
        ("09:41", "Europe protests, third straight day",
         "Cost-of-living rallies; France's sixth weekend of protests.", "DAILY SUMMARY"),
        ("10:25", "Ex-Italian police chief found dead",
         "Gianni De Gennaro dies amid a Sicily bombing cover-up inquiry.", "DAILY SUMMARY"),
    ]),
    ("CLIMATE, MARKETS & THE US", [
        ("22 NOV", "S&P 500 falls 3.7% in a week of rout",
         "Nasdaq down 5.3% on Friday as the AI sell-off spreads to Asia.", "AP"),
        ("22 NOV", "Trump curbs contractors' Congress replies",
         "Contractors must consult the White House before replying.", "AP"),
        ("22 NOV", "US intel chief: Putin 'not a friend'",
         "DNI Jay Clayton speaks days after Trump praised Russia's leader.", "REUTERS"),
        ("22 NOV", "Army to detonate lead in Iowa by Tuesday",
         "68 barrels of toxic lead azide blown up, defying a court order.", "REUTERS"),
        ("22 NOV", "Democrats' biggest House win since 1992",
         "Recount seals the largest Democratic majority in 34 years.", "DAILY SUMMARY"),
        ("19:16", "Delta flights briefly delayed at Atlanta",
         "Automated system issue hits the busiest airport in the US.", "REUTERS"),
        ("00:09", "Teen gamer helps FBI rescue missing girl",
         "Landon, 16, and his mother alerted police after an online chat.", "DAILY SUMMARY"),
    ]),
    ("ASIA & PACIFIC", [
        ("04:19", "Candy factory fire kills 3 in Indonesia",
         "36 workers missing and 15 rescued alive in Cikande, Banten.", "AP / REUTERS"),
        ("22 NOV", "EU-Indonesia sign landmark trade deal",
         "After 10 years of talks; tariffs scrapped on 98.5% of goods.", "AP / REUTERS"),
        ("22 NOV", "South Korea minister quits over AI exam",
         "Minister quits over rule changes to stop AI cheating.", "REUTERS"),
        ("22 NOV", "Nepal PM begins first visit to India",
         "Balendra Shah to meet Modi on energy, trade and connectivity.", "BANGLADESH CHRONICLE"),
        ("22 NOV", "Bangladesh: 773 arrested in Dhaka raids",
         "Includes 181 alleged Awami League members.", "BANGLADESH CHRONICLE"),
        ("22 NOV", "Thai court upholds defamation verdict",
         "Opposition lawmaker's royal defamation sentence cut to 3 years.", "AP"),
        ("00:26", "Fred Nile, NSW political figure, dies at 92",
         "Christian Democratic figurehead; 40 years in NSW parliament.", "DAILY SUMMARY"),
    ]),
    ("AFRICA & DISASTERS", [
        ("15:03", "Sudan drone attacks kill 4 near Khartoum",
         "RSF-blamed strikes damage a UN building while staff were inside.", "DAILY SUMMARY"),
        ("22 NOV", "Nigeria boat capsizes, at least 24 dead",
         "The boat was carrying people to a funeral when it overturned.", "AP"),
        ("07:36", "Blast at Benghazi naval ammunition depot",
         "Explosion triggers a fire at the eastern Libyan port base.", "DAILY SUMMARY"),
        ("22 NOV", "Insecurity hinders DRC Ebola response",
         "Aid teams cannot reach outbreak areas, charity warns.", "GEOQUEST"),
        ("22 NOV", "Brazil storm kills 3, injures 162",
         "Severe weather sweeps the south of the country.", "GEOQUEST"),
        ("02:38", "Lebanon's Aoun demands Israeli pullout",
         "Vows to bring all weapons under state control.", "DAILY SUMMARY"),
    ]),
    ("SPORT & OBITUARIES", [
        ("22 NOV", "Liverpool 4-0 Manchester United",
         "Anfield rout; Hull City beat Brighton 2-0 in the Premier League.", "LIVESCORE / FBREF"),
        ("22 NOV", "Barcelona 3-2 Villarreal in La Liga",
         "Real Madrid 2-1 Celta; Atletico win 3-0 at Getafe.", "LIVESCORE"),
        ("22 NOV", "Boca win Copa Sudamericana final",
         "Boca Juniors beat Atletico Mineiro 2-0 to lift the trophy.", "LIVESCORE"),
        ("22 NOV", "Georgia, Utah, Notre Dame stay top 3",
         "UCLA falls in triple OT; Ohio State upset 31-28 at Nebraska.", "REUTERS / AP"),
        ("22 NOV", "Paolo Bulgari, jeweller, dies at 89",
         "Turned the family business into a global luxury brand.", "AP"),
        ("22 NOV", "Phumzile Mlambo-Ngcuka dies at 71",
         "Former South Africa deputy president and UN Women chief.", "AP"),
    ]),
]

TIMELINE = [
    ("00:09", "RESCUE"), ("02:09", "ECONOMIC WAR"), ("04:19", "FACTORY FIRE"),
    ("07:47", "SETTLER ATTACKS"), ("12:00", "COP31 COLLAPSE"),
    ("14:48", "PATRIOTS PLEA"), ("15:36", "MERKURY HIT"),
    ("17:13", "TANKERS MINED"),
]

SHORT = {
    "REUTERS / AP": "RTR/AP", "AP / REUTERS": "AP/RTR", "REUTERS / AFP": "RTR/AFP",
    "DAILY SUMMARY": "DS", "AP / CNN": "AP/CNN", "BANGLADESH CHRONICLE": "B.CHRONICLE",
    "LIVESCORE / FBREF": "LIVESCORE", "LIVESCORE": "LIVESCORE", "GEOQUEST": "GEOQUEST",
    "AP": "AP", "REUTERS": "RTR",
}

TOTAL_STORIES = 3 + sum(len(items) for _, items in SECTIONS)


def wrap(draw, text, font, max_w):
    """Wrap text to fit max_w pixels; returns list of lines."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def trunc(draw, text, font, max_w):
    """Truncate with ellipsis to fit max_w pixels."""
    if draw.textlength(text, font=font) <= max_w:
        return text
    while text and draw.textlength(text + "…", font=font) > max_w:
        text = text[:-1]
    return text + "…"

def render():
    img = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(img)

    # ---------- masthead ----------
    d.rectangle([0, 0, W, 104], fill=NAVY)
    d.text((24, 12), "THE WORLD IN ONE DAY  •  SUNDAY", font=f_bold(13), fill=(180, 200, 220))
    d.text((24, 30), "22 NOVEMBER 2026", font=f_serif_bold(48), fill=(255, 255, 255))
    d.text((W - 24, 16), "%d STORIES" % TOTAL_STORIES, font=f_bold(16), fill=(255, 210, 90), anchor="ra")
    d.text((W - 24, 38), "ALL TIMES UTC", font=f_bold(13), fill=(180, 200, 220), anchor="ra")
    d.text((W - 24, 58), "SUNDAY 22 NOV 2026", font=f_bold(13), fill=(180, 200, 220), anchor="ra")
    d.rectangle([0, 104, W, 108], fill=RED)

    # ---------- lead row: 3 boxes ----------
    lead_y, lead_h = 116, 132
    col_w = (W - 48 - 2 * 12) // 3
    for i, (t, head, detail, src) in enumerate(LEADS):
        x = 24 + i * (col_w + 12)
        d.rectangle([x, lead_y, x + col_w, lead_y + lead_h], fill=LIGHT, outline=RULE)
        d.rectangle([x, lead_y, x + col_w, lead_y + 4], fill=RED)
        d.text((x + 10, lead_y + 12), "TOP STORY  •  " + t, font=f_bold(10), fill=RED)
        hl = wrap(d, head, f_bold(19), col_w - 20)
        y = lead_y + 30
        for line in hl[:2]:
            d.text((x + 10, y), line, font=f_bold(19), fill=INK)
            y += 22
        dl = wrap(d, detail, f_reg(11), col_w - 20)
        for line in dl[:2]:
            d.text((x + 10, y + 2), line, font=f_reg(11), fill=(60, 60, 60))
            y += 14
        d.text((x + 10, lead_y + lead_h - 16), "SOURCE: " + src, font=f_bold(9), fill=GREY)

    # ---------- UTC timeline strip ----------
    ty = 256
    d.rectangle([24, ty, W - 24, ty + 26], fill=CREAM, outline=RULE)
    d.text((32, ty + 6), "UTC TIMELINE", font=f_bold(10), fill=RED)
    seg = (985 - 175) / len(TIMELINE)
    for i, (t, label) in enumerate(TIMELINE):
        cx = 175 + seg * i + seg / 2
        d.ellipse([cx - 3, ty + 10, cx + 3, ty + 16], fill=RED)
        d.text((cx, ty + 1), t, font=f_bold(9), fill=INK, anchor="ma")
        d.text((cx, ty + 14), label, font=f_bold(8), fill=GREY, anchor="ma")

    # ---------- body: 3 columns ----------
    body_top, body_bottom = 292, 986
    col_w = (W - 48 - 2 * 16) // 3
    col_x = [24, 24 + col_w + 16, 24 + 2 * (col_w + 16)]
    # column assignment: col0 = sections 0+4, col1 = 1+3, col2 = 2+5
    cols = [[0, 4], [1, 3], [2, 5]]
    col_end = body_top
    for ci, sec_idx in enumerate(cols):
        x = col_x[ci]
        y = body_top
        for si in sec_idx:
            title, items = SECTIONS[si]
            d.rectangle([x, y + 2, x + 10, y + 12], fill=RED)
            d.text((x + 14, y), title, font=f_bold(13), fill=NAVY)
            d.line([x, y + 18, x + col_w, y + 18], fill=NAVY, width=1)
            y += 26
            for (t, head, detail, src) in items:
                # headline with inline time, max 2 lines
                full = t + "  " + head
                hl = wrap(d, full, f_bold(13), col_w)
                for j, line in enumerate(hl[:2]):
                    d.text((x, y), line, font=f_bold(13), fill=INK)
                    y += 15
                d.text((x, y), trunc(d, detail + " [" + SHORT.get(src, src) + "]", f_reg(11), col_w),
                       font=f_reg(11), fill=(60, 60, 60))
                y += 13
                y += 4  # gap between items
            y += 5  # gap between sections
        col_end = max(col_end, y)

    # ---------- footer ----------
    d.line([24, 992, W - 24, 992], fill=NAVY, width=1)
    d.text((W // 2, 997),
           "All events happened or were first reported on Sunday 22 November 2026 (any time zone).",
           font=f_reg(10), fill=GREY, anchor="ma")
    d.text((W // 2, 1010),
           "Sources per story: Reuters, AP, AFP, Al Jazeera, Daily Summary of World, Bangladesh Chronicle, LiveScore, FBref.",
           font=f_reg(9), fill=GREY, anchor="ma")
    return img

if __name__ == "__main__":
    out = render()
    out.save("entry.png", optimize=True)
    print("saved entry.png", out.size)
