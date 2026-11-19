/* Countertop Dispatch — page behaviour: comparison chooser, small touch-ups. */
(function () {
  "use strict";

  /* ---------- Comparison chooser (three questions → one verdict) ---------- */
  var chooser = document.getElementById("chooser");
  if (chooser) {
    var answers = { depth: null, style: null, volume: null };
    var VERDICTS = {
      // key: depth|style|volume → asin + text (all dimensions sourced from official listings)
      "small|basket|low":  { asin: "B08DKYBTPH", text: "Chefman 8 Qt TurboFry — smallest depth in the set (32.4 cm) and one basket is plenty if you cook for one or two." },
      "small|basket|high": { asin: "B08DKYBTPH", text: "Chefman 8 Qt TurboFry — the shallowest body here (32.4 cm deep). For larger batches you would cook in two rounds; a dual-basket model needs more depth." },
      "small|oven|low":    { asin: "B08DKYBTPH", text: "Chefman 8 Qt TurboFry — if counter depth is tight, the compact 4-in-1 is the honest fit, even though you asked for oven style." },
      "small|oven|high":   { asin: "B08DKYBTPH", text: "Chefman 8 Qt TurboFry — no oven-style model in this set fits a small-depth counter; the smallest option is the compact TurboFry." },
      "mid|basket|low":    { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — two 3 Qt drawers let you cook two sides at once without the oven footprint." },
      "mid|basket|high":   { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — the only two-drawer model in the set; 34.0 cm deep fits a mid-size counter." },
      "mid|oven|low":      { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — closest practical fit: more capacity than the compact single basket, far shallower than the 26 QT oven." },
      "mid|oven|high":     { asin: "B09B7SB46R", text: "Emeril Lagasse 26 QT French Door — oven style with real capacity (24.6 L), but check 42.9 cm of depth against your counter first." },
      "large|basket|low":  { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — dual drawers use width efficiently when depth is not the constraint." },
      "large|basket|high": { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — two baskets for parallel cooking; the 26 QT oven is the alternative if you prefer one big cavity." },
      "large|oven|low":    { asin: "B0CDY277D3", text: "Chefman 6 Qt Dual Basket — an oven-style cavity needs depth you said you don't have; the dual basket is the workable compromise." },
      "large|oven|high":   { asin: "B09B7SB46R", text: "Emeril Lagasse 26 QT French Door — the capacity pick: 26 quarts, French doors, 30+ presets, at the cost of the largest footprint in the set." }
    };

    chooser.addEventListener("click", function (e) {
      var btn = e.target.closest("button[data-q][data-v]");
      if (!btn) return;
      var q = btn.getAttribute("data-q");
      var v = btn.getAttribute("data-v");
      answers[q] = v;
      chooser.querySelectorAll('button[data-q="' + q + '"]').forEach(function (b) {
        b.setAttribute("aria-pressed", b === btn ? "true" : "false");
      });
      render();
    });

    function render() {
      var out = document.getElementById("chooser-verdict");
      var table = document.getElementById("comparison-table");
      if (!out) return;
      if (!answers.depth || !answers.style || !answers.volume) {
        out.textContent = "Answer all three questions to see a pick — nothing is hidden; every number below comes from the official listings.";
        if (table) table.querySelectorAll("tbody tr").forEach(function (r) {
          r.classList.remove("match", "dimmed");
        });
        return;
      }
      var key = answers.depth + "|" + answers.style + "|" + answers.volume;
      var verdict = VERDICTS[key];
      if (!verdict) return;
      out.innerHTML = "";
      var strong = document.createElement("strong");
      strong.textContent = "Our pick for your answers: ";
      out.appendChild(strong);
      out.appendChild(document.createTextNode(verdict.text + " "));
      var a = document.createElement("a");
      a.href = "https://www.amazon.com/dp/" + verdict.asin + "?tag=shopnow047c-20";
      a.rel = "sponsored noopener";
      a.target = "_blank";
      a.textContent = "See it on Amazon";
      out.appendChild(a);

      if (table) {
        table.querySelectorAll("tbody tr").forEach(function (r) {
          var match = r.getAttribute("data-asin") === verdict.asin;
          r.classList.toggle("match", match);
          r.classList.toggle("dimmed", !match);
        });
        var row = table.querySelector('tbody tr[data-asin="' + verdict.asin + '"]');
        if (row) row.scrollIntoView({ block: "nearest", behavior: "smooth" });
      }

      try {
        window.dispatchEvent(new CustomEvent("cd:chooser", {
          detail: {
            answers: [answers.depth, answers.style, answers.volume],
            verdict_asin: verdict.asin
          }
        }));
      } catch (e) { /* noop */ }
    }

    render();
  }

  /* ---------- Year in colophon is set by the build; nothing else to do. ---------- */
})();
