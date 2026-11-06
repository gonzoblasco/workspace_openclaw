# PROGRAMA - Critic v0.3 "El Cable"

**Programa:** `critic-v0.3`
**Estado:** active
**Objetivo:** convertir al Critic en un rol con producto real y demanda medida: T1 primer veredicto real sobre su propio kit, T3 absorcion de VETOs, T4 extensiones de eje, T5 y v1.0 veredicto como gate invocable por otros agentes.
**Owner:** `kanam-planner` (programa) / `main` (ejecucion)
**Fuente:** `agents/kanam-critic/ROADMAP.md`
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
| T2.2 - `critic-sweep-weekly` | Cerrado | Job `37316655-0a7a-4e6f-802f-95ee2cd76052`: cron `0 18 * * 1`, tz America/Argentina/Buenos_Aires, isolated, agentId `kanam-critic`. Delivery explicito por Telegram; la corrida de prueba no entrego porque `channel=last` no tenia canal previo. El payload usa `emit-verdict.py` y termina con `verify-verdict.py`; no usa `record_verdict.py`. |
| T1 - Primer veredicto real | Cerrado (con salvedad F8) | `verdicts.jsonl` r4: `kanam-critic-kit-v0.3-r4`, S4 H4 A4 R4 P3 = 19/25 Aprobado; registrado con `emit-verdict.py` y verificado con `verify-verdict.py`; r2 y r3 invalidados con motivo. F8: emitido por `minimax-m3.1-flash`, el rol declara `gpt-oss:120b-cloud`; el veredicto es provisional hasta reemitirlo con el modelo declarado. |
| T1.b - Segundo veredicto real (trabajo ajeno) | Cerrado | `docs-ROADMAP-madurez` VETO 15/25 (S3 H3 A3 R2 P4); reporte `agents/kanam-critic/docs/reviews/2026-11-06-docs-ROADMAP-madurez.md`; 5 fricciones F10-F14; F8: emitido por `minimax-m3.1-flash`, provisional. |
| T3.1 - Ledger de fricciones | Cerrado | `agents/kanam-critic/memory/frictions.jsonl`: 14 registros (6 absorbed, 8 open). |
| `agents/kanam-critic/docs/reviews/` | Existe en el workspace del Critic | `agents/kanam-critic/docs/reviews/` contiene r2, r4 y el reporte inicial. El root `docs/reviews/` no se usa. |

**Lectura:** T1 ya existe (r4, 19/25 Aprobado, con F8 provisional). El cuello de botella se mueve a T3: medir si el veredicto cambia algo.

---

## 2. Plan de programa

