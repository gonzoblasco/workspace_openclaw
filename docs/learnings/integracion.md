# Learnings - integracion

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Dos trampas de LiteLLM+Ollama que valen mas alla del proyecto que las origino: el decodeo @json de Dynaconf y el budget de los modelos de razonamiento

Dos trampas genericas que aparecieron al integrar un LLM via Ollama con
LiteLLM (verificadas 2026-10-20). El caso que las origino (PR-Agent) se descarto,
pero las lecciones son de las librerias, no del proyecto: valen para cualquier
integracion con LiteLLM + Ollama.

1) Dynaconf pierde el decodeo "@json" de una env var cuando reconstruye la
seccion desde el entorno. Si el valor es `@json {"a":"b"}` y otra env var de la
MISMA seccion toca la seccion, el valor queda como string crudo y el consumidor
que espera un dict falla. Aislado: por env var -> str; por TOML (.secrets.toml)
-> DataDict (Mapping), con y sin otras vars de la misma seccion. Si algo espera
un dict de una env var, ponerlo en TOML.

2) Los modelos de razonamiento (gpt-oss y familia) consumen el presupuesto de
tokens en el bloque `reasoning`. Con max_tokens chico devuelven `content:""` y
`finish_reason:length` **sin error visible**: parece un fallo de la app, pero
es el modelo consumiendo el budget antes de responder. Con max_tokens holgado
(16000) responden bien. Sintoma: respuesta vacia sin excepcion.

---

## Ollama como proveedor != modelo local: leer el pedido antes de elegir el modelo

/tmp/learning_ollama.md

---

