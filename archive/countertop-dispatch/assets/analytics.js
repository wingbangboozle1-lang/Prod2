/* Countertop Dispatch — privacy-preserving event counter.
 *
 * Five defined events (see data/events.json): page_view, product_impression,
 * outbound_click, guide_read, chooser_result.
 *
 * Privacy: no cookies, no cross-site ids. A random session id lives in
 * sessionStorage only. Outbound clicks are reduced to their ASIN — query
 * strings are never transmitted. Until ENDPOINT below is provisioned
 * (see tools/analytics-endpoint.md), events stay in this browser and are
 * never sent anywhere.
 */
(function () {
  "use strict";

  var ENDPOINT = ""; // e.g. "https://stats.example.com/e" — empty = local only
  var KEY = "cd_session";
  var QUEUE_KEY = "cd_queue";
  var MAX_QUEUE = 100;

  function sessionId() {
    try {
      var id = sessionStorage.getItem(KEY);
      if (!id) {
        id = Array.from(crypto.getRandomValues(new Uint8Array(8)))
          .map(function (b) { return b.toString(16).padStart(2, "0"); })
          .join("");
        sessionStorage.setItem(KEY, id);
      }
      return id;
    } catch (e) {
      return "no-storage";
    }
  }

  function queueRead() {
    try {
      return JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
    } catch (e) {
      return [];
    }
  }

  function queueWrite(q) {
    try {
      localStorage.setItem(QUEUE_KEY, JSON.stringify(q.slice(-MAX_QUEUE)));
    } catch (e) { /* quota or privacy mode: drop silently */ }
  }

  function flush() {
    if (!ENDPOINT) return;
    var q = queueRead();
    if (!q.length) return;
    var payload = JSON.stringify({ events: q });
    try {
      if (navigator.sendBeacon) {
        var ok = navigator.sendBeacon(ENDPOINT, new Blob([payload], { type: "application/json" }));
        if (ok) { localStorage.removeItem(QUEUE_KEY); return; }
      }
      fetch(ENDPOINT, { method: "POST", body: payload, headers: { "Content-Type": "application/json" }, keepalive: true })
        .then(function () { localStorage.removeItem(QUEUE_KEY); })
        .catch(function () { /* keep queue for next flush */ });
    } catch (e) { /* keep queue */ }
  }

  function track(name, fields) {
    var ev = { name: name, session_id: sessionId(), ts: Math.floor(Date.now() / 1000) };
    Object.keys(fields || {}).forEach(function (k) { ev[k] = fields[k]; });
    try {
      window.dispatchEvent(new CustomEvent("cd:event", { detail: ev }));
    } catch (e) { /* noop */ }
    var q = queueRead();
    q.push(ev);
    queueWrite(q);
    flush();
  }

  window.cdTrack = track;

  function path() { return location.pathname.replace(/^.*\/Prod2/, "") || "/index.html"; }

  /* page_view */
  if (document.readyState !== "loading") {
    track("page_view", { path: path() });
  } else {
    document.addEventListener("DOMContentLoaded", function () {
      track("page_view", { path: path() });
    });
  }

  /* product_impression: product cards and data-table rows, 50% visible for 1s */
  function watchImpressions() {
    if (!("IntersectionObserver" in window)) return;
    var seen = new WeakSet();
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (!entry.isIntersecting) return;
        var el = entry.target;
        if (seen.has(el)) return;
        var timer = setTimeout(function () {
          if (entry.intersectionRatio < 0.5) return;
          seen.add(el);
          var asin = el.getAttribute("data-asin");
          if (asin) track("product_impression", { asin: asin, path: path() });
          obs.unobserve(el);
        }, 1000);
        el.addEventListener("cd:cancel", function () { clearTimeout(timer); }, { once: true });
      });
    }, { threshold: [0.5] });
    document.querySelectorAll(".product-card[data-asin], table.data tbody tr[data-asin]")
      .forEach(function (el) { obs.observe(el); });
  }

  /* outbound_click: rel=sponsored links, ASIN only */
  function watchOutbound() {
    document.addEventListener("click", function (e) {
      var a = e.target.closest && e.target.closest('a[rel~="sponsored"]');
      if (!a) return;
      var m = (a.getAttribute("href") || "").match(/\/dp\/([A-Z0-9]{10})/i);
      track("outbound_click", { asin: m ? m[1].toUpperCase() : "unknown", path: path() });
    }, true);
  }

  /* guide_read: article scrolled to 75%, once per session per article */
  function watchRead() {
    var article = document.querySelector("article.article");
    if (!article) return;
    var done = false;
    function onScroll() {
      if (done) return;
      var rect = article.getBoundingClientRect();
      var visible = Math.min(rect.bottom, innerHeight) - Math.max(rect.top, 0);
      if (visible / rect.height >= 0.75 || rect.bottom <= innerHeight * 1.05) {
        done = true;
        track("guide_read", { path: path() });
        removeEventListener("scroll", onScroll);
      }
    }
    addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  /* chooser_result: emitted by site.js after a verdict is rendered */
  addEventListener("cd:chooser", function (e) {
    track("chooser_result", e.detail || {});
  });

  /* flush queue when the tab is hidden */
  document.addEventListener("visibilitychange", function () {
    if (document.visibilityState === "hidden") flush();
  });

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", function () {
      watchImpressions(); watchOutbound(); watchRead();
    });
  } else {
    watchImpressions(); watchOutbound(); watchRead();
  }
})();
