# ADR-098: Los proyectos vuelven al workspace, y `cwd` separa el hogar del agente de su zona de trabajo

**Fecha:** 2026-10-08
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** sesión 2026-10-08 - al reanudar `kanam-tetris`, el agente A no pudo escribir en `~/projects/kanam-tetris` (su sandbox de escritura era su propio directorio). Gonzo: *"la carpeta projects/ está por fuera ya que puede ser accedido por TODOS LOS AGENTES... es el espacio común"*.
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-083 (frontera de roles), ADR-088/089 (pipeline A/B), ADR-090 (modelos y thinking por agente)
**Supersede:** el modelo anterior que ubicaba los proyectos en `~/projects/`, fuera del worktree (decisión de 2026-09-27)

---

## Contexto

Durante la primera corrida del pipeline A/B para `kanam-tetris` (2026-10-08), el agente A (`kanam-dev`) devolvió un blocker de infraestructura, no de tarea:

> *"All file-editing tools are sandboxed to the agent's workspace at `/Users/gonzoblasco/.openclaw/workspace/agents/kanam-dev` and reject any path that escapes this root."*

La causa, medida contra la config real (`openclaw.json`):

- **Los 8 agentes tienen un `workspace` que es su propio directorio.** No es un campo de "dónde trabajan": es **el terreno que el sandbox del gateway hace escribible**. Todo lo demás queda afuera.
- **Ninguno tiene `cwd`.** El campo existe (ver "La pieza que faltaba") y nació exactamente para separar las dos cosas.

Es decir: `workspace` estaba cumpliendo **dos roles incompatibles a la vez** - el hogar del agente (bootstrap, alma, memoria, skills) y la única zona de escritura. Como los proyectos vivían en `~/projects/` (fuera del worktree), un agente de rol **no tenía ningún lugar legítimo donde escribir código**. El síntoma fue la carpeta fantasma `agents/kanam-dev/projects/` que el agente inventó para reconciliar "no puedo escribir afuera" con "tengo que escribir el proyecto".

### La pieza que faltaba: `cwd`

La documentación oficial de OpenClaw (`agents.defaults.cwd`) define el campo literalmente para este caso:

> *"Optional working directory for agent reply runs. Use it to **run coding tools in an existing repository while bootstrap files (`AGENTS.md`, `SOUL.md`) and memory stay in the managed agent workspace**."*

Con la restricción: *"A distinct working directory requires an unsandboxed run; sandboxed runs reject it."*

Dos hechos de precedencia (misma fuente): *"Session-spawned working directories take precedence, then `agents.entries.*.cwd`, then `agents.defaults.cwd`."*

**Consecuencia clave:** un `cwd` **dentro** del workspace no es un "distinct working directory" - no exige apagar el sandbox.

### Lo que la migración a `~/projects/` dejó atrás

La mudanza de `workspace/projects/` a `~/projects/` (2026-09-26) se aplicó a medias, **otra vez**:

- La decisión de entonces afirmaba que `workspace/projects/` "ya no existe en disco" y que "las 143 bajas se commitearon como limpieza legítima".
- **Medido hoy:** `workspace/projects/` existía con **34 archivos en disco y 20 trackeados en el índice de git**, contradiciendo el `.gitignore` que ya los ignoraba.
- El commit `e6d5cad49d` ("drop the old skills/ and projects/ trees") prometió borrar el árbol; no sacó todos los archivos del índice.

La reconciliación (hecha en esta sesión, **aditiva, cero pérdida**) comparó el residuo contra `~/projects`: **14 archivos existían solo en el residuo** (evidencia de validación de `a11y-fixer/bench` y `metrics`, el `threat-model` de `kanam-os`, un HANDOFF viejo del workspace) y **3 diferían** (el residuo tenía drafts anteriores). Todo se rescató. `.next/build/` (cache) se descartó.

## Decisión

### 1. Los proyectos vuelven al workspace: `workspace/projects/` es el espacio común

**Supersede el modelo de `~/projects/`.** Los proyectos viven en `<workspace>/projects/`, **dentro** del árbol que el gateway gobierna, no en `~/projects/`.

- **Motivo:** el workspace es el terreno común que **todos los agentes** alcanzan. Un `cwd` que apunta adentro del workspace **no requiere desactivar el sandbox** - el destrabe llega sin abrir seguridad.
- **El `.gitignore` conserva la regla `/projects/`**, pero **invierte su motivo**: antes era "afuera del worktree"; ahora es "adentro, pero cada proyecto trae su propio `.git`" - sin la regla, git los absorbería como **gitlinks/submodules implícitos** (el riesgo que AGENTS.md marca como red line).
- **El `Home` llega por symlink:** `~/projects -> ~/.openclaw/workspace/projects`. El humano hace `cd projects/` desde el Home exactamente como antes; el symlink es transparente para la terminal. Los agentes usan el path real (los sandboxes rechazan escribir a través de symlinks).

### 2. `cwd` separa el hogar del agente de su zona de trabajo

**`workspace` = el hogar** (bootstrap, SOUL, IDENTITY, memoria, skills). Se queda donde está.
**`cwd` = dónde trabajan las herramientas.** Apunta a `workspace/` (el padre que contiene `projects/` **y** `sandbox/`). Verificado empíricamente (2026-10-08): el alcance del `cwd` es **recursivo** sobre su árbol, no el path exacto - un agente con `cwd` en el workspace alcanza y escribe en las subcarpetas `projects/` y `sandbox/`. Esto permite el flujo `sandbox (incubadora) -> projects (lo que madura)` con un solo `cwd`.

