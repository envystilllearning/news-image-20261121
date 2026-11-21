#!/usr/bin/env python3
"""Compose the Saturday 21 November 2026 front page.

Draws a 2048x2048 broadsheet page with Pillow: every word is typeset by this
program from the story data below, so the text on the page is exact. The
illustrations in elements/ were generated separately as text-free images and
are only cropped or fitted into their slots. The finished page is downscaled
to 1024x1024 and written to page.png next to this script.
"""

import os

from PIL import Image, ImageDraw, ImageFont, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
ELEMENTS = os.path.join(HERE, "elements")
FONT_DIR = "/usr/share/fonts/truetype/liberation"

CANVAS = 2048
MARGIN = 52
CONTENT_W = CANVAS - 2 * MARGIN
CREAM = (245, 239, 226)
INK = (18, 16, 14)
RED = (200, 16, 46)
WHITE = (255, 255, 255)
GREY = (90, 84, 76)

# ---------------------------------------------------------------- fonts

_cache = {}


def font(kind, size):
    key = (kind, size)
    if key not in _cache:
        name = {
            "serif": "LiberationSerif-Regular.ttf",
            "serif_b": "LiberationSerif-Bold.ttf",
            "sans": "LiberationSans-Regular.ttf",
            "sans_b": "LiberationSans-Bold.ttf",
            "sans_i": "LiberationSans-Italic.ttf",
        }[kind]
        _cache[key] = ImageFont.truetype(os.path.join(FONT_DIR, name), size)
    return _cache[key]


# ---------------------------------------------------------------- text utils


def wrap(draw, text, fnt, width):
    """Split text into lines that fit width, measured with the real font."""
    lines = []
    for para in text.split("\n"):
        words = para.split()
        if not words:
            lines.append("")
            continue
        line = words[0]
        for word in words[1:]:
            trial = line + " " + word
            if draw.textlength(trial, font=fnt) <= width:
                line = trial
            else:
                lines.append(line)
                line = word
        lines.append(line)
    return lines


def text_block(draw, x, y, text, fnt, width, leading, fill=INK):
    """Draw wrapped text, return the height it consumed."""
    lines = wrap(draw, text, fnt, width)
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return len(lines) * leading


def tracked(draw, x, y, text, fnt, spacing, fill=INK):
    """Draw letter-spaced text (for the small-caps masthead line)."""
    for ch in text:
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += draw.textlength(ch, font=fnt) + spacing
    return x


def tracked_width(draw, text, fnt, spacing):
    return sum(draw.textlength(ch, font=fnt) + spacing for ch in text) - spacing


def centered(draw, y, text, fnt, fill=INK):
    w = draw.textlength(text, font=fnt)
    draw.text(((CANVAS - w) / 2, y), text, font=fnt, fill=fill)


# ---------------------------------------------------------------- images


def banner(path, w, h):
    """Centre-crop an image to exactly w x h."""
    im = Image.open(path).convert("RGB")
    return ImageOps.fit(im, (w, h), Image.LANCZOS)


# ---------------------------------------------------------------- content

STATS = [
    ("10,000", "Rohingya killed in 2017"),
    ("9\u20136", "the judges' vote"),
    ("400+", "drones over Ukraine"),
    ("3", "missiles downed, Riyadh"),
    ("6.7", "the Peru quake"),
    ("$55.5K", "bitcoin's two-year low"),
]

REGIONS = [("Europe", 7), ("Asia", 12), ("Middle East", 3),
           ("Americas", 9), ("Oceania", 1), ("Global", 3)]

