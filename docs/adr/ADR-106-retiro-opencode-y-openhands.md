# ADR-106: Se retiran opencode y OpenHands; Claude Code queda como único harness

**Fecha:** 2026-10-28
**Estado:** Aceptado
**Decisores:** Gonzo (pedido explícito: "entre los harness que se usaron, cual es el que tuvo mejor promedio?" → "entonces decidido, eliminemos opencode y openhands, tengamos lo menos posible" → "no busco LO mejor en ciertas ocasiones sino el único que responda bien siempre") / Kanam
**Origen:** cierre de la cata de harnesses 2026-10-27/28, con la matriz completa cloud (6 modelos × 3 harnesses × 3 tareas = 54 celdas).
**Relacionado:** ADR-090 (modelos por rol), ADR-102 (minimax como motor del CORE)

---

## Contexto

La cata de harnesses midió la misma matriz de tareas contra tres harnesses (Claude Code, opencode, OpenHands) con seis modelos cloud. El resultado ordena distinto según el criterio:

| Harness | Puntuación total (sobre 180) | Promedio por modelo (sobre 30) | Peor celda | Celdas en 0 | Veces último |
|---|---|---|---|---|---|
| **Claude Code** | 168 | **28,0** | **16/30** | 1 | **0 de 6** |
| opencode | 157 | 26,2 | 0/30 | 2 | 2 de 6 |
| OpenHands | 132 | 22,0 | 0/30 | 1 | 2 de 6 |

El dato que decidió no es el promedio sino **la celda más baja**: opencode y OpenHands tienen celdas en **cero absoluto** - el agente no escribió nada. Claude Code nunca bajó de 16/30 y nunca quedó último con ningún modelo.

Gonzo explicitó el criterio: *"no busco LO mejor en ciertas ocasiones sino el único que responda bien siempre"*. Bajo ese criterio, la consistencia gana al techo. OpenHands alcanzó 30/30 con tres modelos distintos y opencode empató con Claude Code con el mismo modelo, pero un harness que a veces brilla y otras no responde no sirve como default operativo.

### El error de fondo: nunca hicieron falta como containers

Al cerrar el retiro, Gonzo señaló el error original: *"nunca debimos intentar correr local opencode y openhands... técnicamente ya están dentro de Ollama y se pueden correr por CLI (como Claude Code, aunque no es OpenHands)... no hacía falta instalarlo"*.

La captura del menú de `ollama 0.40.11` lo confirma: **Claude Code, OpenCode y OpenClaw se lanzan desde ahí**, sobre el mismo runtime de Ollama que ya estaba instalado. Instalar opencode como container duplicó una integración que ya existía en la máquina.

OpenHands es la excepción que el mismo Gonzo marcó: no aparece en el menú de Ollama porque no es una de sus integraciones. Pero eso no lo justifica como container permanente: es una herramienta que, si se necesita, se decide aparte.

**Consecuencia para el registro:** el motivo del retiro no es solo el rendimiento de la cata. Es que **la vía correcta para correr un harness local es el menú de Ollama (CLI), no un container**. Quien lea este ADR buscando un harness no debe reinstalar opencode: lo lanza desde Ollama.

## Decisión

Se **retiran opencode y OpenHands** del stack. **Claude Code queda como único harness**.

Se elimina de verdad, no se deja "apagado":

- containers (`openhands-canvas`, `opencode`) e imágenes
  (`opencode-local:dev` 343 MB y `ghcr.io/openhands/agent-canvas:1.28.1` 5,4 GB)
- volúmenes `docker_opencode-data` y `docker_opencode-state`
- proyectos `projects/opencode` (635 MB) y `projects/openhands` (76 MB), movidos a la papelera

**Total recuperado: ~6,3 GB de disco** más la RAM fija de la VM de Docker en cada arranque.

## Qué se conserva y por qué

- **Los compose archivados** en `docs/tools/compose-archivados/`. Quedan como **registro de lo que se probó**, no como la vía recomendada: el error a no repetir es instalar como container lo que ya es una integración de Ollama. OpenCode se lanza desde el menú de `ollama` por CLI, junto a Claude Code y OpenClaw.
- **El bloque de catálogo de modelos de `scripts/preflight-cata.sh`**, inerte y guardado por la existencia del container. Sobrevive solo por si un harness en Docker vuelve por decisión explícita.
- **`scripts/watch-docker-cata.sh`**, aunque hoy la cata no necesite Docker.

## Consecuencias

**A favor:** el stack baja a lo mínimo, se recuperan 6,3 GB, y la cata ya no depende de Docker en absoluto (Claude Code es CLI host, y los harness locales se lanzan desde el menú de Ollama). Un solo harness significa una sola superficie de configuración de modelos - el formato de catálogo de opencode era justo el que producía el fallo `unrecognized_model` con los locales.

**En contra:** se pierde la única UI web del stack para pilotar un agente a mano. Con minimax, OpenHands sacó 0/30 - un agente que no arranca tampoco se puede pilotar, así que esa capacidad era teórica con el modelo que nos importa.

**Deuda registrada:** la fase local de la cata quedó cortada antes de la última celda de `qwen3.5:9b-mlx`. Los 3 sellos `LOCAL-DONE` (nova-2b, ornith, gemma4:12b-mlx) quedan en disco y son reanudables. **Para retomar esa fase no hace falta reintroducir ningún container**: los harness locales se lanzan por CLI desde el menú de Ollama.
