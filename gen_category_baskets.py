"""Build basket-instruments/effects/studio.html from basket-lofi.html (live-edited skeleton = source of truth).
Sep 23 2026. Run from site dir."""
import re
ITEMS = {
  "biome":     ("Granular Texture Blender", "Biome", "Drop a rainforest on your beat. Drag in any audio and grow it into huge evolving textures.", 39, "biome.html"),
  "magician":  ("Chord & Melody Generator", "Chordsmith", "Pick a genre, key and mode, hit GENERATE. Chords and a melody, ready to drag into your DAW.", 39, "chordsmith.html"),
  "jelly":     ("Wobble Machine", "Jelly", "Make everything jiggle. LFO-driven movement for basses, synths and anything that sits too still.", 15, "jelly.html"),
  "warble":    ("Drunk Songbird Pitch Wobbler", "Warble", "Make any sound sing like a weird little bird.", 15, "warble.html"),
  "reels":     ("Subtle Tape Machine", "Reels", "Sometimes tape plugins do too much. Reels is just the right amount of vintage.", 15, "reels.html"),
  "gloss":     ("Instant Mix Polish", "Gloss", "Four knobs that make tracks sit right in the mix, fast.", 19, "gloss.html"),
  "orbit":     ("3D Auto-Pan", "Orbit", "Hats that fly around your head. Free forever, and in the basket anyway.", 0, "orbit.html"),
  "fireplace": ("Cozy Ambience Machine", "Fireplace", "Crackling fire, real forest rain, vinyl attic, tape room. Ducks under your beat.", 15, "fireplace.html"),
  "halo":      ("One-Knob Mastering", "Halo", "Drop it on your master. Turn LIFT until the halo closes.", 29, "halo.html"),
}
BASKETS = [
  dict(file="basket-instruments.html", cid="instrumentsbasket", title="INSTRUMENTS BASKET", name="Instruments Basket", price=59,
       img="img/bundles/instruments_bundle.png?v=3", g1="#39e6d0", g2="#60a5fa",
       tag="Both instruments in the store. Grow textures, then write the chords on top.",
       desc="Biome turns any audio into huge evolving textures, pads and drones. Chordsmith writes chords and melodies in any genre, key and mode and drags them straight into your DAW. The sound and the song, one basket.",
       items=["biome", "magician"], meta="2 plugins · VST3 + AU · macOS",
       mdesc="Biome and Chordsmith. Both Sebastian Macan instruments, one basket, VST3 + AU for macOS."),
  dict(file="basket-effects.html", cid="effectsbasket", title="EFFECTS BASKET", name="Effects Basket", price=49,
       img="img/bundles/effects_bundle.png?v=3", g1="#ff5ca8", g2="#8b5cf6",
       tag="Every effect in the store. Wobble, warble, tape and polish, with Orbit thrown in.",
       desc="Jelly makes things jiggle. Warble makes them sing like a weird little bird. Reels puts them on tape. Gloss makes them sit right in the mix. Orbit flies them around your head, free. Every effect we make, one basket.",
       items=["jelly", "warble", "reels", "gloss", "orbit"], meta="4 plugins + Orbit · VST3 + AU · macOS",
       mdesc="Jelly, Warble, Reels, Gloss and Orbit. Every Sebastian Macan effect, one basket, VST3 + AU for macOS."),
  dict(file="basket-studio.html", cid="studiobasket", title="STUDIO TOOLS BASKET", name="Studio Tools Basket", price=59,
       img="img/bundles/studio_bundle.png?v=3", g1="#f5a623", g2="#60a5fa",
       tag="The finishing tools. Atmosphere, tape, mix polish and a one-knob master.",
       desc="Fireplace lays a living room of atmosphere under the beat. Reels puts it on tape. Gloss makes every track sit right. Halo finishes the master with one knob and a verified LUFS meter. From rough idea to release, one basket.",
       items=["fireplace", "halo", "gloss", "reels"], meta="4 plugins · VST3 + AU · macOS",
       mdesc="Fireplace, Halo, Gloss and Reels. The Sebastian Macan finishing tools, one basket, VST3 + AU for macOS."),
]
def row(k):
    kind, name, tag, price, page = ITEMS[k]
    if price:
        act = f'<div class="iprice">${price}</div>\n        <span class="dl buy idl" role="button" tabindex="0" data-cart-buy="{k}">Buy {name} &middot; ${price}</span>'
    else:
        act = f'<div class="iprice"><span class="freetag">FREE forever</span></div>\n        <a class="dl idl" href="{page}">Get it free</a>'
    return f'''    <div class="item">
      <div class="iinfo">
        <div class="ikind">{kind}</div>
        <div class="iname">{name}</div>
        <p class="itag">{tag}</p>
        <a class="rowlink" href="{page}">See how it works &rarr;</a>
      </div>
      <div class="iact">
        {act}
      </div>
    </div>'''
src = open("basket-lofi.html").read()
for b in BASKETS:
    s = src
    s = s.replace("<title>Lofi Basket | Sebastian Macan</title>", f"<title>{b['name']} | Sebastian Macan</title>")
    s = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{b["mdesc"]}">', s)
    s = s.replace("--g1:#f5a623; --g2:#2bb59a;", f"--g1:{b['g1']}; --g2:{b['g2']};")
    s = s.replace("<h1>LOFI BASKET</h1>", f"<h1>{b['title']}</h1>")
    s = re.sub(r'<p class="tag">.*?</p>', f'<p class="tag">{b["tag"]}</p>', s, count=1)
    s = s.replace('src="img/bundles/lofi_bundle.png" alt="LOFI BASKET basket art"', f'src="{b["img"]}" alt="{b["title"]} basket art"')
    s = s.replace('<span class="big">$30</span>', f'<span class="big">${b["price"]}</span>')
    s = s.replace('<div class="meta">2 plugins · VST3 + AU · macOS</div>', f'<div class="meta">{b["meta"]}</div>')
    s = s.replace('data-cart-buy="lofibasket">Buy Lofi Basket &middot; $30</span>', f'data-cart-buy="{b["cid"]}">Buy {b["name"]} &middot; ${b["price"]}</span>')
    s = s.replace('data-cart-add="lofibasket"', f'data-cart-add="{b["cid"]}"').replace('data-cart-buy="lofibasket"', f'data-cart-buy="{b["cid"]}"')
    s = re.sub(r'<p class="sub">.*?</p>', f'<p class="sub">{b["desc"]} Every item below is sold on its own too, or take the whole basket at once.</p>', s, count=1, flags=re.S)
    # replace the item rows block
    start = s.index('    <div class="item">'); end = s.index('  <div class="cta">', start)
    s = s[:start] + "\n".join(row(k) for k in b["items"]) + "\n\n" + s[end:]
    n_paid = sum(1 for k in b["items"] if ITEMS[k][3])
    s = s.replace('<div class="meta">One zip, everything inside. Download once, unzip, done.</div>',
                  f'<div class="meta">{len(b["items"])} installers in one email. Download, install, done.</div>')
    total = sum(ITEMS[k][3] for k in b["items"])
    s = re.sub(r'<div class="mathbox">.*?</div>',
      f'<div class="mathbox">\n    Bought one by one this basket adds up to <b>${total}</b>. As a basket it\'s <b>${b["price"]}</b>, one-time. {len(b["items"])} items, zero catches.\n  </div>', s, flags=re.S)
    assert "lofibasket" not in s and "LOFI" not in s.split("<body>")[1], b["file"]
    open(b["file"], "w").write(s)
    print(b["file"], "ok", "$"+str(total), "->", "$"+str(b["price"]))
