# ADR-049: Claude Code como Motor del Pipeline A/B (Qwen Code a Fallback)

**Fecha:** 2026-09-15
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (Fase 0 de la cola durable; la deriva se detectó al auditar el motor)
**Relacionado:** ADR-049 (Claude Code motor A/B), ADR-077 (pipeline A/B asimétrico)
**Supersede parcialmente:** la sección de motor de la skill `agent-orchestration-pipeline` y `docs/SETUP.md`

---

## Contexto

La documentación operativa (`docs/SETUP.md` línea 29, skill `agent-orchestration-pipeline` línea 10 y 55) dice que **Qwen Code es el motor estándar** de los agentes A/B del pipeline, y que **Claude Code es una alternativa** para SIGKILL o tareas largas.

La práctica es otra. Verificado el 2026-09-15 con fuentes reales:

| Ciclo | Harness real | Fuente |
|---|---|---|
| kanam-tetris v0.2 (2026-09-11) | Claude Code vía Ollama | `docs/learnings/pipeline-agentes.md` |
| Duelos de código atoi (2026-09-13) | Claude Code headless (Claude-3p 2.1.260) | `memory/2026-09-13.md` |
| Prueba de harness (2026-09-15) | Claude Code 2.1.260, `HARNESS_OK` | verificación directa de esta sesión |

Además, `ollama launch` ya lista **claude** como integración de primera clase (junto a qwen, codex, kimi, etc.), y no hay binario global `qwen`/`claude` (Claude Code vive embebido en `Claude-3p/`).

**Resultado:** la documentación y la práctica divergen desde ~2026-09-11. Un doc desactualizado es una deuda: el que lea que "Qwen es el estándar" va a intentar el comando `ollama launch qwen` que ya no es el camino usado.

---

## Decisión

**`Claude Code` (embebido en Claude Desktop 3p, versión >= 2.x) es el motor estándar de los agentes A/B del pipeline**, apuntando al gateway Ollama (`ANTHROPIC_BASE_URL=http://127.0.0.1:11434` o `11435`) con el modelo dinámico de Ollama.

**`Qwen Code` queda como fallback o segundo par de ojos**, no como estándar.

El modelo que ambos cargan se sigue eligiendo por tipo de tarea (ver ADR-090): `deepseek-v4.1-flash:cloud` como default/motor, `glm-5.3-flash` escalada multimodal, `kimi-k2.7-code` nivel superior.

### Comando estándar

```bash
ANTHROPIC_BASE_URL=http://127.0.0.1:11434 \
ANTHROPIC_AUTH_TOKEN=<token> \
claude -p "<tarea>" --model <modelo> \  # headless
  --dangerously-skip-permissions
```

**`claude` ya está en el PATH (2026-09-22).** Instalado global via npm:
`npm install -g --allow-scripts=@anthropic-ai/claude-code @anthropic-ai/claude-code`.
Binario en `/opt/homebrew/bin/claude` (nativo de 217 MB, sin dependencias). Verificado:
2.1.280, smoke test headless devolvió `OK`. Esto elimina la última consecuencia negativa que
declaró este ADR: la ruta embebida de Claude-3p ya no es el único camino.

**Config persistente (verificado 2026-09-22):** `~/.claude/settings.json` acepta un bloque
`env`, así que no hace falta exportar nada en el shell:

```json
{
  "env": {
    "ANTHROPIC_BASE_URL": "http://127.0.0.1:11434",
    "ANTHROPIC_AUTH_TOKEN": "ollama",
    "CLAUDE_CODE_MAX_CONTEXT_TOKENS": "200000"
  }
}
```

Verificado sin variables de entorno externas: respondió `OLLAMA_OK`. **Un install global NO
hereda la config del deployment 3p** - sin este bloque el CLI dice `Not logged in` e intenta
autenticar contra api.anthropic.com. Nunca apuntar a api.anthropic.com con una key real en
este setup.

**Camino recomendado: `ollama launch claude` (verificado 2026-09-22).** Es la via soportada y
la que menos configuración manual requiere: levanta el gateway y resuelve el enmascarado de
modelos por sí sola.

