// Runs in real Chrome (not headless shell) to verify the two claims we make to the maintainer:
// 1) position: absolute does NOT resolve anchor() when the anchor is an ancestor
// 2) position: fixed inside an overflow:auto container does not follow scroll
const {chromium} = require('playwright-core');

const CHROME = '/Users/gonzoblasco/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .host { position:relative; width:200px; height:44px; background:#ddd; margin:16px;
          display:flex; align-items:center; gap:8px; }
  .scroll { height:150px; overflow-y:auto; border:2px solid #333; }
</style></head><body>
<div id="out">PENDING</div>
<div class="host" id="hAbs"><span class="vh"><input id="iAbs"></span>absolute</div>
<div class="host" id="hFix"><span class="vh"><input id="iFix"></span>fixed</div>
<div class="scroll" id="sc"></div>
<script>
let uid=0;
function g(id){let r=document.getElementById(id).getBoundingClientRect();
  return {x:+r.x.toFixed(1),y:+r.y.toFixed(1),w:+r.width.toFixed(1),h:+r.height.toFixed(1)};}
function wire(hostId,inputId,pos){
  let host=document.getElementById(hostId), input=document.getElementById(inputId);
  let name='--n'+(++uid); host.style.anchorName=name;
  input.style.cssText='position:'+pos+';margin:0;position-anchor:'+name+
    ';inset:anchor(top) anchor(right) anchor(bottom) anchor(left)';
  return {host,input,name};
}
let A=wire('hAbs','iAbs','absolute');
let F=wire('hFix','iFix','fixed');

// scroll container items
let items=[];
let sc=document.getElementById('sc');
for(let i=0;i<6;i++){
  let host=document.createElement('div'); host.className='host'; host.style.margin='8px';
  let name='--s'+(++uid); host.style.anchorName=name;
  let vh=document.createElement('span'); vh.className='vh';
  let inp=document.createElement('input');
  inp.style.cssText='position:fixed;margin:0;position-anchor:'+name+
    ';inset:anchor(top) anchor(right) anchor(bottom) anchor(left)';
  vh.appendChild(inp); host.appendChild(vh); host.appendChild(document.createTextNode('item'+i));
  sc.appendChild(host); items.push({host,inp});
}
requestAnimationFrame(()=>{
  let res={caps:{anchorName:CSS.supports('anchor-name: --t'),anchorScope:CSS.supports('anchor-scope: all')}};
  // claim 1
  res.absolute={host:g('hAbs'),input:g('iAbs'),positionAnchor:getComputedStyle(A.input).positionAnchor,
    usedTop:getComputedStyle(A.input).top, usedWidth:getComputedStyle(A.input).width};
  res.fixed={host:g('hFix'),input:g('iFix'),positionAnchor:getComputedStyle(F.input).positionAnchor,
    usedTop:getComputedStyle(F.input).top, usedWidth:getComputedStyle(F.input).width};
  res.claim1_absoluteFails = res.absolute.input.w < res.absolute.host.w - 10;
  res.claim1_fixedWorks = Math.abs(res.fixed.input.w - res.fixed.host.w) <= 1;

  // claim 2: scroll
  function track(){return items.map((p,i)=>{let hr=p.host.getBoundingClientRect(),ir=p.inp.getBoundingClientRect();
    return {tag:i,dy:+(ir.y-hr.y).toFixed(1)};});}
  res.scrollBefore=track();
  sc.scrollTop=40;
  res.scrollTopApplied=sc.scrollTop;
  res.scrollAfter=track();
  res.claim2_scrollBreaks = res.scrollAfter.every(r=>Math.abs(r.dy)>1);

  // claim 3: duplicate names collide?
  let sc2=document.createElement('div'); sc2.className='scroll';
  let dup=[];
  for(let i=0;i<3;i++){
    let host=document.createElement('div'); host.className='host';
    host.style.anchorName='--dup';
    let vh=document.createElement('span'); vh.className='vh';
    let inp=document.createElement('input');
    inp.style.cssText='position:fixed;margin:0;position-anchor:--dup;inset:anchor(top) anchor(right) anchor(bottom) anchor(left)';
    vh.appendChild(inp); host.appendChild(vh); host.appendChild(document.createTextNode('d'+i));
    sc2.appendChild(host); dup.push({host,inp});
  }
  document.body.appendChild(sc2);
  res.duplicates=dup.map((p,i)=>{let hr=p.host.getBoundingClientRect(),ir=p.inp.getBoundingClientRect();
    return {tag:i,dy:+(ir.y-hr.y).toFixed(1),covers:Math.abs(ir.y-hr.y)<=1};});
  res.claim_duplicatesCollide = res.duplicates.some(r=>!r.covers);

  // anchor-scope fixes duplicates?
  sc2.style.anchorScope='all';
  requestAnimationFrame(()=>{
    res.duplicatesScoped=dup.map((p,i)=>{let hr=p.host.getBoundingClientRect(),ir=p.inp.getBoundingClientRect();
      return {tag:i,dy:+(ir.y-hr.y).toFixed(1),covers:Math.abs(ir.y-hr.y)<=1};});
    res.claim_anchorScopeFixes = res.duplicatesScoped.every(r=>r.covers);
    document.getElementById('out').textContent=JSON.stringify(res,null,2);
  });
});
</script></body></html>`;

(async () => {
  const browser = await chromium.launch({executablePath: CHROME, headless: true});
  const page = await browser.newPage();
  const errors = [];
  page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForFunction(() => document.getElementById('out').textContent !== 'PENDING', {timeout: 15000});
  const res = JSON.parse(await page.textContent('#out'));
  res.consoleErrors = errors;
  console.log(JSON.stringify(res, null, 2));
  await browser.close();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