HEROES = [
    ("el_hero1.jpg", "1 \u00b7 THE HAGUE \u00b7 JUSTICE",
     "World court finds Myanmar guilty of genocide",
     "Judges voted 9 to 6 that Myanmar committed genocide against the "
     "Rohingya in 2017. Myanmar must prosecute the commanders and pay "
     "reparations.",
     "Sources: ICJ, Reuters"),
    ("el_hero2.jpg", "2 \u00b7 KYIV \u00b7 WAR",
     "Russia fires 400 drones at Ukraine; two missiles land in Poland",
     "The barrage killed at least eight in Kyiv and hit bridges and rail "
     "stations. Warsaw calls the missiles in Poland a deliberate "
     "provocation.",
     "Sources: France 24, CBS News"),
    ("el_hero3.jpg", "3 \u00b7 ANTALYA \u00b7 CLIMATE",
     "COP31 runs past its deadline with no deal",
     "Nearly 200 nations failed to close on Friday; the draft deletes the "
     "words \u201cfossil fuel\u201d. A call to triple adaptation funding by "
     "2035 survives.",
     "Sources: AFP, Al Jazeera"),
]

MEDIUMS = [
    ("el_m4.jpg", "4 \u00b7 RIYADH \u00b7 WAR",
     "Saudi Arabia downs three Houthi missiles over Riyadh",
     "Second attack on the capital in two days. No casualties. (Reuters)"),
    ("el_m5.jpg", "5 \u00b7 JUN\u00cdN \u00b7 EARTHQUAKE",
     "Magnitude 6.7 quake shakes central Peru",
     "Felt in Lima. Depth disputed: 108 km (USGS), 129 km (IGP). "
     "(USGS, IGP, AFP)"),
    ("el_m6.jpg", "6 \u00b7 MARKETS \u00b7 CRYPTO",
     "Bitcoin crashes through $60,000 to a two-year low",
     "The AI rout spilled into crypto; bitcoin touched $55,500, down 18% "
     "in seven days. (Reuters, CoinGecko)"),
    ("el_m7.jpg", "7 \u00b7 DAVAO \u00b7 AVIATION",
     "146 people walk away from an engine-fire scare",
     "An Air Niugini 767 diverted on a fire indication. All 146 aboard "
     "left by the slides. (AP, CAAP)"),
    ("el_m8.jpg", "8 \u00b7 BRUSSELS \u00b7 POLITICS",
     "UK and EU sign their biggest post-Brexit deal",
     "Food exports, carbon markets, youth mobility. (BBC)"),
    ("el_m9.jpg", "9 \u00b7 NEW YORK \u00b7 CYBER",
     "Three card giants report vendor cyber incidents",
     "JPMorgan, Visa and Mastercard say payments run as normal. (Reuters)"),
    ("el_m10.jpg", "10 \u00b7 LEONIDA \u00b7 GAMES",
     "GTA 6 goes on sale; players move to Leonida",
     "Release weekend, 13 years after the last game. (IGN)"),
    ("el_m11.jpg", "11 \u00b7 WELLINGTON \u00b7 CRICKET",
     "Rahul makes 136 and India take a 118-run lead",
     "Gill fell for 98. India closed day three on 486 for 4; New Zealand "
     "made 368. (ESPNcricinfo)"),
    ("el_m12.jpg", "12 \u00b7 LAHORE \u00b7 CRICKET",
     "Pakistan beat Sri Lanka by eight wickets, take the series",
     "The win ends a two-year series drought. (Dawn)"),
    ("el_m13.jpg", "13 \u00b7 LAS VEGAS \u00b7 FORMULA 1",
     "Russell tops Vegas practice, clashes with Verstappen",
     "His 1:34.041 led a Mercedes one-two. Stewards will investigate the "
     "contact. (Reuters, FIA)"),
]

PINS = [  # (number, name, longitude, latitude)
    (1, "The Hague", 4.5, 52.1),
    (2, "Kyiv", 30.5, 50.4),
    (3, "Antalya", 30.7, 36.9),
    (4, "Riyadh", 46.7, 24.6),
    (5, "Jun\u00edn (Peru)", -75.5, -11.5),
    (6, "New York", -74.0, 40.7),
    (7, "Davao", 125.6, 7.1),
    (8, "Brussels", 4.35, 50.85),
    (9, "Florida", -81.0, 27.0),
    (10, "Wellington", 174.8, -41.3),
    (11, "Lahore", 74.3, 31.5),
    (12, "Las Vegas", -115.1, 36.1),
    (13, "Odisha", 85.1, 19.8),
]

