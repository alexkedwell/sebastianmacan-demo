#!/usr/bin/env python3
"""Nov 18 2026 (Alex): (1) wormhole jump from the Gremlin card into the Gremlin Basket page, which now sits in the stars;
(2) bottom Candy Bag ad: the Jelly balloon and the Warble duck were clipped by the stage box -> stage no longer clips.
Run after gremlins_free_20261118.py. Idempotent."""
import os, sys
S = os.path.join(os.path.expanduser("~"), "sebastianmacan", "site")
def edit(name, pairs):
    p = os.path.join(S, name); s = open(p, encoding="utf-8").read(); o = s
    for old, new in pairs:
        if new in s and old not in s.replace(new, ""): continue
        if s.count(old) != 1: raise SystemExit("%s anchor x%d: %r" % (name, s.count(old), old[:90]))
        s = s.replace(old, new)
    if s != o: open(p, "w", encoding="utf-8").write(s)
    print(name, "changed" if s != o else "already done")

edit("index.html", [
    ('<div class="card gremlinad full" id="gremlinad" data-goto="basket-gremlin.html">', '<div class="card gremlinad full" id="gremlinad" data-goto="basket-gremlin.html" data-warp="basket-gremlin.html">'),
    ('<script src="js/loops.js?v=2" defer></script>\n  <script>\n  (function(){var c=document.getElementById(\'candyad\')', '<script src="js/loops.js?v=2" defer></script>\n<script src="js/wormhole.js?v=1" defer></script>\n  <script>\n  (function(){var c=document.getElementById(\'candyad\')'),
    ("  .candybag .candystage { width:min(100%, 380px); aspect-ratio:1/1; }", "  .candybag .candystage { width:min(100%, 380px); aspect-ratio:1/1; overflow:visible; }"),
])
edit("basket-gremlin.html", [
    ("<body>", "<body data-space>"),
    ("  .wrap { max-width:960px; margin:0 auto; padding:0 24px; }", "  .wrap { max-width:960px; margin:0 auto; padding:0 24px; position:relative; z-index:1; }\n  body[data-space] { background:#080516; }"),
    ('<script src="js/loops.js?v=2" defer></script>\n', '<script src="js/loops.js?v=2" defer></script>\n<script src="js/wormhole.js?v=1" defer></script>\n'),
])
