import test from 'node:test';
import assert from 'node:assert/strict';
import {spawn} from 'node:child_process';
import {once} from 'node:events';
import {createServer} from 'node:net';
import {readFile, rm} from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const ROOT=path.dirname(path.dirname(fileURLToPath(import.meta.url)));
async function freePort(){const server=createServer();server.listen(0,'127.0.0.1');await once(server,'listening');const port=server.address().port;await new Promise(resolve=>server.close(resolve));return port;}

test('self-host mode injects the endpoint config and first-party client, and aggregates the allow-listed event types',async(t)=>{
  const port=await freePort();
  const store=path.join(ROOT,'var','test-events.json');
  await rm(store,{force:true});
  const child=spawn(process.execPath,['server.mjs'],{cwd:ROOT,env:{...process.env,PORT:String(port),EVENT_STORE:store},stdio:['ignore','pipe','pipe']});
  let logs='';child.stdout.on('data',x=>logs+=x.toString());child.stderr.on('data',x=>logs+=x.toString());
  t.after(async()=>{child.kill('SIGTERM');await new Promise(resolve=>child.once('exit',resolve));await rm(store,{force:true});});
  let ready=false;
  for(let n=0;n<60;n++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,50));}
  assert.ok(ready,`server did not start: ${logs}`);
  const page=await fetch(`http://127.0.0.1:${port}/`);assert.equal(page.status,200);
  const html=await page.text();assert.match(html,/Countercraft/);assert.match(html,/COUNTERCRAFT_ENDPOINT="\/api\/events"/);assert.match(html,/api\/client\.js/);
  const client=await fetch(`http://127.0.0.1:${port}/api/client.js`);assert.equal(client.status,200);assert.match(await client.text(),/rss_feed_click/);
  const fixtures=[
    {event:'page_view',page:'/products.html'},
    {event:'outbound_click',product:'P01',page:'/products.html',ts:'2026-11-19T00:00:00Z'},
    {event:'guide_open',guide:'basket-or-oven'},
    {event:'category_open',category:'air-fryers'},
    {event:'rss_feed_click'}
  ];
  for(const event of fixtures){const r=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'text/plain','user-agent':'test-agent'},body:JSON.stringify({...event,query:'must not be retained',email:'not-an-email@example.test',ip:'192.0.2.4'})});assert.equal(r.status,204);}
  const invalid=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({event:'conversion',order:'x'})});assert.equal(invalid.status,400);
  const crossSite=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json','origin':'https://untrusted.example'},body:JSON.stringify({event:'page_view',page:'/'})});assert.equal(crossSite.status,403);
  const stored=await readFile(store,'utf8');
  for(const secret of ['test-agent','192.0.2.4','must not be retained','not-an-email','2026-11-19T00:00:00Z','email','query','ip']) assert.equal(stored.includes(secret),false,`aggregate must omit ${secret}`);
  const counts=JSON.parse(stored);assert.equal(Object.keys(counts).length,5);assert.equal(counts['page_view|/products.html'],1);assert.equal(counts['outbound_click|P01'],1);assert.equal(counts['guide_open|basket-or-oven'],1);assert.equal(counts['category_open|air-fryers'],1);assert.equal(counts['rss_feed_click|feed'],1);
  const traversal=await fetch(`http://127.0.0.1:${port}/%2e%2e/server.mjs`);assert.notEqual(traversal.status,200);
});

test('endpoint aggregates the Countercraft event family safely',async(t)=>{
  const port=await freePort();
  const store=path.join(ROOT,'var','test-events-cc.json');
  await rm(store,{force:true});
  const child=spawn(process.execPath,['server.mjs'],{cwd:ROOT,env:{...process.env,PORT:String(port),EVENT_STORE:store},stdio:['ignore','pipe','pipe']});
  let logs='';child.stdout.on('data',x=>logs+=x.toString());child.stderr.on('data',x=>logs+=x.toString());
  t.after(async()=>{child.kill('SIGTERM');await new Promise(resolve=>child.once('exit',resolve));await rm(store,{force:true});});
  let ready=false;
  for(let n=0;n<60;n++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,50));}
  assert.ok(ready,`server did not start: ${logs}`);
  const fixtures=[
    {event:'product_click',asin:'B0CDY277D3',path:'/comparison.html'},
    {event:'product_click',asin:'NOT-AN-ASIN',path:'/comparison.html'},
    {event:'cta_click',label:'Air fryers'},
    {event:'filter_apply'},
    {event:'guide_read'},
    {event:'not_in_the_list',email:'nope@example.test'}
  ];
  let invalid;
  for(const event of fixtures){
    const r=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(event)});
    if(event.event==='not_in_the_list') invalid=r; else assert.equal(r.status,204);
  }
  assert.equal(invalid.status,400);
  const stored=await readFile(store,'utf8');
  for(const secret of ['email','nope@example.test','NOT-AN-ASIN','label','Air fryers']) assert.equal(stored.includes(secret),false,`aggregate must omit ${secret}`);
  const counts=JSON.parse(stored);
  assert.equal(counts['product_click|B0CDY277D3'],1);
  assert.equal(counts['product_click|unknown'],1);
  assert.equal(counts['cta_click|cta'],1);
  assert.equal(counts['filter_apply|filter'],1);
  assert.equal(counts['guide_read|guide'],1);
});

