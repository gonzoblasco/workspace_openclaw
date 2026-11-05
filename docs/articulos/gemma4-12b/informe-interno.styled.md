<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; }
th { background: #f4f6f4; font-weight: 600; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; line-height: 1.45; }
pre code { background: none; padding: 0; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

# gemma4:12b-mlx — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** ADOPTAR COMO ESPECIALISTA
**Uso recomendado:** codigo Python (escritura, debug, refactor, algoritmos) — no para diagnostico de infraestructura local

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | gemma4:12b-mlx | declarado |
| Contexto declarado | 262144 | declarado |
| Contexto de corrida | 262144 | medido |
| think | false | medido |
| num_ctx | 262144 | medido |
| num_predict | null | medido |
| Temperatura | NO_VERIFICABLE | NO_VERIFICABLE |
| Fecha evaluacion | 2026-11-05 | inferido |

## Mediciones
| Metrica | Valor medido | Valor declarado | Brecha |
|---|---|---|---|
| Contexto (tokens) | 262144 | 262144 | 0 |
| p1_funcion_simple - duracion | 13.05 s |  |  |
| p1_funcion_simple - tokens_out | 233 |  |  |
| p2_explicacion - duracion | 5.51 s |  |  |
| p2_explicacion - tokens_out | 94 |  |  |
| p3_debug - duracion | 12.92 s |  |  |
| p3_debug - tokens_out | 320 |  |  |
| p4_refactor - duracion | 31.57 s |  |  |
| p4_refactor - tokens_out | 707 |  |  |
| p5_complejo - duracion | 43.27 s |  |  |
| p5_complejo - tokens_out | 926 |  |  |
| p6_trampa - duracion | 23.06 s |  |  |
| p6_trampa - tokens_out | 383 |  |  |
| p7_local - duracion | 7.37 s |  |  |
| p7_local - tokens_out | 153 |  |  |

## Prueba por prueba
| Prueba | Veredicto | Severidad | Evidencia (cita) |
|---|---|---|---|
| p1_funcion_simple | CORRECTO | ninguna | "return n % 2 == 0" |
| p2_explicacion | CORRECTO | ninguna | "Lo usás para manejar archivos, conexiones a bases de datos o bloqueos de hilos sin dejar basura tirada." |
| p3_debug | CORRECTO | ninguna | "Para solucionarlo, debes usar el método `.get()`, que permite asignar un valor por defecto (en este caso `0`) si la llave no existe." |
| p4_refactor | CORRECTO | ninguna | "def enviar_recordatorio(email, ahora=None, smtp_client=None):" |
| p5_complejo | CORRECTO | ninguna | "utilizaremos el **Algoritmo de Kahn** para el ordenamiento topológico." |
| p6_trampa | CORRECTO | ninguna | "Raft es perfectamente capaz de funcionar con 3 servidores y tolerar la caída de 1." |
| p7_local | FALSO | alta | "Por favor, verificá si el servicio de la base de datos está encendido y funcionando correctamente." |

## Modo de falla dominante
`no_aplica`

Justificacion: 6 de 7 pruebas CORRECTO. Unica falla en 1 de 7 pruebas (p7_local). No hay patron dominante. La falla en p7_local es respuesta generica sin traducir `127.0.0.1` como loopback ni `ECONNREFUSED` como "nadie escucha en el puerto", con sugerencia vaga "verificá si está encendido" y mencion "si el puerto está disponible". No encaja en `no_entrega`, `falso_seguro` ni `fuera_de_alcance` de forma pura.

## Riesgos
1. **Diagnostico de errores de conexion local incompleto:** En p7_local no identifica loopback ni significado de ECONNREFUSED. Mitigacion: no usar para soporte/on-call ni para triage de logs de infraestructura; derivar a runbook explicito.
2. **Falsa confianza en dominio infraestructura:** El modelo resuelve bien codigo (6/7) pero falla en log concreto. Mitigacion: acotar uso a tareas de codigo verificadas; bloquear prompts de diagnostico de red/DB sin contexto adicional.
3. **Evaluacion limitada a un set de 7 pruebas:** No se midio latencia p95, costo, ni robustez a prompts adversarios. Mitigacion: ver Pendientes.

## Configuracion recomendada
| Parametro | Valor |
|---|---|
| modelo | gemma4:12b-mlx |
| think | false |
| num_ctx | 262144 |
| num_predict | null (default corrida) |
| temperatura | NO_VERIFICABLE — no medida en esta corrida |

El modelo funciona con la configuracion de la corrida para tareas de codigo. Para diagnostico local, sin mitigacion conocida.

## Pendientes
- Medir p7_local con prompt dirigido que exija explicar 127.0.0.1 y ECONNREFUSED explicitamente
- Medir latencia y costo a carga (p95, tokens/s)
- Medir comportamiento con think=true y con num_predict acotado
- Medir alucinacion en librerias y APIs no estandar