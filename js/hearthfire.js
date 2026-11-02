/* Hearth fire (fireplace.html rooms grid). Decorative, always burning.
   - Cursor / finger: flames lean toward and get pushed around by the pointer.
   - Double-click / double-tap: a pan slides in from the left, dumps water, fire goes out, steam, pan leaves, fire regrows. */
(function(){
  var cv=document.getElementById('hearthfire'); if(!cv) return;
  var ctx=cv.getContext('2d'), W=480, H=270; cv.width=W; cv.height=H;
  var t=0, rs=4242; function rnd(){ rs=(rs*1103515245+12345)&0x7fffffff; return rs/0x7fffffff; }
  var BASE=214, CX=240;
  var em=[]; for(var i=0;i<30;i++) em.push({x:170+rnd()*140,y:150+rnd()*90,s:rnd(),v:0.22+rnd()*0.5,r:0.8+rnd()*1.6,ph:rnd()*6.28});
  var F=[[172,66,20,'#c9401d',0,2.1],[200,88,22,'#e4591f',1.3,2.6],[230,106,24,'#ef7a22',2.2,2.3],[260,92,22,'#e4591f',0.7,2.8],[288,70,20,'#c9401d',1.9,2.2]];
  var I=[[185,42,12,'#f2a93b',0.4,3.1],[215,60,13,'#f7c04a',1.8,3.4],[245,68,14,'#f9d35c',2.9,3.0],[273,56,12,'#f7c04a',1.1,3.6]];

  /* pointer -> wind */
  var px=-1, py=-1, inside=false, wind=0, windT=0, poke=0;
  function toLocal(e){ var r=cv.getBoundingClientRect(); px=(e.clientX-r.left)/r.width*W; py=(e.clientY-r.top)/r.height*H; }
  cv.addEventListener('pointermove',function(e){ toLocal(e); inside=true; });
  cv.addEventListener('pointerenter',function(e){ toLocal(e); inside=true; });
  cv.addEventListener('pointerleave',function(){ inside=false; });
  cv.addEventListener('pointercancel',function(){ inside=false; });

  /* double click / tap -> douse */
  var state='burn', st=0, fs=1, lastTap=0, drops=[], steam=[];
  function douse(){ if(state!=='burn') return; state='pan_in'; st=0; }
  cv.addEventListener('dblclick',function(e){ e.preventDefault(); douse(); });
  cv.addEventListener('pointerdown',function(e){ var n=performance.now(); if(n-lastTap<380){ douse(); lastTap=0; } else lastTap=n; toLocal(e); inside=true; poke=1; });

  function flame(x,b,h,w,c,ph,sp,lean){
    var f=(1+0.18*Math.sin(t*sp+ph)+0.08*Math.sin(t*sp*2.3+ph*1.7))*fs; if(f<0.02) return;
    var l=8*Math.sin(t*0.9+ph)+lean;
    ctx.fillStyle=c; ctx.beginPath(); ctx.moveTo(x-w,b);
    ctx.bezierCurveTo(x-w*1.1,b-h*0.45*f,x-w*0.25+l*0.5,b-h*0.75*f,x+l,b-h*f);
    ctx.bezierCurveTo(x+w*0.25+l*0.5,b-h*0.75*f,x+w*1.1,b-h*0.45*f,x+w,b); ctx.closePath(); ctx.fill();
  }
  function leanFor(x,h){
    if(!inside) return 0;
    var dx=px-x, dy=py-(BASE-h*0.6), d=Math.sqrt(dx*dx+dy*dy);
    var near=Math.max(0,1-d/150);                 /* push away when the pointer is right in the fire */
    var pull=Math.max(-1,Math.min(1,dx/120));     /* lean toward the pointer across the tile */
    return pull*18*(1-near*0.6) - Math.sign(dx||1)*near*34*poke;
  }
  function drawPan(x,tilt){
    ctx.save(); ctx.translate(x,96); ctx.rotate(tilt);
    ctx.fillStyle='#2b2b30'; ctx.beginPath(); ctx.roundRect(-70,-16,80,32,[6,6,14,14]); ctx.fill();      /* pot body */
    ctx.fillStyle='#3a3a40'; ctx.fillRect(-70,-16,80,5);
    if(tilt<0.6){ ctx.fillStyle='#4a90ff'; ctx.beginPath(); ctx.roundRect(-64,-10,68,8,3); ctx.fill(); } /* water inside */
    ctx.fillStyle='#1c1c20'; ctx.beginPath(); ctx.roundRect(-150,-6,84,12,6); ctx.fill();                 /* handle */
    ctx.restore();
  }
  var last=performance.now(), dt=1/60;
  function frame(){
    var now=performance.now(); dt=Math.min(0.05,(now-last)/1000); last=now;
    ctx.clearRect(0,0,W,H);
    var g=(0.8+0.2*Math.sin(t*2.2)+0.06*Math.sin(t*7.1))*fs;
    var gr=ctx.createRadialGradient(CX,215,5,CX,215,170);
    gr.addColorStop(0,'rgba(255,120,30,'+(0.26*g).toFixed(3)+')'); gr.addColorStop(0.5,'rgba(255,80,10,'+(0.08*g).toFixed(3)+')'); gr.addColorStop(1,'rgba(255,80,10,0)');
    ctx.fillStyle=gr; ctx.fillRect(0,0,W,H);
    ctx.fillStyle='rgba(0,0,0,.35)'; ctx.beginPath(); ctx.ellipse(CX,238,120,10,0,0,6.28); ctx.fill();
    ctx.fillStyle='#3b2416'; ctx.beginPath(); ctx.roundRect(132,222,216,18,9); ctx.fill();
    ctx.fillStyle='#4a2d1a'; ctx.beginPath(); ctx.roundRect(152,207,176,17,8); ctx.fill();
    var k;
    for(k=0;k<F.length;k++) flame(F[k][0],BASE,F[k][1],F[k][2],F[k][3],F[k][4],F[k][5],leanFor(F[k][0],F[k][1]));
    for(k=0;k<I.length;k++) flame(I[k][0],BASE,I[k][1],I[k][2],I[k][3],I[k][4],I[k][5],leanFor(I[k][0],I[k][1])*0.8);
    for(k=0;k<em.length;k++){ var e=em[k]; e.y-=e.v*(0.3+0.7*fs); e.x+=Math.sin(t*1.6+e.ph)*0.3+(inside?Math.max(-1,Math.min(1,(px-e.x)/200))*0.6:0);
      if(e.y<20||rnd()<0.002){ e.y=200+rnd()*14; e.x=175+rnd()*130; }
      var a=Math.max(0,Math.min(1,(e.y-20)/120))*(0.55+0.45*Math.sin(t*5+e.ph))*fs;
      ctx.fillStyle='rgba(255,'+(150+Math.round(e.s*80))+',40,'+a.toFixed(2)+')'; ctx.beginPath(); ctx.arc(e.x,e.y,e.r,0,6.28); ctx.fill(); }
    /* water drops + steam */
    for(k=drops.length-1;k>=0;k--){ var d=drops[k]; d.vy+=0.35; d.x+=d.vx; d.y+=d.vy; if(d.y>BASE+4){ drops.splice(k,1); for(var s=0;s<2;s++) steam.push({x:d.x+(rnd()-0.5)*20,y:BASE-6,r:4+rnd()*6,a:0.55,vy:-(0.6+rnd()*0.7)}); continue; }
      ctx.fillStyle='rgba(90,160,255,.9)'; ctx.beginPath(); ctx.ellipse(d.x,d.y,3,5,0,0,6.28); ctx.fill(); }
    for(k=steam.length-1;k>=0;k--){ var sm=steam[k]; sm.y+=sm.vy*1.4; sm.r+=0.2; sm.a-=(state==='regrow'||state==='burn')?0.016:0.006; sm.x+=Math.sin(t*2+sm.r)*0.3; if(sm.a<=0){ steam.splice(k,1); continue; }
      ctx.fillStyle='rgba(220,225,235,'+sm.a.toFixed(3)+')'; ctx.beginPath(); ctx.arc(sm.x,sm.y,sm.r,0,6.28); ctx.fill(); }
    /* pan sequence */
    st+=dt;
    if(state==='pan_in'){ var p=Math.min(1,st/0.55), ease=1-Math.pow(1-p,3); drawPan(-160+ease*(CX-30+160),0); if(p>=1){ state='tip'; st=0; } }
    else if(state==='tip'){ var q=Math.min(1,st/0.45); drawPan(CX-30,q*1.25); if(q>0.35 && (st*20|0)!==((st-dt)*20|0)) for(var n=0;n<4;n++) drops.push({x:CX-28+Math.sin(q*3)*6+rnd()*10,y:108+rnd()*8,vx:0.4+(rnd()-0.5)*0.8,vy:1.5+rnd()*1.5});
      if(q>=1){ state='douse'; st=0; } }
    else if(state==='douse'){ drawPan(CX-30,1.25); if(st<0.5 && (st*20|0)!==((st-dt)*20|0)) for(var n2=0;n2<4;n2++) drops.push({x:CX-28+rnd()*10,y:108+rnd()*8,vx:0.4+(rnd()-0.5)*0.8,vy:1.5+rnd()*1.5}); fs=Math.max(0,1-st/0.35); if(st>0.9){ state='pan_out'; st=0; } }
    else if(state==='pan_out'){ var r2=Math.min(1,st/0.5), e2=r2*r2; drawPan(CX-30-e2*(CX+140),1.25-e2*1.25); if(r2>=1){ state='regrow'; st=0; } }
    else if(state==='regrow'){ fs=Math.min(1,st/2.4); fs=fs*fs*(3-2*fs); if(st>=2.4){ state='burn'; fs=1; } }
    poke*=0.9; t+=dt*60/60;
  }
  window.__douse=douse; window.__hearth=function(){ return state+' '+st.toFixed(2)+' fs='+fs.toFixed(2)+' drops='+drops.length+' steam='+steam.length; };
  var vis=true; function loop(){ if(vis) frame(); requestAnimationFrame(loop); }
  if('IntersectionObserver' in window){ new IntersectionObserver(function(en){ vis=en[0].isIntersecting; }).observe(cv); }
  loop();
})();
