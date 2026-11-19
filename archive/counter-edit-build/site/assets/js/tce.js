/* The Counter Edit — measurement + chooser layer.
   Privacy-preserving by construction: no cookies, no third-party requests by default.
   Events are appended to a per-browser queue (localStorage) and, only when a self-hosted
   endpoint is configured via window.TCE_ENDPOINT, beaconed as aggregate JSON.
   Five defined events (data/events.schema.json):
     E1 page_view · E2 outbound_product_click · E3 chooser_completed
     E4 article_half_read · E5 disclosure_viewed
*/
(function () {
  "use strict";
  var ENDPOINT = window.TCE_ENDPOINT || null;
  var QUEUE_KEY = "tce-events-v1";

  function queue(ev) {
    try {
      var q = JSON.parse(localStorage.getItem(QUEUE_KEY) || "[]");
      q.push(ev);
      while (q.length > 200) q.shift();
      localStorage.setItem(QUEUE_KEY, JSON.stringify(q));
    } catch (e) { /* storage unavailable — measurement silently off */ }
    if (ENDPOINT && navigator.sendBeacon) {
      try { navigator.sendBeacon(ENDPOINT, JSON.stringify(ev)); } catch (e) { /* noop */ }
    } else if (ENDPOINT && navigator.fetch) {
      try { fetch(ENDPOINT, { method: "POST", body: JSON.stringify(ev), keepalive: true }); } catch (e) { /* noop */ }
    }
  }

  function nowIso() { return new Date().toISOString(); }
  function path() { return location.pathname; }

  function sameOriginRef() {
    if (document.referrer.indexOf(location.origin) === 0) {
      return document.referrer.replace(location.origin, "");
    }
    return "";
  }

  /* E1 — page_view */
  queue({ event: "page_view", ts: nowIso(), path: path(), ref: sameOriginRef() });

  /* E2 — outbound product clicks */
  document.addEventListener("click", function (e) {
    var a = e.target && e.target.closest ? e.target.closest("a[data-outbound]") : null;
    if (!a) return;
    queue({
      event: "outbound_product_click",
      ts: nowIso(),
      path: path(),
      product: a.getAttribute("data-product") || "",
      position: a.getAttribute("data-position") || "",
      host: a.hostname || ""
    });
  }, { passive: true });

  /* E4 — article half read */
  var body = document.querySelector("[data-article-body]");
  if (body && "IntersectionObserver" in window) {
    var depth = { fifty: false, full: false };
    function watcher(marker, bucket) {
      return new IntersectionObserver(function (entries) {
        entries.forEach(function (en) {
          if (en.isIntersecting && !depth[bucket]) {
            depth[bucket] = true;
            queue({ event: "article_half_read", ts: nowIso(), path: path(), depth: bucket === "fifty" ? 50 : 100 });
          }
        });
      }, { threshold: 0.1 });
    }
    var mid = document.createElement("span");
    mid.style.cssText = "display:block;height:0";
    mid.setAttribute("aria-hidden", "true");
    body.appendChild(mid);
    var marker50 = watcher(mid, "fifty"); marker50.observe(mid);
    var endMarker = document.createElement("span");
    endMarker.style.cssText = "display:block;height:0";
    endMarker.setAttribute("aria-hidden", "true");
    body.appendChild(endMarker);
    var marker100 = watcher(endMarker, "full"); marker100.observe(endMarker);
  }

  /* E5 — disclosure viewed */
  var disc = document.querySelector("[data-disclosure]");
  if (disc && "IntersectionObserver" in window) {
    var seen = false;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting && !seen) {
          seen = true;
          queue({ event: "disclosure_viewed", ts: nowIso(), path: path() });
          io.disconnect();
        }
      });
    }, { threshold: 0.6 });
    io.observe(disc);
  }

  /* Chooser (compare page) — E3 chooser_completed */
  var form = document.getElementById("chooser-form");
  if (form) {
    var RESULT = {
      dual: {
        verdict: "Look at dual-basket air fryers first",
        why: "You cook two things at once and want them to finish together — two independent baskets with sync-finish are built for exactly that. Start with the Chefman 6 Qt dual basket.",
        pick: "P1"
      },
      oven: {
        verdict: "Look at oven-style air fryers first",
        why: "You want one appliance to roast, toast and air-fry bigger batches — a french-door oven-style unit trades counter space for versatility. Start with the Emeril Lagasse 26 QT.",
        pick: "P2"
      },
      compact: {
        verdict: "Look at compact single-basket fryers first",
        why: "Counter space beats batch size for you — a single 8-quart basket without a tower footprint is the sweet spot. Start with the Chefman 8 Qt TurboFry.",
        pick: "P3"
      },
      therm: {
        verdict: "Pair any fryer with an instant-read thermometer",
        why: "You care more about doneness than volume — a sub-second instant-read is the cheapest upgrade to every meal you already cook. Start with the ThermoMaven.",
        pick: "P4"
      },
      smart: {
        verdict: "Look at a wireless smart thermometer",
        why: "You want range and ambient-aware cooking without hovering over the grill — a multi-probe wireless unit covers it. Start with the CHEF iQ Sense.",
        pick: "P5"
      }
    };
    var out = document.getElementById("chooser-result");
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var answers = {};
      ["c-people", "c-space", "c-goal"].forEach(function (name) {
        var el = form.querySelector('input[name="' + name + '"]:checked');
        answers[name] = el ? el.value : null;
      });
      var pick = null;
      var goal = answers["c-goal"];
      if (goal === "twoatonce") pick = "dual";
      else if (goal === "bigbatches") pick = "oven";
      else if (goal === "smallcounter") pick = "compact";
      else if (goal === "doneness") pick = answers["c-people"] === "family" ? "smart" : "therm";
      else if (goal === "precision") pick = answers["c-space"] === "roomy" ? "smart" : "therm";
      if (!pick) pick = "dual";
      var r = RESULT[pick];
      var el = document.getElementById("chooser-result");
      el.querySelector(".verdict").textContent = r.verdict;
      el.querySelector(".why").textContent = r.why;
      var link = el.querySelector("a");
      link.setAttribute("href", "#" + r.pick);
      el.classList.add("show");
      queue({ event: "chooser_completed", ts: nowIso(), path: path(), answers: JSON.stringify(answers), recommendation: r.pick });
      el.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  }
})();
