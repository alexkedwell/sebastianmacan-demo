#!/usr/bin/env python3
"""Generate site/honey.html (product page) + site/basket-tape.html (Tape Basket) from the house template.
Run from ~/sebastianmacan/site. Idempotent."""
import re, os
S = os.path.dirname(os.path.abspath(__file__))
tpl = open(f"{S}/reels.html").read()

# ---------- HONEY ----------
h = tpl
h = h.replace("--g1:#e8a05c; --g2:#f5d7a1;", "--g1:#f0a04a; --g2:#ffd98a;")
h = h.replace("rgba(232,160,92,.26)", "rgba(240,160,74,.30)")
h = h.replace("<title>Reels | Tape Emulation VST3/AU Plugin</title>", "<title>Honey | Tape Smoothness for Chords, Pads and Melodies (VST3/AU)</title>")
h = h.replace('content="Reels is a tape machine plugin (VST3 and AU for macOS). Real tape saturation, wow and flutter, in the box. By Sebastian Macan."',
              'content="Honey is a tape plugin built on real tape physics. Tape smoothness for chords, pads and melodies. Three machines, three faces. VST3 and AU. By Sebastian Macan."')
# JSON-LD block: rewrite wholesale
h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "Honey",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "Honey is a tape plugin built on real tape physics. Tape smoothness for chords, pads and melodies. Three machines, three faces. By Sebastian Macan.",
   "url": "https://sebastianmacan.com/honey.html",
   "offers": { "@type": "Offer", "price": "15", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
    { "@type": "Question", "name": "What is the difference between Honey and Reels?",
      "acceptedAnswer": { "@type": "Answer", "text": "Honey is tape smoothness for chords, pads and melodies: it takes the digital edge off and glues. Reels is dirty tape for lofi drums: it makes the vibe filthier. Same producer, different tracks. The Tape Basket has both for $22." } },
    { "@type": "Question", "name": "How much is Honey?",
      "acceptedAnswer": { "@type": "Answer", "text": "Honey is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription." } },
    { "@type": "Question", "name": "What DAWs does Honey work in?",
      "acceptedAnswer": { "@type": "Answer", "text": "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more. Logic and GarageBand pick up the AU version automatically." } },
    { "@type": "Question", "name": "Is there a Windows version of Honey?",
      "acceptedAnswer": { "@type": "Answer", "text": "Yes. Honey ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both." } }
   ]
  }
 ]
}
</script>''', h, flags=re.S)

body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
body = '''  <section class="hero">
    <div class="kind">Tape Smoothness</div>
    <h1>HONEY</h1>
    <p class="tag">Tape smoothness for chords, pads and melodies. Three machines, three faces.</p>
    <div class="faces">
      <span class="face on" data-face="cassette">CASSETTE</span><span class="face" data-face="studio">STUDIO</span><span class="face" data-face="walkman">WALKMAN</span>
    </div>
    <div class="videobox"><img id="honeyface" src="img/ui/honey_cassette.png?v=1.0.0" alt="Honey tape plugin, cassette face" width="1800" height="1160"></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="honey">Buy Honey &middot; $15</span>
      <div class="meta">v1.0.0 &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What Honey does</h2>
  <p>Honey is what happens to your chords when they get printed to good tape. It is built on real tape physics: the record and playback emphasis curves, magnetic hysteresis, gentle tape compression, head bump, high-frequency loss, wow and flutter and hiss, all modelled instead of faked. The result is not distortion. It is smoothness. Digital edges round off, sustains glue together, and pads sit back in the mix like they belong there.</p>

  <h2>Get started in 3 steps</h2>
  <div class="step"><b>1. Put Honey on your chords.</b> Keys, pads, guitars, melodies, vocals. It is warmer than dry with nothing touched.</div>
  <div class="step"><b>2. Pick a machine.</b> STUDIO is a two-inch deck at 15 ips: expensive glue. CASSETTE is the default: moderate hiss, a little wobble. WALKMAN is a worn tape on dying batteries: heavy wow, dropouts, a ceiling around 9 kHz. The whole face changes with it.</div>
  <div class="step"><b>3. Turn DRIVE until it smiles.</b> Then WARMTH for the head bump, WOBBLE for movement, AGE for years of wear. Save it as a preset when it is yours.</div>

  <h2>Honey and Reels</h2>
  <div class="step"><b>Honey is for chords, pads and melodies.</b> Tape smoothness. It takes the digital edge off and glues. <b>Reels is for lofi drums.</b> Dirty tape. It makes the vibe filthier. Same producer, different tracks in the same session. <a href="basket-tape.html" style="color:var(--g1);font-weight:800;">Tape Basket: both for $22 &rarr;</a></div>

  <h2>Make it yours</h2>
  <div class="knob"><b>DRIVE.</b> How hard you hit the tape. Low is glue, high is soft saturation that stays smooth because the highs saturate first.</div>
  <div class="knob"><b>WARMTH.</b> Head bump and low-mid weight, tuned per machine. Where chords get their body.</div>
  <div class="knob"><b>WOBBLE.</b> Wow and flutter. A little is human, a lot is a memory.</div>
  <div class="knob"><b>HISS.</b> Real tape noise, dosed to taste, machine-dependent. Cassette is louder, Studio is faint.</div>
  <div class="knob"><b>AGE.</b> Years of wear. Dulls the top, adds dropouts on Walkman, softens everything.</div>
  <div class="knob"><b>MIX and OUTPUT.</b> Parallel blend and level. Same positions on every face, so your hands always know where they are.</div>
  <div class="knob"><b>PRESETS + INIT.</b> Preset pill in the header, save unlimited of your own. Right-click, two-finger tap or Cmd-click any knob for INIT: that one control snaps back to the preset you loaded.</div>

  <h3>Pro tip</h3>
  <p>Put Honey on the chord bus in CASSETTE with DRIVE around 11 o'clock and WOBBLE just past off. Then put Reels on the drum bus. That is the lofi session in two plugins.</p>

  <h2>Common questions</h2>
  <div class="knob"><b>What is the difference between Honey and Reels?</b> Honey is tape smoothness for chords, pads and melodies. Reels is dirty tape for lofi drums. Same producer, different tracks. The Tape Basket has both for $22.</div>
  <div class="knob"><b>How much is Honey?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>
  <div class="knob"><b>What DAWs does Honey work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of Honey?</b> Yes. macOS (VST3 + AU) and Windows (VST3), code-signed on both.</div>
  <div class="knob"><b>How do I install Honey?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="honey">Buy Honey &middot; $15</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
