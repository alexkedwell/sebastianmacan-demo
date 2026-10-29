// Resume silent UI loops when iOS Safari comes back from the background / bfcache.
// Safari pauses every <video autoplay> on app switch and doesn't always restart them.
(function(){
  function resume(){
    document.querySelectorAll('video[autoplay][muted]').forEach(function(v){
      if(v.paused){ var p=v.play(); if(p&&p.catch) p.catch(function(){}); }
    });
  }
  document.addEventListener('visibilitychange',function(){ if(!document.hidden) resume(); });
  window.addEventListener('pageshow',resume);
  window.addEventListener('focus',resume);
})();
