#!/usr/bin/env python3
"""Generate site/gremlin-duo.html ($7 Chop + Smear) from gremlin.html. Run from ~/sebastianmacan/site. Idempotent."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
h = open(f"{S}/gremlin.html").read()
VER = "1.0.0"

h = h.replace("--g1:#2ed14f; --g2:#c9ff4a;", "--g1:#9ad63a; --g2:#c86cff;")
h = re.sub(r"rgba\(46,209,79,(\.\d+)\)", r"rgba(176,112,255,\1)", h)
h = h.replace("<title>Gremlin | Glitch, Stutter and Granular Mangler VST3/AU Plugin</title>",
              "<title>Gremlin Duo | Chop + Smear VST3/AU Plugin</title>")
h = re.sub(r'<meta name="description" content="[^"]*">',
           '<meta name="description" content="Gremlin Duo is Chop and Smear in one box: a tempo-synced rhythm chopper feeding a granular plate that melts your loop into a wash. $7, VST3 and AU, macOS and Windows. By Sebastian Macan.">', h)

h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Gremlin Duo",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Gremlin Duo is Chop and Smear in one box: a tempo-synced rhythm chopper feeding a granular plate that melts your loop into a wash. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/gremlin-duo.html",
   "offers": { "@type": "Offer", "price": "7", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "How much is Gremlin Duo?",
      "acceptedAnswer": { "@type": "Answer", "text": "Gremlin Duo is $7, one-time. Instant download after checkout, full version, no subscription." } },
    { "@type": "Question", "name": "What is the difference between Chop, Gremlin Duo and Gremlin?",
      "acceptedAnswer": { "@type": "Answer", "text": "Chop is the free rhythm chopper. Gremlin Duo adds Smear, the granular plate, for $7. Gremlin adds the full Stutter rack on top for $15. Same engines in every tier, so presets and sound match." } },
    { "@type": "Question", "name": "What DAWs does Gremlin Duo work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more." } },
    { "@type": "Question", "name": "Is there a Windows version?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Gremlin Duo ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both. One purchase covers both platforms." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = f'''  <section class="hero">
    <div class="kind">Chop + Smear</div>
    <h1>GREMLIN DUO</h1>
    <p class="tag">Chop it. Smear it. Two mischiefs, one box.</p>
    <div class="videobox"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/gremlin-duo.png?v={VER}" aria-label="Gremlin Duo plugin UI: the green chomper and the purple smear blob side by side while the knobs move"><source src="https://video.sebastianmacan.com/img/video/gremlin_duo_ui_loop.mp4?v={VER}" type="video/mp4"></video></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlinduo">Buy Gremlin Duo &middot; $7</span>
      <div class="meta">v{VER} &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What Gremlin Duo does</h2>
  <p>Two of Gremlin's three sections in one plugin. CHOP gates your sound on the tempo grid so a pad, a vocal or a loop turns into a rhythm. SMEAR takes what comes out and melts it: a granular plate that blurs the chops into a wash, pitches it up an octave of shimmer, drifts it, freezes it. Chop feeds Smear, so every stab you cut leaves a tail. Both sections have their own ON pill, so you can run either alone.</p>

  <h2>Where it comes from</h2>
  <p>Gremlin is the full mangler: Chop, Stutter and Smear. A lot of people only ever used the first and the last. Duo is those two, same engines, same presets behaviour, for $7. If you want the Stutter rack later, <a href="gremlin.html">Gremlin</a> is the upgrade.</p>

  <h2>CHOP, six knobs</h2>
  <div class="bot"><b>RATE.</b> 1/4 to 1/32 with triplets, locked to your DAW tempo.</div>
  <div class="bot"><b>PATTERN.</b> STRAIGHT, OFFBEAT, 3-3-2, GALLOP, RANDOM.</div>
  <div class="bot"><b>LENGTH and SHAPE.</b> How much of each step you hear, and whether the edge is a soft pluck or a hard gate.</div>
  <div class="bot"><b>SWING and HUMANIZE.</b> Up to 66% MPC swing, plus random timing and level drift so it breathes.</div>

  <h2>SMEAR, ten knobs</h2>
  <div class="bot"><b>SMEAR.</b> How much of the signal goes into the cloud.</div>
  <div class="bot"><b>PITCH and SHIMMER.</b> Pitch the grains, add the octave-up halo.</div>
  <div class="bot"><b>BLUR, WASH, DECAY.</b> Grain size, plate amount and how long the tail hangs.</div>
  <div class="bot"><b>DEPTH, TONE, DRIFT.</b> Modulation depth, tilt of the tail, slow wander of the grain positions.</div>
  <div class="bot"><b>FREEZE.</b> Pill. Holds the cloud where it is for as long as you like.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Duo on something that sustains.</b> A pad, a chord stab, a vocal, a drum loop.</div>
  <div class="step"><b>2. Press play.</b> Both sections open ON. You already hear chopped rhythm with a soft tail.</div>
  <div class="step"><b>3. Pick a preset.</b> Chomp &amp; Haze, Half-Time Melt, Gallop Wash, Offbeat Shimmer, Bite &amp; Bloom, Taffy Pull, Jawbreaker Jam, Syrup Stomp and Frosted Teeth, plus Init. Then turn the knobs.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>THE MASCOTS.</b> The green chomper bites every time the gate opens. The purple blob glows with the smear. They are the readout.</div>
  <div class="knob"><b>MIX and OUT.</b> Blend with the dry signal, trim the result. BYPASS pill in the header for an honest A/B.</div>
  <div class="knob"><b>PRESETS.</b> 10 to start, save unlimited of your own. Right-click or Cmd-click any knob to send it home.</div>

  <h2>Common questions</h2>
  <div class="knob"><b>How much is Gremlin Duo?</b> $7, one-time. Instant download after checkout. Full version, no subscription.</div>
  <div class="knob"><b>Chop, Duo or Gremlin?</b> <a href="chop.html">Chop</a> is free. Duo adds Smear for $7. <a href="gremlin.html">Gremlin</a> adds the Stutter rack for $15. Same engines in every tier.</div>
  <div class="knob"><b>What DAWs does it work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version?</b> Yes. macOS (VST3 + AU) and Windows (VST3), code-signed on both. One purchase covers both.</div>
  <div class="knob"><b>How do I install it?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlinduo">Buy Gremlin Duo &middot; $7</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
_a = h.find("/* In the studio")
if _a > 0:
    _b = h.index("  .knob {", _a); h = h[:_a] + h[_b:]
open(f"{S}/gremlin-duo.html", "w").write(h); print("wrote gremlin-duo.html", len(h))
