# Learnings - integracion

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## PR-Agent + Ollama en Docker: bearer por TOML (no env var) y presupuesto de salida holgado para modelos de razonamiento <!-- project: github.com/gonzoblasco/workspace_openclaw -->

PR-Agent + Ollama: dos trampas de integracion verificadas el 2026-10-20 al montar
The-PR-Agent/pr-agent en Docker contra el server de Ollama del host.

1) El bearer NO puede ir por env var. Dynaconf reconstruye una seccion desde las env
vars de esa seccion cuando se la toca (al importar pr_agent.mosaico.server), y en
ese camino se pierde el decodeo "@json": el valor queda como str crudo y
MosaicoAuthenticationBackend aborta el arranque con "mosaico.bearer_tokens must map
principal names to distinct bearer secrets". Aislado: por env var -> str; por
TOML (.secrets.toml) -> DataDict (Mapping), con y sin otras vars de la misma
seccion. Solucion: [mosaico] en el .secrets.toml montado.

2) Los modelos de razonamiento (gpt-oss) consumen el presupuesto en el bloque
reasoning. Con max_tokens chico devuelven content:"" y finish_reason:length, sin
error visible. Con CONFIG__MAX_OUTPUT_TOKENS=16000 responden bien.

Tambien: los :cloud de Ollama (proxy, no local) son la via para usar Ollama sin
cargar RAM local; host.docker.internal:11434 desde el container. Y el clone por
git deja los archivos en 600, que el container (UID 10001) no puede leer: hay
que chmod a+rX antes de build.

3) Los presupuestos de timeout del health probe tienen que estar escalonados:
server (mosaico.health_timeout_seconds) > cliente HTTP > timeout del healthcheck
de Docker. Medido: el probe tardo hasta 17s bajo carga; con el cliente cortando
antes (25s vs 30s del server) el container caia a unhealthy con un 503
"Unhealthy: LLM probe failed" aunque el server respondiera bien. Un 503 aislado
es timeout transitorio, no caida: reintentar antes de diagnosticar.

4) Modo plain-diff (--diff-file / --stdin): no necesita token de GitHub ni URL de PR,
y es la via para probar la CLI nativa. Corriendo el comando DESDE el repo que contiene
los archivos, PR-Agent los lee del disco y aplica el diff en reversa para reconstruir la
version base: con base y head completos el modelo tiene contexto real del archivo, no
solo los hunks. Los flags --output / --json-output tienen que ir ANTES del comando, o el
CLI imprime el help y no ejecuta nada.

5) Un hunk con el conteo de lineas mal escrito (a mano) revienta unidiff con PatchSet
error, y el CLI tambien imprime el help en vez de fallar claro. Generar el diff con
git diff, no escribirlo a mano. Diagnostico: si el CLI imprime el help, el error real
esta arriba en el log (capturar head, no tail).

---

## Ollama como proveedor != modelo local: leer el pedido antes de elegir el modelo

/tmp/learning_ollama.md

---

