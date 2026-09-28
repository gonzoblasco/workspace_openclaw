// Isolates which of the two changes breaks anchoring:
//   (a) longhands (top/left + anchor-size) vs inset shorthand
//   (b) literal anchor name vs var() with fallback
// Run in whatever browser binary is passed via argv.
const {chromium, webkit, firefox} = require('playwright');

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .host { position:relative; width:200px; height:44px; background:#ddd; margin:12px; }
</style></head><body>
<div id="out">PENDING</div>
<div class="host" id="hA"><span class="vh"><input id="iA"></span></div>
<div class="host" id="hB"><span class="vh"><input id="iB"></span></div>
<div class="host" id="hC"><span class="vh"><input id="iC"></span></div>
<div class="host" id="hD"><span class="vh"><input id="iD"></span></div>
<div class="host" id="hE"><span class="vh"><input id="iE"></span></div>

<script>
function g(id){let r=document.getElementById(id).getBoundingClientRect();
  return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)};}
function cs(id,p){return getComputedStyle(document.getElementById(id)).getPropertyValue(p).trim();}
function run(hostId,inputId,opts){
  let host=document.getElementById(hostId), input=document.getElementById(inputId);
  let name=opts.name, useVar=opts.useVar, shorthand=opts.shorthand;
  if(useVar){
    host.style.anchorName='var('+opts.varName+', '+name+')';
    input.style.positionAnchor='var('+opts.varName+', '+name+')';
  } else {
    host.style.anchorName=name;
    input.style.positionAnchor=name;
  }
  input.style.position='fixed';
  input.style.margin='0';
  if(shorthand){ input.style.inset='anchor(top) anchor(right) anchor(bottom) anchor(left)'; }
  else {
    input.style.top='anchor(top)'; input.style.left='anchor(left)';
    input.style.width='anchor-size(width)'; input.style.height='anchor-size(height)';
  }
  let hr=g(hostId), ir=g(inputId);
  return {
    case:opts.label,
    computedAnchorName: cs(hostId,'anchor-name'),
    computedPositionAnchor: cs(inputId,'position-anchor'),
    usedInset: cs(inputId,'inset'),
    usedWidth: cs(inputId,'width'),
    host:{w:hr.w,h:hr.h}, input:{x:ir.x,w:ir.w,h:ir.h},
    covers: Math.abs(ir.x-hr.x)<=1 && ir.w>=hr.w-1 && ir.h>=hr.h-1,
    exactSize: Math.abs(ir.w-hr.w)<=1 && Math.abs(ir.h-hr.h)<=1
  };
}
window.__probe = () => {
  let res={caps:{
    anchorName: CSS.supports('anchor-name: --t'),
    positionAnchor: CSS.supports('position-anchor: --t'),
    anchorFn: CSS.supports('top: anchor(top)'),
    anchorSize: CSS.supports('width: anchor-size(width)'),
    insetAnchor: CSS.supports('inset: anchor(top) anchor(right) anchor(bottom) anchor(left)')
  }};
  res.A='A-literal-name+longhands';
  res.A=run('hA','iA',{label:'literal + longhands', name:'--lit-a', useVar:false, shorthand:false});
  res.B=run('hB','iB',{label:'literal + inset shorthand', name:'--lit-b', useVar:false, shorthand:true});
  res.C=run('hC','iC',{label:'var() + longhands', name:'--lit-c', useVar:true, varName:'--my-var', shorthand:false});
  res.D=run('hD','iD',{label:'var() + inset shorthand', name:'--lit-d', useVar:true, varName:'--my-var', shorthand:true});
  res.E=run('hE','iE',{label:'var() declared on host only, input reads var too', name:'--lit-e', useVar:true, varName:'--my-var', shorthand:true});
  return res;
};
</script></body></html>`;

(async () => {
  const which = process.argv[2] || 'webkit';
  const map = {chromium, webkit, firefox};
  const launcher = map[which];
  const browser = await launcher.launch({headless: true});
  const page = await browser.newPage({viewport: {width: 900, height: 800}});
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForTimeout(300);
  const res = await page.evaluate(() => window.__probe());
  res.consoleErrors = errors;
  console.log('#### browser:', which);
  console.log(JSON.stringify(res, null, 2));
  await browser.close();
})().catch(e => { console.error('FAILED', process.argv[2] || 'webkit', e.message); process.exit(1); });
