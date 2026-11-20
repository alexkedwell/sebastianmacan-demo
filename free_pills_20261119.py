"""Nov 19 2026 (Alex): every free card says 'Free · Limited time' like Stutter. ONLY Orbit keeps '100% Free · Forever'."""
import io, re
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def one(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a), n)
    return s.replace(a, b)

s = rd("index.html")
for slug in ("warble", "chop"):
    blk = re.search(r'<div class="card %s">.*?</div>\n    </div>' % slug, s, re.S); assert blk, slug
    s = s[:blk.start()] + one(blk.group(0), ">100% Free</span>", ">Free &middot; Limited time</span>") + s[blk.end():]
assert s.count("100% Free &middot; Forever") == 1 and ">100% Free</span>" not in s
wr("index.html", s)

s = rd("pricing.html")
s = one(s, '<td>Bird pitch-wobble effect</td><td class="price">FREE</td>', '<td>Bird pitch-wobble effect</td><td class="price">FREE, limited time</td>')
s = one(s, '<td>Free rhythm chopper</td><td class="price">FREE</td>', '<td>Free rhythm chopper</td><td class="price">FREE, limited time</td>')
wr("pricing.html", s)

s = rd("candy-bag.html")
s = one(s, '<p class="itag">Chomps any sound into a groove.</p>', '<p class="itag">Chomps any sound into a groove. Free for a limited time.</p>')
s = one(s, '<p class="itag">Make any sound sing like a weird little bird.</p>', '<p class="itag">Make any sound sing like a weird little bird. Free for a limited time.</p>')
wr("candy-bag.html", s)
print("ok")
