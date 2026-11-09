#!/usr/bin/env python3
"""Generate smear.html / stutter.html / twitch.html (the Gremlin split, Nov 9 2026) from the house template gremlin.html.
Run from ~/sebastianmacan/site. Idempotent. Modelled on gen_taffy.py. Presets lists come from each plugin's factoryPresetOrder()."""
import re, os, sys
S = os.path.dirname(os.path.abspath(__file__))

def faq_ld(name, pairs):
    return ",\n".join('    { "@type": "Question", "name": "%s",\n      "acceptedAnswer": { "@type": "Answer", "text": "%s" } }' % (q, a) for q, a in pairs)

def build(slug, NAME, ver, g1, g2, rgb, title, meta, ld_desc, kind, tagline, aria, what, why_h, why, knobs_h, knobs, steps, yours, presets, faqs, ld_faqs):
    h = open(f"{S}/_tpl/product.html").read().replace('<meta name="robots" content="noindex">\n', "")
    h = h.replace("--g1:#ff4fa3; --g2:#ff7ab8;", f"--g1:{g1}; --g2:{g2};")
    h = re.sub(r"rgba\(255,79,163,(\.\d+)\)", r"rgba(%s,\1)" % rgb, h)
    assert f"--g1:{g1}" in h and "255,79,163" not in h
    h = re.sub(r"<title>.*?</title>", f"<title>{title}</title>", h)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{meta}">', h)
    h = re.sub(r'<script type="application/ld\+json">.*?</script>', '''<script type="application/ld+json">
{
 "@context": "https://schema.org",
 "@graph": [
  {
   "@type": "SoftwareApplication",
   "name": "%s",
   "operatingSystem": "macOS, Windows",
   "applicationCategory": "MultimediaApplication",
   "applicationSubCategory": "Audio plugin (VST3, AU)",
   "description": "%s",
   "url": "https://sebastianmacan.com/%s.html",
   "offers": { "@type": "Offer", "price": "15", "priceCurrency": "USD" },
   "author": { "@type": "Person", "name": "Sebastian Macan" },
   "publisher": { "@type": "Organization", "name": "Aluetion, LLC", "url": "https://sebastianmacan.com" }
  },
  {
   "@type": "FAQPage",
   "mainEntity": [
%s
   ]
  }
 ]
}
</script>''' % (NAME, ld_desc, slug, faq_ld(NAME, ld_faqs)), h, flags=re.S)

    body_start = h.index('  <section class="hero">'); body_end = h.index('  <footer>')
    knob_html = "\n".join(f'  <div class="bot"><b>{k}.</b> {v}</div>' for k, v in knobs)
    step_html = "\n".join(f'  <div class="step"><b>{i+1}. {k}</b> {v}</div>' for i, (k, v) in enumerate(steps))
    yours_html = "\n".join(f'  <div class="knob"><b>{k}.</b> {v}</div>' for k, v in yours)
    faq_html = "\n".join(f'  <div class="knob"><b>{q}</b> {a}</div>' for q, a in faqs)
    body = f'''  <section class="hero">
    <div class="kind">{kind}</div>
    <h1>{NAME.upper()}</h1>
    <p class="tag">{tagline}</p>
    <div class="videobox"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/{slug}.png?v={ver}" aria-label="{aria}"><source src="https://video.sebastianmacan.com/img/video/{slug}_ui_loop.mp4?v={ver}" type="video/mp4"></video></div>
    <div class="cta">
      <span class="dl buy" role="button" tabindex="0" data-cart-buy="{slug}">Buy {NAME} &middot; $15</span>
      <div class="meta">v{ver} &middot; VST3 + AU effect &middot; macOS + Windows</div>
    </div>
  </section>

  <h2>What {NAME} does</h2>
  <p>{what}</p>

  <h2>{why_h}</h2>
  <p>{why}</p>

  <h2>{knobs_h}</h2>
{knob_html}

  <h2>Get started in 3 steps</h2>
{step_html}

  <h2>Make it yours</h2>
{yours_html}

  <h2>Presets</h2>
  <p>{presets}</p>

  <h2>Common questions</h2>
  <div class="knob"><b>How much is {NAME}?</b> $15, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.</div>
{faq_html}
  <div class="knob"><b>What DAWs does {NAME} work in?</b> Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more.</div>
  <div class="knob"><b>Is there a Windows version of {NAME}?</b> Yes. {NAME} ships for macOS (VST3 + AU) and Windows (VST3), code-signed on both. One purchase covers both platforms.</div>
  <div class="knob"><b>How do I install {NAME}?</b> Run the installer and it puts the plugin files in the right folders. Restart your DAW, rescan if needed, done.</div>

  <div class="cta">
    <span class="dl buy" role="button" tabindex="0" data-cart-buy="{slug}">Buy {NAME} &middot; $15</span>
    <div class="meta">Email required &middot; instant download</div>
  </div>

'''
    h = h[:body_start] + body + h[body_end:]
    open(f"{S}/{slug}.html", "w").write(h); print(f"wrote {slug}.html", len(h))

