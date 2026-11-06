<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; vertical-align: top; word-wrap: break-word; }
th { background: #f4f6f4; font-weight: 600; }
td:nth-child(1) { width: 40%; } td:nth-child(2) { width: 38%; } td:nth-child(3) { width: 22%; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; word-break: break-word; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; line-height: 1.45; }
pre code { background: none; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 1.6em auto; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

# hf.co/bartowski/SmolLM2-360M-Instruct-GGUF:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** ADOPTAR COMO ESPECIALISTA
**Uso recomendado:** solo generacion de funciones Python acotadas con guarda de lista vacia (c1, c3, c4)

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | hf.co/bartowski/SmolLM2-360M-Instruct-GGUF:Q4_K_M | declarado |
| Cuantizacion | Q4_K_M | declarado |
| Contexto maximo | 8192 | declarado |
| Contexto de corrida | 8192 | medido |
| think | false | medido |
| num_predict | null (sin limite) | medido |
| Temperatura | NO_VERIFICABLE | inferido |
| Parametros totales | NO_VERIFICABLE | NO_VERIFICABLE |
| Licencia | NO_VERIFICABLE | NO_VERIFICABLE |

## Mediciones
| Prueba | Segundos | Tokens de salida |
|---|---|---|
| c1_funcion_simple | 1.07 s | 82 |
| c2_texto_corto | 0.64 s | 80 |
| c3_debug_facil | 0.94 s | 156 |
| c4_completar | 0.21 s | 26 |
| c5_clasificar | 0.51 s | 87 |
| c6_instruccion_exacta | 0.14 s | 22 |
| c7_aritmetica | 0.09 s | 13 |
| c8_resumen | 0.38 s | 60 |

## Prueba por prueba
| Prueba | Veredicto | Severidad |
|---|---|---|
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | FALSO | alta |
| c3_debug_facil | CORRECTO | ninguna |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | FALSO | alta |
| c6_instruccion_exacta | FALSO | alta |
| c7_aritmetica | FALSO | alta |
| c8_resumen | CORRECTO | ninguna |

### Evidencia citada

**c1_funcion_simple.** `return n % 2 == 0`

**c2_texto_corto.** "Utilizar el comando `git pull` para actualizar las claves y compartir las buenas versión de tu repositorio."

**c3_debug_facil.** "The `sum` function will raise a `ZeroDivisionError` if the input list is empty." + `if not nums: return 0`

**c4_completar.** `if not nums: return None` / `return max(nums)`

**c5_clasificar.** "1. Me encanto el trato, volveria. 2. Tardo tres horas y nadie me aviso. 3. El local esta en la calle San Martin." — sin etiqueta

**c6_instruccion_exacta.** "Un cuidado con la oración OK y no importa nada más." — no devuelve solo `OK`

**c7_aritmetica.** "47 * 23 = 1101" — correcto es 1081

**c8_resumen.** "El sistema se cayo tres veces durante la madrugada y el equipo de guardia detecto que un disco estaba lleno; se libero espacio y volvio a la normalidad a las 6 de la manana."

## Modo de falla dominante
`falso_seguro` + `fuera_de_alcance`. Justificacion: 4 de 8 pruebas fallan. 2 de 8 por `falso_seguro` (c2 inventa definicion de `git pull`, c7 entrega 1101 con confianza), 2 de 8 por `fuera_de_alcance` (c5 ignora formato `frase | etiqueta`, c6 ignora instruccion literal de devolver solo `OK`).

## Riesgos
1. **Riesgo:** Desinformacion tecnica con confianza (c2: `git pull` como "actualizar las claves"). Mitigacion: bloquear uso para documentacion/explicacion de comandos; requerir validacion humana.
2. **Riesgo:** Error aritmetico no detectado (c7: 47*23=1101 vs 1081). Mitigacion: no usar para calculo; derivar a calculadora/herramienta externa; sin mitigacion conocida dentro del modelo.
3. **Riesgo:** Incumplimiento de formato/registro (c5 no clasifica, c6 agrega texto, c2 no usa rioplatense). Mitigacion: no usar para pipelines que exijan formato estricto; agregar validador externo que rechace salidas fuera de esquema.
4. **Riesgo:** Falsa sensacion de competencia por acierto en codigo simple (3/3 en c1,c3,c4). Mitigacion: limitar a funciones acotadas verificadas con tests unitarios; sin mitigacion conocida para tareas compuestas.

## Configuracion recomendada
Modelo: hf.co/bartowski/SmolLM2-360M-Instruct-GGUF:Q4_K_M, think: false, num_ctx: 8192, num_predict: null, temperatura: NO_VERIFICABLE. No funciona bien con ninguna configuracion para obediencia literal, clasificacion o aritmetica (4/4 fallos en c2,c5,c6,c7 con ctx 8192 y think false). Solo utilizable en la configuracion medida para codigo simple.

## Pendientes
- Medir aritmetica multi-paso y con herramienta externa.
- Medir obediencia a formato JSON/CSV estricto con validador.
- Medir clasificacion con taxonomia controlada y registro rioplatense con mas prompts.
- Medir latencia y calidad con num_predict acotado y temperaturas distintas.
- Medir tareas de codigo no triviales (manejo de archivos, concurrencia, tests).

