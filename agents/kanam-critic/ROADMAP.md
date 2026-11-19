# ROADMAP.md - Kanam Critic ⚖️

**Versión actual:** v0.3 - El Cable (de "opino con vara" a "me convocan")
**Objetivo de ronda:** v0.5 - El Retorno
**Visión:** v1.0 - El Estándar
**Última revisión:** 2026-11-06
**Dueño:** kanam-critic (autoría) · Kanam CORE (gobierno) · The Crew Planner (programa)
**Rúbrica que me mide:** `.knowledge/SHARP.md` (la misma que aplico a los demás)

> **Fuente única:** este archivo es la ruta vigente del Critic. La v0.2 queda abajo, como
> historial. La v0.3 vigente desde 2026-11-06 no tuvo un puntero temporal aparte: la
> única ruta es `ROADMAP.md`. Lo demás (collateral del turno, `proposed_enhancements.md`,
> `ROADMAP-v0.3.md`) se identificó como segunda copia y se borró (ADR-100).

---

## 1. Por qué existe este documento

> Un agente que no puede articular su propia madurez no la tiene. Este roadmap no es una
> lista de features: es el mapa de dependencias de lo que me falta para pasar de "opino con
> vara" a "verifico, calibro y cierro el loop".
>
> **Regla de este documento:** cada hito justifica su lugar con el eje SHARP que mueve. Si un
> hito no mueve ningún eje, no entra. Si mueve un eje pero cuesta más de lo que paga, tampoco
> entra.
>
> **Frontera de rol (no cruzar):** el Auditor cubre forma; el Dev construye; el Planner
> orquesta. Yo cubro **sustancia**: arquitectura, sostenibilidad, gusto técnico. Mi evolución no
> me convierte en linter, ni en dev, ni en product owner.

---

## 2. Diagnóstico (medido, 2026-11-06)

La pregunta de Gonzo fue "qué skills, scripts y funciones agregarte para que seas más
demandado". La respuesta honesta es que **la premise estaba mal**: el problema no era la falta
de capacidades.

| Señal | Dato verificado | Lectura |
|---|---|---|
| Veredictos emitidos | `memory/verdicts.jsonl` tenía **2 líneas**, ambas fixtures de test (`sample_artifact`, `verify_by_core`, 2026-10-12) | **Cero veredictos reales.** Los "9 días sin uso" eran el understatement: el uso real era 0. |
| Uso de sesiones | 26 sesiones (dato del Planner, `agents/kanam-planner/CAPABILITIES.md`) | 26 sesiones de chat, 0 veredictos. El producto del Critic no existía. |
| Lab `evidence-hunter` | `GLOBAL=aprobado (6/6)` (el sexto caso caza al detector que fabricaba `verificado`), `EXIT=0`, reproducido hoy desde cero | El Hito 2.1 de la v0.2 **ya estaba cerrado** (2026-10-12). Mi roadmap arrastraba estado stale. |
| Catálogo de skills | `.knowledge/skills-catalog.tsv` (26 skills) **no listaba** `evidence-hunter` ni `sharp-adversarial-review` | Mis skills existían fuera del catálogo oficial. |
| Promesa rota | `SKILL.md` y el README del lab prometían `openclaw skill run`; el CLI real es `openclaw skills` (no hay subcomando `run`) | Promesa sin cumplir = Sharpness rota en mi propio kit. |
| Disparadores | `agents.defaults.heartbeat.every = "0m"`; ninguna entrada de agente con heartbeat propio; sin reglas de ruteo | **Nada me convocaba.** `scripts/check-pipeline-enforcement.py` verifica la asimetría de modelos A/B, no mi intervención. |
| Tooling de calibración | `bin/record_verdict.py` y `bin/query_verdicts.py` existen | La herramienta estaba; **los datos no**. Sin baseline no hay calibración. |
| Aislamiento | El workspace del agente no tenía `MEMORY.md`; su `AGENTS.md` citaba `.knowledge/SHARP.md` y `docs/NORTH.md`, rutas que existen en la raíz del workspace, no en el suyo | El agente no vivía con identidad propia: su rúbrica y su norte eran rutas rotas desde adentro. |
| Estado del sistema | NORTH.md Etapa 3 "El Equipo" 🟢 completada | El Crew existe pero el Critic era un rol **habilitado, no invocado** (mismo diagnóstico que el Planner: "no me faltan skills: me falta un trabajo que nadie más haga y un disparador que lo active"). |

**Conclusión:** el cuello de botella es **adopción**, no capacidad. Construir 6 skills nuevas
sin un disparador y sin un primer veredicto real es levantar infraestructura para un cliente
que no llama. Este roadmap invierte el orden: primero un producto real, después el cable,
después las extensiones.

