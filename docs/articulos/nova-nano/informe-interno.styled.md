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

# hf.co/ModernoTech/Nova-Nano:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | hf.co/ModernoTech/Nova-Nano:Q4_K_M | declarado |
| Cuantización | Q4_K_M | declarado |
| Contexto declarado | 128000 | declarado |
| Contexto de corrida | 8192 | medido |
| think | false | medido |
| num_predict | null | medido |
| Fecha de evaluación | 2026-11-05 | medido |

## Mediciones
| Prueba | Segundos | Tokens de salida |
|---|---|---|
| c1_funcion_simple | 0.38 s | 86 |
| c2_texto_corto | 0.14 s | 29 |
| c3_debug_facil | 0.58 s | 136 |
| c4_completar | 0.12 s | 27 |
| c5_clasificar | 0.11 s | 23 |
| c6_instruccion_exacta | 0.02 s | 3 |
| c7_aritmetica | 0.02 s | 2 |
| c8_resumen | 0.23 s | 47 |

## Prueba por prueba
| Prueba | Veredicto | Severidad |
|---|---|---|
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | INCOMPLETO | media |
| c3_debug_facil | FALSO | critica |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | CORRECTO | ninguna |
| c6_instruccion_exacta | FALSO | alta |
| c7_aritmetica | FALSO | critica |
| c8_resumen | CORRECTO | ninguna |

### Evidencia citada

**c1_funcion_simple.** `return n % 2 == 0`

**c2_texto_corto.** `Rioplatense, git pull es cuando el repositorio actual se actualiza con los cambios de otro lugar.` — no menciona fusión/integración en branch local; no usa voseo/registro rioplatense

**c3_debug_facil.** `se pasa una lista vacía, lo que genera un TypeError` — causa real es división por cero; fix `return sum(nums) / len(nums)` no maneja lista vacía

**c4_completar.** `if not nums: return None return max(nums)`

**c5_clasificar.** `1. POSITIVA 2. NEGATIVA 3. NEUTRA`

**c6_instruccion_exacta.** `OK nada` — exigido exactamente `OK`

**c7_aritmetica.** `529` — esperado 1081

**c8_resumen.** `El sistema cayó tres veces durante la madrugada, y el equipo de guardia detectó un disco lleno, liberando espacio y volviéndose a la normalidad a las 6 de la manana.`

## Modo de falla dominante
`falso_seguro` + `fuera_de_alcance`

Justificación: 3 de 8 pruebas fallan por contenido invertido con redacción segura o desobediencia de formato. 2 de 8 son `falso_seguro` puro (c3_debug_facil: TypeError inventado, c7_aritmetica: 529 en vez de 1081). 1 de 8 es `fuera_de_alcance` (c6_instruccion_exacta: agrega "nada" a salida literal). c2_texto_corto también es `fuera_de_alcance` parcial (ignora registro pedido).

## Riesgos
1. **Diagnóstico falso con confianza:** Atribuye ZeroDivisionError a TypeError y propone fix que no corrige. Mitigación: sin mitigación conocida en esta configuración.
2. **Aritmética no fiable:** Error de cálculo 529 vs 1081 sin señal de incertidumbre. Mitigación: derivar cálculo a herramienta externa; no usar para cómputo.
3. **No obedece instrucciones literales:** Falla en `OK` exacto (añade token). Mitigación: sin mitigación conocida; validar con post-procesamiento estricto y rechazo.
4. **Registro/locale no sostenido:** No produce voseo rioplatense aunque lo etiqueta. Mitigación: sin mitigación conocida.
5. **Contexto no verificado:** Declarado 128000, medido solo 8192. Riesgo de degradación fuera de ventana medida. Mitigación: medir a 32k/128k antes de cualquier uso con contexto largo.

## Configuracion recomendada
Modelo hf.co/ModernoTech/Nova-Nano:Q4_K_M con think=false, ctx=8192, temperatura NO_VERIFICABLE — no funciona de forma fiable para razonamiento, aritmética ni instrucciones exactas. No hay configuración recomendada para adopción general. Para tareas aisladas de generación simple (c1, c4) y clasificación/resumen (c5, c8) operó correctamente con latencias 0.11-0.38 s, pero sin garantías fuera de esos casos.

## Pendientes
- Medir contexto real >8192 hasta 128000 declarado (NO_VERIFICABLE)
- Medir aritmética multi-paso y diagnóstico de errores con suite ampliada
- Medir obediencia a formato con pruebas de instrucción exacta adicionales
- Medir variación con temperatura y think=true
- Medir latencia y estabilidad con carga concurrente

