/* os-dl.js — one download button per plugin.
 * Buttons carry data-mac / data-win. The button serves the visitor's own system.
 * The other system's installer is in the welcome email and in the library.
 * Default (Mac, phones, anything unknown) = the Mac installer, exactly what the HTML already says.
 * Runs before email-gate.js reads the href on click, so the gate hands out the right file. */
(function () {
  "use strict";
  var ua = (navigator.userAgent || "") + " " + (navigator.platform || "");
  var isWin = /Win(dows|32|64)/i.test(ua) && !/Windows Phone/i.test(ua);
  if (!isWin) return;
  var links = document.querySelectorAll("a[data-win][data-mac]");
  for (var i = 0; i < links.length; i++) {
    var a = links[i];
    if (a.hasAttribute("data-alt")) {
      a.setAttribute("href", a.getAttribute("data-mac"));
      a.textContent = "Mac version";
    } else {
      a.setAttribute("href", a.getAttribute("data-win"));
    }
  }
})();
