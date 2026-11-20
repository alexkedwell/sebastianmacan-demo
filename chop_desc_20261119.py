"""Nov 19 2026 (Alex's pick): Chop shop card description = 'Feed him a pad. He spits out a beat.'"""
import io
s = io.open("index.html", encoding="utf-8").read()
a = '<p class="desc">Anything that sustains becomes a rhythm.</p>'
assert s.count(a) == 1
s = s.replace(a, '<p class="desc">Feed him a pad. He spits out a beat.</p>')
io.open("index.html", "w", encoding="utf-8", newline="").write(s)
print("ok")
