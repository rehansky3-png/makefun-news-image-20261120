#!/usr/bin/env python3
"""THE WORLD — Friday 20 November 2026.
One-page newspaper front page, drawn entirely in code with Pillow.
Deterministic: same input -> same PNG bytes every run.
Stdlib + Pillow only. Run: python3 main.py  (writes entry.png next to main.py)
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 16  # outer margin

# ---- palette: warm newsprint ----
PAPER = (250, 246, 236)
INK = (24, 24, 22)
RED = (178, 34, 28)
DARKRED = (140, 22, 18)
NAVY = (26, 42, 74)
BLUE = (44, 82, 130)
TEAL = (18, 110, 105)
GREEN = (46, 110, 58)
GOLD = (176, 128, 28)
GREY = (110, 108, 100)
LINE = (24, 24, 22)
SOFT = (232, 226, 212)
CREAM = (244, 238, 222)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIFI = "/usr/share/fonts/truetype/noto/NotoSerif-Italic.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    """Greedy word wrap; returns list of lines fitting width."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= width:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, lines, font, fill=INK, leading=None):
    if leading is None:
        leading = font.size + 2
    for ln in lines:
        d.text((x, y), ln, font=font, fill=fill)
        y += leading
    return y


def rule(d, x, y, w, weight=2, fill=INK):
    d.rectangle([x, y, x + w, y + weight - 1], fill=fill)


def tag(d, x, y, label, font, bg, fg=(255, 255, 255)):
    tw = d.textlength(label, font=font)
    pad = 6
    d.rectangle([x, y, x + tw + pad * 2, y + font.size + 6], fill=bg)
    d.text((x + pad, y + 3), label, font=font, fill=fg)
    return x + tw + pad * 2


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    d.text((M, 2), "THE WORLD IN ONE DAY", font=F(SANSB, 12), fill=RED)
    r = "44 STORIES  ·  7 REGIONS  ·  EVERY ONE FROM FRIDAY 20 NOVEMBER 2026"
    d.text((W - M - d.textlength(r, font=F(SANSB, 12)), 2),
           r, font=F(SANSB, 12), fill=INK)
    rule(d, M, 20, W - 2 * M, 3)
    d.text((M, 24), "Friday 20 November 2026", font=F(SERIFB, 52), fill=INK)
    sub = ("Russian missiles hit Kyiv\u2019s bridges  ·  Cyclone Akvan strikes India  ·  "
           "An AI sell-off sinks world markets  ·  UK and EU seal a deal")
    d.text((M, 82), sub, font=F(SERIFI, 15), fill=(60, 58, 52))
    rule(d, M, 102, W - 2 * M, 2)


# ---------------------------------------------------------------- figures
FIGURES = [
    ("110+", "missiles Russia fired at Ukraine"),
    ("27", "of them ballistic missiles"),
    ("300,000+", "people moved to shelters before Akvan"),
    ("\u22126.2%", "Taiwan\u2019s index at Friday\u2019s close"),
    ("\u221214%", "Nvidia after a report of an SEC probe"),
    ("844", "under-5s killed by Ebola in DR Congo"),
    ("100,000", "youth visas a year in the UK\u2013EU deal"),
    ("209 mm", "of rain at Patrapur as Akvan crossed Odisha"),
]


def draw_figures(d):
    y = 110
    cw = (W - 2 * M) // 8
    for i, (num, cap) in enumerate(FIGURES):
        x = M + i * cw
        d.rectangle([x, y + 2, x + 3, y + 30], fill=RED)
        d.text((x + 8, y), num, font=F(SANSB, 17), fill=INK)
        lines = wrap(d, cap, F(SANS, 9), cw - 12)
        text_block(d, x + 8, y + 20, lines[:2], F(SANS, 9), fill=(70, 68, 62), leading=11)
        if i < 7:
            d.line([x + cw - 2, y + 2, x + cw - 2, y + 38], fill=(200, 194, 178))
    rule(d, M, 152, W - 2 * M, 1)


