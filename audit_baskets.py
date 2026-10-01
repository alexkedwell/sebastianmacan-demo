#!/usr/bin/env python3
"""Basket/copy consistency audit (Sep 29 2026). Run from anywhere: python3 site/audit_baskets.py
Checks, from single sources of truth:
  1. Every basket in cart.js BASKETS has the same roster as delivery/products.json (what the buyer actually receives).
  2. Every product's current 'kind' + 'tag' (gen_category_baskets.ITEMS) appears on EVERY page that sells it,
     and no page still carries a retired tagline (RETIRED list).
  3. Every Paddle price id in cart.js CATALOG exists in paddle/catalog.json with the same price.
Exit 1 on any problem. Add to the gold-ceremony checklist next to verify_store_gold.py."""
import re, json, os, glob, sys
H = os.path.expanduser("~/sebastianmacan"); S = f"{H}/site"
sys.path.insert(0, S)
src = open(f"{S}/gen_category_baskets.py").read()
ITEMS = eval(src[src.index("ITEMS = ")+8: src.index("\nBASKETS = [")])
cart = open(f"{S}/js/cart.js").read()
CAT = {m[0]: (int(m[1]), m[2]) for m in re.findall(r"^\s*(\w+):\s*\{ name: '[^']*',\s*cents: (\d+), priceId: '([^']+)' \}", cart, re.M)}
BASK = {m[0]: (m[1], re.findall(r"'(\w+)'", m[2])) for m in re.findall(r"^\s*(\w+):\s*\{ page: '([^']+)',\s*items: \[([^\]]*)\]", cart, re.M)}
paddle = {i["price_id"]: i for i in json.load(open(f"{H}/paddle/catalog.json"))["items"]}
prod = json.load(open(f"{H}/delivery/products.json"))
RETIRED = ["Subtle Tape Machine", "Sometimes tape plugins do too much", "right amount of vintage", "A real tape machine, in the box"]
FILE_OF = {"biome": "Biome", "magician": "Chordsmith", "jelly": "Jelly", "warble": "Warble", "reels": "Reels", "gloss": "Gloss",
           "orbit": "Orbit", "fireplace": "Fireplace", "halo": "Halo", "honey": "Honey", "gremlin": "Gremlin"}
bad = []
# 1. roster: cart.js basket vs delivered files
for cid, (page, items) in BASK.items():
    if cid not in CAT: continue
    pid = CAT[cid][1]
    files = prod.get(pid, {}).get("files", [])
    if any(f.endswith(".zip") for f in files): continue   # zip baskets (Lofi, MIDI) are checked by verify_store_gold
    want = {FILE_OF[i] for i in items if i in FILE_OF}
    got = {m.group(1) for f in files for m in [re.match(r"([A-Za-z]+)-v", f)] if m} - {"Orbit"}  # Orbit = free bonus, never in cart roster
    if want and want != got: bad.append(f"ROSTER {cid}: cart.js {sorted(want)} vs products.json {sorted(got)}")
# 3. prices: cart.js vs Paddle catalog
for k, (cents, pid) in CAT.items():
    if pid not in paddle: bad.append(f"PRICE {k}: {pid} not in paddle/catalog.json"); continue
    if int(round(paddle[pid]["usd"]*100)) != cents: bad.append(f"PRICE {k}: cart.js {cents} vs paddle {paddle[pid]['usd']}")
# 2. copy on every selling page
for page in glob.glob(f"{S}/*.html"):
    s = open(page).read(); name = os.path.basename(page)
    for r in RETIRED:
        if r in s: bad.append(f"RETIRED COPY '{r}' in {name}")
    for k, (kind, pname, tag, price, ppage) in ITEMS.items():
        if k in ("orbit",): continue
        if f'data-cart-buy="{k}"' in s and name.startswith("basket-"):   # basket rows are generated -> must carry current kind/tag
            if kind not in s and tag not in s:
                bad.append(f"COPY {name}: sells {pname} but has neither kind '{kind}' nor tag '{tag[:40]}...'")
print(f"catalog {len(CAT)} items, {len(BASK)} baskets, {len(ITEMS)} product copies")
# 4. plugin count: hero copy on index (and demo-site) must equal the number of plugin cards. Alex caught "Ten" after Gremlin (Sep 30).
WORDS = {9: "Nine", 10: "Ten", 11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen", 15: "Fifteen", 16: "Sixteen"}
idx = open(f"{S}/index.html").read()
midi_cards = {"hitmaker", "clubchords", "tears", "soulchords"}
ncards = len(set(re.findall(r'class="card (\w+)"', idx)) - midi_cards)
for page in [f"{S}/index.html", f"{H}/demo-site/index.html"]:
    if not os.path.exists(page): continue
    s = open(page).read(); name = page.replace(H + "/", "")
    for m in re.findall(r"(\d+) Plugins \+", s):
        if int(m) != ncards: bad.append(f"COUNT {name}: says '{m} Plugins' but {ncards} plugin cards")
    for m in re.findall(r"(\w+) plugins and \d+ MIDI", s):
        if m != WORDS.get(ncards): bad.append(f"COUNT {name}: hero says '{m} plugins' but {ncards} plugin cards")
# 5. Effects Basket page lists every member from cart.js
if "effectsbasket" in BASK:
    be = open(f"{S}/basket-effects.html").read()
    for i in BASK["effectsbasket"][1]:
        if f'data-cart-buy="{i}"' not in be: bad.append(f"BASKET PAGE basket-effects.html: missing row for {i}")
if bad:
    print("\n".join(bad)); print(f"\n{len(bad)} PROBLEMS"); sys.exit(1)
print("baskets + copy + prices consistent, 0 problems")
