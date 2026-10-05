#!/usr/bin/env python3
"""Generate site/gremlin.html (product page) from the house template (reels.html).
Run from ~/sebastianmacan/site. Idempotent. Modelled on gen_honey.py."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
VIDCSS = '''  .vidstack { margin:26px 0 6px; }
  .vidstack .big { border-radius:18px; overflow:hidden; border:1px solid var(--line); background:#0b0806; aspect-ratio:16/9; position:relative; }
  .vidstack .big video, .vidstack .big img { display:block; width:100%; height:100%; object-fit:cover; }
  .vidrow { display:grid; grid-template-columns:repeat(4,1fr); gap:10px; margin-top:10px; }
  .vidrow.three { grid-template-columns:repeat(3,1fr); }
  @media (max-width:560px){ .vidrow, .vidrow.three { grid-template-columns:repeat(2,1fr); } }
  .vidrow .sm { border-radius:12px; overflow:hidden; border:1px solid var(--line); background:#0b0806; aspect-ratio:16/9; position:relative; }
  .vidrow .sm video, .vidrow .sm img { display:block; width:100%; height:100%; object-fit:cover; }
  .vidrow .sm span, .vidstack .big span { position:absolute; left:8px; bottom:6px; font-size:11px; letter-spacing:.08em; text-transform:uppercase; color:#fff; text-shadow:0 1px 6px rgba(0,0,0,.9); }
  .vidstack .big span { font-size:13px; left:14px; bottom:10px; }
  @media (max-width:640px){ .vidrow { grid-template-columns:repeat(3,1fr); } }
  .sm, .big { cursor:pointer; }
  .play { position:absolute; left:50%; top:50%; width:44px; height:44px; margin:-22px 0 0 -22px; border-radius:50%; background:rgba(0,0,0,.55); border:2px solid rgba(255,255,255,.85); box-shadow:0 6px 24px rgba(0,0,0,.5); transition:transform .18s, background .18s; }
  .play::after { content:""; position:absolute; left:17px; top:12px; border-left:16px solid #fff; border-top:10px solid transparent; border-bottom:10px solid transparent; }
  .vidstack .big .play { width:84px; height:84px; margin:-42px 0 0 -42px; background:linear-gradient(135deg,var(--g1),var(--g2)); border:3px solid rgba(255,255,255,.9); }
  .vidstack .big .play::after { left:33px; top:24px; border-left:30px solid #fff; border-top:18px solid transparent; border-bottom:18px solid transparent; }
  [data-vid]:hover .play { transform:scale(1.08); }
  [data-vid].on .play { display:none; }
  .vidhint { font-size:12px; color:var(--muted,#9a8f86); margin-top:8px; letter-spacing:.04em; }
  .vidstack .big .seek { position:absolute; left:0; right:0; bottom:0; height:26px; background:linear-gradient(to top,rgba(0,0,0,.75),rgba(0,0,0,0)); cursor:pointer; opacity:0; transition:opacity .25s; }
  .vidstack .big:hover .seek, .vidstack .big.on .seek { opacity:1; }
  .vidstack .big .seek i { position:absolute; left:10px; right:10px; bottom:9px; height:3px; background:rgba(255,255,255,.25); border-radius:2px; display:block; }
  .vidstack .big .seek i { background:linear-gradient(90deg,var(--g1),var(--g2)) no-repeat, rgba(255,255,255,.25); background-size:var(--p,0%) 100%, 100% 100%; }
  .vidstack .big .seek b { position:absolute; right:12px; bottom:14px; font-size:11px; font-weight:600; color:#fff; letter-spacing:.04em; text-shadow:0 1px 4px rgba(0,0,0,.9); }
  .vidstack .big.on span { opacity:0; }'''
_fp = open(f"{S}/fireplace.html").read()
_i = _fp.index("(function(){var vids="); _j = _fp.index("</script>", _i)
JS = _fp[_i:_j].strip()
h = open(f"{S}/reels.html").read()

h = h.replace("--g1:#e8a05c; --g2:#f5d7a1;", "--g1:#2ed14f; --g2:#c9ff4a;")
h = h.replace("rgba(232,160,92,.26)", "rgba(46,209,79,.30)")
h = h.replace("<title>Reels | Tape Emulation VST3/AU Plugin</title>",
              "<title>Gremlin | Glitch, Stutter and Granular Mangler VST3/AU Plugin</title>")
h = h.replace('content="Reels is a tape machine plugin (VST3 and AU for macOS). Real tape saturation, wow and flutter, in the box. By Sebastian Macan."',
              'content="Gremlin is the glitch box for beats: tempo-synced chops, pitched stutters and granular smear into a plate reverb. One plugin, three sections. VST3 and AU. By Sebastian Macan."')
h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Gremlin",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Gremlin is the glitch box for beats: tempo-synced chops, pitched stutters and granular smear into a plate reverb. One plugin, three switchable sections. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/gremlin.html",
   "offers": { "@type": "Offer", "price": "15", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "How much is Gremlin?",
      "acceptedAnswer": { "@type": "Answer", "text": "Gremlin is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription." } },
    { "@type": "Question", "name": "Is Gremlin three plugins?",
      "acceptedAnswer": { "@type": "Answer", "text": "No. Gremlin is one plugin with three switchable sections: CHOP, STUTTER and SMEAR. All three sit side by side, each with its own ON switch, so you can run one, two or all three at once." } },
    { "@type": "Question", "name": "What DAWs does Gremlin work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Gremlin?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Gremlin ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both. One purchase covers both platforms." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = '''  <section class="hero">
    <div class="kind">The Mangler Box</div>
    <h1>GREMLIN</h1>
    <p class="tag">Chop it. Stutter it. Smear it. The glitch box for beats.</p>
    <div class="videobox"><video autoplay muted loop playsinline poster="img/ui/gremlin.png?v=3.1.0"><source src="img/video/gremlin_ui_loop.mp4?v=3.1.0" type="video/mp4"></video></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlin">Buy Gremlin &middot; $15</span>
      <div class="meta">v3.1.0 &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What Gremlin does</h2>
  <p>$15 buys you the mangler box. Gremlin takes a boring loop and breaks it on purpose: tempo-synced gate chops, buffer stutters that pitch every repeat, and a granular smear that melts your beat into a plate reverb. It is an effect, not an instrument. Put it on drums, chords, vocals, the whole bus, and turn a straight loop into a moment.</p>

  <h2>Three sections, one box</h2>
  <div class="vidstack">
    <div class="big" data-vid><video preload="none" playsinline poster="img/ui/gremlin_demo.jpg?v=3.1.0d"><source src="img/video/gremlin_demo.mp4?v=3.1.0d" type="video/mp4"></video><span>Before / after, in Ableton</span><i class="play"></i></div>
    <div class="big" data-vid style="margin-top:12px"><video preload="none" playsinline poster="img/ui/gremlin_production.jpg?v=1"><source src="img/video/gremlin_production.mp4?v=2" type="video/mp4"></video><span>Sebastian using Gremlin in his production</span><i class="play"></i></div>
    <div class="vidhint">Tap to play. Sound on.</div>
  </div>
  <div class="bot"><b>CHOP.</b> A tempo-synced gate and slicer. Pick a rate from 1/4 down to 1/32, set the GATE length, choose a pattern or roll a new one with the seed. Instant trance gates, triplet holes and rhythmic silence that always lands on the grid.</div>
  <div class="bot"><b>STUTTER.</b> Buffer repeats on demand. RATE sets the slice, REPEATS how many times it fires, REVERSE flips them backwards, and PITCH is true pitch from -12 to +12 semitones. Every repeat in a burst shares one interval, so stutters stay musical instead of turning to mush. Noon is 0 st, plain repeats.</div>
  <div class="bot"><b>SMEAR.</b> Grain blur into a Dattorro plate reverb. WASH sets how much of the signal melts, DECAY runs from 0.6 s to 14 s, DEPTH pushes the verb further back in the room, TONE darkens or opens it, SHIMMER adds a +12 st feedback pitch shift, and FREEZE holds the tail forever.</div>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Gremlin on a loop.</b> Drums are the classic. It opens on Init: Stutter only, at 1/8, so you hear it working immediately.</div>
  <div class="step"><b>2. Switch on the gremlins you want.</b> CHOP for rhythmic holes, STUTTER for repeats and pitch tricks, SMEAR to melt it into reverb. Run one, or all three at once; each keeps its own settings.</div>
  <div class="step"><b>3. Raid the presets.</b> Machine Gun, Frozen Lake, Full Meltdown. Find one that ruins your loop in the right way, then tweak and save your own.</div>

  <h2>Make it yours</h2>
  <div class="knob"><b>CHOP: RATE.</b> Tempo-synced slice size, 1/4 down to 1/32. Always on your DAW's grid.</div>
  <div class="knob"><b>CHOP: GATE.</b> How long each slice stays open. Short is choppy, long is pumping.</div>
  <div class="knob"><b>CHOP: PATTERNS + SEED.</b> Pick a gate pattern or roll the seed for a new one. Same seed, same pattern, every time.</div>
  <div class="knob"><b>STUTTER: RATE and REPEATS.</b> Slice size and how many times the buffer fires.</div>
  <div class="knob"><b>STUTTER: REVERSE.</b> Plays the repeats backwards. Instant tape-rewind moments.</div>
  <div class="knob"><b>STUTTER: PITCH.</b> True pitch, -12 to +12 semitones. All repeats in a burst share one interval; noon is 0 st.</div>
  <div class="knob"><b>SMEAR: WASH and DECAY.</b> How much melts, and for how long: 0.6 s up to a 14 s tail.</div>
  <div class="knob"><b>SMEAR: DEPTH.</b> Predelay, early/late balance and a high-cut in one move, so the verb sits further back instead of on top.</div>
  <div class="knob"><b>SMEAR: TONE, SHIMMER, FREEZE and MIX.</b> Darken or open the tail, add a +12 st shimmer to the feedback, freeze it forever, blend it in.</div>
  <div class="knob"><b>PRESETS + INIT.</b> Preset dropdown in the header, save unlimited of your own. Right-click, two-finger tap or Cmd-click any knob for INIT: that one control snaps back to the preset you loaded.</div>

  <h2>Presets</h2>
  <p>12 to start: Init, Chop, Smear, Gentle Hiccup, Plucky Cloud, Rewind Room, Machine Gun, Frozen Lake, Broken Toy, Tape Chewer, Sugar Rush and Full Meltdown. From polite hiccups to a beat that no longer exists.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>How much is Gremlin?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>
  <div class="knob"><b>Is Gremlin three plugins?</b> No. One plugin with three switchable sections: CHOP, STUTTER and SMEAR. All three sit side by side, each with its own ON switch, so you can run one, two or all three at once.</div>
  <div class="knob"><b>What DAWs does Gremlin work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Gremlin?</b> Yes. Gremlin ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both. One purchase covers both platforms.</div>
  <div class="knob"><b>How do I install Gremlin?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="gremlin">Buy Gremlin &middot; $15</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
h = h.replace("  .videobox video { display:block; width:100%; height:auto; }",
              "  .videobox video { display:block; width:100%; height:auto; }\n" + VIDCSS.replace("#0b0806", "#07100a"))
h = h.replace("</body>", "<script>"+JS+"</script>\n</body>")
open(f"{S}/gremlin.html", "w").write(h); print("wrote gremlin.html", len(h))
