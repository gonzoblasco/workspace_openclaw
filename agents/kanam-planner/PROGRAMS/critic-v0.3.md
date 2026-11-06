# PROGRAMA - Critic v0.3 "El Cable"

**Programa:** `critic-v0.3`
**Estado:** active
**Objetivo:** convertir al Critic en un rol con producto real y demanda medida: T1 primer veredicto real sobre su propio kit, T3 absorcion de VETOs, T4 extensiones de eje, T5 y v1.0 veredicto como gate invocable por otros agentes.
**Owner:** `kanam-planner` (programa) / `main` (ejecucion)
**Fuente:** `agents/kanam-critic/ROADMAP-v0.3.md`
**Fecha:** 2026-11-06
**Regla:** ninguna afirmacion de estado sin evidencia verificable (`archivo:linea` o comando). Si no se pudo verificar, se marca como supuesto y se agrega un paso de verificacion.

---

## 1. Verificacion de estado

Lo ya ejecutado se verifica, no se repite.

| Item | Estado | Evidencia |
|---|---|---|
| T0.1 - ROADMAP v0.3 | Cerrado | `agents/kanam-critic/ROADMAP.md:3-7` declara v0.3 y revision 2026-11-06. |
| T0.2 - Skills en catalogo | Cerrado | `.knowledge/skills-catalog.tsv:11` (`evidence-hunter`) y `:27` (`sharp-adversarial-review`). |
| T0.3 - Promesa rota | Cerrado | `agents/kanam-critic/skills/evidence-hunter/SKILL.md:93-95` corrige `openclaw skill run`; no quedan promesas en `skills/` ni en el README. |
| T2.1 - Heartbeat | Cerrado | `openclaw.json`: `agents.entries.kanam-critic.heartbeat` = every 24h, target last, lightContext true, timeout 900. |
| T2.2 - `critic-sweep-weekly` | Declarado cerrado | El Critic reporta cron `0 18 * * 1`, tz America/Argentina/Buenos_Aires, isolated, agentId `kanam-critic`. El Planner no puede listar automations de otro agente por scope; CORE debe adjuntar job ID, next run y last run. |
| T1 - Primer veredicto real | Abierto | `agents/kanam-critic/memory/verdicts.jsonl` tiene 2 lineas, ambas fixtures (`sample_artifact`, `verify_by_core`); 0 veredictos reales. |
| `docs/reviews/` | No existe | T1.1 crea `agents/kanam-critic/docs/reviews/`; el reporte se publica ahi. |

**Lectura:** el cuello de botella no es capacidad, es adopcion. T1 es el producto que falta; T3-T5 no se tocan hasta que T1 exista.

---

## 2. Plan de programa

