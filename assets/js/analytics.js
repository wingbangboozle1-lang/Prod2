/* The Crisp Counter — first-party, cookieless event recorder.
   Five defined events (data/events.json):
     page_view | product_link_click | chooser_step | article_read | guide_to_compare_click
   Aggregates in localStorage; optionally ships anonymous event lines to a
   self-hosted collector when window.CC_COLLECT_URL is configured.
   No cookies. No fingerprinting. No IP or user-agent storage. */
(function () {
  "use strict";
  var ENDPOINT = window.CC_COLLECT_URL || "";
  var KEY = "cc_counts_v1";

  function counts() {
    try { return JSON.parse(localStorage.getItem(KEY)) || {}; } catch (e) { return {}; }
  }
  function bump(ev) {
    var c = counts();
    c[ev] = (c[ev] || 0) + 1;
    c.__last = new Date().toISOString();
    try { localStorage.setItem(KEY, JSON.stringify(c)); } catch (e) { /* storage unavailable */ }
    return c;
  }
  function send(ev, props) {
    var c = bump(ev);
    try { document.dispatchEvent(new CustomEvent("cc:event", { detail: { event: ev, counts: c } })); } catch (e) {}
    if (!ENDPOINT) return;
    var body = JSON.stringify({
      event: ev,
      ts: new Date().toISOString(),
      path: location.pathname,
      props: props || {}
    });
    try {
      navigator.sendBeacon(ENDPOINT, new Blob([body], { type: "application/json" }));
    } catch (e) {
      try {
        fetch(ENDPOINT, { method: "POST", body: body, keepalive: true, headers: { "Content-Type": "application/json" } }).catch(function () {});
      } catch (e2) { /* offline */ }
    }
  }

  // EV-01 page_view
  send("page_view");

  // EV-02 product_link_click (sponsored anchors) and EV-05 guide_to_compare_click
  document.addEventListener("click", function (e) {
    if (!e.target || !e.target.closest) return;
    var a = e.target.closest('a[rel~="sponsored"], a.product-link');
    if (a) send("product_link_click", { href: a.getAttribute("href") });
    var g = e.target.closest('a[data-cc="guide-to-compare"]');
    if (g) send("guide_to_compare_click", { href: g.getAttribute("href") });
  }, true);

  // EV-04 article_read: past the 75% mark of the article body
  var art = document.querySelector(".article-body");
  if (art) {
    var sent = false;
    window.addEventListener("scroll", function () {
      if (sent) return;
      var r = art.getBoundingClientRect();
      if (r.top < window.innerHeight * 0.25) { sent = true; send("article_read"); }
    }, { passive: true });
  }

  window.CC = { counts: counts, send: send };
})();
