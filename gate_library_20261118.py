#!/usr/bin/env python3
"""Nov 18 2026 (Alex): "the whole no account thing totally goes against everything we set up... they need to type in
their email and remember we create them an account so they have a library page".
 (1) js/email-gate.js: the email box says the email IS the library; after the download starts a panel confirms the
     library and links to it. A browser that already gave an email skips the box but still gets that panel
     (before: silent download, which read as "no account").
 (2) basket-gremlin.html: FREE back (not $0), LIMITED TIME ONLY under the price, buttons "Download for Mac/Windows",
     "No account, no catches" and "free forever" gone.
 (3) Smear/Stutter/Twitch/Gremlin Basket no longer say "forever" on the homepage or pricing page.
Anchored edits with asserts, one write per file. --dry prints only."""
import os, sys, glob
S = os.path.dirname(os.path.abspath(__file__)) + "/"
DRY = "--dry" in sys.argv
out = {}
def rep(s, a, b, n=1):
    assert s.count(a) == n, (a[:70], s.count(a))
    return s.replace(a, b)

# ---------- (1) email gate ----------
j = open(S + "js/email-gate.js").read()
j = rep(j, """ * capture endpoint, then starts the download.
""", """ * capture endpoint, then starts the download.
 * The email IS the customer's library account (dl.sebastianmacan.com/library, no password): the box says so,
 * and after every free download a panel confirms the library and links to it.
""")
j = rep(j, '''    ".eg-hp{position:absolute''', '''    ".eg-lib{display:block;text-align:center;text-decoration:none;border:none;cursor:pointer;color:#fff;font-weight:800;font-size:15px;padding:14px;border-radius:999px;letter-spacing:.02em;background:linear-gradient(135deg,var(--eg1),var(--eg2));box-shadow:0 8px 32px var(--egsh);transition:transform .15s}" +
    ".eg-lib:hover{transform:translateY(-1px)}" +
    ".eg-mail{color:#f2f2f4;font-weight:700;word-break:break-all}" +
    ".eg-row{display:flex;justify-content:center;gap:18px;margin-top:14px}" +
    ".eg-hp{position:absolute''')
j = rep(j, """      '<h3 class="eg-title">Get <em>' + name + '</em> + future updates</h3>' +
      '<p class="eg-sub">Drop your email and the download starts instantly. You\\u2019ll also get new presets, updates and future plugins first. Unsubscribe anytime.</p>' +""",
"""      '<h3 class="eg-title">Get <em>' + name + '</em></h3>' +
      '<p class="eg-sub">Type your email and the download starts right away. That email becomes your library: every plugin you grab is kept there, with fresh download links any time. No password.</p>' +""")
j = rep(j, """      '<div class="eg-note">Your email is only used for plugin news. Ever.</div>' +""",
           """      '<div class="eg-note">You\\u2019ll also hear about new plugins and updates. Unsubscribe anytime.</div>' +""")
j = rep(j, """      postEmail(email, plugin).then(function () {
        try { localStorage.setItem(STORAGE_KEY, email); } catch (_) {}
        close();
        startDownload(href);
      });""", """      postEmail(email, plugin).then(function () {
        try { localStorage.setItem(STORAGE_KEY, email); } catch (_) {}
        document.removeEventListener("keydown", onKey);
        overlay.remove();
        startDownload(href);
        openDone(href, plugin, email);
      });""")
j = rep(j, """  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a.dl") : null;""", """  /* After the download starts: say where it is kept. Shown to new AND returning visitors. */
  function openDone(href, plugin, email) {
    var acc = ACCENTS[plugin] || ACCENTS.chaos;
    var name = acc.label || (plugin.charAt(0).toUpperCase() + plugin.slice(1));
    var overlay = document.createElement("div");
    overlay.className = "eg-overlay";
    overlay.style.setProperty("--eg1", acc.g1);
    overlay.style.setProperty("--eg2", acc.g2);
    overlay.style.setProperty("--egsh", acc.shadow);
    overlay.innerHTML =
      '<div class="eg-modal eg-done" role="dialog" aria-modal="true" aria-label="' + name + ' is downloading">' +
      '<button class="eg-close" aria-label="Close">&times;</button>' +
      '<div class="eg-kind">Downloading</div>' +
      '<h3 class="eg-title"><em>' + name + '</em> is in your library</h3>' +
      '<p class="eg-sub">Your library is tied to <span class="eg-mail"></span>. Everything you grab is kept there, with fresh download links any time. Opening it emails you a sign-in code, no password.</p>' +
      '<a class="eg-lib" href="https://dl.sebastianmacan.com/library" target="_blank" rel="noopener">Open my library</a>' +
      '<div class="eg-row"><button class="eg-skip eg-other" type="button">Use a different email</button><button class="eg-skip eg-ok" type="button">Done</button></div>' +
      "</div>";
    overlay.querySelector(".eg-mail").textContent = email;
    document.body.appendChild(overlay);
    requestAnimationFrame(function () { overlay.classList.add("eg-show"); });
    function close() {
      overlay.classList.remove("eg-show");
      setTimeout(function () { overlay.remove(); }, 200);
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) { if (e.key === "Escape") close(); }
    document.addEventListener("keydown", onKey);
    overlay.addEventListener("click", function (e) { if (e.target === overlay) close(); });
    overlay.querySelector(".eg-close").addEventListener("click", close);
    overlay.querySelector(".eg-ok").addEventListener("click", close);
    overlay.querySelector(".eg-other").addEventListener("click", function () {
      try { localStorage.removeItem(STORAGE_KEY); } catch (_) {}
      document.removeEventListener("keydown", onKey);
      overlay.remove();
      openModal(href, plugin);
    });
  }

  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a.dl") : null;""")
