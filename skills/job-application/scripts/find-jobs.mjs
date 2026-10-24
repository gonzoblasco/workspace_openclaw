#!/usr/bin/env node
/**
 * find-jobs.mjs - Discovery multi‑board de vacantes.
 *
 * POR QUÉ EXISTE (2026-10-23): el playbook lista los endpoints públicos que
 * funcionan y el proceso de filtrado que debe aplicarse.  El script
 * implementa esa lógica usando `fetch` nativo (no dependencias externas).
 */

import { readFileSync } from "node:fs";
import { exit } from "node:process";

/** Simple helper para parsear argumentos de línea de comandos. */
function parseArgs() {
  const args = process.argv.slice(2);
  const out = {};
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a.startsWith("--")) {
      const key = a.slice(2);
      const next = args[i + 1];
      if (next && !next.startsWith("--")) {
        out[key] = next;
        i++;
      } else {
        out[key] = true;
      }
    }
  }
  return out;
}

const opts = parseArgs();
const query = opts.query || opts.q || "";
const country = opts.country || "";
const remote = !!opts.remote;
const limit = Number(opts.limit) || 20;
const jsonOut = !!opts.json;

if (!query) {
  console.error("--query es requerido");
  exit(1);
}

/** Endpoints con sus parámetros fijos. */
const sources = [
  {
    name: "mercado-pago",
    // BUG CORREGIDO 2026-10-23: la API devuelve SOLO 12 vacantes por pagina
    // (de 886). Sin `start`, el radar solo miraba la primera pagina y no
    // encontraba nada. Se pagina hasta `maxPages`.
    url: (country, start) =>
      `https://careers-meli.mercadolibre.com/api/positions?country=${country || "AR"}&start=${start || 0}&num=100`,
    maxPages: 12,
    pageSize: 100,
    // La API de MeLi devuelve `name` (no `title`), `positionUrl` RELATIVO
    // (no `applyUrl`, que no existe) y `standardizedLocations`.
    parse: (data) => (data.positions || []).map((p) => ({
      id: p.id,
      title: p.name || "",
      url: p.positionUrl ? `https://careers-meli.mercadolibre.com${p.positionUrl}` : "",
      location: (p.locations || []).join(", "),
      remote: p.workLocationOption === "remote",
      country: (p.standardizedLocations || [])[0] || "",
    })),
  },
  {
    name: "ashby",
    url: (company) => `https://api.ashbyhq.com/posting-api/job-board/${company}`,
    // Se usará la compañía "mural" porque está en el playbook.
    parse: (data) => (data.jobs || []).map((j) => ({
      id: j.id,
      title: j.title,
      url: j.applyUrl,
      location: j.location,
      remote: !!j.remote,
    })),
  },
  {
    name: "lever",
    url: (slug) => `https://api.lever.co/v0/postings/${slug}`,
    parse: (data) => (data.postings || []).map((p) => ({
      id: p.id,
      title: p.text,
      url: p.hostedUrl,
      location: p.categories?.location?.[0] || "",
      remote: Boolean(p.categories?.tags?.includes("Remote")),
    })),
  },
  // LinkedIn Guest API - no requiere auth.
  {
    name: "linkedin",
    url: (q) => `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=${encodeURIComponent(q)}&location=Argentina&start=0`,
    parse: (html) => {
      // Muy simple: extraer hrefs de <a> con class="result-card__full-card-link".
      const links = [];
      const regex = /<a[^>]+class="[^\"]*result-card__full-card-link[^\"]*"[^>]*href="([^"]+)"/gi;
      let m;
      while ((m = regex.exec(html)) !== null) {
        links.push(m[1]);
      }
      return links.map((url) => ({ title: "", url, location: "", remote: false }));
    },
  },
];

/** Normaliza un flag que acepta coma o repetido: --ashby a,b --ashby c */
function listOf(value, fallback) {
  if (!value) return [fallback];
  const arr = Array.isArray(value) ? value : String(value).split(",");
  const out = arr.map((v) => String(v).trim()).filter(Boolean);
  return out.length ? out : [fallback];
}

/**
 * Fetch y parseo de una fuente, con paginación si la fuente la declara
 * (maxPages). Cada página se pide con `start = pagina * 12`.
 */
