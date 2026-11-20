"""Nov 19 2026 (Alex): 'Library' in the top menu on every page + email box ending #2.
Site only. The library page wording itself lives in delivery/library.py."""
import io, glob, re
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)

LINK = '<a class="libnav" href="https://dl.sebastianmacan.com/library">Library</a>'
done = []
for p in sorted(glob.glob("*.html") + glob.glob("gen_*.py") + glob.glob("_tpl/*.html")):
    s = rd(p)
    if "libnav" in s or "</a></nav>" not in s: continue
    n = s.count("</a></nav>")
    wr(p, s.replace("</a></nav>", "</a>" + LINK + "</nav>")); done.append(f"{p}x{n}")
print("menu link added:", len(done), "files:", " ".join(done))

# homepage on phones: the menu is a sideways-scrolling strip, so Library goes first where it can be seen
s = rd("index.html")
a = "  nav a { margin:0 10px; display:inline-block; }"
assert s.count(a) == 1
s = s.replace(a, a + "\n  nav { display:flex; } nav a, nav #smcart-tab { flex:0 0 auto; } nav a.libnav { order:-1; }")
wr("index.html", s)

s = rd("js/email-gate.js")
old = "with fresh links any time. No password.</p>"
assert s.count(old) == 1
s = s.replace(old, "with fresh links any time. No password to remember. Your email is the key: enter it on the Library page and we send you a sign-in code.</p>")
wr("js/email-gate.js", s)
n = 0
for p in glob.glob("*.html"):
    s = rd(p)
    if "js/email-gate.js?v=lib2" in s:
        wr(p, s.replace("js/email-gate.js?v=lib2", "js/email-gate.js?v=lib3")); n += 1
print("email box ending updated, version bumped on", n, "pages")
