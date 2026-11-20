import {createServer} from 'node:http';
import {readFile, writeFile, mkdir, rename, readdir} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
// The deployed publication is generated to docs/ by tools/build.py. The preserved
// site/ tree is a separate legacy build and is not the publication this server serves.
const SITE = path.join(ROOT, 'docs');
const DATA = path.join(ROOT, 'data', 'p2');
const STORE = path.resolve(process.env.EVENT_STORE || path.join(ROOT, 'var', 'events-aggregate.json'));
const PORT = Number(process.env.PORT || 4173);
const MIME = {
  '.css': 'text/css; charset=utf-8',
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain; charset=utf-8',
  '.xml': 'application/xml; charset=utf-8',
};

const settings = JSON.parse(await readFile(path.join(DATA, 'settings.json'), 'utf8'));
const eventContract = JSON.parse(await readFile(path.join(DATA, 'events.json'), 'utf8'));
const productsData = JSON.parse(await readFile(path.join(DATA, 'products.json'), 'utf8'));
const PUBLIC_BASE = String(settings.base_url || '').replace(/\/$/, '');
const EVENTS = new Set(eventContract.events.map((event) => event.name));
// Literal accepted list, cross-checked against the declared contract below. The
// gate (tools/checks.py, measurement section) reads this set, and it must stay
// identical to the events the site's measure.js sends (F-P23 was the drift).
const ACCEPTED_EVENTS = new Set([
  'page_view',
  'outbound_click',
  'guide_read_75',
  'category_click',
  'feed_click',
]);
const PRODUCT_ASINS = new Set(productsData.products.map((product) => product.asin));
const CATEGORIES = new Set(['dual-basket', 'toaster-oven', 'single-basket', 'thermometers']);
const HTML_PAGES = new Set((await readdir(SITE)).filter((name) => name.endsWith('.html')));

if (EVENTS.size !== 5 || eventContract.endpoint_contract.accepted_events.length !== 5 ||
    eventContract.endpoint_contract.accepted_events.some((name) => !EVENTS.has(name))) {
  throw new Error('The local analytics endpoint contract must match exactly five declared events.');
}
if (EVENTS.size !== ACCEPTED_EVENTS.size ||
    [...ACCEPTED_EVENTS].some((name) => !EVENTS.has(name))) {
  throw new Error('ACCEPTED_EVENTS must equal the five events declared in data/p2/events.json (F-P23).');
}

let counts = {};
try {
  const stored = JSON.parse(await readFile(STORE, 'utf8'));
  if (stored && typeof stored === 'object' && !Array.isArray(stored)) counts = stored;
} catch (error) {
  if (error.code !== 'ENOENT') throw error;
}

let writeQueue = Promise.resolve();

// The store is {event: {YYYY-MM-DD: {dimension: count}}}: daily counts per event
// and path, exactly as data/p2/events.json declares. It holds no visitor record.
function today() {
  return new Date().toISOString().slice(0, 10);
}

