#!/usr/bin/env python3
"""Nov 18 2026 (Alex): all five gremlins are FREE. Smear, Stutter, Twitch join Chop + Scrap; the Gremlin Basket is a free download.
Also: homepage Free section lists every free plugin (adds Smear, Stutter, Twitch, Jelly, Warble), Gremlin card pill says CLICK.
Site tree only (demo-site is regenerated nightly from it). Every edit is anchored and counted; files are written once at the end.
Paddle side: paddle/gremlins_free_20261118.py (run first).  Usage: gremlins_free_20261118.py [--dry]
"""
import os, re, sys, json, glob, shutil, subprocess
H = os.path.join(os.path.expanduser("~"), "sebastianmacan"); S = os.path.join(H, "site"); DRY = "--dry" in sys.argv
OUT = {}
def rd(name): return OUT.get(name) or open(os.path.join(S, name), encoding="utf-8").read()
def sub(s, old, new, n=1):
    c = s.count(old)
    if c != n: raise SystemExit("anchor x%d (want %d): %r" % (c, n, old[:110]))
    return s.replace(old, new)

G = {  # slug: (Name, mac, win, g1, g2, shadow, kind, tagline, ui version)
    "smear":   ("Smear",   "Smear-v1.0.1-macOS.pkg",   "Smear-v1.0.1-Windows-Setup.exe",   "#9a6bff", "#44e0c8", "rgba(154,107,255,.30)", "Granular Smear", "It's a reverb.", "1.0.1"),
    "stutter": ("Stutter", "Stutter-v2.0.3-macOS.pkg", "Stutter-v2.0.3-Windows-Setup.exe", "#ff2ea6", "#ff7ad1", "rgba(255,46,166,.30)", "Beat Repeat", "Trips over your beat.", "2.0.3"),
    "twitch":  ("Twitch",  "Twitch-v1.1.1-macOS.pkg",  "Twitch-v1.1.1-Windows-Setup.exe",  "#3cdcff", "#9aefff", "rgba(60,220,255,.30)", "Per-Step Glitch Rack", "The mad scientist of the bunch.", "1.1.1"),
}
FREEPILL = '<div class="cartrow"><span class="cartbtn add" style="pointer-events:none;border-color:rgba(255,216,74,.5);color:#ffd84a;">100% Free &middot; Forever</span></div>'

# ---------------- index.html ----------------
s = rd("index.html")
for k, (N, mac, win, g1, g2, sh, kind, tag, uiv) in G.items():
    s = sub(s, '<span class="dl buy" style="background:linear-gradient(135deg,%s,%s);box-shadow:0 6px 28px %s;" role="button" tabindex="0" data-cart-buy="%s">Buy %s &middot; $15</span>\n      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="%s">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="%s">Buy Now</span></div>' % (g1, g2, sh, k, N, k, k),
            '<a class="dl" style="background:linear-gradient(135deg,%s,%s);box-shadow:0 6px 28px %s;" href="downloads/%s">Download %s</a>\n      %s' % (g1, g2, sh, mac, N, FREEPILL))
    s = sub(s, '<div class="card %s">\n      <span class="new">NEW</span>\n      <div class="kind">%s</div>' % (k, kind), '<div class="card %s">\n      <span class="new">NEW</span>\n      <div class="kind">Free %s</div>' % (k, kind))
# Gremlin card pill
s = sub(s, '<div class="card gremlinad full" id="gremlinad" data-goto="basket-gremlin.html">', '<div class="card gremlinad full" id="gremlinad" data-goto="basket-gremlin.html">')
i = s.index('<div class="card gremlinad full"'); j = s.index("</div>\n    </div>", i) if False else s.index('<a class="golink"', i)
blk = s[i:j]; assert blk.count('<span class="pill">BASKET</span>') == 1
s = s[:i] + blk.replace('<span class="pill">BASKET</span>', '<span class="pill">CLICK</span>') + s[j:]
# baskets intro + Gremlin Basket card
s = sub(s, "the Gremlin Basket is $35 for Smear, Stutter, Twitch, Chop and Scrap,", "the Gremlin Basket is free with Smear, Stutter, Twitch, Chop and Scrap,")
s = sub(s, '''        <div class="price">$35</div>
        <span class="dl bopen" style="background:linear-gradient(135deg,#ff8ad8,#6ec8ff);">Open the basket</span>
        <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="gremlinbasket">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="gremlinbasket">Buy Now</span></div>''',
'''        <div class="price"><span class="freebie">FREE</span></div>
        <span class="dl bopen" style="background:linear-gradient(135deg,#ff8ad8,#6ec8ff);">Open the basket</span>
        %s''' % FREEPILL)
