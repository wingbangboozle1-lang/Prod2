/* site.js — interactive bits: the three-question chooser (decision D-23).
   All routing uses only published listed values. */
(function () {
  "use strict";

  function show(html) {
    var out = document.getElementById("chooser-out");
    if (!out) return;
    out.innerHTML = html;
    out.classList.add("show");
  }

  function pick(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : null;
  }

  function runChooser() {
    var q1 = pick("q1"), q2 = pick("q2"), q3 = pick("q3");
    if (!q1 || !q2 || !q3) {
      show("<p>Please answer all three questions.</p>");
      return;
    }
    // Routing table built only from listed capacities and dimensions (see compare table).
    var format, product, why;
    if (q3 === "yes" || (q3 === "sometimes" && q1 === "l")) {
      format = "a dual-basket air fryer";
      product = "P1 — Chefman 6 qt dual basket";
      why = "Two independent 3 qt baskets with a listed Sync Finish are the direct answer to cooking two dishes at once (listed on the official listing).";
    } else if (q2 === "deep" && q1 !== "s") {
      format = "an oven-style air fryer";
      product = "P2 — Emeril Lagasse 26 qt French door";
      why = "Rack cooking with a 26 qt listed interior fits sheet-pan meals — and at a listed 16.9\" deep it needs a deeper counter than the basket types.";
    } else if (q2 === "shallow") {
      format = "a compact single-basket air fryer";
      product = "P3 — Chefman 8 qt TurboFry";
      why = "At a listed 12.75\" deep it is the shallowest of the three air fryers here, while keeping an 8 qt listed basket.";
    } else if (q1 === "s" && q3 === "no") {
      format = "a compact single-basket air fryer";
      product = "P3 — Chefman 8 qt TurboFry";
      why = "One basket, one job: the listed 8 qt basket handles one- and two-person meals without surrendering a second basket's footprint.";
    } else {
      format = "a dual-basket air fryer";
      product = "P1 — Chefman 6 qt dual basket";
      why = "For occasional two-dish cooking the dual basket flexes between one big zone and two 3 qt zones (listed).";
    }
    show(
      "<h3>Answer: " + format + "</h3>" +
      "<p><strong>Closest match in the shortlist: " + product + ".</strong> " + why + "</p>" +
      "<p class='muted'>This routes to a format based on listed values only — it is not a ranking, and prices and ratings are not published here. " +
      "<a href='compare.html#P1'>See the full comparison</a> or <a href='buying-guide.html'>read the buying guide</a>.</p>"
    );
  }

  /* The mobile compare bar (SG-23): dismissible, and it stays dismissed. No cookie, no
     storage beyond a single localStorage flag, no personal data - see privacy.html. */
  function initCompareBar() {
    var bar = document.getElementById("compare-bar");
    var close = document.getElementById("compare-bar-close");
    if (!bar || !close) return;
    try {
      if (window.localStorage.getItem("p2-bar-dismissed") === "1") bar.hidden = true;
    } catch (e) { /* private mode: leave the bar up */ }
    close.addEventListener("click", function () {
      bar.hidden = true;
      try { window.localStorage.setItem("p2-bar-dismissed", "1"); } catch (e) {}
    });
  }

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("chooser-run");
    if (btn) btn.addEventListener("click", runChooser);
    initCompareBar();
  });
})();
