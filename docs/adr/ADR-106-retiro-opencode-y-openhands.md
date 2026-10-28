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

## Decisión

Se **retiran opencode y OpenHands** del stack. **Claude Code queda como único harness**.

Se elimina de verdad, no se deja "apagado":

- containers (`openhands-canvas`, `opencode`) e imágenes
  (`opencode-local:dev` 343 MB y `ghcr.io/openhands/agent-canvas:1.28.1` 5,4 GB)
- volúmenes `docker_opencode-data` y `docker_opencode-state`
- proyectos `projects/opencode` (635 MB) y `projects/openhands` (76 MB), movidos a la papelera

**Total recuperado: ~6,3 GB de disco** más la RAM fija de la VM de Docker en cada arranque.

## Qué se conserva y por qué

- **Los compose archivados** en `docs/tools/compose-archivados/`. Reintroducir cualquiera de los dos no exige reescribir su configuración, y el costo de guardar dos archivos de texto es cero.
- **El bloque de catálogo de modelos de `scripts/preflight-cata.sh`**, inerte y guardado por la existencia del container. Se documentó que reintroducir opencode exige volver a agregar su sonda `need`: sin ella la cata arranca sin verificar infra y pierde celdas en silencio.
- **`scripts/watch-docker-cata.sh`**, aunque hoy la cata no necesite Docker: sobrevive por si un harness en Docker vuelve.

## Consecuencias

**A favor:** el stack baja a lo mínimo, se recuperan 6,3 GB, y la cata ya no depende de Docker en absoluto (Claude Code es CLI host). Un solo harness significa una sola superficie de configuración de modelos - el formato de catálogo de opencode era justo el que producía el fallo `unrecognized_model` con los locales.

**En contra:** se pierde la única UI web del stack para pilotar un agente a mano. Con minimax, OpenHands sacó 0/30 - un agente que no arranca tampoco se puede pilotar, así que esa capacidad era teórica con el modelo que nos importa.

**Deuda registrada:** la matriz de la cata queda incompleta para los locales (la fase local se cortó por decisión de Gonzo antes de la última celda de `qwen3.5:9b-mlx`). Los 3 sellos `LOCAL-DONE` existentes (nova-2b, ornith, gemma4:12b-mlx) quedan en disco y son reanudables, pero hoy no hay harness en Docker que los pueda correr: reintroducir un harness en Docker es requisito para retomar esa fase.
