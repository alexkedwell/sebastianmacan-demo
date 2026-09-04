/* Sebastian Macan store cart
   - Cart tab pinned top-left of every page, live item-count badge
   - Slide-out drawer: items, remove, subtotal, CHECKOUT via Paddle.js v2
   - Product buttons: any element with data-cart-add="<id>" or data-cart-buy="<id>"
   Storage: localStorage "sm_cart_v1" = ["biome","reels",...] (qty is always 1,
   these are licenses/downloads).

   PADDLE WIRING
   - PADDLE_CLIENT_TOKEN must be a CLIENT-SIDE token from the Paddle dashboard
     (Developer Tools > Authentication > Client-side tokens). It is NOT the
     server API key in ~/sebastianmacan/paddle/credentials.json - never put
     that key here.
   - Until the token is set, CHECKOUT shows a friendly "checkout opens soon"
     note instead of calling Paddle.
   - priceId values come from ~/sebastianmacan/paddle/catalog.json. Items with
     priceId:null have no Paddle product yet (Warble, Lofi baskets, Hitmaker
     Complete) - create them at catalog-sync time and fill in.
   - KNOWN STALE PADDLE PRICES (site price shown here is source of truth;
     sync Paddle before launch): Jelly $15 (Paddle $0), Reels $15 (Paddle $19),
     Halo $29 (Paddle $19), Hit Chords 500 $20 (renamed/repriced pending). */