```bash
ollama launch claude --model deepseek-v4.1-flash:cloud -- -p "<tarea>"   # verificado: LAUNCH_OK
```

- El paquete npm trae un `postinstall` (`install.cjs`) que detecta plataforma y hardlinkea el
  binario nativo. Auditado en cuarentena: cero red, cero ejecución arbitraria, cero
  dependencias. npm 11 lo bloquea por defecto; se autoriza con `--allow-scripts`.
- El embebido de Claude Desktop 3p (`~/Library/Application Support/Claude-3p/claude-code/<ver>/`)
  sigue existiendo y funciona; queda como respaldo. Ambas versiones coexisten.
- Requiere Claude Code >= 2.x (la 0.2.18 no maneja el bloque `{type:thinking}` de los modelos de razonamiento).
- `ANTHROPIC_AUTH_TOKEN`: cualquier valor no vacío cuando el base url es el daemon o el gateway local.

### Enmascarado de modelos: donde vive cada cosa (verificado 2026-09-22)

Ollama permite **enmascarar cualquier modelo** con un alias estilo Anthropic, editado en la
app de Ollama (Apps -> panel de Claude) y persistido en
`~/.ollama/config.json` -> `integrations.claude-desktop.aliases`:

| Alias (lo que habla Claude Code) | Modelo real de Ollama |
|---|---|
| `claude-sonnet-5` | deepseek-v4.1-flash:cloud |
| `claude-sonnet-4-6` | deepseek-v4-flash:0731:cloud |
| `claude-opus-5` | glm-5.3:cloud |
| `claude-fable-5` | kimi-k2.7-code:cloud |
| `claude-haiku-4-5-20251001` | gemma4:31b-cloud |

**Los aliases los resuelve el gateway, no el daemon.** El gateway vive en
`http://127.0.0.1:11435` (`~/Library/Application Support/Claude-3p/configLibrary/*.json`:
`inferenceProvider: gateway`, `inferenceGatewayApiKey: ollama`) y **requiere que Claude
Desktop haya corrido al menos una vez**. El daemon (`11434`) no conoce los aliases: pasarle
`--model claude-sonnet-5` falla con *"It may not exist or you may not have access to it"*.

Regla práctica:

- **Alias** (`claude-sonnet-5`) -> gateway `11435`, o simplemente `ollama launch claude`.
- **Tag crudo** (`deepseek-v4.1-flash:cloud`) -> funciona contra el daemon `11434` o el gateway.
  Es la única opción para un modelo que el owner todavía no mapeó.

### Corrección 2026-09-22: los dos enunciados del 15/09 quedaron stale

Al reverificar se comprobó que **ambos eran ciertos cuando se escribieron**, y hoy ya no:

| Enunciado original (2026-09-15) | Estado al 2026-09-22 |
|---|---|
| "NO usar `ollama launch claude --model` (bug: rechaza el flag como unknown option)" | **Stale.** El binario de Ollama es del **2026-09-19** (posterior a este ADR, versión 0.34.2) y ya no reproduce el bug: `ollama launch claude --help` expone `--model string`, y la integración acepta el flag (verificado end-to-end: `LAUNCH_OK`) |
| "no hay binario global `qwen`/`claude`" | **Stale.** `qwen` global se instaló el **2026-09-22 17:24** (`/opt/homebrew/bin/qwen` -> `@qwen-code/qwen-code` 0.24.4); `claude` global también existe desde hoy (2.1.280) |

Ninguno de los dos era un error de escritura: son datos que caducaron. Un ADR con datos
caducados sin fecha de revalidación es indistinguible de un ADR equivocado. De ahí la regla
de revalidación agregada abajo.

---

## Consecuencias

### Positivas
- **La documentación refleja la práctica**: quien retome una sesión encuentra el camino que de verdad se usa.
- Claude Code maneja mejor sesiones largas que Qwen (menos SIGKILL), que era la motivación original para tenerlo como alternativa.
- Una sola forma de lanzar los agentes A/B, con el mismo modelo dinámico de Ollama.

