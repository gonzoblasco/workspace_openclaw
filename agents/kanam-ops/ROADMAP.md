# ROADMAP.md - kanam-ops 🛠️

**Versión actual:** v0.1
**Objetivo:** v0.5 - OPS como default de todo lo que toca el sustrato
**Última revisión:** 2026-11-06 (reemplaza el roadmap v0.1 del 2026-10-07, backup en `ROADMAP.v0.1.bak-20261106`)
**Estado de ejecución:** E1 y E2 EJECUTADAS y verificadas el 2026-11-06. Commit `7e19519438`.
**Dueño:** kanam-ops autoría / Kanam CORE gobierno

---

## 1. El problema real: no es falta de capacidades, es falta de demanda

Gonzo preguntó por qué este agente no se usa desde hace 17 días. Medí el uso real antes de proponer nada.

### 1.1 Uso medido

| Evidencia | Dato |
|---|---|
| Sesiones de `kanam-ops` en disco | **10**, todas cerradas y comprimidas |
| Sesiones reales (más de 2 mensajes) | **3**: 2026-09-28 (dos turnos), 2026-10-07 (48 mensajes) |
| Sesiones de 2 mensajes | **7**, son pings de prueba del handshake multi-agente |
| Última sesión con trabajo | **2026-10-08** (la del 48 mensajes arrancó 2026-10-07 23:28) |
| Total de mensajes en 5 semanas | **~76** |
| Automations con `agentId: kanam-ops` | **0** de 11 |
| Hooks que despiertan a OPS | **0** (`hooks.allowedAgentIds` = `["main"]`) |
| Mención de OPS en dailies, octubre | 4 archivos, casi siempre como registro de que existe |

### 1.2 La causa, en orden de peso

1. **Los trabajos de OPS los hace `main`.** El job `gateway-daily-audit` existe, corre todos los días a las 09:30, y ejecuta `bash ~/.openclaw/workspace/scripts/gateway-audit.sh`. Es literalmente el script de OPS, corriendo con `agentId: main`. Igual `gateway-jobs-watcher` y `openclaw-backup-schedule`. OPS tiene la skill y el script; `main` tiene el cron. Eso explica el 90% del desuso: **el sistema ya hace trabajo de OPS, solo que sin OPS**.
2. **OPS solo entra cuando CORE se acuerda.** No tiene entrada por evento. CORE tiene que: notar que hay un problema de infra, decidir que es de OPS, y hacer `sessions_spawn agentId=kanam-ops`. Tres pasos manuales que compiten con "lo hago yo en un comando".
3. **`main` es más barato de invocar y sabe hacer el 80%.** Un cambio de modelo, un `config get`, un restart: `main` ya lo tiene en contexto. OPS agrega protocolo de backup y verificación, que suena a overhead cuando el pedido es chico.
4. **Modelo desalineado.** `kanam-ops.model.primary` es `ollama/gpt-oss:120b-cloud`. `main`, `kanam-dev`, `kanam-mind`, `kanam-studio` usan `deepseek-v4.1-flash:cloud`. OPS corre en un modelo distinto al resto del equipo, sin una razón medida registrada.
5. **Scripts duplicados y divergentes.** `workspace/scripts/gateway-audit.sh` (63 líneas, con health check `doctor --lint`) es **distinto** a `agents/kanam-ops/scripts/gateway-audit.sh` (37 líneas, sin health check). El que corre en producción es el de la raíz, mantenido fuera del workspace de OPS. Lo mismo con `aggregate-sync.sh` (ya hubo un incidente de drift stale en octubre, registrado en el daily del 2026-10-12).
6. **Cero tests.** Los 6 scripts pasan `bash -n`, pero no hay una sola prueba. Un rol de confiabilidad sin pruebas de sus propias herramientas no puede pedir confianza.

### 1.3 Un detalle incómodo sobre el roadmap anterior

