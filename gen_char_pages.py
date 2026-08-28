#!/usr/bin/env python3
"""Generate product pages for the 3 new character plugins from the Jelly template.
Run from site dir: python3 gen_char_pages.py"""

TPL = open("jelly.html").read()

def build(slug, name, kind, tag, g1, g2, glow, desc_meta, what, steps, knobs, protip, faq1_q, faq1_a, pkg, av_type):
    h = TPL
    # colors
    h = h.replace("--g1:#ff7ab8; --g2:#8fe8c0;", f"--g1:{g1}; --g2:{g2};")
    h = h.replace("rgba(255,122,184,.26)", glow)
    # head
    h = h.replace("<title>Jelly | Free Wobble Effect VST3/AU Plugin</title>",
                  f"<title>{name} | Free {kind} VST3/AU Plugin</title>")
    h = h.replace("Jelly is a free wobble effect plugin (VST3 and AU for macOS). LFO-driven jiggle for basses, synths and anything that needs movement. By Sebastian Macan.",
                  desc_meta)
    h = h.replace('"name": "Jelly"', f'"name": "{name}"')
    h = h.replace("https://sebastianmacan.com/jelly.html", f"https://sebastianmacan.com/{slug}.html")
    # hero
    h = h.replace('<div class="kind">Wobble Machine</div>', f'<div class="kind">{kind}</div>')
    h = h.replace("<h1>JELLY</h1>", f"<h1>{name.upper()}</h1>")
    h = h.replace('<p class="tag">Make everything jiggle.</p>', f'<p class="tag">{tag}</p>')
    h = h.replace('poster="img/ui/jelly.png"', f'poster="img/ui/{slug}.png"')
    h = h.replace("img/video/jelly_ui_loop.mp4", f"img/video/{slug}_ui_loop.mp4")
    h = h.replace('href="downloads/Jelly-v1.0-macOS.pkg">Download Jelly Free</a>',
                  f'href="downloads/{pkg}">Download {name} Free</a>')
    h = h.replace("v1.0 &middot; VST3 + AU effect &middot; macOS", f"v1.0 &middot; VST3 + AU {av_type} &middot; macOS")
    # body copy
    h = h.replace("<h2>What Jelly does</h2>", f"<h2>What {name} does</h2>")
    import re
    h = re.sub(r"<p>Jelly is one huge wobbling blob.*?</p>", f"<p>{what}</p>", h, flags=re.S)
    steps_html = "\n".join(f'  <div class="step"><b>{i+1}. {b}</b> {t}</div>' for i, (b, t) in enumerate(steps))
    h = re.sub(r'  <div class="step"><b>1\..*?1/4 is a slow groove, faster rates get silly in the best way\.</div>',
               steps_html, h, flags=re.S)
    knobs_html = "\n".join(f'  <div class="knob"><b>{k}.</b> {t}</div>' for k, t in knobs)
    h = re.sub(r'  <div class="knob"><b>WOBBLE\..*?adds life to a static loop\.</div>',
               knobs_html, h, flags=re.S)
    h = re.sub(r"<p>Automate WOBBLE.*?</p>", f"<p>{protip}</p>", h, flags=re.S)
    # FAQ: swap first Q (concept) both in JSON-LD and visible; genericize the rest
    h = h.replace('"name": "What is a wobble effect?"', f'"name": "{faq1_q}"')
    h = h.replace('"text": "It moves the sound in rhythm, volume, filter and pitch wiggling together, so static sounds start to bounce and breathe. Classic for wobble bass in dubstep and house, but Jelly makes pads, keys and even vocals jiggle in time with your track."',
                  f'"text": "{faq1_a}"')
    h = h.replace("<b>What is a wobble effect?</b> It moves the sound in rhythm, volume, filter and pitch wiggling together, so static sounds start to bounce and breathe. Classic for wobble bass in dubstep and house, but Jelly makes pads, keys and even vocals jiggle in time with your track.",
                  f"<b>{faq1_q}</b> {faq1_a}")
    for a, b in [("Is Jelly really free?", f"Is {name} really free?"),
                 ("What DAWs does Jelly work in?", f"What DAWs does {name} work in?"),
                 ("Is there a Windows version of Jelly?", f"Is there a Windows version of {name}?"),
                 ("How do I install Jelly?", f"How do I install {name}?"),
                 ("Jelly makes pads", f"{name} makes pads")]:
        h = h.replace(a, b)
    open(f"{slug}.html", "w").write(h)
    print("wrote", f"{slug}.html")

