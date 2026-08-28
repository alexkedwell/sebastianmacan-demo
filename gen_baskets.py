#!/usr/bin/env python3
"""Generate the 4 candy-basket bundle pages. Shared dark style, per-basket gradient.
Each page: hero + basket art + contents list (every item with its own gated download)
+ value math + FAQ-ish footer. Run from site dir: python3 gen_baskets.py"""

ITEMS = {
    # name: (kind, tagline, price, page, download)
    "Ghost":   ("Granular Texture Machine", "Freeze sound. Then haunt it.", 19, "ghost.html",   "downloads/Ghost-v1.1-macOS.pkg"),
    "Liftoff": ("Space Phaser-Flanger", "Rockets. Actual rockets.", 19, "liftoff.html", "downloads/Liftoff-v1.0-macOS.pkg"),
    "Orbit":   ("3D Auto-Pan", "Hats that fly around your head.", 19, "orbit.html",   "downloads/Orbit-v1.0-macOS.pkg"),
    "Reels":   ("Tape Machine", "A real tape machine, in the box.", 19, "reels.html",   "downloads/Reels-v1.0-macOS.pkg"),
    "Gloss":   ("Instant Mix Polish", "Mixes that sit right. Four knobs.", 19, "gloss.html",   "downloads/Gloss-v1.0-macOS.pkg"),
    "Halo":    ("Mastering Finisher", "Turn LIFT until the halo closes.", 19, "halo.html",    "downloads/Halo-v1.0-macOS.pkg"),
    "Biome":   ("Granular Texture Blender", "Drop a rainforest on your beat.", 39, "biome.html",   "downloads/Biome-v1.0-macOS.pkg"),
    "Magician":("Chord & Melody Generator", "Hit songs on tap. 20 genres.", 39, "magician.html","downloads/Magician-v1.2-macOS.pkg"),
    "Fauna":   ("Creature Voice Synth", "Play the ocean. Play the sky.", 29, "fauna.html",   "downloads/Fauna-v1.0-macOS.pkg"),
    "Jelly":   ("Wobble Machine", "Make everything jiggle. Free forever.", 0, "jelly.html",  "downloads/Jelly-v1.0-macOS.pkg"),
    "Bounce":  ("Beat Repeater", "Stutter like a bouncing ball. Free forever.", 0, "bounce.html", "downloads/Bounce-v1.0-macOS.pkg"),
    "Hit Chords 200":  ("MIDI Chord Pack", "200 progressions built for hooks.", 15, None, "downloads/HitChords200-SebastianMacan.zip"),
    "Club Chords 120": ("MIDI Chord Pack", "120 progressions for the floor.", 15, None, "downloads/ClubChords120-SebastianMacan.zip"),
    "Soul Chords 120": ("MIDI Chord Pack", "120 progressions with feel.", 15, None, "downloads/SoulChords120-SebastianMacan.zip"),
    "Ionian Mode 48":     ("MIDI Mode Pack", "48 progressions. The bright classic.", 10, None, "downloads/IonianMode48-SebastianMacan.zip"),
    "Dorian Mode 48":     ("MIDI Mode Pack", "48 progressions. Smooth and soulful.", 10, None, "downloads/DorianMode48-SebastianMacan.zip"),
    "Phrygian Mode 48":   ("MIDI Mode Pack", "48 progressions. Dark and exotic.", 10, None, "downloads/PhrygianMode48-SebastianMacan.zip"),
    "Lydian Mode 48":     ("MIDI Mode Pack", "48 progressions. Dreamy and floating.", 10, None, "downloads/LydianMode48-SebastianMacan.zip"),
    "Mixolydian Mode 48": ("MIDI Mode Pack", "48 progressions. Groovy and warm.", 10, None, "downloads/MixolydianMode48-SebastianMacan.zip"),
    "Aeolian Mode 48":    ("MIDI Mode Pack", "48 progressions. The minor mood.", 10, None, "downloads/AeolianMode48-SebastianMacan.zip"),
    "Locrian Mode 48":    ("MIDI Mode Pack", "48 progressions. The forbidden one.", 10, None, "downloads/LocrianMode48-SebastianMacan.zip"),
}

