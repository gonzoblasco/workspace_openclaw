# hf.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** ADOPTAR COMO ESPECIALISTA
**Uso recomendado:** Generación de funciones Python triviales con guarda de vacío; ningún otro uso sin validación externa.

## Ficha
| Campo | Valor | Fuente |
| Modelo | hf.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF:Q4_K_M | declarado |
| Familia base | Qwen2.5-0.5B-Instruct | declarado |
| Cuantización | Q4_K_M (GGUF) | declarado |
| Parámetros | 0.5B | declarado |
| Contexto declarado | 32768 tokens | declarado |
| Contexto de corrida | 8192 tokens | medido |
| Think | false | medido |
| Temperatura corrida | no especificada (default) | inferido |
| num_predict corrida | null (sin límite) | medido |

## Mediciones

| Prueba | Segundos | Tokens de salida |
| c1_funcion_simple | 2.67 | 304 |
| c2_texto_corto | 0.74 | 110 |
| c3_debug_facil | 1.16 | 172 |
| c4_completar | 0.3 | 43 |
| c5_clasificar | 0.39 | 54 |
| c6_instruccion_exacta | 0.03 | 2 |
| c7_aritmetica | 0.12 | 5 |
| c8_resumen | 0.3 | 41 |

No hay valor declarado de latencia ni de tokens de salida para comparar. Tiempo total medido: 5.71 s para 8 pruebas. Latencia máxima medida: 2.67 s (c1). Latencia mínima medida: 0.03 s (c6). Carga inicial medida: 0.54 s (c1), 0 s en resto (modelo ya cargado).

## Prueba por prueba

| Prueba | Veredicto | Severidad |
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | FALSO | alta |
| c3_debug_facil | INCOMPLETO | media |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | FALSO | alta |
| c6_instruccion_exacta | CORRECTO | ninguna |
| c7_aritmetica | FALSO | crítica |
| c8_resumen | CORRECTO | ninguna |

Evidencia por prueba (cita textual de salida medida):

c1_funcion_simple: `return n % 2 == 0` — función correcta. La explicación contiene errores (afirma que 7 es par y 10 impar) pero no invalida el código pedido.

c2_texto_corto: "`git pull` es una operación que se utiliza para descargar el estado actual de un repositorio Git, actualizando los archivos y subversiones." — omite fusión en branch local, usa "subversiones" impreciso, registro neutro no rioplatense.

c3_debug_facil: "El código está mal porque intenta calcular el promedio de un conjunto de números vacío, lo que resultará en un error." — identifica síntoma (vacío) sin nombrar causa (división por cero / ZeroDivisionError).

c4_completar: `if not nums: return None ... return max(nums)` — implementación correcta con guarda.

c5_clasificar: "Tardo tres horas y nadie me aviso. | NEUTRA" y "El local esta en la calle San Martin. | POSITIVA" — 2 de 3 etiquetas invertidas.

c6_instruccion_exacta: "OK" — cumple instrucción literal sin texto adicional.

c7_aritmetica: "1161" — respuesta incorrecta; valor esperado 1081 para 47*23.

c8_resumen: "El sistema se cayó tres veces durante la madrugada, detectando un disco lleno que liberó espacio y volvió a la normalidad a las 6 de la mañana." — contiene las 3 piezas requeridas en una frase.

## Modo de falla dominante
`falso_seguro` — responde con confianza y contenido invertido.

Justificación: 3 de 8 pruebas (c2, c5, c7) entregan salida con formato correcto y tono seguro pero con contenido factualmente falso. c5 invierte 2 de 3 clasificaciones. c7 inventa 1161 por 1081. c2 define git pull sin mencionar merge. No hay casos de `no_entrega` (0 de 8) ni `fuera_de_alcance` puro en formato.

## Riesgos
1. **Cálculo inventado con formato válido.** c7 devuelve 1161 en lugar de 1081 sin señal de incertidumbre. Mitigación: prohibir uso para aritmética/cálculo; derivar a calculadora/herramienta externa.
2. **Clasificación de sentimiento invertida.** c5 etiqueta negativa como NEUTRA y neutra como POSITIVA (2/3 errores). Mitigación: no usar para clasificación sin dataset de validación propio; sin mitigación conocida con prompt actual.
3. **Explicación técnica incompleta/imprecisa.** c2 omite fusión y usa "subversiones"; c3 no nombra ZeroDivisionError. Mitigación: revisión humana obligatoria para documentación técnica.
4. **Falsa correlación prolijidad-exactitud.** Salidas estructuradas (tablas, código con comentarios) ocultan errores de contenido. Mitigación: validar contenido, no forma.
5. **Errores en ejemplos aunque el código sea correcto.** c1 explica paridad al revés (7 par, 10 impar). Mitigación: test unitario automático de todo snippet generado.

## Configuracion recomendada
Modelo: `hf.co/bartowski/Qwen2.5-0.5B-Instruct-GGUF:Q4_K_M` | think: `false` | num_ctx: `8192` | num_predict: `null` | temperatura: default (no medida). No se encontró configuración que corrija aritmética o clasificación; funciona solo para funciones triviales y obediencia literal (c1, c4, c6, c8) en esta configuración.

## Pendientes
- Medir con contexto >8192 para verificar límite declarado de 32768.
- Medir tasa de alucinación aritmética con batería numérica (n>50 operaciones).
- Medir clasificación con dataset etiquetado rioplatense (n>100).
- Medir robustez a instrucciones de formato adversas y a temperatura != default.
- Medir consumo RAM/VRAM con Q4_K_M y latencia p50/p95 en hardware objetivo.

