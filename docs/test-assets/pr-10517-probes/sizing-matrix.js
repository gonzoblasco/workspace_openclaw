// Sizing matrix: which declaration actually sizes the replaced <input> element.
// Structure mirrors the real component: static label host > VisuallyHidden wrapper > input.
const {chromium, webkit} = require('playwright');

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .host { width:200px; height:44px; background:#ddd; margin:12px; }
</style></head><body>
<div id="out">PENDING</div>
<div class="host" id="hA"><span class="vh"><input id="iA"></span></div>
<div class="host" id="hB"><span class="vh"><input id="iB"></span></div>
<div class="host" id="hC"><span class="vh"><input id="iC"></span></div>
<div class="host" id="hD"><span class="vh"><input id="iD"></span></div>
<div class="host" id="hE"><span class="vh"><input id="iE"></span></div>
<div class="host" id="hF"><span class="vh"><input id="iF"></span></div>
<div class="host" id="hG"><span class="vh"><input id="iG"></span></div>
<div class="host" id="hH"><span class="vh"><input id="iH"></span></div>

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
    usedWidth:cs(inputId,'width'), usedHeight:cs(inputId,'height'),
    usedInset:cs(inputId,'inset'), usedBoxSizing:cs(inputId,'box-sizing'),
    host:[hr.w,hr.h], input:[ir.w,ir.h],
    covers: ir.w>=hr.w-1 && ir.h>=hr.h-1,
    exact: Math.abs(ir.w-hr.w)<=1 && Math.abs(ir.h-hr.h)<=1
  };
}
window.__probe=()=>{
  let res={caps:{anchorName:CSS.supports('anchor-name: --t'),
    insetAnchor:CSS.supports('inset: anchor(top) anchor(right) anchor(bottom) anchor(left)')}};
  const SH='anchor(top) anchor(right) anchor(bottom) anchor(left)';
  const A={inset:SH};
  const B={inset:SH, width:'anchor-size(width)', height:'anchor-size(height)'};
  const C={top:'anchor(top)', left:'anchor(left)', width:'anchor-size(width)', height:'anchor-size(height)'};
  const D={top:'anchor(top)', left:'anchor(left)', width:'anchor-size(width)', height:'anchor-size(height)', boxSizing:'border-box'};
  const E={inset:SH, width:'anchor-size(width)', height:'anchor-size(height)', boxSizing:'border-box'};
  const F={insetBlockStart:'anchor(top)', insetInlineStart:'anchor(left)', width:'anchor-size(width)', height:'anchor-size(height)'};
  const G={top:'anchor(top)', left:'anchor(left)', width:'anchor-size(width)', height:'anchor-size(height)', padding:'0', border:'0'};
  const H={inset:SH, width:'anchor-size(width)', height:'anchor-size(height)', padding:'0', border:'0'};
  res.A=setup('hA','iA',A,'A inset shorthand only');
  res.B=setup('hB','iB',B,'B inset + anchor-size');
  res.C=setup('hC','iC',C,'C topleft + anchor-size (old)');
  res.D=setup('hD','iD',D,'D topleft + anchor-size + border-box');
  res.E=setup('hE','iE',E,'E inset + anchor-size + border-box');
  res.F=setup('hF','iF',F,'F logical inline-start + anchor-size');
  res.G=setup('hG','iG',G,'G topleft + anchor-size zero pad/border');
  res.H=setup('hH','iH',H,'H inset + anchor-size zero pad/border');
  return res;
};
</script></body></html>`;

(async () => {
  const which = process.argv[2] || 'webkit';
  const map = {chromium, webkit};
  const browser = await map[which].launch({headless: true});
  const page = await browser.newPage({viewport: {width: 1280, height: 720}});
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForTimeout(400);
  const res = await page.evaluate(() => window.__probe());
  console.log('#### ' + which);
  for (const k of ['A','B','C','D','E','F','G','H']) {
    const r = res[k];
    console.log(`${r.case.padEnd(42)} covers=${String(r.covers).padEnd(5)} exact=${String(r.exact).padEnd(5)} host=${JSON.stringify(r.host)} input=${JSON.stringify(r.input)}`);
  }
  console.log('caps:', JSON.stringify(res.caps));
  await browser.close();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
