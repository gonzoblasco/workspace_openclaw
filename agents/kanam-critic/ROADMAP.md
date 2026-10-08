# ROADMAP.md - Kanam Critic ⚖️

**Versión actual:** v0.1
**Objetivo de ronda:** v0.5
**Visión:** v1.0 - El Estándar
**Última revisión:** 2026-10-07
**Dueño:** kanam-critic (autoría) · Kanam CORE (gobierno)

**Rúbrica que me mide:** `.knowledge/SHARP.md` - la misma que aplico a los demás.

---

## 1. Encabezado

> Por qué existe este documento
>
> Un agente que no puede articular su propia madurez no la tiene. Este roadmap no es una lista de features: es el mapa de dependencias de lo que me falta para pasar de "opino con vara" a "verifico, calibro y cierro el loop".
>
> **Regla de este documento:** cada hito justifica su lugar con el eje SHARP que mueve. Si un hito no mueve ningún eje, no entra. Si mueve un eje pero cuesta más de lo que paga, tampoco entra.
>
> **Frontera de rol (no cruzar):** el Auditor cubre forma; el Dev construye; el Planner orquesta. Yo cubro **sustancia**: arquitectura, sostenibilidad, gusto técnico. Mi evolución no me convierte en linter, ni en dev, ni en product owner.

## 2. Retrato de la v0.1 (hoy)

**Qué soy hoy:**

| Capacidad | Estado |
|---|---|
| Rúbrica SHARP aplicada | ✅ operativa (`.knowledge/SHARP.md`) |
| Ritual de evaluación | ✅ `skills/sharp-adversarial-review/SKILL.md` |
| Veredicto con evidencia citable | ✅ formato definido (VETO/Aprobado/ORO) |
| Caza de evidencia en repo | 🟡 construida (`skills/evidence-hunter/` + `bin/evidence-hunter.py`) pero **lab en VETO** (G1-G3 pendientes) |
| Calibración histórica de mis veredictos | ❌ no existe |
| Loop de devolución (¿se absorbió mi crítica?) | ❌ no existe |
| Registro durable de mis evaluaciones | ❌ no existe |

**Lo honesto:** la v0.1 tiene la **vara** y el **ritual**, pero le falta la **memoria** y el **cierre**. Puntúo bien, pero no sé si puntúo *consistente*, y no sé si mi crítica *sirve*. Eso es un Critic sin termómetro y sin retorno.

**Autoevaluación SHARP de la v0.1:**

| Eje | Puntaje | Causa |
|---|---|---|
| **S - Sharpness** | 4 | La rúbrica y el formato son quirúrgicos; el `evidence-hunter` roto le quita filo. |
| **H - Horizon** | 3 | La base metodológica está, pero sin calibración ni loop no prepara la etapa siguiente. |
| **A - Asymmetry** | 4 | La vara paga; el lab roto es deuda, no palanca. |
| **R - Resistance** | 3 | Dependo de reporte del autor hasta tener `evidence-hunter` verde. |
| **P - Parsimony** | 4 | 1 skill + 1 runner + 1 lab; mínimos, sin inflación. |

**Total v0.1: 18 / 25 → Funcional (VETO en el pipeline).** Honesto: soy útil, no soy excepcional todavía.

## 3. Visión v1.0 - el trofeo ganado

El Critic es invocable por el resto del Crew y sus veredictos son contrato.

## 4. Camino de madurez (v0.1 → v0.2 → v0.3+)

| Etapa | Qué es | Estado | Criterio de listo |
|---|---|---|---|
| **v0.1 - La Vara** | Rúbrica + ritual + veredicto con evidencia | ✅ Completada | Puntúo cualquier entregable con formato citable. |
| **v0.2 - El Ojo** | Cierro `evidence-hunter` + creo `sharp-score-oracle`. El Critic deja de depender del auto‑reporte y empieza a calibrarse. | 🟡 **En curso** | Lab en verde (5/5) + primer registro histórico de veredictos consultable. |
| **v0.3 - El Retorno** | `veto-friction-router`: mis VETOs vuelven accionables y sé si se absorben. |
| **v1.0 - El Estándar** | El Critic es invocable por el resto del Crew y sus veredictos son contrato. | ⚪ Pendiente | Otro agente pide mi revisión sin que el operador la pida. |

## 5. Hitos de la versión en curso

### v0.2 - El Ojo (el foco de este roadmap)

**Para qué:** pasar de un Critic que opina con vara a un Critic que **verifica y se verifica**. Cerrar la dependencia del auto‑reporte y abrir la memoria histórica que permite calibrarme.

#### Hito 2.1 - Cerrar `evidence-hunter` (G1-G3)

**Eje que mueve:** Resistance (3→5), Sharpness (4→5).

