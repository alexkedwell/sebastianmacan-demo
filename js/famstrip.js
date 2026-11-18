/* Character strip (creators page top, homepage bottom).
   Each character starts as a still picture. Its animation downloads only when the strip is near the screen,
   plays only while the strip is on screen, and never plays for visitors who asked their device for less motion. */
(function () {
  var rows = document.querySelectorAll('.fam .row');
  if (!rows.length || !('IntersectionObserver' in window)) return;
  if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  Array.prototype.forEach.call(rows, function (row) {
    var imgs = Array.prototype.slice.call(row.querySelectorAll('img[data-anim]'));
    if (!imgs.length) return;
    var started = false, onScreen = false;
    imgs.forEach(function (im) { im.setAttribute('data-still', im.getAttribute('src')); });
    function paint(im) {
      var want = (onScreen && im.famReady) ? im.getAttribute('data-anim') : im.getAttribute('data-still');
      if (im.getAttribute('src') !== want) im.setAttribute('src', want);
    }
    function start() {
      if (started) return; started = true;
      imgs.forEach(function (im) {
        var pre = new Image();
        pre.onload = function () { im.famReady = true; paint(im); };
        pre.src = im.getAttribute('data-anim');
      });
    }
    new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { onScreen = e.isIntersecting; });
      if (onScreen) start();
      imgs.forEach(paint);
    }, { rootMargin: '250px 0px' }).observe(row);
  });
})();
