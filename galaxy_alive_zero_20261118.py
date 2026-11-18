#!/usr/bin/env python3
"""Nov 18 2026 (Alex), Gremlin Basket page:
 (1) price reads $0 instead of the word FREE (big price + the five row tags);
 (2) candy galaxy background (js/galaxy.js) - the wormhole landing now brakes, then fades into the galaxy;
 (3) the five gremlin faces get barely-there idles (marketing/cast-anim/out_alive, same paint code as the plugins).
Anchored edits with asserts, one write per file. --dry prints only."""
import os, sys, shutil
S = os.path.dirname(os.path.abspath(__file__)) + "/"
DRY = "--dry" in sys.argv
ALIVE = S + "../marketing/cast-anim/out_alive/"

p = S + "basket-gremlin.html"; g = open(p).read(); g0 = g
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a, s.count(a))
    return s.replace(a, b)
g = rep(g, '<span class="big freebie">FREE</span>', '<span class="big freebie">$0</span>')
g = rep(g, '<div class="freetag">FREE</div>', '<div class="freetag">$0</div>', 5)
g = rep(g, '<body data-space>', '<body data-space data-galaxy>')
g = rep(g, '<script src="js/wormhole.js?v=1" defer></script>', '<script src="js/galaxy.js?v=1" defer></script>\n<script src="js/wormhole.js?v=2" defer></script>')
for n in ("smear", "stutter", "twitch", "chop", "scrap"):
    g = rep(g, f'<img class="gface" src="img/gremlinad/{n}.png?v=1" alt="">', f'<img class="gface" src="img/gremlinad/alive/{n}.webp?v=1" alt="">')

w = S + "js/wormhole.js"; j = open(w).read(); j0 = j
j = rep(j, "    if (REDUCED) arrived = false;\n",
        "    if (REDUCED) arrived = false;\n"
        "    var GALAXY = document.body.hasAttribute('data-galaxy');     /* js/galaxy.js owns the background: we only do the arrival */\n"
        "    if (GALAXY && !arrived) return;\n")
j = rep(j, "    document.body.insertBefore(c, document.body.firstChild);\n    var stars = makeStars(Math.round(Math.min(700",
        "    var gx = document.getElementById('sm-galaxy');\n"
        "    document.body.insertBefore(c, gx ? gx.nextSibling : document.body.firstChild);\n    var stars = makeStars(Math.round(Math.min(700")
j = rep(j, "      if (REDUCED) return;\n      requestAnimationFrame(frame);\n    }\n    requestAnimationFrame(frame);\n  }",
        "      if (REDUCED) return;\n"
        "      if (GALAXY && t > 0.55) {                                   /* braking done: melt into the candy galaxy */\n"
        "        var o = 1 - (t - 0.55) / 0.45; c.style.opacity = String(Math.max(0, o));\n"
        "        if (t >= 1) { c.remove(); return; }\n"
        "      }\n"
        "      requestAnimationFrame(frame);\n    }\n    requestAnimationFrame(frame);\n  }")

print("basket-gremlin.html", "changed" if g != g0 else "same", "| wormhole.js", "changed" if j != j0 else "same")
if not DRY:
    os.makedirs(S + "img/gremlinad/alive", exist_ok=True)
    for n in ("smear", "stutter", "twitch", "chop", "scrap"):
        shutil.copy2(ALIVE + n + ".webp", S + f"img/gremlinad/alive/{n}.webp")
    open(p, "w").write(g); open(w, "w").write(j)
