/* decide.js — the buyer decision engine (content/pages/decide.html).

   Design rules, from the register rather than from taste:

   1. The recommendation is a FUNCTION, not a lookup table. Every branch is
      written in terms of a listed value (counter depth in inches, listed
      capacity, basket count, probe count, heat rating), so a reader can check
      the logic against the comparison table instead of trusting a score.
   2. Every answer names the listed fact it rests on AND the fact that would
      flip it to another machine. A recommendation that cannot say what would
      change its mind is an opinion, and this site does not publish opinions
      as findings.
   3. No price, no star rating, no popularity, no ranking language: the gate
      fails the build if any of those appear, and this file ships.
   4. Nothing here is measured beyond the five existing events. A decision
      path ending in a sponsored click is an outbound_click like any other, so
      measure.js already counts it; we add no new event vocabulary.
   5. Progressive enhancement: with JavaScript off the form still renders and
      the product cards below it still sell. The JSON-LD FAQ mirrors the same
      four decisions for a reader arriving from search.

   Nothing is transmitted. Nothing is stored except the reader's own local
   event counts, handled by measure.js. */
(function () {
  "use strict";

  var TAG = "?tag=shopnow047c-20";
  var PAID = "<span class=\"paid\">(paid link)</span>";

  /* Listed values, kept in one place so every branch cites the same number the
     comparison table prints. Source: data/p2/products.json (read 2026-11-14 to
     2026-11-20 from the official listings; see compare.html#table). */
  var FACTS = {
    P1: { depth: 13.38, width: 11.81, height: 10.63, qt: 6, baskets: 2 },
    P2: { depth: 16.9, width: 15.8, height: 14.8, qt: 26, baskets: 0 },
    P3: { depth: 12.75, width: 13.5, height: 10, qt: 8, baskets: 1 }
  };

  var MACHINE = {
    P1: {
      name: "Chefman 6 qt dual basket air fryer oven",
      short: "Chefman 6 qt dual basket",
      asin: "B0CDY277D3",
      format: "Dual-basket air fryer",
      label: "the dual-basket air fryer"
    },
    P2: {
      name: "Emeril Lagasse 26 qt French door air fryer toaster oven",
      short: "Emeril Lagasse 26 qt French door oven",
      asin: "B09B7SB46R",
      format: "Air fryer toaster oven",
      label: "the French-door oven"
    },
    P3: {
      name: "Chefman 8 qt TurboFry air fryer",
      short: "Chefman 8 qt TurboFry",
      asin: "B08DKYBTPH",
      format: "Single-basket air fryer",
      label: "the single-basket air fryer"
    },
    P4: {
      name: "ThermoMaven 1-second digital meat thermometer",
      short: "ThermoMaven instant-read",
      asin: "B0DHZTCNR5",
      format: "Instant-read thermometer",
      label: "the instant-read thermometer"
    },
    P5: {
      name: "CHEF iQ Sense Gen3 wireless meat thermometer",
      short: "CHEF iQ Sense Gen3",
      asin: "B0DZFD6R9Z",
      format: "Wireless leave-in thermometer",
      label: "the wireless leave-in thermometer"
    }
  };

  function buy(pid, text) {
    var url = "https://www.amazon.com/dp/" + MACHINE[pid].asin + TAG;
    return "<p class=\"out-buy\"><a class=\"btn btn-buy\" href=\"" + url + "\" " +
      "rel=\"sponsored nofollow noopener\" target=\"_blank\" data-affiliate=\"1\">" +
      text + "</a> " + PAID + "</p>";
  }

  function answer(pid, reason, fact, alt, caveat) {
    return { pid: pid, reason: reason, fact: fact, alt: alt, caveat: caveat };
  }

  /* ---------------------------------------------------------------- routing

     Air fryers, in the order a wrong guess costs the most money:
       counter depth first (a machine that does not fit is a return),
       then the two-dish question (it decides basket count),
       then capacity for the number of people. */
  function routeAirFryer(a) {
    var P1 = FACTS.P1, P2 = FACTS.P2, P3 = FACTS.P3;
    var twoDishes = a.cook === "two";
    var ovenCooking = a.cook === "oven";

    if (a.counter === "shallow") {
      return answer("P3",
        "At a listed " + P3.depth + "\" deep it is the shallowest of the three air fryers here, so it is the one that fits a counter under 13 inches — and it still lists an 8 qt basket, the largest single basket on this shelf.",
        "Counter depth: " + P3.depth + "\" (listed), against the " + P1.depth + "\" of the dual-basket machine and " + P2.depth + "\" of the oven.",
        twoDishes
          ? "You said you cook two dishes at once. This machine has one basket, so you would cook in two rounds. If two finishing times matter more than the counter, the dual basket is the trade — at " + P1.depth + "\" it needs about " + (P1.depth - P3.depth).toFixed(2) + "\" more depth."
          : "If your counter turns out to be deeper than you think, the dual-basket machine buys a second cooking zone for about " + (P1.depth - P3.depth).toFixed(2) + "\" more depth.",
        "One basket means one temperature and one timer. Sequencing two dishes is a manual job.");
    }

    if (twoDishes) {
      return answer("P1",
        "Two independent 3 qt baskets with a listed Sync Finish are the direct answer to two dishes that need to land at the same minute — and at a listed " + P1.depth + "\" deep it fits the 13-to-16-inch counter you described.",
        "Basket count: 2 independent 3 qt baskets (listed). Counter depth: " + P1.depth + "\" (listed).",
        a.counter === "deep"
          ? "If the two dishes are usually a main plus a tray of vegetables rather than two equal portions, the oven format holds more at once — but it needs " + P2.depth + "\" of depth."
          : "If you mostly cook one thing at a time, the single 8 qt basket gives you a bigger single zone for " + (P1.depth - P3.depth).toFixed(2) + "\" less depth.",
        "Dual zone is not the same as double capacity: each side is a 3 qt basket, so a full 6 qt batch still needs both zones at the same temperature.");
    }

    if (ovenCooking) {
      if (a.counter === "deep") {
        return answer("P2",
          "Rack cooking with a listed 26 qt interior is the only format on this shelf that takes a sheet pan flat, and your counter has the " + P2.depth + "\" of depth it asks for.",
          "Format: French-door toaster oven with racks (listed). Counter depth: " + P2.depth + "\" (listed). Listed capacity: 26 qt.",
          "If most of your cooking is a single basket of fries or wings, a basket machine heats a smaller volume and takes less counter — the oven only pays off when you use the racks.",
          "Oven-style machines preheat and cook differently from basket fryers; the listed 26 qt is interior volume, not a serving count.");
      }
      return answer("P2",
        "You described rack and sheet-pan cooking, which is what the oven format is for. Check the fit first: it lists a " + P2.depth + "\" depth, and you told us your counter is not clearly deeper than 16 inches.",
        "Counter depth: " + P2.depth + "\" (listed) — the deepest of the five tools here.",
        "If the tape measure says you have under 13 inches, the single-basket machine is the only one on this shelf that fits, at " + P3.depth + "\".",
        "We are not going to pretend this fits an unmeasured counter. Measure before you order — this is the one answer on this page that a 30-second check can change.");
    }

    // one-big-batch, or anything left over
    if (a.who === "crowd") {
      return answer("P2",
        "Five or more people, or hosting, is a volume problem before it is a format problem: the listed 26 qt interior of the oven format is the most cooking space on this shelf. It also needs the most counter, at " + P2.depth + "\".",
        "Listed capacity: 26 qt (oven) against 8 qt (single basket) and 6 qt total (dual baskets).",
        "For hosting, a second machine beats a bigger one: two basket fryers at different temperatures finish more food at once than one larger oven, if you have the counter.",
        "Bigger listed capacity does not mean faster: a larger interior takes longer to come to temperature.");
    }
    return answer("P3",
      "One big basket, one job: the listed 8 qt basket is the largest single zone here, and at " + P3.depth + "\" deep it asks for the least counter of the three air fryers.",
      "Listed capacity: 8 qt, single basket. Counter depth: " + P3.depth + "\" (listed).",
      "If you regularly cook two different things that need to finish together, the dual basket removes the sequencing — for about " + (P1.depth - P3.depth).toFixed(2) + "\" more depth.",
      "A single basket holds one temperature at a time; batch cooking means waiting between rounds.");
  }

  function routeThermometer(a) {
    if (a.check === "long" || a.basket === "air") {
      return answer("P5",
        "A probe you leave in while the food cooks is the only way to watch a long cook without opening the lid or the basket — and the listed probes are rated to 1000°F, which is what makes them usable inside an air fryer.",
        "Probe type: wireless leave-in, 3 probes in this configuration (listed). Heat rating: 1000°F (listed) — air-fryer-safe as listed.",
        "If you only ever want a number in the last minute of a cook, the instant-read does that in one second for a fraction of the complexity, and it never needs charging.",
        "This is the higher-commitment of the two: a hub, an app and probes to charge. Two probe-count variants exist on the listing (F-P05).");
    }
    return answer("P4",
      "You want a number now, at the counter or the grill, and a one-second thermocouple read is exactly that. The listed tolerance is ±0.5°F, and it needs no app and no hub.",
      "Read time: 1 second (listed). Stated tolerance: ±0.5°F, NIST-certified as claimed in the listing title.",
      "If you want the temperature watched for you over a two-hour cook, the leave-in probes do that; a hand-held probe cannot.",
      "Accuracy claims are the manufacturer's, published as listed and not graded by us. Placement matters more than the last half-degree — that is what the placement long read is about.");
  }

  function route(a) {
    return a.job === "temp" ? routeThermometer(a) : routeAirFryer(a);
  }

  /* ---------------------------------------------------------------- render */

  function read(form) {
    var a = {};
    ["job", "cook", "counter", "who", "check", "basket"].forEach(function (k) {
      var el = form.querySelector('input[name="' + k + '"]:checked');
      a[k] = el ? el.value : null;
    });
    return a;
  }

  function showQuestions(a) {
    // Only show the second-stage questions that the first answer can use, so a
    // thermometer shopper is never asked about counter depth.
    var isTemp = a.job === "temp";
    var pairs = [
      ["cook", !isTemp],
      ["counter", !isTemp],
      ["who", !isTemp],
      ["check", isTemp],
      ["basket", isTemp]
    ];
    pairs.forEach(function (p) {
      var fs = document.querySelector('.decide-q[data-q="' + p[0] + '"]');
      if (fs) fs.hidden = !p[1];
    });
  }

  function render(form) {
    var out = document.getElementById("decide-out");
    if (!out) return;
    var a = read(form);
    showQuestions(a);
    var r = route(a);
    var m = MACHINE[r.pid];
    var steps = a.job === "temp" ? 3 : 3;
    out.classList.remove("is-empty");
    out.innerHTML =
      "<p class=\"decide-progress\" aria-hidden=\"true\">" +
        new Array(steps + 1).join("<span class=\"on\"></span>") +
        new Array(4 - steps + 1).join("<span></span>") +
      "</p>" +
      "<p class=\"out-kicker\">Your answer</p>" +
      "<span class=\"out-format\">" + m.format + "</span>" +
      "<h3>" + m.name + "</h3>" +
      "<p class=\"out-reason\">" + r.reason + "</p>" +
      "<p class=\"out-fact\"><b>The listed fact this rests on.</b> " + r.fact +
        " <a href=\"compare.html#table\">Check it in the table</a>.</p>" +
      buy(r.pid, "Check the price of " + m.short + " on Amazon") +
      "<p class=\"out-alt\"><b>What would change this answer:</b> " + r.alt + "</p>" +
      "<p class=\"out-caveat\">" + r.caveat + " No price and no rating is published here (<a href=\"flagged.html#F-02\">F-02</a>). " +
        "<a href=\"products.html#" + r.pid + "\">Every listed spec for this machine</a>.</p>";
    if (out.scrollIntoView && window.matchMedia && window.matchMedia("(max-width: 60rem)").matches) {
      out.scrollIntoView({ block: "nearest", behavior: "smooth" });
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    var form = document.getElementById("decide-form");
    if (!form) return;
    showQuestions(read(form));
    form.addEventListener("change", function () { render(form); });
    form.addEventListener("submit", function (e) { e.preventDefault(); render(form); });
    var reset = document.getElementById("decide-reset");
    if (reset) {
      reset.addEventListener("click", function () {
        window.setTimeout(function () {
          var out = document.getElementById("decide-out");
          if (out) {
            out.classList.add("is-empty");
            out.innerHTML =
              "<p class=\"decide-progress\" aria-hidden=\"true\"><span class=\"on\"></span><span></span><span></span><span></span></p>" +
              "<p class=\"out-kicker\">Waiting on you</p><h3>The answer appears here</h3>" +
              "<p class=\"out-reason\">Answer the questions on the left and we will name one machine, quote the listed fact the answer rests on, and say what would change it.</p>" +
              "<p class=\"out-caveat\">Nothing on this page is a price, a rating or a rank (<a href=\"flagged.html#F-02\">F-02</a>).</p>";
          }
          showQuestions(read(form));
        }, 0);
      });
    }
  });
})();