# Free section: every free plugin. Chop, Scrap, Smear, Stutter, Twitch (the gremlins), Jelly, Warble, Orbit.
def freecard(k, kind, N, p, g1, g2, sh, poster, loop, mac):
    return '''    <div class="freecard %s">
      <span class="pill">FREE</span>
      <div class="kind">%s</div>
      <h3 style="background:linear-gradient(135deg,%s,%s);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;">%s</h3>
      <p>%s</p>
      <div class="shot"><video autoplay muted loop playsinline preload="metadata" poster="%s"><source src="%s" type="video/mp4"></video></div>
      <a class="dl" style="background:linear-gradient(135deg,%s,%s);box-shadow:0 6px 22px %s;" href="downloads/%s">Download %s</a>
      <a class="more" href="%s.html">See how it works &rarr;</a>
    </div>
''' % (k, kind, g1, g2, N.upper(), p, poster, loop, g1, g2, sh.replace(".30)", ".28)"), mac, N.upper(), k)
def media(k):  # poster + loop exactly as that plugin's own shop card uses them
    m = re.search(r'<div class="card %s">.*?poster="([^"]+)"><source src="([^"]+)"' % k, s, re.S); assert m, k; return m.group(1), m.group(2)
new = ""
for k, (N, mac, win, g1, g2, sh, kind, tag, uiv) in G.items():
    po, lo = media(k); new += freecard(k, "Free " + kind, N, tag, g1, g2, sh, po, lo, mac)
po, lo = media("jelly");  new += freecard("jelly", "Free Wobble Machine", "Jelly", "Make everything jiggle.", "#ff7ab8", "#8fe8c0", "rgba(255,122,184,.30)", po, lo, "Jelly-v1.1.0-macOS.pkg")
po, lo = media("warble"); new += freecard("warble", "Free Drunk Songbird Wobbler", "Warble", "Make any sound sing like a weird little bird.", "#2bb59a", "#ff9f43", "rgba(43,181,154,.30)", po, lo, "Warble-v1.4.0-macOS.pkg")
a = s.index('    <div class="freecard orbit">'); assert s.count('    <div class="freecard orbit">') == 1
s = s[:a] + new + s[a:]
assert s.count('<div class="freecard ') == 8
s = sub(s, "  .freegrid { display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:14px; margin-top:10px; }",
           "  .freegrid { display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; margin-top:10px; }")
assert "data-cart-buy=\"smear\"" not in s and "gremlinbasket" not in s and "$15</span>" not in s.split('id="studio"')[0].split('id="effects"')[-1]
OUT["index.html"] = s

# ---------------- smear / stutter / twitch pages ----------------
for k, (N, mac, win, g1, g2, sh, kind, tag, uiv) in G.items():
    s = rd(k + ".html")
    s = sub(s, '"price": "15",', '"price": "0",')
    s = sub(s, '"name": "How much is %s?"' % N, '"name": "Is %s really free?"' % N)
    s = sub(s, '"text": "$15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription."', '"text": "Yes. Enter your email and the download starts right away. Full version, no locked knobs, no trial timer."')
    s = sub(s, '<b>How much is %s?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.' % N, '<b>Is %s really free?</b> Yes. Enter your email and the download starts right away. Full version, no locked knobs, no trial timer.' % N)
    s = sub(s, "One purchase covers both platforms.", "One download covers both platforms.", 2)
    btn = '<span class="dl buy" role="button" tabindex="0" data-cart-buy="%s">Buy %s &middot; $15</span>' % (k, N)
    assert s.count(btn) == 2
    s = s.replace('      ' + btn, '      <a class="dl" href="downloads/%s">Download %s Free &middot; macOS</a>\n      <a class="dl dl-win" href="downloads/%s">Download %s Free &middot; Windows</a>' % (mac, N, win, N))
    s = s.replace('    ' + btn, '    <a class="dl" href="downloads/%s">Download %s Free &middot; macOS</a>\n    <a class="dl dl-win" href="downloads/%s">Download %s Free &middot; Windows</a>' % (mac, N, win, N))
    s = sub(s, '<script src="js/cart.js?v=toy2" defer></script>\n', '')
    assert "$15" not in s and "data-cart" not in s and s.count("downloads/") == 4, k
    OUT[k + ".html"] = s

