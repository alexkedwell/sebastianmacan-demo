/* Wormhole (Nov 18 2026, Alex): clicking the Gremlin card on the homepage blasts through a wormhole
   and lands in the stars on the Gremlin Basket page.
   - Homepage: any element with [data-warp="page.html"] plays the jump, then navigates.
   - Landing page: <body data-space> gets a slow star field behind the content; if we arrived by
     wormhole the stars come in at warp speed and brake.
   Plain canvas, no libraries. Reduced-motion users get a normal link and still stars. */
(function () {
  'use strict';
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var KEY = 'sm_warp';
  var COLS = ['#ffffff', '#ffffff', '#ffd4ec', '#ff8ad8', '#6ec8ff', '#c9b6ff', '#9ad63a'];

  function makeCanvas(z, fixedBehind) {
    var c = document.createElement('canvas');
    c.setAttribute('aria-hidden', 'true');
    c.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;display:block;pointer-events:' + (fixedBehind ? 'none' : 'auto') + ';z-index:' + z + ';';
    return c;
  }
  function fit(c) {
    var d = Math.min(window.devicePixelRatio || 1, 1.5);
    c.width = Math.round(window.innerWidth * d); c.height = Math.round(window.innerHeight * d);
    return d;
  }
  function makeStars(n) {
    var a = [];
    for (var i = 0; i < n; i++) a.push({ x: (Math.random() * 2 - 1), y: (Math.random() * 2 - 1), z: Math.random() * 0.98 + 0.02, c: COLS[(Math.random() * COLS.length) | 0], s: Math.random() * 0.9 + 0.4 });
    return a;
  }
  /* one frame of the star tunnel. speed = how far stars travel toward the viewer this frame (0..~0.08) */
  function drawStars(ctx, W, H, stars, speed, cx, cy, fade) {
    ctx.globalCompositeOperation = 'source-over';
    ctx.fillStyle = 'rgba(8,5,22,' + fade + ')';
    ctx.fillRect(0, 0, W, H);
    ctx.globalCompositeOperation = 'lighter';
    var f = Math.max(W, H) * 0.55;
    ctx.lineCap = 'round';
    for (var i = 0; i < stars.length; i++) {
      var st = stars[i], pz = st.z;
      st.z -= speed * st.s;
      if (st.z <= 0.012) { st.x = Math.random() * 2 - 1; st.y = Math.random() * 2 - 1; st.z = 1; pz = 1; }
      var x0 = cx + st.x / pz * f, y0 = cy + st.y / pz * f, x1 = cx + st.x / st.z * f, y1 = cy + st.y / st.z * f;
      if (x1 < -50 || x1 > W + 50 || y1 < -50 || y1 > H + 50) { st.z = 0; continue; }
      var w = Math.min(3.4, (1 - st.z) * 2.6 * st.s + 0.5) * (W / 1400 + 0.6);
      ctx.strokeStyle = st.c; ctx.globalAlpha = Math.min(1, 1.25 - st.z); ctx.lineWidth = w;
      ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(x1 + 0.01, y1 + 0.01); ctx.stroke();
    }
    ctx.globalAlpha = 1;
  }
  /* glowing rings rushing past = the wormhole walls */
  function drawRings(ctx, W, H, t, power, cx, cy) {
    if (power <= 0) return;
    ctx.globalCompositeOperation = 'lighter';
    var R = Math.hypot(W, H) * 0.62;
    for (var k = 0; k < 9; k++) {
      var p = ((k / 9) + t * 1.35) % 1, e = p * p * p;
      var r = 8 + e * R;
      ctx.beginPath();
      ctx.ellipse(cx + Math.sin(t * 5 + k) * 10 * (1 - p), cy + Math.cos(t * 4 + k * 2) * 8 * (1 - p), r, r * 0.92, t * 0.9 + k * 0.7, 0, Math.PI * 2);
      ctx.strokeStyle = k % 2 ? '#ff8ad8' : '#6ec8ff';
      ctx.globalAlpha = power * (0.10 + 0.5 * p) * (1 - e * 0.55);
      ctx.lineWidth = 1 + e * 26;
      ctx.stroke();
    }
    var g = ctx.createRadialGradient(cx, cy, 0, cx, cy, R * 0.34);
    g.addColorStop(0, 'rgba(255,255,255,' + (0.55 * power) + ')'); g.addColorStop(0.25, 'rgba(255,138,216,' + (0.30 * power) + ')'); g.addColorStop(1, 'rgba(110,200,255,0)');
    ctx.globalAlpha = 1; ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
  }
  function ease(x) { return x < 0 ? 0 : x > 1 ? 1 : x * x * (3 - 2 * x); }

  /* ---------- the jump (homepage) ---------- */
  var jumping = false;
  function jump(url, originEl) {
    if (jumping) return; jumping = true;
    try { sessionStorage.setItem(KEY, String(Date.now())); } catch (_) {}
    var c = makeCanvas(2147483000, false), ctx = c.getContext('2d'), d = fit(c), W = c.width, H = c.height;
    var flash = document.createElement('div');
    flash.style.cssText = 'position:fixed;inset:0;z-index:2147483001;background:#fff;opacity:0;pointer-events:none;';
    c.style.opacity = '0'; c.style.transition = 'opacity .22s ease';
    document.body.appendChild(c); document.body.appendChild(flash);
    c.id = 'sm-warp'; flash.id = 'sm-warp-flash';
    var r = originEl && originEl.getBoundingClientRect ? originEl.getBoundingClientRect() : null;
    var ox = r ? (r.left + r.width / 2) * d : W / 2, oy = r ? (r.top + r.height / 2) * d : H / 2;
    ox = Math.max(0, Math.min(W, ox)); oy = Math.max(0, Math.min(H, oy));
    var stars = makeStars(Math.round(Math.min(900, 420 + W * H / 5200)));
    ctx.fillStyle = '#080516'; ctx.fillRect(0, 0, W, H);
    requestAnimationFrame(function () { c.style.opacity = '1'; });
    var DUR = 1500, t0 = performance.now(), gone = false;
    function go() { if (gone) return; gone = true; window.location.href = url; }
    setTimeout(go, DUR + 400); /* never strand a visitor if a tab throttles the animation */
    (function frame(now) {
      var t = Math.min(1, (now - t0) / DUR);
      var k = ease(t / 0.55);                      /* tunnel centre glides from the card to the middle of the screen */
      var cx = ox + (W / 2 - ox) * k, cy = oy + (H / 2 - oy) * k;
      var speed = 0.0025 + Math.pow(t, 2.4) * 0.085;
      drawStars(ctx, W, H, stars, speed, cx, cy, 0.42 - 0.30 * t);
      drawRings(ctx, W, H, t * DUR / 1000, ease((t - 0.12) / 0.5), cx, cy);
      flash.style.opacity = String(Math.pow(ease((t - 0.80) / 0.20), 1.6));
      if (t < 1) requestAnimationFrame(frame); else go();
    })(t0);
  }
  function hook() {
    var els = document.querySelectorAll('[data-warp]');
    for (var i = 0; i < els.length; i++) (function (el) {
      el.addEventListener('click', function (e) {
        if (REDUCED || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey || e.button) return;
        if (e.target.closest && e.target.closest('[data-cart-add],[data-cart-buy]')) return;
        e.preventDefault(); e.stopPropagation();
        jump(el.getAttribute('data-warp'), el);
      }, true);
    })(els[i]);
  }
  /* back button: the homepage can come back from the page cache with the overlay still on it */
  window.addEventListener('pageshow', function () {
    var a = document.getElementById('sm-warp'), b = document.getElementById('sm-warp-flash');
    if (a) a.remove(); if (b) b.remove(); jumping = false;
  });

  /* ---------- the landing (basket page) ---------- */
  function space() {
    var arrived = false;
    try { var v = +sessionStorage.getItem(KEY); arrived = v && Date.now() - v < 8000; sessionStorage.removeItem(KEY); } catch (_) {}
    if (REDUCED) arrived = false;
    var GALAXY = document.body.hasAttribute('data-galaxy');     /* js/galaxy.js owns the background: we only do the arrival */
    if (GALAXY && !arrived) return;
    var c = makeCanvas(0, true), ctx = c.getContext('2d'), W, H;
    var gx = document.getElementById('sm-galaxy');
    document.body.insertBefore(c, gx ? gx.nextSibling : document.body.firstChild);
    var stars = makeStars(Math.round(Math.min(700, 260 + window.innerWidth * window.innerHeight / 4200)));
    function size() { fit(c); W = c.width; H = c.height; ctx.fillStyle = '#080516'; ctx.fillRect(0, 0, W, H); }
    size(); window.addEventListener('resize', size);
    var flash = null;
    if (arrived) {
      flash = document.createElement('div');
      flash.style.cssText = 'position:fixed;inset:0;z-index:2147483001;background:#fff;opacity:1;pointer-events:none;';
      document.body.appendChild(flash);
    }
    var LAND = 1500, t0 = performance.now(), running = true;
    document.addEventListener('visibilitychange', function () { running = !document.hidden; if (running) requestAnimationFrame(frame); });
    function frame(now) {
      if (!running) return;
      var t = arrived ? Math.min(1, (now - t0) / LAND) : 1, b = 1 - ease(t);       /* b: 1 = still at warp, 0 = landed */
      drawStars(ctx, W, H, stars, 0.00045 + Math.pow(b, 2) * 0.075, W / 2, H * 0.42, 0.30 + 0.5 * (1 - b));
      if (b > 0.02) drawRings(ctx, W, H, now / 1000, b * 0.8, W / 2, H * 0.42);
      if (flash) { flash.style.opacity = String(Math.pow(1 - ease(t / 0.45), 1.5)); if (t >= 0.45) { flash.remove(); flash = null; } }
      if (REDUCED) return;
      if (GALAXY && t > 0.55) {                                   /* braking done: melt into the candy galaxy */
        var o = 1 - (t - 0.55) / 0.45; c.style.opacity = String(Math.max(0, o));
        if (t >= 1) { c.remove(); return; }
      }
      requestAnimationFrame(frame);
    }
    requestAnimationFrame(frame);
  }

  function init() { hook(); if (document.body.hasAttribute('data-space')) space(); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
