#!/usr/bin/env python3
"""Ghost 1.4.2 -> live store (Nov 18 2026, Alex: "GOLD CERTIFY. PUT ON SEBASTIANMACAN.COM").
Builds site/ghost.html from the parked demo page (copy kept; only the facts that changed are edited:
free -> paid, v1.1 -> v1.4.2, Windows, presets, download link -> Buy button), adds the home card, cart row,
pricing row, sitemap row, audit map entry, then mirrors the page + card to demo-site. Idempotent. Run from anywhere.
WIN=1 env = the signed Windows installer is proven and in delivery."""
import os, re, json, shutil
H = os.path.expanduser('~') + '/sebastianmacan'; S = H + '/site'; D = H + '/demo-site'
V = '1.4.2'; USD = 15
WIN = os.environ.get('WIN') == '1'
PID = {i['product']: i for i in json.load(open(H + '/paddle/catalog.json'))['items']}['Ghost']['price_id']
PLAT = 'macOS + Windows' if WIN else 'macOS'
def rep(s, a, b, n=1):
    assert s.count(a) == n, (s.count(a), a[:70]); return s.replace(a, b)

# ---------- product page ----------
h = open(S + '/_tpl/ghost_parked.html').read()   # the parked demo page as it stood before this launch (the generator rewrites demo-site/ghost.html)
honey = open(S + '/honey.html').read()
h = rep(h, '<meta name="robots" content="noindex, nofollow">\n<script src="js/gate.js"></script>\n', '')
icons = honey[honey.index('<link rel="icon" href="/favicon.ico"'): honey.index('<title>')]
h = rep(h, '<title>Ghost | Free Granular Freeze VST3/AU Plugin</title>', icons + '<title>Ghost | Granular Freeze VST3/AU Plugin</title>')
DESC = f"Ghost is a granular freeze effect (VST3 and AU, {'macOS and Windows' if WIN else 'macOS'}). Freeze any sound into a haunted, infinite tape texture. ${USD}. By Sebastian Macan."
old_desc = 'Ghost is a free granular freeze effect (VST3 and AU for macOS). Freeze any sound into a haunted, infinite tape texture. By Sebastian Macan.'
seo = honey[honey.index('<!-- seo:start -->'): honey.index('<!-- seo:end -->') + len('<!-- seo:end -->\n')]
seo = seo.replace('honey.html', 'ghost.html').replace('og/honey.jpg', 'og/ghost.jpg')
seo = re.sub(r'(og:title" content=|twitter:title" content=)"[^"]*"', r'\1"Ghost | Granular Freeze VST3/AU Plugin"', seo)
seo = re.sub(r'(og:description" content=|twitter:description" content=)"[^"]*"', lambda m: m.group(1) + '"' + DESC + '"', seo)
assert 'oney' not in seo
h = rep(h, f'<meta name="description" content="{old_desc}">', seo + f'<meta name="description" content="{DESC}">')
h = rep(h, f'"description": "{old_desc}"', f'"description": "{DESC}"')
h = rep(h, '"operatingSystem": "macOS"', '"operatingSystem": "macOS, Windows"' if WIN else '"operatingSystem": "macOS"')
h = rep(h, '"price": "0"', f'"price": "{USD}"')
# FAQ (json-ld + visible): the two answers that are no longer true
FREE_Q = 'Is Ghost really free?'; FREE_A = 'Yes. Enter your email and the download starts right away. Full version, no locked knobs, no trial timer.'
PAY_Q = 'How much is Ghost?'; PAY_A = f'${USD}, one-time. Instant download after checkout. Full version, no locked knobs, no subscription.'
WIN_A_OLD = 'Windows builds are finished and getting their final polish. macOS is live today and Windows lands soon. Join the email list when you download and you will hear the moment it drops.'
WIN_A = 'Yes. Ghost ships for macOS (VST3 + AU) and Windows (VST3). One purchase covers both platforms.' if WIN else WIN_A_OLD
DAW_OLD = 'Any macOS DAW that loads VST3 or AU plugins'; DAW_NEW = 'Any DAW that loads VST3 or AU plugins' if WIN else DAW_OLD
h = rep(h, FREE_Q, PAY_Q, 2); h = rep(h, FREE_A, PAY_A, 2); h = rep(h, WIN_A_OLD, WIN_A, 2); h = rep(h, DAW_OLD, DAW_NEW, 2)
# hero + bottom buttons
h = rep(h, '<video autoplay muted loop playsinline poster="img/ui/ghost.png"><source src="https://video.sebastianmacan.com/img/video/ghost_ui_loop.mp4" type="video/mp4"></video>',
        f'<video autoplay muted loop playsinline preload="metadata" poster="img/ui/ghost.png?v={V}" aria-label="Ghost plugin UI: a glowing cursor drifting around the freeze pad while FREEZE lights up"><source src="https://video.sebastianmacan.com/img/video/ghost_ui_loop.mp4?v={V}" type="video/mp4"></video>')
