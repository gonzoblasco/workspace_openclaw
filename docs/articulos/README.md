# Artículos: reseñas de modelos LLM

Once modelos evaluados con el mismo método: batería de pruebas acotada, fuente
de verdad versionada, evaluador distinto del evaluado, y un artículo por modelo
en `.md` y `.pdf`.

Generado con `scripts/model-review.sh`. Cada carpeta tiene `articulo.md`,
`informe-interno.md` y sus PDFs.

## Modelos de código (batería de 7 pruebas)

| Modelo | Aciertos | Falla característica |
|---|---|---|
| [nova-core](nova-core/articulo.pdf) | 3/7 | Invirtió el consenso de Raft; no entrega p5 |
| [qwen2-5-coder-3b](qwen2-5-coder-3b/articulo.pdf) | 3/7 | Rechazo falso en soporte: "no puedo ayudarte con eso" |
| [gemma4-12b](gemma4-12b/articulo.pdf) | 6/7 | — |
| [qwen3-5-9b](qwen3-5-9b/articulo.pdf) | 5/7 | Invirtió el consenso de Raft |
| [nova-coder](nova-coder/articulo.pdf) | 3/7 | Invirtió el consenso de Raft |

## Modelos de bolsillo (batería de 8 pruebas, ≤1B)

| Modelo | Tamaño | Aciertos |
|---|---|---|
| [qwen2-5-1-5b](qwen2-5-1-5b/articulo.pdf) | 986 MB | **6/8** |
| [nova-mini](nova-mini/articulo.pdf) | 484 MB | 5/8 |
| [nova-nano](nova-nano/articulo.pdf) | 229 MB | 4/8 |
| [qwen2-5-0-5b](qwen2-5-0-5b/articulo.pdf) | 397 MB | 4/8 |
| [smollm2-360m](smollm2-360m/articulo.pdf) | 270 MB | 4/8 |
| [nova-spark](nova-spark/articulo.pdf) | 563 MB | 3/8 |

## Hallazgos que cruzan modelos

**El umbral está entre 0,8B y 1,5B.** Qwen2.5-1.5B es el único de la liga
chica que pasa el 75 %. Todo lo que está por debajo se queda en la mitad.

**Más parámetros no garantiza mejor resultado.** Nova-Spark (0,8B) saca 3/8,
menos que Nova-Nano (350M) con 4/8.

**La inversión del consenso se repite.** Nova-Coder, Nova-Core y Qwen3.5-9B
recomiendan no usar Raft con 3 nodos, cuando Raft tolera exactamente la caída
de 1 con 3 nodos. Los tres con formato impecable.

**Nova-Core no es lo que dice su nombre.** El archivo se llama
`Q4_K_M` y adentro declara `Q2_K`. También declara `architecture: gemma4`
cuando la ficha dice "transformer denso propio".

## Configuración de la corridas

- Hardware: Mac mini M4, 10 núcleos, 24 GB RAM.
- Temperatura 0, sin límite de tokens de salida.
- Contexto: 8.192 tokens para los densos de 3-4B (a 32.768 se colgaban).
- Tiempos medidos, no estimados.

---

*Once modelos, once artículos. Ninguno se comparó contra un modelo cloud: la
vara fue siempre la categoría.*