| # | Tramo | Tarea | Rol | Dueno | Criterio de salida | Depende de | Gate | Bloqueo |
|---|---|---|---|---|---|---|---|---|
| 1 | T1.1 | Preparar snapshot del kit y verificar modelo del Critic | core | main | Existe `docs/reviews/2026-11-06-kit-snapshot.md` con manifiesto de skills, bin y tests; incluye `modelo=gpt-oss:120b-cloud`; el directorio existe. | - | - | Si el Critic corre con otro modelo, T1 no cuenta. |
| 2 | T1.2 | Ejecutar el ritual SHARP sobre `kanam-critic-kit-v0.3` | critic | kanam-critic | `verdicts.jsonl` tiene una linea con `artifact=kanam-critic-kit-v0.3`, total 5-25, verdict VETO/Aprobado/ORO, timestamp >= 2026-11-06 y 5 ejes con evidencia citada. | 1 | critic | Modelo distinto o evidencia no citada: no se registra. |
| 3 | T1.3 | Publicar el reporte del primer veredicto | critic | kanam-critic | Existe `docs/reviews/2026-11-06-critic-kit-v0.3.md` con 5 secciones de eje, al menos 5 citas `archivo:linea`, veredicto y modelo. | 2 | critic | - |
| 4 | T3.1 | Definir el ledger de fricciones y registrar el primer veredicto | critic | kanam-critic | Existe `memory/frictions.jsonl` con schema documentado y al menos 1 registro del veredicto T1, o `status=none` si no hubo fricciones. | 3 | - | T1 debe producir al menos una friccion; si no, se registra `none`. |
| 5 | T3.2 | Producir 3 VETOs reales y registrar sus fricciones | critic | kanam-critic | `verdicts.jsonl` tiene 3 VETOs reales (incluye T1 si es VETO; si no, 3 artefactos adicionales elegidos por CORE/Gonzo) y `frictions.jsonl` tiene 3 registros. | 4 | critic | Faltan 2 artefactos reales si T1 no es VETO. Sin artefactos, T3 se bloquea. |
| 6 | T3.3 | Medir absorcion de VETOs y publicar la tasa | critic | kanam-critic | Existe `docs/reviews/<fecha>-absorcion.md` con `absorbed`, `total` y `rate`; cada friccion tiene `status` y `fix_url` o `rejected`. | 5 | critic | Los fixes pueden no existir; tasa 0 es valida, pero debe medirse. |
| 7 | T4.1 | Implementar `objective-extractor` con gate del Critic | dev | kanam-dev | Existe `skills/objective-extractor/SKILL.md`; `openclaw skills list --agent kanam-critic` la muestra; el lab tiene un caso; el Critic emite veredicto Aprobado u ORO. | 6 | critic | T1-T3 cerrados. |
| 8 | T4.2 | Agregar detectores horizon, resistance y auto-reportado a `evidence-hunter` | dev | kanam-dev | `evidence-hunter.py` tiene los detectores nuevos; el lab pasa `GLOBAL=aprobado (6/6 o mas)`; cada detector tiene un caso trampa. | 6 | critic | Lab 5/5 verde; T1-T3 cerrados. |
| 9 | T4.3 | Implementar `format_sharp_report.py` y publicar 1 PR comment real | dev | kanam-dev | Existe `bin/format_sharp_report.py`; 1 veredicto real publicado como PR comment con URL; el Critic emite veredicto. | 6 | critic | Publicacion externa requiere OK de Gonzo; sin PR target, se bloquea. |
| 10 | T5.1 | Definir el contrato de invocacion cruzada al Critic | core | main | Existe `docs/CRITIC-INVOCATION.md` con `sessions_spawn(agentId=kanam-critic)`, contexto requerido, salida esperada y regla de gate; CORE lo aprueba. | 3 | - | CORE debe aprobar la politica de invocacion cruzada. |
| 11 | T5.2 | Cablear el veredicto del Critic como gate del pipeline | dev | kanam-dev | Un run del pipeline sin veredicto del Critic falla; con veredicto pasa; el check queda en `scripts/check-pipeline-enforcement.py` o en la skill del pipeline. | 10, 9 | critic | T5.1 aprobado; sin veredicto real no hay gate. |
| 12 | v1.0 | Aceptacion final del Critic como estandar | core | main | 1+ solicitud/mes originada en otro agente y veredicto como gate; acta de aceptacion en `docs/reviews/<fecha>-critic-v1.0.md` firmada por CORE. | 11 | - | 30 dias de observacion; no se puede forzar. |

---

## 3. Contratos de ejecucion por tramo

### T1 - Primer veredicto real

**Sujeto elegido por Gonzo:** el agente mismo, no un proyecto de producto. El artefacto es `kanam-critic-kit-v0.3`.

| Campo | Contrato |
|---|---|
| Artefacto | Verdicto SHARP del kit + reporte publicado. |
| Donde se escribe | `agents/kanam-critic/memory/verdicts.jsonl` y `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3.md`. |
| Como se verifica | `python3 agents/kanam-critic/bin/query_verdicts.py --artifact kanam-critic-kit-v0.3` devuelve 1 fila; `test -f agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3.md`; `grep -c "archivo:linea"` >= 5. |
| Senal de listo | 1 veredicto real, 0 fixtures, 5 ejes con evidencia, reporte con lector. |
| Dueno | Critic emite; CORE verifica; Planner registra. |
| Bloqueo | Modelo distinto de `ollama/gpt-oss:120b-cloud` invalida el veredicto. |

**Precondicion dura:** T1.1 debe probar que la sesion del Critic usa `gpt-oss:120b-cloud`. Si corre con `minimax-m3.1-flash` u otro, se detiene y se re-spawnea; no se emite veredicto con el modelo equivocado.

### T3 - Absorcion de VETOs

