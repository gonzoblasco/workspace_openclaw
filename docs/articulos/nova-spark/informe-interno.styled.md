<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; vertical-align: top; word-wrap: break-word; }
th { background: #f4f6f4; font-weight: 600; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; word-break: break-word; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; line-height: 1.45; }
pre code { background: none; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 1.6em auto; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

# hf.co/ModernoTech/Nova-Spark:Q4_0 — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno

## Ficha
| Campo | Valor | Fuente |
| Modelo | hf.co/ModernoTech/Nova-Spark:Q4_0 | declarado |
| Cuantizacion | Q4_0 | declarado |
| Contexto declarado | 262144 | declarado |
| Contexto de corrida | 8192 | medido |
| Think | false | medido |
| Temperatura | no especificada | NO_VERIFICABLE |
| Fecha de evaluacion | 2026-11-05 | medido |

## Mediciones

| Prueba | Segundos | Tokens de salida |
| c1_funcion_simple | 3.09 | 170 |
| c2_texto_corto | 0.9 | 81 |
| c3_debug_facil | 2.35 | 196 |
| c4_completar | 0.37 | 31 |
| c5_clasificar | 0.35 | 26 |
| c6_instruccion_exacta | 0.06 | 2 |
| c7_aritmetica | 0.1 | 5 |
| c8_resumen | 0.46 | 38 |

No hay valor declarado de latencia o throughput para comparar. Tiempos medidos con ctx=8192, think=false. Carga inicial: 1.06 s en c1. Ninguna prueba supera 3.09 s. Tokens de salida entre 2 y 196.

## Prueba por prueba

| Prueba | Veredicto | Severidad |
| c1_funcion_simple | CORRECTO | ninguna |
| c2_texto_corto | FALSO | alta |
| c3_debug_facil | FALSO | crítica |
| c4_completar | CORRECTO | ninguna |
| c5_clasificar | FALSO | alta |
| c6_instruccion_exacta | CORRECTO | ninguna |
| c7_aritmetica | FALSO | crítica |
| c8_resumen | INCOMPLETO | media |

Evidencia por prueba:

c1_funcion_simple: `def es_par(n): return n % 2 == 0` — Implementacion correcta.

c2_texto_corto: `"`git pull` es la herramienta que permite sincronizar el estado actual de la carpeta de trabajo con la versión más reciente de la versión de código fuente (base) en línea."` — No usa registro rioplatense pedido y definicion vaga; no describe fetch+merge al branch local.

c3_debug_facil: `"la división entre dos números enteros puede causar división por cero si el vector es vacío. Además, la función no tiene un parámetro para el número de elementos, y la función `print` no está definida en la misma función."` — Atribuye causas inexistentes. El fix propuesto no maneja lista vacia.

c4_completar: `"if len(nums) == 0: return None return max(nums)"` — Guarda correcta para vacio.

c5_clasificar: `"| 1 | NEUTRA |"` — Falla clasificacion 1 de 3. Frase 1 "Me encanto el trato, volveria." es POSITIVA.

c6_instruccion_exacta: `"OK"` — Obedece instruccion literal de una palabra.

c7_aritmetica: `"1001"` — 47*23 = 1081. Error de 80.

c8_resumen: `"El sistema se cayeron tres veces y el equipo de guardia detectó que un disco estaba lleno, lo que permitió a la normalidad volver a las 6 de la mañana."` — Omite accion de liberacion del disco; concordancia rota ("El sistema se cayeron").

## Modo de falla dominante
`falso_seguro`: responde con confianza y contenido invertido.

Justificacion: 4 de 8 pruebas con veredicto FALSO por contenido inventado o invertido (c2, c3, c5, c7). En c3 diagnostica bugs que no existen. En c7 entrega 1001 como resultado aritmetico correcto. En c2 y c5 entrega definiciones y clasificaciones erroneas sin senal de incertidumbre.

## Riesgos
1. **Alucinacion en debug:** diagnostica causas falsas y propone fix que no corrige division por cero. Sin mitigacion conocida. No usar para asistencia de codigo sin revision humana.
2. **Error aritmetico silencioso:** falla en multiplicacion de dos cifras (47*23). Sin mitigacion conocida. Requiere calculadora externa si se adoptara.
3. **Clasificacion no fiable:** error en sentimiento basico (1 de 3). Sin mitigacion conocida.
4. **Incumplimiento de registro:** ignora instruccion de voseo rioplatense. Mitigacion: prompt mas explicito no evaluado.
5. **Resumen incompleto:** omite accion clave (liberacion de disco). Mitigacion: exigir checklist de entidades en prompt.

## Configuracion recomendada
Modelo: hf.co/ModernoTech/Nova-Spark:Q4_0, think=false, num_ctx=8192, num_predict=null (default), temperatura no evaluada. Con esta configuracion el modelo falla en 4 de 8 pruebas con 2 criticas. No hay configuracion donde funcione de forma general. Como especialista solo para generacion de funciones triviales (c1, c4) y copia literal (c6).

## Pendientes
- Medir con contexto >8192 (declarado 262144 no verificado).
- Medir con think=true y temperaturas distintas.
- Medir latencia p50/p95 con carga concurrente.
- Medir clasificacion y resumen con set mas amplio.
- Medir aritmetica con calculadora/tool-use habilitado.

