#!/usr/bin/env python3
# DEAD GENERATOR (Nov 9 2026): template drifted (neon skin) + VER stale. chop.html is hand-edited now. Do not run.
raise SystemExit("gen_chop.py is retired - edit chop.html directly")
"""Generate site/chop.html (FREE product page) from gremlin.html. Run from ~/sebastianmacan/site. Idempotent.
Chop = free forever (Orbit pattern: direct download links, no cart)."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
h = open(f"{S}/_tpl/product.html").read().replace('<meta name="robots" content="noindex">\n', "")

VER = "1.0.1"
MAC = f"downloads/Chop-v{VER}-macOS.pkg"
WIN = f"downloads/Chop-v{VER}-Windows-Setup.exe"

# palette: Chop green (mascot)
h = re.sub(r"--g1:#[0-9a-fA-F]{6}; --g2:#[0-9a-fA-F]{6};", "--g1:#8fd62a; --g2:#d4ff5a;", h)
# any accent-coloured glow in gremlin.html (whatever palette it currently uses) -> Chop green
h = re.sub(r"rgba\((?:46,209,79|154,107,255|176,107,255),(\.\d+)\)", r"rgba(143,214,42,\1)", h)
assert "--g1:#8fd62a" in h and "154,107,255" not in h and "176,107,255" not in h

h = h.replace("<title>Gremlin | Glitch, Stutter and Granular Mangler VST3/AU Plugin</title>",
              "<title>Chop | Free Rhythm Chopper VST3/AU Plugin</title>")
h = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Chop is a free tempo-synced rhythm chopper (VST3 and AU, macOS and Windows). Six rates, five patterns, swing and humanize. Chomps any loop into a groove. By Sebastian Macan.">', h)

h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Chop",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Chop is a free tempo-synced rhythm chopper. Six rates from 1/4 to 1/32 including triplets, five patterns, swing and humanize. Chomps any loop, pad or vocal into a groove. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/chop.html",
   "offers": { "@type": "Offer", "price": "0", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "Is Chop really free?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Chop is free forever. Full version, every knob, no email wall, no subscription." } },
    { "@type": "Question", "name": "What does Chop do?",
      "acceptedAnswer": { "@type": "Answer", "text": "It gates your audio on a tempo grid. Pick a rate from 1/4 to 1/32 (triplets included), a pattern (straight, offbeat, 3-3-2, gallop, random), set how much of each step stays open, add swing and humanize. Any sustained sound becomes a rhythm." } },
    { "@type": "Question", "name": "What DAWs does Chop work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Chop?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Chop ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = f'''  <section class="hero">
    <div class="kind">Free Rhythm Chopper</div>
    <h1>CHOP</h1>
    <p class="tag">Chomps any sound into a groove. Free forever.</p>
    <div class="videobox"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/chop.png?v={VER}" aria-label="Chop plugin UI: a green chomper mascot biting on the beat while the knobs move"><source src="https://video.sebastianmacan.com/img/video/chop_ui_loop.mp4?v={VER}" type="video/mp4"></video></div>
    <div class="cta">
      <a class="dl" href="{MAC}">Download Chop Free &middot; macOS</a>
      <a class="dl dl-win" href="{WIN}">Download Chop Free &middot; Windows</a>
      <div class="meta">v{VER} &middot; VST3 + AU effect &middot; macOS + Windows &middot; 100% free</div>
    </div>
  </section>

  <h2>What Chop does</h2>
  <p>Drop it on a pad, a vocal, a guitar loop, a whole bus. Chop opens and closes on the beat so the sound turns into a rhythm. Six rates from quarter notes to 1/32s with triplets, five patterns from straight to gallop to random, and a LENGTH knob that decides how much of every step you hear. SHAPE goes from a soft pluck to a hard gate. SWING and HUMANIZE keep it from sounding like a machine.</p>

  <h2>Same family as Smear, Stutter and Twitch</h2>
  <p>Chop shares its panel, its chomper and its engine with the three $15 boxes. Each one does one thing; this one happens to be free. Nothing held back.</p>

  <h2>Six knobs, one groove</h2>
  <div class="bot"><b>RATE.</b> 1/4, 1/8, 1/8T, 1/16, 1/16T, 1/32. Locked to your DAW tempo.</div>
  <div class="bot"><b>PATTERN.</b> STRAIGHT, OFFBEAT, 3-3-2, GALLOP, RANDOM. Which steps open.</div>
  <div class="bot"><b>LENGTH.</b> How much of each step stays open. Short for stabs, long for a pulse.</div>
  <div class="bot"><b>SHAPE.</b> Soft pluck at zero, hard gate at full. 2 ms edges so it never clicks.</div>
  <div class="bot"><b>SWING.</b> Every second step lands late, up to 66% MPC swing.</div>
  <div class="bot"><b>HUMANIZE.</b> Up to 12 ms of timing drift and up to 6 dB of level drift, random per step.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Chop on something that sustains.</b> A pad, a held chord, a vocal, a reverb return.</div>
  <div class="step"><b>2. Press play.</b> It opens on Init at 1/8 straight. You already have a groove.</div>
  <div class="step"><b>3. Pick a pattern and a rate.</b> GALLOP at 1/16 is the trap move. 3-3-2 at 1/8 is the latin one. RANDOM is the surprise.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>THE CHOMPER.</b> The green face is the readout. It bites every time the gate opens, so you see the pattern before you hear it.</div>
  <div class="knob"><b>MIX and OUT.</b> Blend the chopped signal with the dry one, trim the result. BYPASS pill in the header for an honest A/B.</div>
  <div class="knob"><b>PRESETS.</b> 11 to start: Init, Nibble, Machine Gun, Gentle Hiccup, Gallop, Chomp, Triplet Bite, Swing Snack, Three Three Two, Offbeat Munch and Feral. Save unlimited of your own.</div>
  <div class="knob"><b>INIT ANY KNOB.</b> Right-click or Cmd-click a knob to send it home.</div>

  <h2>Want more?</h2>
  <p>Smear, Stutter and Twitch each pick up where Chop leaves off: <a href="smear.html">Smear</a> melts your chopped loop into a plate reverb, <a href="stutter.html">Stutter</a> repeats it on a dice roll, <a href="twitch.html">Twitch</a> is the per-step glitch rack with a draw pad. $15 each.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>Is Chop really free?</b> Yes. Free forever. Full version, every knob, no email wall, no subscription.</div>
  <div class="knob"><b>What DAWs does Chop work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Chop?</b> Yes. Chop ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both.</div>
  <div class="knob"><b>How do I install Chop?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <a class="dl" href="{MAC}">Download Chop Free &middot; macOS</a>
    <a class="dl dl-win" href="{WIN}">Download Chop Free &middot; Windows</a>
    <div class="meta">No email needed &middot; direct download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
_a = h.find("/* In the studio")
if _a > 0:
    _b = h.index("  .knob {", _a); h = h[:_a] + h[_b:]
open(f"{S}/chop.html", "w").write(h); print("wrote chop.html", len(h))
