// Silent UI loops (video[autoplay][muted]) on every page.
// 1. Only the loops that are on screen play. Phones cap how many videos can play at once,
//    so a page that tries to run all of them leaves some frozen on their poster frame.
// 2. Browsers pause these videos by themselves (tab or app switch, coming back to the page,
//    iPhone Low Power Mode). Anything on screen is restarted when the page is shown again
//    and on the next touch, click or scroll.
// Videos with a play button (no autoplay attribute) are never touched.
(function(){
  function init(){
    var vids = Array.prototype.slice.call(document.querySelectorAll('video[autoplay][muted]'));
    if (!vids.length) return;
    var hasIO = 'IntersectionObserver' in window;
    function start(v){ if (v.paused) { var p = v.play(); if (p && p.catch) p.catch(function(){}); } }
    function resume(){
      if (document.hidden) return;
      vids.forEach(function(v){ if (!hasIO || v._onscreen) start(v); });
    }
    if (hasIO) {
      var io = new IntersectionObserver(function(entries){
        entries.forEach(function(e){
          var v = e.target;
          v._onscreen = e.isIntersecting;
          if (e.isIntersecting) start(v); else v.pause();
        });
      }, { rootMargin: '100px 0px' });
      vids.forEach(function(v){ io.observe(v); });
    }
    var tick = 0;
    function soon(){ if (tick) return; tick = setTimeout(function(){ tick = 0; resume(); }, 150); }
    document.addEventListener('visibilitychange', resume);
    window.addEventListener('pageshow', resume);
    window.addEventListener('focus', resume);
    window.addEventListener('scroll', soon, { passive: true });
    document.addEventListener('touchend', resume, { passive: true });
    document.addEventListener('click', resume);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
