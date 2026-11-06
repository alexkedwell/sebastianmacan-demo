#!/usr/bin/env python3
"""Pre-launch reshape (Alex, Nov 6 2026): Jelly + Warble FREE in the Candy Bag (5 free), Effects Basket gone,
Lofi Basket = Honey + Fireplace $22 (Cozy folded in). Anchored str.replace edits run on BOTH site/ and demo-site/.
Also: Candy Bag art in all 3 spots gets the Jelly balloon (right) + Warble toy duck (left)."""
import os, re, sys, shutil, json
H = os.path.expanduser("~/sebastianmacan")

def sub1(s, old, new, n=1):
    c = s.count(old)
    if c != n: raise SystemExit(f"anchor x{c} (want {n}): {old[:90]!r}")
    return s.replace(old, new)

def edit(path, fn):
    s = open(path).read(); t = fn(s)
    if t != s: open(path, "w").write(t); print("edited", os.path.relpath(path, H))

FREE_BTN = lambda slug, g1, g2, sh, label: (
    f'<a class="dl" style="background:linear-gradient(135deg,{g1},{g2});box-shadow:0 6px 28px {sh};" href="downloads/{slug}">{label}</a>')

JELLY_MAC, JELLY_WIN = "Jelly-v1.1.0-macOS.pkg", "Jelly-v1.1.0-Windows-Setup.exe"
WARB_MAC, WARB_WIN = "Warble-v1.4.0-macOS.pkg", "Warble-v1.4.0-Windows-Setup.exe"

