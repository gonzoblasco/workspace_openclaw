# HANDOFF - workspace

**Fecha:** 2026-10-20 22:25 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Cline instalado y registrado como herramienta IA (sin tocar otros proyectos). Clone shallow de github.com/cline/cline en projects/cline (main @ 0870796), toolchain Bun 1.4.2 (el repo prohibe npm/yarn/pnpm), build:sdk obligatorio. Provider ollama contra http://localhost:11434 por la API NATIVA /api/chat (no /v1: el path OpenAI-compatible ignora options.num_ctx y todo modelo cargaria con 4096 tokens), modelo minimax-m3.1-flash:cloud. Dashboard en :8787 y el chat del agente en /chat (la home / es el monitor del hub y no tiene composer). Verificado end-to-end: turno real con tool calls via chat (creo archivos) y via CLI headless. Ademas se RESTAURO el registro vivo de herramientas IA (scripts/ai-toolbox.py + docs/tools/REGISTRY.md + skill ai-toolbox) que habia sido borrado por scope en el commit de Onyx, y se corrigio el test fragil que rompio el CI (afirmaba rutas absolutas de la Mac Mini en vez de formas). Cline quedo como entrada propia del registro, con wrapper scripts/cline-tool.sh porque son DOS procesos (dashboard :8787 y daemon del hub :25466). Commit db65c4d324 en origin/main, CI verde.

## Estado actual

Registro de herramientas IA restaurado y vigente con 11 entradas (Ollama, Onyx, browser-use, PR-Agent, AnythingLLM, LiteLLM, Milvus, Vane, opencode, OpenHands, Cline); el estado sale de docker compose ls + docker ps + sonda HTTP real, la tabla declara COMO se levanta y nunca SI corre. 7/7 gates OK, 395 tests verdes, CI success. Cline nativo (no Docker): CLINE_DIR aislado en projects/cline/.cline-local para no tocar ~/.cline con la sesion OAuth del usuario. Servidor de Cline CERRADO al cierre (dashboard y daemon detenidos; config y sesiones conservadas). Queda pendiente la sesion de sudoku que el usuario empezo por el chat y quedo failed por un error propio (yo habia borrado el /tmp que era su cwd); se preservo y se movio al sandbox, y no se retomo.

## Proximos pasos

1. Retomar la sesion de sudoku de Cline desde Sessions (quedo preservada y con cwd en projects/cline-sandbox).\n2. Si el usuario quiere Cline en un proyecto real: borrar las sesiones viejas (el workspace del chat lo hereda de la sesion mas reciente) y arrancar con ./scripts/cline-tool.sh up apuntando al proyecto.\n3. Decidir el destino de PR-Agent: quedo registrado en el CHANGELOG como descartado, con la evidencia en docs/evaluacion/pr-agent-2026-10-20.md, pero el proyecto sigue en projects/.

## Decisiones y contexto que no debe perderse

- Cline corre NATIVO, no en Docker: el build exige Bun 1.4.2 y parches de dependencias (patches/ollama-ai-provider-v2@4.0.1.patch), y el daemon del hub es un proceso nativo. El aislamiento se logra con CLINE_DIR + --cwd, sin el overhead del contenedor.\nEl registro de herramientas se reconstruyo COMO DUENO INDEPENDIENTE, no dentro del commit de Onyx: el borrado anterior fue por scope ('no es de Onyx'), y el defecto de fondo era el TEST (afirmaba existencia de rutas del host y rompio el CI), no el registro.\nEl test ahora afirma FORMAS (ruta absoluta, nombre de compose, camino de levantamiento) y no existencia: un compose puede no estar instalado en la maquina que corre el test y el registro seguir siendo correcto.\nCline tiene wrapper propio (scripts/cline-tool.sh) porque el up/down generico del registro no alcanza: son dos procesos y el dashboard no para el daemon.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