### Negativas
- Claude Code no tiene binario global en el PATH; la ruta al ejecutable de Claude-3p es frágil a cambios de versión. Se mitiga documentándola en `docs/SETUP.md`.
- Claude Code emite warnings cosméticos por modelos custom (`unrecognized_model`); son ruido, no bloquean.

### Regla de actualización
- **Este ADR es la fuente de la verdad.** Cualquier doc/skill que describa el motor del pipeline se actualiza para reflejarlo cuando se toque ese archivo. Si mañana el estándar vuelve a cambiar, se escribe ADR-052+ (supersede a este), no se edita la práctica por debajo del ADR.

### Consecuencia: Claude Code ignora AGENTS.md (verificado empíricamente 2026-09-15)

Claude Code no lee AGENTS.md por defecto - **no lo prioriza, lo ignora**. Verificado con el binario 2.1.260:

| Escenario | Resultado |
|---|---|
| `CLAUDE.md` + `AGENTS.md` juntos | Responde al de `CLAUDE.md` (lo prioriza) |
| Solo `AGENTS.md` | *"I'm not instructed to reply with any specific token"* - no se lee (issue antrhopics/claude-code #6235) |
| `CLAUDE.md` con `@./AGENTS.md` | Las reglas del AGENTS.md se aplican |
| Import con ruta absoluta | Funciona |
| cwd en subdir + `CLAUDE.md` en el padre | Auto-discovery sube directorios y lo lee |

**Mecanismo adoptado:** **cada directorio raíz de proyecto (o workspace) lleva el PAR** `AGENTS.md` + `CLAUDE.md`. El `AGENTS.md` es la **única fuente de verdad** de las reglas del proyecto; el `CLAUDE.md` es su **espejo que se dirige a él** (`@import` del `AGENTS.md`), no lo reemplaza. Así nada se duplica y Claude Code carga las convenciones.

**Prioridad verificada empíricamente (2026-09-15, binario 2.1.260):** con cwd dentro de un proyecto que tiene su par propio Y la raíz con el suyo, Claude Code obedece **el par del proyecto** (respondió al marker del AGENTS.md del proyecto, no al de la raíz). El paquete de reglas más específico (el del proyecto) gana sobre el global.

**Contenido del par:** el `AGENTS.md` del proyecto es **especializado y personalizado para la tarea en curso** (que es el proyecto, su stack, su dominio y sus decisiones vivas), no una copia del global. El `CLAUDE.md` hace `@import` de ese `AGENTS.md` para que Claude Code lo cargue.

**Regla:** se crea el par en un proyecto **cuando ese proyecto entra al flujo de pipeline** (se trabaja con agentes Claude Code sobre el). El clon de un proyecto para pipeline agrega su par si no lo tiene. Hoy están en el workspace raíz y en kanam-fixer (piloto 2026-09-15).

---

## Alternativas consideradas

1. **Mantener Qwen como estándar** (no documentar el cambio): ignoraría la práctica real y dejaría el doc mintiendo. Rechazado.
2. **Dual estándar** (Qwen y Claude al mismo nivel): agrega complejidad sin beneficio; los ciclos reales ya usan Claude. Rechazado.
3. **Esto no es una decisión de modelo**: ADR-090 sigue definiendo *qué* modelo carga el harness. Este ADR solo decide *en qué harness* corre. No pisa esa decisión.

## Actualización 2026-09-29 - retiro de `deepseek-v4-flash`

`deepseek-v4-flash:cloud` fue **retirado por Ollama el 2026-09-25** (verificado con el daemon:
`ollama show deepseek-v4-flash:cloud` responde `was retired at 2026-09-25 00:00:00 -0700 PDT`,
ref `7e00c916-e009-455f-aa4c-f6f64a81a6bd`). Su lugar como motor de los agentes A/B del pipeline
lo ocupa **`deepseek-v4.1-flash:cloud`**, que deja de ser "fase de escalada" y pasa a ser el
reemplazo (la escalada sigue siendo `glm-5.3-flash:cloud`). Este ADR se conserva como registro de
la decisión vigente a su fecha; las referencias a v4-flash que quedan en el texto son históricas.