BRIEFS = [
    "14 Shenzhen \u2014 Trump, Xi and Putin open a trilateral summit and "
    "sign fuel deals (Reuters)",
    "15 Moscow \u2014 Russia rules out NATO membership in any Ukraine "
    "settlement (TASS)",
    "16 Budapest \u2014 Hungary drops its block on the EU package (Reuters)",
    "17 Naypyidaw \u2014 Myanmar calls the genocide ruling biased and "
    "unjust (AFP)",
    "18 Gaza \u2014 UNICEF counts child casualties still rising (UNICEF)",
    "19 Kuala Lumpur \u2014 Malaysia will resettle 10,000 Rohingya in "
    "T\u00fcrkiye (Bernama)",
    "20 New York \u2014 A US court jails an Indian national for 19 years "
    "over a plot to kill a Sikh separatist (AP)",
    "21 Washington \u2014 Trump attacks the Fed over interest rates "
    "(Bloomberg)",
    "22 Jakarta \u2014 Indonesia counts $30 billion in fire losses (Antara)",
    "23 Rome \u2014 The WFP warns 2027 food aid falls short (WFP)",
    "24 Kathmandu \u2014 Nepal's prime minister visits India on "
    "22\u201323 November (PTI)",
    "25 Delhi \u2014 Pakistan's climate minister joins the SCO forum in "
    "India (Dawn)",
    "26 Gaza \u2014 Israeli strikes kill Palestinians as West Bank "
    "violence continues (One Turn)",
    "27 Washington \u2014 Trump threatens to ban US firms from building AI "
    "data centres abroad (Reuters)",
    "28 Washington \u2014 A hacker reportedly breaches an FBI criminal "
    "database as outages continue (One Turn)",
    "29 London \u2014 A trial pill makes pancreatic tumours undetectable "
    "in 1 in 12 patients (One Turn)",
    "30 Berlin \u2014 Gen Z protests spread across 25 European countries "
    "(One Turn)",
    "31 Los Angeles \u2014 A court convicts the man who started the deadly "
    "Palisades fire (AFP)",
    "32 Port-au-Prince \u2014 Salvadoran troops in Haiti lose soldiers to "
    "explosives (One Turn)",
    "33 Madrid \u2014 Spain sets a 29 November election as conservatives "
    "gain (El Pa\u00eds)",
    "34 Odisha \u2014 Crews clear Cyclone Akvan's damage as the storm "
    "weakens (PTI)",
    "35 Kuno \u2014 A cheetah brought from Botswana gives birth to four "
    "cubs (PTI)",
]

DATE_CHECK = (
    "DATE CHECK \u2014 Left out as Friday's news: the first strikes on "
    "Kyiv's bridges (Saturday's barrage is story 2), Thursday's missile "
    "hit on Riyadh's PIF tower, the Sensex's 898-point Friday close, and "
    "Akvan's landfall; its clean-up is brief 34. Not confirmed when drawn: "
    "a final COP31 text, and whether any fire burned on the Davao jet "
    "\u2014 officials report an indication, not a fire."
)


# ---------------------------------------------------------------- layout
# Tunable sizes (2048px canvas). Sections advance a cursor; build() prints
# where each section ends so overflow is visible before the final render.

P = dict(
    kick_size=25, title_size=80, stand_size=28,
    stat_num=52, stat_cap=22,
    hero_img=84, hero_kick=25, hero_head=37, hero_head_lead=40,
    hero_body=24, hero_body_lead=29, hero_src=22,
    med_img=28, med_kick=20, med_head=22, med_head_lead=26,
    med_body=21, med_body_lead=24,
    map_head=30, map_w=690, legend_size=21, legend_lead=25,
    brief_size=21, brief_lead=23,
    check_size=21, check_lead=24,
)


def rule(draw, y, weight=3):
    draw.line([(MARGIN, y), (CANVAS - MARGIN, y)], fill=INK, width=weight)
    return y + weight