build(
    "rusty", "Rusty", "Industrial Foley Machine",
    "Creaking doors. Groaning metal. Playable.",
    "#ff8c42", "#c9a227", "rgba(255,140,66,.26)",
    "Rusty is a playable industrial foley synth (VST3 and AU for macOS). Creaking doors, groaning ship hulls and ringing metal, pitched to your keys. By Sebastian Macan.",
    "Rusty is a little robot that turns your keyboard into a scrapyard. Every key plays real physical metal: creaks, groans, scrapes and clanks, all pitched to the note you play. The exact industrial textures you hear in huge electronic drops, now on tap.",
    [("Put Rusty on a MIDI track.", "He shows up as an instrument. Play a key and the metal rings."),
     ("Turn CREAK up slowly.", "That is the rusty door hinge. CRK RATE sets how fast it groans."),
     ("Pick a preset.", "Door of Doom, Ship Hull, Factory Ghost. 14 machines ready to play.")],
    [("MATERIAL", "Morphs the metal from rusty junk to a clean ringing bell."),
     ("CREAK", "Stick-slip friction, the sound of metal under strain. The character knob."),
     ("SCRAPE", "Adds grinding noise excitement, like dragging something heavy."),
     ("RING", "How long the metal rings after you let go. Short clank to nine-second wash."),
     ("RUST", "Grit. Drive and crunch for when the metal needs to feel dangerous."),
     ("SPACE", "Puts the whole scrapyard in a room, from closet to cathedral.")],
    "Play one low note with RING maxed and record 30 seconds. Chop that recording into a percussion kit and you have drums nobody else owns.",
    "What is an industrial foley synth?",
    "It synthesizes the sounds of physical metal, creaking doors, groaning hulls, struck beams, and lets you play them like an instrument, in tune with your song. No samples, every note is generated live.",
    "Rusty-v1.0-macOS.pkg", "instrument")

build(
    "mayday", "Mayday", "Riser Generator",
    "Hold a note. Brace for takeoff.",
    "#5ad0ff", "#ffb347", "rgba(90,208,255,.26)",
    "Mayday is a riser generator plugin (VST3 and AU for macOS). Hold one note and get a massive climbing riser, tempo-synced to your track, with an infinite-climb mode. By Sebastian Macan.",
    "Mayday is a little jet that makes huge risers on demand. Hold a note and the sound climbs for exactly 1, 2, 4 or 8 bars, then holds at the top until you let go. Truly intense risers are weirdly hard to find. Now they live on one key.",
    [("Put Mayday on a MIDI track.", "It is an instrument. One held note is all it needs."),
     ("Set LAUNCH to match your build.", "4 bars before the drop? Pick 4 bars. It lands exactly on time."),
     ("Hold the note until the drop hits.", "Release exactly on the downbeat. Clean fade, no mess.")],
    [("LAUNCH", "How long the climb takes. Tempo-synced bars or free seconds."),
     ("CLIMB", "How far it rises, 1 to 4 octaves. More octaves, more panic."),
     ("JET", "The engine-noise layer that sweeps up underneath. Adds the whoosh."),
     ("INFINITY", "Shepard mode. The riser climbs forever and never arrives. Unsettling in the best way."),
     ("SHAKE", "Flutter that speeds up near the top, like the airframe rattling."),
     ("AFTERBURN", "Drive and stereo width that kick in as you approach the peak.")],
    "Stack two Maydays an octave apart with slightly different LAUNCH times. The offset makes the rise feel enormous, like the whole mix is lifting off.",
    "What is a riser plugin?",
    "It generates the climbing tension sound before a drop or chorus. Instead of hunting sample packs for one that fits your key and tempo, Mayday builds the riser live from the note you hold, synced to your song.",
    "Mayday-v1.0-macOS.pkg", "instrument")

build(
    "warble", "Warble", "Drunk Songbird Pitch Wobbler",
    "Make any sound sing like a weird little bird.",
    "#2bb59a", "#ff9f43", "rgba(43,181,154,.26)",
    "Warble is a pitch-wobble effect plugin (VST3 and AU for macOS). Tempo-synced warble, random bird chirp gestures and a formant beak filter make any sound bend like a songbird. By Sebastian Macan.",
    "Warble is a googly-eyed bird that bends whatever you feed it. Smooth tempo-synced pitch wobble, sudden little chirp flicks, and a beak-shaped filter that opens and closes with the bend. Vocals, keys, guitars and pads come out warbling like they had a big night.",
    [("Put Warble on any track.", "Vocals and keys are magic, but the bird does not judge."),
     ("Turn WARBLE up until it bends.", "That is the wobble. SPEED locks it to your tempo."),
     ("Smash HATCH.", "Every hatch is a new bird with new habits. Type a seed to bring one back.")],
    [("WARBLE", "How far the pitch bends. Subtle tape drift to full drunk canary."),
     ("SPEED", "Wobble rate, synced to your tempo or free in Hz."),
     ("CHIRP", "Random quick pitch flicks, the birdiest part. More chirp, more chaos."),
     ("BEAK", "A formant filter that opens with the bend. Makes things vowel-y and alive."),
     ("FLUTTER", "Fast tremolo feathering on top of the wobble."),
     ("FEATHERS", "The mix knob. Blend the bird with your dry sound.")],
    "Print a vocal chop through Warble with CHIRP high, then pick your favorite three warbled notes and resample them as a hook. Instant character melody.",
    "What does a pitch wobbler do?",
    "It bends pitch in musical motion, like vibrato with a personality. Warble adds tempo-synced wobble plus randomized birdlike gestures, so static sounds turn into living, slightly unhinged ones.",
    "Warble-v1.0-macOS.pkg", "effect")