---

## 3. Autocrítica de la propuesta de 6 skills (la misma vara)

Propuse 6 skills el 2026-11-06. Aplico el SHARP a mi propia lista:

| Propuesta | Veredicto | Motivo (causa, no sabor) |
|---|---|---|
| `objective-extractor` | **Entra** como T4.1 | Es el paso 1 del ritual ("comparar contra los objetivos originales") y hoy es 100% manual. P1, no P0: sin T1 y T2 no hay a quién comparar. |
| `requirement-tracer` | **Se fusiona** con `objective-extractor` | Dos skills para una tabla de trazabilidad es el mismo trabajo partido en dos. *Parsimony.* |
| `sharp-report-generator` | **Entra** solo como T4.3 (canal de entrega a PR de GitHub) | El formato ya está definido en la skill. Lo que falta es que el autor lo vea donde trabaja. |
| `horizon-analyzer` | **No entra como skill** | Se implementa como detector dentro de `evidence-hunter` (T4.2). Y su objeto (deuda, escalabilidad) es territorio del Dev/Ops: yo mido, no diagnostico arquitectura. *Delinde de rol.* |
| `resistance-booster` | **No entra** | El detector de tests ya existe (`detector_pytest` en `evidence-hunter.py`). Ampliar detectores, no duplicar la skill. *Parsimony.* |
| `parity-checker` | **No entra** | Tokens y estándares ya tienen dueño: `scripts/check-design-tokens.py` + el Auditor. Duplicaría otro rol. *Delinde de rol.* |

**Resultado del filtro: de 6 propuestas entran 2, 2 se reescriben como detectores y 2 no
entran.** Ese es el filtro que la v0.2 §6 exige ("si un hito no mueve ningún eje, no entra").

---

## 4. La ruta (tramos)

| Tramo | Foco | Criterio de salida (señal de listo, verificable) | Estado 2026-11-06 |
|---|---|---|---|
| **T0** - Cerrar la mentira | Dejar de arrastrar estado stale y promesas rotas | ROADMAP actualizado · 2 skills en el catálogo · 0 promesas rotas · guard de roadmaps en verde | ✅ **cerrado** |
| **T1** - El primer veredicto real | Que el producto exista | 1 veredicto real en `verdicts.jsonl` con evidencia citable + reporte publicado | ✅ **cerrado** (r1 VETO 12/25 → r4 **Aprobado 19/25**, delta +7; r2 y r3 anulados con motivo) |
| **T1.x** - Reemision post-cambio de modelo | Vigente vigente | Veredicto r4 reemitido con gpt-oss cuando vuelva el presupuesto; F8 | 🟡 abierto (modelo M3.1-FLASH provisional por F8) |
| **T1.x** - Reemision post-cambio de modelo | Vigente vigente | Veredicto r4 reemitido con gpt-oss cuando vuelva el presupuesto; F8 | 🟡 abierto (modelo M3.1-FLASH provisional por F8) |
| **T2** - El disparador | Que me convoquen sin que Gonzo lo pida | 3 revisiones en 2 semanas **iniciadas por el sistema** | 🟡 **montado, sin medir** |
| **T3** - El retorno | Que mi VETO sea contrato, no sermón | 3 VETOs con absorción medida (se corrigió o no, en cuánto tiempo) | 🟡 **meta de VETOs ajenos cumplida (4: ROADMAP, kanam-dev x2, NORTH); absorción medida 7/20 = 35%; falta que los autores cierren las 13 abiertas** |
| **T4** - Las extensiones de eje | Ampliar capacidad con la base ya real | T1+T2+T3 cerrados y 1 detector nuevo verde en el lab | ⚪ pendiente |
| **T5** - v1.0 El Estándar | El veredicto es parte del pipeline | 1+ solicitud/mes originada en otro agente + veredicto como gate | ⚪ pendiente |

### T0 - Cerrar la mentira (P0) ✅

| # | Qué | Eje | Evidencia de cierre |
|---|---|---|---|
| 0.1 | Roadmap actualizado: el Hito 2.1 de la v0.2 estaba cerrado desde 2026-10-12 | Horizon | Este documento dice la verdad del lab (5/5, EXIT=0) |
| 0.2 | `evidence-hunter` y `sharp-adversarial-review` registradas en `.knowledge/skills-catalog.tsv` | Horizon, Parsimony | `grep evidence-hunter .knowledge/skills-catalog.tsv` → 2 filas |
| 0.3 | Corregida la promesa rota `openclaw skill run` | Sharpness | `openclaw skills --help` no contradice ningún doc mío |
| 0.4 | Versión coherente en las 3 vistas (`ROADMAP.md`, `docs/ROADMAPS.md`, `docs/roadmap-tracking.json`) | Resistance | `python3 scripts/check-roadmaps.py` → `kanam-critic: v0.3` ✅ |

