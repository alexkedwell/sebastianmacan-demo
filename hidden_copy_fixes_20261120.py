"""Nov 20 2026 (Alex): site side of the hidden-copy fixes: email box, after-download panel, stale cart lines."""
import io, glob
def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def sub1(s, a, b):
    assert s.count(a) == 1, a[:60]
    return s.replace(a, b)
s = rd("js/email-gate.js")
s = sub1(s, "That email becomes your library: every plugin you grab is kept there, with fresh links any time. No password to remember. Your email is the key: enter it on the Library page and we send you a sign-in code.</p>",
            "The email you use becomes your library: sign in any time and you\\u2019ll find all your products there. No password to remember.</p>")
s = sub1(s, "Everything you grab is kept there, with fresh download links any time. Opening it emails you a sign-in code, no password.</p>",
            "Everything you download is kept there, ready to download again any time. To open it, enter your email and we send you a sign-in code. No password.</p>")
wr("js/email-gate.js", s)
s = rd("js/cart.js")
s = sub1(s, "setMsg('Paid checkout opens soon. Everything in the store is a free download during launch, so grab it from the product buttons for now.');",
            "setMsg('Checkout is not available right now. Please try again in a few minutes.');")
s = sub1(s, "setMsg('Checkout is not wired up yet for: '", "setMsg('Checkout is not available yet for: '")
wr("js/cart.js", s)
n = 0
for p in glob.glob("*.html") + glob.glob("_tpl/*") + glob.glob("gen_*.py"):
    s = rd(p); o = s
    s = s.replace("js/email-gate.js?v=lib3", "js/email-gate.js?v=lib4").replace("cart.js?v=free8", "cart.js?v=free9")
    if s != o: wr(p, s); n += 1
print("ok, version bumped on", n, "files")
