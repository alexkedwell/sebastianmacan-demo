"""Nov 19 2026 (Alex): only Orbit is 'free forever'. Warble drops it. Chop card description shortened. Orbit card loses 'Pure rage-trap space.'"""
import io, re
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def one(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a), n)
    return s.replace(a, b)

s = rd("index.html")
blk = re.search(r'<div class="card warble">.*?</div>\n    </div>', s, re.S); assert blk
s = s[:blk.start()] + one(blk.group(0), "100% Free &middot; Forever", "100% Free") + s[blk.end():]
s = one(s, '<p class="desc">Tempo-synced gate with six rates, five patterns, swing and humanize. Pads, vocals, loops: anything that sustains becomes a rhythm.</p>',
        '<p class="desc">Anything that sustains becomes a rhythm.</p>')
s = one(s, " Tempo-synced, with a live orbit visual. Pure rage-trap space.</p>", " Tempo-synced, with a live orbit visual.</p>")
assert s.count("100% Free &middot; Forever") == 1  # Orbit only
wr("index.html", s)

s = rd("pricing.html")
s = one(s, '<tr><td>Warble</td><td>Bird pitch-wobble effect</td><td class="price">FREE forever</td></tr>',
        '<tr><td>Warble</td><td>Bird pitch-wobble effect</td><td class="price">FREE</td></tr>')
wr("pricing.html", s)

s = rd("candy-bag.html")
s = one(s, '<p class="itag">Make any sound sing like a weird little bird. Free forever.</p>', '<p class="itag">Make any sound sing like a weird little bird.</p>')
wr("candy-bag.html", s)
print("ok")
