# hf.co/ModernoTech/Nova-Mini:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** ADOPTAR COMO ESPECIALISTA
**Uso recomendado:** Generación de funciones Python triviales y corrección de errores sintácticos simples, sin tareas de comprensión/resumen/clasificación.

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | hf.co/ModernoTech/Nova-Mini:Q4_K_M | declarado |
| Cuantización | Q4_K_M | declarado |
| Contexto declarado | 40960 | declarado |
| Contexto de corrida | 8192 | medido |
| think | false | medido |
| num_predict | null (sin límite fijado) | medido |
| Temperatura | NO_VERIFICABLE | inferido |
| Fecha de evaluación | 2026-11-05 | medido |
| N pruebas corridas | 8 | medido |
| Tasa de acierto | 5/8 (62.5%) | medido |

## Mediciones
| Prueba | Segundos | Tokens de salida |
|---|---|---|
| c1_funcion_simple | 3 s | 268 |
| c2_texto_corto | 1.25 s | 180 |
| c3_debug_facil | 2.94 s | 416 |
| c4_completar | 2.14 s | 303 |
| c5_clasificar | 3.98 s | 535 |
| c6_instruccion_exacta | 0.62 s | 87 |
| c7_aritmetica | 1.65 s | 233 |
| c8_resumen | 1.64 s | 225 |

## Prueba por prueba
| Prueba | Veredicto | Severidad |
|---|---|---|
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | FALSO | alta |
| c3_debug_facil | CORRECTO | ninguna |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | FALSO | alta |
| c6_instruccion_exacta | CORRECTO | ninguna |
| c7_aritmetica | CORRECTO | ninguna |
| c8_resumen | FALSO | media |

### Evidencia citada

**c1_funcion_simple.** `def es_par(n): return n % 2 == 0`

**c2_texto_corto.** `Git Pull es un comando que te permite fetchar las últimas modificaciones de un repositorio remoto.`

**c3_debug_facil.** `El código falla porque, al pasar el parámetro [], se divide por 0 (el len([]) es 0).`

**c4_completar.** `def maximo(nums): if not nums: return None; return max(nums)`

**c5_clasificar.** `1. POS 2. NEUTRA 3. POS`

**c6_instruccion_exacta.** `OK`

**c7_aritmetica.** `1081`

**c8_resumen.** `El sistema se cayo tres veces durante la madrugada, detectó un disco lleno, liberó espacio y volvió a la normalidad a las 6 de la mañana.`

## Modo de falla dominante
`falso_seguro` + `fuera_de_alcance` en combinación.

Justificación con cuenta: 3 de 8 pruebas fallan. 2 de 3 fallos son `falso_seguro` (c5_clasificar y c8_resumen responden con confianza contenido invertido/inventado). 1 de 3 es `fuera_de_alcance` (c2_texto_corto ignora instrucción de registro rioplatense y definición incompleta). El patrón es respuesta fluida y segura aunque el contenido es falso.

Detalle:
- c5: clasifica `Tardo tres horas y nadie me aviso.` como NEUTRA cuando es NEGATIVA, y `El local esta en la calle San Martin.` como POS cuando es NEUTRA. Acierta 1 de 3.
- c8: cambia `tarde/noche` por `madrugada` y omite al guardia como actor.
- c2: define git pull solo como `fetchar` sin fusión, usa `fetchar` no rioplatense.

## Riesgos
1. **Alucinación en resumen:** inventa marco temporal (`madrugada` por `tarde/noche`) y omite actores. Mitigación: prohibir uso para resumen/síntesis; exigir verificación humana contra fuente.
2. **Clasificación invertida:** etiqueta sentimiento con 66% de error en muestra (2/3). Mitigación: no usar para clasificación de sentimiento/intención; sin mitigación automática conocida.
3. **Falsa seguridad:** redacción fluida oculta error (c5, c8). Severidad alta. Mitigación: forzar salida estructurada con cita literal obligatoria y score de confianza externo.
4. **Incumplimiento de registro/formato:** ignora `rioplatense` pedido (c2). Mitigación: validación post-hoc de estilo con lista de marcadores (voseo, léxico).
5. **Definición técnica incompleta:** git pull descrito solo como fetch. Mitigación: sin mitigación conocida para tareas de documentación técnica sin revisión.

## Configuracion recomendada
- modelo: `hf.co/ModernoTech/Nova-Mini:Q4_K_M`
- think: `false` (única configuración medida)
- num_ctx: `8192` (configuración de corrida; 40960 declarado NO_VERIFICABLE en esta evaluación)
- num_predict: `null` (sin límite)
- temperatura: NO_VERIFICABLE (no medida; usar 0 para tareas determinísticas hasta medir)

El modelo funciona con esa configuración solo para código trivial y obedecimiento literal (c1, c3, c4, c6, c7). No funciona bien con ninguna configuración medida para clasificación, resumen o registro rioplatense.

## Pendientes
- Medir con `num_ctx=40960` para verificar contexto declarado.
- Medir temperatura 0 vs 0.7 en c5 y c8 para estabilidad de alucinación.
- Medir tareas de código no trivial (con tests unitarios, edge cases, manejo de excepciones).
- Medir resistencia a prompt injection y manejo de contexto largo multi-turno.
- Medir costo real (tokens/s, memoria VRAM con Q4_K_M) en hardware objetivo.