- **El hogar no se toca.** Un cambio de `workspace` a `projects` habría borrado el contexto de bootstrap del agente (su alma, memoria y skills viven ahí): el efecto colateral que esta decisión evita.
- **`cwd` dentro del workspace** → el sandbox sigue activo. Sin "full access", sin `sandbox: off`.
- Precedencia: un `cwd` seteado por spawn gana al de `agents.entries.*.cwd`; el de `agents.defaults.cwd` es el último.

### 3. La regla de asignación (por rol)

- **Escriben código:** dev, ops → `cwd` a `workspace/` (el padre; el alcance recursivo cubre `projects/` y `sandbox/`).
- **No escriben código de proyecto:** critic, auditor, planner, mind, studio, main → sin `cwd` (su hogar alcanza). Si un spawn puntual necesita un repo, se le pasa el working directory por sesión.

Esta asignación es coherente con ADR-083 (el CORE no escribe código) y con ADR-090 (rol por agente).

## Consecuencias

### Positivas
- **El bloqueo de DEV desaparece sin abrir seguridad.** El sandbox sigue activo: el `cwd` queda adentro del terreno que ya estaba permitido.
- **"Espacio común de todos los agentes" pasa a ser verdad literal**, no una convención que cada agente interpreta distinto (que es, exactamente, cómo nació la carpeta fantasma).
- **Un solo `projects/`** donde antes había dos árboles superpuestos (`workspace/projects/` residuo + `~/projects` vivo).
- **El home del agente conserva su identidad:** `cwd` no toca el bootstrap ni la memoria.

### Negativas / pendientes
- **Los repos de proyecto ahora viven dentro de un repo git ajeno** (`workspace_openclaw`). Mitigado por la regla `/projects/` del `.gitignore`; el riesgo de gitlinks es real si la regla se pierde. Los guardas de gobernanza deben verificar que sigue en pie.
- **Cambio de config del gateway** (los `cwd` por agente): requiere restart. No se puede aplicar desde una sesión que corre sobre el agente modificado (ADR-090).
- **Working trees sucios movidos tal cual:** `a11y-fixer` (3 untracked), `kanam-pulse` (1 modificado), `kanam-spec` (3 untracked). El move es rename atómico: sus `.git` viajan intactos (verificado: 13/13 repos sanos). Pendiente commitearlos.
- **La memoria de proyecto (`.knowledge/`) sigue siendo del proyecto** (regla no revertida en ese punto): viaja con él, excluida por `.git/info/exclude`.

### Correcciones durante la verificación (2026-10-08, mismo día)
- **Falso positivo de medición:** un `git check-ignore -v projects` inicial devolvió "NO ignorado" y se reportó como blocker. Era artefacto de medir una ruta que **no existía en ese instante** (el residuo ya se había movido a `.trash`). La regla matchea correctamente cuando la carpeta existe. Lección: verificar contra un objeto real; una medición sobre algo inexistente no es evidencia.
- **El residuo no era "un error de la matrix"** como parecía: contenía 14 archivos únicos. Se rescataron antes de limpiar.

## Alternativas consideradas

1. **Mover `workspace` de los agentes a `~/projects`.** Rechazada: le borra el contexto de bootstrap (AGENTS/SOUL/IDENTITY/memoria/skills viven en su workspace). Es el efecto colateral que `cwd` evita.
2. **Clonar el proyecto dentro del sandbox del agente.** Rechazada: recrea la carpeta fantasma con contenido y viola la convención de que los proyectos viven en un lugar común.
3. **`cwd` a `~/projects` (fuera del workspace).** Rechazada: es un "distinct working directory" y **exige apagar el sandbox** de cada agente. Traer los proyectos adentro evita ese costo.
6. **`cwd` al `projects/` exacto (en vez del padre `workspace/`).** Rechazada: un solo `cwd` no cubriría las dos zonas (`projects/` + `sandbox/`) y rompería el flujo de madurez descrito por Gonzo. El `cwd` al padre da alcance recursivo a ambas, verificado empíricamente.
4. **Symlink como mecanismo primario de los agentes.** Rechazada: los sandboxes rechazan escribir a través de symlinks. El symlink es solo la puerta cómoda del humano; los agentes usan el path real.
5. **Borrar el residuo sin comparar.** Rechazada: había contenido único. Se comparó archivo por archivo primero.

## Artefactos

- Config a modificar: `~/.openclaw/openclaw.json` (`agents.entries.kanam-dev.cwd`, `kanam-ops.cwd`, `repoRoot`).
- Symlink: `~/projects -> ~/.openclaw/workspace/projects`.
- `.gitignore` del workspace: regla `/projects/` con motivo invertido; bloque `projects_openclaw/` retirado (repo archivado).
- Repo archivado: `gonzoblasco/projects_openclaw` (2026-10-08).
- Reconciliación del residuo: `.trash/workspace-projects-residue-*` y `.trash/merge-backup-*` (backups en `.trash`).
- Verificación de la mudanza: 13/13 repos git sanos; `cd projects/` desde el Home operativo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
