# hf.co/ModernoTech/Nova-Core:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | hf.co/ModernoTech/Nova-Core:Q4_K_M | declarado |
| Cuantizacion | Q4_K_M | declarado |
| Contexto declarado | 131072 | declarado |
| Contexto de corrida | 8192 | medido |
| think | false | medido |
| num_ctx | 8192 | medido |
| num_predict | null | medido |
| Temperatura | no informada | inferido |

## Mediciones

| Prueba | Segundos | Tokens de salida |
|---|---|---|
| p1_funcion_simple | 12.47 | 572 |
| p2_explicacion | 2.35 | 112 |
| p3_debug | 15.16 | 734 |
| p4_refactor | 22.47 | 1073 |
| p5_complejo | NO_VERIFICABLE | NO_VERIFICABLE |
| p6_trampa | NO_VERIFICABLE | NO_VERIFICABLE |
| p7_local | NO_VERIFICABLE | NO_VERIFICABLE |

No hay valor declarado de latencia/tokens para comparar. Diferencia no calculable. No se completa con estimaciones. p5-p7 sin mediciones de tiempo/tokens en el lote entregado.

## Prueba por prueba

| Prueba | Veredicto | Severidad |
|---|---|---|
| p1_funcion_simple | CORRECTO | ninguna |
| p2_explicacion | FALSO | media |
| p3_debug | CORRECTO | ninguna |
| p4_refactor | CORRECTO | ninguna |
| p5_complejo | NO_ENTREGA | critica |
| p6_trampa | FALSO | critica |
| p7_local | FALSO | alta |

p1_funcion_simple: CORRECTO. Entrega funcion operativa.

> def es_par(n): ... return n % 2 == 0

p2_explicacion: FALSO. Ignora instruccion de registro rioplatense. Entrega español neutro de manual.

> Un **context manager** en Python es un objeto que se usa para gestionar recursos, típicamente asegurando que algo se limpie o se cierre correctamente.

p3_debug: CORRECTO. Identifica KeyError y corrige con default.

> El bug es que la función intenta acceder a `i['cantidad']` cuando el diccionario solo tiene la clave `'precio'`. y cantidad = item.get('cantidad', 1)

p4_refactor: CORRECTO. Inyeccion de dependencia de tiempo correcta.

> def enviar_recordatorio(email, tiempo_actual): ... ahora = tiempo_actual ... if ahora.hour < 18:

p5_complejo: NO_ENTREGA. Bucle degenerado, repeticion masiva sin entregar implementacion. Truncado por limite.

> El conjunto de dependencias pendientes es el conjunto de todas las dependencias. (repetido cientos de veces hasta el corte)

p6_trampa: FALSO. Contenido invertido sobre Raft. Afirma sobrecarga para 3 nodos y recomienda no usarlo.

> Raft introduce una complejidad y sobrecarga para un sistema de solo 3 servidores. y Raft es ideal para sistemas con **más de 3 servidores**

p7_local: FALSO. Diagnostico invertido de ECONNREFUSED local como servidor remoto/puerto bloqueado. No indica levantar servicio local.

> El error indica que el servidor al que intentaste conectar no está disponible o el puerto está bloqueado. y el servidor está bien, pero el puerto 5432 no está respondiendo.

## Modo de falla dominante
`falso_seguro` + `no_entrega` combinados. Justificacion: 3 de 7 pruebas con contenido invertido y confianza alta (p2, p6, p7) y 1 de 7 con colapso por repeticion sin entrega (p5). Patron: formato impecable oculta error tecnico.

## Riesgos
1. **Recomendacion tecnica invertida con confianza:** p6 afirma que Raft no es para 3 nodos por sobrecarga. Contradice tolerancia N=3 -> f=1 y diseño para ser entendible. Riesgo de decision arquitectonica erronea. Sin mitigacion conocida.
2. **Diagnostico local erroneo:** p7 interpreta 127.0.0.1 como servidor remoto. Lleva a troubleshooting de red/firewall en lugar de levantar servicio local. Sin mitigacion conocida.
3. **Colapso en tarea compleja:** p5 entra en bucle de repeticion y no entrega codigo. Consume presupuesto de tokens sin resultado. Mitigacion: limitar num_predict y detectar repeticion, pero no corrige capacidad.
4. **Ignora instruccion de formato/registro:** p2 incumple voseo rioplatense explicito. Riesgo de fuera_de_alcance en prompts con restricciones de estilo. Sin mitigacion conocida.

## Configuracion recomendada
Modelo: hf.co/ModernoTech/Nova-Core:Q4_K_M, think: false, num_ctx: 8192, num_predict: null, temperatura: no informada. Con esta configuracion: 3 de 7 CORRECTO, 3 de 7 FALSO, 1 de 7 NO_ENTREGA. No funciona bien con ninguno para uso general. No adoptar.

## Pendientes
- Medir p5, p6, p7 con latencia y tokens bajo mismo contexto (8192) para completar tabla de mediciones.
- Medir con contexto declarado (131072) para verificar si el colapso de p5 es por ventana de 8192.
- Medir tasa de falso_seguro en pruebas trampa adicionales de consenso y diagnostico local.
- Medir adherencia a instrucciones de registro con suite dedicada.

