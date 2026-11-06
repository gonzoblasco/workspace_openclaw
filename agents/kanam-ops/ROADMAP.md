# ROADMAP.md - kanam-ops 🛠️

**Versión actual:** v0.2
**Objetivo:** v0.5 - OPS como default de todo lo que toca el sustrato
**Última revisión:** 2026-11-06 18:30 (reemplaza v0.1 del 2026-10-07; backup en `ROADMAP.v0.1.bak-20261106`)
**Dueño:** kanam-ops autoría / Kanam CORE gobierno

---

## 0. Dónde estamos, en una pantalla

El diagnóstico de v0.1 era duro y correcto: **un agente no se usa porque tiene
skills, se usa porque algo lo llama.** Ese diagnóstico sigue valiendo. Lo que
cambió es que hoy algo lo llama.

| Métrica | 2026-10-07 (v0.1) | 2026-11-06 (v0.2) |
|---|---|---|
| Automations con `agentId: kanam-ops` | **0 de 11** | **7**, todas `ok` |
| Hooks que despiertan a OPS | **0** (`["main"]`) | **sí** (`["main","kanam-ops"]`) |
| Regla de despacho en CORE | no existía | `docs/OPS-DISPATCH.md` + sección en `AGENTS.md` |
| Scripts duplicados | 5 divergentes | **1 dueño**, la raíz son symlinks |
| Drift | DRIFT 7 de 7 días | `OK: sin drift (235 campos)` |
| Tests | **0** | **59 verdes** |
| Cambios registrados | prosa en el daily | **10 entradas** en `gateway-changes.jsonl` |
| Watchdogs de infraestructura | 0 | **4** (canales, presupuesto, incidentes, drift) |

**Etapas:** E1 completa - E2 completa - E3 3 de 4 - E4 1 de 3 (4.2 hecho).

---

## 1. El diagnóstico original, que sigue siendo la base

Gonzo preguntó por qué este agente no se usaba desde hacía 17 días. Ese
diagnóstico, del 2026-10-07, se conserva porque explica por qué las etapas
tienen el orden que tienen.

### 1.1 Uso medido entonces

| Evidencia | Dato |
|---|---|
| Sesiones reales (más de 2 mensajes) | **3** de 10 |
| Sesiones de 2 mensajes | 7, pings de prueba del handshake multi-agente |
| Última sesión con trabajo | 2026-10-08 |
| Automations con `agentId: kanam-ops` | **0** de 11 |
| Hooks que despertaban a OPS | **0** |

### 1.2 La causa, en orden de peso

1. **Los trabajos de OPS los hacía `main`.** El job `gateway-daily-audit`
   existe, corre todos los días a las 09:30, y ejecuta el script de OPS. Con
   `agentId: main`. Eso explicaba el 90% del desuso: el sistema ya hacía
   trabajo de OPS, solo que sin OPS.
2. **OPS solo entraba cuando CORE se acordaba.** Sin entrada por evento.
3. **`main` era más barato de invocar** y sabía hacer el 80%.
4. ~~**Modelo desalineado.**~~ **NO ES UN PROBLEMA.** Corregido por Gonzo el
   2026-11-06: `gpt-oss:120b-cloud` es una elección deliberada, por alcance
   creativo para idear la extensión del agente. El modelo lo elige Gonzo según
   la etapa del rol, no un criterio de alineación.
5. **Scripts duplicados y divergentes.** La copia de OPS era una foto vieja.
6. **Cero tests.** Un rol de confiabilidad sin pruebas de sus herramientas no
   puede pedir confianza.

---

## 2. Principio rector

> **Un agente no se usa porque tiene skills. Se usa porque algo lo llama.**

E1 lo pone en el flujo. E2 hace que merezca estar. E3 lo vuelve proactivo.
E4 le da autonomía acotada. **No hay etapa de "más skills"**: el catálogo
nunca fue el problema.

---

## 3. Etapas

### E1 - Ser invocable ✅ COMPLETA

