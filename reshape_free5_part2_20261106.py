#!/usr/bin/env python3
"""Part 2 of the Nov 6 reshape: cart.js + email-gate + audit/gen scripts + delivery library + free downloads/zips."""
import os, re, json, shutil, subprocess, glob
H = os.path.expanduser("~/sebastianmacan")
def sub1(s, old, new):
    assert s.count(old) == 1, (s.count(old), old[:80]); return s.replace(old, new)

import sys
for site in sys.argv[1:] or ("site", "demo-site"):
    S = f"{H}/{site}"
    # cart.js: drop Jelly/Warble/Effects/Cozy from CATALOG+BASKETS (keys gone -> cached carts drop them), Lofi $22 Honey+Fireplace
    p = f"{S}/js/cart.js"; s = open(p).read()
    s = re.sub(r"^\s*jelly:\s*\{ name: 'Jelly'.*\n", "", s, flags=re.M)
    s = re.sub(r"^\s*warble:\s*\{ name: 'Warble'.*\n", "", s, flags=re.M)
    s = re.sub(r"^\s*effectsbasket:\s*\{ name: 'Effects Basket'.*\n", "", s, flags=re.M)
    s = re.sub(r"^\s*effectsbasket:\s*\{ page: 'basket-effects.html'.*\n", "", s, flags=re.M)
    s = re.sub(r"^\s*cozy:\s*\{ page: 'basket-cozy.html'.*\n", "", s, flags=re.M)
    s = re.sub(r"^(\s*lofibasket:\s*\{ name: 'Lofi Basket',\s*cents: )3000", r"\g<1>2200", s, flags=re.M)
    s = re.sub(r"(lofibasket:\s*\{ page: 'basket-lofi.html',\s*items: \[)[^\]]*\]", r"\1'fireplace', 'honey']", s); assert "items: ['fireplace', 'honey']" in s
    # cozy CATALOG line was last entry (no trailing comma) -> remove it and fix the comma on the new last line
    s = re.sub(r",\n\s*cozy:\s*\{ name: 'Cozy Basket'.*\n", "\n", s, flags=re.M)
    for k in ("jelly:", "warble:", "effectsbasket", "cozy"):
        assert not re.search(r"^\s*" + re.escape(k) + r"\s*\{", s, re.M), k
    assert "cents: 2200, priceId: 'pri_01m1nckxzp0m01qh26zs7qq99t'" in s
    open(p, "w").write(s)
    # email-gate: FREE set + candy bag covers jelly/warble (welcome mail), + ACCENT for warble
    p = f"{S}/js/email-gate.js"; s = open(p).read()
    s = s.replace("var FREE = { candybag: 1, chop: 1, scrap: 1, orbit: 1 };", "var FREE = { candybag: 1, chop: 1, scrap: 1, orbit: 1, jelly: 1, warble: 1 };")  # demo gate is an older build without FREE
    if "warble:" not in s:
        s = sub1(s, '    jelly:  { g1: "#ff7ab8", g2: "#8fe8c0", shadow: "rgba(255,122,184,.30)" },\n',
                    '    jelly:  { g1: "#ff7ab8", g2: "#8fe8c0", shadow: "rgba(255,122,184,.30)" },\n    warble: { g1: "#2bb59a", g2: "#ff9f43", shadow: "rgba(43,181,154,.30)" },\n')
    open(p, "w").write(s)
    for f in glob.glob(f"{S}/*.html") + glob.glob(f"{S}/learn/*.html"):
        t = open(f).read(); u = re.sub(r'email-gate\.js\?v=[a-z0-9]+', 'email-gate.js?v=free5', t)
        if u != t: open(f, "w").write(u)
    # free installers (byte-identical to delivery gold files) + rebuilt bag zips
    D = f"{S}/downloads"
    for src, dst in (("Jelly-v1.1.0-macOS.pkg", "Jelly-v1.1.0-macOS.pkg"), ("Jelly-v1.1.0-Windows.exe", "Jelly-v1.1.0-Windows-Setup.exe"),
                     ("Warble-v1.4.0-macOS.pkg", "Warble-v1.4.0-macOS.pkg"), ("Warble-v1.4.0-Windows.exe", "Warble-v1.4.0-Windows-Setup.exe")):
        shutil.copy2(f"{H}/delivery/files/{src}", f"{D}/{dst}")
    for zipname, files in (("CandyBag-macOS.zip", ["Chop-v1.1.1-macOS.pkg", "Scrap-v1.0.1-macOS.pkg", "Orbit-v1.0-macOS.pkg", "Jelly-v1.1.0-macOS.pkg", "Warble-v1.4.0-macOS.pkg"]),
                           ("CandyBag-Windows.zip", ["Chop-v1.1.1-Windows-Setup.exe", "Scrap-v1.0.1-Windows-Setup.exe", "Orbit-v1.0-Windows-Setup.exe", "Jelly-v1.1.0-Windows-Setup.exe", "Warble-v1.4.0-Windows-Setup.exe"])):
        os.remove(f"{D}/{zipname}")
        subprocess.run(["zip", "-q", "-X", zipname] + files, cwd=D, check=True)
    print(site, "cart/gate/downloads done")

