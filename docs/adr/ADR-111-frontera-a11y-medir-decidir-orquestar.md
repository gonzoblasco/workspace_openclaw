# ADR-111: Frontera de accesibilidad — medir, decidir y orquestar son tres capas

**Fecha:** 2026-11-06
**Estado:** Aceptado
**Decisores:** Gonzo / The UI/UX Auditor
**Origen:** Roadmap v0.2, Fase 0.2 — "hoy hay dos caminos de accesibilidad compitiendo"
**Relacionado:** `scripts/a11y-scan.mjs` (medición a11y con axe-core, 2026-10-06), ADR-100 (fuente única), ADR-110 (disparadores del Critic), `ROADMAP.md` del auditor (red line "el pipeline no fabrica verde")

---

## Contexto

El workspace tiene hoy tres piezas que tocan accesibilidad y ninguna declara su borde:

| Pieza | Qué hace | Dónde corre |
|---|---|---|
| `scripts/a11y-scan.mjs` | axe-core sobre una URL o archivo; `classify()` puro y testeado; exit 2 si falta infra | `tests/node/`, uso manual; CI no lo corre con browser |
| `agents/kanam-auditor/skills/accessibility-oracle` | axe + teclado + foco + target-size, multi-ruta, reportes HTML/JSON, screenshots | local, con app levantada |
| `scripts/check-a11y-trigger.py` | Decide **cuándo** un cambio exige validación manual con AT (VoiceOver/NVDA) | pre-commit y CI (`.github/workflows/skills-ci.yml`) |

La lectura fácil es "hay duplicación, unifiquemos en uno". Es la lectura equivocada: las tres
hacen cosas distintas y fusionarlas destruiría la propiedad más valiosa de cada una.

- `a11y-scan.mjs` vale por su **costo cero de dependencias**: resuelve `playwright-core` del
  OpenClaw que ya viaja con el gateway. Es lo único que puede correr en un runner sin instalar
  100MB de browser.
- `oracle` vale por su **cobertura**: multi-ruta, teclado, foco visible, evidencia visual. Es lo
  que un humano mira para arreglar algo.
- `check-a11y-trigger.py` vale por ser **política, no medición**: un grep no distingue "toca el
  anuncio" de "toca ARIA", y por eso avisa en vez de bloquear cuando corresponde.

## Decisión

Se separan tres capas con dueños distintos. Ninguna capa invade a la otra.

```
┌─ Capa 3 · ORQUESTACIÓN ────────────────────────────────┐
│  audit-surface (surface-pipeline)                      │
│  Único punto de entrada que emite VEREDICTO.           │
│  Consume capas 1 y 2; no mide por su cuenta.           │
└────────────────────────────────────────────────────────┘
              ▲                              ▲
┌─ Capa 2 · POLÍTICA ──────────┐  ┌─ Capa 1 · MEDICIÓN ──────────────┐
│ check-a11y-trigger.py        │  │ oracle  (auditoría completa)     │
│ ¿Cuándo exijo validación     │  │ a11y-scan.mjs (probe mínimo,     │
│ manual con AT?               │  │   cero deps, CI/local rápido)    │
│ No mide. Decide.             │  │ Ambos miden con axe-core.        │
└──────────────────────────────┘  └──────────────────────────────────┘
```

Reglas que se derivan:

1. **Medición vs política.** `check-a11y-trigger.py` no mide accesibilidad: decide cuándo la
   medición automática no alcanza. Por eso no se fusiona con `oracle`.
2. **Un solo orquestador.** Si una pieza emite veredicto, es `audit-surface`. `a11y-scan.mjs`
   emite exit code para su propio consumidor (un test), no un veredicto de superficie.
3. **Dos medidores, un dueño de reglas.** `oracle` y `a11y-scan.mjs` usan la misma fuente de
   reglas (axe-core). No se permite un tercer medidor con otro motor sin pasar por este ADR.
4. **El costo manda la lane.** `a11y-scan.mjs` es la lane barata (CI sin browser); `oracle` es la
   lane profunda (local o CI con app levantada). No se instala Playwright en CI para reemplazar
   lo que ya corre sin él.
5. **Ninguna capa simula.** Si `oracle` no puede levantar la app, falla explícito; no reporta
   "0 violaciones". Es la red line del ROADMAP.

## Consecuencia operativa inmediata

- `accessibility-oracle` **no** absorbe a `a11y-scan.mjs` (revisión de la recomendación inicial:
  absorberlo obligaría a instalar Playwright en la lane que hoy no lo necesita, y a perder
  `classify()` como función pura testeada sin browser).
- `.kanam/pipeline.config.yaml` deja `accessibility-oracle` como stage opcional (`--only`), no
  como parte del gate de PR. En CI corre solo `design-system-enforcer`.
- Cualquier propuesta futura de "unificar a11y" tiene que responder qué pasa con el costo de
  dependencias de la lane barata.

## Alternativas rechazadas

| Alternativa | Por qué no |
|---|---|
| Que `oracle` absorba `a11y-scan.mjs` (recomendación inicial) | Mete Playwright + @axe-core/playwright en la lane de CI que hoy corre con cero deps, y convierte `classify()` (puro, testeable sin red) en código acoplado al browser |
| Que `a11y-scan.mjs` absorba `oracle` | Pierde multi-ruta, teclado, foco, target-size y evidencia visual: es un downgrade de cobertura |
| Fusionar `check-a11y-trigger.py` con la medición | Política y medición tienen insumos distintos (diff vs DOM). Fusionarlas obliga a correr un browser para decidir si hace falta un humano |
| Un cuarto medidor "mejor" | Tres ya es suficiente. El problema era el borde, no la cantidad |

---

_Un borde claro no es burocracia: es lo que permite que tres piezas se sumen en vez de competir._
