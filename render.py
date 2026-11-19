#!/usr/bin/env python3
"""news-image-20261118 v2 — 'The World's News in One Picture' (rebuild, target top 10).
48 verified 18 Nov 2026 stories, 7 regions, 13 flat-vector infographic panels drawn
entirely with PIL primitives (no photos). Deterministic: same bytes every run.
Layout: masthead + region bar + UTC strip + 3 heroes + 10 medium panels +
compact world map + 3-column briefs + SOURCES footer.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)
INK = (20, 20, 20)
NAVY = (20, 38, 63)
RED = (178, 34, 34)
GOLD = (201, 162, 39)
TEAL = (15, 118, 110)
GREY = (110, 110, 105)
LIGHT = (232, 227, 216)

FDIR = "/usr/share/fonts/truetype/liberation/"

def f(name, size):
    return ImageFont.truetype(FDIR + name, size)

SERIF_B = lambda s: f("LiberationSerif-Bold.ttf", s)
SERIF = lambda s: f("LiberationSerif-Regular.ttf", s)
SANS_B = lambda s: f("LiberationSans-Bold.ttf", s)
SANS = lambda s: f("LiberationSans-Regular.ttf", s)

def wrap(draw, text, font, width):
    """Wrap text to pixel width; returns list of lines."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def fit_lines(draw, text, font, width, max_lines):
    """Wrap and truncate to max_lines with ellipsis."""
    lines = wrap(draw, text, font, width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        while lines and draw.textlength(lines[-1] + " ...", font=font) > width:
            lines[-1] = lines[-1][:-1]
        lines[-1] = lines[-1].rstrip() + " ..."
    return lines

# ---------------------------------------------------------------- stories
# (n, region, source, headline, deck, art_kind, art_data)
REGIONS = ["ASIA", "OCEANIA", "EUROPE", "MIDDLE EAST", "AFRICA", "AMERICAS", "WORLD"]
REGION_COLOR = {
    "ASIA": (178, 34, 34), "EUROPE": (20, 38, 63), "MIDDLE EAST": (146, 90, 16),
    "AFRICA": (15, 118, 110), "AMERICAS": (90, 60, 140), "OCEANIA": (0, 110, 120),
    "WORLD": (70, 70, 70),
}

LEADS = [
    (1, "ASIA", "AP", "Three presidents greet in Shenzhen",
     "Trump, Xi and Putin meet at APEC's welcome reception on day one.",
     "summit"),
    (2, "MIDDLE EAST", "CLAIM", "Iran fires on US bases in the Gulf",
     "Iran claims drones hit US bases in Kuwait and Bahrain; both report interceptions, no damage.",
     "gulf"),
    (3, "EUROPE", "AP", "Russia launches 141 drones overnight",
     "Ukraine downs 126 by 08:00; six hurt in Dnipro as strikes hit seven locations.",
     "drones"),
    (4, "AMERICAS", "FED", "Fed minutes point to more hikes; Dow falls 561",
     "Almost all back further rises; some see a bigger move in December.",
     "chart"),
    (5, "WORLD", "SENSOR TOWER", "GTA VI counts down to midnight launch",
     "Take-Two up 8%; est. 17.1m units sold (Sensor Tower), Metacritic 99.",
     "gta"),
    (6, "AMERICAS", "CNN", "Jeffries wins speaker nomination 251-11",
     "Democrats renominate Jeffries; if elected in January he would be the first Black Speaker.",
     "votes"),
    (7, "EUROPE", "REUTERS", "EU proposes EUR 45bn loan for Ukraine",
     "EUR 25bn arms, EUR 20bn budget in 2027; needs all 27 to agree.",
     "money"),
    (8, "WORLD", "NASA", "Voyager 1 reaches one light-day",
     "16.1 billion miles from Earth; a one-way signal now takes a full day.",
     "voyager"),
    (9, "ASIA", "IMD", "Cyclone Akvan bears down on Andhra",
     "Landfall forecast Friday, Narsapur to Puri; winds 90-100, gusting 110.",
     "cyclone"),
    (10, "ASIA", "REUTERS", "Indonesia, China agree $71.8bn in deals",
     "Four partnerships at APEC Shenzhen, incl. 10 smart cities; $50bn Danantara-led deal.",
     "deals"),
    (11, "AMERICAS", "REUTERS", "Anthropic prices its IPO at $83",
     "Above the $70-78 range; ticker ANT on the Nasdaq.",
     "ipo"),
    (12, "ASIA", "AP", "Bangladesh garment strike spreads",
     "132 factories shut in Ashulia; hundreds arrested over Tk30,000 wage demand.",
     "strike"),
    (13, "EUROPE", "INFP", "Magnitude 5.7 quake shakes Romania",
     "Vrancea tremor felt across Ukraine and Moldova; no major damage reported.",
     "quake"),
]

# briefs: (n, region, text) — one line each, region pill shown
BRIEFS = [
    (14, "WORLD", "COP31 talks stall over fossil fuels in Antalya"),
    (15, "AFRICA", "Ethiopia and Eritrea mass troops at their border"),
    (16, "MIDDLE EAST", "Israel ground op crosses Gaza's Yellow Line"),
    (17, "EUROPE", "EU creates Sanctions Office, names Danielsson envoy"),
    (18, "ASIA", "Trump seals trade understanding with Manila"),
    (19, "EUROPE", "UK, EU drop 'trusted partnership' term"),
    (20, "MIDDLE EAST", "Saudi coalition says it hit 60 Houthi targets"),
    (21, "MIDDLE EAST", "One missing, 11 hurt after Hormuz tanker attack"),
    (22, "AMERICAS", "Outages hit Microsoft, FAA and banks; Rubio: no link found"),
    (23, "AMERICAS", "Hegseth announces US-Venezuela military ties in Caracas"),
    (24, "AMERICAS", "Waller calls for half-point Fed hike in December"),
    (25, "EUROPE", "Europe EV sales jump 60% in October"),
    (26, "EUROPE", "Ukraine refinery strikes cut Russian output 45%"),
    (27, "ASIA", "Japan exports hit record ¥11.8tn in October"),
    (28, "ASIA", "India-US trade deal nearly done, signing waits"),
    (29, "AMERICAS", "Nvidia slips 2.9% to $150.96"),
    (30, "AMERICAS", "UnitedHealth falls 10% on Medicare audit plan"),
    (31, "EUROPE", "Germany adopts first financial-literacy plan"),
    (32, "EUROPE", "Officials: sunken LPG tanker was hit by 4 projectiles"),
    (33, "EUROPE", "UK inflation hits 3.6%, highest in a year"),
    (34, "EUROPE", "EU Parliament may block €1.8tn budget over cuts"),
    (35, "EUROPE", "EU agrees to speed up grid permits"),
    (36, "OCEANIA", "Australia sanctions over West Bank settlements"),
    (37, "ASIA", "EU approves signing EU-Indonesia trade deals"),
    (38, "AFRICA", "Ethiopian Airlines hit by cyberattack"),
    (39, "AMERICAS", "Canada pitches Mexico on defence bank"),
    (40, "ASIA", "Bangladesh: 71 arrested in Hasina-return unrest"),
    (41, "EUROPE", "Istanbul mayor Imamoglu gets 2 more years and a ban"),
    (42, "EUROPE", "Spain approves 7 decree-laws, €182m flood aid"),
    (43, "AFRICA", "Uganda activist Mugumya charged with treachery"),
    (44, "AFRICA", "EU gives €550,000 for Moyale displaced"),
    (45, "AFRICA", "AfDB gives $1m for ECOWAS Data Embassy"),
    (46, "AMERICAS", "China's Jetour to build cars in Brazil"),
    (47, "ASIA", "Tendulkar posts tribute to Dhoni"),
    (48, "AFRICA", "Uganda Airlines starts daily Entebbe-Kigali flights"),
]

REGION_COUNT = {"ASIA": 10, "EUROPE": 14, "MIDDLE EAST": 4, "AFRICA": 6,
                "AMERICAS": 10, "OCEANIA": 1, "WORLD": 3}

# ---------------------------------------------------------------- vector art
def art_summit(d, x, y, w, h):
    """Three leaders at a summit table: skyline + three flag dots + table."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 214))
    # skyline
    for i, bh in enumerate([0.45, 0.7, 0.55, 0.85, 0.6, 0.75, 0.5]):
        bx = x + 8 + i * (w - 16) // 7
        bw = (w - 16) // 7 - 4
        d.rectangle([bx, y + h - 58 - bh * 40, bx + bw, y + h - 58], fill=(190, 185, 165))
    d.rectangle([x, y + h - 58, x + w, y + h - 54], fill=NAVY)
    # three flag circles: CN red, RU white-blue-red, US stars stripes
    cx = [x + w * 0.22, x + w * 0.5, x + w * 0.78]
    cols = [(222, 41, 16), (20, 60, 160), (178, 34, 34)]
    for cxx, c in zip(cx, cols):
        d.ellipse([cxx - 17, y + 12, cxx + 17, y + 46], fill=c, outline=INK, width=2)
    d.text((x + w / 2, y + h - 46), "XI  ·  PUTIN  ·  TRUMP", font=SANS_B(13),
           anchor="ma", fill=INK)
    d.text((x + w / 2, y + h - 26), "APEC · SHENZHEN", font=SANS_B(11),
           anchor="ma", fill=RED)

def art_gulf(d, x, y, w, h):
    """Mini-map of the Gulf: sea, land, Qeshm, drone dots, interceptor arcs."""
    d.rectangle([x, y, x + w, y + h], fill=(18, 52, 86))
    # land masses
    d.polygon([(x + 8, y + 8), (x + w * 0.42, y + 8), (x + w * 0.34, y + h * 0.42),
               (x + 8, y + h * 0.5)], fill=(214, 196, 150))
    d.polygon([(x + w * 0.72, y + h), (x + w, y + h), (x + w, y + h * 0.45),
               (x + w * 0.62, y + h * 0.6)], fill=(214, 196, 150))
    # Qeshm island
    d.ellipse([x + w * 0.5, y + h * 0.42, x + w * 0.66, y + h * 0.58], fill=(178, 34, 34))
    d.text((x + w * 0.58, y + h * 0.6), "QESHM", font=SANS_B(9), anchor="ma", fill=(255, 220, 200))
    # drone dots + arcs
    for i in range(5):
        dx = x + w * (0.18 + i * 0.13)
        dy = y + h * (0.62 + (i % 2) * 0.14)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=(255, 200, 60))
    d.arc([x + w * 0.1, y + h * 0.3, x + w * 0.9, y + h * 0.95], 200, 340,
          fill=(255, 200, 60), width=2)
    d.text((x + 10, y + h - 22), "KUWAIT · BAHRAIN", font=SANS_B(11), fill=(255, 255, 255))
    d.text((x + w - 10, y + 8), "4 GULF STATES", font=SANS_B(11),
           anchor="ra", fill=(255, 200, 60))

def art_drones(d, x, y, w, h):
    """141 dots, 126 downed (grey) vs 15 through (red); big 141.
    Grid is 12x12 in the left ~2/3 so all 141 dots draw: the 141
    callout sits in the clear right column, the caption below the grid."""
    d.rectangle([x, y, x + w, y + h], fill=(24, 24, 28))
    n = 0
    for r in range(12):
        for c in range(12):
            if n >= 141:
                break
            dx = x + 12 + c * 20
            dy = y + 6 + r * 7
            col = (120, 120, 120) if n < 126 else (230, 60, 50)
            d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=col)
            n += 1
    d.text((x + w - 8, y + 44), "141", font=SANS_B(28), anchor="ra", fill=(255, 255, 255))
    d.text((x + w - 8, y + h - 2), "DRONES · 126 DOWNED", font=SANS_B(10),
           anchor="rb", fill=(255, 200, 60))

def art_chart(d, x, y, w, h):
    """Falling Dow line chart with -561 callout."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.text((x + 12, y + 6), "-561", font=SANS_B(24), fill=RED)
    d.text((x + w - 10, y + 10), "DOW 50,198", font=SANS_B(11), anchor="ra", fill=INK)
    pts = []
    for i, v in enumerate([0.15, 0.22, 0.18, 0.35, 0.3, 0.5, 0.45, 0.62, 0.58, 0.78, 0.85]):
        px = x + 10 + i * (w - 20) / 10
        py = y + 36 + v * (h - 58)
        pts.append((px, py))
    d.line(pts, fill=RED, width=3)
    d.ellipse([pts[-1][0] - 4, pts[-1][1] - 4, pts[-1][0] + 4, pts[-1][1] + 4], fill=RED)
    d.text((x + 12, y + h - 12), "S&P -0.23% · 5TH DAY", font=SANS(9), fill=GREY)

def art_gta(d, x, y, w, h):
    """GTA VI launch: sun-soaked vice city strip + big 17.1M."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 183, 77))
    d.rectangle([x, y + h * 0.68, x + w, y + h], fill=(255, 120, 90))
    # palm silhouettes (right half only)
    for px in [0.62, 0.8, 0.94]:
        bx = x + w * px
        d.line([(bx, y + h * 0.68), (bx, y + h * 0.18)], fill=(40, 30, 30), width=3)
        for a in (-0.9, -0.45, 0.0, 0.45, 0.9):
            import math
            ex = bx + math.cos(a - 1.57) * 22
            ey = y + h * 0.18 + math.sin(a - 1.57) * 12
            d.line([(bx, y + h * 0.18), (ex, ey)], fill=(40, 30, 30), width=2)
    d.text((x + 12, y + 6), "17.1M", font=SANS_B(30), fill=(40, 30, 30))
    d.text((x + 12, y + 38), "PRE-ORDERS", font=SANS_B(11), fill=(40, 30, 30))
    d.rectangle([x, y + h - 22, x + w, y + h], fill=(40, 30, 30))
    d.text((x + w - 10, y + h - 11), "TAKE-TWO +6% · 99 METACRITIC", font=SANS_B(11),
           anchor="rm", fill=(255, 255, 255))

def art_votes(d, x, y, w, h):
    """251-11 seat bar."""
    d.rectangle([x, y, x + w, y + h], fill=(20, 38, 63))
    d.text((x + 12, y + 8), "251", font=SANS_B(34), fill=(255, 255, 255))
    d.text((x + w - 12, y + 8), "11", font=SANS_B(34), anchor="ra", fill=(255, 120, 100))
    # seat bar
    bx, by, bw, bh = x + 12, y + h - 30, w - 24, 16
    d.rectangle([bx, by, bx + bw, by + bh], fill=(60, 80, 110))
    d.rectangle([bx, by, bx + bw * 251 / 262, by + bh], fill=(90, 160, 255))
    d.text((x + w / 2, y + h - 11), "FIRST BLACK SPEAKER IF ELECTED", font=SANS_B(9),
           anchor="ma", fill=(255, 255, 255))

def art_money(d, x, y, w, h):
    """EUR 45bn coin stack + split bar."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 214))
    d.text((x + 12, y + 6), "€45bn", font=SANS_B(32), fill=(20, 38, 63))
    d.text((x + 12, y + 40), "EU LOAN FOR UKRAINE", font=SANS_B(11), fill=INK)
    # split bar: 25 arms / 20 budget
    bx, by, bw, bh = x + 12, y + h - 34, w - 24, 18
    d.rectangle([bx, by, bx + bw * 25 / 45, by + bh], fill=(20, 38, 63))
    d.rectangle([bx + bw * 25 / 45, by, bx + bw, by + bh], fill=(201, 162, 39))
    d.text((bx + bw * 25 / 90, by + bh / 2), "€25bn", font=SANS_B(10),
           anchor="mm", fill=(255, 255, 255))
    d.text((bx + bw * (25 + 20 / 2) / 45, by + bh / 2), "€20bn", font=SANS_B(10),
           anchor="mm", fill=INK)

def art_voyager(d, x, y, w, h):
    """Voyager: sun, distance scale, probe dot at one light-day."""
    d.rectangle([x, y, x + w, y + h], fill=(10, 12, 30))
    d.ellipse([x + 10, y + h * 0.62 - 14, x + 38, y + h * 0.62 + 14], fill=(255, 200, 60))
    d.text((x + 44, y + h - 20), "SUN", font=SANS_B(9), fill=(255, 200, 60))
    # scale line
    sy = y + h * 0.62
    d.line([(x + 44, sy), (x + w - 30, sy)], fill=(120, 140, 180), width=2)
    for i in range(1, 6):
        px = x + 44 + i * (w - 90) / 6
        d.line([(px, sy - 5), (px, sy + 5)], fill=(120, 140, 180), width=2)
    d.ellipse([x + w - 34, sy - 6, x + w - 22, sy + 6], fill=(255, 255, 255))
    d.text((x + w - 10, y + 6), "1 LIGHT-DAY", font=SANS_B(15), anchor="ra", fill=(255, 255, 255))
    d.text((x + w - 10, y + 26), "16.1 BILLION MILES", font=SANS_B(11), anchor="ra",
           fill=(180, 200, 230))
    d.text((x + w - 10, y + h - 20), "SIGNAL: 24 HOURS", font=SANS_B(10), anchor="ra",
           fill=(120, 140, 180))

def art_cyclone(d, x, y, w, h):
    """Cyclone spiral over a coast line."""
    d.rectangle([x, y, x + w, y + h], fill=(200, 225, 235))
    cx, cy = x + w * 0.30, y + h * 0.38
    for r, col in [(28, (20, 60, 110)), (19, (60, 120, 170)), (11, (120, 180, 210))]:
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 300, fill=col, width=5)
    d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(20, 60, 110))
    # coast (right side)
    d.polygon([(x + w * 0.68, y), (x + w, y), (x + w, y + h), (x + w * 0.78, y + h)],
              fill=(214, 196, 150))
    d.text((x + w - 8, y + 8), "ANDHRA", font=SANS_B(10), anchor="ra", fill=INK)
    d.text((x + w - 8, y + h - 40), "90-100", font=SANS_B(24), anchor="ra", fill=(20, 60, 110))
    d.text((x + 10, y + h - 14), "GUSTING 110 · LANDFALL FRI", font=SANS_B(10), fill=INK)

