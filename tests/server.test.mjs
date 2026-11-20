import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {mkdtemp, readFile, rm} from 'node:fs/promises';
import http from 'node:http';
import {tmpdir} from 'node:os';
import path from 'node:path';
import test from 'node:test';

const repo = path.resolve(new URL('..', import.meta.url).pathname);
const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

// Send a request path verbatim, without the normalisation fetch() applies.
function rawStatus(port, method, rawPath) {
  return new Promise((resolve, reject) => {
    const request = http.request({host: '127.0.0.1', port, method, path: rawPath},
      (response) => {
        response.resume();
        response.on('end', () => resolve(response.statusCode));
      });
    request.on('error', reject);
    request.end();
  });
}

async function waitUntilReady(url, process) {
  const deadline = Date.now() + 5000;
  while (Date.now() < deadline) {
    if (process.exitCode !== null) throw new Error(`server exited with ${process.exitCode}`);
    try {
      const response = await fetch(url);
      if (response.ok) return response;
    } catch {}
    await pause(50);
  }
  throw new Error(`server did not listen at ${url}`);
}

test('local event endpoint serves docs and aggregates the five privacy-preserving publication events', async (t) => {
  const dir = await mkdtemp(path.join(tmpdir(), 'prod2-events-'));
  const port = 23000 + Math.floor(Math.random() * 20000);
  const base = `http://127.0.0.1:${port}`;
  const child = spawn(process.execPath, ['server.mjs'], {
    cwd: repo,
    env: {...process.env, PORT: String(port), EVENT_STORE: path.join(dir, 'events.json')},
    stdio: 'ignore',
  });
  t.after(async () => {
    child.kill('SIGTERM');
    await new Promise((resolve) => child.once('exit', resolve));
    await rm(dir, {recursive: true, force: true});
  });

  const page = await waitUntilReady(`${base}/`, child);
  assert.match(await page.text(), /data-endpoint="\/api\/events"/);

  const source = await readFile(path.join(repo, 'data/p2/events.json'), 'utf8');
  const contract = JSON.parse(source);
  const samples = {
    page_view: {event: 'page_view', path: '/index.html'},
    outbound_click: {event: 'outbound_click', path: '/index.html', asin: 'B0CDY277D3'},
    guide_read_75: {event: 'guide_read_75', path: '/guide-capacity.html'},
    category_click: {event: 'category_click', path: '/index.html', target: 'dual-basket'},
    feed_click: {event: 'feed_click', path: '/index.html'},
  };
  assert.deepEqual(new Set(Object.keys(samples)), new Set(contract.endpoint_contract.accepted_events));

  for (const [name, body] of Object.entries(samples)) {
    const response = await fetch(`${base}/api/events`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify(body),
    });
    assert.equal(response.status, 204, `${name} accepted`);
  }
  const repeated = await fetch(`${base}/api/events`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(samples.page_view),
  });
  assert.equal(repeated.status, 204);

  const store = JSON.parse(await readFile(path.join(dir, 'events.json'), 'utf8'));

  // The store is {event: {YYYY-MM-DD: {dimension: count}}} — daily counts per
  // event and path, exactly as data/p2/events.json declares.
  const total = (event, dimension) => Object.values(store[event] || {}).reduce(
    (sum, day) => sum + (Number(day[dimension]) || 0), 0);
  assert.equal(total('page_view', '/index.html'), 2);
  assert.equal(total('outbound_click', 'B0CDY277D3'), 1);
  assert.equal(total('guide_read_75', '/guide-capacity.html'), 1);
  assert.equal(total('category_click', '/index.html|dual-basket'), 1);
  assert.equal(total('feed_click', '/index.html'), 1);
  for (const event of Object.keys(store)) {
    assert.ok(contract.endpoint_contract.accepted_events.includes(event),
      `${event} is a declared event`);
    for (const day of Object.keys(store[event])) {
      assert.match(day, /^\d{4}-\d{2}-\d{2}$/, `${event} bucket is a dated day`);
    }
  }

  // No visitor record of any kind may reach the store.
  const keys = [];
  (function collect(node) {
    for (const [key, value] of Object.entries(node)) {
      keys.push(key);
      if (value && typeof value === 'object') collect(value);
    }
  })(store);
  for (const key of keys) {
    assert.doesNotMatch(key, /user|ip|agent|referer|referrer|cookie|session|ident|token/i,
      `store key ${key} carries no visitor field`);
  }

  const badEvent = await fetch(`${base}/api/events`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({event: 'session', path: '/index.html'}),
  });
  assert.equal(badEvent.status, 400);

  // The superseded twelve-event family must never be accepted by the endpoint.
  const legacyEvents = ['guide_open', 'category_open', 'rss_feed_click', 'chooser_completed',
    'article_half_read', 'disclosure_viewed', 'cta_click', 'product_click', 'filter_apply',
    'guide_read'];
  for (const event of legacyEvents) {
    const response = await fetch(`${base}/api/events`, {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({event, path: '/index.html'}),
    });
    assert.equal(response.status, 400, `${event} rejected`);
  }

  const badAsin = await fetch(`${base}/api/events`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({event: 'outbound_click', path: '/', asin: 'P01'}),
  });
  assert.equal(badAsin.status, 400);
  const crossOrigin = await fetch(`${base}/api/events`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json', Origin: 'https://elsewhere.example'},
    body: JSON.stringify(samples.page_view),
  });
  assert.equal(crossOrigin.status, 403);
  assert.equal(await (await fetch(`${base}/api/events`, {method: 'GET'})).status, 405);

  // The endpoint serves the generated publication in docs/, never the preserved
  // legacy tree in site/ and never a path outside the served root.
  assert.equal((await fetch(`${base}/shop.html`)).status, 200);
  assert.equal((await fetch(`${base}/research-desk.html`)).status, 404);
  // fetch() normalises ".." away before it reaches the server, so probe the
  // traversal guard with a raw request that keeps the path intact.
  // "/../server.mjs" is collapsed to "/server.mjs" by URL parsing and is not in
  // docs/; the percent-encoded form survives that step and must hit the guard.
  assert.equal(await rawStatus(port, 'GET', '/../server.mjs'), 404);
  assert.equal(await rawStatus(port, 'GET', '/..%2fserver.mjs'), 403);
  assert.equal(await rawStatus(port, 'GET', '/..%2f..%2fserver.mjs'), 403);
});