# ---------- index.html ----------
def index(s):
    # Jelly card -> free
    s = sub1(s, '<span class="dl buy" role="button" tabindex="0" data-cart-buy="jelly">Buy Jelly &middot; $15</span>\n      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="jelly">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="jelly">Buy Now</span></div>',
        f'<a class="dl" style="background:linear-gradient(135deg,#ff7ab8,#8fe8c0);box-shadow:0 6px 28px rgba(255,122,184,.30);" href="downloads/{JELLY_MAC}">Download Jelly</a>\n      <div class="cartrow"><span class="cartbtn add" style="pointer-events:none;border-color:rgba(255,216,74,.5);color:#ffd84a;">100% Free &middot; Forever</span></div>')
    s = sub1(s, '<div class="kind">Wobble Machine</div>\n      <h2>JELLY</h2>', '<div class="kind">Free Wobble Machine</div>\n      <h2>JELLY</h2>')
    # Warble card -> free
    s = sub1(s, '<span class="dl buy" role="button" tabindex="0" data-cart-buy="warble">Buy Warble &middot; $15</span>\n      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="warble">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="warble">Buy Now</span></div>',
        f'<a class="dl" style="background:linear-gradient(135deg,#2bb59a,#ff9f43);box-shadow:0 6px 28px rgba(43,181,154,.30);" href="downloads/{WARB_MAC}">Download Warble</a>\n      <div class="cartrow"><span class="cartbtn add" style="pointer-events:none;border-color:rgba(255,216,74,.5);color:#ffd84a;">100% Free &middot; Forever</span></div>')
    s = sub1(s, '<div class="kind">Drunk Songbird Pitch Wobbler</div>\n      <h2>WARBLE</h2>', '<div class="kind">Free Drunk Songbird Pitch Wobbler</div>\n      <h2>WARBLE</h2>')
    # Effects basket card gone
    s = re.sub(r'    <a class="bundle fx-b" href="basket-effects.html">.*?</a>\n(?=    <a class="bundle studio-b")', '', s, count=1, flags=re.S)
    assert 'basket-effects' not in s
    # Cozy basket card gone (folded into Lofi)
    s = re.sub(r'    <a class="bundle cozy-b" href="basket-cozy.html">.*?</a>\n(?=    <a class="bundle chord-b")', '', s, count=1, flags=re.S)
    assert 'basket-cozy' not in s
    # Lofi card
    s = sub1(s, '<img src="img/bundles/lofi_bundle.png?v=5" alt="Lofi Basket: Fireplace, Warble and Honey as wrapped candy in a basket" loading="lazy">',
        '<img src="img/bundles/lofi_bundle.png?v=6" alt="Lofi Basket: Honey and Fireplace as wrapped candy in a basket" loading="lazy">')
    s = sub1(s, '<p class="desc">Fireplace, Warble and Honey. A crackling room, a weird little songbird and smooth tape for the chords. The complete lofi mood.</p>\n        <div class="price">$30</div>',
        '<p class="desc">Honey and Fireplace. Smooth tape for your chords and the cozy room around them. The complete lofi mood.</p>\n        <div class="price">$22</div>')
    # bundles intro
    s = re.sub(r'(<p style="color:var\(--dim\);font-size:14px;max-width:720px;margin-top:6px;">)Eight baskets\..*?</p>',
        r'\1Six baskets. Instruments at $59 and Studio Tools at $35 sort the plugins by what they do, and the Lofi Basket is $22 for Honey and Fireplace. The Chord Basket is Chordsmith plus every MIDI pack at $69, the MIDI Mega Basket packs all 4796 progressions at $49, and the whole Modal Series is just $12.</p>', s, count=1, flags=re.S)
    assert 'Six baskets.' in s
    # Candy bag copy: 3 -> 5
    s = s.replace('<div class="kind">Three free plugins</div>', '<div class="kind">Five free plugins</div>')
    s = sub1(s, '<p class="desc">Chop, Scrap and Orbit. One zip, all three installers. Three plugins, zero dollars.</p>',
        '<p class="desc">Chop, Scrap, Orbit, Jelly and Warble. One zip, all five installers. Five plugins, zero dollars.</p>')
    s = sub1(s, '<div class="meta">Chop &middot; Scrap &middot; Orbit &middot; macOS + Windows</div>', '<div class="meta">Chop &middot; Scrap &middot; Orbit &middot; Jelly &middot; Warble &middot; macOS + Windows</div>')
    s = sub1(s, '<div class="inside">Chop &middot; Scrap &middot; Orbit &middot; one zip, all three installers</div>', '<div class="inside">Chop &middot; Scrap &middot; Orbit &middot; Jelly &middot; Warble &middot; one zip, all five installers</div>')
    s = sub1(s, '/* Candy Bag: the closer. Full width, all three free plugins in one zip. */', '/* Candy Bag: the closer. Full width, all five free plugins in one zip. */')
    # --- Candy Bag art: ad card (c1 c2 c3 + toy duck left, balloon right) ---
    s = sub1(s, '''        <img class="candy c3" src="img/candyad/candy_orbit_yellow.png" alt="">
        <img class="bagfront" src="img/candyad/bag_party.png" alt="">
      </div>''', '''        <img class="candy c3" src="img/candyad/candy_orbit_yellow.png" alt="">
        <img class="toy" src="img/candyad/toy_warble.png" alt="">
        <img class="balloon" src="img/candyad/balloon_jelly.png" alt="">
        <img class="bagfront" src="img/candyad/bag_party.png" alt="">
      </div>''')
    s = sub1(s, '  .card.candyad:hover .candy { animation-duration:1.2s; }',
        '''  .card.candyad .toy { left:-3%; width:27%; bottom:1%; z-index:4; transform-origin:50% 100%; animation:toyrock 3.2s ease-in-out infinite; filter:drop-shadow(0 6px 10px rgba(0,0,0,.3)); }
  .card.candyad .balloon { right:-4%; width:26%; bottom:26%; z-index:4; transform-origin:50% 100%; animation:balloonsway 4.5s ease-in-out infinite; filter:drop-shadow(0 8px 14px rgba(0,0,0,.28)); }
  @keyframes toyrock { 0%,100% { transform:rotate(-4deg); } 50% { transform:rotate(4deg); } }
  @keyframes balloonsway { 0%,100% { transform:translateY(0) rotate(-5deg); } 50% { transform:translateY(-6%) rotate(5deg); } }
  .card.candyad:hover .candy { animation-duration:1.2s; }''')
    s = sub1(s, '  @media (prefers-reduced-motion:reduce) { .card.candyad .candy { animation:none; } }',
        '  @media (prefers-reduced-motion:reduce) { .card.candyad .candy, .card.candyad .toy, .card.candyad .balloon { animation:none; } }')
    # --- Candy Bag art: closer stage ---
    s = sub1(s, '''      <img class="candy cf" src="img/candyad/candy_chop.png" alt="">
      <img class="bagfront" src="img/candyad/bag_party.png" alt="">
    </div></div>''', '''      <img class="candy cf" src="img/candyad/candy_chop.png" alt="">
      <img class="toy" src="img/candyad/toy_warble.png" alt="">
      <img class="balloon" src="img/candyad/balloon_jelly.png" alt="">
      <img class="bagfront" src="img/candyad/bag_party.png" alt="">
    </div></div>''')
    s = sub1(s, '  @media (prefers-reduced-motion:reduce) { .candystage .candy { animation:none; } }',
        '''  .candystage .toy { left:-3%; width:26%; bottom:1%; z-index:4; transform-origin:50% 100%; animation:toyrock 3.2s ease-in-out infinite; filter:drop-shadow(0 6px 10px rgba(0,0,0,.3)); }
  .candystage .balloon { right:-4%; width:25%; bottom:28%; z-index:4; transform-origin:50% 100%; animation:balloonsway 4.5s ease-in-out infinite; filter:drop-shadow(0 8px 14px rgba(0,0,0,.28)); }
  @media (prefers-reduced-motion:reduce) { .candystage .candy, .candystage .toy, .candystage .balloon { animation:none; } }''')
    # title/meta counts stay (12 plugins still 12 plugins)
    return s