def art_deals(d, x, y, w, h):
    """Indonesia-China deals: $71.8bn, 4 partnerships at APEC."""
    d.rectangle([x, y, x + w, y + h], fill=(235, 230, 214))
    d.text((x + 10, y + 6), "$71.8bn", font=SANS_B(30), fill=(20, 38, 63))
    d.text((x + 10, y + 40), "INDONESIA-CHINA", font=SANS_B(11), fill=INK)
    d.text((x + 10, y + h - 14), "4 DEALS · APEC SHENZHEN", font=SANS_B(10), fill=GREY)

def art_ipo(d, x, y, w, h):
    """IPO price tag: $83 above the $70-78 range."""
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255))
    d.rectangle([x + 10, y + 6, x + w - 10, y + 40], fill=(15, 118, 110))
    d.text((x + w / 2, y + 23), "$83", font=SANS_B(28), anchor="mm", fill=(255, 255, 255))
    d.text((x + w / 2, y + 52), "ABOVE $70-78 RANGE", font=SANS_B(10), anchor="ma", fill=INK)
    d.text((x + w / 2, y + h - 12), "NASDAQ: ANT", font=SANS_B(10), anchor="ma", fill=INK)

def art_strike(d, x, y, w, h):
    """Garment strike: factory + picket line + 300 arrested."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 235, 220))
    # factory block, bottom-left
    d.rectangle([x + 12, y + h - 30, x + w * 0.6, y + h - 8], fill=(120, 110, 100))
    d.rectangle([x + w * 0.52, y + h - 48, x + w * 0.52 + 9, y + h - 8], fill=(120, 110, 100))
    for i in range(2):
        d.rectangle([x + 20 + i * 24, y + h - 24, x + 36 + i * 24, y + h - 14],
                    fill=(255, 220, 120))
    # picket dots (top-left)
    for i in range(4):
        px = x + 16 + i * 18
        d.ellipse([px - 4, y + 14, px + 4, y + 22], fill=(178, 34, 34))
        d.line([(px, y + 22), (px, y + 32)], fill=(178, 34, 34), width=2)
    d.text((x + w - 8, y + 8), "132", font=SANS_B(26), anchor="ra", fill=RED)
    d.text((x + w - 8, y + 32), "FACTORIES SHUT", font=SANS_B(10), anchor="ra", fill=INK)

def art_quake(d, x, y, w, h):
    """Seismograph trace + M5.7."""
    d.rectangle([x, y, x + w, y + h], fill=(30, 30, 34))
    mid = y + h * 0.58
    pts = [(x + 8, mid)]
    import math
    for i in range(1, 40):
        px = x + 8 + i * (w - 16) / 40
        amp = 3 if i < 18 or i > 28 else 15 * math.sin(i * 1.7)
        pts.append((px, mid + amp))
    d.line(pts, fill=(255, 200, 60), width=2)
    d.text((x + 10, y + 8), "M5.7", font=SANS_B(30), fill=(255, 255, 255))
    d.text((x + w - 10, y + 12), "VRANCEA", font=SANS_B(11), anchor="ra", fill=(255, 200, 60))
    d.text((x + 10, y + h - 18), "FELT IN UKRAINE + MOLDOVA", font=SANS_B(10),
           fill=(200, 200, 200))

ART = {"summit": art_summit, "gulf": art_gulf, "drones": art_drones, "chart": art_chart,
       "gta": art_gta, "votes": art_votes, "money": art_money, "voyager": art_voyager,
       "cyclone": art_cyclone, "deals": art_deals, "ipo": art_ipo, "strike": art_strike,
       "quake": art_quake}

# ---------------------------------------------------------------- layout
def draw_panel(d, n, region, source, headline, deck, art_kind, x, y, w, h, hero=False):
    col = REGION_COLOR[region]
    d.rectangle([x, y, x + w, y + h], fill=(255, 255, 255), outline=(200, 195, 180), width=1)
    # ribbon
    d.rectangle([x, y, x + w, y + 20], fill=col)
    d.text((x + 7, y + 10), "%d · %s" % (n, region), font=SANS_B(10), anchor="lm", fill=(255, 255, 255))
    d.text((x + w - 7, y + 10), source, font=SANS_B(9), anchor="rm", fill=(255, 230, 150))
    # art
    art_h = 96 if hero else 74
    ART[art_kind](d, x + 1, y + 21, w - 2, art_h)
    # headline + deck
    ty = y + 21 + art_h + 6
    hl_size = 15 if hero else 12
    for line in fit_lines(d, headline, SANS_B(hl_size), w - 14, 2 if hero else 2):
        d.text((x + 7, ty), line, font=SANS_B(hl_size), fill=INK)
        ty += hl_size + 2
    dk_size = 10 if hero else 9
    for line in fit_lines(d, deck, SANS(9 if hero else 9), w - 14, 2):
        d.text((x + 7, ty), line, font=SANS(9), fill=(60, 60, 60))
        ty += 11

# coarse continent polygons (equirectangular, lon -180..180, lat 90..-60)
CONTINENTS = [
    [(-168, 66), (-140, 70), (-120, 72), (-95, 69), (-80, 73), (-60, 62), (-55, 47),
     (-70, 42), (-75, 35), (-80, 26), (-90, 21), (-97, 26), (-105, 20), (-110, 24),
     (-120, 34), (-125, 49), (-150, 60), (-168, 66)],  # N America
    [(-80, 10), (-60, 8), (-50, 0), (-40, -5), (-35, -8), (-40, -20), (-50, -28),
     (-60, -35), (-70, -40), (-75, -20), (-80, -5), (-80, 10)],  # S America
    [(-18, 70), (-10, 58), (0, 51), (5, 58), (10, 57), (18, 56), (24, 58), (28, 71),
     (40, 68), (30, 60), (23, 54), (20, 45), (12, 44), (8, 39), (0, 39), (-9, 37),
     (-9, 43), (-18, 70)],  # Europe
    [(20, 32), (30, 36), (35, 30), (43, 12), (51, 12), (58, 22), (60, 25), (48, 30),
     (40, 32), (32, 31), (22, 33), (20, 32)],  # Middle East / Arabia
    [(10, 37), (20, 32), (32, 31), (35, 28), (43, 12), (48, 11), (51, 10), (44, -2),
     (40, -10), (35, -18), (32, -26), (26, -34), (19, -35), (15, -27), (12, -18),
     (9, -1), (9, 4), (4, 6), (-8, 4), (-13, 8), (-17, 15), (-17, 21), (-16, 27),
     (-10, 31), (0, 36), (10, 37)],  # Africa
    [(60, 70), (90, 75), (120, 77), (160, 70), (180, 66), (170, 60), (160, 55),
     (140, 45), (135, 43), (130, 35), (122, 30), (110, 20), (105, 10), (100, 8),
     (95, 16), (90, 22), (80, 13), (77, 8), (72, 20), (66, 25), (60, 25), (60, 70)],  # Asia
    [(113, -22), (130, -12), (142, -11), (150, -22), (153, -27), (147, -39), (140, -38),
     (129, -32), (115, -35), (113, -22)],  # Australia
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(225, 235, 240), outline=(200, 195, 180), width=1)
    d.text((x + 8, y + 6), "THE WORLD, MAPPED", font=SANS_B(11), fill=INK)
    d.text((x + w - 8, y + 6), "PINS 1-13 · DOTS 14-48", font=SANS_B(9), anchor="ra", fill=GREY)
    mx, my = x + 6, y + 22
    mw, mh = w - 12, h - 52
    def proj(lon, lat):
        px = mx + (lon + 180) / 360 * mw
        py = my + (90 - lat) / 150 * mh
        return (px, py)
    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly], fill=(190, 185, 165),
                  outline=(140, 135, 120))
    # pins for leads (lon, lat) + dots for briefs (approx region centres)
    pins = {1: (113, 22), 2: (50, 27), 3: (36, 49), 4: (-77, 39), 5: (-122, 37),
            6: (-77, 39), 7: (5, 50), 8: (-118, 34), 9: (80, 16), 10: (113, 22),
            11: (-122, 37), 12: (90, 24), 13: (26, 45)}
    # offsets (px) for pins sharing a city, with connector lines.
    # Verified by geometry (proj + land test): every badge sits
    # on land and >=17px from every other badge. 6 was in the Atlantic,
    # 11 in the Pacific; 1-10, 3-13, 9-12 overlapped. Pin 10 moved to
    # Shenzhen with the Indonesia-China deals lead (rev5); pin 1 stacks
    # above it on land (Hunan).
    pin_off = {1: (0, -18), 5: (0, -18), 6: (-13, -13), 8: (15, 9),
               12: (0, -10), 13: (14, 12)}
    # jitter brief dots deterministically by story number
    import hashlib
    # dots sit on each story's own city/region, spread so no two dots
    # share a centre (checked pairwise).
    brief_xy = {14: (30, 36), 15: (38, 15), 16: (34, 31), 17: (2, 47), 18: (121, 14),
                19: (-1, 51), 20: (47, 18), 21: (56, 26), 22: (-122, 47), 23: (-67, 10),
                24: (-77, 39), 25: (20, 54), 26: (38, 48), 27: (139, 36), 28: (77, 21),
                29: (-122, 37), 30: (-93, 45), 31: (13, 48), 32: (21, 42), 33: (-1, 52),
                34: (10, 52), 35: (25, 61), 36: (133, -25), 37: (113, -2), 38: (39, 9),
                39: (-100, 50), 40: (90, 24), 41: (29, 41), 42: (-3, 40), 43: (33, 2),
                44: (41, 3), 45: (6, 11), 46: (-62, -3), 47: (77, 13), 48: (30, -2)}
    for n, (lon, lat) in brief_xy.items():
        px, py = proj(lon, lat)
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=REGION_COLOR[
            dict((b[0], b[1]) for b in BRIEFS)[n]])
    for n, (lon, lat) in pins.items():
        px, py = proj(lon, lat)
        ox, oy = pin_off.get(n, (0, 0))
        if (ox, oy) != (0, 0):
            d.line([(px, py), (px + ox, py + oy)], fill=RED, width=1)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=RED)
        px, py = px + ox, py + oy
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py), str(n), font=SANS_B(10), anchor="mm", fill=(255, 255, 255),
               stroke_width=1, stroke_fill=(255, 255, 255))
    d.text((x + 8, y + h - 20), "Pins are approximate.", font=SANS(9), fill=GREY)

def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # ---- masthead
    d.rectangle([0, 0, W, 78], fill=NAVY)
    d.text((14, 40), "THE WORLD'S NEWS", font=SERIF_B(44), anchor="lm", fill=(255, 255, 255))
    d.text((W - 14, 24), "WEDNESDAY 18 NOVEMBER 2026", font=SANS_B(15), anchor="rm",
           fill=(255, 255, 255))
    d.text((W - 14, 52), "48 STORIES · 7 REGIONS · 13 DRAWN", font=SANS_B(12), anchor="rm",
           fill=(255, 200, 60))
    d.text((14, 40), "THE WORLD'S NEWS", font=SERIF_B(44), anchor="lm", fill=(255, 255, 255))
    # ---- region proportion bar
    x = 10
    d.text((10, 84), "REGIONS", font=SANS_B(10), fill=GREY)
    bx, bw_total = 62, W - 72
    total = sum(REGION_COUNT.values())
    segs = []
    for r in REGIONS:
        wseg = bw_total * REGION_COUNT[r] / total
        d.rectangle([x, 82, x + wseg - 1, 98], fill=REGION_COLOR[r])
        segs.append((x, wseg, r))
        x += wseg
    for sx, wseg, r in segs:
        label = "%s %d" % (r, REGION_COUNT[r])
        if wseg >= 45:
            d.text((sx + wseg / 2, 90), label, font=SANS_B(8),
                   anchor="mm", fill=(255, 255, 255))
        else:
            # narrow segment (OCEANIA sits between two wide segments, so
            # its smaller label overflows onto empty space, never on text)
            d.text((sx + wseg / 2, 90), label, font=SANS_B(7),
                   anchor="mm", fill=(255, 255, 255))
    # ---- UTC strip
    d.rectangle([10, 104, W - 10, 122], fill=(255, 255, 255), outline=(200, 195, 180), width=1)
    d.text((16, 113), "THE DAY IN UTC", font=SANS_B(10), anchor="lm", fill=NAVY)
    utc = [("00:48", "Romania quake M5.7"), ("08:00", "126 downed"),
           ("10:16", "Voyager 1 light-day"), ("18:04", "Dhaka unrest reported"),
           ("19:00", "Fed minutes"), ("21:00", "Dow closes -561")]
    ux = 150
    for t, label in utc:
        d.text((ux, 113), t, font=SANS_B(10), anchor="lm", fill=RED)
        d.text((ux + 42, 113), label, font=SANS(9), anchor="lm", fill=INK)
        ux += 42 + d.textlength(label, font=SANS(9)) + 16
    # ---- heroes
    hy = 128
    for i, lead in enumerate(LEADS[:3]):
        draw_panel(d, *lead, x=10 + i * 337, y=hy, w=329, h=172, hero=True)
    # ---- rows 2-3
    for row, leads in enumerate((LEADS[3:8], LEADS[8:13])):
        ry = 306 + row * 170
        for i, lead in enumerate(leads):
            draw_panel(d, *lead, x=10 + i * 202, y=ry, w=194, h=164)
    # ---- bottom: map + briefs
    by = 646
    draw_map(d, 10, by, 278, 292)
    d.text((298, by + 4), "ALSO ON WEDNESDAY", font=SANS_B(12), fill=INK)
    d.text((W - 10, by + 4), "35 MORE STORIES", font=SANS_B(10), anchor="ra", fill=GREY)
    cols = [BRIEFS[i::3] for i in range(3)]
    col_w = (W - 10 - 298 - 16) / 3
    for ci, col in enumerate(cols):
        cx = 298 + ci * (col_w + 8)
        cy = by + 24
        for n, region, text in col:
            c = REGION_COLOR[region]
            d.ellipse([cx, cy + 3, cx + 12, cy + 15], fill=c)
            d.text((cx + 6, cy + 9), str(n), font=SANS_B(7), anchor="mm", fill=(255, 255, 255))
            for line in fit_lines(d, text, SANS(9), col_w - 18, 2):
                d.text((cx + 16, cy), line, font=SANS(9), fill=INK)
                cy += 11
            cy += 3
    # ---- footer: SOURCES
    fy = 946
    d.rectangle([10, fy, W - 10, 1014], fill=(255, 240, 235), outline=RED, width=2)
    d.text((18, fy + 10), "SOURCES", font=SANS_B(12), fill=RED)
    d.text((18, fy + 30),
           "AP · Reuters · NASA · Fed · INFP · IMD · CNN · Sensor Tower.",
           font=SANS(10), fill=INK)
    d.text((18, fy + 48),
           "Every story on this page was first reported on Wednesday 18 November 2026.",
           font=SANS(10), fill=INK)
    return img

if __name__ == "__main__":
    render().save("entry.png", optimize=True)
    print("saved entry.png")
