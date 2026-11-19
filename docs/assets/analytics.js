
/* Countercraft privacy-preserving outbound-click counter.
   No cookies, no third parties. An anonymous id is stored in localStorage.
   Events: page_view, cta_click, product_click, filter_apply, guide_read.
   Point window.COUNTERCRAFT_ENDPOINT at your self-hosted /collect endpoint. */
(function () {
  var EVENTS = ["page_view","cta_click","product_click","filter_apply","guide_read"];
  var ENDPOINT = window.COUNTERCRAFT_ENDPOINT || "/collect";
  function uid() {
    var k = "cc_uid";
    try {
      var v = localStorage.getItem(k);
      if (!v) { v = "cc_" + Math.random().toString(36).slice(2, 10) + Date.now().toString(36);
        localStorage.setItem(k, v); }
      return v;
    } catch (e) { return "cc_anon"; }
  }
  var queue = [];
  function send() {
    if (!queue.length) return;
    var batch = queue.splice(0, queue.length);
    var body = JSON.stringify({ events: batch });
    try {
      if (navigator.sendBeacon) {
        navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
      } else {
        fetch(ENDPOINT, { method: "POST", body: body,
          headers: { "Content-Type": "application/json" }, keepalive: true });
      }
    } catch (e) { /* endpoint not hosted yet; events stay local and are not lost silently */ }
  }
  window.ccTrack = function (event, extra) {
    if (EVENTS.indexOf(event) === -1) return;
    queue.push({ event: event, path: location.pathname, ts: Date.now(),
                 ref: document.referrer, uid: uid(), extra: extra || null });
    if (queue.length >= 5) send();
  };
  document.addEventListener("click", function (e) {
    var el = e.target.closest("[data-event]");
    if (!el) return;
    var ev = el.getAttribute("data-event");
    if (EVENTS.indexOf(ev) === -1) return;
    window.ccTrack(ev, { asin: el.getAttribute("data-asin") || null,
                         label: (el.textContent || "").trim().slice(0, 80) });
  }, true);
  window.ccTrack("page_view");
  window.addEventListener("beforeunload", send);
})();