function cleanPage(value) {
  if (typeof value !== 'string' || value.length > 256) return '/unknown';
  // Drop query strings and fragments before validating; neither is an analytics dimension.
  const pathname = value.split(/[?#]/, 1)[0] || '/';
  const page = pathname === '/' ? '/index.html' : pathname;
  if (!/^\/[A-Za-z0-9._/-]+$/.test(page) || page.includes('..')) return '/unknown';
  const filename = page.slice(1);
  return HTML_PAGES.has(filename) ? `/${filename}` : '/unknown';
}

function eventDimension(body) {
  const event = body?.event;
  if (typeof event !== 'string' || !EVENTS.has(event)) return null;
  const page = cleanPage(body.path);

  if (event === 'page_view' || event === 'guide_read_75' || event === 'feed_click') {
    return {event, dimension: page};
  }
  if (event === 'outbound_click') {
    if (typeof body.asin !== 'string' || !PRODUCT_ASINS.has(body.asin)) return null;
    return {event, dimension: body.asin};
  }
  if (event === 'category_click') {
    if (typeof body.target !== 'string' || !CATEGORIES.has(body.target)) return null;
    return {event, dimension: `${page}|${body.target}`};
  }
  return null;
}

async function record(key) {
  writeQueue = writeQueue.then(async () => {
    const day = today();
    const days = (counts[key.event] = counts[key.event] || {});
    const bucket = (days[day] = days[day] || {});
    bucket[key.dimension] = (Number(bucket[key.dimension]) || 0) + 1;
    await mkdir(path.dirname(STORE), {recursive: true, mode: 0o700});
    const temporary = `${STORE}.${process.pid}.tmp`;
    await writeFile(temporary, JSON.stringify(counts, null, 2), {mode: 0o600});
    await rename(temporary, STORE);
  });
  return writeQueue;
}

async function readBody(request) {
  const chunks = [];
  let size = 0;
  for await (const chunk of request) {
    size += chunk.length;
    if (size > 2048) throw new Error('payload too large');
    chunks.push(chunk);
  }
  return JSON.parse(Buffer.concat(chunks).toString('utf8'));
}

function selfHostedHtml(source) {
  let html = source;
  // The static Pages build keeps this empty. In this opt-in Node mode, enable
  // the same first-party tracker against this server's same-origin endpoint.
  html = html.replace(/data-endpoint=(['"]).*?\1/, 'data-endpoint="/api/events"');
  // Keep the local self-host run self-contained instead of loading its CSS and
  // measurement script from the public GitHub Pages origin.
  if (PUBLIC_BASE) {
    html = html.replaceAll(`href="${PUBLIC_BASE}/assets/`, 'href="/assets/');
    html = html.replaceAll(`src="${PUBLIC_BASE}/assets/`, 'src="/assets/');
    html = html.replaceAll(`href="${PUBLIC_BASE}/feed.xml"`, 'href="/feed.xml"');
    html = html.replaceAll(`href="${PUBLIC_BASE}/index.html"`, 'href="/index.html"');
  }
  return html;
}

async function handler(request, response) {
  const url = new URL(request.url, 'http://localhost');
  if (url.pathname === '/api/events') {
    if (request.method !== 'POST') {
      response.writeHead(405, {Allow: 'POST', 'Cache-Control': 'no-store'}).end();
      return;
    }

    const origin = request.headers.origin;
    if (origin) {
      try {
        if (new URL(origin).host !== request.headers.host) {
          response.writeHead(403, {'Cache-Control': 'no-store'}).end();
          return;
        }
      } catch {
        response.writeHead(403, {'Cache-Control': 'no-store'}).end();
        return;
      }
    }

    const contentType = request.headers['content-type'] || '';
    if (!contentType.startsWith('application/json') && !contentType.startsWith('text/plain')) {
      response.writeHead(415, {'Cache-Control': 'no-store'}).end();
      return;
    }

    try {
      const body = await readBody(request);
      const key = eventDimension(body);
      if (!key) {
        response.writeHead(400, {'Cache-Control': 'no-store'}).end();
        return;
      }
      await record(key);
      response.writeHead(204, {
        'Cache-Control': 'no-store',
        'Referrer-Policy': 'no-referrer',
      }).end();
    } catch {
      response.writeHead(400, {'Cache-Control': 'no-store'}).end();
    }
    return;
  }

  if (request.method !== 'GET' && request.method !== 'HEAD') {
    response.writeHead(405, {Allow: 'GET, HEAD'}).end();
    return;
  }

  let pathname;
  try {
    pathname = decodeURIComponent(url.pathname);
  } catch {
    response.writeHead(400).end();
    return;
  }
  if (pathname.split('/').includes('..')) {
    response.writeHead(403).end();
    return;
  }
  if (pathname === '/') pathname = '/index.html';
  if (pathname.endsWith('/')) pathname += 'index.html';

  const target = path.resolve(SITE, `.${pathname}`);
  if (!target.startsWith(`${SITE}${path.sep}`)) {
    response.writeHead(403).end();
    return;
  }

  try {
    let content = await readFile(target);
    if (path.extname(target) === '.html') {
      content = Buffer.from(selfHostedHtml(content.toString('utf8')));
    }
    response.writeHead(200, {
      'Content-Type': MIME[path.extname(target)] || 'application/octet-stream',
      'Cache-Control': path.extname(target) === '.html' ? 'no-store' : 'public, max-age=300',
      'X-Content-Type-Options': 'nosniff',
      'Referrer-Policy': 'strict-origin-when-cross-origin',
    });
    if (request.method === 'HEAD') response.end();
    else response.end(content);
  } catch {
    response.writeHead(404, {'Content-Type': 'text/plain; charset=utf-8'}).end('Not found');
  }
}

createServer(handler).listen(PORT, '0.0.0.0', () => {
  // The application deliberately does not log request metadata or event values.
  console.log(`Prod2 self-host mode listening on 0.0.0.0:${PORT}; aggregate store: ${STORE}`);
});