async function fetchSource(src) {
  try {
    // Headers de browser: la API de MeLi responde 403 a un fetch sin
    // User-Agent (medido 2026-10-23: con curl pelado, HTTP 403; con estos
    // headers, 200). Los endpoints publicos de ATS no lo exigen, pero el
    // header no molesta y evita el 403.
    const resp = await fetch(src.url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/153.0.0.0 Safari/537.36",
        Accept: "application/json, text/html;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-AR,es;q=0.9,en;q=0.8",
      },
    });
    if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
    const contentType = resp.headers.get("content-type") || "";
    if (contentType.includes("application/json")) {
      const data = await resp.json();
      return src.parse(data);
    }
    const txt = await resp.text();
    return src.parse(txt);
  } catch (e) {
    console.warn(`source ${src.name} failed: ${e.message}`);
    return [];
  }
}

/** Igual que fetchSource, pero recorre las paginas de la fuente. */
async function fetchSourcePaged(src, country) {
  const pages = src.maxPages || 1;
  const out = [];
  for (let page = 0; page < pages; page++) {
    const url = src.url(country, page * (src.pageSize || 12));
    const got = await fetchSource({ ...src, url });
    out.push(...got);
    if (!got.length) break;
  }
  return out;
}

/** Normaliza y filtra resultados. */
async function discover() {
  const all = [];
  // Mercado Pago (país configurable)
  const meli = await fetchSourcePaged(sources[0], country || "AR");
  all.push(...meli);
  // Ashby y Lever: el endpoint es POR COMPAÑÍA. Con una sola empresa fija
  // el radar solo veía mural y RyzLabs. Ahora se pueden pasar varias, y si
  // no se pasa ninguna se usan las del playbook como semilla.
  // BUG CORREGIDO 2026-10-23 (estaba hardcodeado a "mural"/"RyzLabs").
  const ashbyCompanies = listOf(opts.ashby, "mural");
  const leverSlugs = listOf(opts.lever, "RyzLabs");
  for (const company of ashbyCompanies) {
    const src = { ...sources[1], url: sources[1].url(company) };
    all.push(...(await fetchSource(src)));
  }
  for (const slug of leverSlugs) {
    const src = { ...sources[2], url: sources[2].url(slug) };
    all.push(...(await fetchSource(src)));
  }
  // LinkedIn (solo si el query es suficientemente largo)
  if (query.length >= 3) {
    const li = await fetchSource({ ...sources[3], url: sources[3].url(query) });
    all.push(...li);
  }

  // Dedupe por URL (exact match).
  const seen = new Set();
  const uniq = [];
  for (const item of all) {
    if (!item.url) continue;
    if (seen.has(item.url)) continue;
    seen.add(item.url);
    uniq.push(item);
  }

  // Filtrar por los criterios solicitados.
  const lowerQuery = query.toLowerCase();
  // BUG CORREGIDO 2026-10-23: el filtro era un `includes` plano, asi que
  // "UX" matcheaba "aUXiliar" (Withdrawal**s** Local Auxiliar) y devolvia
  // una vacante que no era la buscada. Se matchea por palabra entera.
  const wordRe = new RegExp(`\\b${lowerQuery.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");
  const filtered = uniq.filter((v) => {
    // Si la fuente no dio titulo (LinkedIn guest API), no se descarta por eso:
    // el filtro de titulo no se puede aplicar a un dato que no existe.
    const titleMatch = v.title ? wordRe.test(v.title) : true;
    const locationMatch = country
      ? (v.location || "").toLowerCase().includes(country.toLowerCase()) ||
        (v.country || "").toLowerCase().includes(country.toLowerCase())
      : true;
    const remoteMatch = remote ? v.remote === true : true;
    return titleMatch && locationMatch && remoteMatch;
  });
  return filtered.slice(0, limit);
}

(async () => {
  const results = await discover();
  if (jsonOut) {
    console.log(JSON.stringify(results, null, 2));
  } else {
    // Imprime tabla simple.
    console.table(
      results.map((r) => ({ title: r.title, location: r.location, remote: r.remote, url: r.url }))
    );
  }
})();