El roadmap v0.1 declaraba `gateway-config-drift.sh` como "🟡 parcial: requiere revisión manual para aceptar cambios". El problema no es que sea parcial: es que **nunca se puede aceptar limpio**. El baseline es un hash de todo el archivo, y con 8 agentes y sesiones rotando, `openclaw.json` cambia por razones ajenas a OPS varias veces por semana. El baseline del 2026-11-02 ya está desactualizado, y el daily del 2026-09-26 registra el mismo problema. Mientras la herramienta central de OPS dé DRIFT permanente, OPS va a parecer un role que siempre tiene una alarma pendiente.

---

## 2. Principio rector de este roadmap

> **Un agente no se usa porque tiene skills. Se usa porque algo lo llama.**

Las cuatro etapas de abajo están ordenadas por esa idea. Primero OPS **entra** en el flujo (deja de ser manual). Después OPS **merece** estar ahí (herramientas confiables). Después OPS **anticipa** (eventos en vez de pedidos). Recién al final OPS **decide** (política propia, dentro de límites).

No hay una etapa de "más skills". Las skills existentes están bien; el problema nunca fue el catálogo.

---

## 3. Etapas

### E1 - Ser invocable (v0.1 -> v0.2)

**Objetivo:** que OPS llegue al trabajo sin que CORE tenga que acordarse.

**Estado: EJECUTADA 2026-11-06.** Evidencia abajo.

| # | Entregable | Criterio de listo |
|---|---|---|
| 1.1 | Los 3 jobs de infraestructura corren con `agentId: kanam-ops`: `gateway-daily-audit`, `gateway-jobs-watcher`, `openclaw-backup-schedule` | `automations list` muestra `kanam-ops` en los 3; cada uno corre al menos una vez y deja evidencia en el log |
| 1.2 | OPS accesible por hook (`hooks.allowedAgentIds` incluye `kanam-ops`) | Un POST al hook despierta a OPS y vuelve con respuesta |
| 1.3 | `AGENTS.md` de CORE con una regla explícita de despacho: qué es de OPS y qué no | El doc existe y CORE lo cita en un handoff real |
| 1.4 | Modelo de OPS alineado con el equipo | `config get agents.entries.kanam-ops.model.primary` = `deepseek-v4.1-flash:cloud`, con fallback a `gpt-oss:120b-cloud` |

**Evidencia de cierre (2026-11-06):**
- 1.1: los 3 jobs tienen `agentId: kanam-ops` (`gateway-daily-audit`, `gateway-jobs-watcher`, `openclaw-backup-scheduled`), verificado en `openclaw automations list`. Ademas se corrio `gateway-daily-audit` a mano: status `ok`, 55s, escribio `~/.openclaw/gateway-audit.log` con el audit completo.
- 1.4: `agents.entries.kanam-ops.model.primary` = `ollama/deepseek-v4.1-flash:cloud`. Backup: `openclaw.json.bak-ops-invocable-20261106`.
- 1.2 y 1.3 siguen pendientes: hook y regla de despacho en el AGENTS.md de CORE.

**Por qué primero:** sin esto, todo lo demás es material que nadie va a buscar. El punto 1.1 solo ya cambia la curva de uso de 0 sesiones por semana a 3.

**Riesgo:** mover un job de `main` a `kanam-ops` cambia quién recibe las notificaciones y con qué modelo corre. Si OPS falla, el audit diario deja de correr. Mitigación: migrar uno a la vez, con el anterior en `enabled: false` por una semana antes de borrarlo.

### E2 - Merecer la confianza (v0.2 -> v0.3)

**Objetivo:** que cuando OPS diga "verificado", eso signifique algo.

**Estado: EJECUTADA 2026-11-06** (2.1, 2.2 y 2.3). Evidencia abajo. 2.4 pendiente.

