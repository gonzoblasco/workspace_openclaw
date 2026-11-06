# Veredicto SHARP - `docs-ROADMAP-madurez`

**Fecha:** 2026-11-06 · **Sujeto:** `docs/ROADMAP.md` (el mapa de madurez del sistema)
**Emisor:** `ollama/minimax-m3.1-flash:cloud` (Critic, sesion principal) - **desviacion declarada**: el rol declara `gpt-oss:120b-cloud` como primario (ADR-090). Ver friccion F8 en `agents/kanam-critic/memory/frictions.jsonl`.
**Rubrica:** `.knowledge/SHARP.md` · **Total:** 15/25 -> **VETO** (13-18 = Funcional, deuda registrada)

> **Por que este sujeto.** Gonzo eligio `docs/ROADMAP.md` (madurez del sistema) como segundo
> veredicto sobre trabajo **ajeno** al Critic: hasta ahora solo me audite a mi mismo, y medir
> la tasa de absorcion con auto-correccion es la metrica mas facil del mundo.

## Snapshot

| Pieza | Ubicacion |
|---|---|
| Documento evaluado | `docs/ROADMAP.md:1` |
| Checklist de mantenimiento que el doc declara | `docs/checklists/roadmap-review-checklist.md:1` |
| Indice de roadmaps de rol (fuera de este doc) | `docs/ROADMAPS.md:1` |
| Norte del sistema | `docs/NORTH.md:1` |
| Tracker de busqueda laboral (fuente declarada) | `docs/entrevistas/_general/job-search-tracker.md:1` |

## Evidencia mecanica (corrida real del 2026-11-06)

### 1. El doc dice "revisado 2026-10-06"; el ultimo commit que lo toco es de octubre 23

```
$ git log -1 --format="%h %ad %s" --date=short -- docs/ROADMAP.md
9bc945aca9 2026-10-23 docs(oss): radar de oportunidades OSS medido + roadmap 2.2 actualizado
```

### 2. La tabla de bootstrap (linea 46-55) ya no coincide con el disco

```
$ python3 scripts/check-bootstrap-budget.py
OK: 5 archivos de bootstrap bajo cap; total 48714/60000.
 AGENTS.md=19992/20000(+8)  MEMORY.md=18680/20000(+1320)  USER.md=3884/4000(+116)  SOUL.md=2915/20000(+17085)  IDENTITY.md=3243/20000(+16757)
```

El doc declara `AGENTS.md` = 18.798 con **+1.202** de margen (`docs/ROADMAP.md:50`). El valor
real es **19.992 con +8 caracteres de margen**: 8 caracteres de margen en un archivo que se
inyecta en cada arranque. El propio cap esta a un par de lineas de truncar en silencio.

### 3. El estado de busqueda laboral del doc esta desactualizado frente a su propia fuente

```
$ grep -n "procesos vivos" docs/entrevistas/_general/job-search-tracker.md
3:> **Estado 2026-10-28: 3 procesos vivos (Mercor/Project Odin nuevo, Infjini/Disney con entrevista en noviembre, TEAM International con reevaluación prometida).**
```

El doc afirma en `docs/ROADMAP.md:171` "**No hay procesos abiertos: todos cerrados**" y en
`docs/ROADMAP.md:168` lo llama "CORRECCIÓN MAYOR". La fuente de verdad que el propio doc declara
(`docs/entrevistas/_general/job-search-tracker.md`) dice **3 procesos vivos** al 2026-10-28, y
ademas registra un funnel nuevo verificado el 2026-11-06. La "corrección mayor" del doc es ella
misma un estado viejo presentado como verdad.

### 4. Otros numeros del doc contra el disco

| Afirmacion del doc | Ubicacion | Medido |
|---|---|---|
| "27 skills en el arbol del workspace" | `docs/ROADMAP.md:198` | **113** `SKILL.md` en el arbol (34 en `skills/`, 84 en `agents/*/skills/`) |
| "0 de 21 proyectos con hook" | `docs/ROADMAP.md:121` | `projects/` tiene **6** directorios y **1** con `pre-commit` instalado |
| "git status muestra solo M memory/memory.db y M memory/todos.md" | `docs/ROADMAP.md:73` | Hoy hay cambios en `agents/kanam-dev/`, `agents/kanam-studio/`, `studies/design/` y 4 archivos sin trackear |

### 5. Que si esta bien

- El gate existe y esta cableado: `scripts/check-roadmaps.py` pasa **7/7 roles OK**, y
  `scripts/check-single-source.py` incluye `docs/ROADMAP.md` en su corpus normativo. La regla
  "una regla sin guarda se viola sola" esta resuelta en la forma.