# ---------- candy-bag.html ----------
def candy(s):
    s = sub1(s, '<title>Candy Bag | Three Free Plugins | Sebastian Macan</title>', '<title>Candy Bag | Five Free Plugins | Sebastian Macan</title>')
    s = sub1(s, 'content="Candy Bag: Chop, Scrap and Orbit. Three free Sebastian Macan plugins in one zip.', 'content="Candy Bag: Chop, Scrap, Orbit, Jelly and Warble. Five free Sebastian Macan plugins in one zip.')
    s = sub1(s, '<div class="kind">Three free plugins</div>', '<div class="kind">Five free plugins</div>')
    s = sub1(s, '<div class="meta">3 plugins · VST3 + AU · macOS + Windows</div>', '<div class="meta">5 plugins · VST3 + AU · macOS + Windows</div>')
    s = sub1(s, '<div class="meta">Chop &middot; Scrap &middot; Orbit &middot; one zip, all three installers</div>', '<div class="meta">Chop &middot; Scrap &middot; Orbit &middot; Jelly &middot; Warble &middot; one zip, all five installers</div>')
    s = sub1(s, 'Orbit flies your hats around your head. Three Sebastian Macan plugins, free forever.', 'Orbit flies your hats around your head. Jelly makes everything jiggle. Warble makes any sound sing like a weird little bird. Five Sebastian Macan plugins, free forever.')
    s = sub1(s, '<div class="meta">3 installers in one zip. Download once, unzip, done.</div>', '<div class="meta">5 installers in one zip. Download once, unzip, done.</div>')
    s = sub1(s, 'Three plugins, <b>$0</b>.', 'Five plugins, <b>$0</b>.')
    rows = f'''    <div class="item">
      <div class="iinfo">
        <div class="ikind">Wobble Machine</div>
        <div class="iname">Jelly</div>
        <p class="itag">Make everything jiggle. Free forever.</p>
        <a class="rowlink" href="jelly.html">See how it works &rarr;</a>
      </div>
      <div class="iact">
        <div class="freetag">FREE</div>
        <a class="dl idl" href="downloads/{JELLY_MAC}">Mac</a>
        <a class="dl dl-win idl" href="downloads/{JELLY_WIN}">Windows</a>
      </div>
    </div>
    <div class="item">
      <div class="iinfo">
        <div class="ikind">Drunk Songbird Pitch Wobbler</div>
        <div class="iname">Warble</div>
        <p class="itag">Make any sound sing like a weird little bird. Free forever.</p>
        <a class="rowlink" href="warble.html">See how it works &rarr;</a>
      </div>
      <div class="iact">
        <div class="freetag">FREE</div>
        <a class="dl idl" href="downloads/{WARB_MAC}">Mac</a>
        <a class="dl dl-win idl" href="downloads/{WARB_WIN}">Windows</a>
      </div>
    </div>
'''
    s = sub1(s, '''        <a class="dl dl-win idl" href="downloads/Orbit-v1.0-Windows-Setup.exe">Windows</a>
      </div>
    </div>
''', '''        <a class="dl dl-win idl" href="downloads/Orbit-v1.0-Windows-Setup.exe">Windows</a>
      </div>
    </div>
''' + rows)
    # art
    s = sub1(s, '''        <img class="candy cf" src="img/candyad/candy_chop.png" alt="">
        <img class="bagfront" src="img/candyad/bag_party.png" alt="">''', '''        <img class="candy cf" src="img/candyad/candy_chop.png" alt="">
        <img class="toy" src="img/candyad/toy_warble.png" alt="">
        <img class="balloon" src="img/candyad/balloon_jelly.png" alt="">
        <img class="bagfront" src="img/candyad/bag_party.png" alt="">''')
    s = sub1(s, '  @media (prefers-reduced-motion:reduce) { .candystage .candy { animation:none; } }',
        '''  .candystage .toy { left:-1%; width:24%; bottom:1%; z-index:4; transform-origin:50% 100%; animation:toyrock 3.2s ease-in-out infinite; filter:drop-shadow(0 6px 10px rgba(0,0,0,.3)); }
  .candystage .balloon { right:-2%; width:23%; bottom:28%; z-index:4; transform-origin:50% 100%; animation:balloonsway 4.5s ease-in-out infinite; filter:drop-shadow(0 8px 14px rgba(0,0,0,.28)); }
  @keyframes toyrock { 0%,100% { transform:rotate(-4deg); } 50% { transform:rotate(4deg); } }
  @keyframes balloonsway { 0%,100% { transform:translateY(0) rotate(-5deg); } 50% { transform:translateY(-6%) rotate(5deg); } }
  @media (prefers-reduced-motion:reduce) { .candystage .candy, .candystage .toy, .candystage .balloon { animation:none; } }''')
    return s