test('the shipped publication tracker emits exactly five events and every one is accepted',async(t)=>{
  // Regression guard: before 2026-11-20 three of the five shipped events
  // (guide_read_75, category_click, feed_click) were silently rejected (400) by
  // this endpoint, so their counts would have been lost without an error anyone saw.
  const port=await freePort();
  const store=path.join(ROOT,'var','test-events-shipped.json');
  await rm(store,{force:true});
  const child=spawn(process.execPath,['server.mjs'],{cwd:ROOT,env:{...process.env,PORT:String(port),EVENT_STORE:store},stdio:['ignore','pipe','pipe']});
  let logs='';child.stdout.on('data',x=>logs+=x.toString());child.stderr.on('data',x=>logs+=x.toString());
  t.after(async()=>{child.kill('SIGTERM');await new Promise(resolve=>child.once('exit',resolve));await rm(store,{force:true});});
  let ready=false;
  for(let n=0;n<60;n++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,50));}
  assert.ok(ready,`server did not start: ${logs}`);

  // read the event names straight out of the shipped tracker
  const tracker=await readFile(path.join(ROOT,'assets','js','measure.js'),'utf8');
  const m=tracker.match(/var EVENTS = \[([^\]]+)\]/);
  assert.ok(m,'measure.js has no EVENTS list');
  const shipped=[...m[1].matchAll(/"([a-z_0-9]+)"/g)].map(x=>x[1]);
  assert.deepEqual(shipped.sort(),['category_click','feed_click','guide_read_75','outbound_click','page_view']);

  // every shipped event must be stored, not silently rejected
  const bodies={
    page_view:{event:'page_view',path:'/index.html'},
    outbound_click:{event:'outbound_click',path:'/index.html',asin:'B0CDY277D3',target:'www.amazon.com'},
    guide_read_75:{event:'guide_read_75',path:'/guide-capacity.html'},
    category_click:{event:'category_click',path:'/index.html',target:'category-air-fryers.html#dual'},
    feed_click:{event:'feed_click',path:'/guides.html'},
  };
  for(const name of shipped){
    const r=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(bodies[name])});
    assert.equal(r.status,204,`${name} rejected by the endpoint (status ${r.status})`);
  }
  const counts=JSON.parse(await readFile(store,'utf8'));
  assert.equal(Object.keys(counts).length,5,'all five shipped events must each produce a stored key');
  assert.equal(counts['outbound_click|B0CDY277D3'],1);
  assert.equal(counts['guide_read_75|/guide-capacity.html'],1);
  assert.ok(Object.keys(counts).some(k=>k.startsWith('category_click|')&&k!=='category_click|/unknown'),'category_click must keep its target');
  assert.equal(counts['feed_click|/guides.html'],1);
  assert.equal(counts['page_view|/index.html'],1);
});

test('measure.js posts {event, path} and the endpoint keys on the real page, not /unknown',async(t)=>{
  // measure.js sends the page as `path`. Before this fix the endpoint read only
  // `page`, so every page view collapsed into a single "page_view|/unknown" row.
  const tracker=await readFile(path.join(ROOT,'assets','js','measure.js'),'utf8');
  assert.match(tracker,/path:\s*location\.pathname/,'measure.js must send the page path');

  const port=await freePort();
  const store=path.join(ROOT,'var','test-events-path.json');
  await rm(store,{force:true});
  const child=spawn(process.execPath,['server.mjs'],{cwd:ROOT,env:{...process.env,PORT:String(port),EVENT_STORE:store},stdio:['ignore','pipe','pipe']});
  let logs='';child.stdout.on('data',x=>logs+=x.toString());child.stderr.on('data',x=>logs+=x.toString());
  t.after(async()=>{child.kill('SIGTERM');await new Promise(resolve=>child.once('exit',resolve));await rm(store,{force:true});});
  let ready=false;
  for(let n=0;n<60;n++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,50));}
  assert.ok(ready,`server did not start: ${logs}`);
  for(const p of ['/index.html','/guide-capacity.html','/compare.html']){
    const r=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({event:'page_view',path:p})});
    assert.equal(r.status,204);
  }
  const counts=JSON.parse(await readFile(store,'utf8'));
  assert.equal(counts['page_view|/index.html'],1,'real path must be retained');
  assert.equal(counts['page_view|/guide-capacity.html'],1);
  assert.equal(counts['page_view|/compare.html'],1);
  assert.equal(counts['page_view|/unknown'],undefined,'page views must not collapse into /unknown');
});
