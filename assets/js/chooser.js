/* The Crisp Counter — three-question chooser (decision D-12).
   Recommends spec priorities per format, never products: attribution and
   performance claims stay unverified by design. Emits EV-03 chooser_step. */
(function () {
  "use strict";
  var root = document.getElementById("chooser-app");
  if (!root) return;
  var dataEl = document.getElementById("chooser-data");
  var data = JSON.parse(dataEl.textContent);
  var answers = {};

  function render() {
    root.innerHTML = "";
    data.questions.forEach(function (q, i) {
      var step = document.createElement("div");
      step.className = "chooser-step";
      var h = document.createElement("h3");
      h.textContent = (i + 1) + ". " + q.q;
      step.appendChild(h);
      var opts = document.createElement("div");
      opts.className = "chooser-options";
      q.options.forEach(function (o) {
        var b = document.createElement("button");
        b.type = "button";
        b.textContent = o.label;
        if (answers[q.id] === o.key) b.className = "selected";
        b.addEventListener("click", function () {
          answers[q.id] = o.key;
          if (window.CC) window.CC.send("chooser_step", { step: q.id, choice: o.key });
          render();
        });
        opts.appendChild(b);
      });
      step.appendChild(opts);
      root.appendChild(step);
    });
    var done = data.questions.every(function (q) { return answers[q.id]; });
    if (done) root.appendChild(result());
  }

  function result() {
    var wrap = document.createElement("div");
    wrap.className = "chooser-result";
    var d = answers.depth, c = answers.cook, w = answers.cleanup;
    var title, blurb, checks = [];
    if (c === "batch" || (d === "deep" && c === "family")) {
      title = "Oven-style priorities";
      blurb = "Your answers point at a door-front air fryer oven: tray capacity and rack layers do the work. Compare listed depth against your counter first - these bodies run deepest.";
      checks = ["Single-layer tray area (what one rack actually holds)", "Door swing clearance at your spot", "Parts count for washing (racks, tray, crumb shelf, door)"];
    } else if (c === "family" && (d === "mid" || d === "shallow")) {
      title = "Dual-basket priorities";
      blurb = "Your answers point at two independent baskets in one body: two foods at two settings, finishing together. The trade is a wider body than a single basket.";
      checks = ["Each basket's single-layer area (2 x half is not one big layer)", "Sync/finish function if timing matters", "Two baskets = two wash-ups: dishwasher-safe parts help"];
    } else if (c === "snacks") {
      title = "Single-basket priorities";
      blurb = "Your answers point at the classic drawer: fastest for snacks and sides, easiest cleanup, smallest footprint. Buy for the meal you cook most, not the biggest number.";
      checks = ["Single-layer area over headline quarts", "Basket release and dishwasher-safe claim", "Weight if it will move in and out of a cupboard"];
    } else {
      title = "Space-first priorities";
      blurb = "Your answers make counter depth (or its absence) the boss. Shop by listed depth and weight, and let capacity be the second filter.";
      checks = ["Listed depth + the manual's clearance at your spot", "Capacity per centimetre of depth (see the method page)", "Weight and handle bulk for the daily move"];
    }
    if (d === "stored") checks.push("Weight and cord storage - you lift this thing daily");
    if (w === "dishwasher") checks.push("Dishwasher-safe removable parts, stated in the listing");
    if (w === "fewparts") checks.push("Fewest washable parts in the format you choose");

    var chip = document.createElement("span");
    chip.className = "chip";
    chip.textContent = "Your spec priorities";
    var h = document.createElement("h3");
    h.textContent = title;
    var p = document.createElement("p");
    p.textContent = blurb;
    var ul = document.createElement("ul");
    checks.forEach(function (t) {
      var li = document.createElement("li");
      li.textContent = t;
      ul.appendChild(li);
    });
    var note = document.createElement("p");
    note.className = "module-note";
    note.textContent = "The chooser recommends formats and spec checks - never products - so it stays honest while performance claims and click attribution remain unverified. Now take these checks to the table below.";
    wrap.appendChild(chip); wrap.appendChild(h); wrap.appendChild(p); wrap.appendChild(ul); wrap.appendChild(note);
    return wrap;
  }

  render();
})();