# ---------- jelly.html / warble.html -> free product pages ----------
def freepage(name, slug, mac, g1, g2, sh):
    def fn(s):
        btn = f'<a class="dl" href="downloads/{mac}">Download {name} Free</a>'
        s = s.replace(f'<span class="dl buy" role="button" tabindex="0" data-cart-buy="{slug}">Buy {name} &middot; $15</span>', btn)
        assert s.count(btn) == 2, s.count(btn)
        s = sub1(s, f'"text": "{name} is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription."',
                    f'"text": "Yes. Enter your email and the download starts right away. Full version, no locked knobs, no trial timer."')
        s = sub1(s, f'"name": "How much is {name}?"', f'"name": "Is {name} really free?"')
        s = sub1(s, f'<div class="knob"><b>How much is {name}?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>',
                    f'<div class="knob"><b>Is {name} really free?</b> Yes. Enter your email and the download starts right away. Full version, no locked knobs, no trial timer.</div>')
        s = s.replace('One purchase covers both platforms.', 'One download covers both platforms.')
        s = re.sub(r'<script src="js/cart.js\?v=[a-z0-9]+" defer></script>\n', '', s, count=1)
        assert 'cart.js' not in s and '$15' not in s, [l for l in s.split('\n') if '$15' in l]
        return s
    return fn

# ---------- basket-lofi.html ----------
def lofi(s):
    s = sub1(s, 'content="Fireplace lays a living room of atmosphere under the beat. Warble makes them sing like a weird little bird. Honey puts the chords on smooth tape. The bedroom lofi mood in four plugins."',
        'content="Honey puts the chords on smooth tape. Fireplace lays a living room of atmosphere under the beat. The bedroom lofi mood in two plugins."')
    s = sub1(s, '<p class="tag">The complete lofi mood. A crackling room, a weird little songbird and smooth tape.</p>', '<p class="tag">The complete lofi mood. Smooth tape for your chords and the cozy room around them.</p>')
    s = sub1(s, 'src="img/bundles/lofi_bundle.png?v=5"', 'src="img/bundles/lofi_bundle.png?v=6"')
    s = sub1(s, '<div class="pricebar"><span class="big">$30</span></div>\n    <div class="meta">3 plugins · VST3 + AU · macOS</div>', '<div class="pricebar"><span class="big">$22</span></div>\n    <div class="meta">2 plugins · VST3 + AU · macOS + Windows</div>')
    s = s.replace('data-cart-buy="lofibasket">Buy Lofi Basket &middot; $30</span>', 'data-cart-buy="lofibasket">Buy Lofi Basket &middot; $22</span>'); assert s.count('Buy Lofi Basket &middot; $22</span>') == 2
    s = sub1(s, '<p class="sub">Fireplace lays a living room of atmosphere under the beat. Warble makes them sing like a weird little bird. Honey puts the chords on smooth tape. The bedroom lofi mood in four plugins.',
        '<p class="sub">Honey puts the chords on smooth tape. Fireplace lays a living room of atmosphere under the beat. The bedroom lofi mood in two plugins.')
    s = re.sub(r'    <div class="item">\n      <div class="iinfo">\n        <div class="ikind">Drunk Songbird Pitch Wobbler</div>\n        <div class="iname">Warble</div>.*?</div>\n    </div>\n', '', s, count=1, flags=re.S)
    assert 'warble' not in s.lower()
    s = sub1(s, '<div class="meta">3 installers in one zip. Download once, unzip, done.</div>', '<div class="meta">2 installers. Download once, install, done.</div>')
    s = sub1(s, "Bought one by one this basket adds up to <b>$45</b>. As a basket it's <b>$30</b>, one-time. 3 items, zero catches.", "Bought one by one this basket adds up to <b>$30</b>. As a basket it's <b>$22</b>, one-time. 2 items, zero catches.")
    return s

