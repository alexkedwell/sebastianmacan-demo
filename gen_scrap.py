#!/usr/bin/env python3
"""Scrap page + card for site/ and demo-site/. Clones chop.html (free pattern), re-palettes to Scrap orange/cyan.
Card goes right after Chop in Color & Motion FX. Idempotent. Pass VER."""
import re, os, sys
VER = sys.argv[1] if len(sys.argv) > 1 else "1.0.1"
MAC = f"downloads/Scrap-v{VER}-macOS.pkg"
WIN = f"downloads/Scrap-v{VER}-Windows-Setup.exe"
for root in ("site", "demo-site"):
    S = os.path.expanduser(f"~/sebastianmacan/{root}")
    h = open(f"{S}/chop.html", encoding="utf-8").read()
    h = re.sub(r"--g1:#8fd62a; --g2:#d4ff5a;", "--g1:#ff7a2e; --g2:#ffb347;", h)
    h = re.sub(r"rgba\(143,214,42,(\.\d+)\)", r"rgba(255,122,46,\1)", h)
    assert "--g1:#ff7a2e" in h and "143,214,42" not in h
    h = h.replace("<title>Chop | Free Rhythm Chopper VST3/AU Plugin</title>",
                  "<title>Scrap | Free Glitch Repeater VST3/AU Plugin</title>")
    h = re.sub(r'<meta name="description" content="[^"]*">',
               '<meta name="description" content="Scrap is a free stutter-buffer glitch effect (VST3 and AU, macOS and Windows). Grabs slices of whatever is playing, repeats them, flips them backwards, kicks them an octave. Metallic, broken, great on drops. By Sebastian Macan.">', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Scrap",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Scrap is a free stutter-buffer glitch effect. It grabs slices of the incoming audio, repeats them, reverses them and pitches them in octaves and fifths, with a growl drive and an air return. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/scrap.html",
   "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "Is Scrap really free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Scrap is free forever. Full version, every knob, no email wall, no subscription." } },
    { "@type": "Question", "name": "What does Scrap do?",
      "acceptedAnswer": { "@type": "Answer", "text": "It records what is playing into a short buffer, grabs a slice between 15 and 220 milliseconds, and plays it back up to thirteen times. Each slice can be reversed and pitched down an octave, up a fifth or up an octave. TWIST decides how broken it gets." } },
    { "@type": "Question", "name": "What DAWs does Scrap work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Scrap?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Scrap ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

    body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
    body = f'''  <section class="hero">
    <div class="kind">Free Glitch Repeater</div>
    <h1>SCRAP</h1>
    <p class="tag">Grabs a slice and won't let go. Free forever.</p>
    <div class="videobox"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/scrap.png?v={VER}" aria-label="Scrap plugin UI: an orange rusty robot glitching while the knobs move"><source src="https://video.sebastianmacan.com/img/video/scrap_ui_loop.mp4?v={VER}" type="video/mp4"></video></div>
    <div class="cta">
      <a class="dl" href="{MAC}">Download Scrap Free &middot; macOS</a>
      <a class="dl dl-win" href="{WIN}">Download Scrap Free &middot; Windows</a>
      <div class="meta">v{VER} &middot; VST3 + AU effect &middot; macOS + Windows &middot; 100% free</div>
    </div>
  </section>

  <h2>What Scrap does</h2>
  <p>Scrap keeps a short recording of whatever is playing. Every few beats it grabs a slice, between 15 and 220 milliseconds, and plays it back up to thirteen times. Some slices come back reversed. Some come back an octave down, a fifth up, an octave up. Then it hands you the dry signal again like nothing happened. The result is metallic, broken and rhythmic in a way you could never program by hand. Put it on a drop, a vocal chop, a hi-hat loop, a whole bus for one bar.</p>

  <h2>Six knobs, one robot</h2>
  <div class="bot"><b>TWIST.</b> How broken. Low is a polite hiccup every so often. High is shorter slices, more repeats, more reversals, more pitch jumps.</div>
  <div class="bot"><b>REPEAT.</b> How many times a slice can fire. All the way up is a thirteen-shot stutter.</div>
  <div class="bot"><b>PITCH.</b> How often a slice gets kicked an octave down, a fifth up or an octave up. Zero keeps everything at pitch.</div>
  <div class="bot"><b>REVERSE.</b> How often a slice plays backwards.</div>
  <div class="bot"><b>GROWL.</b> Drive on the glitched signal only. Turn it up and the repeats get teeth.</div>
  <div class="bot"><b>AIR.</b> Adds the top end of the dry signal back on top so the glitch never goes dull.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Scrap on something rhythmic.</b> A drum loop, a vocal chop, the last bar before a drop.</div>
  <div class="step"><b>2. Press play.</b> It opens on Init. Already interesting.</div>
  <div class="step"><b>3. Turn TWIST up and PITCH up.</b> That is the metallic one. Automate MIX from zero to full for the drop and back.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>THE ROBOT.</b> The rusty face is the readout. It tears and ghosts every time a slice fires, so you see the glitch before you hear it.</div>
  <div class="knob"><b>MIX and OUT.</b> Blend the glitch with the dry signal, trim the result. BYPASS pill in the header for an honest A/B.</div>
  <div class="knob"><b>PRESETS.</b> 9 to start: Init, Light Rust, Machine Jam, Backmasker, Octave Gremlin, Stutter Storm, Chrome Teeth, Airy Sputter and Total Meltdown. Save unlimited of your own.</div>
  <div class="knob"><b>INIT ANY KNOB.</b> Right-click or Cmd-click a knob to send it home.</div>
  <div class="knob"><b>Window size.</b> Drag the corner grip to resize the whole plugin; your DAW remembers it.</div>

  <h2>Want more?</h2>
  <p><a href="chop.html">Chop</a> is the other free one: a tempo-synced gate that turns anything into a rhythm. <a href="stutter.html">Stutter</a>, <a href="smear.html">Smear</a> and <a href="twitch.html">Twitch</a> are the $15 boxes next to it.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>Is Scrap really free?</b> Yes. Free forever. Full version, every knob, no email wall, no subscription.</div>
  <div class="knob"><b>What DAWs does Scrap work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Scrap?</b> Yes. Scrap ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both.</div>
  <div class="knob"><b>How do I install Scrap?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <a class="dl" href="{MAC}">Download Scrap Free &middot; macOS</a>
    <a class="dl dl-win" href="{WIN}">Download Scrap Free &middot; Windows</a>
    <div class="meta">No email needed &middot; direct download</div>
  </div>

'''
    h = h[:body_start] + body + h[body_end:]
    assert "Chop" not in h.split('<section class="hero">')[1].split("Want more?")[0]
    open(f"{S}/scrap.html", "w", encoding="utf-8").write(h)

    # ---- card on index.html, right after the chop card ----
    idx = open(f"{S}/index.html", encoding="utf-8").read()
    idx = re.sub(r'    <div class="card scrap">\n.*?\n    </div>\n', '', idx, flags=re.S)
    m = re.search(r'    <div class="card chop">\n.*?\n    </div>\n', idx, re.S); assert m
    card = f'''    <div class="card scrap">
      <span class="new">NEW</span>
      <div class="kind">Free Glitch Repeater</div>
      <h2 style="background:linear-gradient(135deg,#ff7a2e,#ffb347);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;">SCRAP</h2>
      <p class="tag">Grabs a slice and won't let go.</p>
      <p class="desc">Stutter-buffer glitch that repeats, reverses and pitch-kicks slices of whatever is playing, with a growl drive and an air return. Metallic, broken, built for drops.</p>
      <div class="shot"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/scrap.png?v={VER}"><source src="https://video.sebastianmacan.com/img/video/scrap_ui_loop.mp4?v={VER}" type="video/mp4"></video></div>
      <a class="dl" style="background:linear-gradient(135deg,#ff7a2e,#ffb347);box-shadow:0 6px 28px rgba(255,122,46,.30);" href="{MAC}">Download Scrap</a>
      <div class="cartrow"><span class="cartbtn add" style="pointer-events:none;border-color:rgba(255,216,74,.5);color:#ffd84a;">100% Free &middot; Forever</span></div>
      <a class="more" href="scrap.html">See how it works &rarr;</a>
      <div class="meta">v{VER} · VST3 + AU effect · macOS + Windows</div>
    </div>
'''
    idx = idx.replace(m.group(0), m.group(0) + card, 1)
    pal = '  .chop   { --g1:#8fd62a; --g2:#d4ff5a; --glow:#8fd62a; --shadow:rgba(143,214,42,.26); }\n'
    assert idx.count(pal) == 1
    if '.scrap  {' not in idx:
        idx = idx.replace(pal, pal + '  .scrap  { --g1:#ff7a2e; --g2:#ffb347; --glow:#ff7a2e; --shadow:rgba(255,122,46,.26); }\n')
    assert idx.count('<div class="card scrap">') == 1
    open(f"{S}/index.html", "w", encoding="utf-8").write(idx)
    print(root, "scrap.html + card OK")
