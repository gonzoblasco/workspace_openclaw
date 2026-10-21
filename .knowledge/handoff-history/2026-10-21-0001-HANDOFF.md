# HANDOFF - workspace

**Fecha:** 2026-10-21 00:01 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-21). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-21.md`.

---

## Que se hizo en esta sesion

Deploy de AnythingLLM v1.18.0 con Ollama en Docker, verificado end-to-end y endurecido.

**Que se hizo:**
- Repo clonado en ~/projects/anything-llm (HEAD feb0ebe8, 2026-10-19), solo lectura. Imagen oficial prebuilt mintplexlabs/anythingllm (arm64) en vez de compilar desde fuente.
- Deploy aislado en ~/anythingllm-data/ (compose + .env + storage/), fuera del workspace. Contenedor en 127.0.0.1:3001 (solo loopback).
- Ollama como PROVEEDOR: LLM `minimax-m3.1-flash:cloud` (cloud servido por la API de Ollama, con tools+thinking+vision), embeddings `qwen3-embedding:0.6b` (local), vector store LanceDB.
- Verificado end-to-end: chat real (respondio 'Azul', model minimax-m3.1-flash:cloud, provider OllamaAILLM) y RAG real (documento subido, vectorizado, y respuesta con sources score 0.67).
- Hardening aplicado tras revision adversarial: AUTH_TOKEN + JWT_SECRET (API paso de 200 abierto a 401), DISABLE_TELEMETRY, DISABLE_SWAGGER_DOCS, OLLAMA_MODEL_TOKEN_LIMIT 32768 -> 131072, OLLAMA_EMBEDDING_BATCH_SIZE 1 -> 8, mounts de collector/hotdir y collector/outputs, compose sin `version:` obsoleto.
- Servidor parado con `docker compose stop` (datos intactos: 480K, anythingllm.db sano).

**Hallazgos y trampas (importantes para retomar):**
- El subagente que edito el .env trunco el SIG_KEY (copio la forma redactada). Si el container hubiera arrancado asi, la base quedaba ilegible. Detectado comparando contra el backup .env.bak.20261020-173023, restaurado y verificado identico (64 chars).
- El .env lo REESCRIBE la app (dumpENV) cuando se guardan settings desde la UI. Orden obligatorio: down -> editar .env -> up. AUTH_TOKEN/JWT_SECRET/SIG_KEY/SIG_SALT estan en protectedKeys y sobreviven, pero el archivo se reordena.
- CORS reflectivo sigue activo (Access-Control-Allow-Origin refleja cualquier Origin), pero el vector real quedo cerrado por el AUTH_TOKEN (401 sin credencial).
- El health check que registraba ai-toolbox apuntaba a /api/health, endpoint que NO existe en AnythingLLM. Corregido a /api/ping.
- Single-user mode: no hay pantalla de onboarding (markOnboarded.js marca completo al detectar LLM_PROVIDER). La password es el AUTH_TOKEN.
- Falla intermitente 'too many concurrent requests' del cloud de Ollama cuando el RAG dispara embedding de query y completion a la vez. Reintentar funciona.

**Estado final:** contenedor detenido, datos persistidos, ~/anythingllm-data/README.md con credenciales y trampas, docs/tools/REGISTRY.md y MEMORY.md actualizados.

## Estado actual

AnythingLLM desplegado, verificado y endurecido en ~/anythingllm-data/. Contenedor parado (docker compose stop), datos intactos. LLM minimax-m3.1-flash:cloud via Ollama, embeddings qwen3-embedding:0.6b local, LanceDB. Password = AUTH_TOKEN del .env. Levantar: cd ~/anythingllm-data && docker compose up -d

## Proximos pasos

- Levantar cuando haga falta: `cd ~/anythingllm-data && docker compose up -d` (o `python3 scripts/ai-toolbox.py up anythingllm` desde el workspace)
- Opcional: cambiar el AUTH_TOKEN por algo mas memorable que Gonzo pueda tipear sin mirar (no se hizo sin que lo elija)
- Opcional: backup programado del directorio storage/ (datos + .env con SIG_KEY/SIG_SALT)
- Opcional: documentar en un .knowledge/ propio si el deploy deja de ser una tool mas del inventario

## Decisiones y contexto que no debe perderse

- Decisiones tomadas por Gonzo: (1) usar Docker para no ensuciar el host; (2) Ollama como PROVEEDOR, no necesariamente con modelos locales - el LLM es cloud servido por la API de Ollama. El deploy quedo aislado en ~/anythingllm-data/ (fuera del workspace), no en projects/.

## Archivos tocados

```
.knowledge/HANDOFF.md
.knowledge/SESSIONS.md
.knowledge/handoff-history/2026-10-20-1201-HANDOFF.md
MEMORY.md
docs/CHANGELOG.md
docs/archive/CHANGELOG-archive.md
docs/tools/REGISTRY.md
memory/2026-10-20.md
memory/memory.db
scripts/ai-toolbox.py
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-21.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
