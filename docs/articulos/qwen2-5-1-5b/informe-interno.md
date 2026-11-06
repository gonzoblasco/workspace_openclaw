# hf.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** ADOPTAR COMO ESPECIALISTA
**Uso recomendado:** Generación de código simple y ejecución de instrucciones literales

## Ficha
| Campo | Valor | Fuente |
| Modelo | hf.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M | declarado |
| Cuantización | Q4_K_M | declarado |
| Contexto declarado | 32768 | declarado |
| Contexto de corrida | 8192 | medido |
| think | false | medido |
| Temperatura | no especificada | NO_VERIFICABLE |
| num_predict | null | medido |

## Mediciones
| Prueba | Segundos | Tokens de salida |
| c1_funcion_simple | 2.42 | 96 |
| c2_texto_corto | 1.1 | 76 |
| c3_debug_facil | 2.06 | 146 |
| c4_completar | 0.76 | 51 |
| c5_clasificar | 0.35 | 18 |
| c6_instruccion_exacta | 0.07 | 2 |
| c7_aritmetica | 0.2 | 5 |
| c8_resumen | 0.56 | 34 |

Contexto declarado por el fabricante: 32768. Contexto de la corrida: 8192. Diferencia: -24576 tokens. Significa que la evaluación no verifica comportamiento en contexto largo; el rendimiento medido aplica solo hasta 8192.

No hay valor declarado de latencia o throughput para comparar. Tiempos medidos: 0.07 s a 2.42 s por prueba. Tokens de salida: 2 a 146.

## Prueba por prueba
| Prueba | Veredicto | Severidad |
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | FALSO | alta |
| c3_debug_facil | CORRECTO | ninguna |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | CORRECTO | ninguna |
| c6_instruccion_exacta | CORRECTO | ninguna |
| c7_aritmetica | CORRECTO | ninguna |
| c8_resumen | INCOMPLETO | media |

Evidencia c1_funcion_simple: `return n % 2 == 0` — implementación correcta de paridad.

Evidencia c2_texto_corto: `git pull es como un autobús que te lleva de la parada actual a la parada más cercana, sin necesidad de tomar el autobús de la parada anterior.` — analogía no describe fetch+merge del remoto.

Evidencia c3_debug_facil: `lo que divide por cero y produce un error` + `return 0  # Devuelve 0 si la lista está vacía` — diagnóstico y guarda correctos.

Evidencia c4_completar: `if not nums: return None` y bucle `if num > max_num` — guarda y lógica correctas.

Evidencia c5_clasificar: `1. POSITIVA 2. NEGATIVA 3. NEUTRA` — clasificación correcta.

Evidencia c6_instruccion_exacta: `OK` — obediencia literal.

Evidencia c7_aritmetica: `1081` — resultado correcto.

Evidencia c8_resumen: `El sistema se cayó tres veces durante la madrugada, liberó espacio y regresó a la normalidad a las 6 de la mañana.` — omite causa raíz disco lleno.

## Modo de falla dominante
`no_aplica`: no se detectó un modo dominante.

Justificación: 1 de 8 pruebas con `falso_seguro` (c2), 1 de 8 con omisión de causa (c8). 6 de 8 correctas. Sin patrón repetido que alcance mayoría.

## Riesgos
1. Explicaciones técnicas con analogías vacías en registro rioplatense — sin mitigación conocida; no usar para documentación o soporte.
2. Resúmenes omiten causa raíz (disco lleno) — mitigación: requerir checklist de causa en prompt y validación humana.
3. Contexto no verificado por encima de 8192 — mitigación: no desplegar con num_ctx >8192 sin medir.

## Configuracion recomendada
- modelo: hf.co/bartowski/Qwen2.5-1.5B-Instruct-GGUF:Q4_K_M
- think: false
- num_ctx: 8192
- num_predict: null (default)
- temperatura: NO_VERIFICABLE — no medir variación

Si se requiere explicación en lenguaje natural o resumen de incidentes, no funciona bien con ninguna configuración medida.

## Pendientes
- Medir con num_ctx 32768 para verificar contexto declarado.
- Medir tareas de código con dependencias externas y contexto multi-archivo.
- Medir robustez a instrucciones con negación y formato estricto adicional.
- Medir variación con temperatura y num_predict acotado.

