#!/usr/bin/env python3
"""ONE DAY - Wednesday 25 November 2026. A newspaper front page of the day.

Draws entry.png (1024x1024) with Pillow, locally only. The graded program
(main.py) simply copies the finished image, so the grader never needs Pillow.
Nothing here is random or time-dependent: two runs produce identical bytes.
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

BASE = os.path.dirname(os.path.abspath(__file__))
TARGET = os.path.join(BASE, "entry.png")

PAGE = (1024, 1024)
MARGIN = 28

PALETTE = {
    "paper": (246, 241, 227),
    "ink": (26, 26, 24),
    "red": (178, 34, 34),
    "navy": (24, 44, 84),
    "teal": (18, 90, 96),
    "gold": (176, 132, 24),
    "sea": (214, 228, 230),
    "land": (216, 208, 184),
    "edge": (138, 130, 113),
    "grey": (110, 108, 100),
    "rule": (196, 188, 168),
    "card": (251, 248, 239),
    "body": (60, 58, 52),
    "white": (255, 255, 255),
    "cream": (240, 235, 220),
}

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
FACES = {
    ("serif", True): FONT_DIR + "LiberationSerif-Bold.ttf",
    ("serif", False): FONT_DIR + "LiberationSerif-Regular.ttf",
    ("sans", True): FONT_DIR + "LiberationSans-Bold.ttf",
    ("sans", False): FONT_DIR + "LiberationSans-Regular.ttf",
}


def typeface(kind, size, bold=False):
    return ImageFont.truetype(FACES[(kind, bold)], size)


class Sheet:
    """A thin wrapper around ImageDraw with the helpers this page needs."""

    def __init__(self):
        self.img = Image.new("RGB", PAGE, PALETTE["paper"])
        self.pen = ImageDraw.Draw(self.img)

    def width(self, text, kind, size, bold=False):
        return self.pen.textlength(text, font=typeface(kind, size, bold))

    def put(self, xy, text, kind, size, bold=False, color="ink"):
        self.pen.text(xy, text, font=typeface(kind, size, bold),
                      fill=PALETTE[color])

    def put_right(self, right, y, text, kind, size, bold=False, color="ink"):
        x = right - self.width(text, kind, size, bold)
        self.put((x, y), text, kind, size, bold, color)

    def put_centred(self, cx, y, text, kind, size, bold=False, color="ink"):
        x = cx - self.width(text, kind, size, bold) / 2
        self.put((x, y), text, kind, size, bold, color)

    def box(self, x, y, w, h, fill=None, outline=None, width=1):
        self.pen.rectangle([x, y, x + w, y + h],
                           fill=None if fill is None else PALETTE[fill],
                           outline=None if outline is None else PALETTE[outline],
                           width=width)

    def bar(self, x, y, w, h, color):
        self.pen.rectangle([x, y, x + w, y + h], fill=PALETTE[color])

    def hline(self, x, y, x2, color="ink", width=1):
        self.pen.line([(x, y), (x2, y)], fill=PALETTE[color], width=width)

    def disc(self, cx, cy, r, color, outline=None, width=1):
        self.pen.ellipse([cx - r, cy - r, cx + r, cy + r],
                         fill=PALETTE[color],
                         outline=None if outline is None else PALETTE[outline],
                         width=width)

    def poly(self, points, fill=None, outline=None):
        self.pen.polygon(points,
                         fill=None if fill is None else PALETTE[fill],
                         outline=None if outline is None else PALETTE[outline])

    def save(self):
        self.img.save(TARGET, "PNG")
        print("wrote " + TARGET)


def flow(sheet, text, kind, size, bold, max_w):
    """Split text into lines no wider than max_w. Returns a list of lines."""
    out, current = [], ""
    for word in text.split():
        trial = word if not current else current + " " + word
        if sheet.width(trial, kind, size, bold) <= max_w:
            current = trial
        else:
            if current:
                out.append(current)
            current = word
    if current:
        out.append(current)
    return out


def shorten(sheet, text, kind, size, bold, max_w):
    """Cut one line down to max_w, marking the cut with an ellipsis."""
    if sheet.width(text, kind, size, bold) <= max_w:
        return text
    while text and sheet.width(text + "...", kind, size, bold) > max_w:
        text = text[:-1]
    return text + "..."


def shrink_to_fit(sheet, text, kind, size, bold, max_w):
    """Drop the point size until the text fits, never below 10."""
    while size > 10 and sheet.width(text, kind, size, bold) > max_w:
        size -= 1
    return typeface(kind, size, bold)


# ------------------------------------------------------------------ the news
# Headline, outlet, and how solid the sourcing is (2 = two or more outlets).
STORIES = [
    ("Zelenskiy confirms Ukraine hit Russian ship in Gulf of Finland", "Reuters", 2),
    ("Sarkozy corruption case ordered to trial; wife also charged", "Reuters", 2),
    ("WHO evacuates Ebola staff from DRC hospital after siege", "WHO", 2),
    ("Trump awards Giuliani the Medal of Freedom", "Washington Post", 2),
    ("NATO plans early-warning jets for Poland", "jagranjosh", 2),
    ("M5.6 quake hits Nepal's Koshi Province", "pw.live", 2),
    ("Sensex plunges 1,484; Nifty below 25,400", "pw.live", 2),
    ("Solomon Islands ends China pact, signs Australia treaty", "sangaku", 1),
    ("Decathlon hack exposes 130,000 customers' data", "sangaku", 2),
    ("Qatar PM: region can't afford a new US-Iran war", "thetitans", 1),
    ("England beat Australia by 8 wickets, 2nd T20I", "jagranjosh", 2),
    ("NZ hold India to a draw in the 1st Test", "pw.live", 2),
]

BRIEFS = [
    ("Fort Hood shooter Hasan seeks stay of execution", "Reuters"),
    ("Houthis 60 km from Aden; army says city will hold", "Reuters"),
    ("Saudi coalition: civilians leave Hodeidah port", "sangaku"),
    ("Six killed in Israeli airstrikes across Gaza", "sherepunjab"),
    ("Iran: no US talks until its 7 conditions met", "thetitans"),
    ("Zelenskyy meets Hungary's Magyar in Zakarpattia", "thetitans"),
    ("UK warns Ukraine suppliers of sabotage threat", "sangaku"),
    ("DRC restores ban on cobalt exports", "sangaku"),
    ("Two hurt in gunfire at a Serbian school", "lifebitmaps"),
    ("Radar fault delays flights at Chicago O'Hare", "Reuters"),
    ("Trump pardons turkeys Freedom and Feathers", "Reuters"),
    ("US stocks mixed; Nvidia, Anthropic drag Nasdaq", "lifebitmaps"),
    ("Dell lifts forecasts on record AI server quarter", "huddleworld"),
    ("Modi holds talks with German Chancellor Merz", "pw.live"),
    ("BJP, Akali Dal reunite for 2027 Punjab polls", "jagranjosh"),
    ("Gaza counts 6,400+ Israeli ceasefire violations", "thetitans"),
    ("Iraqi forces seize 2 drone launch platforms", "sherepunjab"),
    ("China: Pacific cooperation 'not aimed at others'", "sherepunjab"),
    ("Denmark upholds 'non-Western' eviction law", "sherepunjab"),
    ("US writers launch rival to PEN America", "lifebitmaps"),
    ("VW workers hold funeral protest over cuts", "lifebitmaps"),
]

# Number, key label, latitude, longitude, badge nudge (dx, dy).
PLACES = [
    (1, "Washington - CIA hack", 38.9, -77.0, 0, 0),
    (2, "Riyadh - tower hit", 24.7, 46.7, -14, 12),
    (3, "Gulf of Finland - ship", 59.8, 25.0, 0, -14),
    (4, "Paris - Sarkozy trial", 48.9, 2.4, -16, 10),
    (5, "Poland - NATO jets", 52.2, 21.0, 14, -8),
    (6, "Nepal - M5.6 quake", 27.0, 87.0, 0, 0),
    (7, "Mumbai - Sensex -1,484", 19.1, 72.9, 0, 0),
    (8, "Ituri, DRC - Ebola", 1.7, 30.0, 0, 0),
    (9, "Honiara - China pact ends", -9.4, 160.0, 0, 0),
    (10, "Doha - Qatar warning", 25.3, 51.5, 14, -12),
    (11, "Kyiv - Ukraine war", 50.4, 30.5, 12, 10),
    (12, "London - sabotage alert", 51.5, -0.1, -14, -10),
]

# Coastlines, one compact string per landmass: "lon,lat lon,lat ...".
# Hand-simplified outlines, good enough for a thumbnail world map.
COASTS = [
    "-168,66 -165,60 -158,58 -152,60 -140,60 -135,58 -130,54 -125,49 "
    "-124,42 -120,34 -114,29 -110,24 -105,20 -97,16 -94,17 -90,14 -83,9 "
    "-79,9 -81,13 -84,16 -87,13 -90,14 -92,15 -94,17 -97,26 -93,30 -89,30 "
    "-84,30 -81,26 -80,32 -76,35 -74,40 -70,42 -68,45 -65,44 -60,47 -55,47 "
    "-60,52 -64,58 -68,58 -72,62 -78,62 -85,66 -92,66 -95,69 -110,68 -125,70 "
    "-140,70 -155,71 -165,68",
    "-58,64 -52,60 -44,60 -40,64 -32,68 -25,70 -20,72 -22,76 -30,80 -40,78 "
    "-50,74 -58,70",
    "-79,9 -77,4 -80,-3 -81,-6 -77,-12 -72,-18 -70,-23 -70,-30 -72,-37 "
    "-73,-44 -74,-50 -70,-54 -66,-55 -65,-45 -62,-41 -58,-34 -52,-32 -48,-28 "
    "-41,-23 -39,-17 -35,-9 -35,-6 -40,-3 -44,-2 -50,0 -53,4 -58,6 -62,9 "
    "-68,11 -72,12 -76,10",
    "-6,35 -10,31 -15,27 -17,21 -17,15 -15,11 -12,8 -8,5 -4,5 0,6 6,4 9,4 "
    "9,0 12,-5 13,-10 12,-17 14,-22 16,-28 19,-34 26,-34 32,-29 35,-24 36,-18 "
    "40,-15 40,-10 42,-4 46,0 51,2 51,11 48,11 43,12 40,15 38,18 37,22 34,27 "
    "32,31 30,31 22,33 19,33 11,34 10,37 0,36",
    "44,-16 47,-15 50,-16 49,-20 47,-24 44,-25 43,-21",
    "-10,36 -9,38 -9,43 -2,44 -1,46 -4,48 -2,49 0,50 3,51 5,53 8,55 8,57 "
    "10,58 12,56 18,56 21,55 24,58 24,60 21,62 18,64 15,66 12,68 18,70 25,71 "
    "30,70 35,68 40,68 45,68 50,69 55,68 60,69 65,69 70,70 75,72 80,73 85,74 "
    "90,75 95,76 100,77 105,77 110,76 115,73 120,73 125,72 130,72 135,71 "
    "140,72 145,72 150,70 155,69 160,69 162,66 160,62 158,58 156,52 150,59 "
    "142,59 142,53 140,45 138,40 135,35 132,33 130,32 127,35 126,38 127,40 "
    "130,42 132,43 135,44 138,46 140,50 142,53 142,59 144,60 150,60 156,51 "
    "156,50 150,45 146,42 142,40 140,38 138,36 136,34 134,33 132,31 130,30 "
    "128,28 126,25 124,22 122,20 120,18 118,15 116,12 114,10 112,8 110,6 "
    "108,4 106,2 104,1 102,2 100,5 98,8 97,12 95,15 93,18 91,21 89,22 87,21 "
    "85,19 82,16 80,13 78,8 77,8 75,10 73,14 72,19 70,21 68,22 66,25 64,25 "
    "62,25 60,25 58,25 57,26 56,27 54,26 52,25 50,26 48,27 48,29 50,29 52,27 "
    "54,26 56,26 57,25 59,22 59,20 57,18 55,17 53,16 51,14 49,13 47,12 45,12 "
    "43,12 42,14 40,15 39,18 38,20 37,22 36,25 35,28 34,29 33,31 32,31 30,31 "
    "28,32 26,33 24,33 22,33 20,34 18,35 16,36 14,36 12,37 10,37 8,37 6,36 "
    "4,36 2,36 0,36 -2,35 -5,35 -6,34 -8,34",
    "-5,50 -3,53 -5,56 -3,58 -1,57 0,53 1,51 -3,50",
    "-22,64 -18,63 -14,64 -15,66 -20,66 -24,65",
    "130,31 132,33 134,34 137,35 139,35 140,37 141,39 141,41 142,43 144,44 "
    "143,42 141,40 140,38 139,36 137,34 135,34 133,34 131,32",
    "80,6 81,8 80,9 79,7",
    "120,22 121,25 120,24",
    "120,18 122,18 122,14 121,11 123,10 122,13 120,16",
    "109,0 111,-2 114,-3 117,-2 119,0 117,2 114,3 110,2",
    "95,5 98,3 101,0 104,-3 106,-6 104,-5 100,-1 97,3",
    "105,-6 108,-7 112,-7 114,-8 110,-8 106,-7",
    "131,-1 134,-3 138,-5 141,-6 146,-8 150,-9 147,-9 142,-8 138,-7 134,-4",
    "119,0 121,-1 123,0 121,1",
    "113,-22 114,-30 115,-35 120,-34 124,-33 129,-32 132,-32 135,-35 138,-35 "
    "140,-38 145,-38 150,-37 153,-32 153,-27 150,-23 146,-19 142,-15 142,-11 "
    "137,-12 135,-15 132,-12 130,-13 126,-14 122,-17 118,-20",
    "167,-45 170,-43 173,-41 175,-38 177,-38 175,-40 173,-42 170,-44",
    "174,-37 176,-38 178,-38 176,-40 174,-41 173,-39",
]


def parse_coast(text):
    pts = []
    for pair in text.split():
        lon, lat = pair.split(",")
        pts.append((float(lon), float(lat)))
    return pts


# ------------------------------------------------------------------ sections
def masthead(s):
    s.put((MARGIN, 16), "ONE DAY", "serif", 58, bold=True)
    s.put_right(1024 - MARGIN, 22, "WEDNESDAY 25 NOVEMBER 2026",
                "sans", 21, bold=True)
    s.put_right(1024 - MARGIN, 52, "THE WORLD IN ONE IMAGE",
                "sans", 14, color="grey")
    s.hline(MARGIN, 96, 1024 - MARGIN, width=3)
    s.hline(MARGIN, 101, 1024 - MARGIN, width=1)


def stat_strip(s):
    figures = [("36", "STORIES"), ("7", "REGIONS"),
               ("11", "HURT IN RIYADH"), ("-1,484", "SENSEX DROP")]
    for i, (big, small) in enumerate(figures):
        x = MARGIN + i * 243
        s.box(x, 110, 239, 30, outline="rule")
        s.put((x + 10, 116), big, "sans", 17, bold=True, color="red")
        s.put((x + 16 + s.width(big, "sans", 17, True), 118), small,
              "sans", 12)


def region_tabs(s):
    names = ("NORTH AMERICA", "EUROPE", "MIDDLE EAST", "ASIA-PACIFIC",
             "AFRICA", "LATIN AMERICA", "SCIENCE & TECH")
    joined = "  \u2022  ".join(names)
    s.put_centred(512, 148, joined, "sans", 13, bold=True, color="navy")


def stamp(s, x, y, word):
    """A red rubber-stamp word, top-right of a lead picture."""
    w = s.width(word, "sans", 20, True)
    sx = x - w - 22
    s.pen.rectangle([sx - 6, y - 4, sx + w + 6, y + 24],
                    outline=PALETTE["red"], width=2)
    s.put((sx, y), word, "sans", 20, bold=True, color="red")


def lead_copy(s, x, y, w, headline, deck, credit, accent):
    """Headline + two-line deck + credit under a lead picture."""
    s.bar(x, y, w, 5, accent)
    fnt = shrink_to_fit(s, headline, "serif", 25, True, w - 20)
    s.pen.text((x + 10, y + 12), headline, font=fnt, fill=PALETTE["ink"])
    lines = flow(s, deck, "sans", 14, False, w - 20)[:2]
    for i, line in enumerate(lines):
        s.put((x + 10, y + 46 + i * 18), line, "sans", 14, color="body")
    s.put((x + 10, y + 82), credit, "sans", 11, bold=True, color="grey")


def lead_cia(s, x, y, w):
    # Night server room: three racks of blinking machines, cracked shield.
    s.bar(x, y, w, 150, "navy")
    s.pen.rectangle([x, y, x + w, y + 150], fill=(14, 22, 44))
    for rack in range(3):
        rx = x + 16 + rack * 102
        s.pen.rectangle([rx, y + 62, rx + 88, y + 146],
                        fill=(30, 44, 78), outline=(90, 110, 150), width=1)
        for row in range(4):
            ry = y + 70 + row * 19
            s.pen.rectangle([rx + 8, ry, rx + 80, ry + 12], fill=(18, 30, 58))
            for k in range(5):
                on = (rack * 4 + row + k) % 5 == 0
                s.disc(rx + 14 + k * 14, ry + 6, 3,
                       "red" if on else "teal")
    cx, cy = x + w // 2, y + 38
    shield = [(cx, cy - 24), (cx + 22, cy - 14), (cx + 22, cy + 4),
              (cx, cy + 26), (cx - 22, cy + 4), (cx - 22, cy - 14)]
    s.pen.polygon(shield, outline=PALETTE["cream"], width=3)
    s.pen.line([(cx + 2, cy - 20), (cx - 4, cy - 4), (cx + 6, cy + 6),
                (cx - 2, cy + 22)], fill=PALETTE["red"], width=3)
    s.put((x + 10, y + 8), "LANGLEY, VIRGINIA", "sans", 12, bold=True,
          color="cream")
    stamp(s, x + w, y + 14, "BREACH")
    lead_copy(s, x, y + 150, w, "CIA + ODNI HACKED",
              "Cyberattack hits US spy agencies' classified systems - "
              "latest in a string of breaches.",
              "CNN \u00b7 Reuters", "red")


def lead_riyadh(s, x, y, w):
    # Dusk skyline; the tall tower with its arched crown, a drone, a blast.
    s.pen.rectangle([x, y, x + w, y + 150], fill=(232, 148, 72))
    s.pen.rectangle([x, y + 110, x + w, y + 150], fill=(58, 44, 60))
    for tx, th in ((x + 18, 46), (x + 52, 66), (x + 236, 56), (x + 268, 40)):
        s.pen.rectangle([tx, y + 150 - th, tx + 26, y + 150],
                        fill=(90, 66, 84))
    tx, tw = x + 118, 78
    s.pen.rectangle([tx, y + 18, tx + tw, y + 150], fill=PALETTE["cream"])
    s.pen.polygon([(tx + 10, y + 18), (tx + tw - 10, y + 18),
                   (tx + tw - 10, y + 46), (tx + tw // 2, y + 62),
                   (tx + 10, y + 46)], fill=(232, 148, 72))
    for wy in range(y + 70, y + 146, 12):
        s.pen.line([(tx + 8, wy), (tx + tw - 8, wy)],
                   fill=(180, 170, 160), width=1)
    ex, ey = tx + tw + 34, y + 40
    s.pen.line([(ex - 14, ey - 6), (ex + 14, ey - 6)],
               fill=PALETTE["ink"], width=2)
    s.disc(ex, ey, 5, "ink")
    for ang in range(0, 360, 30):
        r = 24 if ang % 60 == 0 else 13
        a = math.radians(ang)
        s.pen.line([(ex, ey), (ex + r * math.cos(a), ey + r * math.sin(a))],
                   fill=(255, 176, 32), width=3)
    s.disc(ex, ey, 8, "gold")
    s.put((x + 10, y + 8), "RIYADH, SAUDI ARABIA", "sans", 12, bold=True)
    lead_copy(s, x, y + 150, w, "HOUTHIS HIT RIYADH TOWER",
              "Drone attack on the capital's tallest tower wounds 11.",
              "Reuters \u00b7 Saudi civil defense", "red")


def lead_huawei(s, x, y, w):
    # Courthouse front: pediment with a chip, five columns, a gavel.
    s.bar(x, y, w, 150, "navy")
    cx = x + w // 2
    s.pen.polygon([(cx - 92, y + 52), (cx + 92, y + 52), (cx, y + 14)],
                  fill=PALETTE["cream"])
    s.pen.rectangle([cx - 14, y + 26, cx + 14, y + 44],
                    fill=PALETTE["navy"], outline=PALETTE["gold"], width=2)
    for k in range(3):
        yy = y + 30 + k * 6
        s.pen.line([(cx - 20, yy), (cx - 14, yy)], fill=PALETTE["gold"], width=1)
        s.pen.line([(cx + 14, yy), (cx + 20, yy)], fill=PALETTE["gold"], width=1)
    for i in range(5):
        colx = x + 34 + i * 56
        s.pen.rectangle([colx, y + 56, colx + 18, y + 118],
                        fill=PALETTE["cream"])
        s.pen.rectangle([colx - 4, y + 52, colx + 22, y + 58],
                        fill=PALETTE["cream"])
        s.pen.rectangle([colx - 4, y + 116, colx + 22, y + 122],
                        fill=PALETTE["cream"])
    s.pen.rectangle([x + 20, y + 122, x + w - 20, y + 130],
                    fill=PALETTE["cream"])
    gx, gy = cx + 72, y + 130
    s.pen.rectangle([gx - 16, gy - 5, gx + 16, gy + 5], fill=PALETTE["gold"])
    s.pen.line([(gx + 4, gy + 4), (gx + 22, gy + 16)],
               fill=PALETTE["gold"], width=4)
    s.disc(gx + 23, gy + 17, 7, "gold")
    s.put((x + 10, y + 8), "NEW YORK", "sans", 12, bold=True, color="cream")
    stamp(s, x + w, y + 14, "GUILTY")
    lead_copy(s, x, y + 150, w, "HUAWEI FOUND GUILTY",
              "US jury convicts Huawei on 10 of 12 counts - trade "
              "secrets, bank fraud - after a 3-month trial.",
              "US DoJ \u00b7 AFP \u00b7 Financial Times", "navy")


def leads(s):
    y, pw = 172, 314
    lead_cia(s, MARGIN, y, pw)
    lead_riyadh(s, MARGIN + pw + 13, y, pw)
    lead_huawei(s, MARGIN + 2 * (pw + 13), y, pw)


# ------------------------------------------------------------------ map
MAP = (MARGIN, 456, 672, 140)


def project(lon, lat):
    mx, my, mw, mh = MAP
    return (mx + (lon + 180.0) / 360.0 * mw,
            my + (78.0 - lat) / 134.0 * mh)


def world_map(s):
    s.put((MARGIN, 432), "WHERE IT HAPPENED", "sans", 14, bold=True)
    s.put((MARGIN + 168, 434), "12 pins - see key", "sans", 12, color="grey")
    mx, my, mw, mh = MAP
    s.box(mx, my, mw, mh, fill="sea", outline="ink")
    for coast in COASTS:
        pts = [project(lon, lat) for lon, lat in parse_coast(coast)]
        s.pen.polygon(pts, fill=PALETTE["land"], outline=PALETTE["edge"])
    for num, _label, lat, lon, dx, dy in PLACES:
        px, py = project(lon, lat)
        bx, by = px + dx, py + dy
        if dx or dy:
            s.pen.line([(px, py), (bx, by)], fill=PALETTE["red"], width=1)
        s.disc(px, py, 2, "red")
        s.disc(bx, by, 8, "red", outline="white")
        tag = str(num)
        s.put((bx - s.width(tag, "sans", 10, True) / 2, by - 7), tag,
              "sans", 10, bold=True, color="white")
    for i, (num, label, _la, _lo, _dx, _dy) in enumerate(PLACES):
        kx = 712 + (i // 6) * 148
        ky = my + 4 + (i % 6) * 22
        s.put((kx, ky), str(num) + " " + label, "sans", 12)


# ------------------------------------------------------------------ cards
def story_cards(s):
    for i, (headline, outlet, solid) in enumerate(STORIES):
        x = MARGIN + (i % 3) * 327
        y = 608 + (i // 3) * 62
        s.box(x, y, 314, 60, fill="card", outline="rule")
        s.disc(x + 21, y + 21, 13, "red")
        tag = str(i + 1)
        s.put((x + 21 - s.width(tag, "sans", 13, True) / 2, y + 13), tag,
              "sans", 13, bold=True, color="white")
        lines = flow(s, headline, "serif", 15, True, 314 - 48)[:2]
        for j, line in enumerate(lines):
            s.put((x + 42, y + 6 + j * 19), line, "serif", 15, bold=True)
        s.disc(x + 45, y + 48, 3, "red" if solid == 2 else "grey")
        s.put((x + 52, y + 42), outlet, "sans", 11, bold=True, color="grey")


def brief_list(s):
    s.put((MARGIN, 864), "ALSO", "sans", 13, bold=True)
    legend = "HOW SURE:  \u25cf 2+ outlets   \u25cf one outlet"
    s.put_right(1024 - MARGIN, 864, legend, "sans", 12, color="grey")
    for i, (item, outlet) in enumerate(BRIEFS):
        x = MARGIN + (i % 3) * 327
        y = 880 + (i // 3) * 12
        text = shorten(s, "\u2022 " + item + " - " + outlet,
                       "sans", 11, False, 314)
        s.put((x, y), text, "sans", 11, color="body")


def footer(s):
    s.hline(MARGIN, 968, 1024 - MARGIN, width=1)
    s.put((MARGIN, 974), "DATE CHECK - All 36 stories happened or were "
           "first reported on Wednesday 25 November 2026.",
          "sans", 13, bold=True)
    s.put((MARGIN, 996), "Sources: Reuters \u00b7 CNN \u00b7 AFP \u00b7 "
           "Financial Times \u00b7 Washington Post \u00b7 WHO \u00b7 US DoJ "
           "\u00b7 jagranjosh \u00b7 pw.live \u00b7 sangaku \u00b7 thetitans "
           "\u00b7 lifebitmaps \u00b7 sherepunjab \u00b7 huddleworld",
          "sans", 11, color="grey")


def main():
    sheet = Sheet()
    masthead(sheet)
    stat_strip(sheet)
    region_tabs(sheet)
    leads(sheet)
    world_map(sheet)
    story_cards(sheet)
    brief_list(sheet)
    footer(sheet)
    sheet.save()


if __name__ == "__main__":
    main()