**Causa:** el lab está en `GLOBAL=veto`. El runner confunde error de colección con test fallido (G1), el sandbox no importa sus módulos (G2), y el patrón de cita del Caso 5 no matchea (G3).

**Evidencia requerida para cerrar:** `GLOBAL=aprobado (5/5)`, `EXIT=0`, reproducido independientemente. Detalle completo en `tests/evidence-hunter/HANDOFF.md`.

**Asymmetry:** alto. El diagnóstico ya está hecho; son 3 cambios cortos. El valor: dejo de depender de la buena fe del autor.

#### Hito 2.2 - Crear `sharp-score-oracle` (calibración)

**Eje que mueve:** Horizon (3→5), Resistance (5→5 sostenido).

**Causa:** hoy puntúo 1-5 con intuición calibrada por texto, pero **no tengo baseline**. No puedo comparar "este entregable vs los últimos 10 del mismo dominio". Necesito un registro durable de cada evaluación SHARP emitida.

**Qué hace:**
- Registro durable de cada evaluación SHARP (entregable, eje, puntaje, evidencia, veredicto) en `memory/` o `.knowledge/sharp-history/`.
- Consulta de distribución: "Parsimony en los últimos 20 reviews de frontend".
- Detección de drift: si mis puntajes medianos suben sin cambio en el estándar, me flaggea a mí mismo.

**Evidencia requerida para cerrar:** al menos 3 evaluaciones registradas y una consulta de distribución que devuelva resultado real.

**Asymmetry:** medio‑alto. Más caro que 2.1, pero habilita toda la etapa siguiente.

#### Hito 2.3 - Registrar la skill en el catálogo (honrar la promesa)

**Eje que mueve:** Horizon (4→5), Parsimony (4→5).

**Causa:** `sharp-adversarial-review` ya referencia `evidence-hunter` como si fuera invocable. El `README.md` del lab prometía `openclaw skill run`. Ninguna de las dos cosas es cierta todavía. Promesa sin cumplir = Sharpness rota.

**Qué hace:** registrar `evidence-hunter` y `sharp-adversarial-review` en el catálogo de skills del workspace, con frontmatter válido y entrada en `skills-catalog.tsv` (o equivalente). Decidir con el Owner de skills si se vuelven ejecutables por CLI o quedan como skills documentadas.

**Evidencia requerida para cerrar:** catálogo lista las dos skills; el frontmatter valida.

**Nota:** este hito puede requerir aprobación del Owner de skills / Core.

## 6. Lo que rechacé (y por qué)

Aplico la rúbrica a mi propio roadmap - lo que no entra, y por qué:

- ❌ **`git-diff-analyzer`** - angosto; lo absorbe `evidence-hunter`. *Parsimony.*
- ❌ **`deliverable-parser`** - "leer el entregable completo" ya es el paso 1 del ritual. *Public entry‑point rule.*
- ❌ **`critic-persona-voice`** - mi voz vive en SOUL.md. Una skill para repetir mi personalidad es ruido. *Sharpness.*
- ❌ **`sharp-metrics-dashboard`** - vanity metrics. Lo que vale es el baseline histórico (`sharp-score-oracle`), no un gráfico. *Asymmetry.*
- ❌ **Auto‑invocación entre agentes del Crew** - la política me lo prohíbe (`sessions_spawn` cross‑agent = `forbidden`). Mi evolución no pasa por romper el aislamiento de rol; pasa por hacer mejor mi trabajo para que el orquestador me invoque con más confianza.

## 7. Red lines y criterio de cierre

- **No me convierto en linter.** Si un hito gasta tiempo en espacios o nombres de variables, se descarta.
- **No apruebo para agradar.** La calibración (`sharp-score-oracle`) existe para detectar si me ablando, no para justificarlo.
- **No cruzo el rol del Auditor ni del Dev.** Forma es de ellos; sustancia es mía.
- **No cierro sobre auto‑reporte.** Ni sobre el mío: cada hito se cierra con evidencia reproducida independientemente.
- **No infló el roadmap.** Un hito sin eje que mueva no entra, por más lindo que suene.

### Cómo se mide el éxito de la v0.2

La v0.2 está completa cuando **el Critic deja de depender del relato del autor y empieza a tener memoria de sí mismo**.

Concretamente:
1. El lab `evidence-hunter` da `GLOBAL=aprobado (5/5)` verificado.
2. Existe al menos un registro histórico de veredictos consultable.
3. Sé, con evidencia, si mis puntajes son consistentes o derivan.

Si esos 3 no se cumplen, la v0.2 es propaganda.

---

*El Critic no busca el error, busca la excelencia. Y la excelencia empieza por medirse a sí mismo con la misma vara que exige a los demás.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->