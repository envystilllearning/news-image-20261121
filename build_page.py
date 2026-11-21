#!/usr/bin/env python3
"""Build the Saturday 21 November 2026 news front page (v2: panel-rich layout).

Composes 14 fresh, text-free illustration elements into a 2048x2048
broadsheet page. Every word is typeset here, from the verified story
list in dataset.md, so nothing on the page can be misspelled.
Output: page.png at 1024x1024, <= 1,000,000 bytes.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
EL = os.path.join(HERE, "elements")
W = 2048
M = 44                      # page margin
CW = W - 2 * M              # content width = 1960
CREAM = (245, 239, 226)
INK = (18, 16, 14)
RED = (200, 16, 46)
WHITE = (255, 255, 255)
GRAY = (90, 84, 76)
TINTS = [(220, 232, 228), (239, 227, 200), (240, 220, 210)]

FD = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FD + "LiberationSerif-Bold.ttf"
SERIF_I = FD + "LiberationSerif-Italic.ttf"
SANS = FD + "LiberationSans-Regular.ttf"
SANS_B = FD + "LiberationSans-Bold.ttf"
SANS_I = FD + "LiberationSans-Italic.ttf"

# ---- tunable sizes (measured layout; bottom must stay <= 2048) ----
P = dict(
    caps=24, title=86, stand=25,
    stat_n=46, stat_c=18,
    region=22, bar_h=22,
    hero_panel=126, hero_k=23, hero_h=33, hero_b=24, hero_s=20,
    med_panel=74, med_k=20, med_h=23, med_l=20,
    map_head=26, map_h=156, map_leg=23,
    brief=21, brief_lh=25,
    dc=22, dc_lh=28, foot=19,
)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def wrap_mixed(d, parts, width):
    """Wrap [(text, font), ...] as one paragraph; returns lines of segments."""
    tokens = []  # (word, font)
    for text, font in parts:
        for w in text.split():
            tokens.append((w, font))
    space_w = {id(f): d.textlength(" ", font=f) for _, f in parts}
    lines, cur, cur_w = [], [], 0.0
    for w, f in tokens:
        ww = d.textlength(w, font=f)
        add = ww if not cur else ww + space_w[id(f)]
        if cur and cur_w + add > width:
            lines.append(cur)
            cur, cur_w = [(w, f)], ww
        else:
            cur.append((w, f))
            cur_w += add
    if cur:
        lines.append(cur)
    return lines


def draw_mixed(d, lines, x, y, lh, color=INK):
    for line in lines:
        cx = x
        for w, f in line:
            d.text((cx, y), w, font=f, fill=color)
            cx += d.textlength(w, font=f) + d.textlength(" ", font=f)
        y += lh
    return y


def paste_cover(img, path, box):
    """Scale-to-cover + centre crop into box (x, y, w, h)."""
    x, y, w, h = box
    im = Image.open(path).convert("RGB")
    sc = max(w / im.width, h / im.height)
    im = im.resize((max(1, round(im.width * sc)), max(1, round(im.height * sc))),
                   Image.LANCZOS)
    ox = (im.width - w) // 2
    oy = (im.height - h) // 2
    img.paste(im.crop((ox, oy, ox + w, oy + h)), (x, y))


def banner(d, x, y, text, font, h):
    tw = d.textlength(text, font=font)
    d.rectangle([x, y, x + tw + 22, y + h], fill=RED)
    d.text((x + 11, y + h // 2 - font.size // 2 - 2), text, font=font, fill=WHITE)
    return tw + 22


# ---------------------------------------------------------------- data
HEROES = [
    dict(img="el_hero1.jpg", label="ICJ: GENOCIDE VERDICT",
         kicker="1 · THE HAGUE · JUSTICE",
         head="World court finds Myanmar guilty of genocide",
         body="Judges voted 9 to 6 that Myanmar committed genocide against the Rohingya in 2017. Myanmar must prosecute the commanders and pay reparations.",
         src="Sources: ICJ, Reuters"),
    dict(img="el_hero2.jpg", label="KYIV: 400 DRONES",
         kicker="2 · KYIV · WAR",
         head="Russia fires 400 drones at Ukraine; two missiles land in Poland",
         body="The barrage killed at least eight in Kyiv and hit bridges and rail stations. Warsaw calls the missiles in Poland a deliberate provocation.",
         src="Sources: France 24, CBS News"),
    dict(img="el_hero3.jpg", label="COP31: OVERTIME",
         kicker="3 · ANTALYA · CLIMATE",
         head="COP31 runs past its deadline with no deal",
         body="Nearly 200 nations failed to close on Friday; the draft deletes the words \u201cfossil fuel\u201d. A call to triple adaptation funding by 2035 survives.",
         src="Sources: AFP, Al Jazeera"),
]

MEDIUMS = [
    dict(img="el_m4.jpg", label="RIYADH: MISSILES DOWN", kicker="4 · RIYADH · WAR",
         head="Saudi Arabia downs three Houthi missiles over Riyadh",
         line="Second attack on the capital in two days. No casualties. (Reuters)"),
    dict(img="el_m5.jpg", label="PERU: QUAKE 6.7", kicker="5 · JUNÍN · EARTHQUAKE",
         head="Magnitude 6.7 quake shakes central Peru",
         line="Felt in Lima. Depth disputed: 108 km (USGS), 129 km (IGP). (USGS, IGP, AFP)"),
    dict(img="el_m6.jpg", label="BITCOIN: TWO-YEAR LOW", kicker="6 · MARKETS · CRYPTO",
         head="Bitcoin crashes through $60,000 to a two-year low",
         line="The AI rout spilled into crypto; bitcoin touched $55,500, down 18% in seven days. (Reuters, CoinGecko)"),
    dict(img="el_m7.jpg", label="DAVAO: 146 SAFE", kicker="7 · DAVAO · AVIATION",
         head="146 people walk away from an engine-fire scare",
         line="An Air Niugini 767 diverted on a fire indication. All 146 aboard left by the slides. (AP, CAAP)"),
    dict(img="el_m8.jpg", label="BRUSSELS: EU DEAL", kicker="8 · BRUSSELS · POLITICS",
         head="UK and EU sign their biggest post-Brexit deal",
         line="Food exports, carbon markets, youth mobility. (BBC)"),
    dict(img="el_m9.jpg", label="CARDS: CYBER SCARE", kicker="9 · NEW YORK · CYBER",
         head="Three card giants report vendor cyber incidents",
         line="JPMorgan, Visa and Mastercard say payments run as normal. (Reuters)"),
    dict(img="el_m10.jpg", label="GTA 6: ON SALE", kicker="10 · LEONIDA · GAMES",
         head="GTA 6 goes on sale; players move to Leonida",
         line="Release weekend, 13 years after the last game. (IGN)"),
    dict(img="el_m11.jpg", label="RAHUL: 136", kicker="11 · WELLINGTON · CRICKET",
         head="Rahul makes 136 and India take a 118-run lead",
         line="Gill fell for 98. India closed day three on 486 for 4; New Zealand made 368. (ESPNcricinfo)"),
    dict(img="el_m12.jpg", label="PAKISTAN: SERIES WON", kicker="12 · LAHORE · CRICKET",
         head="Pakistan beat Sri Lanka by eight wickets, take the series",
         line="The win ends a two-year series drought. (Dawn)"),
    dict(img="el_m13.jpg", label="VEGAS: RUSSELL P1", kicker="13 · LAS VEGAS · FORMULA 1",
         head="Russell tops Vegas practice, clashes with Verstappen",
         line="His 1:34.041 led a Mercedes one-two. Stewards will investigate the contact. (Reuters, FIA)"),
]

STATS = [("10,000", "Rohingya killed in 2017"), ("9–6", "the judges' vote"),
         ("400+", "drones over Ukraine"), ("3", "missiles downed, Riyadh"),
         ("6.7", "the Peru quake"), ("$55.5K", "bitcoin's two-year low")]
REGIONS = [("Europe", 7), ("Asia", 12), ("Middle East", 3),
           ("Americas", 9), ("Oceania", 1), ("Global", 3)]

PINS = [(1, 4.5, 52.1, "The Hague"), (2, 30.5, 50.4, "Kyiv"),
        (3, 30.7, 36.9, "Antalya"), (4, 46.7, 24.6, "Riyadh"),
        (5, -75.5, -11.5, "Junín (Peru)"), (6, -74.0, 40.7, "New York"),
        (7, 125.6, 7.1, "Davao"), (8, 4.35, 50.85, "Brussels"),
        (9, -81.0, 27.0, "Florida"), (10, 174.8, -41.3, "Wellington"),
        (11, 74.3, 31.5, "Lahore"), (12, -115.1, 36.1, "Las Vegas"),
        (13, 85.1, 19.8, "Odisha")]

BRIEFS = [
    (14, "Shenzhen", "Trump, Xi and Putin open a trilateral summit and sign fuel deals", "Reuters"),
    (15, "Moscow", "Russia rules out NATO membership in any Ukraine settlement", "TASS"),
    (16, "Budapest", "Hungary drops its block on the EU package", "Reuters"),
    (17, "Naypyidaw", "Myanmar calls the genocide ruling biased and unjust", "AFP"),
    (18, "Gaza", "UNICEF counts child casualties still rising", "UNICEF"),
    (19, "Kuala Lumpur", "Malaysia will resettle 10,000 Rohingya in Türkiye", "Bernama"),
    (20, "New York", "A US court jails an Indian national for 19 years over a plot to kill a Sikh separatist", "AP"),
    (21, "Washington", "Trump attacks the Fed over interest rates", "Bloomberg"),
    (22, "Jakarta", "Indonesia counts $30 billion in fire losses", "Antara"),
    (23, "Rome", "The WFP warns 2027 food aid falls short", "WFP"),
    (24, "Kathmandu", "Nepal's prime minister visits India on 22–23 November", "PTI"),
    (25, "Delhi", "Pakistan's climate minister joins the SCO forum in India", "Dawn"),
    (26, "Gaza", "Israeli strikes kill Palestinians as West Bank violence continues", "One Turn"),
    (27, "Washington", "Trump threatens to ban US firms from building AI data centres abroad", "Reuters"),
    (28, "Washington", "A hacker reportedly breaches an FBI criminal database as outages continue", "One Turn"),
    (29, "London", "A trial pill makes pancreatic tumours undetectable in 1 in 12 patients", "One Turn"),
    (30, "Berlin", "Gen Z protests spread across 25 European countries", "One Turn"),
    (31, "Los Angeles", "A court convicts the man who started the deadly Palisades fire", "AFP"),
    (32, "Port-au-Prince", "Salvadoran troops in Haiti lose soldiers to explosives", "One Turn"),
    (33, "Madrid", "Spain sets a 29 November election as conservatives gain", "El País"),
    (34, "Odisha", "Crews clear Cyclone Akvan's damage as the storm weakens", "PTI"),
    (35, "Kuno", "A cheetah brought from Botswana gives birth to four cubs", "PTI"),
]

DATE_CHECK = ("Left out as Friday's news: the first strikes on Kyiv's bridges "
              "(Saturday's barrage is story 2), Thursday's missile hit on Riyadh's "
              "PIF tower, the Sensex's 898-point Friday close, and Akvan's "
              "landfall; its clean-up is brief 34. Not confirmed when drawn: a "
              "final COP31 text, and whether any fire burned on the Davao jet — "
              "officials report an indication, not a fire.")
FOOTER = ("Every story here happened, or was first reported, on Saturday 21 "
          "November 2026. Officials' counts and claims are attributed. "
          "Sources named beside each story.")


def build():
    img = Image.new("RGB", (W, W), CREAM)
    d = ImageDraw.Draw(img)
    y = 26

    # ---- masthead ----
    f = F(SANS_B, P["caps"])
    t = "THE WORLD IN ONE DAY — SATURDAY EDITION"
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=RED)
    y += P["caps"] + 12
    f = F(SERIF_B, P["title"])
    t = "Saturday 21 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
    y += P["title"] + 10
    f = F(SERIF_I, P["stand"])
    t = "World court convicts Myanmar of genocide · 400 drones over Kyiv · COP31 ends without a deal"
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
    y += P["stand"] + 12
    d.line([M, y, W - M, y], fill=INK, width=4)
    y += 14

    # ---- stat band ----
    fn, fc = F(SERIF_B, P["stat_n"]), F(SANS, P["stat_c"])
    colw = CW // 6
    for i, (num, cap) in enumerate(STATS):
        x = M + i * colw
        if i:
            d.line([x - 12, y + 4, x - 12, y + P["stat_n"] + P["stat_c"] + 8],
                   fill=GRAY, width=1)
        d.text((x, y), num, font=fn, fill=INK)
        d.text((x, y + P["stat_n"] + 6), cap, font=fc, fill=GRAY)
    y += P["stat_n"] + P["stat_c"] + 16
    d.line([M, y, W - M, y], fill=INK, width=2)
    y += 10

    # ---- region bar ----
    total = sum(n for _, n in REGIONS)
    x = M
    for i, (_, n) in enumerate(REGIONS):
        wseg = CW * n // total
        if i == len(REGIONS) - 1:
            wseg = W - M - x
        d.rectangle([x, y, x + wseg, y + P["bar_h"]],
                    fill=RED if i % 2 else INK)
        x += wseg
    y += P["bar_h"] + 6
    f = F(SANS, P["region"])
    t = "  ·  ".join(f"{name} {n}" for name, n in REGIONS)
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
    y += P["region"] + 14

    # ---- heroes ----
    fk, fh, fb, fs = (F(SANS_B, P["hero_k"]), F(SERIF_B, P["hero_h"]),
                      F(SANS, P["hero_b"]), F(SANS_I, P["hero_s"]))
    flab = F(SANS_B, 23)
    gap, colw = 29, (CW - 2 * 29) // 3
    # measure
    cards = []
    for hro in HEROES:
        hh = len(wrap(d, hro["head"], fh, colw - 16))
        hb = len(wrap(d, hro["body"], fb, colw - 16))
        cards.append((hh, hb))
    card_h = (P["hero_panel"] + 8 + P["hero_k"] + 6 +
              max(c[0] for c in cards) * (P["hero_h"] + 7) + 5 +
              max(c[1] for c in cards) * (P["hero_b"] + 5) + 5 + P["hero_s"] + 4)
    for i, hro in enumerate(HEROES):
        x = M + i * (colw + gap)
        d.rectangle([x - 8, y - 6, x + colw + 8, y + card_h + 6], fill=TINTS[i % 3])
        paste_cover(img, os.path.join(EL, hro["img"]), (x, y, colw, P["hero_panel"]))
        banner(d, x, y, hro["label"], flab, 36)
        ty = y + P["hero_panel"] + 8
        d.text((x, ty), hro["kicker"], font=fk, fill=RED)
        ty += P["hero_k"] + 6
        for ln in wrap(d, hro["head"], fh, colw - 16):
            d.text((x, ty), ln, font=fh, fill=INK)
            ty += P["hero_h"] + 7
        ty += 5
        for ln in wrap(d, hro["body"], fb, colw - 16):
            d.text((x, ty), ln, font=fb, fill=INK)
            ty += P["hero_b"] + 5
        ty += 5
        d.text((x, ty), hro["src"], font=fs, fill=GRAY)
    y += card_h + 18

    # ---- mediums ----
    fk, fh, fl = (F(SANS_B, P["med_k"]), F(SANS_B, P["med_h"]), F(SANS, P["med_l"]))
    flab = F(SANS_B, 18)
    gap, colw = 25, (CW - 4 * 25) // 5
    for row in range(2):
        group = MEDIUMS[row * 5:(row + 1) * 5]
        hh = max(len(wrap(d, m["head"], fh, colw - 12)) for m in group)
        hl = max(len(wrap(d, m["line"], fl, colw - 12)) for m in group)
        card_h = (P["med_panel"] + 6 + P["med_k"] + 4 + hh * (P["med_h"] + 5) +
                  4 + hl * (P["med_l"] + 5))
        for i, m in enumerate(group):
            x = M + i * (colw + gap)
            d.rectangle([x - 7, y - 5, x + colw + 7, y + card_h + 5],
                        fill=TINTS[(row * 5 + i) % 3])
            paste_cover(img, os.path.join(EL, m["img"]), (x, y, colw, P["med_panel"]))
            banner(d, x, y, m["label"], flab, 29)
            ty = y + P["med_panel"] + 6
            d.text((x, ty), m["kicker"], font=fk, fill=RED)
            ty += P["med_k"] + 4
            for ln in wrap(d, m["head"], fh, colw - 12):
                d.text((x, ty), ln, font=fh, fill=INK)
                ty += P["med_h"] + 5
            ty += 4
            for ln in wrap(d, m["line"], fl, colw - 12):
                d.text((x, ty), ln, font=fl, fill=INK)
                ty += P["med_l"] + 5
        y += card_h + 14

    # ---- map band ----
    f = F(SANS_B, P["map_head"])
    d.text((M, y), "ALSO ON SATURDAY 21 NOVEMBER", font=f, fill=RED)
    y += P["map_head"] + 8
    map_box_w = 500
    mim = Image.open(os.path.join(EL, "el_map.jpg")).convert("RGB")
    sc = min(map_box_w / mim.width, P["map_h"] / mim.height)
    mw2, mh2 = int(mim.width * sc), int(mim.height * sc)
    mim = mim.resize((mw2, mh2), Image.LANCZOS)
    mx = M + (map_box_w - mw2) // 2
    img.paste(mim, (mx, y))
    fp = F(SANS_B, 14)
    for n, lon, lat, _name in PINS:
        px = mx + int((lon + 180) / 360 * mw2)
        py = y + int((0.40 + (27 - lat) / 187) * mh2)
        if n == 8:  # Brussels nudged off The Hague
            px, py = px + 13, py + 8
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED, outline=WHITE, width=2)
        s = str(n)
        d.text((px - d.textlength(s, font=fp) / 2, py - 8), s, font=fp, fill=WHITE)
    fl = F(SANS, P["map_leg"])
    lx = M + map_box_w + 28
    colw_l = (W - M - lx) // 3
    for i, (n, _lon, _lat, name) in enumerate(PINS):
        cx = lx + (i % 3) * colw_l
        cy = y + (i // 3) * (P["map_leg"] + 7)
        d.text((cx, cy), f"{n} {name}", font=fl, fill=INK)
    y += P["map_h"] + 12

    # ---- briefs (3 columns, filled down) ----
    fb_b, fb_r = F(SANS_B, P["brief"]), F(SANS, P["brief"])
    colw = (CW - 2 * 29) // 3
    counts = [8, 7, 7]
    idx = 0
    col_ends = []
    for c in range(3):
        x = M + c * (colw + 29)
        cy = y
        for _ in range(counts[c]):
            n, city, text, src = BRIEFS[idx]
            idx += 1
            parts = [(f"{n} {city} — ", fb_b), (f"{text} ({src})", fb_r)]
            lines = wrap_mixed(d, parts, colw - 8)
            cy = draw_mixed(d, lines, x, cy, P["brief_lh"])
            cy += 9
        col_ends.append(cy)
    y = max(col_ends) + 4

    # ---- date check box ----
    fd_b, fd_r = F(SANS_B, P["dc"]), F(SANS, P["dc"])
    parts = [("DATE CHECK — ", fd_b), (DATE_CHECK, fd_r)]
    lines = wrap_mixed(d, parts, CW - 48)
    box_h = len(lines) * P["dc_lh"] + 22
    d.rectangle([M, y, W - M, y + box_h], outline=RED, width=3)
    draw_mixed(d, lines, M + 24, y + 11, P["dc_lh"])
    y += box_h + 12

    # ---- footer ----
    f = F(SANS_I, P["foot"])
    for ln in wrap(d, FOOTER, f, CW):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=GRAY)
        y += P["foot"] + 5

    print("bottom edge:", y, "of", W)
    out = img.resize((1024, 1024), Image.LANCZOS)
    tmp = os.path.join(HERE, "_page_tmp.png")
    out.save(tmp)
    size = os.path.getsize(tmp)
    if size > 1_000_000:
        out = out.quantize(colors=256)
        out.save(tmp)
        size = os.path.getsize(tmp)
    os.replace(tmp, os.path.join(HERE, "page.png"))
    print("page.png bytes:", size)


if __name__ == "__main__":
    build()
