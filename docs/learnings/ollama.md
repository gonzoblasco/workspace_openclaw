# Learnings - ollama

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## ollama-ai-provider-v2 v4 ignora options.num_ctx en creation-time: hay que pasarlo por providerOptions

En bolt.diy, app/lib/modules/llm/providers/ollama.ts pasaba num_ctx asi: ollamaProvider.chat(model, { options: { num_ctx } }). Con ollama-ai-provider-v2 v4.0.1 eso se IGNORA en silencio: el chat model lee num_ctx solo del bag call-time providerOptions.ollama.options (ver buildBaseArgs: 'options: ollamaOptions?.options', y ollamaOptions viene de parseProviderOptions(providerOptions) con provider:'ollama'). Verificado empiricamente: creation-time -> Ollama corre con el contexto nativo del modelo (262144 para gemma4) y 8.9GB de KV cache; call-time -> el contexto pedido (16384) y 7.7GB. Fix: agregar getProviderOptions() al provider y en stream-text.ts inyectar forwardedOptions.providerOptions = { ...forwardedOptions.providerOptions, ...providerOptions }. Detalle extra: getDefaultNumCtx leia solo serverEnv (bindings de workerd) y por eso DEFAULT_NUM_CTX del .env no llegaba; ahora fallback a process.env. Efecto: prefill de 5.3k tokens paso de ~130s (111 tok/s) a sub-segundo con el modelo ya cargado. <!-- project: github.com/gonzoblasco/workspace_openclaw -->

---