BASKETS = [
    {
        "file": "basket-effects.html", "title": "EFFECTS BASKET", "price": 59, "img": "img/bundles/effects_bundle.png",
        "g1": "#8b5cf6", "g2": "#60a5fa",
        "tag": "Six flavors of motion, texture and polish. One basket.",
        "desc": "All six paid effects in one grab. Freeze it, lift it, spin it, tape it, shine it, drown it in glow.",
        "items": ["Ghost", "Liftoff", "Orbit", "Reels", "Gloss", "Halo"],
        "meta": "6 plugins · VST3 + AU · macOS",
        "big_dl": ("Download the whole basket", "downloads/EffectsBasket-SebastianMacan.zip"),
    },
    {
        "file": "basket-instruments.html", "title": "INSTRUMENTS BASKET", "price": 69, "img": "img/bundles/instruments_bundle.png",
        "g1": "#3ecf6e", "g2": "#ffd257",
        "tag": "The three big ones. Texture, hits, creatures.",
        "desc": "Biome grows textures from any sound, Magician writes the chords and melodies, Fauna is a synth full of living things. The whole instrument shelf.",
        "items": ["Biome", "Magician", "Fauna"],
        "meta": "3 plugins · VST3 + AU · macOS",
        "big_dl": ("Download the whole basket", "downloads/InstrumentsBasket-SebastianMacan.zip"),
    },
    {
        "file": "basket-midi.html", "title": "MIDI MEGA BASKET", "price": 49, "img": "img/bundles/midi_mega_bundle.png",
        "g1": "#ff5ca8", "g2": "#8b5cf6",
        "tag": "796 progressions. The complete harmonic arsenal.",
        "desc": "Every MIDI pack we make: all 3 genre chord packs plus all 7 mode packs. Drag and drop into any DAW, works with any synth or piano you already own.",
        "items": ["Hit Chords 200", "Club Chords 120", "Soul Chords 120",
                  "Ionian Mode 48", "Dorian Mode 48", "Phrygian Mode 48", "Lydian Mode 48",
                  "Mixolydian Mode 48", "Aeolian Mode 48", "Locrian Mode 48"],
        "meta": "10 packs · 796 MIDI files · any DAW",
        "big_dl": ("Download all 796", "downloads/MIDIMega796-SebastianMacan.zip"),
    },
    {
        "file": "basket-candy-shop.html", "title": "THE WHOLE CANDY SHOP", "price": 99, "img": "img/bundles/everything_bundle.png",
        "g1": "#ff3d5a", "g2": "#ffd257",
        "tag": "Every plugin. Every MIDI pack. All of it.",
        "desc": "One basket to rule the store: all 11 plugins (the free ones too, obviously) plus all 796 MIDI progressions. If it is on the shelf, it is in this basket.",
        "items": ["Biome", "Magician", "Fauna", "Ghost", "Liftoff", "Orbit", "Reels", "Gloss", "Halo", "Jelly", "Bounce",
                  "Hit Chords 200", "Club Chords 120", "Soul Chords 120",
                  "Ionian Mode 48", "Dorian Mode 48", "Phrygian Mode 48", "Lydian Mode 48",
                  "Mixolydian Mode 48", "Aeolian Mode 48", "Locrian Mode 48"],
        "meta": "11 plugins + 796 MIDI files",
        "big_dl": ("Download the whole candy shop", "downloads/WholeCandyShop-SebastianMacan.zip"),
    },
]

def row(name):
    kind, tag, price, page, dl = ITEMS[name]
    price_html = f'<s>${price}</s>' if price else '<span class="freetag">FREE forever</span>'
    link = f'<a class="rowlink" href="{page}">See how it works &rarr;</a>' if page else ''
    return f'''    <div class="item">
      <div class="iinfo">
        <div class="ikind">{kind}</div>
        <div class="iname">{name}</div>
        <p class="itag">{tag}</p>
        {link}
      </div>
      <div class="iact">
        <div class="iprice">{price_html}</div>
        <a class="dl idl" href="{dl}">Download</a>
      </div>
    </div>'''

