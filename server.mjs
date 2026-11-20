import {createServer} from 'node:http';
import {readFile, writeFile, mkdir, rename} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT = path.dirname(fileURLToPath(import.meta.url));
const SITE = path.join(ROOT, 'site'); // INT-06: canonical site is site/ (Countercraft); docs/ archived
const STORE = path.resolve(process.env.EVENT_STORE || path.join(ROOT, 'var', 'events-aggregate.json'));
const PORT = Number(process.env.PORT || 4173);
const allowedEvents = new Set(['page_view', 'outbound_click', 'guide_open', 'category_open', 'rss_feed_click', 'chooser_completed', 'article_half_read', 'disclosure_viewed', 'cta_click', 'product_click', 'filter_apply', 'guide_read']);
const products = new Set(['P01', 'P02', 'P03', 'P04', 'P05']);
const guides = new Set(['basket-or-oven', 'capacity-checklist', 'cleanup-and-space', 'questions-before-buying']);
const categories = new Set(['air-fryers', 'meat-thermometers']);
const mime = {'.html':'text/html; charset=utf-8','.css':'text/css; charset=utf-8','.js':'text/javascript; charset=utf-8','.xml':'application/xml; charset=utf-8','.txt':'text/plain; charset=utf-8','.png':'image/png','.svg':'image/svg+xml'};
let counts = {};
try { counts = JSON.parse(await readFile(STORE, 'utf8')); } catch (error) { if (error.code !== 'ENOENT') throw error; }
let writeQueue = Promise.resolve();

function cleanPage(value) {
  return typeof value === 'string' && /^\/[a-zA-Z0-9/_\-.]*$/.test(value) && !value.includes('..') ? value.slice(0, 160) : '/unknown';
}
function keyFor(body) {
  // The existing static click tracker names the event in `event`; this endpoint
  // also accepts `type` for simple self-hosted probes. Timestamps and extra keys
  // are deliberately ignored and never written to disk.
  const event = body?.type || body?.event;
  if (!allowedEvents.has(event)) return null;
  if (event === 'page_view') return `${event}|${cleanPage(body.page)}`;
  if (event === 'outbound_click') return `${event}|${products.has(body.product) ? body.product : 'unknown'}`;
  if (event === 'guide_open') return `${event}|${guides.has(body.guide) ? body.guide : 'unknown'}`;
  if (event === 'category_open') return `${event}|${categories.has(body.category) ? body.category : 'unknown'}`;
  if (event === 'chooser_completed') return `${event}|${products.has(body.recommendation) ? body.recommendation : 'unknown'}`;
  if (event === 'article_half_read') return `${event}|${body.depth === 100 ? 100 : 50}`;
  if (event === 'disclosure_viewed') return `${event}|disclosure`;
  if (event === 'product_click') return `${event}|${body.asin && /^[A-Z0-9]{10}$/.test(String(body.asin)) ? body.asin : 'unknown'}`;
  if (event === 'cta_click') return `${event}|cta`;
  if (event === 'filter_apply') return `${event}|filter`;
  if (event === 'guide_read') return `${event}|guide`;
  return `${event}|feed`;
}
async function record(key) {
  writeQueue = writeQueue.then(async () => {
    counts[key] = (Number(counts[key]) || 0) + 1;
    await mkdir(path.dirname(STORE), {recursive:true, mode:0o700});
    const temp = `${STORE}.tmp`;
    await writeFile(temp, JSON.stringify(counts, null, 2), {mode:0o600});
    await rename(temp, STORE);
  });
  return writeQueue;
}
async function readBody(req) {
  const parts=[]; let size=0;
  for await (const part of req) {
    size += part.length;
    if (size > 2048) throw new Error('payload too large');
    parts.push(part);
  }
  return JSON.parse(Buffer.concat(parts).toString('utf8'));
}
async function handler(req, res) {
  const pathname = new URL(req.url, 'http://localhost').pathname;
  if (pathname === '/api/events' && req.method === 'POST') {
    const origin=req.headers.origin;
    if (origin) {
      try { if (new URL(origin).host !== req.headers.host) { res.writeHead(403, {'Cache-Control':'no-store'}).end(); return; } }
      catch { res.writeHead(403, {'Cache-Control':'no-store'}).end(); return; }
    }
    const contentType=req.headers['content-type'] || '';
    if (!contentType.startsWith('application/json') && !contentType.startsWith('text/plain')) { res.writeHead(415, {'Cache-Control':'no-store'}).end(); return; }
    try {
      const body = await readBody(req);
      const key = keyFor(body);
      if (!key) { res.writeHead(400, {'Cache-Control':'no-store'}).end(); return; }
      await record(key);
      res.writeHead(204, {'Cache-Control':'no-store'}).end();
    } catch (_) { res.writeHead(400, {'Cache-Control':'no-store'}).end(); }
    return;
  }
  if (pathname === '/api/client.js' && (req.method === 'GET' || req.method === 'HEAD')) {
    const script = await readFile(path.join(ROOT,'analytics-client.js'));
    res.writeHead(200, {'Content-Type':'text/javascript; charset=utf-8','Cache-Control':'no-store','X-Content-Type-Options':'nosniff'});
    if (req.method === 'HEAD') res.end(); else res.end(script);
    return;
  }
  if (req.method !== 'GET' && req.method !== 'HEAD') { res.writeHead(405, {'Allow':'GET, HEAD'}).end(); return; }
  let relative;
  try { relative = decodeURIComponent(pathname); } catch (_) { res.writeHead(400).end(); return; }
  if (relative === '/') relative='/index.html';
  if (relative.endsWith('/')) relative += 'index.html';
  const target=path.resolve(SITE, `.${relative}`);
  if (!target.startsWith(`${SITE}${path.sep}`) && target !== path.join(SITE,'index.html')) { res.writeHead(403).end(); return; }
  try {
    let content=await readFile(target);
    if (path.extname(target)==='.html') {
      let html=content.toString('utf8');
      // INT-06: canonical site (Countercraft) opts in via window.COUNTERCRAFT_ENDPOINT;
      // legacy Counter Notes pages opted in via the body attribute. Support both.
      html=html.replace('data-analytics-endpoint=""','data-analytics-endpoint="/api/events"');
      /* 2026-11-20 chrome: tools/build.py emits the endpoint on <html data-endpoint=""> */
      html=html.replace('data-endpoint=""','data-endpoint="/api/events"');
      html=html.replace('</head>','<script>window.COUNTERCRAFT_ENDPOINT="/api/events";</script></head>');
      html=html.replace('</body>','<script src="/api/client.js" defer></script></body>');
      content=Buffer.from(html);
    }
    res.writeHead(200, {'Content-Type':mime[path.extname(target)]||'application/octet-stream','X-Content-Type-Options':'nosniff','Referrer-Policy':'strict-origin-when-cross-origin'});
    if (req.method==='HEAD') res.end(); else res.end(content);
  } catch (_) { res.writeHead(404, {'Content-Type':'text/plain; charset=utf-8'}).end('Not found'); }
}
createServer(handler).listen(PORT,'0.0.0.0',()=>{
  // Deliberately do not log request metadata (including client IP addresses).
  console.log(`Counter Notes self-host mode listening on 0.0.0.0:${PORT}; aggregate store: ${STORE}`);
});
