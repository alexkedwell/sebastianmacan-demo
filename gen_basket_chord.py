"""Build basket-chord.html from basket-midi.html (same skeleton, live-edited page = source of truth)."""
import re
s = open("basket-midi.html").read()
s = s.replace("<title>Midi Mega Basket | Sebastian Macan</title>", "<title>Chord Basket | Sebastian Macan</title>")
s = re.sub(r'<meta name="description" content="[^"]*">',
  '<meta name="description" content="Chordsmith plus every MIDI pack we make. The chord generator plugin, Hitmaker Chords, Tears, Club, Soul and all 7 mode packs. 4796 progressions and the machine that writes the next one.">', s)
s = s.replace("--g1:#ff5ca8; --g2:#8b5cf6;", "--g1:#60a5fa; --g2:#ff5ca8;")
s = s.replace("<h1>MIDI MEGA BASKET</h1>", "<h1>CHORD BASKET</h1>")
s = s.replace('<p class="tag">4796 progressions. The complete harmonic arsenal.</p>',
              '<p class="tag">Chordsmith plus every MIDI pack we make. All the chords, ever.</p>')
s = s.replace('src="img/bundles/midi_mega_bundle.png" alt="MIDI MEGA BASKET basket art"',
              'src="img/bundles/chord_bundle.png" alt="CHORD BASKET basket art"')
s = s.replace('<div class="pricebar"><span class="big">$49</span></div>', '<div class="pricebar"><span class="big">$69</span></div>')
s = s.replace('<div class="meta">11 packs · 4796 MIDI files · any DAW</div>',
              '<div class="meta">1 plugin + 11 packs · 4796 MIDI files · VST3 + AU · macOS · any DAW</div>')
s = s.replace('data-cart-buy="midimega">Buy MIDI Mega Basket &middot; $49</span>', 'data-cart-buy="chordbasket">Buy Chord Basket &middot; $69</span>')
s = s.replace('data-cart-add="midimega"', 'data-cart-add="chordbasket"').replace('data-cart-buy="midimega"', 'data-cart-buy="chordbasket"')
s = re.sub(r'<p class="sub">Every MIDI pack we make:.*?</p>',
  '<p class="sub">Chordsmith writes chords and melodies for you in any genre, key and mode, then you drag them straight into your DAW. The MIDI packs are 4796 finished progressions ready to drop in. Together they are the whole chord side of the store. Every item below is sold on its own too, or take the whole basket at once.</p>', s, flags=re.S)
row = '''    <div class="item">
      <div class="iinfo">
        <div class="ikind">Chord &amp; Melody Generator</div>
        <div class="iname">Chordsmith</div>
        <p class="itag">Pick a genre, key and mode, hit GENERATE. Chords and a melody, ready to drag into your DAW.</p>
        <a class="rowlink" href="chordsmith.html">See how it works &rarr;</a>
      </div>
      <div class="iact">
        <div class="iprice">$39</div>
        <span class="dl buy idl" role="button" tabindex="0" data-cart-buy="magician">Buy Chordsmith &middot; $39</span>
      </div>
    </div>
'''
s = s.replace('    <div class="item">\n      <div class="iinfo">\n        <div class="ikind">MIDI Chord Pack Series</div>', row + '    <div class="item">\n      <div class="iinfo">\n        <div class="ikind">MIDI Chord Pack Series</div>', 1)
s = s.replace('<div class="meta">One zip, everything inside. Download once, unzip, done.</div>',
              '<div class="meta">Two downloads: the Chordsmith installer and one zip with every MIDI pack inside.</div>')
s = re.sub(r'<div class="mathbox">.*?</div>',
  '<div class="mathbox">\n    Bought one by one this basket adds up to <b>$139</b>. As a basket it\'s <b>$69</b>, one-time. 1 plugin, 11 packs, zero catches.\n  </div>', s, flags=re.S)
open("basket-chord.html", "w").write(s)
print("midimega left:", s.count("midimega"), "| chordbasket:", s.count("chordbasket"), "| $69:", s.count("$69"))
