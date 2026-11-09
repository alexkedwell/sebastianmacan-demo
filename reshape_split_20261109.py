#!/usr/bin/env python3
"""Site restructure for the Gremlin split (Nov 9 2026). Idempotent. Run from ~/sebastianmacan/site.
Gremlin card/css/cart/pricing/sitemap out; Smear / Stutter / Twitch cards + cart rows + pricing rows + sitemap in.
Copy for the Chop card/page: drop the Gremlin lineage sentence."""
import re, os, json
S = os.path.dirname(os.path.abspath(__file__))
cat = {i["product"]: i for i in json.load(open(f"{S}/../paddle/catalog.json"))["items"]}
PRI = {k: cat[k.capitalize()]["price_id"] for k in ("smear", "stutter", "twitch")}

def rw(name, fn):
    p = f"{S}/{name}"; s = open(p).read(); t = fn(s)
    if t != s: open(p, "w").write(t); print("updated", name)
    else: print("unchanged", name)

# ---------------- index.html ----------------
CARDS = {
 "smear": dict(NAME="SMEAR", Name="Smear", ver="1.0.0", kind="Granular Smear", g1="#9a6bff", g2="#44e0c8", rgb="154,107,255",
   tag="Melts anything into a cloud.",
   desc="Grains of your sound, some thrown up an octave, smudged and poured into a plate reverb with a tail up to 14 seconds. SHIMMER climbs, FREEZE holds it forever. Melty drips along."),
 "stutter": dict(NAME="STUTTER", Name="Stutter", ver="2.0.0", kind="Beat Repeat", g1="#ff2ea6", g2="#ff7ad1", rgb="255,46,166",
   tag="Repeats it until it is a new idea.",
   desc="Buffer repeats on a dice roll. RATE from whole bars to 1/32 or FREE in milliseconds, REPEATS, RAMP, REVERSE, true PITCH, TAPE, SCATTER, HOLD and a patch bay you can click. Jitter twitches with every burst."),
 "twitch": dict(NAME="TWITCH", Name="Twitch", ver="1.0.0", kind="Per-Step Glitch Rack", g1="#3cdcff", g2="#9aefff", rgb="60,220,255",
   tag="Twelve effects. One grid. Draw the rest.",
   desc="GATE, CRUSH, WARP, COMB, GRAIN, GLITCH, FORMANT, RING and CHAOS, each firing on the step grid. SKETCH is a draw pad: TIME scrubs, VOL gates, MAD throws seeded events. Zappy sparks on every hit."),
}
def card(slug, d):
    return f'''    <div class="card {slug}">
      <span class="new">NEW</span>
      <div class="kind">{d["kind"]}</div>
      <h2 style="background:linear-gradient(135deg,{d["g1"]},{d["g2"]});-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;">{d["NAME"]}</h2>
      <p class="tag">{d["tag"]}</p>
      <p class="desc">{d["desc"]}</p>
      <div class="shot"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/{slug}.png?v={d["ver"]}"><source src="https://video.sebastianmacan.com/img/video/{slug}_ui_loop.mp4?v={d["ver"]}" type="video/mp4"></video></div>
      <span class="dl buy" style="background:linear-gradient(135deg,{d["g1"]},{d["g2"]});box-shadow:0 6px 28px rgba({d["rgb"]},.30);" role="button" tabindex="0" data-cart-buy="{slug}">Buy {d["Name"]} &middot; $15</span>
      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="{slug}">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="{slug}">Buy Now</span></div>
      <a class="more" href="{slug}.html">See how it works &rarr;</a>
      <div class="meta">v{d["ver"]} · VST3 + AU effect · macOS + Windows</div>
    </div>
'''
def css(slug, d):
    return f'  .{slug} {{ --g1:{d["g1"]}; --g2:{d["g2"]}; --glow:{d["g1"]}; --shadow:rgba({d["rgb"]},.30); }}\n'

def strip_card(h, slug):
    """remove <div class="card slug"> ... matching </div> by depth walk"""
    m = re.search(r'[ \t]*<div class="card %s">' % slug, h)
    if not m: return h
    i = m.start(); j = m.end(); depth = 1
    while depth:
        nxt = re.compile(r'<div\b|</div>').search(h, j)
        depth += 1 if nxt.group().startswith('<div') else -1; j = nxt.end()
    if h[j:j+1] == "\n": j += 1
    return h[:i] + h[j:]

