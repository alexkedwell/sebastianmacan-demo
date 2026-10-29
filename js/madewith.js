/* MADE WITH — track players + video lightbox. Shared by index.html cards and plugin pages.
   .mw[data-src]   = audio track (inline play/pause + progress)
   .mw[data-video] = opens a fullscreen 9:16 video lightbox with sound  */
(function(){
  var cur=null;
  function fmt(s){s=Math.max(0,s|0);return (s/60|0)+":"+("0"+(s%60)).slice(-2);}
  function stopCurrent(){ if(cur){cur();cur=null;} }

  /* ---- lightbox ---- */
  var lb=null, lbv=null;
  function lightbox(src,poster,title){
    stopCurrent();
    if(!lb){
      lb=document.createElement('div'); lb.className='mw-lb';
      lb.innerHTML='<div class="mw-lb-in"><video playsinline controls></video><div class="mw-lb-t"></div><span class="mw-lb-x" role="button" aria-label="Close">&times;</span></div>';
      document.body.appendChild(lb); lbv=lb.querySelector('video');
      function close(){ lbv.pause(); lb.classList.remove('on'); document.body.style.overflow=''; setTimeout(function(){ if(!lb.classList.contains('on')) lbv.removeAttribute('src'); },300); }
      lb.addEventListener('click',function(e){ if(e.target===lb) close(); });
      lb.querySelector('.mw-lb-x').addEventListener('click',close);
      document.addEventListener('keydown',function(e){ if(e.key==='Escape'&&lb.classList.contains('on')) close(); });
      lbv.addEventListener('ended',close);
    }
    lbv.poster=poster||''; lbv.src=src; lb.querySelector('.mw-lb-t').textContent=title||'';
    lb.classList.add('on'); document.body.style.overflow='hidden';
    var p=lbv.play(); if(p&&p.catch) p.catch(function(){});
  }

  document.querySelectorAll('.mw').forEach(function(el){
    var btn=el.querySelector('.mw-play'), t=el.querySelector('.mw-time');
    if(el.dataset.video){
      var v=document.createElement('video'); v.preload='metadata'; v.src=el.dataset.video;
      v.addEventListener('loadedmetadata',function(){ t.textContent=fmt(v.duration); });
      el.classList.add('vid');
      var open=function(e){ e.preventDefault(); e.stopPropagation(); lightbox(el.dataset.video, el.dataset.poster, el.querySelector('.mw-title').textContent); };
      btn.addEventListener('click',open); el.querySelector('.mw-body').addEventListener('click',open);
      return;
    }
    var a=new Audio(el.dataset.src); a.preload='metadata';
    var bar=el.querySelector('.mw-bar i'), seek=el.querySelector('.mw-bar');
    a.addEventListener('loadedmetadata',function(){t.textContent=fmt(a.duration);});
    a.addEventListener('timeupdate',function(){bar.style.width=(a.currentTime/a.duration*100)+'%';t.textContent=fmt(a.duration-a.currentTime);});
    /* Oct 26 2026: replay after the track ended needed a page refresh (Galaxy). Rewind on end, clear the
       "current" slot, and if play() is refused after an end (Safari drops the decoded buffer) reload + retry. */
    a.addEventListener('ended',function(){el.classList.remove('on');bar.style.width='0%';t.textContent=fmt(a.duration);a.currentTime=0;if(cur===stop)cur=null;setTimeout(function(){ if(a.paused){ a.load(); } },50);});
    function stop(){a.pause();el.classList.remove('on');}
    function start(){
      stopCurrent(); cur=stop; el.classList.add('on');
      if(a.ended||a.currentTime>=a.duration-0.05) a.currentTime=0;
      var p=a.play();
      if(p&&p.catch) p.catch(function(){ a.load(); a.currentTime=0; var q=a.play(); if(q&&q.catch) q.catch(function(){ el.classList.remove('on'); cur=null; }); });
    }
    btn.addEventListener('click',function(e){e.preventDefault();e.stopPropagation();
      if(a.paused){ start(); }
      else { stop(); cur=null; }
    });
    seek.addEventListener('click',function(e){e.stopPropagation();var r=seek.getBoundingClientRect();a.currentTime=(e.clientX-r.left)/r.width*a.duration;});
  });
})();