P = {}
P["smear"] = dict(slug="smear", NAME="Smear", ver="1.0.0", g1="#9a6bff", g2="#44e0c8", rgb="154,107,255",
    title="Smear | Granular Smear and Plate Reverb VST3/AU Plugin",
    meta="Smear melts any sound into a cloud. Grain blur into a plate reverb with PITCH, BLUR, WASH, DECAY, SHIMMER and FREEZE. VST3 and AU, macOS and Windows. By Sebastian Macan.",
    ld_desc="Smear is a granular smear into a plate reverb. SMEAR sets how dense the grain cloud is, PITCH throws grains up an octave, a fifth or down an octave, BLUR smudges them, WASH and DECAY run the plate from 0.6 s to 14 s, SHIMMER adds a +12 st feedback shift, FREEZE holds the tail forever. By Sebastian Macan.",
    kind="Granular Smear", tagline="Melts anything into a cloud.",
    aria="Smear plugin UI: a violet melting creature dripping while WASH and DECAY sweep",
    what="Smear takes whatever you feed it and melts it. The incoming sound gets cut into a cloud of grains, some of them thrown up an octave or a fifth, smudged by a feedback delay, then poured into a plate reverb that runs from a short room to a 14 second wash. A dry drum loop turns into a pad. A vocal turns into a choir in the next room. Turn SMEAR up and the edges go, turn WASH up and the whole thing dissolves, hit FREEZE and the tail hangs there for as long as you want it.",
    why_h="Melty, the readout", why="The violet creature in the panel is the meter. It drips with the wash and melts harder the more you smear, so you can see how far gone the sound is before you hear it.",
    knobs_h="Ten controls, one cloud",
    knobs=[("SMEAR", "How dense the grain cloud is. Zero is clean, full is soup."),
           ("PITCH", "Chance a grain plays +12, +7 or -12 semitones. A little is sparkle, a lot is a choir."),
           ("BLUR", "A feedback delay that smudges the grains. Low keeps the groove, high turns rhythm into texture."),
           ("WASH", "Reverb amount behind the cloud."),
           ("DECAY", "Reverb tail, 0.6 s to 14 s."),
           ("DEPTH", "Predelay, early/late balance and a high-cut in one move, so the verb sits further back instead of on top."),
           ("SHIMMER", "A +12 st pitch shift in the reverb feedback. Every pass climbs an octave."),
           ("TONE", "Dark to bright on the wet sound only."),
           ("DRIFT", "Slow wobble of grain pitch and delay time, so a long tail never sits still."),
           ("FREEZE", "Holds the grains and an endless reverb while lit. Play over it, then let go.")],
    steps=[("Put Smear on something.", "A drum loop, a chord stab, a vocal phrase. It opens on Init, already wet."),
           ("Turn WASH and DECAY up.", "The sound starts to pour out behind itself. Stop where it still feels like your track."),
           ("Hit FREEZE at the right moment.", "The tail hangs. Automate it on a transition and let it go on the drop.")],
    yours=[("MIX and OUT", "Blend the cloud with the dry sound, trim the result. BYPASS pill in the header for an honest A/B."),
           ("ON pill", "The switch in the panel corner. Off dims the box and passes the dry signal, same as inside the mangler."),
           ("INIT ANY KNOB", "Right-click or Cmd-click a knob to send it home."),
           ("Window size", "Opens compact. Drag the corner grip to make it as big as you like; your DAW remembers it.")],
    presets="__PRESETS__",
    faqs=[("Is Smear a reverb?", "It is a reverb with a granular front end. The plate alone is a proper Dattorro plate; SMEAR, PITCH, BLUR and DRIFT are what make it melt instead of just echo.")],
    ld_faqs=[("How much is Smear?", "Smear is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription."),
             ("Is Smear a reverb?", "It is a plate reverb with a granular front end: grains of the input get blurred and pitched before the plate, so sounds melt instead of just echoing."),
             ("What DAWs does Smear work in?", "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more."),
             ("Is there a Windows version of Smear?", "Yes. Smear ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.")])

