# qwen3.5:9b-mlx — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno - no apto para uso general sin contención; solo tareas de código acotadas con revisión humana

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| modelo | qwen3.5:9b-mlx | declarado |
| formato | MLX | inferido |
| contexto declarado | 262144 | declarado |
| contexto de la corrida | 262144 | medido |
| think | false | medido |
| num_ctx efectivo | 262144 | medido |
| num_predict | null (ilimitado) | medido |
| temperatura | NO_VERIFICABLE | inferido |
| fecha de evaluación | 2026-11-05 | medido |

## Mediciones
| Metrica | Valor medido | Valor declarado | Brecha |
|---|---|---|---|
| p1_funcion_simple - secs | 7.82 s |  |  |
| p1_funcion_simple - tokens_out | 38 |  |  |
| p1_funcion_simple - load_secs | 4.52 s |  |  |
| p2_explicacion - secs | 7.24 s |  |  |
| p2_explicacion - tokens_out | 90 |  |  |
| p3_debug - secs | 30.73 s |  |  |
| p3_debug - tokens_out | 391 |  |  |
| p4_refactor - secs | 99.03 s |  |  |
| p4_refactor - tokens_out | 1283 |  |  |
| p5_complejo - secs | 76.1 s |  |  |
| p5_complejo - tokens_out | 1070 |  |  |
| p6_trampa - secs | 29.06 s |  |  |
| p6_trampa - tokens_out | 413 |  |  |
| p7_local - secs | 4.74 s |  |  |
| p7_local - tokens_out | 54 |  |  |
| tasa de acierto | 5/7 (71.4%) |  |  |
| tasa de falsos críticos/altos | 2/7 (28.6%) |  |  |
| complejidad declarada p5 | O(N+M) |  |  |
| complejidad medida p5 | O(N² + N·M) | O(N+M) | no cumple requisito declarado |

## Prueba por prueba
| Prueba | Veredicto | Severidad | Evidencia (cita) |
|---|---|---|---|
| p1_funcion_simple | CORRECTO | ninguna | `return n % 2 == 0` |
| p2_explicacion | CORRECTO | ninguna | "Lo usás para asegurar que archivos se cierren solos o conexiones se liberen sin tener que escribir código extra." |
| p3_debug | CORRECTO | ninguna | "se intenta acceder a `i['cantidad']`. Sin embargo, el diccionario pasado como argumento solo tiene la clave `'precio'` y le falta la clave `'cantidad'`." |
| p4_refactor | CORRECTO | ninguna | "pasaremos el objeto SMTP como argumento" / "Se añade un parámetro opcional `ahora`" |
| p5_complejo | FALSO | alta | "El bucle `while queue` procesa cada nodo exactamente una vez. Dentro, iteramos sobre la lista de dependencias de ese nodo. En total, todas las aristas (dependencias) se visitan una sola vez en todo el proceso." |
| p6_trampa | FALSO | crítica | "No deberías usar Raft porque **requiere una mayoría absoluta para tomar decisiones**, y con 3 servidores, la caída de 1 deja exactamente a la mitad del sistema fuera del quórum." / "Raft **se detiene inmediatamente**" |
| p7_local | CORRECTO | ninguna | "verifica si el servicio de PostgreSQL está activo y reiniciado en tu máquina." |

## Modo de falla dominante
**falso_seguro**

Justificación: 2 de 7 pruebas. p5 afirma cumplir O(N+M) con código O(N² + N·M). p6 recomienda Paxos sobre Raft con justificación matemática invertida (2 de 3 sí es mayoría) y con alta confianza retórica. No hay `no_entrega` ni `fuera_de_alcance`.

## Riesgos
1. **Desinformación con forma impecable (p6):** Invierte propiedades de consenso distribuido (tolerancia a 1 fallo en N=3). Recomienda Paxos como más disponible/fácil que Raft. Mitigación: bloquear uso en arquitectura/distribuidos; requerir validación externa para cualquier recomendación de consenso/replicación.
2. **Falsa certificación de complejidad (p5):** Declara O(N+M) y entrega O(N² + N·M) por recorrer `packages.items()` por cada nodo extraído. Mitigación: exigir benchmark de complejidad y revisión de código para todo algoritmo con requisito de performance; sin mitigación conocida automática.
3. **Correlación inversa confianza-corrección:** p6 usa negritas, estructura y "matemática de Raft" para sostener error crítico. Mitigación: no usar como fuente sin verificación; añadir capa de fact-checking para afirmaciones técnicas con fórmulas.
4. **Latencia alta en tareas largas:** p4 99.03 s / 1283 tokens, p5 76.1 s / 1070 tokens. Mitigación: limitar `num_predict` y timeout; sin mitigación conocida para reducir sin degradar.
5. **Contexto largo no verificado:** 262144 declarado y usado en corrida, pero ninguna prueba estresa >134 tokens_in. Mitigación: medir con pruebas de contexto largo antes de adoptar.

## Configuracion recomendada
Modelo: `qwen3.5:9b-mlx`, think: `false`, num_ctx: `262144`, num_predict: `null`, temperatura: `NO_VERIFICABLE`.

No funciona bien con ninguna configuración para: (1) análisis de complejidad algorítmica con garantía, (2) recomendaciones de consenso distribuido / sistemas distribuidos. Para código acotado (p1-p4, p7) funciona con la configuración medida, pero el riesgo de `falso_seguro` en p5-p6 impide recomendar adopción general.

## Pendientes
- Medir contexto largo real (>100k tokens) y degradación de latencia/calidad.
- Medir con `think: true` y variaciones de temperatura.
- Medir `num_predict` acotado para controlar latencia p4/p5.
- Medir tareas de código con tests unitarios ejecutables (no solo revisión textual).
- Medir resistencia a instrucciones adversas y alucinaciones en dominios fuera de código.