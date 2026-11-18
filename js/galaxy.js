/* Candy Galaxy (Nov 18 2026, Alex): "a whole candy galaxy as the background for the gremlins page... candy planets,
   space ships shooting lazers at each other fly by... maybe a candy astronaut."
   <body data-galaxy> gets a fixed canvas behind the page. Everything is drawn in code (no image files):
     nebula + star field, five candy planets (lollipop swirl, sprinkle donut, candy-cane ringed jawbreaker, gumball,
     peppermint moon), a gummy bear astronaut on a slow tumble, two candy ships that fly past firing at each other,
     and a wrapped-candy comet now and then. Planets drift with the scroll (parallax).
   Tuning knobs are the constants right below. Reduced-motion visitors get one still frame. */
(function () {
  'use strict';
  if (!document.body || !document.body.hasAttribute('data-galaxy')) return;
  var REDUCED = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var FIGHT_EVERY = [9, 15];      /* seconds between dogfights (min, max) */
  var FIRST_FIGHT = 3.2;          /* seconds after load */
  var COMET_EVERY = [10, 18];
  var TAU = Math.PI * 2;
  var CANDY = ['#ff8ad8', '#6ec8ff', '#ffd84a', '#9ad63a', '#c9b6ff', '#ff6b6b', '#7ef0d4', '#ffffff'];

  var cv = document.createElement('canvas');
  cv.id = 'sm-galaxy'; cv.setAttribute('aria-hidden', 'true');
  cv.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;display:block;pointer-events:none;z-index:0;';
  document.body.insertBefore(cv, document.body.firstChild);
  var ctx = cv.getContext('2d'), W = 0, H = 0, D = 1, K = 1, NARROW = false, bg = null, stars = [], planets = [], sprites = {};

  function rnd(a, b) { return a + Math.random() * (b - a); }
  /* seeded so the galaxy looks the same on every visit */
  var seed = 20261118;
  function sr() { seed = (seed * 1664525 + 1013904223) >>> 0; return seed / 4294967296; }
  function srr(a, b) { return a + sr() * (b - a); }
  function off(w, h) { var c = document.createElement('canvas'); c.width = Math.ceil(w * D); c.height = Math.ceil(h * D); var x = c.getContext('2d'); x.scale(D, D); return [c, x]; }
  function shade(x, r, cx, cy) {   /* round-ball lighting on top of whatever is clipped to the circle */
    var g = x.createRadialGradient(cx - r * 0.38, cy - r * 0.42, r * 0.05, cx, cy, r * 1.05);
    g.addColorStop(0, 'rgba(255,255,255,.55)'); g.addColorStop(0.35, 'rgba(255,255,255,.08)'); g.addColorStop(0.75, 'rgba(20,6,50,.18)'); g.addColorStop(1, 'rgba(20,6,50,.62)');
    x.fillStyle = g; x.fillRect(cx - r, cy - r, r * 2, r * 2);
  }
  function glow(x, cx, cy, r, col) {
    var g = x.createRadialGradient(cx, cy, r * 0.7, cx, cy, r * 1.45);
    g.addColorStop(0, col); g.addColorStop(1, 'rgba(0,0,0,0)'); x.fillStyle = g; x.fillRect(cx - r * 1.5, cy - r * 1.5, r * 3, r * 3);
  }

  /* ---------- planet sprites ---------- */
  function swirl(r, c1, c2, arms, twist, halo) {
    var p = r * 0.5, o = off((r + p) * 2, (r + p) * 2), c = o[0], x = o[1], cx = r + p, cy = r + p;
    glow(x, cx, cy, r, halo);
    x.save(); x.beginPath(); x.arc(cx, cy, r, 0, TAU); x.clip();
    x.fillStyle = c2; x.fillRect(0, 0, c.width, c.height);
    x.fillStyle = c1;
    for (var a = 0; a < arms; a++) {
      var a0 = a / arms * TAU, wdt = TAU / arms / 2;
      x.beginPath(); x.moveTo(cx, cy);
      for (var i = 0; i <= 40; i++) { var q = i / 40, rr = q * r * 1.05, th = a0 + q * twist; x.lineTo(cx + Math.cos(th) * rr, cy + Math.sin(th) * rr); }
      for (i = 40; i >= 0; i--) { q = i / 40; rr = q * r * 1.05; th = a0 + wdt + q * twist; x.lineTo(cx + Math.cos(th) * rr, cy + Math.sin(th) * rr); }
      x.closePath(); x.fill();
    }
    shade(x, r, cx, cy); x.restore();
    return { c: c, half: r + p };
  }
  function jawbreaker(r, bands, halo) {
    var p = r * 0.5, o = off((r + p) * 2, (r + p) * 2), c = o[0], x = o[1], cx = r + p, cy = r + p;
    glow(x, cx, cy, r, halo);
    x.save(); x.beginPath(); x.arc(cx, cy, r, 0, TAU); x.clip();
    var n = bands.length, bh = r * 2 / n;
    x.fillStyle = bands[0]; x.fillRect(cx - r, cy - r, r * 2, r * 2);   /* no unpainted cap above the first curved band */
    for (var i = 0; i < n; i++) {
      x.fillStyle = bands[i]; x.beginPath();
      var y0 = cy - r + i * bh;
      x.moveTo(cx - r, y0); x.quadraticCurveTo(cx, y0 + bh * 0.55, cx + r, y0); x.lineTo(cx + r, cy + r); x.lineTo(cx - r, cy + r); x.closePath(); x.fill();
    }
    shade(x, r, cx, cy); x.restore();
    return { c: c, half: r + p };
  }
  function donut(r, halo) {
    var p = r * 0.5, o = off((r + p) * 2, (r + p) * 2), c = o[0], x = o[1], cx = r + p, cy = r + p, hole = r * 0.30;
    glow(x, cx, cy, r, halo);
    function ring(rad, wob, col) {
      x.fillStyle = col; x.beginPath();
      for (var i = 0; i <= 90; i++) { var a = i / 90 * TAU, rr = rad * (1 + wob * Math.sin(a * 7 + 1.3) + wob * 0.6 * Math.sin(a * 11)); x[i ? 'lineTo' : 'moveTo'](cx + Math.cos(a) * rr, cy + Math.sin(a) * rr); }
      x.closePath(); x.moveTo(cx + hole, cy); x.arc(cx, cy, hole, 0, TAU, true); x.fill('evenodd');
    }
    ring(r, 0, '#f2b872');
    x.save(); x.beginPath(); x.arc(cx, cy, r, 0, TAU); x.moveTo(cx + hole, cy); x.arc(cx, cy, hole, 0, TAU, true); x.clip('evenodd');
    ring(r * 0.86, 0.045, '#ff8ad8');
    x.lineCap = 'round'; x.lineWidth = Math.max(2, r * 0.045);
    for (var i = 0; i < 46; i++) {
      var a = srr(0, TAU), rr = srr(hole + r * 0.12, r * 0.74), t = srr(0, TAU), L = r * 0.07;
      x.strokeStyle = CANDY[(sr() * CANDY.length) | 0]; x.beginPath();
      x.moveTo(cx + Math.cos(a) * rr - Math.cos(t) * L, cy + Math.sin(a) * rr - Math.sin(t) * L); x.lineTo(cx + Math.cos(a) * rr + Math.cos(t) * L, cy + Math.sin(a) * rr + Math.sin(t) * L); x.stroke();
    }
    shade(x, r, cx, cy);
    x.restore();
    x.strokeStyle = 'rgba(90,40,20,.35)'; x.lineWidth = r * 0.03; x.beginPath(); x.arc(cx, cy, hole, 0, TAU); x.stroke();
    return { c: c, half: r + p };
  }
  function gumball(r, col, halo) {
    var p = r * 0.5, o = off((r + p) * 2, (r + p) * 2), c = o[0], x = o[1], cx = r + p, cy = r + p;
    glow(x, cx, cy, r, halo);
    x.save(); x.beginPath(); x.arc(cx, cy, r, 0, TAU); x.clip();
    x.fillStyle = col; x.fillRect(0, 0, c.width, c.height);
    x.fillStyle = 'rgba(20,6,50,.22)';
    [[0.35, -0.2, 0.2], [-0.3, 0.3, 0.15], [0.15, 0.45, 0.1], [-0.45, -0.3, 0.09]].forEach(function (q) { x.beginPath(); x.arc(cx + q[0] * r, cy + q[1] * r, q[2] * r, 0, TAU); x.fill(); });
    shade(x, r, cx, cy); x.restore();
    return { c: c, half: r + p };
  }

  /* ---------- gummy bear astronaut ---------- */
  function astronaut(s) {
    var o = off(s * 2.2, s * 2.6), c = o[0], x = o[1], cx = s * 1.1, cy = s * 1.3, col = '#ff5a7a', dk = '#d93a62';
    function blob(px, py, rx, ry, rot, fill) { x.fillStyle = fill; x.beginPath(); x.ellipse(cx + px * s, cy + py * s, rx * s, ry * s, rot || 0, 0, TAU); x.fill(); }
    /* jetpack (a marshmallow) + candy-cane hose */
    x.fillStyle = '#fff5fa'; x.beginPath(); (x.roundRect ? x.roundRect(cx - s * 0.36, cy - s * 0.12, s * 0.72, s * 0.62, s * 0.12) : x.rect(cx - s * 0.36, cy - s * 0.12, s * 0.72, s * 0.62)); x.fill();
    /* legs, arms (one waving), body */
    blob(-0.20, 0.62, 0.17, 0.24, 0.25, dk); blob(0.20, 0.62, 0.17, 0.24, -0.25, dk);
    blob(-0.42, 0.10, 0.15, 0.25, 0.9, dk); blob(0.44, -0.08, 0.15, 0.25, -2.2, dk);
    blob(0, 0.22, 0.36, 0.42, 0, col);
    blob(0, 0.30, 0.20, 0.24, 0, 'rgba(255,255,255,.16)');
    /* head + ears */
    blob(-0.22, -0.66, 0.11, 0.11, 0, dk); blob(0.22, -0.66, 0.11, 0.11, 0, dk);
    blob(0, -0.42, 0.30, 0.28, 0, col);
    blob(-0.10, -0.46, 0.035, 0.045, 0, '#3a0d22'); blob(0.10, -0.46, 0.035, 0.045, 0, '#3a0d22');
    x.strokeStyle = '#3a0d22'; x.lineWidth = s * 0.028; x.lineCap = 'round'; x.beginPath(); x.arc(cx, cy - s * 0.37, s * 0.07, 0.15 * Math.PI, 0.85 * Math.PI); x.stroke();
    blob(-0.10, -0.54, 0.09, 0.05, -0.5, 'rgba(255,255,255,.35)');
    /* glass helmet */
    var g = x.createRadialGradient(cx - s * 0.16, cy - s * 0.62, s * 0.04, cx, cy - s * 0.44, s * 0.5);
    g.addColorStop(0, 'rgba(255,255,255,.42)'); g.addColorStop(0.5, 'rgba(180,220,255,.10)'); g.addColorStop(1, 'rgba(180,220,255,.22)');
    x.fillStyle = g; x.beginPath(); x.arc(cx, cy - s * 0.44, s * 0.47, 0, TAU); x.fill();
    x.strokeStyle = 'rgba(255,255,255,.85)'; x.lineWidth = s * 0.03; x.stroke();
    x.strokeStyle = 'rgba(255,255,255,.9)'; x.lineWidth = s * 0.04; x.beginPath(); x.arc(cx, cy - s * 0.44, s * 0.37, 1.15 * Math.PI, 1.45 * Math.PI); x.stroke();
    /* collar */
    x.strokeStyle = '#ffd84a'; x.lineWidth = s * 0.07; x.beginPath(); x.ellipse(cx, cy - s * 0.06, s * 0.30, s * 0.07, 0, 0, Math.PI); x.stroke();
    /* lollipop in the waving hand */
    x.strokeStyle = '#ffffff'; x.lineWidth = s * 0.035; x.beginPath(); x.moveTo(cx + s * 0.58, cy - s * 0.22); x.lineTo(cx + s * 0.78, cy - s * 0.62); x.stroke();
    var lp = swirl(s * 0.17, '#ff8ad8', '#ffffff', 5, 2.4, 'rgba(0,0,0,0)');
    x.drawImage(lp.c, cx + s * 0.78 - lp.half, cy - s * 0.66 - lp.half, lp.half * 2, lp.half * 2);
    return { c: c, w: s * 2.2, h: s * 2.6 };
  }

  /* ---------- ships (both drawn nose-right) ---------- */
  function shipCorn(s) {         /* candy corn fighter */
    var o = off(s * 2.4, s * 1.4), c = o[0], x = o[1], cy = s * 0.7;
    x.save(); x.beginPath(); x.moveTo(s * 2.25, cy); x.quadraticCurveTo(s * 1.3, cy - s * 0.62, s * 0.5, cy - s * 0.5); x.quadraticCurveTo(s * 0.38, cy, s * 0.5, cy + s * 0.5); x.quadraticCurveTo(s * 1.3, cy + s * 0.62, s * 2.25, cy); x.closePath(); x.clip();
    x.fillStyle = '#ffd84a'; x.fillRect(0, 0, s * 1.05, s * 1.4); x.fillStyle = '#ff9f43'; x.fillRect(s * 1.05, 0, s * 0.7, s * 1.4); x.fillStyle = '#ffffff'; x.fillRect(s * 1.75, 0, s, s * 1.4);
    var g = x.createLinearGradient(0, cy - s * 0.6, 0, cy + s * 0.6); g.addColorStop(0, 'rgba(255,255,255,.45)'); g.addColorStop(0.5, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(60,10,60,.35)'); x.fillStyle = g; x.fillRect(0, 0, s * 2.4, s * 1.4);
    x.restore();
    x.fillStyle = '#ff6b6b'; x.beginPath(); x.moveTo(s * 0.75, cy - s * 0.42); x.lineTo(s * 0.2, cy - s * 0.68); x.lineTo(s * 0.5, cy - s * 0.3); x.fill();
    x.beginPath(); x.moveTo(s * 0.75, cy + s * 0.42); x.lineTo(s * 0.2, cy + s * 0.68); x.lineTo(s * 0.5, cy + s * 0.3); x.fill();
    x.fillStyle = 'rgba(190,235,255,.9)'; x.beginPath(); x.ellipse(s * 1.35, cy - s * 0.12, s * 0.3, s * 0.2, 0, Math.PI, TAU); x.fill();
    return { c: c, w: s * 2.4, h: s * 1.4, tail: s * 0.42 };
  }
  function shipWrap(s) {         /* wrapped-candy cruiser */
    var o = off(s * 2.6, s * 1.4), c = o[0], x = o[1], cy = s * 0.7, cx = s * 1.45;
    x.fillStyle = '#7ef0d4';
    x.beginPath(); x.moveTo(s * 0.75, cy); x.lineTo(s * 0.12, cy - s * 0.55); x.lineTo(s * 0.3, cy); x.lineTo(s * 0.12, cy + s * 0.55); x.closePath(); x.fill();
    x.beginPath(); x.moveTo(s * 2.1, cy); x.lineTo(s * 2.5, cy - s * 0.3); x.lineTo(s * 2.42, cy); x.lineTo(s * 2.5, cy + s * 0.3); x.closePath(); x.fill();
    x.save(); x.beginPath(); x.ellipse(cx, cy, s * 0.78, s * 0.46, 0, 0, TAU); x.clip();
    x.fillStyle = '#c9b6ff'; x.fillRect(0, 0, s * 2.6, s * 1.4);
    x.fillStyle = '#ffffff'; for (var i = -3; i < 6; i++) { x.beginPath(); x.moveTo(s * (0.5 + i * 0.36), 0); x.lineTo(s * (0.66 + i * 0.36), 0); x.lineTo(s * (0.36 + i * 0.36), s * 1.4); x.lineTo(s * (0.2 + i * 0.36), s * 1.4); x.fill(); }
    var g = x.createLinearGradient(0, cy - s * 0.5, 0, cy + s * 0.5); g.addColorStop(0, 'rgba(255,255,255,.5)'); g.addColorStop(0.5, 'rgba(255,255,255,0)'); g.addColorStop(1, 'rgba(40,10,80,.4)'); x.fillStyle = g; x.fillRect(0, 0, s * 2.6, s * 1.4);
    x.restore();
    x.fillStyle = 'rgba(190,235,255,.9)'; x.beginPath(); x.ellipse(cx + s * 0.12, cy - s * 0.3, s * 0.28, s * 0.22, 0, Math.PI, TAU); x.fill();
    return { c: c, w: s * 2.6, h: s * 1.4, tail: s * 0.2 };
  }

  /* ---------- build for the current window ---------- */
  function build() {
    D = Math.min(window.devicePixelRatio || 1, 1.5); W = window.innerWidth; H = window.innerHeight;
    cv.width = Math.round(W * D); cv.height = Math.round(H * D);
    NARROW = W < 1180; K = Math.max(0.55, Math.min(1.25, Math.min(W, 1500) / 1280));
    seed = 20261118;
    /* background: deep space, nebula clouds, a sugar-dust band */
    var o = off(W, H), x = o[1];
    if (bg && bg.parentNode) bg.parentNode.removeChild(bg);
    bg = o[0]; bg.setAttribute('aria-hidden', 'true'); bg.style.cssText = cv.style.cssText; document.body.insertBefore(bg, cv);
    var g = x.createLinearGradient(0, 0, W * 0.4, H); g.addColorStop(0, '#0c0624'); g.addColorStop(0.55, '#080516'); g.addColorStop(1, '#10072a'); x.fillStyle = g; x.fillRect(0, 0, W, H);
    x.globalCompositeOperation = 'lighter';
    [[0.10, 0.18, 0.55, '255,138,216', 0.20], [0.92, 0.30, 0.50, '110,200,255', 0.18], [0.80, 0.92, 0.55, '201,182,255', 0.17], [0.12, 0.85, 0.45, '126,240,212', 0.11], [0.50, 0.50, 0.70, '120,70,220', 0.10], [0.62, 0.08, 0.30, '255,216,74', 0.07]].forEach(function (n) {
      var R = Math.max(W, H) * n[2], gx = x.createRadialGradient(W * n[0], H * n[1], 0, W * n[0], H * n[1], R);
      gx.addColorStop(0, 'rgba(' + n[3] + ',' + n[4] + ')'); gx.addColorStop(0.5, 'rgba(' + n[3] + ',' + (n[4] * 0.35) + ')'); gx.addColorStop(1, 'rgba(' + n[3] + ',0)'); x.fillStyle = gx; x.fillRect(0, 0, W, H);
    });
    var dust = Math.round(W * H / 2600);
    for (var i = 0; i < dust; i++) {     /* sugar dust: denser along a diagonal band, like a milky way */
      var u = sr(), v = (sr() + sr() + sr()) / 3 - 0.5, band = sr() < 0.6;
      var px = band ? u * W * 1.2 - W * 0.1 : sr() * W, py = band ? H * (0.95 - u * 0.9) + v * H * 0.5 : sr() * H;
      x.globalAlpha = srr(0.25, 0.85); x.fillStyle = CANDY[(sr() * CANDY.length) | 0]; var rr = srr(0.35, 1.25);
      x.beginPath(); x.arc(px, py, rr, 0, TAU); x.fill();
    }
    x.globalAlpha = 1; x.globalCompositeOperation = 'source-over';
    /* twinklers */
    stars = [];
    for (i = 0; i < Math.round(W * H / 16000); i++) stars.push({ x: sr() * W, y: sr() * H, r: srr(0.8, 2.0), c: CANDY[(sr() * CANDY.length) | 0], p: sr() * TAU, s: srr(0.6, 2.2), big: sr() < 0.16 });
    /* planets: fx = fraction of width (edges on desktop so the copy stays clean), fy = fraction of a 2-screen tall loop */
    var R = 62 * K;
    sprites.lolly = swirl(R * 1.25, '#ff8ad8', '#fff5fa', 7, 2.6, 'rgba(255,138,216,.22)');
    sprites.donut = donut(R * 1.05, 'rgba(255,216,74,.16)');
    sprites.jaw = jawbreaker(R * 0.95, ['#6ec8ff', '#c9b6ff', '#ff8ad8', '#ffd84a', '#7ef0d4', '#6ec8ff'], 'rgba(110,200,255,.20)');
    sprites.gum = gumball(R * 0.5, '#7ef0d4', 'rgba(126,240,212,.20)');
    sprites.mint = swirl(R * 0.62, '#ff5a6e', '#ffffff', 6, 1.5, 'rgba(255,90,110,.18)');
    sprites.grape = gumball(R * 0.36, '#c9b6ff', 'rgba(201,182,255,.2)');
    planets = [
      { s: sprites.lolly, fx: NARROW ? 0.02 : 0.075, fy: 0.16, par: 0.16, spin: 0.05, bob: 9 },
      { s: sprites.jaw,   fx: NARROW ? 0.99 : 0.925, fy: 0.42, par: 0.22, spin: 0, bob: 7, ring: true },
      { s: sprites.donut, fx: NARROW ? 0.01 : 0.085, fy: 1.08, par: 0.19, spin: -0.07, bob: 8 },
      { s: sprites.gum,   fx: NARROW ? 0.94 : 0.885, fy: 0.84, par: 0.10, spin: 0.02, bob: 5 },
      { s: sprites.mint,  fx: NARROW ? 0.97 : 0.935, fy: 1.42, par: 0.13, spin: 0.09, bob: 6 },
      { s: sprites.grape, fx: NARROW ? 0.06 : 0.135, fy: 0.66, par: 0.08, spin: 0.03, bob: 4 }
    ];
    sprites.bear = astronaut(34 * K);
    sprites.corn = shipCorn(22 * K); sprites.wrap = shipWrap(22 * K);
  }

  /* ---------- actors ---------- */
  var fight = null, nextFight = FIRST_FIGHT, comet = null, nextComet = 6, bolts = [], sparks = [];
  function startFight(t) {
    var y1 = rnd(0.14, 0.80) * H, y2 = y1 + (Math.random() < 0.5 ? -1 : 1) * rnd(60, 130) * K;
    y2 = Math.max(H * 0.08, Math.min(H * 0.92, y2));
    var flip = Math.random() < 0.5;
    fight = { t0: t, dur: rnd(6.2, 7.6), a: { sp: flip ? sprites.corn : sprites.wrap, y: y1, dir: 1, col: '#ff8ad8', next: 1.1, ph: rnd(0, TAU) }, b: { sp: flip ? sprites.wrap : sprites.corn, y: y2, dir: -1, col: '#6ec8ff', next: 1.35, ph: rnd(0, TAU) } };
  }
  function shipPos(sh, u, t) {
    var m = 120 * K, x = sh.dir > 0 ? -m + (W + 2 * m) * u : W + m - (W + 2 * m) * u;
    return { x: x, y: sh.y + Math.sin(t * 1.3 + sh.ph) * 16 * K, a: Math.cos(t * 1.3 + sh.ph) * 0.07 * sh.dir };
  }
  function drawShip(sh, p, t) {
    var s = sh.sp;
    ctx.save(); ctx.translate(p.x, p.y); ctx.scale(sh.dir, 1); ctx.rotate(p.a);
    var fl = (0.75 + 0.25 * Math.sin(t * 40 + sh.ph)) * s.h * 0.9;       /* engine flame */
    var g = ctx.createLinearGradient(-s.w / 2 + s.tail, 0, -s.w / 2 + s.tail - fl, 0); g.addColorStop(0, 'rgba(255,255,255,.95)'); g.addColorStop(0.35, 'rgba(255,216,74,.8)'); g.addColorStop(1, 'rgba(255,107,107,0)');
    ctx.fillStyle = g; ctx.beginPath(); ctx.moveTo(-s.w / 2 + s.tail, -s.h * 0.16); ctx.lineTo(-s.w / 2 + s.tail - fl, 0); ctx.lineTo(-s.w / 2 + s.tail, s.h * 0.16); ctx.fill();
    ctx.drawImage(s.c, -s.w / 2, -s.h / 2, s.w, s.h);
    ctx.restore();
  }
  function burst(x, y, col) {
    for (var i = 0; i < 9; i++) { var a = rnd(0, TAU), v = rnd(40, 150) * K; sparks.push({ x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v, life: 0, max: rnd(0.35, 0.7), c: i % 3 ? CANDY[(Math.random() * CANDY.length) | 0] : col, r: rnd(1.2, 2.6) * K }); }
    sparks.push({ x: x, y: y, ring: true, life: 0, max: 0.4, c: col });
  }

  var last = 0, running = true, T = 0;
  function frame(now) {
    if (!running) return;
    var dt = Math.min(0.05, (now - last) / 1000 || 0); last = now; T += dt;
    var t = T, sy = window.scrollY || 0;
    ctx.setTransform(D, 0, 0, D, 0, 0);
    ctx.clearRect(0, 0, W, H);          /* the nebula is a still canvas underneath: painted once, never redrawn */
    /* twinkle */
    ctx.globalCompositeOperation = 'lighter';
    for (var i = 0; i < stars.length; i++) {
      var s = stars[i], a = 0.35 + 0.65 * (0.5 + 0.5 * Math.sin(t * s.s + s.p)), y = ((s.y - sy * 0.04) % H + H) % H;
      ctx.globalAlpha = a; ctx.fillStyle = s.c;
      if (s.big) { var L = s.r * 3.4 * (0.6 + 0.4 * a); ctx.beginPath(); ctx.moveTo(s.x - L, y); ctx.quadraticCurveTo(s.x, y, s.x, y - L); ctx.quadraticCurveTo(s.x, y, s.x + L, y); ctx.quadraticCurveTo(s.x, y, s.x, y + L); ctx.quadraticCurveTo(s.x, y, s.x - L, y); ctx.fill(); }
      else { ctx.beginPath(); ctx.arc(s.x, y, s.r, 0, TAU); ctx.fill(); }
    }
    ctx.globalCompositeOperation = 'source-over';
    /* planets */
    var loop = H * 2;
    ctx.globalAlpha = NARROW ? 0.5 : 1;
    for (i = 0; i < planets.length; i++) {
      var p = planets[i], hf = p.s.half, py = ((p.fy * H - sy * p.par + hf) % loop + loop) % loop - hf + Math.sin(t * 0.35 + i * 1.7) * p.bob * K, px = p.fx * W;
      if (py > H + hf) continue;
      var rx = hf * 1.05, ry = hf * 0.26;
      if (p.ring) { ctx.save(); ctx.translate(px, py); ctx.rotate(-0.38); ring(rx, ry, Math.PI, TAU, t); ctx.restore(); }
      ctx.save(); ctx.translate(px, py); if (p.spin) ctx.rotate(t * p.spin); ctx.drawImage(p.s.c, -hf, -hf, hf * 2, hf * 2); ctx.restore();
      if (p.ring) { ctx.save(); ctx.translate(px, py); ctx.rotate(-0.38); ring(rx, ry, 0, Math.PI, t); ctx.restore(); }
    }
    ctx.globalAlpha = 1;
    /* gummy bear astronaut: slow lissajous drift + tumble, stays near the edges on wide screens */
    var b = sprites.bear, bx = (NARROW ? 0.5 + 0.42 * Math.sin(t * 0.045 + 1.2) : 0.9 + 0.055 * Math.sin(t * 0.11)) * W, by = (0.62 + 0.2 * Math.sin(t * 0.07 + 2)) * H - (sy * 0.05) % (H * 0.2);
    ctx.save(); ctx.globalAlpha = NARROW ? 0.7 : 1; ctx.translate(bx, by); ctx.rotate(0.35 * Math.sin(t * 0.25) + t * 0.02); ctx.drawImage(b.c, -b.w / 2, -b.h / 2, b.w, b.h); ctx.restore();
    /* comet: a wrapped candy with a sparkle tail */
    if (!comet && t > nextComet) comet = { t0: t, x0: rnd(0.2, 1.1) * W, y0: -40, vx: -rnd(180, 260) * K, vy: rnd(120, 190) * K, c: CANDY[(Math.random() * 5) | 0] };
    if (comet) {
      var ct = t - comet.t0, cx = comet.x0 + comet.vx * ct, cy = comet.y0 + comet.vy * ct, ang = Math.atan2(comet.vy, comet.vx);
      var tg = ctx.createLinearGradient(cx, cy, cx - comet.vx * 0.5, cy - comet.vy * 0.5); tg.addColorStop(0, 'rgba(255,255,255,.7)'); tg.addColorStop(1, 'rgba(255,255,255,0)');
      ctx.strokeStyle = tg; ctx.lineWidth = 3 * K; ctx.lineCap = 'round'; ctx.beginPath(); ctx.moveTo(cx, cy); ctx.lineTo(cx - comet.vx * 0.5, cy - comet.vy * 0.5); ctx.stroke();
      ctx.save(); ctx.translate(cx, cy); ctx.rotate(ang + ct * 3); var q = 7 * K; ctx.fillStyle = comet.c;
      ctx.beginPath(); ctx.moveTo(-q, 0); ctx.lineTo(-q * 2.1, -q * 0.8); ctx.lineTo(-q * 2.1, q * 0.8); ctx.closePath(); ctx.fill(); ctx.beginPath(); ctx.moveTo(q, 0); ctx.lineTo(q * 2.1, -q * 0.8); ctx.lineTo(q * 2.1, q * 0.8); ctx.closePath(); ctx.fill();
      ctx.beginPath(); ctx.arc(0, 0, q, 0, TAU); ctx.fill(); ctx.fillStyle = 'rgba(255,255,255,.6)'; ctx.beginPath(); ctx.arc(-q * 0.3, -q * 0.3, q * 0.35, 0, TAU); ctx.fill(); ctx.restore();
      if (cy > H + 60 || cx < -60) { comet = null; nextComet = t + rnd(COMET_EVERY[0], COMET_EVERY[1]); }
    }
    /* dogfight */
    if (!fight && t > nextFight) startFight(t);
    if (fight) {
      var u = (t - fight.t0) / fight.dur, A = shipPos(fight.a, u, t), B = shipPos(fight.b, u, t), ft = t - fight.t0;
      [[fight.a, A, B], [fight.b, B, A]].forEach(function (z) {
        var sh = z[0], me = z[1], foe = z[2], ahead = (foe.x - me.x) * sh.dir;
        if (ft > sh.next && ahead > 60 * K && me.x > -20 && me.x < W + 20) {     /* only fire while the other ship is in front */
          sh.next = ft + rnd(0.28, 0.5);
          var lead = 0.18 * (W + 240 * K) / fight.dur, tx = foe.x - sh.dir * lead, ty = foe.y + rnd(-26, 26) * K, d = Math.hypot(tx - me.x, ty - me.y), v = 760 * K + W * 0.25;
          bolts.push({ x: me.x + sh.dir * sh.sp.w * 0.5, y: me.y, vx: (tx - me.x) / d * v, vy: (ty - me.y) / d * v, c: sh.col, life: 0, foe: sh === fight.a ? 'b' : 'a' });
        }
      });
      drawShip(fight.a, A, t); drawShip(fight.b, B, t);
      fight.pa = A; fight.pb = B;
      if (u >= 1) { fight = null; nextFight = t + rnd(FIGHT_EVERY[0], FIGHT_EVERY[1]); }
    }
    ctx.globalCompositeOperation = 'lighter'; ctx.lineCap = 'round';
    for (i = bolts.length - 1; i >= 0; i--) {
      var bo = bolts[i]; bo.life += dt; bo.x += bo.vx * dt; bo.y += bo.vy * dt;
      var tgt = fight ? (bo.foe === 'a' ? fight.pa : fight.pb) : null, sp2 = Math.hypot(bo.vx, bo.vy), L2 = 26 * K;
      if (tgt && Math.hypot(bo.x - tgt.x, bo.y - tgt.y) < 20 * K) { burst(bo.x, bo.y, bo.c); bolts.splice(i, 1); continue; }
      if (bo.life > 1.6 || bo.x < -60 || bo.x > W + 60 || bo.y < -60 || bo.y > H + 60) { bolts.splice(i, 1); continue; }
      ctx.globalAlpha = Math.min(1, 1.7 - bo.life);
      ctx.strokeStyle = bo.c; ctx.lineWidth = 5 * K; ctx.beginPath(); ctx.moveTo(bo.x, bo.y); ctx.lineTo(bo.x - bo.vx / sp2 * L2, bo.y - bo.vy / sp2 * L2); ctx.stroke();
      ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2 * K; ctx.beginPath(); ctx.moveTo(bo.x, bo.y); ctx.lineTo(bo.x - bo.vx / sp2 * L2 * 0.8, bo.y - bo.vy / sp2 * L2 * 0.8); ctx.stroke();
    }
    for (i = sparks.length - 1; i >= 0; i--) {
      var k = sparks[i]; k.life += dt; var f = k.life / k.max; if (f >= 1) { sparks.splice(i, 1); continue; }
      ctx.globalAlpha = 1 - f;
      if (k.ring) { ctx.strokeStyle = k.c; ctx.lineWidth = 2.5 * K * (1 - f); ctx.beginPath(); ctx.arc(k.x, k.y, (6 + 30 * f) * K, 0, TAU); ctx.stroke(); }
      else { k.x += k.vx * dt; k.y += k.vy * dt; ctx.fillStyle = k.c; ctx.beginPath(); ctx.arc(k.x, k.y, k.r, 0, TAU); ctx.fill(); }
    }
    ctx.globalAlpha = 1; ctx.globalCompositeOperation = 'source-over';
    if (!REDUCED) requestAnimationFrame(frame);
  }
  function ring(rx, ry, a0, a1, t) {      /* candy-cane ring: white band with red stripes that crawl round */
    ctx.lineCap = 'butt';
    ctx.strokeStyle = 'rgba(255,255,255,.95)'; ctx.lineWidth = 9 * K; ctx.setLineDash([]); ctx.beginPath(); ctx.ellipse(0, 0, rx, ry, 0, a0, a1); ctx.stroke();
    ctx.strokeStyle = '#ff5a6e'; ctx.lineWidth = 9 * K; ctx.setLineDash([9 * K, 11 * K]); ctx.lineDashOffset = -t * 6; ctx.beginPath(); ctx.ellipse(0, 0, rx, ry, 0, a0, a1); ctx.stroke();
    ctx.setLineDash([]);
  }

  build();
  var rz; window.addEventListener('resize', function () { clearTimeout(rz); rz = setTimeout(function () { build(); if (REDUCED) requestAnimationFrame(frame); }, 150); });
  document.addEventListener('visibilitychange', function () { running = !document.hidden; if (running) { last = performance.now(); requestAnimationFrame(frame); } });
  if (REDUCED) window.addEventListener('scroll', function () { requestAnimationFrame(frame); }, { passive: true });
  window.SM_GALAXY = { fightNow: function () { nextFight = 0; }, state: function () { return { fight: !!fight, bolts: bolts.length, sparks: sparks.length, planets: planets.length, t: T }; } };
  last = performance.now(); requestAnimationFrame(frame);
})();
