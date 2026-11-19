/* Injected only by server.mjs self-host mode; GitHub Pages never loads this script. */
(() => {
  const endpoint=document.body?.dataset.analyticsEndpoint;
  if(!endpoint) return;
  const send=(type,detail={})=>{
    const payload=JSON.stringify({type,page:location.pathname,...detail});
    try {
      if(navigator.sendBeacon) navigator.sendBeacon(endpoint,new Blob([payload],{type:'application/json'}));
      else fetch(endpoint,{method:'POST',headers:{'Content-Type':'application/json'},body:payload,keepalive:true}).catch(()=>{});
    } catch (_) { /* analytics must never block navigation */ }
  };
  send('page_view');
  document.addEventListener('click',(event)=>{
    const link=event.target?.closest?.('a[href]');
    if(!link || link.hasAttribute('data-outbound')) return; // existing tracker handles product clicks
    let path;
    try { path=new URL(link.href,location.href).pathname; } catch (_) { return; }
    const guide=path.match(/\/guides\/([a-z0-9-]+)\.html$/);
    const guideSlugs=['basket-or-oven','capacity-checklist','cleanup-and-space','questions-before-buying'];
    if(guide && guideSlugs.includes(guide[1])) { send('guide_open',{guide:guide[1]}); return; }
    if(path.endsWith('/air-fryers.html')) { send('category_open',{category:'air-fryers'}); return; }
    if(path.endsWith('/meat-thermometers.html')) { send('category_open',{category:'meat-thermometers'}); return; }
    if(path.endsWith('/feed.xml')) send('rss_feed_click');
  },true);
})();
