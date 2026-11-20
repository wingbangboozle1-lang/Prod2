/* measure.js — privacy-preserving first-party measurement.
   Five defined local events (data/events.json): page_view, outbound_click,
   guide_read_75, category_click, feed_click.

   Privacy rules enforced here:
   - no cookies, no visitor identifiers, no referrer capture
   - nothing leaves the browser unless the site's analytics endpoint is configured
     (data/settings.json -> analytics_endpoint); when empty, events are counted in
     this browser's localStorage only, for the visitor's own view.
   - outbound_click records the ASIN and the target host only, never the full URL */
(function () {
  "use strict";

  var ENDPOINT = ""; /* set at build time by tools/build.py if configured */
  try {
    ENDPOINT = document.documentElement.getAttribute("data-endpoint") || "";
  } catch (e) { /* ignore */ }

  var EVENTS = ["page_view", "outbound_click", "guide_read_75", "category_click", "feed_click"];

  function localCount(event) {
    try {
      var key = "p2-counts";
      var all = JSON.parse(localStorage.getItem(key) || "{}");
      all[event] = (all[event] || 0) + 1;
      localStorage.setItem(key, JSON.stringify(all));
    } catch (e) { /* storage unavailable: fine */ }
  }

  function record(event, fields) {
    if (EVENTS.indexOf(event) === -1) return;
    localCount(event);
    if (!ENDPOINT) return; /* nothing is transmitted while no endpoint is configured */
    var body = JSON.stringify(Object.assign({ event: event, path: location.pathname }, fields || {}));
    try {
      fetch(ENDPOINT, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: body,
        keepalive: true,
        mode: "no-cors"
      }).catch(function () { /* swallow */ });
    } catch (e) { /* swallow */ }
  }

  document.addEventListener("DOMContentLoaded", function () {
    record("page_view", {});

    /* outbound clicks on sponsored product links */
    document.querySelectorAll("a[data-affiliate]").forEach(function (a) {
      a.addEventListener("click", function () {
        var asin = (a.getAttribute("href") || "").match(/\/dp\/([A-Z0-9]{10})/);
        var host = "";
        try { host = new URL(a.href).hostname; } catch (e) { /* ignore */ }
        record("outbound_click", { asin: asin ? asin[1] : "", target: host });
      });
    });

    /* category entries: explicit data-category tiles, plus any link into a
       category page (the shelf filters route through prod2Record below). */
    var catLinks = Array.prototype.slice.call(
      document.querySelectorAll('a[data-category], a[href*="category-"]')
    );
    catLinks.forEach(function (a) {
      a.addEventListener("click", function () {
        var label = a.getAttribute("data-category") ||
          (a.getAttribute("href") || "").replace(/^.*category-/, "").replace(/\.html.*$/, "");
        record("category_click", { target: label });
      });
    });

    /* feed links */
    document.querySelectorAll("a[href$='feed.xml']").forEach(function (a) {
      a.addEventListener("click", function () { record("feed_click", {}); });
    });

    /* guide depth: fire once at 75% scroll on guide pages */
    if (document.body.getAttribute("data-page") &&
        document.body.getAttribute("data-page").indexOf("guide") === 0) {
      var fired = false;
      window.addEventListener("scroll", function () {
        if (fired) return;
        var h = document.documentElement;
        var depth = (window.scrollY + window.innerHeight) / h.scrollHeight;
        if (depth >= 0.75) { fired = true; record("guide_read_75", {}); }
      }, { passive: true });
    }
  });

  /* expose the recorder so the shelf filters can log a category selection
     without duplicating the endpoint logic (still one of the five events). */
  window.prod2Record = record;

  /* expose the local log for the measurement page */
  window.prod2LocalCounts = function () {
    try { return JSON.parse(localStorage.getItem("p2-counts") || "{}"); }
    catch (e) { return {}; }
  };
})();