| # | Entregable | Estado |
|---|---|---|
| 1.1 | 3 jobs de infra con `agentId: kanam-ops` | ✅ los 3 migrados; `gateway-daily-audit` corrido a mano, `ok` en 55s |
| 1.2 | OPS por hook | ✅ `hooks.allowedAgentIds` = `["main","kanam-ops"]`, `hooks check` 5/5 |
| 1.3 | Regla de despacho en AGENTS.md de CORE | ✅ `docs/OPS-DISPATCH.md`; bootstrap bajo cap |
| 1.4 | Modelo alineado | **RETIRADO** por decisión de Gonzo |

**Corrección registrada:** el 1.4 se había ejecutado mal (cambio a deepseek) y
Gonzo lo revirtió. Un test mío fijaba el modelo y convertía esa decisión en
fallo de test. Corregido: el test valida forma `provider/modelo`, no un valor.

### E2 - Merecer la confianza ✅ COMPLETA

| # | Entregable | Estado |
|---|---|---|
| 2.1 | Un solo dueño por script | ✅ la raíz son symlinks a `agents/kanam-ops/scripts/` |
| 2.2 | Drift semántico, ruido cero | ✅ 235 campos, allowlist explícita |
| 2.3 | Tests de los scripts | ✅ `tests/test_ops_scripts.py` |
| 2.4 | Registro de cambios estructurado | ✅ `gateway-change-log.sh`, 10 entradas |

### E3 - Anticipar (3 de 4)

| # | Entregable | Estado |
|---|---|---|
| 3.1 | Watchdog de canales | ✅ `gateway-channels-watchdog`, cada 5m. Probado en las dos direcciones |
| 3.2 | Watchdog de presupuesto | ✅ `gateway-budget-watchdog`, cada 6h. Umbrales 4GB DB / 6GB dir |
| 3.3 | Pre-flight de cambios | ✅ **adoptado como regla de CORE** el 2026-11-06 |
| 3.4 | Post-mortem automático | ✅ `gateway-incident-postmortem`, cada 1h |

**Criterio que se usó para probar watchdogs, y que queda como norma:** un
watchdog se prueba en las dos direcciones. Silencio cuando está sano, y
disparo cuando la condición es real. Solo lo primero no prueba nada.

### E4 - Decidir (en curso)

| # | Entregable | Estado |
|---|---|---|
| 4.1 | Política de drift propia | Herramienta lista. **1 de 10** cambios resueltos |
| 4.2 | SecretRef completo | ✅ **HECHO.** `doctor` sin hallazgos de plaintext |
| 4.3 | Presupuesto de riesgo | Herramienta lista. **1 de 10** clasificados |

**Arquitectura:** `gateway-config-drift.sh` **mide**, `gateway-risk-policy.sh`
**decide**. No se juntan. Un medidor con permiso de escribir es cómo se acepta
a ciegas un cambio.

**Regla que no se negocia:** la allowlist del medidor nunca gana sobre un
patrón de riesgo alto. Un campo sin patrón conocido es **MEDIO**, no BAJO.

**Primer caso real (2026-11-06 18:15):** `kanam-critic` agregó heartbeat a su
entrada. Clasificado MEDIO, escalado, aprobado por Gonzo, aceptado con backup
`openclaw.json.bak-ops-accept-heartbeat-20261106-1815`. El flujo completo
funcionó: clasificar, escalar, esperar OK, aceptar.

---

## 4. El camino a v0.5

E4 no se cierra escribiendo código: **se cierra acumulando casos**. El criterio
de 10 cambios no se puede fabricar, y fabricarlo lo haría inútil.

### Lo que falta, en orden