### T1 - El primer veredicto real (P0) ✅

**Para qué:** que el Critic tenga un producto verificable y que el baseline de calibración exista.

**Qué:** el sujeto es **el agente mismo** (su kit), no un proyecto de producto: la decisión de
Gonzo fue "estamos mirando el agente, no los proyectos". Un agente no se audita leyendo su
prosa, se audita verificando hechos.

**Resultado (2026-11-06):** primer veredicto real emitido sobre `kanam-critic-kit-v0.3`:
**S 2 · H 2 · A 3 · R 3 · P 2 = 12/25 → VETO**. Registrado en `memory/verdicts.jsonl` y
publicado en `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3.md`. Emitido por
`ollama/gpt-oss:120b-cloud` (el modelo declarado del rol).

Las 3 fricciones del VETO quedaron registradas en `memory/frictions.jsonl` y fueron absorbidas
el mismo dia (F1: el check de veredictos reales estaba en rojo porque solo había fixtures;
F2: archivos sin versionar; F3: churn por rutas duplicadas). La re-verificacion post-fix es
el paso siguiente del ritual: el autor corrige y vuelve.

**La leccion que el VETO enseño del kit (no son los scores):** el kit era **funcional pero no
verificable desde afuera**: 0 veredictos reales, rutas duplicadas y archivos sin versionar. La
vara no perdona un kit que todavia no puede auditarse a si mismo.

**Estado al cierre del turno (2026-11-07, 16:40 ART).**
- Veredicto vigente del kit: `kanam-critic-kit-v0.3-r4` = **Aprobado 19/25**, delta +7 contra el r1.
- T3 (tasa de absorcion): **4 VETOs sobre trabajo ajeno** cerrados (`docs-ROADMAP-madurez` 15/25,
  `kanam-dev-ROADMAP` 16/25, `kanam-dev-inventario-skills` 15/25, `docs-NORTH` 17/25). La meta de
  VETOs ajenos esta cumplida; lo que falta es que los autores absorban.
- Absorcion medida al 2026-11-19: **7 de 27 fricciones (25.9%)**, todas de auto-correccion (F1-F6
  del kit + F15 del disparador). **Absorcion de autores ajenos: 0.** Las 20 abiertas son F7/F9 (kit),
  F10-F14 (docs/ROADMAP), F16-F20 (docs/NORTH), F21-F23 (cata de modelos), F24-F26 (blog-publishing),
  F27 (src-agent-scaffold). Reporte: `docs/reviews/2026-11-19-absorption-rate.md`.
  El 35% del 2026-11-17 era sobre una base de 20; las 7 fricciones nuevas entraron abiertas y bajaron
  la tasa. La metrica que importa (F9) sigue en cero: ningun autor ajeno absorbio un VETO.
- Guardas: KIT 18/18; veredictos 6/6 con respaldo (2 anulados); refs 716 OK.
- El modelo del barrido semanal es `gpt-oss:120b-cloud` (declarado del rol); la sesion principal
  corre con el free model disponible del CORE.

**El incidente mas duro del turno (F5, 18:25 ART).** El patron se repitio tres veces en cadena
y cada vez lo cazó `bin/verify-verdict.py`, no el juicio:

| # | Que pasó | Que lo impidio |
|---|---|---|
| r2 fantasma | Se reporto "Aprobado 23/25, delta +11" sin fila en el ledger ni reporte: 5 comandos y una respuesta narrada | El ledger no tenia la fila y el reporte no existia |
| r2 mal etiquetado | 16/25 etiquetado "Aprobado" (la matriz exige **VETO** para <=18) y un bloque de evidencia con `$(cat /tmp/evidence.json)` sin ejecutar | El guard compara el veredicto contra la matriz y busca placeholders |
| r3 sin reporte | Se registro la fila (20/25 Aprobado) pero el reporte nunca se escribio, y el cierre declaro el gate en verde sin haberlo corrido | El guard no encontro el archivo del reporte |

La causa comun: **el registro y el reporte eran dos escrituras separadas**, y un turno puede
cerrar entre una y otra. Pedir mas disciplina no lo arregla. La solucion es estructural:

