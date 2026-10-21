# HANDOFF - workspace

**Fecha:** 2026-10-20 23:13 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Milvus 3.0.3 + Ollama: clonado, configurado, verificado end-to-end y DESCARTA﻿DO por decision de Gonzo. Se borro todo (containers, red, imagenes por ~3 GB, projects/milvus y projects/milvus-ollama con trash) y se registro el porque en docs/ecosystem/milvus-decision.md (commit 9f1fc96cf8, pre-commit 15 PASS / 0 FAIL). La integracion funciono a la primera: embeddings server-side de Milvus via el provider openai contra el endpoint OpenAI-compatible de Ollama del host (qwen3-embedding:0.6b, 1024 dims), verificado con diff maximo 0.000000 contra el embedding crudo del host. El descarte no fue por dificultad de configurarlo sino por sobreingenieria: la capacidad ya estaba cubierta por SQLite+embeddings en scripts/memory-search.py, ChromaDB en projects/langchain-starter y pgvector en projects/soporteml. Hallazgos verificados que sobreviven a la herramienta: Milvus 3.x no tiene provider ollama (el openai si funciona contra /v1/embeddings); la URL del provider sale solo de function.textEmbedding.providers.openai.url en user.yaml y no de los params de la funcion; la clave de cache real es queryNode.cache.memoryLimit (common.cache.* no existe en 3.0.3 y se ignora en silencio); el etcd embebido se corrompe con SIGKILLs y entra en loop con panic leader changed (fix: borrar volumes/milvus/etcd); Ollama NO puede correr Milvus como app (ollama launch solo lanza agentes de codigo, la doc completa de 247 KB tiene 0 menciones de milvus, ollama.com/apps da 404). Ademas se limpio el registro de herramientas IA (entrada milvus fuera de scripts/ai-toolbox.py, docs/tools/REGISTRY.md y skills/ai-toolbox/SKILL.md: declaraba un compose borrado y estado corriendo falso) y se confirmo el veredicto de tier 3 del triage OSS con la evidencia nueva. Se repararon dos learnings con contenido roto en la DB: el 286 apuntaba a /tmp/learning_ollama.md (contenido efimero) y el 284 estaba truncado a 500 caracteres a media palabra. Se creo el learning transversal 290 "Instalar y verificar no es adoptar".

## Estado actual

El stack de herramientas IA quedo en 10 entradas (Ollama, Onyx, browser-use, AnythingLLM, LiteLLM, Vane, opencode, OpenHands, Cline, y el resto). Milvus ya no esta. El repo projects/milvus (clon shallow del upstream) y projects/milvus-ollama (compose + config + scripts) se movieron a la papelera con trash, reversibles desde ~/.Trash. Backups en /tmp/milvus-retiro/ (compose, user.yaml, test_e2e.py, README) y /tmp/milvus-etcd-backup-224137.tgz. Docker quedo con 0 rastros: sin containers, sin imagenes, sin red, sin volumenes de Milvus. El resto del stack sigue sano: onyx, vane, anythingllm, litellm_ollama, openhands-canvas, opencode, ollama nativo.

## Proximos pasos

1. El learning transversal 290 quedo registrado en la DB y las vistas de docs/learnings/ se regeneraron (244 lecciones en total). La idea: instalar y verificar no es adoptar; el benchmark dice si funciona, no si lo necesitamos, y re-litigar un descarte exige un hecho nuevo (volumen real), no curiosidad. Proximo paso natural: elegir UN proyecto de producto y cerrarlo con un flujo end-to-end que un cliente real pueda usar, en vez de sumar infraestructura. El vectorstore ya esta cubierto y no es el cuello de botella.

## Decisiones y contexto que no debe perderse

- Decision de Gonzo: "no lo usaremos, es demasiado para nosotros" - Milvus queda fuera del stack, no se adopta, no se integra, no se mantiene. Motivo registrado: no fue la dificultad de configurarlo (funciono a la primera, verificado end-to-end) sino que la capacidad ya estaba cubierta en tres lugares del workspace y la complejidad de una base de datos distribuida no se justifica sin volumen real. Se maintains el criterio de re-litigacion: solo vuelve si el volumen real hace doler la alternativa actual. Precedente de formato: mismo patron que el descarte de PR-Agent (evaluado con verdad de base y juez, decidido con el dato, borrado y documentado). Ademas: se aplico trash y no rm a los directorios de proyecto, y se committeo sin push pendiente de OK explicito.

## Archivos tocados

```
docs/learnings/README.md
docs/learnings/integracion.md
docs/learnings/metodologia.md
docs/learnings/pipeline-agentes.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