| Campo | Contrato |
|---|---|
| Artefacto | `frictions.jsonl` + reporte de absorcion. |
| Donde se escribe | `agents/kanam-critic/memory/frictions.jsonl` y `agents/kanam-critic/docs/reviews/<fecha>-absorcion.md`. |
| Como se verifica | `grep -c '"status"'` >= 3; `python3 agents/kanam-critic/bin/query_verdicts.py | grep -c VETO` >= 3; el reporte contiene `absorbed=`, `total=`, `rate=`. |
| Senal de listo | 3 VETOs reales con `fix_url` o `rejected`; tasa numerica publicada. |
| Dueno | Critic mide; CORE verifica fixes; Planner registra. |
| Bloqueo | Si T1 no es VETO, CORE/Gonzo eligen 3 artefactos adicionales. Sin artefactos, T3 se bloquea; no se inventan VETOs. |

**Schema minimo de `frictions.jsonl`:**

```json
{"verdict_artifact":"kanam-critic-kit-v0.3","friction_id":"F1","description":"...","status":"open|absorbed|rejected","fix_url":null,"days_to_fix":null,"measured_at":"2026-11-06T00:00:00Z"}
```

### T4 - Extensiones de eje

| Campo | Contrato |
|---|---|
| Artefacto | `objective-extractor`, detectores nuevos en `evidence-hunter`, `format_sharp_report.py`. |
| Donde se escribe | `agents/kanam-critic/skills/objective-extractor/`, `agents/kanam-critic/bin/evidence-hunter.py`, `agents/kanam-critic/bin/format_sharp_report.py`. |
| Como se verifica | `openclaw skills list --agent kanam-critic` muestra la skill; el lab pasa `GLOBAL=aprobado (6/6 o mas)`; `format_sharp_report.py` produce 1 PR comment con URL. |
| Senal de listo | Cada artefacto existe, tiene caso de lab o PR real, y veredicto del Critic Aprobado/ORO. |
| Dueno | Dev implementa; Critic fija criterio y emite veredicto; CORE verifica. |
| Bloqueo | T1-T3 cerrados; publicacion externa con OK de Gonzo. |

### T5 / v1.0 - Estandar

| Campo | Contrato |
|---|---|
| Artefacto | Contrato de invocacion + gate del pipeline + acta v1.0. |
| Donde se escribe | `docs/CRITIC-INVOCATION.md`, `scripts/check-pipeline-enforcement.py` o la skill del pipeline, `docs/reviews/<fecha>-critic-v1.0.md`. |
| Como se verifica | Un run sin veredicto falla; con veredicto pasa; 1+ solicitud/mes originada en otro agente. |
| Senal de listo | El Critic es invocable por otro agente y su veredicto es gate. |
| Dueno | CORE/Planner definen; Dev cablea; Critic emite; CORE acepta. |
| Bloqueo | Politica de invocacion cruzada aprobada por CORE + 30 dias de observacion. |

---

## 4. Plan de dispatch

**Regla dura:** el CORE ejecuta; el Planner entrega el envelope (plan, contratos, brief); el Critic solo fija criterios de salida y emite veredictos. El Planner no escribe en el workspace del Critic.

| Orden | Paso | Ejecuta | Verifica | Artefacto |
|---|---|---|---|---|
| 1 | T1.1 | CORE | CORE | Snapshot + modelo |
| 2 | T1.2 | Critic | CORE | Verdicto en JSONL |
| 3 | T1.3 | Critic | CORE | Reporte |
| 4 | T3.1 | Critic | CORE | Ledger de fricciones |
| 5 | T3.2 | Critic | CORE | 3 VETOs |
| 6 | T3.3 | Critic | CORE | Tasa de absorcion |
| 7 | T4.1 | Dev | Critic + CORE | Skill `objective-extractor` |
| 8 | T4.2 | Dev | Critic + CORE | Detectores + lab |
| 9 | T4.3 | Dev | Critic + CORE | PR comment |
| 10 | T5.1 | CORE/Planner | CORE | Contrato de invocacion |
| 11 | T5.2 | Dev/CORE | Critic + CORE | Gate del pipeline |
| 12 | v1.0 | CORE | CORE | Acta de aceptacion |

**Reparto:**