| Prioridad | Trabajo | Cómo se cierra |
|---|---|---|
| 1 | **4.1 y 4.3: acumular 9 casos más** | Con uso real. Cada drift que aparezca pasa por la política y queda registrado |
| 2 | **Watchdog de política de riesgo** | Que avise cuando hay drift MEDIO/ALTO, en vez de esperar a que alguien pregunte. Es el único trabajo de E4 que sí se puede construir ya |
| 3 | **3.3 en uso sostenido** | CORE ya lo adoptó; falta que pase por varios cambios reales |
| 4 | **Revisión de E1-E3 a 30 días** | El roadmap pide un mes estable antes de dar E4 por buena |

### Lo que NO se hace ahora

- **Más skills.** El catálogo nunca fue el problema.
- **Auto-reparación sin humano.** Un proceso que cambia config y se valida a
  sí mismo puede dejar drift irreparable.
- **UI de plugins.** `openclaw plugins enable/disable` ya lo hace.
- **Kubernetes o infra cloud.** El sustrato es un Mac mini.

---

## 5. Las tres métricas que importan

1. **Sesiones de OPS por semana con trabajo real.** Antes: 0. Ahora hay 7 jobs
   corriendo; falta medir sesiones con más de 2 mensajes durante una semana.
2. **Ratio de trabajo de infra que hace OPS.** Antes: 0 de 3 jobs. Ahora: 7 de
   7 jobs de infra son de OPS.
3. **Falsas alarmas de drift por semana.** Antes: 7 de 7 días. Ahora: 0 en días
   sin cambios, verificado el 2026-11-06.

---

## 6. Red lines

1. Nunca editar `openclaw.json` a mano; siempre `openclaw config set` o `config patch --stdin`.
2. Nunca un secreto en el JSON, en el chat ni en el historial del shell. Siempre SecretRef.
3. Nunca un restart, un borrado o un cambio de producción sin aprobación humana explícita para esa acción y ese alcance.
4. Nunca `--accept` de un drift con un campo sin explicar.
5. Nunca borrar datos locales (venvs, DBs, uploads) para que algo pase: excluir la ruta.
6. **Nunca commitear con `git add` amplio.** Usar `ops-commit.py`, que aborta si hay archivos ajenos en el índice.

---

## 7. Deudas conocidas, ajenas a este roadmap

Se registran para que no se pierdan, no para resolverlas de paso.

- **`agents/main/agent` pesa 7.6 GB**, de los cuales **5.2 GB son backups de
  migración** del runtime. No es urgencia (124 GB libres) y **no se borró
  nada**: son respaldos y la decisión es humana.
- **16 fallos de arranque del gateway en 158 segundos** (2026-10-18), todos con
  `Tailscale is stopped.` El gateway usa Tailscale para reclamar la ruta: si
  Tailscale está caído, no arranca solo. Dependencia no declarada del host.
- **Drift de versión en roadmaps ajenos:** `kanam-critic` (v0.3 archivo vs v0.2
  índice) y `kanam-studio` (v0.2 vs v0.1). Hace fallar el pre-commit del repo.
- **Migración ADR-073 sin reconciliar:** 268 archivos en el working tree.
  Trabajo real de OPS, pero sesión propia: no se mezcla con este roadmap.

---

## 8. Historial de esta versión

| Fecha | Qué se hizo |
|---|---|
| 2026-11-06 | E1 completa (1.1-1.3; 1.4 retirado por decisión de Gonzo) |
| 2026-11-06 | E2 completa (2.1-2.4) |
| 2026-11-06 | E3.1 canal watchdog, probado con canal plantado |
| 2026-11-06 | E3.2 presupuesto watchdog; hallazgo de 5.2GB en `.bak` |
| 2026-11-06 | E3.4 post-mortem; hallazgo de 16 fallos por Tailscale |
| 2026-11-06 | E5: procedimientos operativos en `docs/OPS-DISPATCH.md` |
| 2026-11-06 | E4.2 SecretRef completo; 4.1/4.3 con `gateway-risk-policy.sh` |
| 2026-11-06 | `ops-commit.py`: commits acotados tras dos incidentes cruzados |
| 2026-11-06 | Primer drift resuelto por la política (heartbeat de critic) |

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
