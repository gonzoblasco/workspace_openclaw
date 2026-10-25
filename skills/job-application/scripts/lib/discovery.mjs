// discovery.mjs - Funciones PURAS del discovery de vacantes.
//
// POR QUE EXISTE (2026-10-25): el 2026-10-25 el radar de vacantes
// dejo de encontrar nada, y la causa NO fue que no hubiera vacantes: fueron
// CINCO bugs encadenados, cada uno invisible desde fuera (un radar mudo
// parece "no hay nada"). El mas caro: las fuentes se llamaban con los
// argumentos en el orden equivocado, asi que se buscaban las vacantes de
// "AR" en vez de la query.
//
// La leccion de fondo: un scraper sin tests es un scraper que se rompe
// callado. Estas funciones son las que decidian QUE se devuelve, asi que
// son las que quedan cubiertas por tests: cuando un sitio cambie su markup
// o sus parametros, el fallo sale en la suite, no en el silencio.
//
// TODO lo de aca es puro (sin red, sin browser): se puede testear.

/**
 * Coincide una vacante con el pais pedido, por palabra entera.
 * "AR" matchea "Argentina" y "Buenos Aires, Argentina", pero NO
 * "Bentonville, Arkansas" (que contiene "ar" como substring).
 */
export function matchesCountry(v, country) {
  const want = String(country).trim().toLowerCase();
  if (!want) return true;
  // La concatenacion dejaba ", " cuando ambos estaban vacios, y eso NO
  // esta vacio: la vacante se descartaba. Se arma la lista y se unite.
  const partes = [v.location, v.country].map((x) => String(x || "").trim()).filter(Boolean);
  const hay = partes.join(", ").toLowerCase();
  // Si la fuente no dio ubicacion, no se descarta: descartar por un dato
  // ausente seria perder la vacante entera.
  if (!hay) return true;
  const esCodigo = /^[a-z]{2}$/.test(want);
  if (esCodigo) {
    // Codigo de 2 letras: se busca el token suelto Y el nombre del pais.
    // "AR" tiene que matchear "Argentina" (que es como lo traen las
    // fuentes), no solo el token "AR" (que no aparece en ningun lado).
    if (new RegExp(`(^|[\s,;/(])${want}($|[\s,;/)])`, "i").test(hay)) return true;
    const nombre = COUNTRY_NAMES[want];
    if (nombre) {
      return new RegExp(`\\b${nombre}\\b`, "i").test(hay);
    }
    return false;
  }
  return new RegExp(`\\b${want.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i").test(hay);
}

/**
 * El nombre del pais a partir del codigo, para las fuentes que lo piden
 * como texto (LinkedIn). Si no hay mapeo, se pasa tal cual.
 */
export function countryName(country) {
  const want = String(country || "AR").trim().toLowerCase();
  const nombre = COUNTRY_NAMES[want];
  if (!nombre) return want;
  // el mapa tiene alternativas ("mexico|méxico"): se toma la primera
  return nombre.split("|")[0];
}

/**
 * Una vacante es "remota en cualquier parte" cuando la fuente la declara
 * remota y su ubicacion no es de un pais concreto. Estas son las que
 *Interestan para LATAM: un puesto "Worldwide" es alcanzable desde Buenos
 * Aires (con el sol del otro lado).
 */
export function isRemoteAnywhere(v) {
  if (!v.remote) return false;
  const loc = String(v.location || "").toLowerCase();
  if (!loc) return true;
  return /worldwide|anywhere|anywhere in the world|global|international|remote|remoto|latam|am[eé]rica latina/i.test(
    loc
  );
}

/**
 * Los codigos de pais de dos letras que aparecen en las fuentes. No es
 * exhaustivo: es lo que hace falta para no descartar por codigo lo que
 * vuelve con el nombre completo.
 */
const COUNTRY_NAMES = {
  ar: "argentina",
  br: "brazil|brasil",
  mx: "mexico|méxico",
  co: "colombia",
  cl: "chile",
  pe: "peru|perú",
  uy: "uruguay",
  py: "paraguay",
  bo: "bolivia",
  ec: "ecuador",
  ve: "venezuela",
  cr: "costa rica",
  pa: "panama|panamá",
  gt: "guatemala",
  do: "dominican|dominicana",
  us: "united states|estados unidos|usa",
  es: "spain|españa",
  ca: "canada",
  gb: "united kingdom|reino unido",
  de: "germany|alemania",
  fr: "france|francia",
  nl: "netherlands|holanda|paises bajos",
  pt: "portugal",
  it: "italy|italia",
  in: "india",
  au: "australia",
  nz: "new zealand",
  za: "south africa|sudafrica",
};



/**
 * Parsea las tarjetas de LinkedIn (guest API).
 *
 * BUG CORREGIDO 2026-10-25: la clase del link cambio. El selector
 * `result-card__full-card-link` ya no existe: ahora es
 * `base-card__full-link`, dentro de un `div.base-card`. Con el selector
 * viejo la fuente devolvia CERO vacantes y nadie lo notaba, porque un 0
 * legitimo y un 0 por markup roto se ven igual.
 *
 * El titulo esta en el `span.sr-only` del link, y la ubicacion en el
 * bloque `job-search-card__location`.
 */
export function parseLinkedinCards(html) {
  const out = [];
  const cards = String(html).split("<li>").slice(1);
  for (const card of cards) {
    const link = card.match(/base-card__full-link[^>]*href="([^"]+)"/i);
    if (!link) continue;
    const url = link[1].replace(/&amp;/g, "&").split("?")[0];
    const titleMatch = card.match(/<span class="sr-only">([\s\S]*?)<\/span>/i);
    if (!titleMatch) continue;
    const title = titleMatch[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim();
    if (!title) continue;
    const locM = card.match(/job-search-card__location[^>]*>([\s\S]*?)</i);
    const location = locM ? locM[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() : "";
    const compM = card.match(/base-search-card__subtitle[^>]*>([\s\S]*?)</i);
    out.push({
      title,
      url,
      location,
      company: compM ? compM[1].replace(/<[^>]+>/g, " ").replace(/\s+/g, " ").trim() : "",
      remote: /remote|remoto|h[ií]brido/i.test(location),
      // El pais NO se hardcodea: la ubicacion de la tarjeta ya lo trae.
      country: (location.match(/([^,]+)$/) || [""])[1].trim(),
    });
  }
  return out;
}

/**
 * Filtra las vacantes por query, pais y remoto.
 *
 * BUG CORREGIDO 2026-10-25: el filtro de pais era un `includes` plano, y
 * "ar" matcheaba "Arkansas" (Bentonville, Arkansas, Estados Unidos pasaba
 * el filtro de Argentina). Y una vacante remota "Worldwide" - que es
 * justamente una oportunidad LATAM - se descartaba por no tener "AR".
 */
export function filterJobs(jobs, { query, country, remote, limit }) {
  const lowerQuery = String(query || "").toLowerCase();
  // Match por palabra entera: "UX" no puede matchear "aUXiliar".
  const wordRe = new RegExp(`\\b${lowerQuery.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`, "i");
  const seen = new Set();
  const uniq = [];
  for (const item of jobs) {
    if (!item.url) continue;
    const key = item.url.split("?")[0].replace(/\/$/, "");
    if (seen.has(key)) continue;
    seen.add(key);
    uniq.push(item);
  }
  const filtered = uniq.filter((v) => {
    const titleMatch = v.title ? wordRe.test(v.title) : true;
    const locationMatch = country ? matchesCountry(v, country) || isRemoteAnywhere(v) : true;
    const remoteMatch = remote ? v.remote === true : true;
    return titleMatch && locationMatch && remoteMatch;
  });
  return filtered.slice(0, limit || filtered.length);
}

/**
 * Normaliza un flag que acepta coma o repetido: --ashby a,b --ashby c
 */
export function listOf(value, fallback) {
  if (!value) return [fallback];
  const arr = Array.isArray(value) ? value : String(value).split(",");
  const out = arr.map((v) => String(v).trim()).filter(Boolean);
  return out.length ? out : [fallback];
}
