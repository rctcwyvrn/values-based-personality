// Share widget for the results page.
//
// The primary action copies a short, snappy message to the clipboard. The
// message is the on-page headline plus the live browser URL (which encodes the
// ranking), so pasting it anywhere shares the result. On devices with the
// native Web Share sheet, an extra "Share…" button is revealed.

(function () {
  "use strict";

  const share = document.getElementById("share");
  if (!share) return;

  const text = share.dataset.text || document.title;
  const title = share.dataset.title || document.title;
  const feedback = document.getElementById("share-feedback");

  // Rebuild from the live URL (canonical https / behind-proxy correct).
  const message = () => `${text}\n${window.location.href}`;

  function flash(msg) {
    if (!feedback) return;
    feedback.textContent = msg;
    setTimeout(() => { feedback.textContent = ""; }, 2500);
  }

  async function copyMessage() {
    const payload = message();
    try {
      await navigator.clipboard.writeText(payload);
      flash("Copied! Paste it anywhere to share.");
    } catch (_) {
      // Fallback for older browsers / insecure contexts.
      const ta = document.createElement("textarea");
      ta.value = payload;
      ta.setAttribute("readonly", "");
      ta.style.position = "absolute";
      ta.style.left = "-9999px";
      document.body.appendChild(ta);
      ta.select();
      try {
        document.execCommand("copy");
        flash("Copied! Paste it anywhere to share.");
      } catch (__) {
        flash("Couldn't copy automatically. Select the text above.");
      }
      document.body.removeChild(ta);
    }
  }

  share.querySelectorAll("[data-share]").forEach((el) => {
    const kind = el.dataset.share;
    if (kind === "copy") {
      el.addEventListener("click", copyMessage);
    } else if (kind === "native") {
      if (navigator.share) {
        el.hidden = false;
        el.addEventListener("click", async () => {
          try {
            await navigator.share({ title, text, url: window.location.href });
          } catch (_) {
            /* user cancelled — ignore */
          }
        });
      }
    }
  });
})();