# ---------------- basket-gremlin.html: a free bag, same pattern as candy-bag.html ----------------
s = rd("basket-gremlin.html")
DLROW = '<div class="dlrow"><a class="dl" href="downloads/GremlinBasket-macOS.zip">Grab the basket &middot; Mac</a><a class="dl dl-win" href="downloads/GremlinBasket-Windows.zip">Grab the basket &middot; Windows</a></div>'
s = sub(s, '<div class="pricebar"><span class="big">$35</span></div>', '<div class="pricebar"><span class="big freebie">FREE</span></div>')
s = sub(s, '<div class="cta" style="margin-top:22px;"><span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlinbasket">Buy Gremlin Basket &middot; $35</span><div class="cartrow" style="justify-content:center;"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="gremlinbasket">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="gremlinbasket">Buy Now</span></div></div>',
        '<div class="cta" style="margin-top:22px;">' + DLROW + '<div class="meta">Smear &middot; Stutter &middot; Twitch &middot; Chop &middot; Scrap &middot; one zip, all five installers</div></div>')
s = sub(s, " Chop and Scrap are free forever, and in the basket anyway. Every item below is sold on its own too, or take the whole basket at once.</p>",
           " Five Sebastian Macan plugins, free forever. Grab them one by one below, or take the whole basket in a single zip.</p>")
ROWS = dict(G); ROWS["chop"] = ("Chop", "Chop-v1.1.3-macOS.pkg", "Chop-v1.1.3-Windows-Setup.exe"); ROWS["scrap"] = ("Scrap", "Scrap-v1.0.2-macOS.pkg", "Scrap-v1.0.2-Windows-Setup.exe")
for k in ("smear", "stutter", "twitch"):
    N = ROWS[k][0]
    s = sub(s, '''        <div class="iprice">$15</div>
        <span class="dl buy idl" role="button" tabindex="0" data-cart-buy="%s">Buy %s &middot; $15</span>''' % (k, N),
'''        <div class="freetag">FREE</div>
        <a class="dl idl" href="downloads/%s">Mac</a>
        <a class="dl dl-win idl" href="downloads/%s">Windows</a>''' % (ROWS[k][1], ROWS[k][2]))
for k in ("chop", "scrap"):
    s = sub(s, '''        <div class="iprice"><span class="freetag">FREE forever</span></div>
        <a class="dl idl" href="%s.html">Get it free</a>''' % k,
'''        <div class="freetag">FREE</div>
        <a class="dl idl" href="downloads/%s">Mac</a>
        <a class="dl dl-win idl" href="downloads/%s">Windows</a>''' % (ROWS[k][1], ROWS[k][2]))
s = sub(s, '<div class="cta"><span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlinbasket">Buy Gremlin Basket &middot; $35</span><div class="cartrow" style="justify-content:center;"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="gremlinbasket">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="gremlinbasket">Buy Now</span></div><div class="meta">5 plugins in one email. Download, install, done.</div></div>',
        '<div class="cta">' + DLROW + '<div class="meta">5 installers in one zip. Download once, unzip, done.</div></div>')