(function () {
  'use strict';

  var PADDLE_ENV = 'production';       // 'sandbox' while testing
  var PADDLE_CLIENT_TOKEN = 'live_cdfa8413fc96d7fac44e0f498d0';

  var CATALOG = {
    /* plugins */
    biome:         { name: 'Biome',                  cents: 3900, priceId: 'pri_01m09h3ccsvkn3gxqt033pppd5' },
    magician:      { name: 'Chordsmith',               cents: 3900, priceId: 'pri_01m09h3cvs4nrrch2v4r9zbq5n' },
    jelly:         { name: 'Jelly',                  cents: 1500, priceId: 'pri_01m1gntsq26gagfdqahmz3thdk' },
    warble:        { name: 'Warble',                 cents: 1500, priceId: 'pri_01m1gntt0z0mpgfr059dve73fj' },
    reels:         { name: 'Reels',                  cents: 1500, priceId: 'pri_01m1gnswg636185tfrqxdgyaqr' },
    fireplace:     { name: 'Fireplace',              cents: 1500, priceId: 'pri_01m1nckxvaekbaccghkvvh4zva' },
    halo:          { name: 'Halo',                   cents: 2900, priceId: 'pri_01m1gnswspxareqhrervwre5a3' },
    gloss:         { name: 'Gloss',                  cents: 1900, priceId: 'pri_01m09knjab3bppsqctg98j5s3b' },
    /* MIDI chord packs */
    hitchords:     { name: 'Hit Chords 500',         cents: 1500, priceId: 'pri_01m1gnsx2qvxew8czas9ym2qa4' },
    clubchords:    { name: 'Club Chords 240',        cents: 1200, priceId: 'pri_01m1gnsxcvj6w77fanegkzwm1j' },
    soulchords:    { name: 'Soul Chords 240',        cents: 1200, priceId: 'pri_01m1gnsxngw04eejk0qr67kpmd' },
    /* Modal Series */
    ionian:        { name: 'Ionian Mode 48',         cents: 500, priceId: 'pri_01m1gnsxxvfs2nbag2280x8ydj' },
    dorian:        { name: 'Dorian Mode 48',         cents: 500, priceId: 'pri_01m1gnsy80zd3s9wnzgxk4dtgc' },
    phrygian:      { name: 'Phrygian Mode 48',       cents: 500, priceId: 'pri_01m1gnsyh2zn6hkdp22h1n6vke' },
    lydian:        { name: 'Lydian Mode 48',         cents: 500, priceId: 'pri_01m1gnsysmfa7ejv2s88q66ae5' },
    mixolydian:    { name: 'Mixolydian Mode 48',     cents: 500, priceId: 'pri_01m1gnsz22tc0s96mj22p199bk' },
    aeolian:       { name: 'Aeolian Mode 48',        cents: 500, priceId: 'pri_01m1gnszb10sszgqjgfhf2ja1z' },
    locrian:       { name: 'Locrian Mode 48',        cents: 500, priceId: 'pri_01m1gnszmtjsf1tay41580e54r' },
    /* bundles / baskets */
    allmodes:      { name: 'All 7 Modes Basket',     cents: 1200, priceId: 'pri_01m1gnszy7hgdp0xw9gfyqe7ha' },
    midimega:      { name: 'MIDI Mega Basket',       cents: 4900, priceId: 'pri_01m09n48fjhgmpb2hxcmr2kyf0' },
    lofibasket:    { name: 'Lofi Basket',            cents: 3000, priceId: 'pri_01m1nckxzp0m01qh26zs7qq99t' },
    lofimastering: { name: 'Lofi Basket + Mastering', cents: 4900, priceId: 'pri_01m1nckyery0c9sqt2m971y8zb' },
    hitmakercomplete: { name: 'Hitmaker Chords - Complete Series', cents: 3000, priceId: 'pri_01m1gnttz53wm3x06bvhhrtcmq' }
  };

  var KEY = 'sm_cart_v1';

  function load() {
    try {
      var raw = JSON.parse(localStorage.getItem(KEY) || '[]');
      if (Array.isArray(raw)) return raw.filter(function (id) { return CATALOG[id]; });
    } catch (e) {}
    return [];
  }
  function save(items) { try { localStorage.setItem(KEY, JSON.stringify(items)); } catch (e) {} }
  function money(cents) { return '$' + (cents % 100 === 0 ? (cents / 100) : (cents / 100).toFixed(2)); }

  var cart = load();

  /* ---------- UI ---------- */

  var css = [
    '#smcart-tab{position:fixed;top:16px;left:16px;z-index:9990;display:flex;align-items:center;gap:8px;',
    ' background:#141418;border:1px solid #2a2a32;border-radius:999px;padding:9px 14px;cursor:pointer;',
    ' color:#f2f2f4;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;',
    ' font-size:13px;font-weight:800;letter-spacing:.04em;box-shadow:0 6px 24px rgba(0,0,0,.5);',
    ' transition:transform .15s ease,border-color .15s ease;user-select:none;-webkit-user-select:none;}',
    '#smcart-tab:hover{transform:translateY(-2px);border-color:#7b5cff;}',
    '#smcart-tab svg{display:block;}',
    '#smcart-badge{min-width:20px;height:20px;border-radius:999px;display:none;align-items:center;justify-content:center;',
    ' padding:0 6px;font-size:11px;font-weight:900;color:#0a0a0c;',
    ' background:linear-gradient(135deg,#ff3d5a,#ffd84a);}',
    '#smcart-badge.on{display:flex;}',
    '#smcart-badge.pulse{animation:smcart-pulse .3s ease;}',
    '@keyframes smcart-pulse{0%{transform:scale(1)}50%{transform:scale(1.45)}100%{transform:scale(1)}}',
    '#smcart-overlay{position:fixed;inset:0;background:rgba(6,6,8,.6);backdrop-filter:blur(2px);z-index:9991;',
    ' opacity:0;pointer-events:none;transition:opacity .25s ease;}',
    '#smcart-overlay.open{opacity:1;pointer-events:auto;}',
    '#smcart-drawer{position:fixed;top:0;left:0;bottom:0;width:min(380px,92vw);z-index:9992;',
    ' background:#101014;border-right:1px solid #222228;transform:translateX(-102%);',
    ' transition:transform .28s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;',
    ' font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Inter,Roboto,sans-serif;color:#f2f2f4;',
    ' box-shadow:24px 0 80px rgba(0,0,0,.55);}',
    '#smcart-drawer.open{transform:translateX(0);}',
    '#smcart-drawer .smhead{display:flex;align-items:center;justify-content:space-between;padding:20px 22px 14px;border-bottom:1px solid #222228;}',
    '#smcart-drawer .smhead h2{font-size:15px;font-weight:900;letter-spacing:.14em;text-transform:uppercase;margin:0;',
    ' background:linear-gradient(120deg,#ff3d5a,#7b5cff,#39e6d0);-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent;}',
    '#smcart-close{background:none;border:0;color:#8a8a94;font-size:22px;line-height:1;cursor:pointer;padding:4px 8px;}',
    '#smcart-close:hover{color:#f2f2f4;}',
    '#smcart-items{flex:1;overflow-y:auto;padding:8px 22px;}',
    '.smcart-row{display:flex;align-items:center;justify-content:space-between;gap:10px;padding:14px 0;border-bottom:1px solid #1c1c22;}',
    '.smcart-row .n{font-size:14px;font-weight:800;}',
    '.smcart-row .p{font-size:13px;color:#8a8a94;font-weight:700;white-space:nowrap;}',
    '.smcart-rm{background:none;border:1px solid #2a2a32;border-radius:999px;color:#8a8a94;width:26px;height:26px;',
    ' font-size:14px;line-height:1;cursor:pointer;flex:none;}',
    '.smcart-rm:hover{color:#ff3d5a;border-color:#ff3d5a;}',
    '#smcart-empty{color:#8a8a94;font-size:14px;text-align:center;padding:40px 10px;}',
    '#smcart-foot{padding:16px 22px 22px;border-top:1px solid #222228;}',
    '#smcart-sub{display:flex;justify-content:space-between;font-size:14px;font-weight:800;margin-bottom:6px;}',
    '#smcart-sub .amt{font-size:18px;font-weight:900;}',
    '#smcart-taxnote{color:#8a8a94;font-size:11.5px;margin-bottom:12px;}',
    '#smcart-checkout{display:block;width:100%;border:0;border-radius:999px;padding:14px 20px;cursor:pointer;',
    ' font-size:15px;font-weight:900;letter-spacing:.06em;color:#fff;text-transform:uppercase;',
    ' background:linear-gradient(135deg,#ff3d5a,#7b5cff);box-shadow:0 6px 28px rgba(123,92,255,.35);transition:transform .15s;}',
    '#smcart-checkout:hover{transform:translateY(-2px);}',
    '#smcart-checkout:disabled{opacity:.45;cursor:default;transform:none;}',
    '#smcart-msg{color:#ffd84a;font-size:12.5px;margin-top:10px;display:none;line-height:1.5;}',
    '#smcart-msg.on{display:block;}',
    /* product-card buttons */
    '.cartrow{display:flex;gap:8px;margin-top:12px;flex-wrap:wrap;position:relative;z-index:2;}',
    '.cartbtn{display:inline-block;font-size:12px;font-weight:800;letter-spacing:.06em;text-transform:uppercase;',
    ' padding:10px 16px;border-radius:999px;cursor:pointer;text-decoration:none;user-select:none;-webkit-user-select:none;',
    ' transition:transform .15s ease;position:relative;z-index:2;text-align:center;}',
    '.cartbtn:hover{transform:translateY(-2px);}',
    '.cartbtn.add{color:#f2f2f4;background:transparent;border:1px solid var(--g1,#7b5cff);}',
    '.cartbtn.buy{color:#fff;border:1px solid transparent;background:linear-gradient(135deg,var(--g1,#ff3d5a),var(--g2,#7b5cff));',
    ' box-shadow:0 4px 18px var(--shadow,rgba(123,92,255,.3));}',
    '.cartbtn.added{border-color:#39e6d0;color:#39e6d0;}',
    '@media (max-width:640px){#smcart-tab{top:10px;left:10px;padding:8px 12px;}}',
    /* in-nav FINAL: plain text "Cart" link, styled exactly like the other nav links; candy count badge only when non-empty */
    '#smcart-tab.innav,#smcart-tab.innav[role]{position:relative;top:auto;left:auto;display:inline;margin-left:22px;padding:0;border:0;border-radius:0;box-shadow:none;background:transparent;',
    ' color:#8a8a94;font:inherit;font-size:14px;font-weight:400;letter-spacing:0;text-transform:none;vertical-align:baseline;transition:color .15s ease;}',
    '#smcart-tab.innav:hover{color:#f2f2f4;transform:none;border-color:transparent;}',
    '#smcart-tab.innav svg{display:none;}',
    '#smcart-tab.innav .smcart-label{position:static;width:auto;height:auto;overflow:visible;clip:auto;}',
    '#smcart-tab.innav #smcart-badge{display:none;position:relative;top:-1px;margin-left:5px;min-width:16px;height:16px;font-size:10px;padding:0 4px;vertical-align:middle;}',
    '#smcart-tab.innav #smcart-badge.on{display:inline-flex;}',
    /* mobile: header stacks logo over a scrolling nav strip; pin the cart top-right of the header so it is never scrolled away */
    '@media (max-width:640px){#smcart-tab.innav[role]{margin-left:0;margin-right:16px;}',
    /* single-row sub-page headers: let the nav wrap instead of overflowing the phone screen */
    ' header:has(#smcart-tab.innav:not(.pin)){flex-wrap:wrap;gap:8px 0;}header nav:has(#smcart-tab.innav:not(.pin)){display:inline-flex;flex-wrap:wrap;align-items:center;row-gap:8px;}',
    ' header nav:has(#smcart-tab.innav:not(.pin)) a{margin-left:0;margin-right:16px;}#smcart-tab.innav:not(.pin)[role]{margin-left:0;}',
    /* homepage stacks logo over a scrolling nav strip: pin the cart on the logo line so it can never scroll away */
    ' #smcart-tab.innav.pin[role]{display:inline;vertical-align:baseline;}}'
  ].join('\n');

  var CART_SVG = '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/></svg>';

  var els = {};

  function buildUI() {
    var style = document.createElement('style');
    style.textContent = css;
    document.head.appendChild(style);

    var tab = document.createElement('div');
    tab.id = 'smcart-tab';
    tab.setAttribute('role', 'button');
    tab.setAttribute('tabindex', '0');
    tab.setAttribute('aria-label', 'Open cart');
    tab.innerHTML = CART_SVG + '<span class="smcart-label">Cart</span><span id="smcart-badge">0</span>';
    /* Preferred home: inside the header nav, right after the last link
       (next to "Bundles"). Fallback: fixed pill top-left. */
    var nav = document.querySelector('header nav, nav');
    if (nav) {
      tab.classList.add('innav');
      // stacked header (logo above nav) = homepage layout; pin the cart there on phones
      var hdr = nav.closest('header');
      if (hdr && getComputedStyle(hdr).flexDirection === 'column') tab.classList.add('pin');
      nav.appendChild(tab);
      var syncSpacing = function () {
        var prev = tab.previousElementSibling; if (!prev) return;
        var cs = getComputedStyle(prev);
        tab.style.marginLeft = cs.marginLeft; tab.style.marginRight = cs.marginRight; tab.style.display = cs.display;
      };
      syncSpacing(); window.addEventListener('resize', syncSpacing);
      window.addEventListener('resize', function () {
        if (!hdr) return;
        tab.classList.toggle('pin', getComputedStyle(hdr).flexDirection === 'column');
      });
    }
    else { document.body.appendChild(tab); }

    var overlay = document.createElement('div');
    overlay.id = 'smcart-overlay';
    document.body.appendChild(overlay);

    var drawer = document.createElement('aside');
    drawer.id = 'smcart-drawer';
    drawer.setAttribute('aria-label', 'Shopping cart');
    drawer.innerHTML =
      '<div class="smhead"><h2>Your Candy Bag</h2>' +
      '<button id="smcart-close" aria-label="Close cart">&times;</button></div>' +
      '<div id="smcart-items"></div>' +
      '<div id="smcart-foot">' +
      '  <div id="smcart-sub"><span>Subtotal</span><span class="amt">$0</span></div>' +
      '  <div id="smcart-taxnote">Prices in USD. Any tax or VAT is added at checkout by Paddle, our merchant of record.</div>' +
      '  <button id="smcart-checkout">Checkout</button>' +
      '  <div id="smcart-msg"></div>' +
      '</div>';
    document.body.appendChild(drawer);

    els.tab = tab;
    els.badge = tab.querySelector('#smcart-badge');
    els.overlay = overlay;
    els.drawer = drawer;
    els.items = drawer.querySelector('#smcart-items');
    els.sub = drawer.querySelector('#smcart-sub .amt');
    els.checkout = drawer.querySelector('#smcart-checkout');
    els.msg = drawer.querySelector('#smcart-msg');

    /* Keep the fixed tab from covering the site logo: if the logo starts near
       the left edge, park the tab just below it and let it slide up to the
       corner as the page scrolls. */
    function positionTab() {
      var logo = document.querySelector('.logo') || document.querySelector('header');
      var top = 16;
      if (logo) {
        var lr = logo.getBoundingClientRect();
        var tw = tab.offsetWidth || 96;
        if (lr.left < tw + 32 && lr.bottom > 0) top = Math.max(16, Math.round(lr.bottom + 10));
      }
      tab.style.top = top + 'px';
    }
    if (!tab.classList.contains('innav')) positionTab();
    var ptTick = false;
    function onScrollResize() {
      if (ptTick) return;
      ptTick = true;
      requestAnimationFrame(function () { ptTick = false; if (!tab.classList.contains('innav')) positionTab(); });
    }
    window.addEventListener('scroll', onScrollResize, { passive: true });
    window.addEventListener('resize', onScrollResize);

    tab.addEventListener('click', toggleDrawer);
    tab.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); toggleDrawer(); } });
    overlay.addEventListener('click', closeDrawer);
    drawer.querySelector('#smcart-close').addEventListener('click', closeDrawer);
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') closeDrawer(); });
    els.checkout.addEventListener('click', function () { checkout(cart.slice()); });
  }

  function render() {
    var n = cart.length;
    els.badge.textContent = String(n);
    els.badge.classList.toggle('on', n > 0);

    if (n === 0) {
      els.items.innerHTML = '<div id="smcart-empty">Your bag is empty.<br>Go grab some candy.</div>';
    } else {
      els.items.innerHTML = cart.map(function (id) {
        var p = CATALOG[id];
        return '<div class="smcart-row">' +
          '<div><div class="n">' + p.name + '</div></div>' +
          '<div style="display:flex;align-items:center;gap:12px;">' +
          '<span class="p">' + money(p.cents) + '</span>' +
          '<button class="smcart-rm" data-cart-remove="' + id + '" aria-label="Remove ' + p.name + '">&times;</button>' +
          '</div></div>';
      }).join('');
    }
    var total = cart.reduce(function (s, id) { return s + CATALOG[id].cents; }, 0);
    els.sub.textContent = money(total);
    els.checkout.disabled = n === 0;
  }

  function pulseBadge() {
    els.badge.classList.remove('pulse');
    void els.badge.offsetWidth; /* restart animation */
    els.badge.classList.add('pulse');
  }

  function setMsg(text) {
    els.msg.textContent = text || '';
    els.msg.classList.toggle('on', !!text);
  }

  function openDrawer() { els.drawer.classList.add('open'); els.overlay.classList.add('open'); }
  function closeDrawer() { els.drawer.classList.remove('open'); els.overlay.classList.remove('open'); setMsg(''); }
  function toggleDrawer() { els.drawer.classList.contains('open') ? closeDrawer() : openDrawer(); }

  function add(id, opts) {
    if (!CATALOG[id]) return;
    if (cart.indexOf(id) === -1) {
      cart.push(id);
      save(cart);
    }
    render();
    pulseBadge();
    if (!opts || !opts.silent) openDrawer();
  }

  function remove(id) {
    var i = cart.indexOf(id);
    if (i !== -1) { cart.splice(i, 1); save(cart); }
    render();
  }

  /* ---------- Paddle ---------- */

  var paddleReady = null;
  function loadPaddle() {
    if (paddleReady) return paddleReady;
    paddleReady = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = 'https://cdn.paddle.com/paddle/v2/paddle.js';
      s.onload = function () {
        try {
          if (PADDLE_ENV === 'sandbox') window.Paddle.Environment.set('sandbox');
          window.Paddle.Initialize({ token: PADDLE_CLIENT_TOKEN });
          resolve(window.Paddle);
        } catch (e) { reject(e); }
      };
      s.onerror = function () { reject(new Error('paddle.js failed to load')); };
      document.head.appendChild(s);
    });
    return paddleReady;
  }

  function checkout(ids) {
    if (!ids.length) return;
    if (!PADDLE_CLIENT_TOKEN) {
      openDrawer();
      setMsg('Paid checkout opens soon. Everything in the store is a free download during launch, so grab it from the product buttons for now.');
      return;
    }
    var missing = ids.filter(function (id) { return !CATALOG[id].priceId; });
    if (missing.length) {
      openDrawer();
      setMsg('Checkout is not wired up yet for: ' + missing.map(function (id) { return CATALOG[id].name; }).join(', ') + '. Remove those items to check out the rest.');
      return;
    }
    setMsg('');
    loadPaddle().then(function (Paddle) {
      Paddle.Checkout.open({
        items: ids.map(function (id) { return { priceId: CATALOG[id].priceId, quantity: 1 }; }),
        settings: { displayMode: 'overlay', theme: 'dark', locale: 'en' }
      });
    }).catch(function (e) {
      openDrawer();
      setMsg('Could not start checkout (' + (e && e.message ? e.message : 'unknown error') + '). Please try again.');
    });
  }

  /* ---------- wire product buttons ---------- */

  function bindButtons() {
    function handle(el, fn) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation(); /* keep whole-card click-throughs and wrapping <a> from firing */
        fn();
      });
      el.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); e.stopPropagation(); fn(); }
      });
    }
    document.querySelectorAll('[data-cart-add]').forEach(function (el) {
      handle(el, function () {
        add(el.getAttribute('data-cart-add'));
        el.classList.add('added');
        var old = el.textContent;
        el.textContent = 'Added \u2713';
        setTimeout(function () { el.classList.remove('added'); el.textContent = old; }, 1400);
      });
    });
    document.querySelectorAll('[data-cart-buy]').forEach(function (el) {
      handle(el, function () {
        var id = el.getAttribute('data-cart-buy');
        if (!PADDLE_CLIENT_TOKEN || !CATALOG[id] || !CATALOG[id].priceId) {
          /* checkout not live yet: put it in the bag and show the note */
          add(id, { silent: true });
          openDrawer();
          checkout([id]);
        } else {
          checkout([id]);
        }
      });
    });
    /* remove buttons are re-rendered, delegate on the drawer */
    els.items.addEventListener('click', function (e) {
      var btn = e.target.closest('[data-cart-remove]');
      if (btn) remove(btn.getAttribute('data-cart-remove'));
    });
  }

  function init() {
    buildUI();
    bindButtons();
    render();
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init);
  else init();

  /* expose for other scripts / debugging */
  window.SM_CART = { add: add, remove: remove, open: openDrawer, close: closeDrawer, items: function () { return cart.slice(); }, catalog: CATALOG };
})();