- El doc tiene senal de listo por item, un checklist de mantenimiento real
  (`docs/checklists/roadmap-review-checklist.md:1`) y una regla de estado explicita ("un item solo
  pasa a 🟢 con evidencia de la señal de listo").
- La correccion historica que hizo (el falso "OFERTA ACEPTADA") fue un trabajo serio y bien
  documentado: el doc sabe auditarse a si mismo cuando se lo propose.

## Los 5 ejes

| Eje | Puntaje | Causa con ubicacion |
|---|---|---|
| **S - Sharpness** | **3** | El doc es preciso en su forma (señal de listo, checklist, estado por item) pero **los numeros que declara son falsos hoy**: `AGENTS.md` dice 18.798/+1.202 y mide 19.992/+8 (`docs/ROADMAP.md:50`), "27 skills" son 113 (`docs/ROADMAP.md:198`), "21 proyectos" son 6 (`docs/ROADMAP.md:121`). Un mapa de madurez con la tabla desactualizada es peor que uno sin tabla: se lee como verdad y no lo es. |
| **H - Horizon** | **3** | La estructura de tramos, prioridades y señales es la correcta y prepara la etapa siguiente. Pero el doc **no menciona al Crew**: `docs/ROADMAPS.md:27` define la vision v1.0 "El Crew como estandar" y `docs/NORTH.md` da la Etapa 3 por completada, y este roadmap del sistema no tiene ni una linea sobre el rol de calidad. El mapa que decide que va primero no ve la capa que se acaba de integrar. |
| **A - Asymmetry** | **3** | Mucha superficie (5 capas, 12 items, ~200 lineas) para un documento cuyo trabajo real es el estado. El mantenimiento es manual: el checklist existe pero **nada lo dispara** (no hay gate de contenido que verifique `docs/ROADMAP.md` contra las fuentes reales). El costo de upkeep ya se ve: 5 semanas de deriva en 4 numeros. |
| **R - Resistance** | **2** | Este es el eje que falla: el doc declara su propio protocolo ("la revisión se hace **contra fuentes reales**, nunca contra lo que creíamos recordar", `docs/ROADMAP.md:5`) y **no hay ningun gate que lo verifique**. El unico guard (`scripts/check-roadmaps.py`) mira la **existencia y la version** de los roadmaps de rol, no el contenido de este doc. Resultado medido: el margen real de `AGENTS.md` es de 8 caracteres y el doc sigue anunciando +1.202. Un protocolo escrito sin enforcement es exactamente el defecto que ADR-083 prohibe. |
| **P - Parsimony** | **4** | Es un documento de capa, no un backlog: delega la lista de tareas a `memory/memory.db`, el para-que a `docs/NORTH.md`, el ecosistema a `docs/ecosystem/DECISIONS.md`, y las skills al indice de roles. No repite datos que tienen dueno. Los 3 puntos se pierden en el exceso de historia inline y en numeros que yenquen. |

## Veredicto

**15/25 -> VETO.** El doc tiene la forma correcta y los gates de existencia, pero **es el mapa
del sistema y hoy miente en 4 numeros verificables**, uno de los cuales (`AGENTS.md` con 8
caracteres de margen) es el mas caro del workspace. El doc se audito a si mismo cuando un
falso "oferta aceptada" lo obligo, y no se audito desde el 23 de octubre.

## Puntos de friccion obligatorios

| # | Eje | Causa | Ubicacion | Ajuste concreto |
|---|---|---|---|---|
| **F1** | Resistance | El protocolo de revision contra fuentes reales no tiene enforcement: ningun gate verifica el contenido de `docs/ROADMAP.md` | `docs/ROADMAP.md:5` | Agregar `scripts/check-roadmap-facts.py` que relea las fuentes (presupuesto de bootstrap, conteo de skills, cantidad de proyectos, estado del tracker) y falle si el doc declara un numero que no coincide. Con la salida del check pegada en el doc, la deriva se ve en el commit |
| **F2** | Sharpness | La tabla de bootstrap esta desactualizada y esconde un margen real de 8 caracteres | `docs/ROADMAP.md:46-55` | Regenerar la tabla con `python3 scripts/check-bootstrap-budget.py` (hoy: `AGENTS.md=19992/20000(+8)`) y, si el margen es menor a 500 caracteres, bajar `AGENTS.md` en vez de dejarlo al borde |
| **F3** | Sharpness | El estado de busqueda laboral esta desactualizado frente a su propia fuente de verdad: el doc dice "todos cerrados" y el tracker dice 3 procesos vivos | `docs/ROADMAP.md:168-171` vs `docs/entrevistas/_general/job-search-tracker.md:3` | Releer el tracker y reescribir el estado; la "correccion mayor" del doc es ella misma un estado viejo |
| **F4** | Sharpness | Numeros del doc que no coinciden con el disco: "27 skills" (son 113), "21 proyectos" (son 6), `git status` con solo 2 archivos modificados | `docs/ROADMAP.md:198`, `docs/ROADMAP.md:121`, `docs/ROADMAP.md:73` | Medir y reescribir, o borrar el numero y dejar el comando que lo produce (el comando no se pudre; el numero si) |
| **F5** | Horizon | El mapa del sistema no menciona al Crew, que ya es Etapa 3 completada y tiene vision v1.0 declarada | `docs/ROADMAPS.md:27`, `docs/NORTH.md` | Agregar el rol de calidad al mapa del sistema como capa o item con su señal de listo (veredicto invocable por otros agentes) |

## Lo que NO hago

No toco `docs/ROADMAP.md`: es del CORE y sus fricciones son suyas para cerrar. Este veredicto
es el insumo, no la edicion. El unico cambio que hago en el turno es la creacion de este reporte.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
