// Verifies the two override paths claimed in the draft, in real Chrome, with the
// actual helper semantics (anchor-name: var(--p, default) on host + input).
const {chromium} = require('playwright-core');
const CHROME = '/Users/gonzo'.replace('gonzo','gonzoblasco') + '/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .host { position:relative; width:200px; height:44px; background:#ddd; margin:12px; }
  .viaClass { --react-aria-anchor-name: --from-class; }
</style></head><body>
<div id="out">PENDING</div>

<!-- 1: no override -->
<div class="host" id="h1"><span class="vh"><input id="i1"></span></div>
<!-- 2: override via class on the host itself -->
<div class="host viaClass" id="h2"><span class="vh"><input id="i2"></span></div>
<!-- 3: override on an ANCESTOR element -->
<div class="viaClass" id="anc"><div class="host" id="h3"><span class="vh"><input id="i3"></span></div></div>

<script>
let uid = 0;
function wire(hostId, inputId, styleOverride) {
  let host = document.getElementById(hostId), input = document.getElementById(inputId);
  let def = '--comp-' + (++uid);
  // component behaviour: var() with the per-instance default as fallback
  host.style.anchorName = 'var(--react-aria-anchor-name, ' + def + ')';
  input.style.cssText = 'position:fixed;margin:0;position-anchor:var(--react-aria-anchor-name, ' + def + ')' +
    ';inset:anchor(top) anchor(right) anchor(bottom) anchor(left)';
  if (styleOverride) { host.style.anchorName = styleOverride; }
  let hr = host.getBoundingClientRect(), ir = input.getBoundingClientRect();
  return {
    host: {x:+hr.x.toFixed(1), w:+hr.width.toFixed(1), h:+hr.height.toFixed(1)},
    input: {x:+ir.x.toFixed(1), w:+ir.width.toFixed(1), h:+ir.height.toFixed(1)},
    anchorName: getComputedStyle(host).getPropertyValue('anchor-name').trim(),
    positionAnchor: getComputedStyle(input).getPropertyValue('position-anchor').trim(),
    covers: Math.abs(ir.x-hr.x)<=1 && Math.abs(ir.width-hr.width)<=1 && Math.abs(ir.height-hr.height)<=1
  };
}
requestAnimationFrame(() => {
  let res = {};
  res.caps = {anchorName: CSS.supports('anchor-name: --t')};
  res['1-default'] = wire('h1','i1');
  res['2-override-class-on-host'] = wire('h2','i2');
  res['3-override-on-ancestor'] = wire('h3','i3');
  // 4: inline style anchorName on the host (the other override path)
  res['4-override-inline-style'] = wire('h1','i1', '--from-inline');
  document.getElementById('out').textContent = JSON.stringify(res, null, 2);
});
</script></body></html>`;

(async () => {
  const browser = await chromium.launch({executablePath: CHROME, headless: true});
  const page = await browser.newPage();
  await page.setContent(HTML, {waitUntil: 'load'});
  await page.waitForFunction(() => document.getElementById('out').textContent !== 'PENDING', {timeout: 15000});
  console.log(await page.textContent('#out'));
  await browser.close();
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
