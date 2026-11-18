#!/usr/bin/env python3
"""Draw the 17 November 2026 world-news poster (1024x1024 PNG).

One day's news, in one image. Every fact below was verified against real
reporting on 17-18 November 2026 (Reuters, AP, Bloomberg, CDC, PAHO, AFP,
Montsame, CSK, Le Monde). No event, figure or quote is invented.

Layout: newspaper front page. Masthead + date, one lead story with a drawn
illustration of the Kerch Bridge, six more stories in a 3x2 grid, an "ALSO"
strip, and a sources footer. Run: python3 draw_poster.py -> entry.png
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (251, 248, 241)
INK = (26, 26, 26)
NAVY = (22, 40, 63)
RED = (180, 35, 24)
GOLD = (245, 185, 66)
MUTED = (91, 100, 112)
CARD = (255, 255, 255)
BORDER = (217, 210, 194)
STRIP = (239, 234, 217)
FOOT = (107, 114, 128)

BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
REG = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap, returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_text_block(draw, x, y, lines, fnt, fill, leading):
    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def starburst(draw, cx, cy, outer, inner, points, fill, outline):
    pts = []
    for i in range(points * 2):
        r = outer if i % 2 == 0 else inner
        a = math.pi * i / points - math.pi / 2
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    draw.polygon(pts, fill=fill, outline=outline, width=2)


# ---------------------------------------------------------------- stories
LEAD = {
    "kicker": "LEAD STORY  \u2022  WAR IN UKRAINE",
    "headline": "UKRAINE HITS THE KERCH BRIDGE",
    "body": (
        "Overnight missiles and drones struck the 19 km road-and-rail link to "
        "Crimea. A road span collapsed, halting road traffic; the rail line "
        "resumed by the afternoon. Kyiv called it stage seven of a weeks-long "
        "campaign. Two killed, Crimea's Russian-installed governor said."
    ),
}

STORIES = [
    {
        "tag": "DIPLOMACY",
        "color": (30, 58, 95),
        "headline": "TRUMP IN MANILA AS QUAD MEETS AGAIN",
        "body": (
            "First in-person Quad leaders' meeting in two years, on the "
            "sidelines of the ASEAN summit. Trump heads next to APEC in "
            "Shenzhen."
        ),
    },
    {
        "tag": "GULF",
        "color": (139, 26, 26),
        "headline": "US AND IRAN TRADE STRIKES",
        "body": (
            "IRGC drones aimed at a US radar in Bahrain were intercepted, "
            "officials said. US jets then hit a missile site on Qeshm Island."
        ),
    },
    {
        "tag": "MARKETS",
        "color": (22, 101, 52),
        "headline": "NVIDIA'S $115.8BN QUARTER",
        "body": (
            "Revenue +103% to $115.8bn; data-centre sales $107.6bn. First "
            "report since founder-CEO Jensen Huang stepped down."
        ),
    },
    {
        "tag": "HEALTH",
        "color": (15, 118, 110),
        "headline": "US LOSES MEASLES-FREE STATUS",
        "body": (
            "PAHO: the US, Mexico and Bolivia lost elimination status. US "
            "cases hit 5,412 in 2026, against 2,289 in all of 2025."
        ),
    },
    {
        "tag": "ASIA",
        "color": (146, 64, 14),
        "headline": "MONGOLIA'S PRESIDENT TO QUIT",
        "body": (
            "Khurelsukh will resign over a $25m bribe claim tied to a coal "
            "railway. He denies it; parliament must approve."
        ),
    },
    {
        "tag": "DISASTER",
        "color": (71, 85, 105),
        "headline": "AN-12 CRASH KILLS 19 IN SIBERIA",
        "body": (
            "A Russian military transport plane crashed in Kemerovo region, "
            "Russia says; a technical fault is the suspected cause."
        ),
    },
]

ALSO = (
    "ALSO:  Dhoni retires from the IPL \u2014 278 matches, 5 titles \u2014 now "
    "CSK mentor  \u2022  146,000 march in France's pay protests"
)
FOOTER = (
    "Sources: Reuters \u00b7 AP \u00b7 Bloomberg \u00b7 CDC \u00b7 PAHO \u00b7 AFP "
    "\u00b7 Montsame \u00b7 CSK  \u2014  All events reported on 17 November 2026"
)


# ---------------------------------------------------------------- drawing
def draw_bridge(draw, x0, y0, x1, y1):
    """Flat stylised Kerch Bridge: sky, sea, deck, towers, arch, blast."""
    sky = (220, 233, 245)
    sea = (168, 196, 222)
    steel = (51, 65, 85)
    draw.rectangle([x0, y0, x1, y1], fill=sky)
    draw.rectangle([x0, y0 + 200, x1, y1], fill=sea)
    # sea ripples
    for i, yy in enumerate((y0 + 216, y0 + 240, y0 + 264)):
        pts = []
        for xx in range(x0 + 8, x1 - 8, 12):
            pts.append((xx, yy + (4 if (xx // 12 + i) % 2 else -4)))
        draw.line(pts, fill=(127, 168, 201), width=2)
    # arch over the deck
    draw.arc([x0 + 16, y0 + 50, x1 - 16, y0 + 280], 180, 360,
             fill=steel, width=5)
    # towers
    for tx in (x0 + 60, x1 - 70):
        draw.rectangle([tx, y0 + 75, tx + 10, y0 + 160], fill=steel)
    # cables from tower tops to the deck
    for tx in (x0 + 65, x1 - 65):
        for dx in range(-50, 51, 25):
            draw.line([(tx, y0 + 78), (tx + dx, y0 + 160)],
                      fill=(100, 116, 139), width=2)
    # deck
    deck_y = y0 + 160
    draw.rectangle([x0 + 16, deck_y, x1 - 16, deck_y + 8], fill=(31, 41, 55))
    # blast on the arch, centre
    cx, cy = (x0 + x1) // 2, y0 + 112
    starburst(draw, cx, cy, 44, 18, 12, (245, 158, 11), (234, 88, 12))
    starburst(draw, cx, cy, 22, 9, 8, (254, 240, 138), (234, 88, 12))
    # smoke
    for sx, sy, sr in ((cx - 52, cy - 34, 12), (cx - 30, cy - 48, 15),
                       (cx + 44, cy - 40, 11)):
        draw.ellipse([sx - sr, sy - sr, sx + sr, sy + sr],
                     fill=(156, 163, 175))
    # crack in the deck under the blast
    crack = [(cx - 26, deck_y + 1), (cx - 12, deck_y + 9),
             (cx + 2, deck_y + 1), (cx + 16, deck_y + 9),
             (cx + 30, deck_y + 1)]
    draw.line(crack, fill=RED, width=3)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)

    # ---- masthead ------------------------------------------------------
    draw.rectangle([0, 0, W, 100], fill=NAVY)
    draw.text((28, 24), "THE WORLD IN ONE DAY", font=font(BOLD, 38),
              fill=(255, 255, 255))
    draw.text((28, 70), "One day's news, in one image",
              font=font(REG, 16), fill=(201, 212, 227))
    draw.text((996, 20), "TUESDAY", font=font(BOLD, 19), fill=GOLD,
              anchor="ra")
    draw.text((996, 46), "17 NOVEMBER 2026", font=font(BOLD, 30),
              fill=(255, 255, 255), anchor="ra")

    # ---- lead story ----------------------------------------------------
    lx0, ly0, lx1, ly1 = 28, 116, 996, 452
    draw.rectangle([lx0, ly0, lx1, ly1], fill=CARD, outline=BORDER, width=1)
    draw.rectangle([lx0, ly0, lx1, ly0 + 6], fill=RED)
    draw.text((48, 138), LEAD["kicker"], font=font(BOLD, 17), fill=RED)
    hl = wrap(draw, LEAD["headline"], font(BOLD, 48), 620)
    y = draw_text_block(draw, 48, 166, hl, font(BOLD, 48), INK, 58)
    body = wrap(draw, LEAD["body"], font(REG, 21), 620)
    draw_text_block(draw, 48, y + 12, body, font(REG, 21), (51, 51, 51), 28)
    draw_bridge(draw, 700, 140, 976, 424)

    # ---- six more stories, 3 x 2 grid ----------------------------------
    cols = [28, 356, 684]
    rows = [468, 702]
    cell_w, cell_h = 312, 222
    for i, st in enumerate(STORIES):
        x0 = cols[i % 3]
        y0 = rows[i // 3]
        x1, y1 = x0 + cell_w, y0 + cell_h
        draw.rectangle([x0, y0, x1, y1], fill=CARD, outline=BORDER, width=1)
        draw.rectangle([x0, y0, x1, y0 + 5], fill=st["color"])
        draw.text((x0 + 14, y0 + 16), st["tag"], font=font(BOLD, 15),
                  fill=st["color"])
        hl = wrap(draw, st["headline"], font(BOLD, 23), cell_w - 28)
        y = draw_text_block(draw, x0 + 14, y0 + 42, hl, font(BOLD, 23),
                            INK, 28)
        body = wrap(draw, st["body"], font(REG, 17), cell_w - 28)
        draw_text_block(draw, x0 + 14, y + 6, body, font(REG, 17),
                        (51, 51, 51), 22)

    # ---- ALSO strip ------------------------------------------------------
    draw.rectangle([28, 936, 996, 968], fill=STRIP)
    fnt = font(BOLD, 15)
    if draw.textlength(ALSO, font=fnt) > 940:
        fnt = font(REG, 14)
        # keep "ALSO:" bold by drawing it separately below; simplest: whole
        # strip in regular 14 if it does not fit bold 15.
    draw.text((42, 947), ALSO, font=fnt, fill=INK, anchor="lm")

    # ---- footer ----------------------------------------------------------
    fw = draw.textlength(FOOTER, font=font(REG, 13))
    draw.text(((W - fw) / 2, 990), FOOTER, font=font(REG, 13), fill=FOOT)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "entry.png")
    img.save(out, optimize=True)
    size = os.path.getsize(out)
    print(f"saved {out}  {W}x{H}  {size} bytes "
          f"({size / 1024:.1f} KiB, limit 1024 KiB)")
    assert size <= 1024 * 1024, "entry.png over the 1 MiB cap"
    print("OK: 1024x1024, under 1 MiB")


if __name__ == "__main__":
    main()
