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

## Ollama como proveedor != modelo local: leer el pedido antes de elegir el modelo

En varios pedidos de clon+configurar de la sesion del 2026-10-20 (opencode, browser-use, milvus, PR-Agent, Chatterbox), Gonzo aclaro la misma cosa: "no hace falta que use los modelos locales, me referia a que corra desde Ollama". El "desde Ollama" no significa "modelo local": significa que el **proveedor** es Ollama, da igual si el modelo concreto es local o cloud servido por Ollama, porque ambos llegan por la misma API (OpenAI-compatible en /v1, nativa en /api/chat). Interpretarlo como "usa un LLM local" tira la sesion hacia donde no va: se instalan modelos locales, se eligen GPU o no, y se pierde el punto.

Corolario: cuando el pedido dice "configurarlo con X", la pregunta que hay que responder primero es **"¿que componente tiene que hablar con X?"**, no "¿que modelo corre?". Si la respuesta es "el server habla con el daemon por la API de X", el modelo se elige despues y es un parametro.

Concreto en el caso Chatterbox: la aclaracion cambio el encargo de "armar un server que consulte a un LLM local" a "que el TTS se sirva con la forma de la API de Ollama" (POST /v1/audio/speech), que es un contrato de endpoint, no una eleccion de modelo.

---

