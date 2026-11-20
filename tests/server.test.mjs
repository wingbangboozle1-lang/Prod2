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

test('the publication client and this endpoint agree on every event name (F-P23 regression)',async(t)=>{
  // The defect this guards: assets/js/measure.js shipped five event names, three
  // of which this endpoint answered 400 to, so two thirds of the site's
  // measurement was lost without any error a reader could see. The event list is
  // read out of measure.js itself, so the two files cannot drift apart again
  // without this test failing.
  const client = await readFile(path.join(ROOT,'assets','js','measure.js'),'utf8');
  const match = client.match(/var EVENTS = \[([^\]]+)\]/);
  assert.ok(match,'measure.js must declare its EVENTS array');
  const events=[...match[1].matchAll(/["']([a-z0-9_]+)["']/g)].map(m=>m[1]);
  assert.equal(events.length,5,'the site publishes exactly five events (data/p2/events.json)');
  const port=await freePort();
  const store=path.join(ROOT,'var','test-events-vocab.json');
  await rm(store,{force:true});
  const child=spawn(process.execPath,['server.mjs'],{cwd:ROOT,env:{...process.env,PORT:String(port),EVENT_STORE:store},stdio:['ignore','pipe','pipe']});
  let logs='';child.stdout.on('data',x=>logs+=x.toString());child.stderr.on('data',x=>logs+=x.toString());
  t.after(async()=>{child.kill('SIGTERM');await new Promise(resolve=>child.once('exit',resolve));await rm(store,{force:true});});
  let ready=false;
  for(let n=0;n<60;n++){try{const r=await fetch(`http://127.0.0.1:${port}/`);if(r.ok){ready=true;break;}}catch{}await new Promise(resolve=>setTimeout(resolve,50));}
  assert.ok(ready,`server did not start: ${logs}`);
  // Payload shapes copied from measure.js record() calls.
  const shapes={
    page_view:{path:'/guide-capacity.html'},
    outbound_click:{asin:'B0CDY277D3',target:'www.amazon.com'},
    guide_read_75:{path:'/guide-capacity.html'},
    category_click:{target:'air-fryers'},
    feed_click:{}
  };
  for(const event of events){
    assert.ok(shapes[event],`test needs a sample payload for ${event}`);
    const r=await fetch(`http://127.0.0.1:${port}/api/events`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({event,path:'/shop.html',...shapes[event]})});
    assert.equal(r.status,204,`endpoint must accept the site's own event "${event}"`);
  }
  const stored=await readFile(store,'utf8');
  const counts=JSON.parse(stored);
  assert.equal(counts['page_view|/guide-capacity.html'],1,'page_view must key off path, not collapse to /unknown');
  assert.equal(counts['outbound_click|B0CDY277D3'],1,'outbound_click must keep the ASIN valid');
  assert.equal(counts['guide_read_75|/guide-capacity.html'],1);
  assert.equal(counts['category_click|air-fryers'],1);
  assert.equal(counts['feed_click|feed'],1);
  assert.equal(Object.keys(counts).length,5,'five distinct keys, no /unknown bucket');
  assert.equal(stored.includes('www.amazon.com'),false,'the target host must not be stored');
});