def page(b):
    total = sum(ITEMS[n][2] for n in b["items"])
    rows = "\n".join(row(n) for n in b["items"])
    big = ""
    hero_dl = ""
    if b.get("big_dl"):
        label, href = b["big_dl"]
        big = f'<div class="cta"><a class="dl" href="{href}">{label}</a><div class="meta">One zip, everything inside. Download once, unzip, done.</div></div>'
        hero_dl = f'<div class="cta" style="margin-top:22px;"><a class="dl" href="{href}">{label}</a></div>'
    n_items = len(b["items"])
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{b["title"].title()} | Sebastian Macan</title>
<meta name="description" content="{b["desc"]}">
<meta name="robots" content="index,follow">
<style>
  :root {{ --bg:#0a0a0c; --card:#141418; --txt:#f2f2f4; --dim:#8a8a94; --line:#222228; --g1:{b["g1"]}; --g2:{b["g2"]}; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--txt); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif; line-height:1.65; }}
  .wrap {{ max-width:960px; margin:0 auto; padding:0 24px; }}
  header {{ padding:28px 0; display:flex; justify-content:space-between; align-items:center; }}
  .logo {{ font-weight:800; letter-spacing:.12em; font-size:15px; text-transform:uppercase; color:var(--txt); text-decoration:none; }}
  .logo span {{ color:#ff3d5a; }}
  nav a {{ color:var(--dim); text-decoration:none; margin-left:22px; font-size:14px; }}
  nav a:hover {{ color:var(--txt); }}
  .back {{ display:inline-block; margin:18px 0 0; color:var(--dim); text-decoration:none; font-size:14px; }}
  .back:hover {{ color:var(--txt); }}
  .hero {{ text-align:center; padding:26px 0 8px; }}
  .kind {{ font-size:12px; letter-spacing:.16em; text-transform:uppercase; color:var(--dim); font-weight:700; }}
  h1 {{ font-size:clamp(38px,8vw,72px); font-weight:900; letter-spacing:-.03em; line-height:1.05;
    background:linear-gradient(135deg,var(--g1),var(--g2)); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .tag {{ font-size:clamp(16px,3vw,21px); font-weight:700; margin-top:8px; }}
  .bimg {{ display:block; width:min(560px,92%); margin:26px auto 4px; border-radius:20px; animation:float 7s ease-in-out infinite; }}
  @keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-8px)}} }}
  .pricebar {{ text-align:center; margin:18px 0 4px; }}
  .pricebar .big {{ font-size:34px; font-weight:900; }}
  .pricebar s {{ color:var(--dim); font-weight:700; font-size:20px; margin-right:10px; }}
  .freebie {{ color:#5ad9d0; font-weight:800; }}
  .meta {{ color:var(--dim); font-size:13px; margin-top:10px; text-align:center; }}
  h2 {{ font-size:clamp(22px,4vw,30px); font-weight:900; letter-spacing:-.02em; margin:48px 0 6px; }}
  .sub {{ color:var(--dim); font-size:14.5px; margin-bottom:18px; }}
  .item {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:18px 22px; margin:12px 0;
    display:flex; justify-content:space-between; align-items:center; gap:18px; flex-wrap:wrap; }}
  .ikind {{ font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim); font-weight:700; }}
  .iname {{ font-size:21px; font-weight:900; letter-spacing:-.01em;
    background:linear-gradient(135deg,var(--g1),var(--g2)); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .itag {{ color:#c8c8d0; font-size:14px; }}
  .rowlink {{ color:var(--dim); font-size:13px; text-decoration:none; }}
  .rowlink:hover {{ color:var(--txt); }}
  .iact {{ text-align:right; display:flex; align-items:center; gap:16px; }}
  .iprice {{ color:var(--dim); font-weight:700; }}
  .iprice s {{ font-size:15px; }}
  .freetag {{ color:#5ad9d0; font-size:12px; font-weight:800; letter-spacing:.06em; }}
  .dl {{ display:inline-block; color:#fff; font-weight:800; font-size:15px; padding:12px 28px; border-radius:999px; text-decoration:none;
    background:linear-gradient(135deg,var(--g1),var(--g2)); box-shadow:0 6px 26px rgba(0,0,0,.4); transition:transform .15s; }}
  .dl:hover {{ transform:translateY(-2px) scale(1.02); }}
  .idl {{ font-size:14px; padding:10px 22px; }}
  .cta {{ text-align:center; margin:34px 0 8px; }}
  .cta .dl {{ font-size:17px; padding:16px 44px; }}
  .mathbox {{ background:var(--card); border:1px solid var(--line); border-radius:16px; padding:20px 24px; margin:30px 0 8px; text-align:center; }}
  .mathbox b {{ color:var(--txt); }}
  footer {{ border-top:1px solid var(--line); margin-top:72px; padding:32px 0 48px; color:var(--dim); font-size:13px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
  footer a {{ color:var(--dim); }}
  @media (max-width:640px){{ .wrap{{padding:0 16px;}} header{{flex-direction:column;gap:10px;}} footer{{flex-direction:column;text-align:center;}} .iact{{width:100%;justify-content:space-between;}} }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <a class="logo" href="/">SEBASTIAN<span>MACAN</span></a>
    <nav><a href="/#effects">Effects</a><a href="/#instruments">Instruments</a><a href="/#midi">MIDI</a></nav>
  </header>
  <a class="back" href="/#bundles">&larr; Back to the baskets</a>

  <section class="hero">
    <div class="kind">Candy Basket</div>
    <h1>{b["title"]}</h1>
    <p class="tag">{b["tag"]}</p>
    <img class="bimg" src="{b["img"]}" alt="{b["title"]} basket art">
    <div class="pricebar"><span class="big"><s>${total}</s> ${b["price"]}</span> <span class="freebie">&middot; free during launch</span></div>
    <div class="meta">{b["meta"]}</div>
    {hero_dl}
  </section>

  <h2>What's in the basket</h2>
  <p class="sub">{b["desc"]} Every item below is yours &mdash; grab them one by one, all free during launch.</p>
{rows}

  {big}

  <div class="mathbox">
    Bought one by one this basket adds up to <b>${total}</b>. As a basket it's <b>${b["price"]}</b> when checkout opens &mdash; and <b>free right now during launch</b>. {n_items} items, zero catches.
  </div>

  <footer>
    <div>&copy; 2026 Aluetion, LLC &middot; Sebastian Macan</div>
    <div><a href="pricing.html">Pricing</a> &middot; <a href="terms.html">Terms</a> &middot; <a href="refunds.html">Refunds</a> &middot; <a href="privacy.html">Privacy</a></div>
  </footer>
</div>
<script src="js/email-gate.js" defer></script>
</body>
</html>'''

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
for b in BASKETS:
    open(b["file"], "w").write(page(b))
    print("wrote", b["file"])
