// Replicates the REAL component geometry: host is a static label with natural size,
// inside a wrapper, with the input nested in a VisuallyHidden-like span.
// Varies exactly the two code deltas: name literal vs var(), longhands vs inset,
// and host position static vs relative.
const {chromium, webkit, firefox} = require('playwright');

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  /* label-like host: inline-flex with natural size, no explicit size */
  .label { display:inline-flex; align-items:center; gap:8px; font:14px system-ui; }
  .mark { width:18px; height:18px; background:#333; display:inline-block; }
  .wrap { margin:20px; }
</style></head><body>
<div id="out">PENDING</div>
<div class="wrap" id="wrapA"><label class="label" id="hA"><span class="vh"><input id="iA"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapB"><label class="label" id="hB"><span class="vh"><input id="iB"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapC"><label class="label" id="hC"><span class="vh"><input id="iC"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapD"><label class="label" id="hD"><span class="vh"><input id="iD"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapE"><label class="label" id="hE"><span class="vh"><input id="iE"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapF"><label class="label" id="hF"><span class="vh"><input id="iF"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapG"><label class="label" id="hG"><span class="vh"><input id="iG"></span><span class="mark"></span>Test</label></div>
<div class="wrap" id="wrapH"><label class="label" id="hH"><span class="vh"><input id="iH"></span><span class="mark"></span>Test</label></div>

<script>
function g(id){let r=document.getElementById(id).getBoundingClientRect();
  return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)};}
function cs(id,p){return getComputedStyle(document.getElementById(id)).getPropertyValue(p).trim();}
function setup(hostId,inputId,opts){
  let host=document.getElementById(hostId), input=document.getElementById(inputId);
  let name='--n-'+(++window.__uid||(window.__uid=0));
  let useVar=opts.useVar, inset=opts.inset, hostPos=opts.hostPos;
  if(hostPos==='relative') host.style.position='relative';
  if(useVar){
    let v='--rac-anchor-'+hostId;
    host.style.anchorName='var('+v+', '+name+')';
    input.style.positionAnchor='var('+v+', '+name+')';
  } else {
    host.style.anchorName=name;
    input.style.positionAnchor=name;
  }
  input.style.position='fixed';
  input.style.margin='0';
  if(inset){ input.style.inset='anchor(top) anchor(right) anchor(bottom) anchor(left)'; }
  else {
    input.style.top='anchor(top)'; input.style.left='anchor(left)';
    input.style.width='anchor-size(width)'; input.style.height='anchor-size(height)';
  }
  let hr=g(hostId), ir=g(inputId);
  return {
    case:opts.label,
    hostPos,
    computedAnchorName:cs(hostId,'anchor-name'),
    computedPositionAnchor:cs(inputId,'position-anchor'),
    usedWidth:cs(inputId,'width'),
    usedInset:cs(inputId,'inset'),
    host:[hr.w,hr.h], input:[ir.w,ir.h],
    inputXY:[ir.x,ir.y], hostXY:[hr.x,hr.y],
    covers: ir.w>=hr.w-1 && ir.h>=hr.h-1 && Math.abs(ir.x-hr.x)<=1 && Math.abs(ir.y-hr.y)<=1
  };
}
window.__uid=0;
window.__probe=()=>{
  let res={caps:{anchorName:CSS.supports('anchor-name: --t')}};
  res.A=setup('hA','iA',{label:'static host, literal name, longhands', useVar:false, inset:false, hostPos:'static'});
  res.B=setup('hB','iB',{label:'static host, var() name, longhands', useVar:true, inset:false, hostPos:'static'});
  res.C=setup('hC','iC',{label:'static host, literal name, inset', useVar:false, inset:true, hostPos:'static'});
  res.D=setup('hD','iD',{label:'static host, var() name, inset', useVar:true, inset:true, hostPos:'static'});
  res.E=setup('hE','iE',{label:'relative host, literal name, longhands', useVar:false, inset:false, hostPos:'relative'});
  res.F=setup('hF','iF',{label:'relative host, var() name, longhands', useVar:true, inset:false, hostPos:'relative'});
  res.G=setup('hG','iG',{label:'relative host, literal name, inset', useVar:false, inset:true, hostPos:'relative'});
  res.H=setup('hH','iH',{label:'relative host, var() name, inset', useVar:true, inset:true, hostPos:'relative'});
  return res;
};
</script></body></html>`;

(async () => {
  const which = process.argv[2] || 'webkit';
  const map = {chromium, webkit, firefox};
  const browser = await map[which].launch({headless: true});
  const page = await browser.newPage({viewport: {width: 1280, height: 720}});
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForTimeout(500);
  const res = await page.evaluate(() => window.__probe());
  console.log('#### ' + which);
  for (const k of ['A','B','C','D','E','F','G','H']) {
    const r = res[k];
    if (!r) continue;
    console.log(`${r.case.padEnd(48)} covers=${String(r.covers).padEnd(5)} host=${JSON.stringify(r.host)} input=${JSON.stringify(r.input)}`);
  }
  console.log('caps:', JSON.stringify(res.caps));
  await browser.close();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
