/* email-gate.js — download gate for sebastianmacan.com
 * Intercepts .dl download clicks, asks for an email, POSTs it to the
 * capture endpoint, then starts the download.
 * IMPORTANT: the download is NEVER blocked — if the endpoint is down,
 * times out, or errors, we start the download anyway.
 */
(function () {
  "use strict";

  // Live endpoint: self-hosted capture service on the Mac mini, exposed via
  // Cloudflare Tunnel. See marketing/email-capture-plan.md.
  var ENDPOINT = "https://forms.ctssystemsai.com/subscribe";
  var TIMEOUT_MS = 6000; // never make the user wait longer than this
  var STORAGE_KEY = "sm_email_captured";

  var ACCENTS = {
    chaos:  { g1: "#ff3d5a", g2: "#7b5cff", shadow: "rgba(255,61,90,.35)" },
    dusty:  { g1: "#f5a623", g2: "#ff6b9d", shadow: "rgba(245,166,35,.32)" },
    ghost:  { g1: "#39e6d0", g2: "#8b5cf6", shadow: "rgba(57,230,208,.30)" },
    sugar:  { g1: "#ff8fc8", g2: "#7ef0d4", shadow: "rgba(255,143,200,.30)" },
    bounce: { g1: "#ff9f1c", g2: "#ffe14d", shadow: "rgba(255,159,28,.30)" },
    liftoff:{ g1: "#ff6b4a", g2: "#4ad9ff", shadow: "rgba(255,107,74,.30)" },
    orbit:  { g1: "#ff9d2e", g2: "#ffd76b", shadow: "rgba(255,157,46,.30)" },
    prism:  { g1: "#ff4ad9", g2: "#4affd9", shadow: "rgba(255,74,217,.30)" },
    jelly:  { g1: "#ff7ab8", g2: "#8fe8c0", shadow: "rgba(255,122,184,.30)" },
    fizz:   { g1: "#ffb347", g2: "#c8f05a", shadow: "rgba(255,179,71,.30)" },
    wizard: { g1: "#8b6bff", g2: "#ffd84a", shadow: "rgba(139,107,255,.30)" },
    magician: { g1: "#8b6bff", g2: "#ffd84a", shadow: "rgba(139,107,255,.30)" },
    biome:  { g1: "#3ecf6e", g2: "#5ad9d0", shadow: "rgba(62,207,110,.30)" },
    fauna:  { g1: "#3e9ecf", g2: "#7de8b8", shadow: "rgba(62,158,207,.30)" },
    gloss:  { g1: "#9be8c9", g2: "#f2a3c2", shadow: "rgba(155,232,201,.30)" },
    halo:   { g1: "#ffd700", g2: "#fff3b0", shadow: "rgba(255,215,0,.30)" },
    hitchords: { g1: "#f2f2f4", g2: "#8b5cf6", shadow: "rgba(139,92,246,.30)" },
    clubchords: { g1: "#4ad9ff", g2: "#ff4ad9", shadow: "rgba(74,217,255,.30)" },
    soulchords: { g1: "#ffd45c", g2: "#c8791c", shadow: "rgba(255,212,92,.30)" }
  };

  var css = "" +
    ".eg-overlay{position:fixed;inset:0;background:rgba(6,6,9,.78);backdrop-filter:blur(6px);-webkit-backdrop-filter:blur(6px);z-index:1000;display:flex;align-items:center;justify-content:center;padding:20px;opacity:0;transition:opacity .18s ease}" +
    ".eg-overlay.eg-show{opacity:1}" +
    ".eg-modal{background:#141418;border:1px solid #26262e;border-radius:20px;max-width:420px;width:100%;padding:36px 32px 30px;position:relative;transform:translateY(10px) scale(.98);transition:transform .18s ease;box-shadow:0 24px 80px rgba(0,0,0,.6)}" +
    ".eg-overlay.eg-show .eg-modal{transform:translateY(0) scale(1)}" +
    ".eg-close{position:absolute;top:14px;right:16px;background:none;border:none;color:#8a8a94;font-size:22px;line-height:1;cursor:pointer;padding:6px}" +
    ".eg-close:hover{color:#f2f2f4}" +
    ".eg-kind{font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:#8a8a94;font-weight:700;margin-bottom:8px}" +
    ".eg-title{font-size:26px;font-weight:900;letter-spacing:-.02em;line-height:1.15;color:#f2f2f4;margin:0 0 8px}" +
    ".eg-title em{font-style:normal;background:linear-gradient(135deg,var(--eg1),var(--eg2));-webkit-background-clip:text;background-clip:text;-webkit-text-fill-color:transparent}" +
    ".eg-sub{color:#8a8a94;font-size:14px;line-height:1.55;margin:0 0 22px}" +
    ".eg-form{display:flex;flex-direction:column;gap:12px}" +
    ".eg-input{background:#0e0e12;border:1px solid #2a2a32;border-radius:12px;padding:14px 16px;color:#f2f2f4;font-size:15px;outline:none;width:100%;transition:border-color .15s}" +
    ".eg-input:focus{border-color:var(--eg1)}" +
    ".eg-input.eg-err{border-color:#ff3d5a}" +
    ".eg-btn{border:none;cursor:pointer;color:#fff;font-weight:800;font-size:15px;padding:14px;border-radius:999px;letter-spacing:.02em;background:linear-gradient(135deg,var(--eg1),var(--eg2));box-shadow:0 8px 32px var(--egsh);transition:transform .15s,opacity .15s;font-family:inherit}" +
    ".eg-btn:hover{transform:translateY(-1px)}" +
    ".eg-btn:disabled{opacity:.6;cursor:default;transform:none}" +
    ".eg-skip{background:none;border:none;color:#8a8a94;font-size:12.5px;cursor:pointer;padding:4px;text-decoration:underline;text-underline-offset:3px;font-family:inherit}" +
    ".eg-skip:hover{color:#f2f2f4}" +
    ".eg-note{color:#5c5c66;font-size:11.5px;text-align:center;margin-top:2px}" +
    ".eg-hp{position:absolute;left:-9999px;opacity:0;height:0;width:0;pointer-events:none}" +
    "@media (max-width:480px){.eg-modal{padding:28px 22px 24px}}";

  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  function pluginOf(link) {
    var href = (link.getAttribute("href") || "").toLowerCase();
    var m = href.match(/downloads\/([a-z0-9]+)/);
    if (m && ACCENTS[m[1]]) return m[1];
    var sec = link.closest("section.plugin, .card");
    if (sec) {
      var names = Object.keys(ACCENTS);
      for (var i = 0; i < names.length; i++)
        if (sec.classList.contains(names[i])) return names[i];
    }
    return m ? m[1] : "plugin";
  }

  function startDownload(href) {
    var a = document.createElement("a");
    a.href = href;
    a.download = "";
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function postEmail(email, plugin) {
    // fire-and-forget with timeout; resolves regardless of outcome
    return new Promise(function (resolve) {
      var done = false;
      var finish = function () { if (!done) { done = true; resolve(); } };
      var t = setTimeout(finish, TIMEOUT_MS);
      try {
        var hp = document.getElementById("eg-hp");
        fetch(ENDPOINT, {
          method: "POST",
          keepalive: true, // survive page navigation / download start
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: email,
            plugin: plugin,
            hp: hp ? hp.value : ""
          })
        }).then(function () { clearTimeout(t); finish(); })
          .catch(function () { clearTimeout(t); finish(); });
      } catch (e) { clearTimeout(t); finish(); }
    });
  }

  function validEmail(v) {
    return /^[^@\s]+@[^@\s]+\.[^@\s]{2,}$/.test(v);
  }

  function openModal(href, plugin) {
    var acc = ACCENTS[plugin] || ACCENTS.chaos;
    var name = plugin.charAt(0).toUpperCase() + plugin.slice(1);

    var overlay = document.createElement("div");
    overlay.className = "eg-overlay";
    overlay.style.setProperty("--eg1", acc.g1);
    overlay.style.setProperty("--eg2", acc.g2);
    overlay.style.setProperty("--egsh", acc.shadow);
    overlay.innerHTML =
      '<div class="eg-modal" role="dialog" aria-modal="true" aria-label="Get ' + name + '">' +
      '<button class="eg-close" aria-label="Close">&times;</button>' +
      '<div class="eg-kind">Free Download</div>' +
      '<h3 class="eg-title">Get <em>' + name + '</em> + future updates</h3>' +
      '<p class="eg-sub">Drop your email and the download starts instantly. You\u2019ll also get new presets, updates and future plugins first. No spam, unsubscribe anytime.</p>' +
      '<form class="eg-form" novalidate>' +
      '<input class="eg-input" type="email" name="email" placeholder="you@studio.com" autocomplete="email" required>' +
      '<input class="eg-hp" type="text" id="eg-hp" name="website" tabindex="-1" autocomplete="off" aria-hidden="true">' +
      '<button class="eg-btn" type="submit">Send it \u2192 Download ' + name + '</button>' +
      '<div class="eg-note">Your email is only used for plugin news. Ever.</div>' +
      "</form></div>";

    document.body.appendChild(overlay);
    requestAnimationFrame(function () { overlay.classList.add("eg-show"); });

    var input = overlay.querySelector(".eg-input");
    var form = overlay.querySelector(".eg-form");
    var btn = overlay.querySelector(".eg-btn");

    function close() {
      overlay.classList.remove("eg-show");
      setTimeout(function () { overlay.remove(); }, 200);
      document.removeEventListener("keydown", onKey);
    }
    function onKey(e) { if (e.key === "Escape") close(); }
    document.addEventListener("keydown", onKey);

    overlay.addEventListener("click", function (e) {
      if (e.target === overlay) close();
    });
    overlay.querySelector(".eg-close").addEventListener("click", close);

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var email = input.value.trim();
      if (!validEmail(email)) {
        input.classList.add("eg-err");
        input.focus();
        return;
      }
      input.classList.remove("eg-err");
      btn.disabled = true;
      btn.textContent = "Starting download\u2026";
      postEmail(email, plugin).then(function () {
        try { localStorage.setItem(STORAGE_KEY, email); } catch (_) {}
        close();
        startDownload(href);
      });
    });

    setTimeout(function () { input.focus(); }, 60);
  }

  document.addEventListener("click", function (e) {
    var link = e.target.closest ? e.target.closest("a.dl") : null;
    if (!link) return;
    var href = link.getAttribute("href");
    if (!href || href.indexOf("downloads/") === -1) return;
    e.preventDefault();
    // Returning subscriber: silently re-log the plugin interest, download now.
    var known = null;
    try { known = localStorage.getItem(STORAGE_KEY); } catch (_) {}
    var plugin = pluginOf(link);
    if (known && validEmail(known)) {
      postEmail(known, plugin);
      startDownload(href);
      return;
    }
    openModal(href, plugin);
  });
})();