def build():
    page = Image.new("RGB", (CANVAS, CANVAS), CREAM)
    d = ImageDraw.Draw(page)
    y = 34

    # ---- masthead
    f_kick = font("sans_b", P["kick_size"])
    label = "THE WORLD IN ONE DAY \u2014 SATURDAY EDITION"
    w = tracked_width(d, label, f_kick, 6)
    tracked(d, (CANVAS - w) / 2, y, label, f_kick, 6, fill=RED)
    y += P["kick_size"] + 16
    centered(d, y, "Saturday 21 November 2026", font("serif_b", P["title_size"]))
    y += P["title_size"] + 14
    centered(d, y,
             "World court convicts Myanmar of genocide \u00b7 400 drones "
             "over Kyiv \u00b7 COP31 ends without a deal",
             font("sans_i", P["stand_size"]))
    y += P["stand_size"] + 12
    y = rule(d, y, 5) + 14
    print(f"masthead ends {y}")

    # ---- stat band
    col = CONTENT_W / 6
    f_num, f_cap = font("sans_b", P["stat_num"]), font("sans", P["stat_cap"])
    for i, (num, cap) in enumerate(STATS):
        x = MARGIN + i * col
        d.text((x, y), num, font=f_num, fill=INK)
        lines = wrap(d, cap, f_cap, col - 18)
        cy = y + P["stat_num"] + 8
        for line in lines:
            d.text((x, cy), line, font=f_cap, fill=GREY)
            cy += P["stat_cap"] + 5
    y += P["stat_num"] + 8 + 2 * (P["stat_cap"] + 5) + 8
    y = rule(d, y, 3) + 12
    print(f"stats end {y}")

    # ---- region bar
    total = sum(n for _, n in REGIONS)
    x = MARGIN
    for i, (_, n) in enumerate(REGIONS):
        w = CONTENT_W * n / total
        d.rectangle([x, y, x + w - 3, y + 24],
                    fill=RED if i % 2 else INK)
        x += w
    y += 24 + 8
    legend = " \u00b7 ".join(f"{name} {n}" for name, n in REGIONS)
    centered(d, y, legend, font("sans_b", 25))
    y += 25 + 14
    print(f"region bar ends {y}")

    # ---- heroes, three columns
    gap = 32
    cw = (CONTENT_W - 2 * gap) / 3
    f_kick = font("sans_b", P["hero_kick"])
    f_head = font("serif_b", P["hero_head"])
    f_body = font("sans", P["hero_body"])
    f_src = font("sans_i", P["hero_src"])
    hero_h = 0
    for i, (img, kick, head, body, src) in enumerate(HEROES):
        x = MARGIN + i * (cw + gap)
        yy = y
        page.paste(banner(os.path.join(ELEMENTS, img), int(cw), P["hero_img"]),
                   (int(x), yy))
        yy += P["hero_img"] + 10
        d.text((x, yy), kick, font=f_kick, fill=RED)
        yy += P["hero_kick"] + 8
        yy += text_block(d, x, yy, head, f_head, cw, P["hero_head_lead"])
        yy += 4
        yy += text_block(d, x, yy, body, f_body, cw, P["hero_body_lead"])
        yy += 4
        d.text((x, yy), src, font=f_src, fill=GREY)
        yy += P["hero_src"] + 4
        hero_h = max(hero_h, yy - y)
    y += hero_h + 6
    y = rule(d, y, 3) + 12
    print(f"heroes end {y}")

    # ---- mediums, 5 x 2 grid
    gap = 24
    cw = (CONTENT_W - 4 * gap) / 5
    f_kick = font("sans_b", P["med_kick"])
    f_head = font("sans_b", P["med_head"])
    f_body = font("sans", P["med_body"])
    for row in range(2):
        cell_h = 0
        for col_i in range(5):
            img, kick, head, body = MEDIUMS[row * 5 + col_i]
            x = MARGIN + col_i * (cw + gap)
            yy = y
            page.paste(banner(os.path.join(ELEMENTS, img), int(cw),
                              P["med_img"]), (int(x), yy))
            yy += P["med_img"] + 7
            d.text((x, yy), kick, font=f_kick, fill=RED)
            yy += P["med_kick"] + 5
            yy += text_block(d, x, yy, head, f_head, cw, P["med_head_lead"])
            yy += 2
            yy += text_block(d, x, yy, body, f_body, cw, P["med_body_lead"])
            cell_h = max(cell_h, yy - y)
        y += cell_h + 10
    y = rule(d, y - 4, 3) + 12
    print(f"mediums end {y}")

    # ---- map band
    d.text((MARGIN, y), "ALSO ON SATURDAY 21 NOVEMBER",
           font=font("sans_b", P["map_head"]), fill=INK)
    y += P["map_head"] + 12
    map_im = Image.open(os.path.join(ELEMENTS, "el_map.jpg")).convert("RGB")
    map_im = ImageOps.contain(map_im, (P["map_w"], 100000), Image.LANCZOS)
    page.paste(map_im, (MARGIN, y))
    mw, mh = map_im.size
    f_pin = font("sans_b", 19)
    for num, _name, lon, lat in PINS:
        fx = (lon + 180) / 360
        fy = 0.41 + (27 - lat) * 0.00524  # calibrated to this map image
        px, py = MARGIN + fx * mw, y + fy * mh
        if num == 8:  # Brussels: nudge off The Hague's pin
            px, py = px + 26, py + 15
        r = 16
        d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
                  outline=WHITE, width=3)
        s = str(num)
        tw = d.textlength(s, font=f_pin)
        d.text((px - tw / 2, py - 10), s, font=f_pin, fill=WHITE)
    lx = MARGIN + mw + 36
    f_leg = font("sans", P["legend_size"])
    ly = y + 4
    for num, name, _lon, _lat in PINS:
        d.ellipse([lx, ly + 4, lx + 20, ly + 24], fill=RED)
        s = str(num)
        tw = d.textlength(s, font=font("sans_b", 15))
        d.text((lx + 10 - tw / 2, ly + 5), s, font=font("sans_b", 15),
               fill=WHITE)
        d.text((lx + 30, ly), name, font=f_leg, fill=INK)
        ly += P["legend_lead"]
    y += max(mh, ly - y) + 8
    y = rule(d, y, 3) + 12
    print(f"map band ends {y}")

    # ---- briefs, three columns
    gap = 32
    cw = (CONTENT_W - 2 * gap) / 3
    f_brief = font("sans", P["brief_size"])
    columns = [BRIEFS[0:8], BRIEFS[8:15], BRIEFS[15:22]]
    brief_h = 0
    for ci, items in enumerate(columns):
        x = MARGIN + ci * (cw + gap)
        yy = y
        for item in items:
            yy += text_block(d, x, yy, item, f_brief, cw, P["brief_lead"])
            yy += 4
        brief_h = max(brief_h, yy - y)
    y += brief_h + 4
    print(f"briefs end {y}")

    # ---- date check strip
    f_check = font("sans_b", P["check_size"])
    lines = wrap(d, DATE_CHECK, f_check, CONTENT_W - 44)
    strip_h = len(lines) * P["check_lead"] + 22
    d.rectangle([MARGIN, y, CANVAS - MARGIN, y + strip_h], fill=RED)
    cy = y + 11
    for line in lines:
        d.text((MARGIN + 22, cy), line, font=f_check, fill=WHITE)
        cy += P["check_lead"]
    y += strip_h
    print(f"date check ends {y} of {CANVAS}")
    assert y <= CANVAS, f"page overflows: content ends at {y}"

    # ---- final render at 1024
    final = page.resize((1024, 1024), Image.LANCZOS)
    out = os.path.join(HERE, "page.png")
    final.save(out, format="PNG", optimize=True)
    size = os.path.getsize(out)
    if size > 1_000_000:
        final.convert("RGB").quantize(colors=256, method=Image.MEDIANCUT) \
            .save(out, format="PNG", optimize=True)
        size = os.path.getsize(out)
    print(f"page.png: {size} bytes")
    assert size <= 1_000_000, f"page.png too large: {size}"
    return out


if __name__ == "__main__":
    build()