s = sub(s, "    Bought one by one this basket adds up to <b>$45</b>. As a basket it's <b>$35</b>, one-time. 5 items, zero catches.", "    Five plugins, <b>$0</b>. No account, no catches. Unzip, install, make noise.")
s = sub(s, "  .mathbox b { color:var(--txt); }\n", "  .mathbox b { color:var(--txt); }\n  .dl.dl-win { background:none; border:1px solid var(--g1); color:var(--g1); box-shadow:none; }\n  .dlrow { display:flex; gap:12px; justify-content:center; flex-wrap:wrap; }\n  .freetag { color:var(--g1); }\n  .freebie { background:linear-gradient(135deg,var(--g1),var(--g2)); -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; }\n")
s = sub(s, '<script src="js/cart.js?v=toy2" defer></script>\n', '')
assert "$" not in re.sub(r"<style>.*?</style>", "", s, flags=re.S) .replace("<b>$0</b>", "") and "data-cart" not in s and s.count("downloads/") == 14
OUT["basket-gremlin.html"] = s

# ---------------- pricing.html, chop.html, scrap.html ----------------
s = rd("pricing.html")
for N in ("Smear", "Stutter", "Twitch"):
    m = re.search(r'(<tr><td>%s</td><td>[^<]*</td><td class="price">)\$15(</td></tr>)' % N, s); assert m
    s = s.replace(m.group(0), m.group(1) + "FREE forever" + m.group(2))
s = sub(s, '<tr><td>Gremlin Basket</td><td>Smear, Stutter and Twitch, plus Chop and Scrap, which are free forever (worth $45)</td><td class="price">$35</td></tr>',
           '<tr><td>Gremlin Basket</td><td>Smear, Stutter, Twitch, Chop and Scrap in one zip</td><td class="price">FREE forever</td></tr>')
s = sub(s, "Orbit and Chop are free.</p>", "Orbit, Jelly, Warble and the five gremlins (Smear, Stutter, Twitch, Chop and Scrap) are free.</p>")
s = sub(s, '    <tr><td>Chop</td><td>Free rhythm chopper</td><td class="price">FREE forever</td></tr>\n', '    <tr><td>Chop</td><td>Free rhythm chopper</td><td class="price">FREE forever</td></tr>\n    <tr><td>Scrap</td><td>Free glitch repeater</td><td class="price">FREE forever</td></tr>\n')
OUT["pricing.html"] = s
s = rd("chop.html")
s = sub(s, "with the three $15 boxes. Each one does one thing; this one happens to be free. Nothing held back.", "with all three. Each one does one thing, and all four are free. Nothing held back.")
s = sub(s, "is the per-step glitch rack with a draw pad. $15 each.</p>", "is the per-step glitch rack with a draw pad. All three are free too.</p>")
OUT["chop.html"] = s
s = rd("scrap.html")
s = sub(s, '<a href="chop.html">Chop</a> is the other free one: a tempo-synced gate', '<a href="chop.html">Chop</a> is free too: a tempo-synced gate')
s = sub(s, "are the $15 boxes next to it.</p>", "are the free boxes next to it.</p>")
OUT["scrap.html"] = s

# ---------------- cart.js ----------------
p = os.path.join(S, "js", "cart.js"); c = open(p).read()
for k, N in (("smear", "Smear"), ("stutter", "Stutter"), ("twitch", "Twitch")):
    c, n = re.subn(r"^\s*%s:\s*\{ name: '%s'.*\n" % (k, N), "", c, flags=re.M); assert n == 1, k