P["stutter"] = dict(slug="stutter", NAME="Stutter", ver="2.0.0", g1="#ff2ea6", g2="#ff7ad1", rgb="255,46,166",
    title="Stutter | Beat Repeat and Buffer Stutter VST3/AU Plugin",
    meta="Stutter is a beat repeat with dice. AMOUNT, RATE, REPEATS, RAMP, REVERSE, true PITCH, TAPE, SCATTER and a patch bay you can click. VST3 and AU, macOS and Windows. By Sebastian Macan.",
    ld_desc="Stutter is a tempo-synced buffer stutter. AMOUNT is the chance a repeat fires per step, RATE from 1/1 to 1/32 or FREE in milliseconds, REPEATS, RAMP, REVERSE, PITCH from -12 to +12 st, TAPE, SCATTER, SHAPE, FILTER, WIDTH, GLIDE, DECLICK and HOLD. By Sebastian Macan.",
    kind="Beat Repeat", tagline="Repeats it until it is a new idea.",
    aria="Stutter plugin UI: a purple jittering creature next to a patch bay while AMOUNT and PITCH sweep",
    what="Stutter grabs a slice of whatever is playing and fires it again. Not on every beat: AMOUNT is the dice, the chance that a repeat happens on each step of the grid. RATE picks the grid from whole bars down to 1/32, or FREE in milliseconds with no transport at all. REPEATS, RAMP and REVERSE shape the burst, PITCH moves every repeat up to an octave either way, and TAPE, SCATTER, SHAPE, FILTER, WIDTH and GLIDE turn one repeat into a trick. HOLD freezes the buffer while you lean on it.",
    why_h="Jitter and the patch bay", why="The purple creature is Jitter. It twitches with every repeat. Next to it is the patch bay: HOLD plugs the dangling cable into the free socket, and you can click any cable to grey it out. The cables are toys. Nothing breaks if you play with them.",
    knobs_h="Sixteen controls, one grid",
    knobs=[("AMOUNT", "The chance a repeat fires on each step. 0% is silence from the engine, 100% is every step."),
           ("RATE and FREE", "Slice size, 1/1 down to 1/32. Pick FREE and the clock runs off the FREE knob, 10 to 2000 ms, transport stopped or not."),
           ("REPEATS and RAMP", "How many times the slice fires, and whether each repeat shrinks."),
           ("REVERSE", "Chance a burst plays backwards. Instant tape-rewind moments."),
           ("PITCH and GLIDE", "True pitch, -12 to +12 semitones, noon is 0. GLIDE ramps the pitch across the burst."),
           ("TAPE and SCATTER", "Chance a burst becomes a tape-stop or tape-start, and chance a repeat reads from an older point in the buffer."),
           ("SHAPE and FILTER", "Gain shape across the burst: square, triangle or swell. FILTER sweeps a low-pass closed or a high-pass open across it."),
           ("WIDTH", "Alternate repeats pan left and right."),
           ("DECLICK", "Finds the hard edges a repeat copies in and smooths only those few milliseconds. The other side of the knob is PUNCH."),
           ("PATTERN", "DICE is the classic. EVERY BAR, EVERY 2 BARS, FILL 4, ACCEL and TRIPLET lock the bursts to the song."),
           ("SEED", "Same seed, same dice, every time. Change it for a new roll."),
           ("HOLD", "Freezes the buffer and fires it for as long as you hold.")],
    steps=[("Put Stutter on a loop.", "Drums are the classic. It opens on Init at 1/8, so you hear it working immediately."),
           ("Set AMOUNT.", "A quarter turn is a fill every few bars. Full is a machine gun."),
           ("Add one trick.", "REVERSE for rewinds, PITCH up an octave for the chipmunk, TAPE for stops, SCATTER for chaos. Then save it.")],
    yours=[("MIX and OUT", "Blend the repeats with the dry loop, trim the result. BYPASS pill in the header for an honest A/B."),
           ("ON and REPEAT pills", "ON dims the box and passes dry. REPEAT is the classic engine; switch it off and TAPE, SCATTER, REVERSE, PITCH and FILTER act on the live signal per step instead."),
           ("INIT ANY KNOB", "Right-click or Cmd-click a knob to send it home."),
           ("Window size", "Opens compact. Drag the corner grip to make it as big as you like; your DAW remembers it.")],
    presets="__PRESETS__",
    faqs=[("Does it work without the transport running?", "Yes. Pick FREE in RATE and the step clock runs off the FREE knob in milliseconds. Jam on it live.")],
    ld_faqs=[("How much is Stutter?", "Stutter is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription."),
             ("Does Stutter work without the transport running?", "Yes. Pick FREE in RATE and the step clock runs off the FREE knob in milliseconds, 10 to 2000 ms."),
             ("What DAWs does Stutter work in?", "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more."),
             ("Is there a Windows version of Stutter?", "Yes. Stutter ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.")])

