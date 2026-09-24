// Hypothesis: the real input is type="checkbox" (replaced widget, intrinsic size),
// and WebKit does not stretch it from the inset shorthand alone — while a text
// input does stretch. Old code passed because it set explicit anchor-size width/height.
const {chromium, webkit} = require('playwright');

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .label { display:inline-flex; align-items:center; gap:8px; font:14px system-ui; }
  .mark { width:18px; height:18px; background:#333; display:inline-block; }
  .wrap { margin:20px; }
</style></head><body>
<div id="out">PENDING</div>
<div class="wrap"><label class="label" id="hA"><span class="vh"><input type="checkbox" id="iA"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hB"><span class="vh"><input type="checkbox" id="iB"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hC"><span class="vh"><input type="checkbox" id="iC"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hD"><span class="vh"><input type="checkbox" id="iD"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hE"><span class="vh"><input type="text" id="iE"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hF"><span class="vh"><input type="radio" id="iF"></span><span class="mark"></span>Test</label></div>
<div class="wrap"><label class="label" id="hG"><span class="vh"><input type="checkbox" id="iG"></span><span class="mark"></span>Test</label></div>

<script>
function g(id){let r=document.getElementById(id).getBoundingClientRect();
  return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)};}
function cs(id,p){return getComputedStyle(document.getElementById(id)).getPropertyValue(p).trim();}
function setup(hostId,inputId,decl,label){
  let host=document.getElementById(hostId), input=document.getElementById(inputId);
  let name='--n-'+hostId;
  host.style.anchorName=name;
  Object.assign(input.style, {position:'fixed', margin:'0', positionAnchor:name}, decl);
  let hr=g(hostId), ir=g(inputId);
  return {
    case:label,
    type:input.getAttribute('type'),
    usedW:cs(inputId,'width'), usedH:cs(inputId,'height'),
    host:[hr.w,hr.h], input:[ir.w,ir.h],
    covers: ir.w>=hr.w-1 && ir.h>=hr.h-1,
    exact: Math.abs(ir.w-hr.w)<=1 && Math.abs(ir.h-hr.h)<=1
  };
}
window.__probe=()=>{
  const SH='anchor(top) anchor(right) anchor(bottom) anchor(left)';
  let r={caps:{anchorName:CSS.supports('anchor-name: --t')}};
  r.A=setup('hA','iA',{inset:SH},'checkbox + inset only (NEW code)');
  r.B=setup('hB','iB',{inset:SH, width:'anchor-size(width)', height:'anchor-size(height)'},'checkbox + inset + anchor-size');
  r.C=setup('hC','iC',{inset:SH, width:'anchor-size(width)', height:'anchor-size(height)', boxSizing:'border-box'},'checkbox + inset + anchor-size + border-box');
  r.D=setup('hD','iD',{top:'anchor(top)', left:'anchor(left)', width:'anchor-size(width)', height:'anchor-size(height)'},'checkbox + longhands (OLD code)');
  r.E=setup('hE','iE',{inset:SH},'TEXT input + inset only (control)');
  r.F=setup('hF','iF',{inset:SH},'RADIO + inset only');
  r.G=setup('hG','iG',{inset:SH, appearance:'none'},'checkbox + inset + appearance:none');
  return r;
};
</script></body></html>`;

(async () => {
  const which = process.argv[2] || 'webkit';
  const browser = await {chromium, webkit}[which].launch({headless: true});
  const page = await browser.newPage({viewport: {width: 1280, height: 720}});
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForTimeout(500);
  const res = await page.evaluate(() => window.__probe());
  console.log('#### ' + which);
  for (const k of ['A','B','C','D','E','F','G']) {
    const r = res[k];
    console.log(`${r.case.padEnd(46)} covers=${String(r.covers).padEnd(5)} exact=${String(r.exact).padEnd(5)} host=${JSON.stringify(r.host)} input=${JSON.stringify(r.input)} usedW=${r.usedW}`);
  }
  await browser.close();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
