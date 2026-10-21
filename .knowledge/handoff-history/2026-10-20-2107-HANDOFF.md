# HANDOFF - workspace

**Fecha:** 2026-10-20 21:07 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Chatterbox TTS servido con la API de Ollama: se implemento, se verifico (8/8 smoke, end-to-end con el codigo real de OpenClaw) y **se borro completo a pedido de Gonzo**. Aprendizaje transversal: 'configurarlo con Ollama' = el proveedor es Ollama (local o cloud), no 'usar un modelo local'.

## Estado actual

Todo el rastro de Chatterbox eliminado: servicios launchd, plists, proyecto (1.3G), cache (2.5G), imagen+volume Docker, modelos Ollama (9.6G + 189M), seccion tts de openclaw.json y 6 WAV de prueba. 7 archivos que lo listaban como vivo corregidos. 2 referencias legitimas conservadas. Config del gateway revalidada.

## Proximos pasos

1. Nada pendiente: el encargo esta cancelado por decision de Gonzo. Si vuelve a pedirlo, el camino esta documentado en el chat de la sesion 2026-10-20: recompilar el POC de llama.cpp (PR #107, rama pascal/poc-chatterbox), endpoint POST /v1/audio/speech, y apuntar tts.providers.openai.baseUrl al server local. Ojo: Docker no sirve en esta maquina por OOM (7.7 GiB de limite, 3.4 ya usados por 12 contenedores ajenos) -> nativo, que ademas tiene MPS.

## Decisiones y contexto que no debe perderse

1) Docker descartado por OOM medido (ExitCode=137); nativo con MPS. 2) 'servir desde Ollama' = contrato de endpoint /v1/audio/speech, no eleccion de modelo. 3) El TTS de Chatterbox no existe como release: solo hay un PR sin mergear, y su sidecar de xOllama no lo soporta. 4) Se borro con 'trash' lo reversible, pero los 5G de pesos/imagen Docker no pasan por la Trash: no hay vuelta atras.

## Archivos tocados

```
MEMORY.md
docs/CHANGELOG.md
docs/SETUP.md
docs/learnings/README.md
docs/learnings/docker.md
docs/learnings/pipeline-agentes.md
memory/2026-10-19.md
memory/2026-10-20.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
