/* gate.js — passcode curtain for demo.sebastianmacan.com
 * Not bank security: keeps casual visitors out of the staging preview.
 * Passcode hash check (SHA-256) so the code isn't in plain text.
 */
(function () {
  "use strict";
  var KEY = "sm_demo_ok";
  if (sessionStorage.getItem(KEY) === "1") return;

  // SHA-256 of the passcode
  var HASH = "0ffe1abd1a08215353c233d6e009613e95eec4253832a761af28ff37ac5a150c";

  document.documentElement.style.visibility = "hidden";

  function sha256hex(str) {
    return crypto.subtle.digest("SHA-256", new TextEncoder().encode(str)).then(function (buf) {
      return Array.prototype.map.call(new Uint8Array(buf), function (b) {
        return ("0" + b.toString(16)).slice(-2);
      }).join("");
    });
  }

  function showGate() {
    document.documentElement.style.visibility = "";
    var css = ".smg-wrap{position:fixed;inset:0;background:#0a0a0c;z-index:99999;display:flex;align-items:center;justify-content:center;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Roboto,sans-serif}" +
      ".smg-box{text-align:center;padding:40px}" +
      ".smg-t{color:#f2f2f4;font-size:22px;font-weight:900;letter-spacing:-.02em;margin-bottom:6px}" +
      ".smg-s{color:#8a8a94;font-size:13px;margin-bottom:24px}" +
      ".smg-i{background:#141418;border:1px solid #2a2a32;border-radius:12px;padding:14px 16px;color:#f2f2f4;font-size:18px;text-align:center;letter-spacing:.3em;outline:none;width:180px}" +
      ".smg-i:focus{border-color:#8b5cf6}" +
      ".smg-i.smg-err{border-color:#ff3d5a;animation:smgshake .3s}" +
      "@keyframes smgshake{25%{transform:translateX(-6px)}75%{transform:translateX(6px)}}";
    var st = document.createElement("style"); st.textContent = css; document.head.appendChild(st);
    var wrap = document.createElement("div"); wrap.className = "smg-wrap";
    wrap.innerHTML = '<div class="smg-box"><div class="smg-t">Staging Preview</div><div class="smg-s">Enter passcode</div><input class="smg-i" type="password" inputmode="numeric" autocomplete="off" maxlength="12"></div>';
    document.body.appendChild(wrap);
    var inp = wrap.querySelector(".smg-i");
    inp.focus();
    inp.addEventListener("input", function () {
      inp.classList.remove("smg-err");
      sha256hex(inp.value).then(function (h) {
        if (h === HASH) {
          sessionStorage.setItem(KEY, "1");
          wrap.remove();
        } else if (inp.value.length >= 4) {
          inp.classList.add("smg-err");
        }
      });
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", showGate);
  } else {
    showGate();
  }
})();
