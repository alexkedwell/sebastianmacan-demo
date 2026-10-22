#!/usr/bin/env python3
"""Generate site/pocket.html (product page) from the house template (gremlin.html).
Run from ~/sebastianmacan/site. Idempotent. Modelled on gen_gremlin.py.
Palette comes from the Pocket UI screenshot: orange arcs on a dark room, cream snare head."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
h = open(f"{S}/gremlin.html").read()

# palette: orange + cream from the Pocket UI
h = h.replace("--g1:#2ed14f; --g2:#c9ff4a;", "--g1:#f08a3c; --g2:#f3d9ae;")
h = re.sub(r"rgba\(46,209,79,(\.\d+)\)", r"rgba(240,138,60,\1)", h)

h = h.replace("<title>Gremlin | Glitch, Stutter and Granular Mangler VST3/AU Plugin</title>",
              "<title>Pocket | Snare Depth VST3/AU Plugin</title>")
h = h.replace('content="Gremlin is the glitch box for beats: tempo-synced chops, pitched stutters and granular smear into a plate reverb. One plugin, three sections. VST3 and AU. By Sebastian Macan."',
              'content="Pocket puts your snare in the mix instead of on top of it. One DEPTH knob pulls the hit back into the room and keeps it dead centre. VST3 and AU, macOS and Windows. By Sebastian Macan."')

h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Pocket",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Pocket puts your snare in the mix instead of on top of it. One DEPTH knob darkens the top, adds distance pre-delay and brings up the room, while the snare stays dead centre. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/pocket.html",
   "offers": { "@type": "Offer", "price": "15", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "How much is Pocket?",
      "acceptedAnswer": { "@type": "Answer", "text": "Pocket is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription." } },
    { "@type": "Question", "name": "Is Pocket just an EQ and a reverb?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. The DEPTH knob moves four things together the way real distance does: it darkens the top end from 16 kHz down to 4.5 kHz, adds up to 12 ms of distance pre-delay, brings up the room and dips the level up to 3 dB. The first reflection is mono, so the snare itself never leaves the centre." } },
    { "@type": "Question", "name": "What DAWs does Pocket work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Pocket?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Pocket ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = '''  <section class="hero">
    <div class="kind">Snare Depth</div>
    <h1>POCKET</h1>
    <p class="tag">Puts your snare in the mix instead of on top of it.</p>
    <div class="videobox"><img src="img/ui/pocket.png?v=1.0.0" alt="Pocket plugin UI: a snare on a dark stage with DEPTH, CRACK, BODY, ROOM, WIDTH, MIX and OUTPUT knobs"></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="pocket">Buy Pocket &middot; $15</span>
      <div class="meta">v1.0.0 &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What Pocket does</h2>
  <p>$15 buys you the depth engine. Most snares sit on top of the beat like a sticker. Pocket moves the snare back into the room: one DEPTH knob darkens the top end the way air does, adds a few milliseconds of distance, brings up the room around it and dips the level, all in one move. The snare stays dead centre the whole way. It stops fighting your vocal and starts living with your drums.</p>

  <h2>Where it comes from</h2>
  <p>Orbit, the free auto-pan, had a side effect nobody planned: it mixed hats in. The darkening and the tiny pre-delay it used to fake distance turned out to be the useful part. Pocket is that depth engine with the motion stripped out and the source pinned to the centre, rebuilt for the one drum that needs it most.</p>

  <h2>One big knob, five helpers</h2>
  <div class="bot"><b>DEPTH.</b> The knob. Together it darkens the top from 16 kHz down to 4.5 kHz, adds 0 to 12 ms of distance pre-delay, brings up the room and dips the level up to 3 dB. Zero is your dry snare. Turn it up and the snare walks to the back of the room without ever leaving the centre.</div>
  <div class="bot"><b>CRACK.</b> The transient. Pull it back to tuck the hit under the beat, push it to snap. Centre is untouched.</div>
  <div class="bot"><b>BODY.</b> 200 Hz, plus or minus 6 dB. Thicken a thin snare or clean up a boomy one. Centre is flat.</div>
  <div class="bot"><b>ROOM.</b> Early reflections plus a short tail, 80 to 450 ms. The first reflection is mono, so the direct sound stays centred no matter how big the room gets.</div>
  <div class="bot"><b>WIDTH.</b> Stereo width of the room only, never the direct. The snare stays mono-solid while the space around it opens up.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Pocket on the snare.</b> Snare track, snare bus, or the whole top kit. It opens on Init, which is close to dry.</div>
  <div class="step"><b>2. Turn DEPTH until the snare sits.</b> Somewhere between 30 and 60 percent it stops poking out and starts sounding placed. That is the pocket.</div>
  <div class="step"><b>3. Shape it.</b> CRACK for the hit, BODY for the weight, ROOM and WIDTH for the space. MIX blends it with the dry signal, OUTPUT trims the result.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>DEPTH.</b> Darkening, distance pre-delay, room lift and a level dip in one move. The whole plugin lives here.</div>
  <div class="knob"><b>CRACK.</b> Transient control. Back is tucked, forward is snappy, centre leaves the hit alone.</div>
  <div class="knob"><b>BODY.</b> 200 Hz shelf, plus or minus 6 dB. Centre is flat.</div>
  <div class="knob"><b>ROOM.</b> Early reflections and a short 80 to 450 ms tail. First reflection is mono so the snare never drifts.</div>
  <div class="knob"><b>WIDTH.</b> Widens the room, never the snare.</div>
  <div class="knob"><b>MIX and OUTPUT.</b> Parallel blend and output trim. BYPASS pill in the header for honest A/B.</div>
  <div class="knob"><b>PRESETS.</b> Preset bar in the header, save unlimited of your own. Zero latency, so it is safe on the way in or at mixdown.</div>

  <h2>Presets</h2>
  <p>7 to start: Init, Trap Dry, Boom Bap, Live Room, Back Of The Club, Stadium and Snap Forward. From bone dry and tucked to a snare echoing off the back wall, plus unlimited slots for your own.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>How much is Pocket?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>
  <div class="knob"><b>Is Pocket just an EQ and a reverb?</b> No. DEPTH moves four things together the way real distance does: darkening from 16 kHz down to 4.5 kHz, up to 12 ms of pre-delay, room lift and up to a 3 dB level dip. The first reflection is mono, so the snare itself never leaves the centre.</div>
  <div class="knob"><b>Does it work on things other than snares?</b> It is tuned for snares and claps, but anything that sits too far forward is fair game: percussion, plucks, even a vocal ad-lib.</div>
  <div class="knob"><b>What DAWs does Pocket work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Pocket?</b> Yes. Pocket ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.</div>
  <div class="knob"><b>How do I install Pocket?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="pocket">Buy Pocket &middot; $15</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
# static hero image instead of the ui loop video
h = h.replace("  .videobox video { display:block; width:100%; height:auto; }",
              "  .videobox img { display:block; width:100%; height:auto; }")
# drop the leftover "In the studio" video CSS block (Pocket has no studio video yet; also kills the em dash)
_a = h.index("/* In the studio")
_b = h.index("  .knob {", _a)
h = h[:_a] + h[_b:]
open(f"{S}/pocket.html", "w").write(h); print("wrote pocket.html", len(h))
