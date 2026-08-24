---
name: search-fusion
metadata:
  category: "Web"
  tags:
    - busqueda
    - search
    - investigacion
    - web
description: "Busqueda efectiva por intencion: elige la estrategia y herramientas segun el tipo de busqueda (research, keyword, answer, news) y fusiona fuentes. Portado del concepto Search Fusion (ClawHub) adaptado a nuestras herramientas (DuckDuckGo + web_fetch + browser)."
user-invocable: false
---

# Search Fusion

Buscar de forma efectiva **eligiendo la estrategia por intencion** y fusionando resultados de multiples fuentes. Portado del concepto del plugin Search Fusion (ClawHub), adaptado a nuestro stack (web_search DuckDuckGo key-free + web_fetch + browser).

## Cuando usar

- Cualquier busqueda web que requiera mas que un resultado simple.
- Investigacion de APIs, specs, docs, precios.
- Cuando se necesita cruzar varias fuentes para confirmar algo.

## Elige la estrategia por intencion

| Intencion | Que es | Estrategia |
|---|---|---|
| **research** | Investigacion profunda de un tema | Varias busquedas + leer fuentes completas (web_fetch) |
| **keyword** | Busqueda clasica de un termino/pagina | DuckDuckGo (web_search) directo |
| **answer** | Respuesta directa a una pregunta | Buscar + extraer respuesta especifica de la fuente |
| **news** | Noticias/eventos recientes | Busqueda reciente (freshness) + verificar fecha |
| **code/spec** | Docs de API, specs tecnicas | Buscar + web_fetch de la doc oficial |

## Como fusionar (multi-fuente)

Para una investigacion seria, no conformarse con el primer resultado:

1. **Buscar** con DuckDuckGo (web_search tool).
2. **Leer** las 2-3 fuentes mas relevantes con web_fetch (no solo el snippet).
3. **Cruzar** - si las fuentes coinciden, es confiable; si contradicen, anotar la discrepancia.
4. **Dedupe** - no repetir el mismo dato de multiples fuentes; sintetizar.

## **Flujo sugerido por intencion**

### Investigacion (research)
```
web_search "<tema>" (2-3 queries distintas)
  -> web_fetch las 2-3 fuentes top
  -> sintetizar, citando la fuente
```

### Doc de API / spec
```
web_search "<libreria> <api> <doc>"
  -> web_fetch la doc oficial (priorizar el sitio oficial sobre blogs)
  -> extraer el spec/parametros
```

### Respuesta a un dato (answer)
```
web_search "<pregunta concreta>"
  -> verificar en 1-2 fuentes confiables
  -> responder con la fuente
```

### Noticias (news)
```
web_search "<tema> <fecha o 'news'>"
  -> verificar freshness (que sea reciente)
  -> cruzar 2 medios si es importante
```

## Reglas

- **Verificar antes de responder** - no confiar en un solo snippet; leer la fuente si el dato importa (precios, fechas, specs - regla de Gonzo).
- **Prefiere el sitio oficial** para specs/APIs (docs oficiales sobre blogs).
- **Dedupe**: no repetir la misma info de varias fuentes; sintetizar una vez.
- **100% con nuestras herramientas** (DuckDuckGo key-free, web_fetch, browser) - sin APIs pagas.

## Limites

- No fusiona N providers automaticamente (solo tenemos DuckDuckGo key-free). La "fusion" es manual: buscar + leer + cruzar.
- Si en el futuro configuramos mas buscadores (Brave, Tavily), podriamos automatizar el fan-out como hace el plugin original.

## Related

- [Deep Research](../deepwiki): investigacion profunda de temas.
- [Knowledge Management](../knowledge-management): consolidar hallazgos de busquedas a la memoria.