| # | Entregable | Criterio de listo |
|---|---|---|
| 2.1 | **Un solo dueño por script.** Eliminar la duplicación: los scripts viven en `agents/kanam-ops/scripts/` y la raíz los llama desde ahí (o al revés, pero uno solo) | `diff` entre las dos copias da 0; el job que corre en producción usa la ruta única |
| 2.2 | **Drift con ruido cero.** Reemplazar el hash de archivo completo por un diff semántico de campos, con allowlist explícita de campos que cambian solos | `gateway-config-drift.sh` da OK en un día normal sin intervención; si hay drift, el reporte nombra el campo y el valor viejo/nuevo |
| 2.3 | **Tests de los 6 scripts.** Suite `bats` o `pytest` con al menos: backup antes de cambio, verificacion despues, drift detecta un cambio plantado, y cada script devuelve exit code correcto | `tests/` con N tests verdes; corre en el hook de pre-commit |
| 2.4 | **Registro de cambios estructurado.** Cada cambio de config deja un registro legible por máquina (qué, cuándo, backup, antes, después, verificación), no solo prosa en el daily | Un comando lista los últimos 20 cambios con su backup y su evidencia |

**Por qué segundo:** una vez que OPS está en el flujo, la primera vez que falle o alarme de más pierde la confianza que costó ganar. E2 es la etapa que hace que E1 sostenga.

**Nota sobre 2.2:** esta es la etapa más valiosa de todo el roadmap y la más ignorada hasta ahora. Es también la que más fácil se puede hacer mal: un drift "inteligente" que ignora campos es peor que uno ruidoso, porque el silencio no se nota.

**Evidencia de cierre (2026-11-06):**
- 2.1: los 5 scripts de la raiz son symlinks a `agents/kanam-ops/scripts/`. La copia de OPS era una foto del 2026-09-27 sin los fixes `b6942d0d33` ni `794727eae8`; ahora tiene el contenido corregido.
- 2.2: `gateway-config-drift.sh` v2, semantico sobre 229 campos. Antes: DRIFT 7 de 7 dias. Ahora: `OK: sin drift`, exit 0. Ciclo probado sobre el config vivo con cambio plantado y reversion.
- 2.3: `agents/kanam-ops/tests/test_ops_scripts.py`, 19 tests verdes. Incluye que la allowlist NO tape cambios de seguridad.
- 2.4 pendiente: registro de cambios legible por maquina.

### E3 - Anticipar (v0.3 -> v0.4)

**Objetivo:** que OPS hable primero, con motivo.

| # | Entregable | Criterio de listo |
|---|---|---|
| 3.1 | **Watchdog de canales.** Un trigger que despierte a OPS cuando un canal cae o el gateway deja de responder | Trigger configurado; una caída simulada genera un aviso en menos de 5 minutos |
| 3.2 | **Watchdog de presupuesto.** Alerta cuando el uso de modelos o el tamaño de la DB de agentes cruza un umbral (hoy `agent DB (main)` está en 1.5 GB según `doctor`, sin alerta) | Umbral configurado; cruzar el umbral dispara aviso, no un silencio |
| 3.3 | **Pre-flight de cambios.** Antes de que CORE aplique un cambio de config, OPS valida en dry-run y devuelve un veredicto | CORE lo llama en al menos un cambio real y ahorra un error |
| 3.4 | **Post-mortem automático.** Cuando algo cae, OPS arma el timeline desde logs y propone la causa | Un incidente real tiene su informe armado por OPS, no a mano |

**Por qué tercero:** un watchdog sin E2 detrás es un generador de falsas alarmas. Y un watchdog sin E1 no existe, porque no hay a quién despertar.

### E4 - Decidir (v0.4 -> v0.5)

**Objetivo:** autonomía acotada, con vuelta atrás siempre disponible.

