// Definitive scroll-tracking check. Measures AFTER waiting frames, in both headless
// and headed Chrome, because anchor positions are recomputed in the compositor and may
// lag the synchronous getBoundingClientRect call.
const {chromium} = require('playwright-core');

const CHROME = '/Users/gonzoblasco/Library/Caches/ms-playwright/chromium-1243/chrome-mac-arm64/Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing';

const HTML = `<!doctype html><html><head><meta charset="utf-8"><style>
  .vh { border:0; clip:rect(0 0 0 0); clip-path:inset(50%); height:1px; margin:-1px;
        overflow:hidden; padding:0; position:absolute; width:1px; white-space:nowrap; }
  .host { position:relative; width:200px; height:44px; background:#ddd; margin:8px;
          display:flex; align-items:center; gap:8px; }
  .scroll { height:150px; overflow-y:auto; border:2px solid #333; }
  .win { height:120px; overflow-y:auto; border:2px solid #09c; }
</style></head><body>
<div id="out">PENDING</div>
<div class="scroll" id="sc"></div>
<div class="win" id="wsc"></div>

<script>
window.__run = async () => {
  const sleep = ms => new Promise(r => setTimeout(r, ms));
  let uid = 0;
  function build(container, pos) {
    let host = document.createElement('div'); host.className='host';
    let name = '--u' + (++uid); host.style.anchorName = name;
    let vh = document.createElement('span'); vh.className='vh';
    let inp = document.createElement('input');
    inp.style.cssText = 'position:'+pos+';margin:0;position-anchor:'+name+
      ';inset:anchor(top) anchor(right) anchor(bottom) anchor(left)';
    vh.appendChild(inp); host.appendChild(vh); host.appendChild(document.createTextNode('x'));
    container.appendChild(host);
    return {host, inp};
  }
  let sc = document.getElementById('sc');
  let items = [];
  for (let i=0;i<6;i++) items.push(build(sc,'fixed'));

  function dy() {
    return items.map(p => {
      let hr = p.host.getBoundingClientRect(), ir = p.inp.getBoundingClientRect();
      return +(ir.y - hr.y).toFixed(1);
    });
  }
  let res = {};
  res.beforeScroll = dy();

  // scroll and then wait several frames / real time
  sc.scrollTop = 40;
  res.scrollTopApplied = sc.scrollTop;
  res.immediate = dy();
  await sleep(50);  res.after50ms = dy();
  await sleep(300); res.after350ms = dy();
  // force a style/layout invalidation on the anchor to see if it re-resolves
  await sleep(300); res.after650ms = dy();

  // also check the window scroller (document scroll)
  document.body.style.height = '3000px';
  window.scrollTo(0, 200);
  await sleep(300);
  res.afterWindowScroll = dy();

  document.getElementById('out').textContent = JSON.stringify(res, null, 2);
  return res;
};
</script></body></html>`;

(async () => {
  for (const headless of [true, false]) {
    const browser = await chromium.launch({executablePath: CHROME, headless});
    const page = await browser.newPage({viewport: {width: 900, height: 700}});
    await page.setContent(HTML, {waitUntil: 'load'});
    await page.evaluate(() => window.__run());
    await page.waitForFunction(() => document.getElementById('out').textContent !== 'PENDING', {timeout: 20000});
    const res = JSON.parse(await page.textContent('#out'));
    console.log(`===== headless=${headless} =====`);
    console.log(JSON.stringify(res));
    await browser.close();
  }
})().catch(e => { console.error('FAILED', e.message); process.exit(1); });