- **Planner:** mantiene el programa, los contratos, el brief semanal y los bloqueos. No ejecuta, no escribe codigo del Critic, no emite veredictos.
- **CORE:** spawnea, verifica el repo, escribe config/politica, registra evidencia y sintetiza.
- **Critic:** corre el ritual SHARP, emite VETO/Aprobado/ORO y mide absorcion. No negocia el plan ni asigna trabajo.
- **Dev:** implementa T4.1, T4.2, T4.3 y T5.2 con gate del Critic.
- **Auditor:** no participa; esto es sustancia, no superficie.

**Secuencia:** T1.1 -> T1.2 -> T1.3 -> T3.1 -> T3.2 -> T3.3 -> T4.1/T4.2/T4.3 -> T5.1 -> T5.2 -> v1.0. T4.1, T4.2 y T4.3 pueden ir en paralelo despues de T3.3; T5.1 puede empezar despues de T1.3, pero T5.2 espera T4.3.

---

## 5. Brief semanal (5 lineas)

1. T0 y T2 cerrados; T1 abierto: 0 veredictos reales, 2 fixtures.
2. Proximo: T1.1 snapshot/modelo y T1.2 ritual SHARP sobre `kanam-critic-kit-v0.3`.
3. T3-T5 pendientes; T4 bloqueado por T1-T3; T5/v1.0 bloqueado por politica CORE + 30 dias.
4. Metricas: veredictos reales/semana = 0 (meta >= 1); absorcion = sin datos; ejes con evidencia = 0%.
5. Decision: ninguna para T1; para T3.2, CORE/Gonzo eligen 2 artefactos reales si T1 no es VETO.

---

## 6. Bloqueos y riesgos

| # | Riesgo | Mitigacion |
|---|---|---|
| R1 | T1 depende de un sujeto listo | Gonzo eligio el agente mismo; el artefacto es `kanam-critic-kit-v0.3`. |
| R2 | T2.1 era un config write | Cerrado; el heartbeat existe y se verifico en `openclaw.json`. |
| R3 | Skills sin disparador | T1 y T2 primero; T4 solo despues de T1-T3. |
| R4 | Modelo del Critic distinto al declarado | T1.1 verifica `gpt-oss:120b-cloud`; si no, se detiene. |
| R5 | Tooling de veredictos nunca usado | T1 ejercita `record_verdict.py` y `query_verdicts.py`; si rompen, se arreglan en T1. |
| R6 | T2.2 no verificable desde el scope del Planner | CORE adjunta job ID, next run y last run de `critic-sweep-weekly`. |
| R7 | T3 necesita 3 VETOs | Si T1 no es VETO, CORE/Gonzo eligen 3 artefactos; no se inventan. |
| R8 | T5/v1.0 requiere politica y tiempo | CORE aprueba la invocacion cruzada; 30 dias de observacion. |

**Tramo bloqueado hoy:** T5/v1.0. Razon: la invocacion cruzada y el veredicto como gate requieren una decision de politica de CORE y 30 dias de observacion; no se puede forzar antes de T1-T4. T3.2 queda condicionado a que existan 3 VETOs reales.

---

## 7. Lo que no entra (filtro de Parsimony)

- Las 6 skills nuevas de la propuesta anterior: 4 no sobreviven el filtro.
- Un dashboard de metricas SHARP: vanity; la metrica que importa es la tasa de absorcion.
- Auto-invocacion del Critic hacia otros agentes: la politica y el deslinde de rol lo prohiben.
- Un "modo severo" del veredicto: la severidad se gradúa con evidencia, no con adjetivos.
- Un plugin de GitHub: el cliente de PR ya es `gh` + T4.3.

---

## 8. Referencias

- `agents/kanam-critic/ROADMAP-v0.3.md` - ruta T0-T5 y criterios originales.
- `agents/kanam-critic/ROADMAP.md` - estado v0.2 corregido.
- `docs/NORTH.md` - Etapa 3 "El Equipo".
- `docs/ROADMAP.md` - Capa 4.1 skills.
- `agents/kanam-planner/CAPABILITIES.md` - contrato del Planner.
- `docs/PLANNER-INTEGRATION.md` - RACI y dispatch.
- `skills/planner-delegation/SKILL.md` - como el CORE convoca al Planner.

---

_El Critic no necesita mas skills: necesita su primer veredicto real. T1 es el programa._