| # | Entregable | Criterio de listo |
|---|---|---|
| 4.1 | **Política de drift propia.** OPS acepta cambios esperados que cumplen la allowlist y escala solo lo que no puede explicar | 10 cambios seguidos resueltos sin intervención humana, 0 aceptados a ciegas |
| 4.2 | **SecretRef completo.** Cero tokens en texto plano en `openclaw.json` (hoy `doctor` reporta "plaintext secret-bearing config fields") | `doctor` deja de reportar el warning; toda credencial cableada por ref |
| 4.3 | **Presupuesto de riesgo.** OPS clasifica cada cambio por reversibilidad y se autolimita a los de riesgo bajo sin aprobación | Clasificación usada en al menos 10 cambios, sin un solo cambio de riesgo alto sin aprobación |

**Por qué último:** es lo único que el roadmap anterior prometía al final también, y por la misma razón: autonomía sin E1 a E3 verificadas es un agente que cambia producción solo.

---

## 4. Qué rechazo

Coincido con el roadmap anterior en sus tres rechazos y agrego uno propio.

- **UI completa de gestión de plugins.** `openclaw plugins enable/disable` ya lo hace. Una UI duplica la vía oficial.
- **Auto-reparación del gateway sin revisión humana.** Un proceso que cambia config y se valida a sí mismo puede dejar drift irreparable.
- **Kubernetes / infra cloud.** Fuera de alcance: el sustrato es un Mac mini.
- **(Nuevo) Más skills.** El diagnóstico no muestra un hueco de capacidades. Agregar `gateway-monitor-alerts`, `backup-schedule` y similares suma catálogo sin sumar demanda. Si E1 a E4 funcionan, las skills necesarias se van a escribir solas en el momento en que un trabajo real las pida.

---

## 5. Las tres métricas que importan

Si al final solo sobreviven tres números, que sean estos.

1. **Sesiones de OPS por semana con trabajo real** (más de 2 mensajes). Hoy: 0. Piso aceptable para v0.5: 5.
2. **Ratio de trabajo de infra que hace OPS sobre el total.** Hoy: 0 de 3 jobs. Para v0.5: los 3, salvo los que por diseño necesiten a `main`.
3. **Falsas alarmas de drift por semana.** Hoy: 7 de 7 días (el baseline está desactualizado desde el 2026-11-02). Para v0.5: 0 en días sin cambios.

Ninguna de las tres se mide leyendo el código. Se miden con `automations list`, los logs de sesión y `gateway-config-drift.sh`.

---

## 6. Red lines

1. Nunca editar `openclaw.json` a mano; siempre `openclaw config set` o `config patch --stdin`.
2. Nunca un secreto en el JSON, en el chat ni en el historial del shell. Siempre SecretRef.
3. Nunca un restart o un cambio de producción sin aprobación humana explícita para esa acción y ese alcance.
4. Nunca `--accept` de un drift con un campo sin explicar.
5. Nunca borrar datos locales (venvs, DBs, uploads) para que algo pase: excluir la ruta.

---

## 7. Orden de ejecución sugerido

**Semana 1:** 1.1 y 1.4. Mover `gateway-daily-audit` a `kanam-ops`, alinear el modelo. Son dos cambios de config, con backup y verificación cada uno. Con esto OPS deja de estar en 0 sesiones por semana.

**Semana 2:** 2.1 y 2.2. Un solo dueño por script, drift con ruido cero. Es donde está el valor más alto por hora invertida.

**Semana 3:** 1.2, 1.3 y 2.3. Hook, regla de despacho en CORE, tests.

**Semana 4:** 3.1 y 3.3. El primer watchdog y el pre-flight. Recién acá OPS empieza a hablar sin que le pregunten.

E4 no tiene fecha: depende de que E1 a E3 se sostengan un mes sin fallas.

---

## 8. Lo que este roadmap no resuelve

La migración ADR-073 sigue sin reconciliar (268 archivos en el working tree, `init-project.sh` y `aggregate-sync.sh` apuntando a `$WORKSPACE/projects` cuando los proyectos viven en `~/projects`). Es trabajo real de OPS y es exactamente el tipo de tarea que lo haría demandado, pero es una sesión propia: no se mezcla con este roadmap ni se resuelve de paso.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
