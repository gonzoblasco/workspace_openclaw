# Notas para después de la transición a Antigravity

**Creadas:** 2026-11-16
**Disparador:** Gonzo — *"deja notas de estos cambios para dentro de par de semanas cuando terminemos la transición a Antigravity"*
**Para leer cuando:** el programa `programa_adaptacion_openclaw_a_gemini.md` esté en Fase 5 (marcha blanca) o cerrado.

Dos decisiones se tomaron el 2026-11-16. Las dos sobreviven la migración, pero **no se portan solas**: cada una tiene un paso concreto que depende de qué soporte el runtime de Antigravity.

---

## 1. Docs se leen en markdown, no en HTML

### Qué se verificó (medido con curl, no de memoria)

Negociación de contenido: `Accept: text/markdown` devuelve el mismo documento ya limpio, con frontmatter de `title` / `url` / `description`.

| Sitio | HTML | Markdown | Ratio |
|---|---|---|---|
| `docs.anthropic.com` (models/overview) | 710.396 B | 29.196 B | **24,3x** |
| `nextjs.org/docs` (routing) | 801.243 B | 13.157 B | **60,9x** |
| `docs.github.com` (rest/repos) | 1.410.913 B | 91.287 B | **15,5x** |
| `platform.openai.com/docs` (reasoning) | 1.118.334 B | 70.357 B | **15,9x** |
| `developer.chrome.com` | 137.342 B | 137.342 B | no soporta |
| `developer.mozilla.org` | 178.392 B | 178.392 B | no soporta |

Alcanza con el header solo; no hace falta una URL `.md` ni un endpoint aparte. Ambos providers devuelven `Content-Type: text/markdown; charset=utf-8`.

`llms.txt` también existe y es más barato todavía cuando sólo se necesita el índice:

```
docs.anthropic.com/llms.txt         200   102.075 B
platform.openai.com/docs/llms.txt   200    45.959 B
```

### Dónde vive hoy

Regla agregada en `AGENTS.md` §3 (Reglas operativas). Es una regla de **lectura**, no de código: no hay script ni dependencia.

### Qué revisar en Antigravity

- [ ] **¿El `web_fetch` de Antigravity manda `Accept`?** Si no, o si no se puede configurar, la regla queda muerta aunque esté escrita. Verificar con una URL de las cuatro que soportan y mirar el `Content-Type` de vuelta.
- [ ] **¿Hay que portarla a `~/.agents/rules/02-kanam-operations.md`?** Las reglas de workspace se leen jerárquico en Antigravity, pero `~/.agents/rules/` es el lugar donde ya viven identity/user/operations. Si la regla tiene que aplicar fuera de este workspace, va ahí, no en `AGENTS.md`.
- [ ] **Criterio de aceptación:** pedir una doc que soporte markdown y confirmar en el log que llegó `text/markdown` y no `text/html`.

### El error que esta regla previene

Asumir que el servidor honró el header. Si no lo honra devuelve HTML con `200 OK` igual — el modo de falla es silencioso: te creés que optimizaste 24x y no cambiaste nada. Por eso el chequeo es sobre el `Content-Type`, no sobre el tamaño.

---

## 2. `modern-web-guidance` (GoogleChrome)

### Qué es

Skills con datos de compatibilidad de navegador para sacar a los agentes del JS legacy. Custodiado por los equipos de Chrome, Edge, Firefox y MDN.

- Repo: `github.com/GoogleChrome/modern-web-guidance` — 19.516 ★, pusheado 2026-11-16
- npm: `modern-web-guidance@1.0.1`, **cero dependencias**, sin `scripts` en `package.json`
- Corpus: **209 guides**, búsqueda **100% offline** (vectores cuantizados `i8` + `guides.json` bundleado; el binario no tiene un solo `fetch`)

Comandos: `search "<query>"`, `retrieve "<id>"`, `legacy-scan <path>`.

### Resultado del test (2026-11-16, aislado en `forks/mwg/`)

Corrido sobre `projects/preflight` (38 de 209 guides con reglas determinísticas, ~20% del corpus). **2 findings, ambos reales — verificados a mano:**

