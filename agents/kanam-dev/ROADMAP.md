# ROADMAP.md - Kanam DEV 💻

**Versión actual:** v0.2
**Objetivo:** v0.5 - Autonomía operativa sin supervisión línea por línea
**Última revisión:** 2026-11-06
**Dueño:** kanam-dev (autoría) · Kanam CORE (gobierno)

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

## 1. Por qué existe esta versión

La v0.1 describía correctamente la visión pero tenía un problema medido: **el rol
no se usaba**. El dueño lo dijo con un dato ("no se utiliza este agente hace 8
horas") y el diagnóstico resultó otro que el esperado.

No faltaban skills (43 documentadas). Lo que faltaba era **superficie de
invocación**: cada tarea arrancaba con "leete el brief, el SPEC y el repo", y ese
costo era mayor que el de hacerla.

La v0.2 es la versión que construyó esa superficie. No agregó conocimiento:
empaquetó lo que ya sabía en comandos de una línea con contratos honestos.

Regla que guio el corte: **si un pedido tarda más en explicarse que en
ejecutarse, no se pide.**

---

## 2. Retrato verificado de la versión actual (v0.2)

Medido, no afirmado. Cada fila tiene el comando que la prueba.

| Capacidad | Estado | Evidencia |
|---|---|---|
| **Superficie del pipeline** (`bin/kanam-dev`, 8 subcomandos) | ✅ operativo | 15 tests. Un subcomando desconocido y un faltante de herramienta salen 2, nunca 0. |
| **S1 intake con elección de plantilla** | ✅ operativo | 32 tests. Un pedido sin `verificacion` falla antes de leer código. |
| **Runner que encadena estaciones** | ✅ operativo, probado en 2 repos reales | 17 tests. `--dry-run` y `--resume` desde la estación que falló. |
| **S3/S4 slice-commit** | ✅ operativo | 19 tests. Dry run por defecto; `.env` y `*.db` bloquean el plan entero. |
| **S5 docs-sync** | ✅ operativo, calibrado en 2 repos | 29 tests. Detecta conteos de tests, tokens, comandos y rutas desalineados. |
| **S7 handoff gate** | ✅ operativo | 22 tests. Rechaza un `verified` con exit distinto de 0. |
| **Skill `kanam-dev-surface`** | ✅ operativa | Registrada en `SKILLS-INDEX.md`, validación de skills sin fallos. |
| **Contrato del pipeline** (`PIPELINE-CONTRACTS.md`) | ✅ escrito | 7 estaciones, 5 plantillas, 3 niveles de obligatoriedad. |
| **Ciclo Hermes** (`hermes-*`, 9 skills) | 🟡 parcial | Documentación completa; la orquestación con estado entre etapas es el runner, que cubre el flujo pero no los hermes por nombre. |
| **CI/CD con gating automático** | ❌ no existe | Ningún workflow ejecuta el pipeline en un PR. |
| **Registro persistente de evidencias** | 🟡 parcial | `run.json` por corrida en disco; no hay base ni dashboard consultable. |
| **Métricas de performance y seguridad automatizadas** | 🟡 parcial | Skills presentes; los scripts no están cableados a estaciones. |

**Totales:** 134 tests, 0 fail, en 6 suites. Verificado al cierre de esta versión.

**Honestidad:** lo que la v0.2 resuelve es la **invocación**. Lo que no resuelve
es la **automatización del trabajo en sí**: `discovery`, `slice` y `build` siguen
siendo manuales, con evidencia declarada obligatoria. Eso es deliberado, no deuda.

---

## 3. Visión v0.5 - Rol con autonomía completa

Un pedido entra, el pipeline decide qué estaciones aplican, las corre, y devuelve
un handoff con evidencia reproducible. El humano aprueba las decisiones de
producto, no las ejecuciones.

La diferencia con "autonomía" mal entendida: **el pipeline no reemplaza el
criterio, lo hace verificable.** Un agente que escribe sin supervisión es el
verde falso que la v1 de minesweeper ya pagó.

---

## 4. Camino de madurez

| Etapa | Qué es | Estado | Criterio de listo (señal verificable) |
|---|---|---|---|
| **v0.1 - Presencia** | El rol existe con `AGENTS.md`, `IDENTITY.md` y catálogo de skills. | ✅ completada | Todos los `SKILL.md` presentes y listados. |
| **v0.2 - Superficie de invocación** | El pipeline existe, encadena estaciones por plantilla y cierra con handoff verificado. | ✅ completada (2026-11-06) | 134 tests verdes; corridas reales sobre `kanam-fixer` y `preflight` con repo intacto. |
| **v0.3 - Evidencia persistente** | Cada corrida deja un registro consultable, no un archivo suelto en `/tmp`. | ⚪ pendiente | Una corrida de hace una semana se puede auditar: qué plantilla, qué estaciones, qué salida por estación, sin abrir el `/tmp`. |
| **v0.4 - Gating en CI** | Un workflow ejecuta `verify` y `docs --check` en cada PR y bloquea el merge si falla. | ⚪ pendiente | Un PR con un token desalineado o un test rojo no puede mergearse; el check aparece en verde cuando corresponde. |
| **v0.5 - Entrega end-to-end** | Tres pedidos distintos recorren el pipeline completo y producen handoff aprobado sin que el humano corrija el proceso. | ⚪ pendiente | Tres corridas reales con `status: completo` en el handoff, sin intervención correctiva en el orden de estaciones. |

---

## 5. Hitos de la versión en curso (v0.3)

| Hito | Capacidad desbloqueada | Evidencia requerida para cerrar |
|---|---|---|
| **5.1 Registro persistente de corridas** | Auditar un trabajo de semanas atrás sin depender de `/tmp`. | Un `runs.db` (SQLite, sin dependencias) con: fecha, plantilla, estaciones, exit por estación, salida truncada y ruta del artefacto. El runner escribe ahí además del `run.json`. |
| **5.2 Consulta del historial** | Responder "¿qué corrí esta semana?" y "¿qué falló más?". | `kanam-dev history [--last N] [--template T]` lee la base y devuelve una tabla. Test con base de fixture. |
| **5.3 Retención y tamaño** | Que la base no crezca sin control. | Política explícita: N corridas o M días, con purga verificable. Sin política, la base se vuelve un depósito. |
| **5.4 Medición de demanda** | Saber si la superficie se usa, con evidencia y no con impresión. | Conteo desde sesiones y memoria (no telemetría en el CLI): pedidos por semana que llegan a DEV sobre los que podrían. Una línea, revisada a las dos semanas. |
| **5.5 Primera corrida completa real** | Probar el pipeline en un trabajo de verdad, no en un fixture. | Un cambio mío, chico, con `task`: intake completo, slice declarado, verify verde, handoff válido, commit. Registrado en 5.1. |

---

## 6. Lo que rechazo y por qué

- **Convertirme en linter de estilo.** Mi foco es sustancia: arquitectura,
  pruebas, documentación. Un linter pertenece a `kanam-ops`.
- **Agentes autónomos de código.** No tengo autorización para publicar ni
  desplegar. El pipeline hace honestas las estaciones manuales, no las reemplaza.
- **Telemetría dentro del CLI.** Agregar instrumentación a cada invocación suma
  superficie de fallo y se puede falsificar con un cron. La demanda se mide desde
  sesiones y memoria.
- **Dependencias nuevas.** Nada de pyyaml, typer, click, rich. Argument parsing y
  SQLite con stdlib, como el resto del pipeline.
- **Más skills como respuesta a "no se usa".** Con 44 skills, sumar la 45 es la
  respuesta equivocada. La próxima skill entra solo con un pedido real repetido
  que no encaje en ninguna existente.
- **Guiones largos como gate.** Retirado por decisión del dueño el 2026-11-06.
  Queda como criterio de estilo opcional, no como barrera.

---

## 7. Red lines y cómo se mide el éxito

**Red lines:**
1. No publicar, desplegar ni borrar fuera del alcance autorizado sin aprobación
   humana explícita para esa acción.
2. No cruzar el dominio de otros roles (`kanam-ops`, `kanam-critic`,
   `kanam-auditor`).
3. No aprobar un trabajo sin la salida del comando que lo prueba. Un `verificado`
   sin output es inválido y el handoff gate lo rechaza.
4. No tocar datos locales (`.env`, `*.db`, `.venv`, `node_modules`) sin respaldo.

**Cómo se mide el éxito de la v0.3 (tres condiciones):**
1. **Auditabilidad:** una corrida de la semana pasada se puede reconstruir desde
   la base sin abrir archivos temporales.
2. **Uso real:** al menos una corrida completa de un cambio propio, registrada y
   con handoff válido.
3. **La base no crece sin control:** la retención tiene una prueba que la verifica.

**Cómo se mide el éxito del rol, en general:** pedidos por semana que llegan a DEV
sobre los que podrían llegarle. Si esa cifra no sube con la superficie ya
construida, el diagnóstico estuvo mal y hay que cambiar el principio, no agregar
fases.

---

## 8. Referencias verificadas

- `PIPELINE-CONTRACTS.md` - las 7 estaciones, 5 plantillas y la matriz de gates.
- `ROADMAP-demand.md` - el diagnóstico que originó la v0.2 y por qué el cuello
  era invocación y no conocimiento.
- `skills/kanam-dev-surface/SKILL.md` - la superficie, con los errores ya
  cometidos y cómo evitarlos.
- `bin/` - los 6 scripts con sus tests.
