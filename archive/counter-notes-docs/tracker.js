/*
 * Outbound-click counter for Counter Notes.
 *
 * Privacy posture:
 *  - No cookies, no local storage, no fingerprinting, no third-party scripts.
 *  - Events are pushed to window.dataLayer in the page only.
 *  - Nothing is transmitted unless the page has a data-analytics-endpoint value
 *    (currently empty; no endpoint is hosted, see flagged item FR-09).
 *
 * Defined events: only "outbound_click" is implemented. The brief names five
 * events, but their definitions were not supplied, so the other four are not built.
 */
(function () {
  "use strict";
  var endpoint = (document.body && document.body.getAttribute("data-analytics-endpoint")) || "";

  function record(name, detail) {
    var payload = {
      event: name,
      page: location.pathname,
      product: detail.product || null,
      ts: new Date().toISOString()
    };
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(payload);
    if (endpoint && navigator.sendBeacon) {
      navigator.sendBeacon(endpoint, JSON.stringify(payload));
    }
  }

  document.addEventListener("click", function (event) {
    var target = event.target;
    var anchor = target && target.closest ? target.closest("a[data-outbound]") : null;
    if (!anchor) { return; }
    record("outbound_click", { product: anchor.getAttribute("data-product") });
  }, true);
})();
