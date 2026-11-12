# Despacho de infraestructura: el CORE llama a OPS

**Fecha:** 2026-11-06
**Regla en `AGENTS.md`:** seccion "Infraestructura: el CORE llama a OPS".
**Base:** ADR-074 (OPS es duenio del sustrato), ADR-083 (el CORE orquesta, no implementa).

Este archivo existe porque la regla completa no entra en el cap de bootstrap
del `AGENTS.md` (20000 caracteres) y lo que se pasa se trunca en silencio. El
`AGENTS.md` lleva el principio; aca va el detalle operativo.

---

## 1. Que es de OPS

Todo cambio sobre el sustrato del gateway:

| Area | Incluye |
|---|---|
| Config | `openclaw.json` en cualquier forma, `config set`, `config patch --stdin` |
| Canales | alta, cambio, credenciales de Telegram y otros |
| Plugins | habilitar, deshabilitar, instalar, actualizar |
| Automatizaciones | crear, editar, mover de agente, triggers, schedules |
| Drift | baseline, aceptar, explicar diferencias |
| Backups | crear, verificar, restaurar |
| Secretos | migracion a SecretRef, rotacion |
| Diagnostico | por que el gateway no responde, por que un job falla |

## 2. Que NO es de OPS

- Codigo de aplicacion: es de `kanam-dev`.
- Contenido, marca, redaccion: es de `kanam-studio`.
- Investigacion y decision de producto: es de `kanam-mind`.
- Gobernar un programa, escribir ADRs: es del CORE.
- Revision de codigo: es de `kanam-critic` / `kanam-auditor`.

## 3. OPS ya esta en el flujo

No hace falta despertarlo a mano para lo rutinario. Dos jobs corren con
`agentId: kanam-ops`:

| Job | Schedule | Que hace |
|---|---|---|
| `gateway-daily-audit` | cron `30 9 * * *` | audit completo a `~/.openclaw/gateway-audit.log` |
| `openclaw-backup-scheduled` | cada 24h | backup git de la config a `~/Backups/openclaw-git` |

El job `gateway-jobs-watcher` (cada 2h) se retiro el 2026-11-12 por decision de
Gonzo, junto con su `gateway-jobs-check.sh`. La vigilancia de automations pasa
por `openclaw automations list`, y `openclaw doctor` ya reporta los jobs en error.

Ademas, `hooks.allowedAgentIds` incluye `kanam-ops`, asi que OPS puede recibir
trabajo por hook, no solo por spawn.

## 4. Como se le pide algo

`sessions_spawn(agentId: "kanam-ops")` con:

1. **Que hay que hacer**, en imperativo.
2. **Riesgo esperado**: que puede salir mal y que NO se debe tocar.
3. **Limite de aprobacion**: si el trabajo incluye un restart, un borrado o un
   cambio de produccion, se dice explicitamente que NO esta aprobado.

## 5. Que devuelve siempre (contrato de handoff)

- Que cambio, con el comando exacto.
- Nombre del backup.
- Valor antes y despues.
- Evidencia de verificacion (salida real del comando, no la promesa).
- Si requiere restart.

**Un "quedo bien" de OPS es un reporte, no una prueba.** El estandar del CORE
sigue siendo correr el efecto real antes de reportar a Gonzo.

## 6. El limite que no se delega

Aprobar un restart, un borrado o un cambio de produccion es de Gonzo, aunque
OPS tenga la capacidad tecnica para hacerlo. Delegar la tarea no delega la
aprobacion.

## 6-bis. Pre-flight obligatorio: OPS dictamina antes de escribir (E3.3)

**Cuando:** antes de aplicar cualquier cambio sobre el sustrato (seccion 1):
`openclaw.json`, canales, plugins, automatizaciones, credenciales. **No aplica**
a codigo de aplicacion ni a contenido: eso es de DEV y STUDIO.

**Como:** el CORE **no aplica**. Delega a OPS con `sessions_spawn(agentId:
"kanam-ops")` y pide el **veredicto antes de escribir**. El pedido lleva, sin
excepcion:

1. **El cambio exacto**: ruta de config y valor destino.
2. **El motivo**, en una linea.
3. **Que haga dry-run**: `openclaw config patch --stdin --dry-run` o
   `openclaw config get` del estado actual, segun corresponda (secciones 7 y 8).
4. **Que responda con**: veredicto (**APLICA / NO APLICA / APLICA CON
   CAMBIOS**), valor actual, valor resultante, que mas toca ese patch y el
   backup que crearia.
5. **Que no aplique nada**: solo evalua. La aplicacion la decide Gonzo.

**Despues:** si el veredicto es APLICA, se vuelve a delegar a OPS para que
aplique con backup (secciones 7 a 16), y a Gonzo se le trae **evidencia real**
---`config get`, `status`, el job corriendo--- no la promesa. Un "quedo bien" de
OPS sigue siendo un reporte, no una prueba (seccion 5).

**Que NO cambia:** el limite de la seccion 6. Un restart, un borrado o un cambio
de produccion necesita el **OK explicito de Gonzo aunque OPS diga APLICA**.
Delegar no delega la aprobacion.

