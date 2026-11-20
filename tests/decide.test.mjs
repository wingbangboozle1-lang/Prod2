// tests/decide.test.mjs — the buyer decision engine (assets/js/decide.js).
//
// Why this test exists: decide.html promises three things to the reader.
//   1. The counter-depth question actually excludes machines that do not fit.
//   2. Every answer names the listed fact it rests on and the fact that would
//      flip it, so a recommendation is checkable against the comparison table.
//   3. No price, no star rating, no popularity and no ranking language is ever
//      produced — the publish gate forbids those, and the engine must too.
// A routing change that quietly breaks any of these would otherwise ship
// invisibly, because the page is interactive and the gate only reads HTML.
//
// The routing logic is sliced out of the shipped file rather than reimplemented,
// so this test fails if the file's structure changes in a way that would let the
// module and the test diverge.
import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
const SRC = readFileSync(path.join(ROOT, 'assets/js/decide.js'), 'utf8');

function engine() {
  const start = SRC.indexOf('var FACTS =');
  const end = SRC.indexOf('function read(form)');
  assert.ok(start > -1 && end > start, 'decide.js no longer has the FACTS..route block this test slices');
  const pure = SRC.slice(start, end);
  return new Function(pure + '\nreturn {route:route, FACTS:FACTS, MACHINE:MACHINE};')();
}

const {route, MACHINE} = engine();

const JOBS = ['fry', 'temp'];
const COOKS = ['two', 'one', 'oven'];
const COUNTERS = ['shallow', 'medium', 'deep', 'unknown'];
const WHOS = ['small', 'family', 'crowd'];
const CHECKS = ['spot', 'long'];
const BASKETS = ['air', 'hand'];

function every() {
  const out = [];
  for (const job of JOBS) for (const cook of COOKS) for (const counter of COUNTERS)
    for (const who of WHOS) for (const check of CHECKS) for (const basket of BASKETS)
      out.push({job, cook, counter, who, check, basket});
  return out;
}

test('every answer combination routes to one of the five registered products', () => {
  const all = every();
  assert.equal(all.length, 288);
  for (const a of all) {
    const r = route(a);
    assert.ok(MACHINE[r.pid], `unregistered product id ${r.pid} for ${JSON.stringify(a)}`);
  }
});

test('a counter under 13 inches never routes to a machine deeper than 13 inches', () => {
  // The published depths are 12.75 (P3), 13.38 (P1) and 16.9 (P2). This is the
  // single promise the page makes in its own copy, so it is the one to hold.
  for (const a of every().filter(x => x.counter === 'shallow' && x.job === 'fry')) {
    assert.equal(route(a).pid, 'P3', `shallow counter routed to ${route(a).pid}`);
  }
});

test('thermometer shoppers never receive an air fryer, and vice versa', () => {
  for (const a of every()) {
    const pid = route(a).pid;
    if (a.job === 'temp') assert.ok(['P4', 'P5'].includes(pid), `temp shopper got ${pid}`);
    if (a.job === 'fry') assert.ok(['P1', 'P2', 'P3'].includes(pid), `fry shopper got ${pid}`);
  }
});

test('two-dish cooking never routes to a single-basket machine when the counter allows', () => {
  for (const a of every().filter(x => x.job === 'fry' && x.cook === 'two' && x.counter !== 'shallow')) {
    assert.ok(['P1', 'P2'].includes(route(a).pid), `two-dish cooking got ${route(a).pid}`);
  }
});

test('every answer carries its listed fact, its falsifier and a caveat', () => {
  for (const a of every()) {
    const r = route(a);
    assert.ok(r.reason && r.reason.length > 40, `thin reason for ${JSON.stringify(a)}`);
    assert.ok(r.fact && r.fact.length > 20, `no listed fact for ${JSON.stringify(a)}`);
    assert.ok(r.alt && r.alt.length > 30, `no "what would change this" for ${JSON.stringify(a)}`);
    assert.ok(r.caveat && r.caveat.length > 15, `no caveat for ${JSON.stringify(a)}`);
  }
});

test('the engine never emits a price, a rating, a rank or a popularity claim', () => {
  // Mirrors the banned-claim gate in tools/checks.py, applied to the strings the
  // engine generates rather than to the published HTML.
  const banned = /\$\s?\d|out of 5 stars|best overall|top pick|#1\b|best[- ]selling|trending|most popular|highest[- ]rated/i;
  for (const a of every()) {
    const r = route(a);
    const blob = [r.reason, r.fact, r.alt, r.caveat].join(' ');
    assert.ok(!banned.test(blob), `banned claim in answer for ${JSON.stringify(a)}: ${blob.slice(0, 80)}`);
  }
});

test('every product the engine can name has a tagged, non-shortened buy URL', () => {
  // The page builds hrefs as https://www.amazon.com/dp/<ASIN>?tag=shopnow047c-20.
  // Assert the ASINs match the register and are never link.amazon short codes.
  const register = JSON.parse(readFileSync(path.join(ROOT, 'data/p2/products.json'), 'utf8')).products;
  const byId = Object.fromEntries(register.map(p => [p.id, p]));
  for (const [pid, m] of Object.entries(MACHINE)) {
    assert.equal(m.asin, byId[pid].asin, `${pid} ASIN drifted from data/p2/products.json`);
    assert.match(m.asin, /^[A-Z0-9]{10}$/, `${pid} is not a 10-character ASIN`);
    assert.ok(byId[pid].buy_url.includes(`?tag=shopnow047c-20`), `${pid} buy_url is untagged`);
  }
});