| # | Tramo | Tarea | Rol | Dueño | Criterio de salida | Depende de | Gate | Bloqueo |
|---|---|---|---|---|---|---|---|---|
| 1 | T1.1 | Verificar snapshot y modelo del veredicto r4 | core | main | El reporte `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r4.md` incluye la seccion "Snapshot del kit evaluado" y declara el modelo emisor; F8 queda registrado si el modelo no es `gpt-oss:120b-cloud`. | - | - | F8: modelo distinto al declarado; ver T1.2. |
| 2 | T1.2 | Ejecutar el ritual SHARP sobre `kanam-critic-kit-v0.3-r4` | critic | kanam-critic | `verdicts.jsonl` tiene la fila r4 con `artifact=kanam-critic-kit-v0.3-r4`, scores 4/4/4/4/3, total 19, veredicto Aprobado; r2 y r3 invalidados con motivo; `verify-verdict.py --artifact kanam-critic-kit-v0.3-r4` da `GLOBAL=aprobado`. | 1 | critic | F8: veredicto provisional hasta reemitir con el modelo declarado. |
| 3 | T1.3 | Publicar el reporte del veredicto r4 | critic | kanam-critic | Existe `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r4.md` con 5 secciones de eje, al menos 5 citas `archivo:linea`, 19/25 Aprobado y la nota de modelo F8; `verify-verdict.py` lo acepta. | 2 | critic | - |
| 4 | T3.1 | Definir el ledger de fricciones y registrar el veredicto r4 | critic | kanam-critic | Existe `memory/frictions.jsonl` con schema documentado y al menos 1 registro del veredicto r4, o `status=none` si no hubo fricciones. | 3 | - | T1 debe producir al menos una friccion; si no, se registra `none`. |
| 5 | T3.2 | Producir el tercer VETO real sobre trabajo ajeno | critic | kanam-critic | `verdicts.jsonl` tiene 3 VETOs reales en total (r1 12/25, docs-ROADMAP 15/25 y 1 adicional ajeno) y `frictions.jsonl` tiene sus registros. | 4 | critic | Falta 1 artefacto ajeno: Gonzo ya eligio docs-ROADMAP; CORE/Gonzo eligen el tercero. Sin artefacto, T3 se bloquea. |
| 6 | T3.3 | Medir absorcion de VETOs y publicar la tasa | critic | kanam-critic | Existe `agents/kanam-critic/docs/reviews/<fecha>-absorcion.md` con `absorbed`, `total` y `rate`; cada friccion tiene `status` y `fix_url` o `rejected`. | 5 | critic | Los fixes pueden no existir; tasa 0 es valida, pero debe medirse. |
| 7 | T4.1 | Implementar `objective-extractor` con gate del Critic | dev | kanam-dev | Existe `skills/objective-extractor/SKILL.md`; `openclaw skills list --agent kanam-critic` la muestra; el lab tiene un caso; el Critic emite veredicto Aprobado u ORO. | 6 | critic | T1-T3 cerrados. |
| 8 | T4.2 | Agregar detectores horizon, resistance y auto-reportado a `evidence-hunter` | dev | kanam-dev | `evidence-hunter.py` tiene los detectores nuevos; el lab pasa `GLOBAL=aprobado (6/6 o mas)`; cada detector tiene un caso trampa. | 6 | critic | Lab 5/5 verde; T1-T3 cerrados. |
| 9 | T4.3 | Implementar `format_sharp_report.py` y publicar 1 PR comment real | dev | kanam-dev | Existe `bin/format_sharp_report.py`; 1 veredicto real publicado como PR comment con URL; el Critic emite veredicto. | 6 | critic | Publicacion externa requiere OK de Gonzo; sin PR target, se bloquea. |
| 10 | T5.1 | Definir el contrato de invocacion cruzada al Critic | core | main | Existe `docs/CRITIC-INVOCATION.md` con `sessions_spawn(agentId=kanam-critic)`, contexto requerido, salida esperada y regla de gate; CORE lo aprueba. | 3 | - | CORE debe aprobar la politica de invocacion cruzada. |
| 11 | T5.2 | Cablear el veredicto del Critic como gate del pipeline | dev | kanam-dev | Un run del pipeline sin veredicto del Critic falla; con veredicto pasa; el check queda en `scripts/check-pipeline-enforcement.py` o en la skill del pipeline. | 10, 9 | critic | T5.1 aprobado; sin veredicto real no hay gate. |
| 12 | v1.0 | Aceptacion final del Critic como estandar | core | main | 1+ solicitud/mes originada en otro agente y veredicto como gate; acta de aceptacion en `agents/kanam-critic/docs/reviews/<fecha>-critic-v1.0.md` firmada por CORE. | 11 | - | 30 dias de observacion; no se puede forzar. |

---

## 3. Contratos de ejecucion por tramo

### T1 - Primer veredicto real

**Sujeto elegido por Gonzo:** el agente mismo, no un proyecto de producto. El artefacto es `kanam-critic-kit-v0.3-r4`.