# ---------------------------------------------------------------- region bar
REGIONS = [
    ("EUROPE 8", (44, 82, 130)), ("ASIA 8", (178, 34, 28)),
    ("AFRICA 7", (46, 110, 58)), ("AMERICAS 6", (120, 72, 150)),
    ("MIDDLE EAST 5", (18, 110, 105)), ("OCEANIA 4", (176, 128, 28)),
    ("GLOBAL 6", (90, 88, 84)),
]


def draw_region_bar(d):
    y = 158
    total = sum(int(r.split()[-1]) for r, _ in REGIONS)
    x = M
    for label, col in REGIONS:
        n = int(label.split()[-1])
        w = (W - 2 * M) * n // total
        d.rectangle([x, y, x + w - 1, y + 18], fill=col)
        d.text((x + 6, y + 3), label, font=F(SANSB, 10), fill=(255, 255, 255))
        x += w


# ---------------------------------------------------------------- timeline
TIMELINE = [
    ("02:00", "Akvan landfall"), ("05:30", "Poland missile"),
    ("06:30", "Tokyo closes \u22125.1%"), ("15:00", "COP31 overtime"),
    ("19:10", "Nvidia probe"), ("21:00", "S&P \u22123.7%"),
]


def draw_timeline(d):
    y = 182
    d.text((M, y), "THE DAY IN UTC", font=F(SANSB, 10), fill=RED)
    x0 = M + 96
    x1 = W - M
    d.line([x0, y + 11, x1, y + 11], fill=GREY)
    for i, (t, ev) in enumerate(TIMELINE):
        x = x0 + (x1 - x0) * i // 5
        d.ellipse([x - 3, y + 8, x + 3, y + 14], fill=INK)
        label = "%s  %s" % (t, ev)
        tw = d.textlength(label, font=F(SANS, 9))
        lx = min(max(x - tw / 2, x0), x1 - tw)
        d.text((lx, y + 18), label, font=F(SANS, 9), fill=(60, 58, 52))

# ---------------------------------------------------------------- illustrations
def panel_kyiv(d, x, y, w, h):
    """Night Kyiv: dark sky, bridge over the Dnipro, explosions, missile trails."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    for sx, sy in [(20, 14), (70, 8), (140, 18), (210, 10), (280, 16), (310, 8), (110, 26), (250, 26)]:
        d.ellipse([x + sx, y + sy, x + sx + 2, y + sy + 2], fill=(255, 255, 255))
    # skyline (kept inside the panel: base at h-40, heights <= 28)
    for bx, bw, bh in [(0, 46, 20), (52, 30, 26), (88, 40, 18), (134, 26, 24),
                       (166, 52, 20), (224, 34, 28), (264, 44, 22)]:
        d.rectangle([x + bx, y + h - 40 - bh, x + bx + bw, y + h - 40], fill=(16, 26, 52))
        for wy in range(y + h - 40 - bh + 6, y + h - 46, 10):
            d.rectangle([x + bx + 6, wy, x + bx + 10, wy + 4], fill=(255, 214, 110))
    # river
    d.rectangle([x, y + h - 40, x + w, y + h], fill=(30, 58, 96))
    # bridge
    d.rectangle([x, y + h - 52, x + w, y + h - 48], fill=(10, 14, 26))
    for ax in (40, 130, 220):
        d.arc([x + ax, y + h - 66, x + ax + 70, y + h - 44], 180, 360, fill=(10, 14, 26), width=4)
    # explosions on the bridge
    for ex, ey, r in [(80, y + h - 58, 10), (185, y + h - 60, 12), (275, y + h - 56, 8)]:
        d.ellipse([ex - r, ey - r, ex + r, ey + r], fill=(255, 170, 40))
        d.ellipse([ex - r // 2, ey - r // 2, ex + r // 2, ey + r // 2], fill=(255, 230, 120))
    # missile trails (dashed arcs)
    for i in range(6):
        px = x + 30 + i * 52
        py = y + 44 - i * 5
        d.line([px, py, px + 26, py - 14], fill=(255, 220, 130), width=2)
    d.rectangle([x, y + h - 22, x + 118, y + h - 4], fill=RED)
    d.text((x + 6, y + h - 20), "3 BRIDGES HIT", font=F(SANSB, 11), fill=(255, 255, 255))


def panel_akvan(d, x, y, w, h):
    """Bay of Bengal: coast, cyclone spiral, rain."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 228, 238))
    # land (India east coast, stylised)
    d.polygon([(x, y), (x + 150, y), (x + 132, y + 34), (x + 118, y + 66),
               (x + 96, y + h), (x, y + h)], fill=(214, 196, 150))
    d.polygon([(x + 150, y), (x + w, y), (x + w, y + h), (x + 96, y + h),
               (x + 118, y + 66), (x + 132, y + 34)], fill=(64, 130, 178))
    d.text((x + 14, y + 8), "ODISHA", font=F(SANSB, 11), fill=(90, 60, 20))
    d.text((x + 14, y + 22), "INDIA", font=F(SANSB, 11), fill=(90, 60, 20))
    # cyclone spiral
    cx, cy = x + 205, y + 62
    for r in (52, 42, 32, 22, 12):
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=(255, 255, 255), width=4)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=RED)
    # landfall arrow + label
    d.line([cx - 52, cy - 18, x + 128, y + 44], fill=RED, width=2)
    d.polygon([(x + 128, y + 44), (x + 140, y + 40), (x + 140, y + 50)], fill=RED)
    d.rectangle([x + w - 128, y + 6, x + w - 6, y + 24], fill=(255, 255, 255))
    d.text((x + w - 122, y + 9), "LANDFALL \u00b7 8 AM", font=F(SANSB, 10), fill=RED)
    # rain streaks
    for rx in range(x + 8, x + 120, 16):
        d.line([rx, y + h - 22, rx - 5, y + h - 10], fill=(90, 130, 170), width=2)
    d.text((x + 14, y + 38), "GOPALPUR", font=F(SANSB, 10), fill=(90, 60, 20))


