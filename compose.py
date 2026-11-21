#!/usr/bin/env python3
"""Compose the Saturday 21 Nov 2026 front page v3: Gemini illustration
elements + program typesetting (all text set here, measured layout).
Canvas 2048x2048 -> export 1024 (JPEG + 256-colour PNG)."""
import os
from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
EL = os.path.join(BASE, "elements")
SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SERIF_I = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

CREAM = (245, 239, 226)
INK = (22, 18, 14)
RED = (176, 28, 38)
GRAY = (96, 88, 76)
WHITE = (250, 247, 240)
W, M = 2048, 48
CW = W - 2 * M

def F(p, s):
    return ImageFont.truetype(p, s)

def wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines

def paste_crop(img, path, box):
    x, y, w, h = box
    if os.path.exists(path):
        im = Image.open(path).convert("RGB")
        s = max(w / im.width, h / im.height)
        im = im.resize((int(im.width * s) + 1, int(im.height * s) + 1), Image.LANCZOS)
        ox, oy = (im.width - w) // 2, (im.height - h) // 2
        im = im.crop((ox, oy, ox + w, oy + h))
    else:
        im = Image.new("RGB", (w, h), (233, 226, 208))
        ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=RED, width=3)
    img.paste(im, (x, y))

def main():
    img = Image.new("RGB", (W, W), CREAM)
    d = ImageDraw.Draw(img)
    y = 34

    # masthead
    f = F(SANS_B, 31)
    t = "THE WORLD IN ONE DAY — SATURDAY EDITION"
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=RED)
    y += 42
    f = F(SERIF_B, 118)
    t = "Saturday 21 November 2026"
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
    y += 128
    f = F(SERIF_I, 34)
    t = "World court convicts Myanmar of genocide · 400 drones over Kyiv · COP31 ends without a deal"
    for ln in wrap(d, t, f, CW):
        d.text(((W - d.textlength(ln, font=f)) / 2, y), ln, font=f, fill=INK)
        y += 42
    y += 6
    d.line([M, y, W - M, y], fill=INK, width=4)
    y += 14

    # stats
    stats = [("10,000", "Rohingya killed in 2017"), ("9–6", "the judges' vote"),
             ("400+", "drones over Ukraine"), ("3", "missiles downed, Riyadh"),
             ("6.7", "the Peru quake"), ("$55.5K", "bitcoin's two-year low")]
    colw = CW // 6
    fn, fl = F(SANS_B, 58), F(SANS_R, 24)
    for i, (num, lab) in enumerate(stats):
        x = M + i * colw
        d.text((x + 6, y), num, font=fn, fill=INK)
        d.text((x + 6, y + 66), lab, font=fl, fill=GRAY)
        if i:
            d.line([x, y + 2, x, y + 92], fill=GRAY, width=2)
    y += 90
    d.line([M, y, W - M, y], fill=INK, width=3)
    y += 12

    # region bar
    regions = [("Europe", 7, RED), ("Asia", 12, INK), ("Middle East", 3, RED),
               ("Americas", 9, INK), ("Oceania", 1, RED), ("Global", 3, INK)]
    total = sum(c for _, c, _ in regions)
    x = M
    for name, c, col in regions:
        wseg = int(CW * c / total)
        d.rectangle([x, y, x + wseg, y + 34], fill=col)
        x += wseg
    y += 42
    f = F(SANS_B, 25)
    t = "   ·   ".join(f"{n} {c}" for n, c, _ in regions)
    d.text(((W - d.textlength(t, font=f)) / 2, y), t, font=f, fill=INK)
    y += 36
    d.line([M, y, W - M, y], fill=INK, width=3)
    y += 14

    # heroes (measured)
    heroes = [
        ("el_hero1.jpg", "1 · THE HAGUE · JUSTICE",
         "World court finds Myanmar guilty of genocide",
         "Judges voted 9 to 6 that Myanmar committed genocide against the Rohingya in 2017. Myanmar must prosecute the commanders and pay reparations.",
         "Sources: ICJ, Reuters"),
        ("el_hero2.jpg", "2 · KYIV · WAR",
         "Russia fires 400 drones at Ukraine; two missiles land in Poland",
         "The barrage killed at least eight in Kyiv and hit bridges and rail stations. Warsaw calls the missiles in Poland a deliberate provocation.",
         "Sources: France 24, CBS News"),
        ("el_hero3.jpg", "3 · ANTALYA · CLIMATE",
         "COP31 runs past its deadline with no deal",
         "Nearly 200 nations failed to close on Friday; the draft deletes the words \u201cfossil fuel\u201d. A call to triple adaptation funding by 2035 survives.",
         "Sources: AFP, Al Jazeera"),
    ]
    gap = 24
    colw = (CW - 2 * gap) // 3
    fk, fh, fb, fs = F(SANS_B, 26), F(SERIF_B, 44), F(SERIF_R, 26), F(SANS_R, 22)
    hy, hend = y, y
    for i, (el, kick, head, body, src) in enumerate(heroes):
        x = M + i * (colw + gap)
        paste_crop(img, os.path.join(EL, el), (x, hy, colw, 104))
        ty = hy + 114
        d.text((x, ty), kick, font=fk, fill=RED)
        ty += 34
        for ln in wrap(d, head, fh, colw):
            d.text((x, ty), ln, font=fh, fill=INK)
            ty += 52
        ty += 2
        for ln in wrap(d, body, fb, colw):
            d.text((x, ty), ln, font=fb, fill=INK)
            ty += 32
        ty += 3
        d.text((x, ty), src, font=fs, fill=GRAY)
        hend = max(hend, ty + 26)
        if i:
            d.line([x - gap // 2, hy, x - gap // 2, hy + 430], fill=GRAY, width=2)
    y = hend + 10
    d.line([M, y, W - M, y], fill=INK, width=3)
    y += 14

    # mediums (measured rows)
    mediums = [
        ("el_m4.jpg", "4 · RIYADH · WAR", "Saudi Arabia downs three Houthi missiles over Riyadh",
         "Second attack on the capital in two days. No casualties. (Reuters)"),
        ("el_m5.jpg", "5 · JUNÍN · EARTHQUAKE", "Magnitude 6.7 quake shakes central Peru",
         "Felt in Lima. Depth disputed: 108 km (USGS), 129 km (IGP). (USGS, AFP)"),
        ("el_m6.jpg", "6 · MARKETS · CRYPTO", "Bitcoin crashes through $60,000 to a two-year low",
         "The AI rout spilled into crypto; bitcoin touched $55,500, down 18% in seven days. (Reuters, CoinGecko)"),
        ("el_m7.jpg", "7 · DAVAO · AVIATION", "146 people walk away from an engine-fire scare",
         "An Air Niugini 767 diverted on a fire indication. All 146 aboard left by the slides. (AP, CAAP)"),
        ("el_m8.jpg", "8 · BRUSSELS · POLITICS", "UK and EU sign their biggest post-Brexit deal",
         "Food exports, carbon markets, youth mobility. (BBC)"),
        ("el_m9.jpg", "9 · NEW YORK · CYBER", "Three card giants report vendor cyber incidents",
         "JPMorgan, Visa and Mastercard say payments run as normal. (Reuters)"),
        ("el_m10.jpg", "10 · LEONIDA · GAMES", "GTA 6 goes on sale; players move to Leonida",
         "Release weekend, 13 years after the last game. (IGN)"),
        ("el_m11.jpg", "11 · WELLINGTON · CRICKET", "Rahul makes 136 and India take a 118-run lead",
         "Gill fell for 98. India closed day three on 486 for 4; New Zealand made 368. (ESPNcricinfo)"),
        ("el_m12.jpg", "12 · LAHORE · CRICKET", "Pakistan beat Sri Lanka by eight wickets, take the series",
         "The win ends a two-year series drought. (Dawn)"),
        ("el_m13.jpg", "13 · LAS VEGAS · FORMULA 1", "Russell tops Vegas practice, clashes with Verstappen",
         "His 1:34.041 led a Mercedes one-two. Stewards will investigate the contact. (Reuters, FIA)"),
    ]
    gap = 16
    colw = (CW - 4 * gap) // 5
    fk, fh, fb = F(SANS_B, 20), F(SANS_B, 24), F(SANS_R, 21)
    for r in range(2):
        ry, rend = y, y
        for c in range(5):
            el, kick, head, line = mediums[r * 5 + c]
            x = M + c * (colw + gap)
            paste_crop(img, os.path.join(EL, el), (x, ry, colw, 42))
            ty = ry + 50
            d.text((x, ty), kick, font=fk, fill=RED)
            ty += 27
            for ln in wrap(d, head, fh, colw):
                d.text((x, ty), ln, font=fh, fill=INK)
                ty += 29
            for ln in wrap(d, line, fb, colw):
                d.text((x, ty), ln, font=fb, fill=INK)
                ty += 26
            rend = max(rend, ty)
        y = rend + 10
    d.line([M, y, W - M, y], fill=INK, width=3)
    y += 12

    # bottom: heading, map row, briefs
    f = F(SANS_B, 30)
    d.text((M, y), "ALSO ON SATURDAY 21 NOVEMBER", font=f, fill=RED)
    y += 40
    mapw, maph = 700, 190
    # contain-fit the full map (cropped to its landmass frame) so pins align
    mim = Image.open(os.path.join(EL, "el_map.jpg")).convert("RGB")
    mim = mim.crop((0, int(mim.height * 0.02), mim.width, int(mim.height * 0.86)))
    sc = min(mapw / mim.width, maph / mim.height)
    mw2, mh2 = int(mim.width * sc), int(mim.height * sc)
    mim = mim.resize((mw2, mh2), Image.LANCZOS)
    mx = M + (mapw - mw2) // 2
    img.paste(mim, (mx, y))
    pins = [(1, 4.5, 52.1), (2, 30.5, 50.4), (3, 30.7, 36.9), (4, 46.7, 24.6),
            (5, -75.5, -11.5), (6, -74.0, 40.7), (7, 125.6, 7.1), (8, 4.35, 50.85),
            (9, -81.0, 27.0), (10, 174.8, -41.3), (11, 74.3, 31.5),
            (12, -115.1, 36.1), (13, 85.1, 19.8)]
    fp = F(SANS_B, 16)
    for n, lon, lat in pins:
        px = mx + int((lon + 180) / 360 * mw2)
        py = y + int((0.452 + (27 - lat) / 157) * mh2)
        if n == 8:  # Brussels sits on top of The Hague at this scale; nudge
            px, py = px + 13, py + 8
        d.ellipse([px - 11, py - 11, px + 11, py + 11], fill=RED, outline=WHITE, width=2)
        s = str(n)
        d.text((px - d.textlength(s, font=fp) / 2, py - 8), s, font=fp, fill=WHITE)
    names = ["1 The Hague", "2 Kyiv", "3 Antalya", "4 Riyadh", "5 Junín (Peru)",
             "6 New York", "7 Davao", "8 Brussels", "9 Florida", "10 Wellington",
             "11 Lahore", "12 Las Vegas", "13 Odisha"]
    fl2 = F(SANS_R, 22)
    lx = M + mapw + 28
    for i, nm in enumerate(names):
        cx = lx + (i % 2) * 430
        cy = y + (i // 2) * 27
        d.text((cx, cy), nm, font=fl2, fill=INK)
    y += maph + 12

    briefs = [
        ("14", "Shenzhen", "Trump, Xi and Putin open a trilateral summit and sign fuel deals (Reuters)"),
        ("15", "Moscow", "Russia rules out NATO membership in any Ukraine settlement (TASS)"),
        ("16", "Budapest", "Hungary drops its block on the EU package (Reuters)"),
        ("17", "Naypyidaw", "Myanmar calls the genocide ruling biased and unjust (AFP)"),
        ("18", "Gaza", "UNICEF counts child casualties still rising (UNICEF)"),
        ("19", "Kuala Lumpur", "Malaysia will resettle 10,000 Rohingya in Türkiye (Bernama)"),
        ("20", "New York", "A US court jails an Indian national for 19 years over a plot to kill a Sikh separatist (AP)"),
        ("21", "Washington", "Trump attacks the Fed over interest rates (Bloomberg)"),
        ("22", "Jakarta", "Indonesia counts $30 billion in fire losses (Antara)"),
        ("23", "Rome", "The WFP warns 2027 food aid falls short (WFP)"),
        ("24", "Kathmandu", "Nepal's prime minister visits India on 22–23 November (PTI)"),
        ("25", "Delhi", "Pakistan's climate minister joins the SCO forum in India (Dawn)"),
        ("26", "Gaza", "Israeli strikes kill Palestinians as West Bank violence continues (One Turn)"),
        ("27", "Washington", "Trump threatens to ban US firms from building AI data centres abroad (Reuters)"),
        ("28", "Washington", "A hacker reportedly breaches an FBI criminal database as outages continue (One Turn)"),
        ("29", "London", "A trial pill makes pancreatic tumours undetectable in 1 in 12 patients (One Turn)"),
        ("30", "Berlin", "Gen Z protests spread across 25 European countries (One Turn)"),
        ("31", "Los Angeles", "A court convicts the man who started the deadly Palisades fire (AFP)"),
        ("32", "Port-au-Prince", "Salvadoran troops in Haiti lose soldiers to explosives (One Turn)"),
        ("33", "Madrid", "Spain sets a 29 November election as conservatives gain (El País)"),
        ("34", "Odisha", "Crews clear Cyclone Akvan's damage as the storm weakens (PTI)"),
        ("35", "Kuno", "A cheetah brought from Botswana gives birth to four cubs (PTI)"),
    ]
    fb2 = F(SANS_R, 19)
    bgap = 20
    bw = (CW - 2 * bgap) // 3
    cols = [briefs[:8], briefs[8:15], briefs[15:]]
    bend = y
    for ci, col in enumerate(cols):
        cx = M + ci * (bw + bgap)
        cy = y
        for num, place, text in col:
            for ln in wrap(d, f"{num} {place} — {text}", fb2, bw):
                d.text((cx, cy), ln, font=fb2, fill=INK)
                cy += 23
            cy += 5
        bend = max(bend, cy)
    y = bend + 8

    strip = ("DATE CHECK — Left out as Friday's news: the first strikes on Kyiv's bridges (Saturday's barrage is "
             "story 2), Thursday's missile hit on Riyadh's PIF tower, the Sensex's 898-point Friday close, and "
             "Akvan's landfall; its clean-up is brief 34. Not confirmed when drawn: a final COP31 text, and whether "
             "any fire burned on the Davao jet — officials report an indication, not a fire.")
    f = F(SANS_R, 21)
    lines = wrap(d, strip, f, CW - 32)
    sh = len(lines) * 26 + 14
    d.rectangle([M, y, W - M, y + sh], fill=RED)
    ty = y + 7
    for ln in lines:
        d.text((M + 16, ty), ln, font=f, fill=WHITE)
        ty += 26
    print("bottom edge:", y + sh, "of", W)

    img.save(os.path.join(BASE, "page_v3_full.png"))
    small = img.resize((1024, 1024), Image.LANCZOS)
    small.save(os.path.join(BASE, "page_v3_1024.jpg"), quality=88)
    small.quantize(colors=256, method=Image.MEDIANCUT).save(os.path.join(BASE, "page_v3.png"))
    print("jpg", os.path.getsize(os.path.join(BASE, "page_v3_1024.jpg")),
          "png", os.path.getsize(os.path.join(BASE, "page_v3.png")))

if __name__ == "__main__":
    main()
