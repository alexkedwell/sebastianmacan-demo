#!/usr/bin/env python3
"""Generate midi-packs.html: one page, a section per MIDI pack (3 chord packs +
7 mode packs + the 336 bundle), each with a styled video placeholder slot that
becomes a YouTube embed when Alex films his Ableton demos.
To drop a video in: replace data-yt="" with data-yt="VIDEOID" in the PACKS list
and rerun. Run from site dir: python3 gen_midi_page.py
WARNING (Sep 2 2026): this generator is STALE vs the live midi-packs.html -
the live page carries the hand-added HITMAKER CHORDS section and the
artist-name scrub (Paddle compliance). Do NOT rerun without first folding
those into PACKS/copy, or the regen wipes them. Cart buttons (cartrow) ARE
included below and map data-cart-add/buy ids to js/cart.js CATALOG keys."""

PACKS = [
    {"id": "hitchords", "name": "HIT CHORDS 500", "kind": "MIDI Chord Pack", "n": "500 .mid files",
     "g1": "#ff5ca8", "g2": "#ffd257",
     "tag": "The progressions behind the hits.",
     "desc": "500 chord progressions across 11 genres: Pop, Trap, RnB, EDM, LoFi, Rock, Latin, Cinematic, Country, Gospel/Jazz, K-Pop. Genre-true voicings with the 7ths and 9ths already in place.",
     "inside": ["11 genres, 500 progressions, all 24 keys", "Voiced like the records, not block triads", "Labeled by genre and key, drag straight in"],
     "dl": "downloads/HitChords500-SebastianMacan.zip", "yt": ""},
    {"id": "clubchords", "name": "CLUB CHORDS 240", "kind": "MIDI Chord Pack", "n": "240 .mid files",
     "g1": "#60a5fa", "g2": "#8b5cf6",
     "tag": "Chords for the dancefloor.",
     "desc": "240 progressions built for club music: House, Techno, Dubstep, Future Bass, Drum & Bass, UK Garage. 20 per genre, voiced the way each scene actually plays them.",
     "inside": ["6 club genres, 40 progressions each, all 24 keys", "Stab voicings and pads that cut through a mix", "Tested against four-on-the-floor grooves"],
     "dl": "downloads/ClubChords240-SebastianMacan.zip", "yt": ""},
    {"id": "soulchords", "name": "SOUL CHORDS 240", "kind": "MIDI Chord Pack", "n": "240 .mid files",
     "g1": "#f5a623", "g2": "#ff5ca8",
     "tag": "The rich stuff. 9ths, 11ths, church.",
     "desc": "240 progressions dripping with soul: Neo-Soul, Gospel, Jazz, Blues, Motown, Funk. Extended voicings, turnarounds and walkups straight from the source.",
     "inside": ["6 soul genres, 40 progressions each, all 24 keys", "Real extended voicings: 9ths, 11ths, 13ths", "Turnarounds and walkups included"],
     "dl": "downloads/SoulChords240-SebastianMacan.zip", "yt": ""},
    {"id": "ionian", "name": "IONIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#ffd84a", "g2": "#ff9f1c",
     "tag": "Pure major. The sound of every anthem chorus ever written.",
     "desc": "48 progressions in pure major, the brightest flavor in the case. Hey Jude, Let It Be, most of pop history. Every loop lands the mode's signature color.",
     "inside": ["48 progressions, every chord true to Ionian", "All keys covered", "Anthem-chorus energy on tap"],
     "dl": "downloads/IonianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "dorian", "name": "DORIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#39e6d0", "g2": "#4a90ff",
     "tag": "Minor with hope. Groovy, cool, never fully sad.",
     "desc": "48 progressions in the mode of Get Lucky, Billie Jean and Mad World. Minor that grooves instead of mopes, with the raised sixth doing the magic.",
     "inside": ["48 progressions, signature raised-6th color", "All keys covered", "The funk and daft-house secret"],
     "dl": "downloads/DorianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "phrygian", "name": "PHRYGIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#ff3d5a", "g2": "#8b0000",
     "tag": "Dark Spanish menace. Villain energy.",
     "desc": "48 progressions with the flat-2 knife edge: dark techno, trap and trance menace, flamenco fire. The mode you reach for when a track needs a threat.",
     "inside": ["48 progressions built on the flat-2 color", "All keys covered", "Techno, trap and cinematic tension"],
     "dl": "downloads/PhrygianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "lydian", "name": "LYDIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#c084fc", "g2": "#7dd8ff",
     "tag": "Floating, dreamlike major. The melodic house secret weapon.",
     "desc": "48 progressions that float: Ben Bohmer territory, film scores, that raised-4 shimmer that makes a chord sound like it's levitating.",
     "inside": ["48 progressions with the raised-4 shimmer", "All keys covered", "Melodic house and score writers, feast"],
     "dl": "downloads/LydianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "mixolydian", "name": "MIXOLYDIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#ff8c42", "g2": "#ffd84a",
     "tag": "Major with a rebel flat seven. Rock, funk and festival gold.",
     "desc": "48 progressions in the mode of Sweet Home Alabama, Clocks and Royals. Major that swaggers, powered by the flat-7.",
     "inside": ["48 progressions on the flat-7 swagger", "All keys covered", "Rock, funk, festival anthems"],
     "dl": "downloads/MixolydianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "aeolian", "name": "AEOLIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#7b8cff", "g2": "#3d4a8f",
     "tag": "Natural minor. The emotional workhorse of modern music.",
     "desc": "48 progressions in natural minor: Lose Yourself, Someone Like You, every sad banger ever. The workhorse, done right.",
     "inside": ["48 progressions of pure natural minor", "All keys covered", "The emotional backbone of modern music"],
     "dl": "downloads/AeolianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "locrian", "name": "LOCRIAN MODE 48", "kind": "Modal Series", "n": "48 .mid files",
     "g1": "#e8e8f0", "g2": "#6b21a8",
     "tag": "The forbidden mode. Almost nobody writes in it. We did.",
     "desc": "48 progressions in the mode theory teachers warn you about. Unstable, unresolved, unforgettable. Army of Me, YYZ, you next.",
     "inside": ["48 progressions taming the diminished tonic", "All keys covered", "Sounds nobody else's pack has"],
     "dl": "downloads/LocrianMode48-SebastianMacan.zip", "yt": ""},
    {"id": "allmodes", "name": "ALL 7 MODES · 336", "kind": "Modal Series Bundle", "n": "336 .mid files",
     "g1": "#ff3d5a", "g2": "#39e6d0",
     "tag": "The complete modal toolkit. Who else even makes this?",
     "desc": "Every mode pack in one download: all 7 modes, 48 progressions each, 336 total. The whole rest of the candy case.",
     "inside": ["All 7 mode packs in one zip", "336 progressions, every key", "One download, the full modal palette"],
     "dl": "downloads/AllModes336-SebastianMacan.zip", "yt": ""},
]

