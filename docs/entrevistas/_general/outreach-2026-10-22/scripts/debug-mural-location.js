// debug-mural-location.js - Sonda del combobox de Location de Ashby.
//
// Por que existe: el campo "Location" de Ashby es un combobox con
// autocompletado (role=combobox, aria-autocomplete=list). Es el unico
// campo que el script no logra completar, y es REQUERIDO ("Missing entry
// for required field: Location"). Los selectores probados
// ([role=option], li, [class*=option], [class*=suggestion]) no lo toman,
// asi que esta sonda vuelca TODO lo visible que matchee "Buenos Aires"
// para ver como se llama realmente la opcion.
//
// Uso: node tmp/job-search-2026-10-22/debug-mural-location.js
const { chromium } = require("/Users/gonzoblasco/.openclaw/workspace/projects/a11y-fixer/node_modules/playwright");
const EXE = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const APPLY = "https://jobs.ashbyhq.com/mural/3493ea21-5b96-4383-964a-996249db3a14/application";

(async () => {
  const b = await chromium.launch({ headless: true, executablePath: EXE });
  const p = await b.newPage();
  await p.goto(APPLY, { waitUntil: "networkidle", timeout: 45000 });
  await p.waitForTimeout(3000);

  const cb = p.locator('input[role="combobox"]').first();
  await cb.click();
  await cb.type("Buenos Aires", { delay: 70 });
  await p.waitForTimeout(4500);

  const dump = await p.evaluate(() => {
    const out = [];
    document.querySelectorAll("body *").forEach((e) => {
      if (e.children.length > 2) return; // solo hojas
      const t = (e.textContent || "").replace(/\s+/g, " ").trim();
      if (!t || t.length > 80) return;
      if (!/buenos aires/i.test(t)) return;
      const r = e.getBoundingClientRect();
      if (r.width === 0 && r.height === 0) return;
      out.push({
        tag: e.tagName,
        cls: (e.className || "").toString().slice(0, 60),
        role: e.getAttribute("role") || "",
        id: (e.id || "").slice(0, 24),
        txt: t,
      });
    });
    return out;
  });

  console.log("=== elementos visibles que matchean 'Buenos Aires':");
  dump.slice(0, 12).forEach((d) =>
    console.log(`  ${d.tag} role=${d.role || "-"} id=${d.id || "-"} cls=${d.cls} | ${d.txt}`)
  );

  // el aria-activedescendant dice cual es la opcion activa
  const aria = await p.evaluate(() => {
    const c = document.querySelector('input[role="combobox"]');
    return {
      expanded: c?.getAttribute("aria-expanded"),
      controls: c?.getAttribute("aria-controls"),
      active: c?.getAttribute("aria-activedescendant"),
      listbox: c?.getAttribute("aria-autocomplete"),
    };
  });
  console.log("\naria del combobox:", JSON.stringify(aria));

  // probamos: Enter
  await cb.press("Enter");
  await p.waitForTimeout(2000);
  const after = await p.evaluate(() => {
    const c = document.querySelector('input[role="combobox"]');
    return {
      valor: c?.value,
      expanded: c?.getAttribute("aria-expanded"),
      active: c?.getAttribute("aria-activedescendant"),
    };
  });
  console.log("tras Enter:", JSON.stringify(after));

  await b.close();
  process.exit(0);
})().catch((e) => {
  console.log("ERR", e.message.slice(0, 250));
  process.exit(1);
});