1. `src/lib/scan.ts:111` — `AbortController` + un único `setTimeout(() => controller.abort())`. El `controller` no se aborta desde ningún otro lado (verificado con grep: sólo el `setTimeout` y un `signal.aborted` de lectura). Reemplazable por `AbortSignal.timeout(TOTAL_BUDGET_MS)`.
2. `src/lib/fix-prompt.ts:45` — `[...input.steps].sort(...)` sobre un array tipado. Reemplazable por `toSorted()`. Aplica el criterio "Drop when: spread sobre iterable no-Array" y no cae en él.

**Lo que hace bueno al scanner:** cada finding trae criterios `Keep when` / `Drop when` explícitos y avisa que el análisis estático es provisorio. No es lint que grita: te dice cuándo el finding es un falso positivo.

**Lo que hay que saber antes de adoptarlo:** el binario declara telemetría anónima de Google, opt-out con `DISABLE_TELEMETRY=1`. En el test se corrió siempre con esa variable. No hay endpoint de telemetría en el bundle (`grep` sobre el `.mjs` no encuentra ni `fetch` ni URL de analytics), pero la declaración está en el README y en el binario.

### Dónde vive (instalado el 2026-11-16)

Decisión: **vendorizado, no `npx` por llamada**. El bundle son ~15 MB (7,4 MB de vectores `query-words.i8`, 5,1 MB de `legacy-scan.mjs`), así que versionarlo en git no tiene sentido y `npx` por invocación paga red en cada consulta cuando la búsqueda ya es offline.

```
skills/modern-web-guidance/SKILL.md   wrapper fino (versionado)
scripts/mwg-install.sh                instalador pinned (versionado)
vendor/mwg/1.0.1/                     bundle real (~15 MB, gitignored)
```

`mwg-install.sh` verifica **integridad sha512 contra el registry** antes de extraer, y corta si no coincide. Reinstalar es borrar `vendor/mwg` y volver a correrlo.

### Qué revisar en Antigravity

- [x] **Instalación:** hecho acá, vendorizado y offline. En Antigravity es distinto: el paquete ya trae `.agents/plugins/marketplace.json` (además de `.claude-plugin`, `.codex-plugin`, `.cursor-plugin` y `.gemini-extension.json`), así que allá se instala como **plugin**, no como skill vendorizada.
- [ ] **Ya hay una copia instalada como plugin de Antigravity:** `~/.gemini/config/plugins/modern-web-guidance-plugin` (con `plugin_data` en `~/.gemini/antigravity` y `~/.gemini/antigravity-cli`). Gonzo dijo que probablemente la borra. **Si se borra, no afecta a OpenClaw**: nuestro bundle vive en `vendor/mwg/` y no depende de ese path. Si se mantiene, hay dos copias del mismo corpus en disco — no rompe nada, pero conviene saberlo antes de preguntarse por qué `legacy-scan` da lo mismo desde dos lados.
- [ ] **`DISABLE_TELEMETRY=1` en el shell profile** de la Mac Mini. Hoy está en la línea de comando de cada invocación, que es frágil: una llamada sin la variable se escapa sin aviso.

### El criterio que se aplicó

El repo era desconocido salvo por el nombre. Se leyó **antes** de ejecutar: tarball bajado a `forks/mwg/`, 281 archivos inspeccionados, `package.json` verificado (cero deps, cero scripts), y el `.mjs` grepeado por `fetch` / `child_process` / `writeFile` / `spawnSync`. Recién después se corrió. Es la regla de `AGENTS.md` §1 sobre código de terceros, aplicada.

---

## Lo que NO se decidió (sigue abierto)

- Si `legacy-scan` pasa a ser un gate de pre-commit de los proyectos de frontend. Necesita más evidencia que un proyecto: correrlo sobre 2-3 más y medir falsos positivos.
- Si la regla de markdown se extiende a los fetch que hacen los proyectos, no sólo a los míos.
- Si la skill vendorizada se replica en Antigravity o se usa el plugin de allá. Son dos caminos válidos; tener las dos es duplicar 15 MB de corpus.

---

## Referencia cruzada

- Plan de migración: `programa_adaptacion_openclaw_a_gemini.md` (Fases 0-2 completas al 2026-11-16; faltan 3-5)
- Regla vigente: `AGENTS.md` §3 — Reglas operativas
- Skill: `skills/modern-web-guidance/SKILL.md` · instalador: `scripts/mwg-install.sh`
- Contexto de la decisión: sesión 2026-11-16 (Moltbook 2026-W47, item de docs en markdown + item de `modern-web-guidance`)