h = rep(h, '<a class="dl" href="downloads/Ghost-v1.1-macOS.pkg">Download Ghost Free</a>\n      <div class="meta">v1.1 &middot; VST3 + AU effect &middot; macOS</div>',
        f'<span class="dl buy" role="button" tabindex="0" data-cart-buy="ghost">Buy Ghost &middot; ${USD}</span>\n      <div class="meta">v{V} &middot; VST3 + AU effect &middot; {PLAT}</div>')
h = rep(h, '<a class="dl" href="downloads/Ghost-v1.1-macOS.pkg">Download Ghost Free</a>', f'<span class="dl buy" role="button" tabindex="0" data-cart-buy="ghost">Buy Ghost &middot; ${USD}</span>')
h = rep(h, '.dl:hover { transform:translateY(-2px) scale(1.02); }', '.dl:hover { transform:translateY(-2px) scale(1.02); }\n  .dl.buy { cursor:pointer; user-select:none; }')
# what the build has now: presets + back / forward (facts; rest of the copy is the parked page as it was)
h = rep(h, '  <div class="knob"><b>Favorites.</b> Save the spots you love and recall them instantly.</div>\n',
        '  <div class="knob"><b>Favorites.</b> Save the spots you love and recall them instantly.</div>\n'
        '  <div class="knob"><b>Presets.</b> 14 to start, from Seance and Poltergeist to Tape Wraith and Whisper Vault. SAVE keeps your own, every knob included.</div>\n'
        '  <div class="knob"><b>Back and forward.</b> Rolled past a good one? The arrows beside RANDOMIZE walk back through everything you heard.</div>\n')
foot = honey[honey.index('  <footer>'): honey.index('  </footer>')]
h = h[:h.index('  <footer>')] + foot + h[h.index('  </footer>'):]
cartv = re.search(r'js/cart\.js\?v=(\w+)', honey).group(1)
h = rep(h, '<script src="js/email-gate.js?v=toy1" defer></script>\n',
        f'<script src="js/cart.js?v={cartv}" defer></script>\n<script src="js/email-gate.js?v={cartv}" defer></script>\n<script src="js/loops.js?v=2" defer></script>\n')
assert '\u2014' not in h and '\u2013' not in h and 'Free' not in h.replace('Freeze', '').replace('FREEZE', '') and 'downloads/Ghost' not in h, 'page check'
ld = re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1); json.loads(ld)
assert h.count('<div') == h.count('</div>') and h.count('<section') == h.count('</section>') and h.count('data-cart-buy="ghost"') == 2
open(S + '/ghost.html', 'w').write(h)
demo = rep(h, '<head>\n', '<head>\n<meta name="robots" content="noindex, nofollow">\n<script src="js/gate.js"></script>\n')
open(D + '/ghost.html', 'w').write(demo)
os.makedirs(S + '/audio', exist_ok=True)
for f in ('ghost_seed31973.m4a', 'ghost_seed31973_first_take.m4a'): shutil.copy(f'{D}/audio/{f}', f'{S}/audio/{f}')
print('ghost.html', len(h), 'bytes; platforms:', PLAT)