P["twitch"] = dict(slug="twitch", NAME="Twitch", ver="1.0.0", g1="#3cdcff", g2="#9aefff", rgb="60,220,255",
    title="Twitch | Per-Step Glitch Rack VST3/AU Plugin",
    meta="Twitch is a per-step glitch rack. GATE, CRUSH, WARP, COMB, GRAIN, GLITCH, FORMANT, RING, CHAOS and SKETCH, a draw pad, all firing on the grid. VST3 and AU, macOS and Windows. By Sebastian Macan.",
    ld_desc="Twitch is a tempo-synced per-step effect rack. Twelve knobs that each fire on the step grid: GATE, CRUSH, WARP, COMB and TUNE, GRAIN, GLITCH, FORMANT, RING and HZ, CHAOS, and SKETCH, a 16-slot draw pad with TIME, VOL and MAD modes. By Sebastian Macan.",
    kind="Per-Step Glitch Rack", tagline="Twelve effects. One grid. Draw the rest.",
    aria="Twitch plugin UI: a cyan creature sparking next to a sketch pad while rack knobs move on the grid",
    what="Twitch is a rack of twelve effects that all fire on the same tempo grid. Pick a RATE, then turn up what you want: GATE for trance gates, CRUSH for bit and sample-rate decimation, WARP for tape-stop dives and tape-start rises on every step, COMB for a tuned ring, GRAIN for a rhythm-locked grain cloud, GLITCH for buffer jumps and micro-repeats, FORMANT for a vowel sweep, RING for a modulator that swoops down to its pitch each step. CHAOS re-rolls every knob you turned up, once a bar, around where you left it. And SKETCH is the draw pad.",
    why_h="Zappy and the sketch pad", why="The cyan creature is Zappy. It twitches with whatever you touch. Under it is the pad: draw 16 bars across one bar of music. TIME mode reads the audio back in time by what you drew, the Gross Beat move. VOL mode is a drawn gate. MAD mode turns each bar you drew into a random seeded event, micro-repeat, reverse, crush or a ring hit, as hard as you drew it. Same drawing, same SEED, same result.",
    knobs_h="Twelve knobs, one grid",
    knobs=[("RATE and FREE", "The step grid every knob fires on, 1/1 down to 1/32, or FREE in milliseconds with the transport stopped."),
           ("GATE", "Trance gate on the grid. SHAPE of the gate follows the step."),
           ("CRUSH", "Bit-crush and decimate, with drive. Full is about 4 bits."),
           ("WARP", "Per-step pitch bend. Left is a tape-stop dive, right is a tape-start rise."),
           ("COMB and TUNE", "A tuned feedback comb that rings on each event, 40 Hz to 2 kHz."),
           ("GRAIN", "Freeze-and-scrub grain cloud of the captured step."),
           ("GLITCH", "Chance per step of a buffer jump, a skip or a micro-repeat."),
           ("FORMANT", "Vowel morph, A to U, swept per step."),
           ("RING and HZ", "Ring modulator, 20 Hz to 2 kHz, swooping down to its pitch on every step."),
           ("CHAOS", "Once a bar, re-rolls every other knob around where you left it. A knob at zero stays at zero, so turn something up first."),
           ("SKETCH and MODE", "How much of the drawing you hear, and whether it is TIME, VOL or MAD."),
           ("SEED", "Same seed, same chaos, same MAD events. Change it for a new roll.")],
    steps=[("Put Twitch on a loop.", "Drums or a chord loop. It opens on Init with everything at zero, so it passes clean."),
           ("Turn up one knob.", "GATE at half is a trance gate. CRUSH at half is a broken radio. WARP left is a tape stop on every step."),
           ("Draw on the pad.", "Drag across it, set MODE to TIME, turn SKETCH up. Right-click clears it.")],
    yours=[("MIX and OUT", "Blend the rack with the dry signal, trim the result. BYPASS pill in the header for an honest A/B."),
           ("ON pill", "The switch in the panel corner. Off dims the box and passes dry."),
           ("INIT ANY KNOB", "Right-click or Cmd-click a knob to send it home."),
           ("Window size", "Opens compact. Drag the corner grip to make it as big as you like; your DAW remembers it.")],
    presets="__PRESETS__",
    faqs=[("Does every knob run at once?", "Yes. Each knob is its own effect on the same grid. Turn up one, or all twelve.")],
    ld_faqs=[("How much is Twitch?", "Twitch is $15, one-time. Instant download after checkout, full version, no locked knobs, no subscription."),
             ("Does every Twitch knob run at once?", "Yes. Each of the twelve knobs is its own effect on the same tempo grid. Turn up one, or all of them."),
             ("What DAWs does Twitch work in?", "Any DAW that loads VST3 or AU plugins: Ableton Live, Logic Pro, FL Studio, GarageBand, Reaper, Studio One and more."),
             ("Is there a Windows version of Twitch?", "Yes. Twitch ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.")])

PRESETS = {}
try:
    exec(open(f"{S}/split_presets.py").read(), PRESETS)
except FileNotFoundError:
    pass
for slug in (sys.argv[1:] or P):
    d = dict(P[slug])
    names = PRESETS.get(slug.upper())
    if names:
        d["presets"] = f"{len(names)} to start: " + ", ".join(names[:-1]) + f" and {names[-1]}. Save unlimited of your own."
    else:
        d["presets"] = "Preset stepper in the header, save unlimited of your own."
    build(**d)