| Campo | Contrato |
|---|---|
| Artefacto | Veredicto SHARP del kit + reporte publicado. |
| Donde se escribe | `agents/kanam-critic/memory/verdicts.jsonl` y `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r4.md`. |
| Como se verifica | `python3 agents/kanam-critic/bin/verify-verdict.py --artifact kanam-critic-kit-v0.3-r4` da `GLOBAL=aprobado`; `test -f agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r4.md`; `grep -c "archivo:linea"` >= 5. |
| Senal de listo | r4 19/25 Aprobado, 5 ejes con evidencia, reporte publicado; r2 y r3 invalidados con motivo. |
| Dueño | Critic emite; CORE verifica; Planner registra. |
| Bloqueo | F8: r4 fue emitido por `minimax-m3.1-flash`; el rol declara `gpt-oss:120b-cloud`. El veredicto es provisional hasta reemitirlo con el modelo declarado. |

**Precondicion dura:** T1.1 verifica el modelo emisor. El r4 actual no cumple `gpt-oss:120b-cloud`; queda registrado como F8 y el veredicto es provisional. Si el contrato exige el modelo declarado, se reemite antes de usar r4 como gate.

### T3 - Absorcion de VETOs

| Campo | Contrato |
|---|---|
| Artefacto | `frictions.jsonl` + reporte de absorcion. |
| Donde se escribe | `agents/kanam-critic/memory/frictions.jsonl` y `agents/kanam-critic/docs/reviews/<fecha>-absorcion.md`. |
| Como se verifica | `grep -c '"status"'` >= 3; `python3 agents/kanam-critic/bin/query_verdicts.py | grep -c VETO` >= 3; `verify-verdict.py` da `GLOBAL=aprobado`; el reporte contiene `absorbed=`, `total=`, `rate=`. |
| Senal de listo | 3 VETOs reales con `fix_url` o `rejected`; tasa numerica publicada. |
| Dueño | Critic mide; CORE verifica fixes; Planner registra. |
| Bloqueo | VETOs reales: r1 12/25 y docs-ROADMAP 15/25. Falta 1 artefacto ajeno; lo eligen CORE/Gonzo. Sin artefacto, T3 se bloquea; no se inventan VETOs. |

**Schema minimo de `frictions.jsonl`:**

```json
{"verdict_artifact":"kanam-critic-kit-v0.3-r4","friction_id":"F1","description":"...","status":"open|absorbed|rejected","fix_url":null,"days_to_fix":null,"measured_at":"2026-11-06T00:00:00Z"}
```

### T4 - Extensiones de eje

| Campo | Contrato |
|---|---|
| Artefacto | `objective-extractor`, detectores nuevos en `evidence-hunter`, `format_sharp_report.py`. |
| Donde se escribe | `agents/kanam-critic/skills/objective-extractor/`, `agents/kanam-critic/bin/evidence-hunter.py`, `agents/kanam-critic/bin/format_sharp_report.py`. |
| Como se verifica | `openclaw skills list --agent kanam-critic` muestra la skill; el lab pasa `GLOBAL=aprobado (6/6 o mas)`; `format_sharp_report.py` produce 1 PR comment con URL. |
| Senal de listo | Cada artefacto existe, tiene caso de lab o PR real, y veredicto del Critic Aprobado/ORO. |
| Dueño | Dev implementa; Critic fija criterio y emite veredicto; CORE verifica. |
| Bloqueo | T1-T3 cerrados; publicacion externa con OK de Gonzo. |

### T5 / v1.0 - Estandar

| Campo | Contrato |
|---|---|
| Artefacto | Contrato de invocacion + gate del pipeline + acta v1.0. |
| Donde se escribe | `docs/CRITIC-INVOCATION.md`, `scripts/check-pipeline-enforcement.py` o la skill del pipeline, `agents/kanam-critic/docs/reviews/<fecha>-critic-v1.0.md`. |
| Como se verifica | Un run sin veredicto falla; con veredicto pasa; 1+ solicitud/mes originada en otro agente. |
| Senal de listo | El Critic es invocable por otro agente y su veredicto es gate. |
| Dueño | CORE/Planner definen; Dev cablea; Critic emite; CORE acepta. |
| Bloqueo | Politica de invocacion cruzada aprobada por CORE + 30 dias de observacion. |

---

## 4. Plan de dispatch

**Regla dura:** el CORE ejecuta; el Planner entrega el envelope (plan, contratos, brief); el Critic solo fija criterios de salida y emite veredictos. El Planner no escribe en el workspace del Critic.