**Por que existe:** OPS ya tiene E3.1 (canales), E3.2 (presupuesto) y E3.4
(post-mortem) en produccion. E3.3 no se cierra escribiendo mas: se cierra
usando el paso al menos una vez en un cambio real.

---

# Procedimientos operativos

Cada procedimiento tiene el mismo esqueleto: inspeccionar, respaldar, aplicar
por la via oficial, verificar el efecto real y registrar. Si un paso no se
puede completar, se vuelve al backup: no se parchea a ciegas.

## 7. Cambiar un valor de config

Ejemplo real: mover el modelo de un agente.

```
BACKUP="$HOME/.openclaw/openclaw.json.bak-<motivo>-$(date +%Y%m%d)"
cp "$HOME/.openclaw/openclaw.json" "$BACKUP"

openclaw config get agents.entries.kanam-ops.model     # 1. que hay ahora
openclaw config set agents.entries.kanam-ops.model.primary "ollama/gpt-oss:120b-cloud"
openclaw config get agents.entries.kanam-ops.model.primary   # 2. verificar

bash agents/kanam-ops/scripts/gateway-change-log.sh record \
  --field agents.entries.kanam-ops.model.primary \
  --before "ollama/deepseek-v4.1-flash:cloud" \
  --after "ollama/gpt-oss:120b-cloud" \
  --reason "<por que>" \
  --backup "$(basename "$BACKUP")" \
  --evidence "config get devuelve gpt-oss:120b-cloud"
```

**Reglas del paso:**

- `config get` primero, siempre. Sin saber el valor viejo no hay antes/despues.
- Si se agregan claves a un objeto existente, `config patch --stdin --dry-run`
  antes de escribir.
- No se edita el JSON a mano: se pierde la validacion y el backup automatico.
- Si el comando dice que requiere restart, **no se reinicia sin OK de Gonzo**.

## 8. Agregar una clave a un objeto existente

`config set` reemplaza; `config patch` fusiona. Para agregar sin borrar:

```
echo '{"hooks":{"allowedAgentIds":["main","kanam-ops"]}}' \
  | openclaw config patch --stdin --dry-run
echo '{"hooks":{"allowedAgentIds":["main","kanam-ops"]}}' \
  | openclaw config patch --stdin
```

El `--dry-run` no es ceremonia: es el unico momento en que se ve si el patch
vació una clave hermana.

## 9. Habilitar o deshabilitar un plugin

Nunca tocando `plugins.entries.<name>.enabled` a mano:

```
openclaw plugins list --json | jq '.entries[] | select(.enabled)'
openclaw plugins disable <id>
openclaw plugins enable <id>
```

## 10. Mover una automatizacion de agente

`automations edit` rechaza `--stdin` y no tiene `--dry-run`. Se hace asi:

```
openclaw automations get <jobId> --json          # estado actual completo
openclaw automations edit <jobId> --agent kanam-ops
openclaw automations list --json | jq '.jobs[] | select(.id=="<jobId>") | .agentId'
```

Verificar tambien que el modelo del payload siga teniendo sentido: mover el
agente no cambia el `payload.model` que ya estaba fijado ahi.

## 11. Crear una automatizacion de alerta

Un script de alerta debe ser **read-only**: mide y avisa, no arregla. La
reparacion vive en el payload del agente que recibe la alerta, con su propio
limite de aprobacion.

```
openclaw automations add <nombre> \
  --every 15m \
  --agent kanam-ops \
  --command "bash /ruta/al/check.sh" \
  --announce --to <chatId> \
  --display-name "<titulo legible>"
```

Detalle que costo encontrar: `--script <archivo>` espera un script de
code-mode (JavaScript), no un shell script. Para correr bash va `--command`.

Un trigger que se calla cuando su propio check falla parece sano estando roto:
si el check no puede correr, la alerta **igual debe dispararse**.

## 12. Auditar secretos

Primero se mira si ya son SecretRef, sin copiar el valor a ningun lado:

```
openclaw config get gateway.auth.token
# { "source": "store", "provider": "default", "id": "..." }  -> ya es ref
```

Si devuelve un string plano, se guarda con la tool de `secrets` y se cablea:

```
openclaw config set <campo> --ref-provider default --ref-source store --ref-id <NOMBRE>
```

El valor no va al chat, ni al JSON, ni al historial del shell. El changelog
redacta solo cualquier campo que huela a credencial, pero eso es una red, no
el procedimiento.

## 13. Aceptar drift

Un `--accept` bendice **cada** diferencia pendiente, incluidas las que uno no
hizo. Por eso se lee el diff antes.

El baseline **no es JSON**: es un archivo de texto plano con una linea por
hoja, en formato `ruta<TAB>valor` (lo produce `flatten` dentro del script). Un
`jq` sobre ese archivo falla con "Invalid numeric literal". El diff se hace
contra el reporte del script, no contra `jq`:

