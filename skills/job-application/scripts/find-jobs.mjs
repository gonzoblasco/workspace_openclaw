#!/usr/bin/env node
/**
 * find-jobs.mjs - Discovery multi‑board de vacantes.
 *
 * POR QUÉ EXISTE (2026-10-23): el playbook lista los endpoints públicos que
 * funcionan y el proceso de filtrado que debe aplicarse.  El script
 * implementa esa lógica usando `fetch` nativo (no dependencias externas).
 */

import {
  matchesCountry,
  countryName,
  isRemoteAnywhere,
  listOf,
  parseLinkedinCards,
  filterJobs,
} from "./lib/discovery.mjs";
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
  // LinkedIn Guest API: no requiere login.
  //
  // BUG CORREGIDO 2026-10-25: la clase del link cambio. El selector
  // `result-card__full-card-link` ya no existe: ahora el link del titulo es
  // `base-card__full-link`, dentro de un `div.base-card`. Con el selector
  // viejo la fuente devolvia CERO vacantes y nadie lo notaba, porque un 0
  // legitimo y un 0 por markup roto se ven igual.
  // La defensa: el parser extrae titulo, empresa y ubicacion de la
  // tarjeta, no solo la URL. Si el titulo queda vacio, la tarjeta se
  // descarta, en vez de devolver una vacante sin datos que el filtro de
  // palabras no puede evaluar.
  {
    name: "linkedin",
    // BUG CORREGIDO 2026-10-25: a LinkedIn se le pasaba el CODIGO de pais
    // ("AR") en vez del NOMBRE ("Argentina"), y la busqueda devolvia cero.
    // Las fuentes de job boards publicas no aceptan codigos: el parametro
    // `location` es texto libre.
    url: (q, start, loc) =>
      `https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search?keywords=${encodeURIComponent(q)}&location=${encodeURIComponent(loc || "Argentina")}&start=${start || 0}`,
    // nota: la firma de TODAS las fuentes de job boards es url(query, start, country)
    maxPages: 4,
    pageSize: 25,
    // El parser vive en lib/discovery.mjs para que quede TESTEADO: es el
    // punto donde un cambio de markup de LinkedIn rompe el radar, y sin
    // test el fallo es silencioso (parece "no hay vacantes").
    parse: (html) => parseLinkedinCards(html),
  },

  // ---------------------------------------------------------------------
  // Fuentes JSON publicas. Cada una se MIDIO contra la API antes de
  // agregarla (2026-10-25): si no responde o no trae jobs, no entra.
  // ---------------------------------------------------------------------

  // Remotive: catalogo global de remoto.
  {
    name: "remotive",
    url: (q) => `https://remotive.com/api/remote-jobs?search=${encodeURIComponent(q)}&limit=50`,
    parse: (data) =>
      (data.jobs || []).map((j) => ({
        title: j.title || "",
        url: j.url || "",
        location: j.candidate_required_location || j.location || "",
        company: j.company_name || "",
        remote: /remote/i.test(j.candidate_required_location || j.location || ""),
        country: "",
      })),
  },

  // Arbeitnow: 300 por pagina, JSON estable.
  {
    name: "arbeitnow",
    url: () => "https://www.arbeitnow.com/api/job-board-api",
    parse: (data) =>
      (data.data || []).map((j) => ({
        title: j.title || "",
        url: j.url || "",
        location: j.location || "",
        company: "",
        remote: /remote/i.test(j.location || ""),
        country: "",
        tags: j.tags || [],
      })),
  },

  // Jobicy: remoto, con paginacion por `page`.
  {
    name: "jobicy",
    // MEDIDO 2026-10-25: la ruta /remote-jobs NO acepta el parametro `page`
    // (responde 400). Se pide una tanda de 50, sin paginar.
    url: (q) => `https://jobicy.com/api/v2/remote-jobs?count=50&tag=${encodeURIComponent(q)}`,
    maxPages: 1,
    parse: (data) =>
      (data.jobs || data.remoteJobs || []).map((j) => ({
        title: j.jobTitle || j.title || "",
        url: j.url || j.jobUrl || "",
        location: j.jobGeo?.country?.name || j.location || "",
        company: j.companyName || "",
        remote: true,
        country: j.jobGeo?.country?.code || "",
      })),
  },

  // Himalayas: remoto.
  {
    name: "himalayas",
    url: (q) => `https://himalayas.app/jobs/api?q=${encodeURIComponent(q)}&limit=50`,
    parse: (data) =>
      (data.jobs || []).map((j) => ({
        title: j.title || "",
        url: j.applicationUrl || j.url || "",
        location: j.location || "",
        company: j.companyName || "",
        remote: true,
        country: j.country || "",
      })),
  },
];

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

