(async()=>{
  const joined=(window.__BETA_PARTS||[]).join('');
  const bytes=Uint8Array.from(atob(joined),c=>c.charCodeAt(0));
  if(typeof DecompressionStream==='undefined'){
    document.body.innerHTML='<div style="padding:24px;color:#eee;background:#111;font-family:system-ui">当前浏览器过旧，无法启动内测版。请使用最新版 Chrome、Safari、Edge 或 Firefox。</div>';
    return;
  }
  const stream=new Blob([bytes]).stream().pipeThrough(new DecompressionStream('gzip'));
  const payload=JSON.parse(await new Response(stream).text());
  window.__ASSETS=payload.assets;
  const style=document.createElement('style');style.textContent=payload.css;document.head.appendChild(style);
  const script=document.createElement('script');script.textContent=payload.bundle;document.body.appendChild(script);
  window.__BETA_PARTS.length=0;
})().catch(err=>{
  console.error(err);
  document.body.innerHTML='<div style="padding:24px;color:#eee;background:#111;font-family:system-ui">内测资源加载失败，请刷新页面重试。</div>';
});