```
bash agents/kanam-ops/scripts/gateway-config-drift.sh --verbose
# leer cada campo listado y explicarlo; si no hay, el script dice OK
bash agents/kanam-ops/scripts/gateway-config-drift.sh --accept
bash agents/kanam-ops/scripts/gateway-config-drift.sh     # OK esperado
```

Si hace falta ver el valor antes/despues de un campo puntual, se pide al
config y al baseline por separado:

```
openclaw config get <ruta.del.campo>
BASE=~/.openclaw/gateway-config.baseline.json
grep -F -- "<ruta.del.campo>"$'\t' "$BASE"
```

La forma `grep -F -- "<ruta>"$'\t'` importa: el `$'\t'` tiene que quedar
**fuera** de las comillas dobles para expandirse a un tab real. Dentro de
comillas, grep busca la cadena literal `\t` y no encuentra nada (fallo
silencioso, peor que un error).

Lo que el script considera **no-drift** por diseno (rutas de instalacion,
rotacion de modelos, `update.*`, `meta.*`, `telemetry.*`, `gateway.auth.*`)
no necesita explicacion: no es ruido acumulado, es actividad normal.

Cada campo del diff se nombra y se explica antes de aceptar. Un campo sin
explicacion se investiga contra el `.bak-*` mas reciente, no se acepta.

## 14. Restaurar desde un backup

```
ls -t ~/.openclaw/openclaw.json.bak-* | head -5      # elegir, no adivinar
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak-antes-de-restaurar
cp <el-backup-elegido> ~/.openclaw/openclaw.json
openclaw config get <campo-a-recuperar>
```

Si el problema era de estado y no de config (sesiones, credenciales, base de
memoria), el backup de config no alcanza: se restaura el archivo que
corresponde, con su propio respaldo previo.

## 15. Cuando algo no responde

Orden de diagnostico, de mas barato a mas caro:

```
openclaw status                       # el gateway esta vivo?
openclaw channels status              # el canal esta conectado?
openclaw automations status           # el scheduler corre?
tail -50 ~/.openclaw/gateway-audit.log
```

Un 503 transitorio de 10 a 30 segundos despues de un cambio es esperable. Si
el turno propio se corto en esa ventana, se re-verifica el estado antes de
repetir comandos: repetir a ciegas un cambio que ya paso duplica el efecto.

## 16. Que se registra siempre

Una linea por cambio, en `~/.openclaw/gateway-changes.jsonl`:

| Campo | De donde sale |
|---|---|
| `field` | la ruta exacta que se toco |
| `before` / `after` | lo que devolvio `config get`, nunca de memoria |
| `reason` | el por que, en una linea |
| `backup` | nombre del archivo de respaldo |
| `evidence` | salida real que prueba el efecto |

Nunca se borra una entrada del log: es append-only. Una correccion se registra
como una entrada nueva que explica la anterior, porque la historia de un
cambio incluye el error.

Verificar la integridad del log:

```
bash agents/kanam-ops/scripts/gateway-change-log.sh verify
bash agents/kanam-ops/scripts/gateway-change-log.sh list --limit 10
```

## 17. Commitear sin llevarse trabajo ajeno

El repo lo comparten siete agentes sobre un working tree comun. Un `git add`
amplio se lleva archivos de otro. Paso dos veces el 2026-11-06 en ambas
direcciones.

Por eso OPS commitea con su propia herramienta, no a mano:

```
python3 agents/kanam-ops/scripts/ops-commit.py            # dry run
python3 agents/kanam-ops/scripts/ops-commit.py --apply -m "..."
```

Qué garantiza:

- Descubre **solo** las rutas de `agents/kanam-ops/`.
- Si hay algo ajeno en el indice, **aborta y no lo desetapea**. Desetapear el
  trabajo de otro agente es otra forma de romperle el commit.
- Rechaza `.db`, `.env`, claves, aunque vivan dentro de la carpeta de OPS.
- Dry-run por defecto. Verifica el indice despues del `add` y saca lo que se
  haya colado.

Lo que **no** resuelve: un commit de otro agente que se lleve archivos de OPS.
Eso solo se evita desde el otro lado. Si pasa, el contenido sobrevive pero el
mensaje no describe lo que el commit toca, y se dice en el daily.

## 18. Clasificar un drift por riesgo

`gateway-config-drift.sh` **mide**; `gateway-risk-policy.sh` **decide**. No se
juntan: un medidor con permiso de escribir es como se acepta a ciegas.

```
bash agents/kanam-ops/scripts/gateway-risk-policy.sh          # informe
bash agents/kanam-ops/scripts/gateway-risk-policy.sh --json   # maquina
```

Exit 0 significa que todo lo pendiente es riesgo BAJO y reversible: OPS puede
aceptar el baseline solo, con registro. Exit 1 significa escalar.

**La allowlist del medidor nunca gana sobre un patron de riesgo alto.** Un
campo permitido por drift que tambien sea de riesgo alto se clasifica ALTO.
El silencio del medidor no es permiso de la politica.

**Un campo sin patron conocido es MEDIO, no BAJO.** El campo que la politica no
entiende es justo el que hay que mirar.

---

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
