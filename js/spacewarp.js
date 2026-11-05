/* Gremlin shop card -> deep space takeover (scroll-driven). v5 Nov 4 2026: phone smoothing (stable canvas size, seeded stars, hysteresis, no mobile blur).
   Fixed canvas behind the page. As the Gremlin card scrolls into view the page
   dissolves into a starfield + nebulae + a spiral galaxy; scrolls back out after.
   Exposes window.__space() for QA. */
(function(){
  var PAGE = !!(document.currentScript && document.currentScript.dataset.mode==='page');
  var card = PAGE ? document.body : document.querySelector('.card.gremlin');
  if(!card) return;
  var c = document.createElement('canvas');
  c.id = 'spacefx';
  c.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0;transition:opacity .12s linear;';
  document.body.insertBefore(c, document.body.firstChild);
  var ctx = c.getContext('2d');
  var W=0,H=0,DPR=1, k=0, kTarget=0, t0=performance.now(), last=t0, scrollY=0;
  var stars=[], shoots=[], galaxy=[];
  var COLS=['#9ad63a','#d64dff','#ff4fa3','#4fd8ff']; // Gremlin quadrant colours

  var seed=1337; function srand(){ seed|=0; seed=seed+0x6D2B79F5|0; var t=Math.imul(seed^seed>>>15,1|seed); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }
  function rnd(a,b){ return a + srand()*(b-a); }
  var Hmax=0;
  function resize(){
    DPR = Math.min(window.devicePixelRatio||1, 2);
    var w = window.innerWidth, h = window.innerHeight;
    // phones: the browser toolbar collapsing/expanding fires resize with a small height change.
    // Keep the canvas at the tallest height seen so the bitmap never reallocates mid-scroll (that reallocation was the glitch).
    if(w===W && Hmax && h<=Hmax && Math.abs(h-H)<Hmax*.35){ H=h; return; }
    W=w; H=h; Hmax=Math.max(Hmax,h);
    c.width = W*DPR; c.height = Hmax*DPR; c.style.height=Hmax+'px'; ctx.setTransform(DPR,0,0,DPR,0,0);
    seed=1337; build();
  }
  function build(){
    stars=[]; var n = Math.round((W*H)/900); // ~330 on a phone, ~900 desktop
    for(var i=0;i<n;i++){
      var layer = srand()<.55?0:(srand()<.65?1:2); // 0 far, 2 near
      stars.push({x:srand()*W, y:srand()*Hmax*1.6, r:[.7,1.2,2.1][layer]*rnd(.7,1.4), l:layer,
        tw:rnd(0,6.28), ts:rnd(.6,2.2), col: srand()<.18 ? COLS[(srand()*4)|0] : '#ffffff', a:rnd(.6,1), big: srand()<.025});
    }
    galaxy=[]; var arms=2, per=260;
    for(var a=0;a<arms;a++) for(var i=0;i<per;i++){
      var f=i/per, ang = f*4.6 + a*Math.PI, rad = 8 + f*f*150;
      galaxy.push({ang:ang+rnd(-.22,.22), rad:rad*rnd(.85,1.12), s:rnd(.5,1.6), col: srand()<.5?'#ffffff':(srand()<.5?'#d64dff':'#4fd8ff'), a:rnd(.25,.9)*(1-f*.6)});
    }
  }
  function smooth(x){ x=Math.max(0,Math.min(1,x)); return x*x*(3-2*x); }
  var desk=false, cr=null;
  function measure(){
    var r = card.getBoundingClientRect(), vh = H;
    desk = (W > 640) && !PAGE; cr = r;
    if(PAGE){ kTarget = 1; scrollY = window.scrollY||0; return; }
    if(desk){ // desktop: space lives INSIDE the Gremlin card only, always on
      kTarget = (r.bottom > -40 && r.top < vh+40) ? 1 : 0; scrollY = window.scrollY||0; return; }
    // fade in while the card rises from the bottom; fade out while it leaves at the top
    var kin  = 1 - (r.top - vh*0.30)/(vh*0.70);
    var kout = (r.bottom - vh*0.02)/(vh*0.60);
    kTarget = smooth(Math.min(kin,kout));
    scrollY = window.scrollY||0;
  }
  function drawGalaxy(cx,cy,rot,scale,alpha){
    ctx.save(); ctx.translate(cx,cy); ctx.rotate(rot); ctx.scale(scale,scale*.42); ctx.rotate(-.5);
    var g = ctx.createRadialGradient(0,0,0,0,0,90);
    g.addColorStop(0,'rgba(255,255,255,'+(.55*alpha)+')'); g.addColorStop(.25,'rgba(214,77,255,'+(.22*alpha)+')'); g.addColorStop(1,'rgba(79,216,255,0)');
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(0,0,90,0,6.283); ctx.fill();
    for(var i=0;i<galaxy.length;i++){ var p=galaxy[i]; ctx.globalAlpha=p.a*alpha; ctx.fillStyle=p.col;
      ctx.beginPath(); ctx.arc(Math.cos(p.ang)*p.rad, Math.sin(p.ang)*p.rad, p.s, 0, 6.283); ctx.fill(); }
    ctx.globalAlpha=1; ctx.restore();
  }
  function nebula(x,y,rx,ry,col,alpha){
    ctx.save(); ctx.translate(x,y); ctx.scale(1,ry/rx);
    var g=ctx.createRadialGradient(0,0,0,0,0,rx); g.addColorStop(0,col.replace('A',alpha)); g.addColorStop(1,col.replace('A',0));
    ctx.fillStyle=g; ctx.beginPath(); ctx.arc(0,0,rx,0,6.283); ctx.fill(); ctx.restore();
  }
  function frame(now){
    var dt=Math.min(.05,(now-last)/1000); last=now; var T=(now-t0)/1000;
    k += (kTarget-k)*Math.min(1,dt*9);
    if(k<.004 && kTarget===0){ k=0; c.style.opacity=0; document.documentElement.style.setProperty('--space','0'); card.classList.remove('inspace'); requestAnimationFrame(frame); return; }
    c.style.opacity=1; document.documentElement.style.setProperty('--space',k.toFixed(3)); if(!PAGE){ if(k>.6) card.classList.add('inspace'); else if(k<.4) card.classList.remove('inspace'); }
    ctx.clearRect(0,0,W,Hmax);
    ctx.save();
    if(desk && cr){ ctx.beginPath(); var rr=18; ctx.moveTo(cr.left+rr,cr.top); ctx.arcTo(cr.right,cr.top,cr.right,cr.bottom,rr); ctx.arcTo(cr.right,cr.bottom,cr.left,cr.bottom,rr); ctx.arcTo(cr.left,cr.bottom,cr.left,cr.top,rr); ctx.arcTo(cr.left,cr.top,cr.right,cr.top,rr); ctx.closePath(); ctx.clip(); }
    // deep space base
    ctx.fillStyle='rgba(3,4,12,'+(k*0.96)+')'; ctx.fillRect(0,0,W,Hmax);
    var par = scrollY; var warp = desk ? 0 : (1-k)*k*4;
    var X0=0,Y0=0,CW=W,CH=H; if(desk&&cr){ X0=cr.left; Y0=cr.top; CW=cr.width; CH=cr.height; } // streak while transitioning (warp-in / warp-out)
    var parN = desk ? 0 : par;
    // nebulae in the four Gremlin colours, slow drift
    nebula((X0+CW*.18) + Math.sin(T*.07)*20, (Y0+CH*.30) - parN*.05, CW*.65, CH*.46, 'rgba(214,77,255,A)', .34*k);
    nebula((X0+CW*.85) + Math.cos(T*.05)*25, (Y0+CH*.72) - parN*.04, CW*.70, CH*.52, 'rgba(79,216,255,A)', .28*k);
    nebula((X0+CW*.60), (Y0+CH*.10) - parN*.06, CW*.45, CH*.30, 'rgba(255,79,163,A)', .24*k);
    nebula((X0+CW*.05), (Y0+CH*.95) - parN*.03, CW*.40, CH*.32, 'rgba(154,214,58,A)', .18*k);
    // spiral galaxy, parallax + slow spin
    if(PAGE){ // full page: galaxies in the outer margins, parallax with scroll
      drawGalaxy(W*.92, H*.18 - par*.10 + Math.sin(T*.1)*6, T*.03, Math.min(1.4, W/420), k*.8);
      drawGalaxy(W*.06, H*.85 - par*.06, 1.1+T*.02, Math.min(.9, W/520), k*.6);
    } else if(desk){ // desktop: galaxies tucked into the card corners, away from the copy
      drawGalaxy((X0+CW*1.0), (Y0+CH*.04) + Math.sin(T*.1)*4, T*.03, Math.min(1.3, CW/300), k*.6);
      drawGalaxy((X0+CW*.02), (Y0+CH*.99), 1.1+T*.02, Math.min(.8, CW/520), k*.5);
    } else {
      drawGalaxy((X0+CW*.78), (Y0+CH*.20) - parN*.08 + Math.sin(T*.1)*6, T*.03, Math.min(1.6, CW/300), k*.95);
      drawGalaxy((X0+CW*.15), (Y0+CH*.78) - parN*.11, 1.1+T*.02, Math.min(.9, CW/520), k*.7);
    }
    // stars with parallax + twinkle
    for(var i=0;i<stars.length;i++){ var s=stars[i]; var sp=[.04,.09,.16][s.l];
      var y = ((s.y - par*sp) % (Hmax*1.6)); if(y<0) y+=Hmax*1.6; y-=Hmax*.3;
      if(y<-10||y>Hmax+10) continue;
      var tw = .65 + .35*Math.sin(T*s.ts + s.tw); ctx.globalAlpha = s.a*tw*k;
      ctx.fillStyle = s.col;
      ctx.beginPath(); ctx.arc(s.x,y,s.r,0,6.283); ctx.fill();
      if(warp>.02){ var L=warp*s.r*44; ctx.globalAlpha*=Math.min(1,warp*6); ctx.fillRect(s.x - s.r*.5, y - L*.5, s.r, L); ctx.globalAlpha = s.a*tw*k; }
      if(s.big){ ctx.globalAlpha*= .7; ctx.fillRect(s.x-s.r*5, y-.5, s.r*10, 1); ctx.fillRect(s.x-.5, y-s.r*5, 1, s.r*10); }
    }
    ctx.globalAlpha=1;
    // shooting stars
    if(k>.6 && Math.random()<dt*.35) shoots.push({x:rnd(W*.1,W*.9), y:rnd(0,H*.4), vx:rnd(-520,-280), vy:rnd(140,260), life:rnd(.5,.9), t:0});
    for(var j=shoots.length-1;j>=0;j--){ var sh=shoots[j]; sh.t+=dt; if(sh.t>sh.life){ shoots.splice(j,1); continue; }
      var f=1-sh.t/sh.life; var x=sh.x+sh.vx*sh.t, y=sh.y+sh.vy*sh.t;
      var g=ctx.createLinearGradient(x,y,x-sh.vx*.12,y-sh.vy*.12); g.addColorStop(0,'rgba(255,255,255,'+(.95*f*k)+')'); g.addColorStop(1,'rgba(255,255,255,0)');
      ctx.strokeStyle=g; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-sh.vx*.12,y-sh.vy*.12); ctx.stroke(); }
    ctx.restore();
    requestAnimationFrame(frame);
  }
  window.addEventListener('resize', function(){ resize(); measure(); });
  window.addEventListener('scroll', measure, {passive:true});
  resize(); measure(); requestAnimationFrame(frame);
  window.__space = function(){ return {k:k, target:kTarget, stars:stars.length}; };
})();