def media(p):
    vid = f'img/video/midi/{p["id"]}_demo.mp4'
    import os as _os
    if _os.path.exists(vid):
        return f'''<div class="vslot live"><video autoplay muted loop playsinline preload="metadata" poster="img/video/midi/{p["id"]}_poster.jpg"><source src="{vid}" type="video/mp4"></video></div>
      <div class="vcap">Real progressions straight from the pack, playing on loop</div>'''
    if p["yt"]:
        return f'''<div class="vslot live"><iframe src="https://www.youtube-nocookie.com/embed/{p["yt"]}" title="{p["name"]} demo" frameborder="0" allow="accelerometer; encrypted-media; picture-in-picture" allowfullscreen loading="lazy"></iframe></div>'''
    return f'''<div class="vslot">
        <div class="vinner">
          <div class="vplay">&#9654;</div>
          <div class="vtxt">Demo video coming soon</div>
          <div class="vsub">Sebastian drags these into a session and plays them live</div>
        </div>
      </div>'''

def section(p, flip):
    lis = "\n".join(f"          <li>{x}</li>" for x in p["inside"])
    return f'''  <section class="pack {'flip' if flip else ''}" id="{p["id"]}" style="--g1:{p["g1"]};--g2:{p["g2"]};">
    <div class="pmedia">
      {media(p)}
    </div>
    <div class="pinfo">
      <div class="kind">{p["kind"]}</div>
      <h2>{p["name"]}</h2>
      <p class="tag">{p["tag"]}</p>
      <p class="desc">{p["desc"]}</p>
      <ul>
{lis}
      </ul>
      <div class="actions">
        <a class="dl" href="{p["dl"]}">Download the Pack</a>
        <span class="meta">{p["n"]} &middot; works in every DAW</span>
      </div>
      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="{p["id"]}">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="{p["id"]}">Buy Now</span></div>
    </div>
  </section>'''