| Orden | Paso | Ejecuta | Verifica | Artefacto |
|---|---|---|---|---|
| 1 | T1.1 | CORE | CORE | Snapshot + modelo |
| 2 | T1.2 | Critic | CORE | Veredicto en JSONL |
| 3 | T1.3 | Critic | CORE | Reporte |
| 4 | T3.1 | Critic | CORE | Ledger de fricciones |
| 5 | T3.2 | Critic | CORE | 1 VETO ajeno (tercero) |
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

1. T0, T2 y T1 cerrados; veredictos reales: r4 Aprobado 19/25 y docs-ROADMAP VETO 15/25.
2. Proximo: T3.2 (tercer VETO ajeno) y T3.3 (tasa de absorcion).
3. T4 bloqueado por T3; T5/v1.0 bloqueado por politica CORE + 30 dias.
4. Metricas: 2 veredictos reales; fricciones 14 (6 absorbed, 8 open); F8 y F9 abiertos.
5. Decision: Gonzo/CORE eligen el tercer artefacto ajeno; F8: reemitir con gpt-oss o cambiar el config del rol.

---

## 6. Bloqueos y riesgos

| # | Riesgo | Mitigacion |
|---|---|---|
| R1 | T1 depende de un sujeto listo | Gonzo eligio el agente mismo; el artefacto es `kanam-critic-kit-v0.3`. |
| R2 | T2.1 era un config write | Cerrado; el heartbeat existe y se verifico en `openclaw.json`. |
| R3 | Skills sin disparador | T1 y T2 primero; T4 solo despues de T1-T3. |
| R4 | Modelo del Critic distinto al declarado | T1.1 verifica el modelo; si no coincide, se registra F8 y el veredicto queda provisional. |
| R5 | Tooling de veredictos nunca usado | T1 ejercita `emit-verdict.py` y `verify-verdict.py`; si rompen, se arreglan en T1. |
| R6 | T2.2 no verificable desde el scope del Planner | CORE adjunta job ID, next run y last run de `critic-sweep-weekly`. |
| R7 | T3 necesita 1 VETO ajeno mas | r1 12/25 y docs-ROADMAP 15/25 ya cuentan; CORE/Gonzo eligen el tercero; no se inventan. |
| R8 | T5/v1.0 requiere politica y tiempo | CORE aprueba la invocacion cruzada; 30 dias de observacion. |

**Tramo bloqueado hoy:** T5/v1.0. Razon: la invocacion cruzada y el veredicto como gate requieren una decision de politica de CORE y 30 dias de observacion; no se puede forzar antes de T1-T4. T3.2 queda condicionado a 1 VETO adicional sobre trabajo ajeno (r1 12/25 y docs-ROADMAP 15/25 ya cuentan).

---

## 7. Lo que no entra (filtro de Parsimony)

- Las 6 skills nuevas de la propuesta anterior: 4 no sobreviven el filtro.
- Un dashboard de metricas SHARP: vanity; la metrica que importa es la tasa de absorcion.
- Auto-invocacion del Critic hacia otros agentes: la politica y el deslinde de rol lo prohiben.
- Un "modo severo" del veredicto: la severidad se gradúa con evidencia, no con adjetivos.
- Un plugin de GitHub: el cliente de PR ya es `gh` + T4.3.

---

## 8. Referencias

- `agents/kanam-critic/ROADMAP.md` - ruta T0-T5 y criterios originales.
- `agents/kanam-critic/ROADMAP.md` - estado v0.2 corregido.
- `docs/NORTH.md` - Etapa 3 "El Equipo".
- `docs/ROADMAP.md` - Capa 4.1 skills.
- `agents/kanam-planner/CAPABILITIES.md` - contrato del Planner.
- `docs/PLANNER-INTEGRATION.md` - RACI y dispatch.
- `skills/planner-delegation/SKILL.md` - como el CORE convoca al Planner.

---

_El Critic no necesita mas skills: necesita su primer veredicto real. T1 es el programa._