h = h[:body_start] + body + h[body_end:]
h = h.replace("  .videobox video { display:block; width:100%; height:auto; }",
 "  .videobox img { display:block; width:100%; height:auto; }\n"
 "  .faces { display:flex; justify-content:center; gap:8px; margin-top:22px; }\n"
 "  .face { cursor:pointer; user-select:none; font-size:12px; font-weight:800; letter-spacing:.14em; padding:9px 18px; border-radius:999px; border:1px solid var(--line); color:var(--dim); background:var(--card); transition:all .15s; }\n"
 "  .face:hover { color:var(--txt); }\n"
 "  .face.on { color:#1a1208; background:linear-gradient(135deg,var(--g1),var(--g2)); border-color:transparent; box-shadow:0 6px 24px rgba(240,160,74,.30); }")
h = h.replace('<script src="js/email-gate.js" defer></script>',
 '<script src="js/email-gate.js" defer></script>\n<script>document.querySelectorAll(".face").forEach(function(f){f.addEventListener("click",function(){document.querySelectorAll(".face").forEach(function(x){x.classList.remove("on")});f.classList.add("on");var i=document.getElementById("honeyface");i.src="img/ui/honey_"+f.dataset.face+".png?v=1.0.0";i.alt="Honey tape plugin, "+f.dataset.face+" face";});});</script>')
open(f"{S}/honey.html", "w").write(h); print("wrote honey.html", len(h))

# ---------- TAPE BASKET basket ----------
b = open(f"{S}/basket-effects.html").read()
print("basket template markers:", "effectsbasket" in b, b.count("data-cart-buy"))
open("/tmp/basket_effects_ref.html", "w").write(b)
