#!/usr/bin/env python3
"""Generate site/taffy.html (product page) from the house template (gremlin.html).
Run from ~/sebastianmacan/site. Idempotent. Modelled on gen_pocket.py.
Palette: brushed steel + amber LED from the Taffy rack UI."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
h = open(f"{S}/gremlin.html").read()

h = h.replace("--g1:#2ed14f; --g2:#c9ff4a;", "--g1:#c9c9c9; --g2:#ffb545;")
h = re.sub(r"rgba\(46,209,79,(\.\d+)\)", r"rgba(255,181,69,\1)", h)

h = h.replace("<title>Gremlin | Glitch, Stutter and Granular Mangler VST3/AU Plugin</title>",
              "<title>Taffy | Transient Shaper VST3/AU Plugin</title>")
h = h.replace('content="Gremlin is the glitch box for beats: tempo-synced chops, pitched stutters and granular smear into a plate reverb. One plugin, three sections. VST3 and AU. By Sebastian Macan."',
              'content="Taffy is a transient shaper that pulls the hit forward or stretches the sustain out, with LENGTH, ROUND and MIX to taste. Rack-unit UI, six knobs, zero latency. VST3 and AU, macOS and Windows. By Sebastian Macan."')

h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Taffy",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Taffy is a transient shaper. ATTACK pulls the hit forward or tucks it back, SUSTAIN stretches the body out or dries it up, LENGTH sets how much of the hit counts, ROUND softens the spikes. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/taffy.html",
   "offers": { "@type": "Offer", "price": "15", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "How much is Taffy?",
      "acceptedAnswer": { "@type": "Answer", "text": "Taffy is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription." } },
    { "@type": "Question", "name": "What is a transient shaper?",
      "acceptedAnswer": { "@type": "Answer", "text": "A transient shaper changes the shape of a sound over time instead of its tone. It splits every hit into the attack (the first few milliseconds) and the sustain (everything after), and lets you turn each one up or down on its own. Taffy does that with two knobs." } },
    { "@type": "Question", "name": "What DAWs does Taffy work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Taffy?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Taffy ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = '''  <section class="hero">
    <div class="kind">Transient Shaper</div>
    <h1>TAFFY</h1>
    <p class="tag">Pull the hit forward. Stretch the body out. Two knobs, done.</p>
    <div class="videobox"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/taffy.png?v=1.0.3" aria-label="Taffy plugin UI: a black rack unit with a chrome stretch bar and six steel knobs, ATTACK and SUSTAIN sweeping"><source src="https://video.sebastianmacan.com/img/video/taffy_ui_loop.mp4?v=1.0.3" type="video/mp4"></video></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="taffy">Buy Taffy &middot; $15</span>
      <div class="meta">v1.0.3 &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What Taffy does</h2>
  <p>Every drum hit has two halves: the crack at the front and the body that follows. Taffy lets you grab each half and pull. Turn ATTACK up and the kick punches through a busy mix without touching the fader. Turn SUSTAIN up and a dry snare stretches out like it was cut in a real room. Turn either one down and the hit tucks back under the beat. It is the fastest way to change how drums feel without changing how they sound.</p>

  <h2>Why it is called Taffy</h2>
  <p>Because that is what it does to a hit. The stretch bar across the top is the sound being pulled: it bulges on every transient, and the harder you push ATTACK and SUSTAIN the further it stretches. ROUND turns the glow up as it softens the sharp edges. You can watch the shape of your drums change in real time.</p>

  <h2>Six knobs, one job</h2>
  <div class="bot"><b>ATTACK.</b> Plus or minus 12 dB on the first few milliseconds of every hit. Up for punch, down to tuck a loud snare under the vocal. Centre leaves it alone.</div>
  <div class="bot"><b>SUSTAIN.</b> Plus or minus 12 dB on everything after the hit. Up for room and ring, down to dry a loop out so it sits tighter.</div>
  <div class="bot"><b>LENGTH.</b> How long the attack window lasts, 5 to 80 ms. Short for clicky hats, long for a kick with a tail.</div>
  <div class="bot"><b>ROUND.</b> Softens the peaks after shaping so a big ATTACK boost never turns spiky. The stretch bar glows amber as you turn it up.</div>
  <div class="bot"><b>MIX and OUTPUT.</b> Parallel blend and output trim. BYPASS switch with an amber LED in the header for honest A/B.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Taffy on a drum.</b> Kick, snare, a full loop, a drum bus. It opens on Init, which is close to flat.</div>
  <div class="step"><b>2. Turn ATTACK up until the hit pokes out.</b> Then back it off a touch. That is usually the whole fix for a kick that disappears in the mix.</div>
  <div class="step"><b>3. Shape the body.</b> SUSTAIN up for room, down for tight. LENGTH tunes which part counts as the hit, ROUND keeps it smooth, MIX blends it with the dry signal.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>ATTACK.</b> The front of the hit, plus or minus 12 dB. Centre is untouched.</div>
  <div class="knob"><b>SUSTAIN.</b> The tail of the hit, plus or minus 12 dB. Centre is untouched.</div>
  <div class="knob"><b>LENGTH.</b> Attack window, 5 to 80 ms.</div>
  <div class="knob"><b>ROUND.</b> Peak softening after the shaper, 0 to 100 percent.</div>
  <div class="knob"><b>MIX and OUTPUT.</b> Parallel blend and output trim.</div>
  <div class="knob"><b>PRESETS.</b> Preset stepper in the header, save unlimited of your own. Zero latency, safe on the way in or at mixdown.</div>

  <h2>Presets</h2>
  <p>10 to start: Init, Snap, Punch, Soft Hands, Room Grab, Gate-ish, Smooth It Out, Round Drums, 404 Butter and Parallel Crack. From a clean snap to full stretch, plus unlimited slots for your own.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>How much is Taffy?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>
  <div class="knob"><b>What is a transient shaper?</b> It changes the shape of a sound over time instead of its tone. Every hit gets split into the attack (the first few milliseconds) and the sustain (everything after), and you turn each one up or down on its own. A compressor reacts to level; Taffy reacts to the hit itself, so it works the same on a quiet take and a loud one.</div>
  <div class="knob"><b>Does it work on things other than drums?</b> Anything with a front edge: plucked guitar, piano, bass, percussion loops. ATTACK down on a plucky bass smooths it out; SUSTAIN up on a short guitar part gives it length.</div>
  <div class="knob"><b>What DAWs does Taffy work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Taffy?</b> Yes. Taffy ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.</div>
  <div class="knob"><b>How do I install Taffy?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="taffy">Buy Taffy &middot; $15</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
_a = h.index("/* In the studio")
_b = h.index("  .knob {", _a)
h = h[:_a] + h[_b:]
open(f"{S}/taffy.html", "w").write(h); print("wrote taffy.html", len(h))