def index(h):
    h = strip_card(h, "gremlin")
    # gremlin css blocks (card styles + spacewarp variants + media rule)
    h = "\n".join(l for l in h.split("\n") if not re.match(r'\s*(\.gremlin\b|\.card\.gremlin\b|/\* Gremlin card|@media \(min-width:641px\)\{ \.card\.gremlin)', l))
    for slug, d in CARDS.items():
        if f'.{slug} {{ --g1' not in h:
            h = h.replace('  .pocket { --g1', css(slug, d) + '  .pocket { --g1', 1)
    if 'class="card smear"' not in h:
        anchor = '  <div class="sect-title" id="effects">Color &amp; Motion FX</div>\n  <div class="grid">\n'
        assert anchor in h
        h = h.replace(anchor, anchor + "".join(card(s, CARDS[s]) for s in ("stutter", "smear", "twitch")), 1)
    h = h.replace(" The first section of Gremlin, free forever.</p>", " Free forever.</p>")
    # counts: 12 plugins - Gremlin + 3 = 14
    h = h.replace("12 Plugins + 11 MIDI Packs", "14 Plugins + 11 MIDI Packs")
    h = h.replace('<p class="sub">Twelve plugins and', '<p class="sub">Fourteen plugins and')
    assert "gremlin" not in h.lower() or print("WARN leftover gremlin refs:", [l.strip()[:90] for l in h.split("\n") if "gremlin" in l.lower()])
    return h
rw("index.html", index)

# ---------------- cart.js ----------------
def cart(s):
    s = re.sub(r"\n    gremlin:\s*\{[^\n]*\n", "\n", s)
    s = re.sub(r"\n    gremlinduo:\s*\{[^\n]*\n", "\n", s)
    rows = "".join("    %-14s { name: %-24s cents: 1500, priceId: '%s' },\n" % (k + ":", "'%s'," % k.capitalize(), PRI[k]) for k in ("smear", "stutter", "twitch"))
    if "smear:" not in s:
        s = s.replace("    pocket:        {", rows + "    pocket:        {", 1)
    return s
rw("js/cart.js", cart)

# ---------------- pricing.html ----------------
def pricing(s):
    s = re.sub(r"\n    <tr><td>Gremlin</td>[^\n]*", "", s)
    if "<td>Smear</td>" not in s:
        s = s.replace("    <tr><td>Pocket</td>",
            '    <tr><td>Smear</td><td>Granular smear into a plate reverb</td><td class="price">$15</td></tr>\n'
            '    <tr><td>Stutter</td><td>Beat repeat with dice and a patch bay</td><td class="price">$15</td></tr>\n'
            '    <tr><td>Twitch</td><td>Per-step glitch rack with a draw pad</td><td class="price">$15</td></tr>\n'
            '    <tr><td>Pocket</td>', 1)
    return s
rw("pricing.html", pricing)

# ---------------- sitemap ----------------
def sitemap(s):
    s = re.sub(r"\n  <url><loc>https://sebastianmacan.com/gremlin(-duo)?.html</loc>[^\n]*", "", s)
    if "smear.html" not in s:
        add = "".join(f"\n  <url><loc>https://sebastianmacan.com/{k}.html</loc><lastmod>2026-11-09</lastmod></url>" for k in ("smear", "stutter", "twitch"))
        s = s.replace("\n  <url><loc>https://sebastianmacan.com/chop.html</loc>", add + "\n  <url><loc>https://sebastianmacan.com/chop.html</loc>", 1)
        assert "smear.html" in s
    return s
rw("sitemap.xml", sitemap)

# ---------------- audit map ----------------
def audit(s):
    s = s.replace('"gremlin": "Gremlin", ', '"smear": "Smear", "stutter": "Stutter", "twitch": "Twitch", ').replace(', "gremlinduo": "Gremlin Duo"', "")
    return s
rw("audit_baskets.py", audit)

# ---------------- creators dropdown ----------------
rw("creators.html", lambda s: s.replace("<option>Gremlin</option>", "<option>Smear</option><option>Stutter</option><option>Twitch</option>") if "<option>Smear</option>" not in s else s)

# ---------------- cache-bust cart.js ----------------
for f in sorted(os.listdir(S)):
    if f.endswith(".html"):
        p = f"{S}/{f}"; s = open(p).read(); t = re.sub(r"js/cart\.js\?v=[A-Za-z0-9]+", "js/cart.js?v=split1", s)
        if t != s: open(p, "w").write(t)
print("cart.js cache-busted to v=split1")