S = f"{H}/site"
# audit_baskets.py: Jelly/Warble are no longer sellable singles; effects branch harmless (keyed on BASK)
# gen_category_baskets.py: drop the effects basket definition so nobody regenerates it
p = f"{S}/gen_category_baskets.py"; s = open(p).read()
s = re.sub(r'  dict\(file="basket-effects.html".*?\),\n(?=  dict\()', '', s, count=1, flags=re.S)
assert 'basket-effects' not in s; open(p, "w").write(s)

# delivery: free products (library cards + welcome mail), library product map
p = f"{H}/delivery/free_products.json"; d = json.load(open(p))
d["candybag"]["kind"] = "Chop \u00b7 Scrap \u00b7 Orbit \u00b7 Jelly \u00b7 Warble \u00b7 five free plugins"
d["jelly"] = {"name": "Jelly", "kind": "Wobble", "slug": "jelly", "g1": "#ff7ab8", "g2": "#8fe8c0", "img": "https://sebastianmacan.com/img/ui/jelly.png",
              "files": [["macOS", "https://sebastianmacan.com/downloads/Jelly-v1.1.0-macOS.pkg"], ["Windows", "https://sebastianmacan.com/downloads/Jelly-v1.1.0-Windows-Setup.exe"]]}
d["warble"] = {"name": "Warble", "kind": "Pitch Wobble", "slug": "warble", "g1": "#2bb59a", "g2": "#ff9f43", "img": "https://sebastianmacan.com/img/ui/warble.png",
               "files": [["macOS", "https://sebastianmacan.com/downloads/Warble-v1.4.0-macOS.pkg"], ["Windows", "https://sebastianmacan.com/downloads/Warble-v1.4.0-Windows-Setup.exe"]]}
json.dump(d, open(p, "w"), indent=1)
p = f"{H}/delivery/gen_library_products.py"; s = open(p).read()
s = sub1(s, ' "Effects Basket": ("basket-effects.html", "Jelly · Warble · Gloss · Gremlin · Orbit", "gremlin.png", []),\n', '')
s = sub1(s, ' "Cozy Basket": ("basket-cozy.html", "Honey + Fireplace", "fireplace.png", []),\n', '')
s = sub1(s, ' "Lofi Basket": ("basket-lofi.html", "The lofi plugins", "honey_cassette.png", []),', ' "Lofi Basket": ("basket-lofi.html", "Honey + Fireplace", "honey_cassette.png", []),')
s = sub1(s, 'UNSOLD = {"Halo", "Reels", "Taffy", "Lofi Basket + Mastering", "Tape Basket", "Tape Room Basket"}',
            'UNSOLD = {"Halo", "Reels", "Taffy", "Lofi Basket + Mastering", "Tape Basket", "Tape Room Basket", "Effects Basket", "Cozy Basket"}')
open(p, "w").write(s)
print("OK")
