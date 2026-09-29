# Cata de codigo: K-esimo mas pequeno en subarray (N=2e6, Q=500k)

> Exportado automaticamente desde kanam-lab el 2026-09-16 20:52.
> Metodologia: mismo prompt VERBATIM; harness ejecutable con suite oculta
> (test del test validado contra solucion de referencia ANTES de medir);
> checksum de 500k queries como testigo de correccion.
> 7 corridas registradas.

## Resultados (orden: query mas rapida primero)

| # | Plataforma / modelo | Familia de solucion | PASS | Build (ms) | 500k q (ms) | RAM (MB) | Checksum |
|---|---|---|---|---|---|---|---|
| 1 | Z.ai GLM-5.3 Deep Think Low | WM prefijo completo | PASS | 282 | 135 | 322 | `-10947250751335` |
| 2 | Kimi K-Instant (Razonamiento) | WM bitmap + compresion | PASS | 209 | 164 | 185 | `-10947250751335` |
| 3 | DeepSeek Free Tier (Pensamiento Profundo) | WM bitmap + compresion | PASS | 212 | 177 | 186 | `-10947250751335` |
| 5 | Gemini 3.1 Pro | PST iterativo | PASS | 295 | 353 | 529 | `-10947250751335` |
| 6 | Gemini 3.6 Flash | PST iterativo | PASS | 320 | 466 | 529 | `-10947250751335` |
| 4 | ChatGPT (tier gratuito) | WM 31 niveles fijos (sin compresion) | PASS | 177 | 625 | 185 | `-10947250751335` |
| 7 | gemma4:31b-cloud (OpenClaw/Ollama) | PST recursivo | PASS | 552 | 712 | 523 | `-10947250751335` |

## Notas por corrida

- **#1 Z.ai GLM-5.3 Deep Think Low:** Documento el trade-off prefijo-vs-bitmap y la medicion lo confirmo en vivo (135ms/322MB vs 164ms/185MB de Kimi). Mas rapido en queries; RAM intermedia. Unico que cuantifica el cruce para elegir otro algoritmo. Flanco: no trajo I/O.
- **#2 Kimi K-Instant (Razonamiento):** Mejor balance del torneo (164ms/185MB). Transparencia de ejecucion: declaro que su TS no corrio y valido con prototipo Python (30k consultas, 0 fallos). Analisis numerico int32/double mas completo.
- **#3 DeepSeek Free Tier (Pensamiento Profundo):** Mismo perfil que Kimi. Ningun claim de timing inventado; memoria estimada exacta. Unico en no filtrar metadata del system prompt en la respuesta. Manejo explicito del borde 1<<31.
- **#5 Gemini 3.1 Pro:** PST iterativo + centinela: el mejor de la familia PST (353ms pero 529MB). Refuto el WM estimando 744MB - se le confirmo en la practica (~529MB). Acierto doble en el trampa de Number. Filtro metadata del system prompt.
- **#6 Gemini 3.6 Flash:** Correcto, pero el claim '40ns/query' es fisicamente imposible: medido 932ns/query (23x). El PST mas lento en queries pese al tag 'flash'. Validacion defensiva de rangos (unico en hacerla). RAM 529MB igual que su hermano Pro.
- **#4 ChatGPT (tier gratuito):** Correcto pero paga 3.8x en queries por no comprimir coordenadas (625ms vs ~170ms de los WM comprimidos), misma RAM (185MB). Detalle fino de V8 excelente (FastScanner, chunks de output). Refutacion del PST con numeros confirmados en la practica.
- **#7 gemma4:31b-cloud (OpenClaw/Ollama):** PASS pero ultimo del torneo (712ms/523MB). Estimo su memoria en 1.2GB cuando la estructura real son 600MB (50M nodos) y el margen contra el buffer es fino (~1.8M nodos). Build recursivo lento (4M llamadas).

## Lecciones de la cata

- Los Wavelet Matrix ganan por memoria (3x vs PST: ~185MB vs ~520MB).
- Dentro de WM, la compresion de coordenadas es obligatoria (3.8x en queries).
- Prefijo completo vs bitmap es un dial: velocidad (GLM) vs memoria (Kimi/DeepSeek).
- La RAM es la metrica estable entre corridas; los tiempos varian +-2x con la maquina:
  registrar la varianza, no un punto unico.
- Cifras de rendimiento inventadas (40ns/query de Gemini 3.6 Flash, 1.2GB de gemma):
  verificar contra medicion propia antes de creerlas.
