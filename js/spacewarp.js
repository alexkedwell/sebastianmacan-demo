/* Gremlin shop card -> deep space takeover (scroll-driven). Mockup v1, Nov 3 2026.
   Fixed canvas behind the page. As the Gremlin card scrolls into view the page
   dissolves into a starfield + nebulae + a spiral galaxy; scrolls back out after.
   Exposes window.__space() for QA. */
(function(){
  var card = document.querySelector('.card.gremlin');
  if(!card) return;
  var c = document.createElement('canvas');
  c.id = 'spacefx';
  c.style.cssText = 'position:fixed;inset:0;width:100%;height:100%;z-index:0;pointer-events:none;opacity:0;transition:opacity .12s linear;';
  document.body.insertBefore(c, document.body.firstChild);
  var ctx = c.getContext('2d');
  var W=0,H=0,DPR=1, k=0, kTarget=0, t0=performance.now(), last=t0, scrollY=0;
  var stars=[], shoots=[], galaxy=[];
  var COLS=['#9ad63a','#d64dff','#ff4fa3','#4fd8ff']; // Gremlin quadrant colours

  function rnd(a,b){ return a + Math.random()*(b-a); }
  function resize(){
    DPR = Math.min(window.devicePixelRatio||1, 2);
    W = window.innerWidth; H = window.innerHeight;
    c.width = W*DPR; c.height = H*DPR; ctx.setTransform(DPR,0,0,DPR,0,0);
    build();
  }
  function build(){
    stars=[]; var n = Math.round((W*H)/900); // ~330 on a phone, ~900 desktop
    for(var i=0;i<n;i++){
      var layer = Math.random()<.55?0:(Math.random()<.65?1:2); // 0 far, 2 near
      stars.push({x:Math.random()*W, y:Math.random()*H*1.6, r:[.7,1.2,2.1][layer]*rnd(.7,1.4), l:layer,
        tw:rnd(0,6.28), ts:rnd(.6,2.2), col: Math.random()<.18 ? COLS[(Math.random()*4)|0] : '#ffffff', a:rnd(.6,1), big: Math.random()<.025});
    }
    galaxy=[]; var arms=2, per=260;
    for(var a=0;a<arms;a++) for(var i=0;i<per;i++){
      var f=i/per, ang = f*4.6 + a*Math.PI, rad = 8 + f*f*150;
      galaxy.push({ang:ang+rnd(-.22,.22), rad:rad*rnd(.85,1.12), s:rnd(.5,1.6), col: Math.random()<.5?'#ffffff':(Math.random()<.5?'#d64dff':'#4fd8ff'), a:rnd(.25,.9)*(1-f*.6)});
    }
  }
  function smooth(x){ x=Math.max(0,Math.min(1,x)); return x*x*(3-2*x); }
  function measure(){
    var r = card.getBoundingClientRect(), vh = H;
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
    c.style.opacity=1; document.documentElement.style.setProperty('--space',k.toFixed(3)); card.classList.toggle('inspace',k>.5);
    ctx.clearRect(0,0,W,H);
    // deep space base
    ctx.fillStyle='rgba(3,4,12,'+(k*0.96)+')'; ctx.fillRect(0,0,W,H);
    var par = scrollY; var warp=(1-k)*k*4; // streak while transitioning (warp-in / warp-out)
    // nebulae in the four Gremlin colours, slow drift
    nebula(W*.18 + Math.sin(T*.07)*20, H*.30 - par*.05, W*.65, H*.46, 'rgba(214,77,255,A)', .34*k);
    nebula(W*.85 + Math.cos(T*.05)*25, H*.72 - par*.04, W*.70, H*.52, 'rgba(79,216,255,A)', .28*k);
    nebula(W*.60, H*.10 - par*.06, W*.45, H*.30, 'rgba(255,79,163,A)', .24*k);
    nebula(W*.05, H*.95 - par*.03, W*.40, H*.32, 'rgba(154,214,58,A)', .18*k);
    // spiral galaxy, parallax + slow spin
    drawGalaxy(W*.78, H*.20 - par*.08 + Math.sin(T*.1)*6, T*.03, Math.min(1.6, W/300), k*.95);
    drawGalaxy(W*.15, H*.78 - par*.11, 1.1+T*.02, Math.min(.9, W/520), k*.7);
    // stars with parallax + twinkle
    for(var i=0;i<stars.length;i++){ var s=stars[i]; var sp=[.04,.09,.16][s.l];
      var y = ((s.y - par*sp) % (H*1.6)); if(y<0) y+=H*1.6; y-=H*.3;
      if(y<-10||y>H+10) continue;
      var tw = .65 + .35*Math.sin(T*s.ts + s.tw); ctx.globalAlpha = s.a*tw*k;
      ctx.fillStyle = s.col;
      if(warp>.08){ ctx.fillRect(s.x - s.r*.5, y - warp*s.r*22, s.r, warp*s.r*44 + s.r); }
      else { ctx.beginPath(); ctx.arc(s.x,y,s.r,0,6.283); ctx.fill();
        if(s.big){ ctx.globalAlpha*= .7; ctx.fillRect(s.x-s.r*5, y-.5, s.r*10, 1); ctx.fillRect(s.x-.5, y-s.r*5, 1, s.r*10); } }
    }
    ctx.globalAlpha=1;
    // shooting stars
    if(k>.6 && Math.random()<dt*.35) shoots.push({x:rnd(W*.1,W*.9), y:rnd(0,H*.4), vx:rnd(-520,-280), vy:rnd(140,260), life:rnd(.5,.9), t:0});
    for(var j=shoots.length-1;j>=0;j--){ var sh=shoots[j]; sh.t+=dt; if(sh.t>sh.life){ shoots.splice(j,1); continue; }
      var f=1-sh.t/sh.life; var x=sh.x+sh.vx*sh.t, y=sh.y+sh.vy*sh.t;
      var g=ctx.createLinearGradient(x,y,x-sh.vx*.12,y-sh.vy*.12); g.addColorStop(0,'rgba(255,255,255,'+(.95*f*k)+')'); g.addColorStop(1,'rgba(255,255,255,0)');
      ctx.strokeStyle=g; ctx.lineWidth=1.6; ctx.beginPath(); ctx.moveTo(x,y); ctx.lineTo(x-sh.vx*.12,y-sh.vy*.12); ctx.stroke(); }
    requestAnimationFrame(frame);
  }
  window.addEventListener('resize', function(){ resize(); measure(); });
  window.addEventListener('scroll', measure, {passive:true});
  resize(); measure(); requestAnimationFrame(frame);
  window.__space = function(){ return {k:k, target:kTarget, stars:stars.length}; };
})();