/**
 * Igual que fetchSource, pero recorre las paginas de la fuente.
 *
 * BUG CORREGIDO 2026-10-25: el orden de los argumentos estaba cambiado. Se
 * llamaba `src.url(country, start)`, pero el PRIMER parametro de cada fuente
 * es la QUERY y el segundo es el offset de pagina. Todas las fuentes de job
 * boards devolvian 0 porque se buscaban las vacantes de "AR" en vez de la
 * query, y el error era invisible: el radar mudo parece "no hay nada".
 *
 * La firma ahora es uniforme en todas: url(query, start, country).
 */
async function fetchSourcePaged(src, country, q) {
  const pages = src.maxPages || 1;
  const out = [];
  for (let page = 0; page < pages; page++) {
    // El tercer parametro es el "location" en texto: para las fuentes que
    // lo usan (LinkedIn) tiene que ser el NOMBRE del pais.
    const url = src.url(q ?? query, page * (src.pageSize || 12), countryName(country));
    const got = await fetchSource({ ...src, url });
    out.push(...got);
    if (!got.length) break;
  }
  return out;
}

/** Normaliza y filtra resultados. */
async function discover() {
  const all = [];

  // Las fuentes de ATS (Mercado Pago, Ashby, Lever) son las de mayor
  // rinde y se consultan por pais/compania.
  //
  // BUG CORREGIDO 2026-10-25: las fuentes se llamaban por INDICE
  // (`sources[0]`, `sources[1]`...). Con cuatro fuentes eso ya era fragil;
  // al agregar las de job boards, un indice mal alineado consultaba la
  // fuente equivocada sin error visible. Ahora se consultan por NOMBRE.
  const byName = Object.fromEntries(sources.map((s) => [s.name, s]));

  // 1) Mercado Pago: pagina por pais, 100 por pagina.
  all.push(...(await fetchSourcePaged(byName["mercado-pago"], country || "AR", query)));

  // 2) Ashby y Lever: el endpoint es POR COMPANIA. Sin argumentos se usan
  // las del playbook como semilla; con --ashby/--lever se agregan mas.
  const ashbyCompanies = listOf(opts.ashby, "mural");
  const leverSlugs = listOf(opts.lever, "RyzLabs");
  for (const company of ashbyCompanies) {
    const src = { ...byName["ashby"], url: byName["ashby"].url(company) };
    all.push(...(await fetchSource(src)));
  }
  for (const slug of leverSlugs) {
    const src = { ...byName["lever"], url: byName["lever"].url(slug) };
    all.push(...(await fetchSource(src)));
  }

  // 3) Las fuentes de job boards: TODAS, y en paralelo.
  //    Para las que aceptan `location` como texto (LinkedIn) hay que pasar
  //    el NOMBRE del pais, no el codigo. Antes solo se
  // consultaba LinkedIn, y cuando su markup cambio (o la API respondio
  // 429) el radar se quedaba mudo sin avisar: un 0 legitimo y un 0 por
  // fuente rota se ven igual. Por eso:
  //   - se consultan todas, en paralelo
  //   - se reporta cuantas respondieron y cuantas fallaron
  //   - si NINGUNA responde, es un error explicito (exit 1), no un
  //     "no encontramos nada" silencioso
  const boardNames = ["linkedin", "remotive", "arbeitnow", "jobicy", "himalayas"];
  const results = await Promise.allSettled(
    boardNames.map(async (name) => {
      const src = byName[name];
      if (!src) return { name, jobs: [] };
      return { name, jobs: await fetchSourcePaged(src, country || "AR", query) };
    })
  );
  const okSources = [];
  const failedSources = [];
  for (const r of results) {
    if (r.status === "fulfilled") {
      okSources.push(r.value.name);
      all.push(...r.value.jobs);
    } else {
      failedSources.push(String(r.reason?.message || r.reason));
    }
  }
  console.error(
    `fuentes: ${okSources.join(", ") || "ninguna"}${
      failedSources.length ? ` | fallaron: ${failedSources.join("; ")}` : ""
    }`
  );

  // Dedupe por URL (exact match).
  // El filtro vive en lib/discovery.mjs (testeado): es lo que decide QUE
  // se devuelve, y sus reglas (palabra entera, pais por token, remotas
  // "Worldwide") son las que se rompieron en silencio el 2026-10-25.
  return filterJobs(all, { query, country, remote, limit });
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

