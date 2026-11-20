"""Nov 19 2026 (Alex): ONE download button, nothing under it. The email box now says the Mac + Windows links get emailed too."""
import io, re, glob
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def one(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a), n)
    return s.replace(a, b)

ALT = re.compile(r'\n[ \t]*<a class="dl dl-alt"[^>]*data-alt="1">Windows version</a>')
CSS = re.compile(r'  \.dl\.dl-alt \{[^}]*\}\n  \.dl\.dl-alt:hover \{[^}]*\}\n')
for page in ("chop", "stutter", "twitch", "scrap", "smear", "warble", "jelly", "orbit"):
    p = page + ".html"; s = rd(p)
    s, n = ALT.subn("", s); assert n == 2, (page, n)
    s, n = CSS.subn("", s); assert n == 1, (page, n)
    assert "dl-alt" not in s
    wr(p, s)

s = rd("gen_chop.py")
s, n = re.subn(r'\n[ \t]*<a class="dl dl-alt"[^>]*data-alt="1">Windows version</a>', "", s); assert n == 2
wr("gen_chop.py", s)

s = rd("js/email-gate.js")
s = one(s, "Type your email and the download starts right away. That email becomes your library: every plugin you grab is kept there, with fresh download links any time. No password.",
        "Type your email and the download starts right away. We also email you the Mac and Windows download links. That email becomes your library: every plugin you grab is kept there, with fresh links any time. No password.")
wr("js/email-gate.js", s)

s = rd("js/os-dl.js")
s = one(s, " * Buttons carry data-mac / data-win. The main button serves the visitor's own system,\n * the small link under it (data-alt) offers the other one.\n",
        " * Buttons carry data-mac / data-win. The button serves the visitor's own system.\n * The other system's installer is in the welcome email and in the library.\n")
wr("js/os-dl.js", s)

n = 0
for p in glob.glob("*.html"):
    s = rd(p)
    if "js/email-gate.js?v=lib1" in s:
        wr(p, s.replace("js/email-gate.js?v=lib1", "js/email-gate.js?v=lib2")); n += 1
print("ok, gate version bumped on", n, "pages")
