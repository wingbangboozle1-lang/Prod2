/* site.js — the interactive layer, kept small and dependency-free.

   1) Shelf filters on shop.html (progressive enhancement: without JavaScript
      every card is already visible, so the page still sells).
   2) The three-question chooser (decision D-23). Routing uses only published
      listed values, so a reader can check the answer against the comparison
      table.

   Nothing here sends data anywhere. Measurement lives in measure.js. */
(function () {
  "use strict";

  /* ------------------------------------------------------------------ filters */
  function slugify(s) {
    return s.toLowerCase().replace(/&/g, "and").replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
  }

  function initFilters() {
    var shelf = document.querySelector(".shelf");
    var status = document.getElementById("filter-status");
    if (!shelf || !status) return;

    var cards = Array.prototype.slice.call(shelf.querySelectorAll(".product-card"));
    if (!cards.length) return;

    // Tag each card with its format slug, read from the card's own rank label so
    // the filter can never disagree with the rendered card.
    cards.forEach(function (card) {
      var rank = card.querySelector(".rank");
      card.dataset.format = rank ? slugify(rank.textContent || "") : "";
      var href = card.querySelector('a[data-affiliate]');
      card.dataset.kind = href && /thermometer/i.test(card.textContent) ? "th" : "af";
    });

    var formatButtons = Array.prototype.slice.call(document.querySelectorAll("[data-format]"));
    var kindButtons = Array.prototype.slice.call(document.querySelectorAll("[data-filter]"));
    var allButton = document.querySelector('.chip[href="shop.html"]');
    var activeFormat = null;
    var activeKind = null;

    function apply() {
      var shown = 0;
      cards.forEach(function (card) {
        var ok =
          (!activeFormat || card.dataset.format === activeFormat) &&
          (!activeKind || card.dataset.kind === activeKind);
        card.hidden = !ok;
        if (ok) shown += 1;
      });
      formatButtons.forEach(function (b) {
        var on = b.getAttribute("data-format") === activeFormat;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.classList.toggle("is-active", on);
      });
      kindButtons.forEach(function (b) {
        var on = b.getAttribute("data-filter") === activeKind;
        b.setAttribute("aria-pressed", on ? "true" : "false");
        b.classList.toggle("is-active", on);
      });
      if (allButton) {
        var all = !activeFormat && !activeKind;
        allButton.setAttribute("aria-pressed", all ? "true" : "false");
        allButton.classList.toggle("is-active", all);
      }
      status.textContent = shown === cards.length
        ? "Showing all " + cards.length + " tools."
        : "Showing " + shown + " of " + cards.length + " tools.";
    }

    formatButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var f = btn.getAttribute("data-format");
        activeFormat = activeFormat === f ? null : f;
        apply();
      });
    });
    kindButtons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var k = btn.getAttribute("data-filter");
        activeKind = activeKind === k ? null : k;
        apply();
      });
    });
    if (allButton) {
      allButton.addEventListener("click", function (e) {
        e.preventDefault();
        activeFormat = null;
        activeKind = null;
        apply();
      });
    }
    apply();
  }

  /* ------------------------------------------------------------------ chooser */
  function show(html) {
    var out = document.getElementById("chooser-out");
    if (!out) return;
    out.innerHTML = html;
    out.classList.add("show");
    if (out.scrollIntoView) out.scrollIntoView({ block: "nearest", behavior: "smooth" });
  }

  function pick(name) {
    var el = document.querySelector('input[name="' + name + '"]:checked');
    return el ? el.value : null;
  }

  function buyFor(pid, label) {
    var url = "https://www.amazon.com/dp/" + pid + "?tag=shopnow047c-20";
    return '<p><a class="btn btn-sm" href="' + url + '" rel="sponsored nofollow noopener" ' +
      'target="_blank" data-affiliate="1">' + label + "</a> " +
      '<span class="paid">(paid link)</span></p>';
  }

  var ASIN = { P1: "B0CDY277D3", P2: "B09B7SB46R", P3: "B08DKYBTPH" };

  function runChooser() {
    var q1 = pick("q1"), q2 = pick("q2"), q3 = pick("q3");
    if (!q1 || !q2 || !q3) {
      show("<p>Please answer all three questions — each one narrows the format.</p>");
      return;
    }
    var format, product, why;
    if (q3 === "yes" || (q3 === "sometimes" && q1 === "l")) {
      format = "a dual-basket air fryer";
      product = "P1 — Chefman 6 qt dual basket";
      why = "Two independent 3 qt baskets with a listed Sync Finish are the direct answer to cooking two dishes at once.";
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
      why = "One basket, one job: the listed 8 qt basket handles one- and two-person meals without a second basket's footprint.";
    } else {
      format = "a dual-basket air fryer";
      product = "P1 — Chefman 6 qt dual basket";
      why = "For occasional two-dish cooking the dual basket flexes between one big zone and two 3 qt zones.";
    }
    var pid = product.slice(0, 2);
    show(
      "<h3>You are looking at " + format + ".</h3>" +
      "<p><strong>Closest match on this shelf: " + product + ".</strong> " + why + "</p>" +
      buyFor(ASIN[pid], "Check the " + product.split(" — ")[1] + " on Amazon") +
      "<p class='muted'>This routes to a format from listed values only — it is not a ranking, and no price or rating is published here. " +
      "<a href='compare.html#table'>Check it against the comparison table</a> or <a href='buying-guide.html'>read the buying guide</a>.</p>"
    );
  }

  document.addEventListener("DOMContentLoaded", function () {
    initFilters();
    var btn = document.getElementById("chooser-run");
    if (btn) btn.addEventListener("click", runChooser);
  });
})();
