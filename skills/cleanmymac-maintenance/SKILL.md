---
name: "cleanmymac-maintenance"
description: "Protocolo flexible de mantenimiento con CleanMyMac CLI vía frases naturales"
---

# cleanmymac-maintenance

Protocolo para correr CleanMyMac CLI desde Kanam, invocado con frases naturales de Gonzo. Flexible, no un script fijo: Kanam elige qué correr según el contexto y el estado del disco.

## Contexto técnico (verificado 2026-08-22)

- CleanMyMac CLI v1.0.0 beta, instalado via `brew install --cask macpaw/taps/cleanmymac-cli`.
- Binarios: `cleanmymac` y `cmm` (mismo tool).
- **No tiene salida plana/JSON/dry-run.** `clean` y `purge` son TUI interactivas; `--force` borra lo preseleccionado sin review. `analyze` es puro TUI. `optimize ram`/`purgeable` e `ignore` son no-interactivos.
- Consecuencia para orquestacion: Kanam **no puede hacer preview plano item-por-item** en texto. La revision detallada vive solo en la TUI.
- Ubicacion de caches detectables: Homebrew, npm, Yarn, pnpm, pip, Cargo, Go, CocoaPods, Docker, VS Code, JetBrains, Maven, Gradle, Poetry, uv, Bun, Deno, mise; AI junk (Claude Code, Claude, Codex, Gemini, Cursor, OpenCode); `purge` detecta node_modules, .next, .turbo, target, .build, .venv, Pods, DerivedData, vendor, cmake-build-*.

## Modos de invocacion

Gonzo pide en lenguaje natural. Kanam interpreta y elige el nivel.

| Frase típica | Nivel | Accion |
|---|---|---|
| "es hora de mantenimiento" / "mantenimiento ligero" | Ligero | `optimize ram` + `optimize purgeable` + `clean trash`. No borra caches. |
| "limpia el disco" / "mantenimiento profundo" | Profundo | `cleanmymac clean` (TUI) para revision manual, o `clean --force` si Gonzo aprobo antes. |
| "barrido total" / "limpiá todo a fondo" | Total | `clean --force` + `purge` (revisar cada projecto en TUI). Solo tras aprobacion explicita. |
| "analizá el disco" / "que ocupa espacio" | Diagnostico | `analyze` (TUI) + reporte de lo que encuentra. |

## Reglas de ejecucion

1. **Por defecto: revision interactiva.** Para cualquier borrado de caches/artifacts, abrir la TUI correspondiente y dejar que Gonzo marque y confirme. Kanam nunca lanza `--force` por iniciativa propia.
2. **`--full` / "yolo" / "a fondo sin preguntar" es el unico disparador de `--force`.** Si no aparece esa senal explicita, no usar `--force`.
3. **`optimize ram`/`purgeable` y `ignore` son seguros** - se pueden correr sin revision previa.
4. **Siempre empezar con diagnostico** si el disco esta lleno pero no se sabe que ocupa: `analyze` antes que `clean`.
5. **No borrar con `purge` en directorios custom sin revisar el detalle** (el propio CLI advierte que puede tocar source code si se escanea mal una ruta).
6. **Respetar la ignore list**: si un proyecto importa, antes de un purge sugerir `cleanmymac ignore add <path>` para protegerlo.
7. **Registrar en daily note** lo que se limpio y cuanta espacio se recupero, tras cada ejecucion real.

## Flujo tipico de una sesion de mantenimiento

1. Kanam interpreta la frase y elige nivel (tabla de arriba).
2. Para niveles Profundo/Total: correr `cleanmymac clean` en un PTY interactivo y pasar el control a Gonzo, o lanzar `--force` si hubo senal yolo.
3. Tras el clean, reportar: `X items removed`, `Y GB cleaned`, y recordar que `cleanmymac ignore add <path>` protege proyectos.
4. Actualizar el daily note y (si aplica) el estado en memory.

## Reglas de seguridad

- CleanMyMac CLI es software **propietario** (MacPaw), licencia EULA, no open source.
- La logica de deteccion es compartida con el app de escritorio, pero es beta: comandos pueden cambiar.
- No sube codigo fuente ni archivos personales; analytics desactivable via `config`.
- Ante duda entre borrar o no: no borrar, mostrar y preguntar.

## Antipatrones a evitar

- No correr `clean --force` automatico por cron/heartbeat sin aprobacion previa de Gonzo.
- No abrir varias TUIs a la vez (confuso); una por sesion.
- No confundir `optimize` (seguro, no borra caches) con `clean` (si borra).
- No tratar el CLI como fuente de verdad de "que puedo borrar" sin mostrar el detalle cuando hay volumen significativo (>5 GB).