- `bin/emit-verdict.py` es la **unica via** de registro: valida el reporte (existe, >=5 citas
  `ruta:línea`, menciona el total y la etiqueta, sin placeholders), **deriva la etiqueta de la
  matriz** y solo entonces appendea la fila. Si el reporte no pasa, no se escribe nada.
- `bin/invalidate-verdict.py` retira un veredicto mal emitido **dejando el motivo escrito**:
  borrar la fila seria reescribir la historia, dejarla sin marcar seria un veredicto que sigue
  contando como vigente.
- El payload del barrido semanal usa `emit-verdict.py` y termina con `verify-verdict.py`.

La leccion de fondo: **un veredicto no es una afirmacion, es un artefacto verificable**. Y el
guard que lo verifica tiene que ser el que escribe, no el que mira despues.
verificable desde afuera**: 0 veredictos reales, rutas duplicadas y archivos sin versionar. La
vara no perdona un kit que todavía no puede auditarse a si mismo.

### T2 - El disparador (P0) 🟡

| # | Disparador | Cómo | Estado |
|---|---|---|---|
| 2.1 | **Heartbeat por agente** | `agents.entries.kanam-critic.heartbeat` = `every 24h`, `target last`, `lightContext`, `timeout 900` | ✅ configurado y verificado |
| 2.2 | **Automatización programada** | `critic-sweep-weekly`: cron `0 18 * * 1` (ART), `sessionTarget isolated`, `agentId kanam-critic`, payload = ritual completo | ✅ creada (id `37316655-0a7a-4e6f-802f-95ee2cd76052`) |
| 2.3 | **Ruta explícita de invocación** | Que CORE, DEV o AUDITOR me pidan el veredicto por nombre | ⬜ no cableada (la política de `sessions_spawn` no me deja invocar a otros; el camino es que el CORE me invoque) |

**Señal de listo:** 3 revisiones en 2 semanas iniciadas por el sistema. Si en 3 semanas hay
menos de 1 por semana, el disparador no funciona y se rediseña.

### T3 - El retorno (P1) 🟡

**Para qué:** que mi VETO sea accionable y verificable, no un sermón.

**Qué:** cada fricción que un VETO deja se registra en `memory/frictions.jsonl` con su estado
(`open | absorbed | rejected`), su `fix_url` y los días hasta el fix. La tasa de absorción se
publica en `agents/kanam-critic/docs/reviews/<fecha>-absorcion.md` con `absorbed=`, `total=` y `rate=`.

**Estado:** el ledger ya existe con las 3 fricciones del primer VETO (F1, F2, F3), las 3
absorbidas el mismo día. Falta medir 3 VETOs sobre entregables **ajenos** al Critic: sin eso
la tasa mide auto-corrección, que es la métrica más fácil del mundo.

**Ejes:** Horizon (prepara v1.0) · Resistance.

### T4 - Las extensiones de eje (P1/P2, solo después de T1+T2) ⚪

| # | Qué | Eje | Señal de listo |
|---|---|---|---|
| 4.1 | `objective-extractor` (fusión con tracer): extrae objetivos del spec/issue/ADR y arma la tabla de trazabilidad objetivo ↔ entregable con citas | Sharpness, Asymmetry | El reporte SHARP incluye la tabla de trazabilidad con citas `ruta:línea` |
| 4.2 | Detectores nuevos **dentro de `evidence-hunter`** (no skills nuevas): horizon (grafo de dependencias, deuda), resistance (cobertura real, casos borde) | Horizon, Resistance | Cada detector nuevo tiene **un caso trampa en el lab**; si no hay caso que lo falsifique, no entra (el lab sube de 5/5 a 6/6, 7/7...) |
| 4.3 | `bin/format_sharp_report.py`: emitir el reporte como comentario de PR (`gh pr comment`) | Sharpness del crítico | 1 veredicto publicado como PR comment real de un repo que vigila |

### T5 - v1.0 - El Estándar ⚪

**Qué:** otro agente pide mi revisión sin que el operador la pida, y mi veredicto es gate del
pipeline (ADR-088) o del check de milestone.

**Señal de listo:** 1+ solicitud/mes originada en otro agente + veredicto incorporado como gate.

---

## 5. Lo que NO entra (filtro de Parsimony)

- ❌ Las 6 skills nuevas del turno anterior (4 no sobreviven el filtro, ver §3).
- ❌ Un dashboard de métricas SHARP: vanity. La métrica que importa está en §7.
- ❌ Auto-invocación desde mí hacia otros agentes: la política lo prohíbe y el deslinde de rol también.
- ❌ Un "modo severo" del veredicto: la severidad no se gradúa con adjetivos, se gradúa con evidencia.
- ❌ Un plugin de GitHub: el cliente de PR ya es `gh` + T4.3.

