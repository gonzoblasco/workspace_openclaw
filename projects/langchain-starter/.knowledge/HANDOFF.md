# HANDOFF - langchain-starter

## Session Context
- **Date:** 2026-09-24
- **Project:** langchain-starter
- **Branch:** main
- **Repo:** https://github.com/gonzoblasco/langchain-starter (PRIVADO, creado 2026-09-24)

## Estado

Starter kit de IA local sobre LangChain, completo y en produccion interna. Corre como servicio permanente del Mac Mini.

| Pieza | Archivo | Estado |
|---|---|---|
| Hello World (validacion de conexion) | `app/main.py` | verificado |
| API FastAPI | `app/api.py` | `/`, `/health`, `/chat` (streaming), `/ingest`, `/docs` |
| RAG | `scripts/{ingest,store,query}.py` | verificado end-to-end |
| Agente ReAct | `scripts/agent.py` | tools en paralelo verificadas |
| Servicio | `scripts/service.sh` + `watchdog.sh` | LaunchAgent con recuperacion automatica |

## Decisiones

- **Python + LangChain**, Ollama local (no OpenAI), ChromaDB local primero. Full razonamiento en `LANGCHAIN_STRATEGY.md` (workspace).
- **LaunchAgent nativo**, no Docker, para el Mac Mini. `Dockerfile` queda escrito para despliegue futuro.
- **Watchdog que respeta el apagado intencional:** `service.sh stop` deja `.intentional-stop` y el watchdog no revive; `start` limpia el marcador.
- **El prompt del RAG responde solo con el contexto recuperado** (si no esta en los documentos, lo dice).

## Versionado (2026-09-24)

Repo creado y pusheado. Antes de esto el codigo existia **solo en disco**.

Deuda cerrada en el mismo paso:
- `requirements.txt` estaba **vacio (0 bytes)** -> ahora 15 dependencias de nivel superior con version fija del venv real.
- `README.md` tenia 8 bytes -> documentacion real (arquitectura, instalacion, endpoints, servicio).
- `.env.example` estaba vacio -> contrato de configuracion completo.

**No versionado (por `.gitignore`):** `venv/` (332 MB), `logs/`, `config/chroma_db/`, `.env`.
**Regla del triple git:** el repo del proyecto excluye `.knowledge/` via `.git/info/exclude`; esa memoria vive en el workspace git.

## Próximo paso

1. **Migrar a Python 3.12** (el venv es 3.9.6, heredado del sistema y al final de su vida).
2. **Tests** de los caminos criticos (chunking, retrieval, endpoint `/chat`).
3. **Migracion a Supabase Vector** cuando haya que compartir conocimiento entre maquinas (hoy Chroma local alcanza).
4. Ingesta de documentos reales mas alla del doc de estrategia (hoy la coleccion `starter_knowledge` tiene 10 chunks).

## Open Questions

- ¿Se migra a `sqlite-vec` en algun momento, para alinear con el stack de vectores de `memory.db` (ADR-057, ADR-062)? Hoy Chroma alcanza.
- El `venv` de este proyecto lo **reusa `kanam-insight`**. Si se recrea o muda, ese acoplamiento importa; conviene un `requirements.txt` propio en kanam-insight.

## Lecciones

- **`KeepAlive` con `SuccessfulExit=false` no revivir un proceso que sale limpio.** La primera version del plist tenia eso: uvicorn salia con 0 y launchd lo daba por terminado. Ahora `KeepAlive=true` incondicional.
- **El plist debe lanzar el proceso directo, no un script que hace `exec`.** Lanzar `service.sh start` creaba uvicorns fuera de launchd que peleaban por el puerto (`address already in use`).
- **El contrato del script payload de OpenClaw:** el output de `exec` se lee en `res.aggregated` (no `stdout`) y el resultado se devuelve con `json({...})`. Adivinar el contrato costo varios intentos fallidos; leer el codigo instalado lo resolvio en un minuto.

---

*Generado por session-lifecycle workflow*