c, n = re.subn(r",\n\s*gremlinbasket:\s*\{ name: 'Gremlin Basket'.*\n", "\n", c); assert n == 1
c, n = re.subn(r"^\s*gremlinbasket:\s*\{ page: 'basket-gremlin.html'.*\n", "", c, flags=re.M); assert n == 1
assert not re.search(r"smear|stutter|twitch|gremlin", c, re.I), re.findall(r".*(?:smear|stutter|twitch|gremlin).*", c, re.I)[:3]
# ---------------- email-gate.js ----------------
pg = os.path.join(S, "js", "email-gate.js"); g = open(pg).read()
g = sub(g, "var FREE = { candybag: 1, chop: 1, scrap: 1, orbit: 1, jelly: 1, warble: 1 };", "var FREE = { candybag: 1, chop: 1, scrap: 1, orbit: 1, jelly: 1, warble: 1, smear: 1, stutter: 1, twitch: 1, gremlinbasket: 1 };")
g = sub(g, '    candybag: { g1: "#4cc2ff", g2: "#5b7cff", shadow: "rgba(76,194,255,.30)", label: "Candy Bag" },\n',
           '    candybag: { g1: "#4cc2ff", g2: "#5b7cff", shadow: "rgba(76,194,255,.30)", label: "Candy Bag" },\n'
           '    gremlinbasket: { g1: "#ff8ad8", g2: "#6ec8ff", shadow: "rgba(255,138,216,.30)", label: "Gremlin Basket" },\n'
           + "".join('    %s: { g1: "%s", g2: "%s", shadow: "%s" },\n' % (k, v[3], v[4], v[5]) for k, v in G.items() if ("\n    %s:" % k) not in g))

if DRY: print("dry ok:", sorted(OUT)); sys.exit(0)

# backups of every page as it was while these were paid
B = os.path.join(H, "marketing", "archive", "before_gremlins_free_20261118"); os.makedirs(B, exist_ok=True)
for name in list(OUT) + ["js/cart.js", "js/email-gate.js"]:
    if not os.path.exists(os.path.join(B, os.path.basename(name))): shutil.copy2(os.path.join(S, name), os.path.join(B, os.path.basename(name)))
for name, t in OUT.items(): open(os.path.join(S, name), "w", encoding="utf-8").write(t)
open(p, "w").write(c); open(pg, "w").write(g)
n = 0
for f in glob.glob(S + "/*.html") + glob.glob(S + "/learn/*.html"):
    t = open(f, encoding="utf-8").read(); u = re.sub(r"email-gate\.js\?v=[a-z0-9]+", "email-gate.js?v=free8", t); u = re.sub(r"cart\.js\?v=[a-z0-9]+", "cart.js?v=free8", u)
    if u != t: open(f, "w", encoding="utf-8").write(u); n += 1
print("pages written:", sorted(OUT), "| version bumps:", n)

# installers (byte-identical to the delivery gold files) + basket zips
D = os.path.join(S, "downloads")
for k, v in G.items():
    shutil.copy2(os.path.join(H, "delivery", "files", v[1]), os.path.join(D, v[1]))
    shutil.copy2(os.path.join(H, "delivery", "files", v[2].replace("-Windows-Setup.exe", "-Windows.exe")), os.path.join(D, v[2]))
for z, idx in (("GremlinBasket-macOS.zip", 1), ("GremlinBasket-Windows.zip", 2)):
    if os.path.exists(os.path.join(D, z)): os.remove(os.path.join(D, z))
    subprocess.run(["zip", "-q", "-X", z] + [ROWS[k][idx] for k in ("smear", "stutter", "twitch", "chop", "scrap")], cwd=D, check=True)
    print(subprocess.run(["unzip", "-l", z], cwd=D, capture_output=True, text=True).stdout)

# delivery: free products (library cards + welcome mail)
fp = os.path.join(H, "delivery", "free_products.json"); d = json.load(open(fp)); U = "https://sebastianmacan.com/"
for k, v in G.items():
    d[k] = {"name": v[0], "kind": v[6], "slug": k, "g1": v[3], "g2": v[4], "img": U + "img/ui/%s.png" % k, "files": [["macOS", U + "downloads/" + v[1]], ["Windows", U + "downloads/" + v[2]]]}
d["gremlinbasket"] = {"name": "Gremlin Basket", "kind": "Smear \u00b7 Stutter \u00b7 Twitch \u00b7 Chop \u00b7 Scrap \u00b7 five free plugins", "slug": "gremlinbasket", "g1": "#ff8ad8", "g2": "#6ec8ff",
                      "img": U + "img/gremlinad/shop.jpg", "files": [["macOS", U + "downloads/GremlinBasket-macOS.zip"], ["Windows", U + "downloads/GremlinBasket-Windows.zip"]]}
json.dump(d, open(fp, "w"), indent=1); print("free_products:", list(d))
