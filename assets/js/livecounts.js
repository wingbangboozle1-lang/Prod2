/* Live, local-only display of the visitor's own aggregate counts on the
   events & privacy page. Reads the same localStorage counters analytics.js
   writes; sends nothing. */
(function () {
  "use strict";
  var out = document.getElementById("cc-live-counts");
  if (!out) return;
  function render() {
    var c = {};
    try { c = JSON.parse(localStorage.getItem("cc_counts_v1")) || {}; } catch (e) {}
    if (!Object.keys(c).length) { out.textContent = "(no events recorded yet in this browser)"; return; }
    out.textContent = JSON.stringify(c, null, 2);
  }
  render();
  document.addEventListener("cc:event", render);
})();