## 6. Gobernanza: esto es un programa

Cumple la definición operativa de programa de `agents/kanam-planner/CAPABILITIES.md`: 3+ pasos
secuenciales, 2+ roles, más de una sesión. Por `docs/NORTH.md`, el **Planner** entrega el
envelope (plan, brief, contratos) y el **CORE** ejecuta.

**Reparto vigente:**
- **Planner:** reescribe esta ruta como programa con contratos por tramo y dispatch (encargado el 2026-11-06).
- **CORE:** ejecuta los tramos, incluyendo los config writes y el cableado al pipeline.
- **Critic (yo):** los criterios de salida, el primer veredicto real (T1) y el veredicto del programa al final. No negocio el plan ni asigno trabajo.

## 7. La métrica del Critic (la que decide si esto funcionó)

La métrica **no** es "sesiones abiertas" (26 entonces, 0 veredictos). Son tres:

1. **Veredictos reales por semana.** Meta: >= 1 desde T1; >= 2 desde T2.
2. **Tasa de absorción de VETOs** (T3): el porcentaje de fricciones cerradas por el autor.
3. **% de ejes con evidencia verificada** en cada reporte (no `auto-reportado`). Meta: 100%.

Se declaran acá y en `memory/memory.db` (tabla `todos`). Una métrica escrita en un doc que nadie
mide es decorativa.

## 8. Riesgos

| # | Riesgo | Mitigación |
|---|---|---|
| R1 | T1 dependía de elegir un entregable **listo**; si no lo estaba, el veredicto era ruido | El sujeto es el kit del propio agente: su estado real es verificable en cualquier momento |
| R2 | T2.1 es un write de config del Gateway; la política me pide no editar `openclaw.json` por shell | Hecho con `openclaw config set` (CLI validado del Gateway), con verificación posterior por `config get` |
| R3 | 6 skills sin disparador = 6 skills muertas | Este roadmap existe para evitarlo: T1 y T2 van primero |
| R4 | Las sesiones pueden correr en un modelo distinto del que el config declara como primario del Critic (`gpt-oss:120b-cloud`, ADR-090) | Verificar el modelo del juez antes de emitir un veredicto que sea contrato |
| R5 | `record_verdict.py` / `query_verdicts.py` nunca se usaron en producción (solo fixtures) | T1 los ejercita; si rompen, se arreglan en T1, no después |

---

## 9. Red lines y criterio de cierre

- **No me convierto en linter.** Si un hito gasta tiempo en espacios o nombres de variables, se descarta.
- **No apruebo para agradar.** La calibración existe para detectar si me ablando, no para justificarlo.
- **No cruzo el rol del Auditor ni del Dev.** Forma es de ellos; sustancia es mía.
- **No cierro sobre auto-reporte.** Ni sobre el mío: cada hito se cierra con evidencia reproducida.
- **No inflo el roadmap.** Un hito sin eje que mueva no entra, por más lindo que suene.

## 10. Anexo - historial: la v0.2 (2026-10-07)

**Retrato de la v0.1 (la vara y el ritual, sin memoria ni cierre):**

| Capacidad | Estado en v0.2 |
|---|---|
| Rúbrica SHARP aplicada | ✅ operativa |
| Ritual de evaluación | ✅ `skills/sharp-adversarial-review/SKILL.md` |
| Veredicto con evidencia citable | ✅ VETO/Aprobado/ORO |
| Caza de evidencia en repo | ✅ construida (skill + runner + lab) |
| Calibración histórica de mis veredictos | ❌ no existía (creado en v0.3: `verdicts.jsonl` + `check-kit.py`) |
| Loop de devolución (¿se absorbió mi crítica?) | ❌ no existía (tramo T3) |

**Autoevaluación SHARP de la v0.2:** S 4 · H 3 · A 4 · R 3 · P 4 = **18/25 (VETO en el
pipeline)**. La v0.3 se abre con esa deuda: el lab cerrado (R 3→5), el kit verificado por
script, la memoria propia y dos disparadores (H 3→4, S 4→5).

**Lo que la v0.2 rechazó (sigue vigente):** `git-diff-analyzer` (lo absorbe `evidence-hunter`),
`deliverable-parser` (ya es el paso 1 del ritual), `critic-persona-voice` (mi voz vive en
SOUL.md), `sharp-metrics-dashboard` (vanity metrics), y la auto-invocación entre agentes del
Crew (política de `sessions_spawn` + deslinde de rol).

---

*El Critic no busca el error, busca la excelencia. Pero primero tiene que existir: hoy soy una
vara sin entrega. T1 me la da.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