def panel_markets(d, x, y, w, h):
    """Dark markets panel: falling chart, red arrow, index board."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 22, 30))
    d.text((x + 10, y + 6), "WORLD STOCKS: WORST WEEK SINCE 2020", font=F(SANSB, 9), fill=(255, 210, 90))
    pts = [(x + 12, y + 28), (x + 48, y + 34), (x + 84, y + 31), (x + 118, y + 44),
           (x + 150, y + 42), (x + 178, y + 56)]
    d.line(pts, fill=(230, 60, 50), width=4)
    d.polygon([(pts[-1][0], pts[-1][1]), (pts[-1][0] - 13, pts[-1][1] - 2),
               (pts[-1][0] - 3, pts[-1][1] + 11)], fill=(230, 60, 50))
    rows = [("TAIPEI", "\u22126.2%"), ("SEOUL", "\u22125.2%"), ("TOKYO", "\u22125.1%"), ("HONG KONG", "\u22121.9%")]
    ry = y + 24
    for name, val in rows:
        d.text((x + w - 116, ry), name, font=F(SANSB, 9), fill=(255, 255, 255))
        d.text((x + w - 48, ry), val, font=F(SANSB, 9), fill=(255, 90, 80))
        ry += 11


def tile_ukeu(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(30, 60, 110))
    # Union Jack (stylised)
    d.rectangle([x + 8, y + 8, x + 82, y + h - 8], fill=(200, 40, 50))
    d.line([x + 8, y + 8, x + 82, y + h - 8], fill=(255, 255, 255), width=5)
    d.line([x + 82, y + 8, x + 8, y + h - 8], fill=(255, 255, 255), width=5)
    d.rectangle([x + 40, y + 8, x + 50, y + h - 8], fill=(255, 255, 255))
    d.rectangle([x + 8, y + h // 2 - 5, x + 82, y + h // 2 + 5], fill=(255, 255, 255))
    # EU flag
    d.rectangle([x + 96, y + 8, x + w - 8, y + h - 8], fill=(20, 50, 130))
    for k in range(12):
        import math
        a = math.pi * 2 * k / 12 - math.pi / 2
        sx = x + 96 + (w - 104) // 2 + int(20 * math.cos(a))
        sy = y + h // 2 + int(14 * math.sin(a))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 220, 60))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "AGREED \u00b7 REUTERS", font=F(SANSB, 9), fill=RED)


def tile_cop(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(190, 220, 225))
    d.ellipse([x + 12, y + 8, x + 78, y + h - 8], fill=(60, 130, 170))
    d.ellipse([x + 30, y + 16, x + 52, y + 30], fill=(90, 170, 90))
    d.ellipse([x + 48, y + 34, x + 66, y + 48], fill=(90, 170, 90))
    d.ellipse([x + 92, y + 10, x + 124, y + 42], fill=(255, 255, 255), outline=INK, width=2)
    d.line([x + 108, y + 26, x + 108, y + 16], fill=INK, width=2)
    d.line([x + 108, y + 26, x + 117, y + 30], fill=INK, width=2)
    d.text((x + 132, y + 8), "OVERTIME", font=F(SANSB, 10), fill=RED)
    d.text((x + 132, y + 20), "NO DEAL", font=F(SANSB, 10), fill=INK)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "ONGOING \u00b7 UN NEWS", font=F(SANSB, 9), fill=RED)


def tile_poland(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(150, 190, 140))
    d.polygon([(x, y + h), (x, y + 30), (x + 60, y + 18), (x + 110, y + 34),
               (x + w, y + 22), (x + w, y + h)], fill=(90, 150, 80))
    d.ellipse([x + 118, y + 26, x + 158, y + 66], fill=(255, 240, 120))
    # missile
    d.polygon([(x + 60, y + 16), (x + 96, y + 10), (x + 100, y + 18), (x + 64, y + 24)], fill=(60, 60, 64))
    for i in range(4):
        d.ellipse([x + 44 - i * 10, y + 20 - i * 2, x + 48 - i * 10, y + 24 - i * 2], fill=(255, 255, 255))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "MINISTER SAYS \u00b7 REUTERS", font=F(SANSB, 9), fill=RED)


def tile_iraq(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(222, 196, 140))
    d.ellipse([x + 130, y + 8, x + 168, y + 46], fill=(255, 220, 130))
    d.polygon([(x, y + h), (x + 40, y + 34), (x + 90, y + 44), (x + 140, y + 30),
               (x + w, y + 40), (x + w, y + h)], fill=(190, 160, 100))
    for tx in (30, 96):
        d.rectangle([x + tx, y + h - 34, x + tx + 46, y + h - 22], fill=(70, 76, 60))
        d.rectangle([x + tx + 14, y + h - 44, x + tx + 30, y + h - 34], fill=(70, 76, 60))
        d.line([x + tx + 30, y + h - 40, x + tx + 52, y + h - 44], fill=(70, 76, 60), width=3)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "WITNESSED \u00b7 REUTERS", font=F(SANSB, 9), fill=RED)


def tile_italy(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 60, 60))
    d.rectangle([x + 20, y + 8, x + w - 20, y + 26], fill=(255, 255, 255))
    d.text((x + 30, y + 11), "SCIOPERO", font=F(SANSB, 11), fill=RED)
    for i, px in enumerate(range(14, w - 10, 22)):
        d.ellipse([x + px, y + 34, x + px + 10, y + 44], fill=(40, 30, 30))
        d.polygon([(x + px - 2, y + h - 18), (x + px + 12, y + h - 18),
                   (x + px + 8, y + 44), (x + px + 2, y + 44)], fill=(40, 30, 30))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "REPORTED \u00b7 REUTERS", font=F(SANSB, 9), fill=RED)


def tile_japan(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(245, 240, 225))
    d.ellipse([x + 14, y + 8, x + 56, y + 50], fill=(200, 40, 50))
    for i, bh in enumerate((14, 22, 30, 40)):
        bx = x + 76 + i * 26
        d.rectangle([bx, y + h - 18 - bh, bx + 18, y + h - 18], fill=(44, 82, 130))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "OFFICIAL DATA \u00b7 REUTERS", font=F(SANSB, 9), fill=RED)


def tile_seoul(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 214, 228))
    d.rectangle([x + 30, y + 10, x + w - 30, y + 20], fill=(90, 100, 115))
    d.polygon([(x + 24, y + 10), (x + w - 24, y + 10), (x + w // 2, y - 2)], fill=(70, 80, 95))
    for cx in range(44, w - 40, 24):
        d.rectangle([x + cx, y + 22, x + cx + 8, y + h - 18], fill=(230, 232, 236))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "PARTY DECISION \u00b7 KOREA HERALD", font=F(SANSB, 9), fill=RED)


def tile_kenya(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(250, 214, 140))
    d.ellipse([x + w - 52, y + 6, x + w - 14, y + 44], fill=(255, 170, 50))
    d.polygon([(x + 60, y + 12), (x + 100, y + 12), (x + 116, y + h - 18),
               (x + 44, y + h - 18)], fill=(60, 56, 50))
    for by in range(20, h - 24, 12):
        d.line([x + 62, y + by, x + 98, y + by], fill=(250, 214, 140), width=2)
    d.polygon([(x + 116, y + h - 18), (x + 150, y + h - 18), (x + 150, y + h - 30),
               (x + 116, y + h - 30)], fill=(40, 40, 44))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "CEREMONY HELD \u00b7 allAfrica", font=F(SANSB, 9), fill=RED)


def tile_bukele(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(200, 220, 240))
    d.rectangle([x + 40, y + 18, x + 118, y + h - 18], fill=(255, 255, 255), outline=INK, width=2)
    d.rectangle([x + 34, y + 10, x + 124, y + 20], fill=(44, 82, 130))
    d.line([x + 56, y + 46, x + 68, y + 58], fill=GREEN, width=4)
    d.line([x + 68, y + 58, x + 94, y + 30], fill=GREEN, width=4)
    d.text((x + 130, y + 24), "3RD", font=F(SANSB, 14), fill=RED)
    d.text((x + 130, y + 40), "TERM", font=F(SANSB, 14), fill=INK)
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "FILED \u00b7 AP", font=F(SANSB, 9), fill=RED)


def tile_cricket(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(90, 160, 80))
    d.rectangle([x + 20, y + 34, x + w - 20, y + h - 18], fill=(140, 200, 110))
    d.rectangle([x + 40, y + 14, x + 52, y + 48], fill=(210, 170, 110))
    d.ellipse([x + 108, y + 12, x + 136, y + 40], fill=(200, 40, 40))
    d.text((x + 142, y + 40), "118", font=F(SANSB, 14), fill=(255, 255, 255))
    d.rectangle([x, y + h - 18, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 6, y + h - 16), "SCORECARD \u00b7 ICC", font=F(SANSB, 9), fill=RED)

# ---------------------------------------------------------------- story data
# (num, place, topic, headline, deck, source, draw_fn)
LEADS = [
    (1, "KYIV, UKRAINE \u00b7 WAR \u2014 Kyiv Independent, BBC",
     "Russian missiles hit three Kyiv bridges",
     "About 110 missiles and 400 drones killed at least eight across Ukraine "
     "and cut power and water in Kyiv.",
     "Kyiv Independent, BBC", panel_kyiv),
    (2, "ODISHA, INDIA \u00b7 CYCLONE \u2014 IMD, Deccan Herald",
     "Akvan comes ashore in eastern India",
     "The storm crossed the coast near Gopalpur from about 8 am after 300,000+ "
     "people moved to shelters. No deaths.",
     "IMD, Deccan Herald", panel_akvan),
    (3, "TAIPEI \u00b7 SEOUL \u00b7 TOKYO \u2014 Al Jazeera, Anadolu",
     "AI sell-off sinks Asia\u2019s stock markets",
     "Taiwan\u2019s index fell 6.2% to end its worst week since 1991. Seoul lost "
     "5.2% and Tokyo 5.1% as chips led the slide.",
     "Al Jazeera, Anadolu", panel_markets),
]

TILES = [
    (4, "BRUSSELS \u00b7 DIPLOMACY", "UK and EU seal a \u201creset\u201d deal",
     "Food trade, youth visas, carbon link.", "Reuters", tile_ukeu),
    (5, "ANTALYA \u00b7 CLIMATE", "COP31 reaches its last day with no deal",
     "The draft text leaves out fossil fuels.", "UN News", tile_cop),
    (6, "EASTERN POLAND \u00b7 SECURITY", "Russian cruise missile lands in Poland",
     "It fell in a field; two airports paused.", "Reuters", tile_poland),
    (7, "CENTRAL IRAQ \u00b7 SECURITY", "Iraqi army enters a militia stronghold",
     "Troops deploy to Jurf al-Sakhar.", "Reuters", tile_iraq),
    (8, "ITALY \u00b7 LABOUR", "General strike over Italy\u2019s budget",
     "Workers and students march.", "Reuters", tile_italy),
    (9, "TOKYO \u00b7 ECONOMY", "Japan\u2019s inflation picks up to 2.3%",
     "A December rate rise stays in view.", "Reuters", tile_japan),
    (10, "SEOUL \u00b7 POLITICS", "Korea\u2019s ruling party to impeach top judge",
     "It follows an overturned conviction.", "Korea Herald", tile_seoul),
    (11, "TURKANA, KENYA \u00b7 ENERGY", "Kenya starts drilling its first oil well",
     "First crude is due on 1 December.", "allAfrica", tile_kenya),
    (12, "SAN SALVADOR \u00b7 POLITICS", "Bukele files to run for a third term",
     "The vote is on 28 February 2027.", "AP", tile_bukele),
    (13, "WELLINGTON \u00b7 CRICKET", "Phillips hits 118 against India",
     "Hundreds v India in all three formats.", "ICC", tile_cricket),
]

# (num, place, one-line brief, source)
ALSO = [
    (14, "Lviv", "A strike on a railway station kills two", "BBC"),
    (15, "Moscow", "Russia declares Estonia border closure", "Reuters"),
    (16, "Berlin", "Pupils strike over military service", "Al Jazeera"),
    (17, "London", "General: UK runs cyber attacks abroad", "Sky News"),
    (18, "Beijing", "China holds loan rates for an 18th month", "Xinhua"),
    (19, "Tokyo", "SoftBank shares fall over 14% in a day", "Al Jazeera"),
    (20, "Seoul", "Kospi index ends the week 7.9% lower", "Anadolu"),
    (21, "Ganjam", "209 mm of rain falls as Akvan crosses Odisha", "PTI"),
    (22, "Lebanon", "Israeli air strikes hit south and east", "Anadolu"),
    (23, "Yemen", "Gunmen fire on a cargo ship off the coast", "UKMTO"),
    (24, "Abuja", "Court bars new evidence against Tinubu", "Channels"),
    (25, "Kampala", "Police to enforce Ebola ban on rallies", "allAfrica"),
    (26, "Malawi", "Fuel crisis brings night-long queues", "Al Jazeera"),
    (27, "Africa", "AfDB: 22 countries near debt distress", "allAfrica"),
    (28, "New York", "Nasdaq futures fall 1.6% before the bell", "24/7"),
    (29, "Washington", "Democrats query free law-firm work", "Al Jazeera"),
    (30, "Wellington", "Nicholls makes 175 in a stand of 216", "ICC"),
    (31, "Sydney", "Australian shares fall 1.8% in the sell-off", "Reuters"),
    (32, "Antalya", "Panama asks COP31 to cap world oil output", "Anadolu"),
    (33, "Turin", "ATP backs a plan to lift player pay past $350m", "Anadolu"),
    (34, "Hodeidah", "Saudi-led coalition strikes Yemen\u2019s port", "Reuters"),
    (35, "Hormuz", "Tanker burns after a strike off Hormuz", "UKMTO"),
    (36, "DR Congo", "Ebola has killed 844 under-5s, WHO says", "Reuters"),
    (37, "S. Africa", "Mlambo-Ngcuka dies at 71", "SA govt"),
    (38, "Brazil", "Storm unroofs 5,107 homes in Rio Grande do Sul", "G1"),
    (39, "Haiti", "Two Salvadoran soldiers killed in Haiti blast", "AP"),
    (40, "Sydney", "Man, 35, charged over alleged bomb research", "AFP"),
    (41, "Orbit", "Cargo Dragon leaves the space station", "NASA"),
    (42, "New Delhi", "Pakistani minister visits, first since May 2025 clash", "PTI, Dawn"),
    (43, "Argentina", "Country risk jumps to 1,070", "JPM"),
    (44, "Health", "Pancreatic cancer pill: 60.7% respond", "Trial data"),
]

# map pins: (story num, lon, lat)
PINS = [(1, 30.5, 50.4), (2, 84.9, 19.3), (4, 4.4, 50.8), (5, 30.7, 36.9),
        (6, 22.0, 50.5), (7, 44.0, 32.9), (8, 12.5, 41.9), (9, 139.7, 35.7),
        (10, 127.0, 37.5), (11, 36.0, 3.5), (12, -89.2, 13.7), (13, 174.8, -41.3),
        (14, 24.0, 49.8), (15, 37.6, 55.8), (22, 35.5, 33.9), (24, 7.5, 9.1),
        (34, 42.8, 14.8), (36, 29.0, 0.5), (38, -52.0, -30.0), (42, 77.2, 28.6)]

# simplified continents (equirectangular lon/lat boxes -> polygons)
LAND = [
    # North America
    [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
     (-80, 62), (-75, 58), (-70, 45), (-75, 38), (-80, 32), (-85, 29),
     (-90, 21), (-95, 19), (-105, 20), (-115, 28), (-125, 40), (-125, 49),
     (-140, 60), (-155, 58), (-165, 60)],
    # South America
    [(-78, 8), (-72, 12), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-38, -5), (-35, -9), (-40, -20), (-48, -28), (-58, -35), (-65, -41),
     (-70, -50), (-73, -54), (-70, -40), (-72, -25), (-77, -12), (-80, -3)],
    # Africa
    [(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (30, 31), (35, 28),
     (43, 12), (51, 11), (48, 2), (40, -5), (35, -18), (32, -29), (26, -34),
     (19, -35), (15, -27), (12, -18), (9, -1), (-8, 5)],
    # Europe
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (12, 55),
     (18, 56), (21, 55), (24, 59), (28, 60), (30, 70), (40, 68), (45, 66),
     (40, 58), (35, 55), (30, 50), (28, 45), (23, 40), (19, 42), (12, 44),
     (7, 44), (3, 42), (-2, 37)],
    # Asia
    [(45, 68), (60, 69), (75, 72), (90, 75), (105, 77), (120, 73), (140, 72),
     (160, 70), (170, 66), (162, 60), (158, 52), (142, 50), (140, 40),
     (130, 35), (127, 40), (122, 31), (120, 23), (110, 20), (105, 9),
     (100, 7), (97, 15), (92, 21), (88, 22), (85, 19), (80, 13), (77, 8),
     (73, 20), (67, 25), (60, 25), (52, 28), (48, 30), (44, 39), (40, 42)],
    # Australia
    [(114, -22), (114, -32), (124, -33), (130, -32), (136, -35), (140, -38),
     (147, -39), (150, -37), (153, -27), (146, -19), (142, -11), (136, -12),
     (130, -13), (124, -15)],
]


def lonlat_to_xy(lon, lat, x, y, w, h):
    px = x + (lon + 180.0) / 360.0 * w
    py = y + (90.0 - lat) / 180.0 * h
    return px, py


def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(206, 224, 232))
    for poly in LAND:
        pts = [lonlat_to_xy(lon, lat, x, y, w, h) for lon, lat in poly]
        d.polygon(pts, fill=(226, 208, 170), outline=(180, 160, 130))
    for num, lon, lat in PINS:
        px, py = lonlat_to_xy(lon, lat, x, y, w, h)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255))
        label = str(num)
        tw = d.textlength(label, font=F(SANSB, 8))
        d.text((px - tw / 2, py - 5), label, font=F(SANSB, 8), fill=(255, 255, 255))
    d.text((x + 4, y + h - 13), "Each number is that story on this page.",
           font=F(SANS, 8), fill=(70, 68, 62))


# ---------------------------------------------------------------- page build
def build():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_figures(d)
    draw_region_bar(d)
    draw_timeline(d)

    # ---- 3 lead panels
    ly = 212
    pw = (W - 2 * M - 16) // 3
    for i, (num, place, head, deck, src, fn) in enumerate(LEADS):
        x = M + i * (pw + 8)
        fn(d, x, ly, pw, 66)
        rule(d, x, ly + 70, pw, 2, RED)
        d.text((x, ly + 74), "%d  %s" % (num, place), font=F(SANSB, 9), fill=RED)
        d.text((x, ly + 88), head, font=F(SERIFB, 14), fill=INK)
        dlines = wrap(d, deck, F(SANS, 10), pw)
        text_block(d, x, ly + 106, dlines[:2],
                   F(SANS, 10), fill=(60, 58, 52), leading=12)

    # ---- 10 feature tiles, 2 rows x 5
    ty = 348
    tw = (W - 2 * M - 32) // 5
    th = 106
    for i, (num, place, head, deck, src, fn) in enumerate(TILES):
        row, col = divmod(i, 5)
        x = M + col * (tw + 8)
        y = ty + row * (th + 8)
        fn(d, x, y, tw, 52)
        d.text((x, y + 56), "%d  %s" % (num, place), font=F(SANSB, 8), fill=RED)
        lines = wrap(d, head, F(SERIFB, 11), tw)
        text_block(d, x, y + 68, lines[:2], F(SERIFB, 11), leading=13)
        dlines = wrap(d, deck, F(SANS, 9), tw)
        text_block(d, x, y + 68 + 13 * len(lines[:2]), dlines[:1],
                   F(SANS, 9), fill=(60, 58, 52), leading=11)

    # ---- map + also list
    my = 584
    rule(d, M, my, W - 2 * M, 2)
    d.text((M, my + 6), "WHERE IT HAPPENED", font=F(SANSB, 11), fill=RED)
    d.text((M + 352, my + 6), "ALSO ON FRIDAY 20 NOVEMBER \u2014 31 MORE STORIES",
           font=F(SANSB, 11), fill=RED)
    draw_map(d, M, my + 24, 336, 300)
    # also list in 2 columns
    ax = M + 352
    colw = (W - M - ax - 8) // 2
    per_col = 16
    for i, (num, place, brief, src) in enumerate(ALSO):
        col, row = divmod(i, per_col)
        x = ax + col * (colw + 8)
        y = my + 26 + row * 19
        d.text((x, y), str(num), font=F(SANSB, 9), fill=RED)
        line = "%s: %s (%s)" % (place, brief, src)
        lines = wrap(d, line, F(SANS, 9), colw - 20)
        text_block(d, x + 18, y, lines[:1], F(SANS, 9), leading=11)

    # ---- date check footer
    fy = 928
    d.rectangle([M, fy, W - M, fy + 56], outline=RED, width=2)
    d.rectangle([M + 8, fy + 5, M + 8 + d.textlength("DATE CHECK", font=F(SANSB, 10)) + 10,
                 fy + 20], fill=RED)
    d.text((M + 10, fy + 6), "DATE CHECK", font=F(SANSB, 10), fill=(255, 255, 255))
    note = ("Left out, first reported before Friday: ICJ ruling on Myanmar (19 Nov); "
            "Trump\u2013Xi\u2013Putin summit, Shenzhen (19 Nov); Senate Iran war-powers vote "
            "(19 Nov); Kerch Bridge strikes (17\u201319 Nov); Anthropic\u2019s $83bn IPO debut "
            "(19 Nov). Not yet: BepiColombo\u2019s Mercury orbit capture; COP31\u2019s final text "
            "(21 Nov); ATP Finals final (22 Nov).")
    lines = wrap(d, note, F(SANS, 10), W - 2 * M - 16)
    text_block(d, M + 8, fy + 24, lines[:2], F(SANS, 10), fill=(60, 58, 52), leading=12)

    d.text((M, 992), "Every story here happened, or was first reported, on Friday 20 November 2026. "
                      "Officials\u2019 counts are attributed.",
           font=F(SANS, 9), fill=GREY)
    r = "Sources named beside each story \u00b7 original drawings"
    d.text((W - M - d.textlength(r, font=F(SANS, 9)), 992), r,
           font=F(SANS, 9), fill=GREY)
    return img


def main():
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
    img = build()
    img.save(out, format="PNG")
    print("wrote", out, img.size)


if __name__ == "__main__":
    main()