sections = "\n\n".join(section(p, i % 2 == 1) for i, p in enumerate(PACKS))
toc = "\n".join(f'      <a href="#{p["id"]}" style="--g1:{p["g1"]};--g2:{p["g2"]};">{p["name"]}</a>' for p in PACKS)

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Free MIDI Chord Packs &amp; Mode Packs | Sebastian Macan</title>
<meta name="description" content="1316 MIDI chord progressions: genre chord packs (Pop, Trap, RnB, Club, Soul) and the complete Modal Series covering all 7 modes. Drag-and-drop .mid files that work in every DAW. Free during launch.">
<style>
  :root {{ --bg:#0a0a0c; --card:#141418; --txt:#f2f2f4; --dim:#8a8a94; --line:#222228; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:var(--bg); color:var(--txt); font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif; line-height:1.65; }}
  .wrap {{ max-width:1080px; margin:0 auto; padding:0 24px; }}
  header {{ padding:28px 0; display:flex; justify-content:space-between; align-items:center; }}
  .logo {{ font-weight:800; letter-spacing:.12em; font-size:15px; text-transform:uppercase; color:var(--txt); text-decoration:none; }}
  .logo span {{ color:#ff3d5a; }}
  nav a {{ color:var(--dim); text-decoration:none; margin-left:22px; font-size:14px; }}
  nav a:hover {{ color:var(--txt); }}
  .back {{ display:inline-block; margin:18px 0 0; color:var(--dim); text-decoration:none; font-size:14px; }}
  .back:hover {{ color:var(--txt); }}
  .hero {{ text-align:center; padding:30px 0 6px; }}
  .hero .kind {{ font-size:12px; letter-spacing:.16em; text-transform:uppercase; color:var(--dim); font-weight:700; }}
  h1 {{ font-size:clamp(34px,7vw,64px); font-weight:900; letter-spacing:-.03em; line-height:1.05;
    background:linear-gradient(135deg,#ff5ca8,#8b5cf6); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .hero p {{ color:var(--dim); max-width:640px; margin:12px auto 0; font-size:15.5px; }}
  .toc {{ display:flex; flex-wrap:wrap; gap:10px; justify-content:center; margin:26px 0 8px; }}
  .toc a {{ font-size:12px; font-weight:800; letter-spacing:.04em; text-decoration:none; padding:8px 14px; border-radius:999px;
    border:1px solid var(--line); color:var(--txt); background:var(--card); transition:transform .15s, border-color .15s; }}
  .toc a:hover {{ transform:translateY(-2px); border-color:var(--g1); }}
  .pack {{ display:grid; grid-template-columns:1fr 1fr; gap:34px; align-items:center; margin:58px 0; }}
  .pack.flip .pmedia {{ order:2; }}
  .kind {{ font-size:11px; letter-spacing:.14em; text-transform:uppercase; color:var(--dim); font-weight:700; }}
  .pack h2 {{ font-size:clamp(26px,4vw,40px); font-weight:900; letter-spacing:-.02em; line-height:1.05; margin-top:4px;
    background:linear-gradient(135deg,var(--g1),var(--g2)); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .tag {{ font-size:16px; font-weight:700; margin-top:6px; }}
  .desc {{ color:#c8c8d0; font-size:15px; margin-top:10px; }}
  ul {{ margin:12px 0 0 20px; }}
  li {{ color:var(--dim); font-size:14px; margin-bottom:6px; }}
  .actions {{ margin-top:18px; display:flex; align-items:center; gap:16px; flex-wrap:wrap; }}
  .dl {{ display:inline-block; color:#fff; font-weight:800; font-size:15px; padding:13px 30px; border-radius:999px; text-decoration:none;
    background:linear-gradient(135deg,var(--g1),var(--g2)); box-shadow:0 6px 28px rgba(0,0,0,.45); transition:transform .15s; }}
  .dl:hover {{ transform:translateY(-2px) scale(1.02); }}
  .meta {{ color:var(--dim); font-size:12.5px; }}
  .vslot {{ position:relative; aspect-ratio:16/9; border-radius:18px; overflow:hidden; border:1px solid var(--line);
    background:radial-gradient(120% 120% at 30% 20%, color-mix(in srgb, var(--g1) 16%, #101014), #0d0d10);
    display:flex; align-items:center; justify-content:center; animation:float 7s ease-in-out infinite; }}
  .vslot iframe, .vslot video {{ position:absolute; inset:0; width:100%; height:100%; object-fit:cover; }}
  .vslot.live {{ animation:none; }}
  .vcap {{ text-align:center; color:var(--dim); font-size:12.5px; margin-top:10px; }}
  @keyframes float {{ 0%,100%{{transform:translateY(0)}} 50%{{transform:translateY(-7px)}} }}
  .vinner {{ text-align:center; padding:20px; }}
  .vplay {{ width:64px; height:64px; margin:0 auto; border-radius:50%; display:flex; align-items:center; justify-content:center;
    font-size:22px; color:#fff; background:linear-gradient(135deg,var(--g1),var(--g2)); box-shadow:0 8px 34px rgba(0,0,0,.5); }}
  .vtxt {{ margin-top:14px; font-weight:800; font-size:16px; }}
  .vsub {{ color:var(--dim); font-size:13px; margin-top:4px; }}
  .megabar {{ text-align:center; background:var(--card); border:1px solid var(--line); border-radius:20px; padding:30px 26px; margin:64px 0 8px; }}
  .megabar h2 {{ font-size:clamp(24px,4vw,34px); font-weight:900;
    background:linear-gradient(135deg,#ff5ca8,#8b5cf6); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }}
  .megabar p {{ color:var(--dim); font-size:14.5px; margin:8px auto 16px; max-width:560px; }}
  .megabar .dl {{ background:linear-gradient(135deg,#ff5ca8,#8b5cf6); font-size:16px; padding:15px 40px; }}
  footer {{ border-top:1px solid var(--line); margin-top:72px; padding:32px 0 48px; color:var(--dim); font-size:13px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:12px; }}
  footer a {{ color:var(--dim); }}
  @media (max-width:760px) {{
    .pack {{ grid-template-columns:1fr; gap:18px; margin:44px 0; }}
    .pack.flip .pmedia {{ order:0; }}
    .wrap {{ padding:0 16px; }}
    header {{ flex-direction:column; gap:10px; }}
    footer {{ flex-direction:column; text-align:center; }}
  }}
</style>
</head>
<body>
<div class="wrap">
  <header>
    <a class="logo" href="/">SEBASTIAN<span>MACAN</span></a>
    <nav><a href="/#effects">Effects</a><a href="/#instruments">Instruments</a><a href="/#midi">MIDI</a></nav>
  </header>
  <a class="back" href="/#midi">&larr; Back to the store</a>

  <section class="hero">
    <div class="kind">MIDI Packs</div>
    <h1>1316 PROGRESSIONS</h1>
    <p>Every chord pack and mode pack in the store, up close. Drag any .mid file into your DAW, drop it on any synth or piano you already own, and it plays. No plugin required, works everywhere MIDI works.</p>
    <div class="toc">
{toc}
    </div>
  </section>

{sections}

  <div class="megabar">
    <h2>WANT ALL OF IT?</h2>
    <p>The MIDI Mega Basket packs all 3 chord packs and all 7 mode packs, 1316 progressions, into one download.</p>
    <a class="dl" href="downloads/MIDIMega1316-SebastianMacan.zip">Download all 1316</a>
    <div class="cartrow" style="justify-content:center;"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="midimega">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="midimega">Buy Now</span></div>
    <div class="meta" style="margin-top:12px;"><a href="basket-midi.html" style="color:var(--dim);">or open the MIDI Mega Basket &rarr;</a></div>
  </div>

  <footer>
    <div>&copy; 2026 Aluetion, LLC &middot; Sebastian Macan</div>
    <div><a href="pricing.html">Pricing</a> &middot; <a href="terms.html">Terms</a> &middot; <a href="refunds.html">Refunds</a> &middot; <a href="privacy.html">Privacy</a></div>
  </footer>
</div>
<script src="js/cart.js" defer></script>
<script src="js/email-gate.js" defer></script>
</body>
</html>'''

import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
open("midi-packs.html", "w").write(html)
print("wrote midi-packs.html")