# ---------- home card ----------
CSS = "  .ghost { --g1:#39e6d0; --g2:#8b5cf6; --glow:#39e6d0; --shadow:rgba(57,230,208,.26); }\n"
GRAD = 'linear-gradient(135deg,#39e6d0,#8b5cf6)'
CARD = f'''    <div class="card ghost">
      <span class="new">NEW</span>
      <div class="kind">Granular Texture Machine</div>
      <h2 style="background:{GRAD};-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;">GHOST</h2>
      <p class="tag">Freeze sound. Then haunt it.</p>
      <p class="desc">Grabs the last four seconds of whatever you played and refuses to let it move on. Very unhealthy. Sounds incredible.</p>
      <div class="shot"><video autoplay muted loop playsinline preload="metadata" poster="img/ui/ghost.png?v={V}"><source src="https://video.sebastianmacan.com/img/video/ghost_ui_loop.mp4?v={V}" type="video/mp4"></video></div>
      <span class="dl buy" style="background:{GRAD};box-shadow:0 6px 28px rgba(57,230,208,.26);" role="button" tabindex="0" data-cart-buy="ghost">Buy Ghost &middot; ${USD}</span>
      <div class="cartrow"><span class="cartbtn add" role="button" tabindex="0" data-cart-add="ghost">Add to Cart</span><span class="cartbtn buy" role="button" tabindex="0" data-cart-buy="ghost">Buy Now</span></div>
      <a class="more" href="ghost.html">See how it works &rarr;</a>
      <div class="meta">v{V} · VST3 + AU effect · {PLAT}</div>
    </div>
'''
WORDS = {13: 'Thirteen', 14: 'Fourteen'}
def card_in(path, demo_tree):
    s = open(path).read()
    anchor = '  <div class="sect-title" id="effects">Color &amp; Motion FX</div>\n  <div class="grid">\n'
    if 'data-cart-buy="ghost"' not in s:
        if demo_tree:   # demo index still carries the parked Ghost card further down: take it out, the new one goes where live has it
            a = s.index('<div class="card ghost">'); b = s.index('<div class="card ', a + 10); s = s[:a] + s[b:]
        else:
            pk = '  .pocket { --g1:#4f97e8;'; s = rep(s, pk, CSS + pk)
        s = rep(s, anchor, anchor + CARD)
        s = rep(s, '13 Plugins + 11 MIDI Packs', '14 Plugins + 11 MIDI Packs', 4)
        s = rep(s, 'Thirteen plugins and 4796', 'Fourteen plugins and 4796')
    else:   # re-run: refresh the card (platform line)
        import re as _re; s = _re.sub(r'  \.ghost \{ --g1:[^\n]*\n', CSS, s)
        a = s.index('    <div class="card ghost">'); b = s.index('    <div class="card ', a + 10); s = s[:a] + CARD + s[b:]
    assert s.count('class="card ghost"') == 1 and s.count('.ghost { --g1') == 1
    open(path, 'w').write(s)
card_in(S + '/index.html', False); card_in(D + '/index.html', True)

# ---------- cart, audit map, pricing, sitemap ----------
for tree in (S, D):   # demo-site keeps its own cart.js (it lags the live one); same one-row add in each
    c = open(tree + '/js/cart.js').read()
    if "ghost:" not in c:
        row = "    pocket:        { name: 'Pocket',                 cents: 1500, priceId: 'pri_01m5jmgg27ch339v1v5gkr6g7a' },\n"
        c = rep(c, row, row + f"    ghost:         {{ name: 'Ghost',                  cents: {USD*100}, priceId: '{PID}' }},\n")
        open(tree + '/js/cart.js', 'w').write(c)
a = open(S + '/audit_baskets.py').read()
if '"ghost": "Ghost"' not in a:
    a = rep(a, '"pocket": "Pocket"}', '"pocket": "Pocket", "ghost": "Ghost"}'); open(S + '/audit_baskets.py', 'w').write(a)
p = open(S + '/pricing.html').read()
if '<td>Ghost</td>' not in p:
    row = '    <tr><td>Pocket</td><td>Snare depth</td><td class="price">$15</td></tr>\n'
    p = rep(p, row, row + f'    <tr><td>Ghost</td><td>Granular freeze effect</td><td class="price">${USD}</td></tr>\n'); open(S + '/pricing.html', 'w').write(p)
m = open(S + '/sitemap.xml').read()
if 'ghost.html' not in m:
    row = '  <url><loc>https://sebastianmacan.com/pocket.html</loc><lastmod>2026-11-10</lastmod></url>\n'
    m = rep(m, row, row + '  <url><loc>https://sebastianmacan.com/ghost.html</loc><lastmod>2026-11-18</lastmod></url>\n'); open(S + '/sitemap.xml', 'w').write(m)
print('card + cart + pricing + sitemap done; price id', PID[:8] + '...')