# ---------- pricing.html ----------
def pricing(s):
    s = sub1(s, '<tr><td>Warble</td><td>Bird pitch-wobble effect</td><td class="price">$15</td></tr>', '<tr><td>Warble</td><td>Bird pitch-wobble effect</td><td class="price">FREE forever</td></tr>')
    s = sub1(s, '<tr><td>Jelly</td><td>Wobble effect</td><td class="price">$15</td></tr>', '<tr><td>Jelly</td><td>Wobble effect</td><td class="price">FREE forever</td></tr>')
    s = sub1(s, '    <tr><td>Effects Basket</td><td>Jelly, Warble, Gloss and Gremlin, plus Orbit (worth $64)</td><td class="price">$49</td></tr>\n', '')
    s = sub1(s, '    <tr><td>Cozy Basket</td><td>Honey and Fireplace (worth $30)</td><td class="price">$22</td></tr>\n', '')
    s = sub1(s, '<tr><td>Lofi Basket</td><td>Fireplace, Warble and Honey (worth $45)</td><td class="price">$30</td></tr>', '<tr><td>Lofi Basket</td><td>Honey and Fireplace (worth $30)</td><td class="price">$22</td></tr>')
    return s

def sitemap(s):
    s = re.sub(r'  <url><loc>https://sebastianmacan.com/basket-effects.html</loc>[^\n]*\n', '', s)
    s = re.sub(r'  <url><loc>https://sebastianmacan.com/basket-cozy.html</loc>[^\n]*\n', '', s)
    return s

REDIR = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={url}"><link rel="canonical" href="https://sebastianmacan.com/{url}">
<title>Redirecting</title></head><body><a href="{url}">Continue</a></body></html>
'''

for site in ("site", "demo-site"):
    S = f"{H}/{site}"
    if site == "site": edit(f"{S}/index.html", index)   # demo index is nightly-generated, never hand-edited
    edit(f"{S}/candy-bag.html", candy)
    edit(f"{S}/jelly.html", freepage("Jelly", "jelly", JELLY_MAC, "#ff7ab8", "#8fe8c0", "rgba(255,122,184,.30)"))
    edit(f"{S}/warble.html", freepage("Warble", "warble", WARB_MAC, "#2bb59a", "#ff9f43", "rgba(43,181,154,.30)"))
    edit(f"{S}/basket-lofi.html", lofi)
    edit(f"{S}/pricing.html", pricing)
    if os.path.exists(f"{S}/sitemap.xml"): edit(f"{S}/sitemap.xml", sitemap)
    for old, new in (("basket-effects.html", "/#bundles"), ("basket-cozy.html", "basket-lofi.html")):
        p = f"{S}/{old}"
        if os.path.exists(p):
            open(p, "w").write(REDIR.format(url=new)); print("redirect", site, old, "->", new)
    # lofi art = the Honey+Fireplace basket (cozy art, no text in it)
    shutil.copy2(f"{S}/img/bundles/cozy_bundle.png", f"{S}/img/bundles/lofi_bundle.png")
    # cart.js version bump everywhere in this tree
    import glob
    n = 0
    for f in glob.glob(f"{S}/*.html") + glob.glob(f"{S}/learn/*.html"):
        t = open(f).read(); u = re.sub(r'cart\.js\?v=[a-z0-9]+', 'cart.js?v=free5', t)
        if u != t: open(f, "w").write(u); n += 1
    print(site, "cart.js bump on", n, "pages")
print("OK")
