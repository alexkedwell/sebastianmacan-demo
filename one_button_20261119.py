"""Nov 19 2026 (Alex): description pages get ONE download button everywhere.
The button serves the visitor's own system (js/os-dl.js); a small text link under it offers the other one.
Also: Chop is free right now, not 'free forever'.
One-off, idempotent-ish: asserts on every replacement so a second run fails loudly instead of double-editing."""
import re, io

PAGES = {  # page: (Name, mac, win)
    "chop":    ("Chop",    "Chop-v1.1.3-macOS.pkg",    "Chop-v1.1.3-Windows-Setup.exe"),
    "stutter": ("Stutter", "Stutter-v2.0.3-macOS.pkg", "Stutter-v2.0.3-Windows-Setup.exe"),
    "twitch":  ("Twitch",  "Twitch-v1.1.1-macOS.pkg",  "Twitch-v1.1.1-Windows-Setup.exe"),
    "scrap":   ("Scrap",   "Scrap-v1.0.2-macOS.pkg",   "Scrap-v1.0.2-Windows-Setup.exe"),
    "smear":   ("Smear",   "Smear-v1.0.1-macOS.pkg",   "Smear-v1.0.1-Windows-Setup.exe"),
    "warble":  ("Warble",  "Warble-v1.4.0-macOS.pkg",  "Warble-v1.4.0-Windows-Setup.exe"),
    "jelly":   ("Jelly",   "Jelly-v1.1.0-macOS.pkg",   "Jelly-v1.1.0-Windows-Setup.exe"),
    "orbit":   ("Orbit",   "Orbit-v1.0-macOS.pkg",     "Orbit-v1.0-Windows-Setup.exe"),
}
CSS = ("  .dl.dl-alt { display:block; width:fit-content; margin:14px auto 0; padding:4px 6px; background:none; box-shadow:none;\n"
       "    color:var(--g1); font-size:14px; font-weight:700; border-radius:6px; text-decoration:underline; text-underline-offset:4px; }\n"
       "  .dl.dl-alt:hover { transform:none; }\n")
SCRIPT = '<script src="js/os-dl.js?v=1" defer></script>\n'


def rd(p): return io.open(p, encoding="utf-8").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)


def one(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a), n)
    return s.replace(a, b)


for page, (name, mac, win) in PAGES.items():
    p = page + ".html"; s = rd(p)
    m, w = "downloads/" + mac, "downloads/" + win
    new = (f'<a class="dl" href="{m}" data-mac="{m}" data-win="{w}">Download {name} Free</a>\n'
           f'{{ind}}<a class="dl dl-alt" href="{w}" data-mac="{m}" data-win="{w}" data-alt="1">Windows version</a>')
    two = re.compile(r'([ \t]*)<a class="dl" href="%s">Download %s Free &middot; macOS</a>\n[ \t]*<a class="dl dl-win" href="%s">Download %s Free &middot; Windows</a>'
                     % (re.escape(m), name, re.escape(w), name))
    single = re.compile(r'([ \t]*)<a class="dl" href="%s">Download %s Free</a>' % (re.escape(m), name))
    rx = two if two.search(s) else single
    s, n = rx.subn(lambda mo: mo.group(1) + new.replace("{ind}", mo.group(1)), s)
    assert n == 2, (page, n)
    # css right after the .dl:hover rule
    hov = re.search(r'[ \t]*\.dl:hover \{[^}]*\}\n', s); assert hov, page
    s = s[:hov.end()] + CSS + s[hov.end():]
    # helper script right before the email gate
    gate = re.search(r'<script src="js/email-gate\.js[^"]*" defer></script>\n', s); assert gate, page
    s = s[:gate.start()] + SCRIPT + s[gate.start():]
    # the gate asks for an email on every free download: say the same thing the sibling pages say
    if "No email needed &middot; direct download" in s:
        s = one(s, "No email needed &middot; direct download", "Email required &middot; instant download")
    if page == "chop":
        s = one(s, "Chomps any sound into a groove. Free forever.</p>", "Chomps any sound into a groove.</p>")
        s = one(s, "Yes. Free forever. Full version, every knob, no subscription.", "Yes. Full version, every knob, no subscription.", 2)
    wr(p, s); print("ok", p)

# home: Chop card + invisible data-win on the eight free cards so the one button serves Windows visitors too
s = rd("index.html")
s = one(s, "anything that sustains becomes a rhythm. Free forever.</p>", "anything that sustains becomes a rhythm.</p>")
blk = re.search(r'<div class="card chop">.*?</div>\n    </div>', s, re.S); assert blk
b2 = one(blk.group(0), "100% Free &middot; Forever", "100% Free")
s = s[:blk.start()] + b2 + s[blk.end():]
tot = 0
for page, (name, mac, win) in PAGES.items():
    a = f'href="downloads/{mac}"'
    c = s.count(a); assert c >= 1, page
    s = s.replace(a, f'{a} data-mac="downloads/{mac}" data-win="downloads/{win}"'); tot += c
gate = re.search(r'<script src="js/email-gate\.js[^"]*" defer></script>\n', s); assert gate
s = s[:gate.start()] + SCRIPT + s[gate.start():]
wr("index.html", s); print("ok index.html, data-win on", tot, "buttons")

s = rd("pricing.html")
s = one(s, '<tr><td>Chop</td><td>Free rhythm chopper</td><td class="price">FREE forever</td></tr>',
        '<tr><td>Chop</td><td>Free rhythm chopper</td><td class="price">FREE</td></tr>')
wr("pricing.html", s); print("ok pricing.html")

s = rd("candy-bag.html")
s = one(s, '<p class="itag">Chomps any sound into a groove. Free forever.</p>', '<p class="itag">Chomps any sound into a groove.</p>')
wr("candy-bag.html", s); print("ok candy-bag.html")

# keep the Chop generator telling the same story
s = rd("gen_chop.py")
s = one(s, "Chomps any sound into a groove. Free forever.</p>", "Chomps any sound into a groove.</p>")
s = one(s, "Yes. Chop is free forever. Full version", "Yes. Full version")
s = one(s, "Yes. Free forever. Full version", "Yes. Full version")
s = one(s, "No email needed &middot; direct download", "Email required &middot; instant download")
s, n = re.subn(r'<a class="dl" href="\{MAC\}">Download Chop Free &middot; macOS</a>\n([ \t]*)<a class="dl dl-win" href="\{WIN\}">Download Chop Free &middot; Windows</a>',
               lambda mo: '<a class="dl" href="{MAC}" data-mac="{MAC}" data-win="{WIN}">Download Chop Free</a>\n' + mo.group(1) +
                          '<a class="dl dl-alt" href="{WIN}" data-mac="{MAC}" data-win="{WIN}" data-alt="1">Windows version</a>', s)
assert n == 2
wr("gen_chop.py", s); print("ok gen_chop.py (text only; css/script not templated there, see this file)")