j = rep(j, """      postEmail(known, plugin);
      startDownload(href);
      return;""", """      postEmail(known, plugin);
      startDownload(href);
      openDone(href, plugin, known);
      return;""")
out["js/email-gate.js"] = j

# ---------- (2) gremlin basket page ----------
g = open(S + "basket-gremlin.html").read()
g = rep(g, '<div class="pricebar"><span class="big freebie">$0</span></div>',
           '<div class="pricebar"><span class="big freebie">FREE</span><div class="limited">Limited time only</div></div>')
g = rep(g, '<div class="freetag">$0</div>', '<div class="freetag">FREE</div>', 5)
g = rep(g, "  .pricebar s {", "  .pricebar .limited { font-size:12px; font-weight:800; letter-spacing:.2em; text-transform:uppercase; color:#ffd84a; margin-top:6px; }\n  .pricebar s {")
g = rep(g, '>Grab the basket &middot; Mac</a>', '>Download for Mac</a>', 2)
g = rep(g, '>Grab the basket &middot; Windows</a>', '>Download for Windows</a>', 2)
g = rep(g, "Five Sebastian Macan plugins, free forever. Grab them one by one below, or take the whole basket in a single zip.",
           "Five Sebastian Macan plugins, free for a limited time. Grab them one by one below, or take the whole basket in a single zip.")
g = rep(g, "Five plugins, <b>$0</b>. No account, no catches. Unzip, install, make noise.",
           "Five plugins, <b>free</b>, for a limited time. Type your email once and all five are kept in your library.")
out["basket-gremlin.html"] = g

# ---------- (3) no "forever" on the four that just went free ----------
PILL = '<div class="cartrow"><span class="cartbtn add" style="pointer-events:none;border-color:rgba(255,216,74,.5);color:#ffd84a;">100% Free &middot; Forever</span></div>'
NEWP = PILL.replace("100% Free &middot; Forever", "Free &middot; Limited time")
h = open(S + "index.html").read(); n = 0
for key in ("downloads/Smear-v", "downloads/Stutter-v", "downloads/Twitch-v", '<span class="dl bopen" style="background:linear-gradient(135deg,#ff8ad8,#6ec8ff);">Open the basket</span>'):
    i = h.index(key); k = h.index(PILL, i); assert k - i < 900, (key, k - i)
    h = h[:k] + NEWP + h[k + len(PILL):]; n += 1
assert n == 4
out["index.html"] = h
pr = open(S + "pricing.html").read()
for row in ("<td>Smear</td><td>Granular smear into a plate reverb</td>", "<td>Stutter</td><td>Beat repeat with dice and a patch bay</td>",
            "<td>Twitch</td><td>Per-step glitch rack with a draw pad</td>", "<td>Gremlin Basket</td><td>Smear, Stutter, Twitch, Chop and Scrap in one zip</td>"):
    pr = rep(pr, row + '<td class="price">FREE forever</td>', row + '<td class="price">FREE, limited time</td>')
out["pricing.html"] = pr

# cache-bust the gate on every page
for f in glob.glob(S + "*.html") + glob.glob(S + "learn/*.html"):
    k = os.path.relpath(f, S); s = out.get(k) or open(f).read()
    if "email-gate.js?v=free8" in s: out[k] = s.replace("email-gate.js?v=free8", "email-gate.js?v=lib1")
print(len(out), "files", sorted(out)[:6], "...")
if not DRY:
    for k, s in out.items(): open(S + k, "w").write(s)
