<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; vertical-align: top; word-wrap: break-word; }
th { background: #f4f6f4; font-weight: 600; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; }
pre code { background: none; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 1.6em auto; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

# hf.co/bartowski/Qwen2.5-Coder-3B-Instruct-GGUF:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno

## Ficha
| Campo | Valor | Fuente |
| Modelo | hf.co/bartowski/Qwen2.5-Coder-3B-Instruct-GGUF:Q4_K_M | declarado |
| Cuantización | Q4_K_M | declarado |
| Contexto declarado | 32768 | declarado |
| Contexto de corrida | 8192 | medido |
| Think | false | medido |
| Temperatura | no especificada | NO_VERIFICABLE |

## Mediciones

| Prueba | Segundos | Tokens de salida |
| p1_funcion_simple | 16.77 | 142 |
| p2_explicacion | 5.5 | 89 |
| p3_debug | 40.3 | 311 |
| p4_refactor | 73.55 | 634 |
| p5_complejo | 29.32 | 676 |
| p6_trampa | 15.37 | 510 |
| p7_local | 0.6 | 13 |

Contexto declarado por el modelo: 32768. Contexto de corrida: 8192. Diferencia: -24576 tokens. La corrida no verifica comportamiento en ventana completa; cualquier inferencia sobre contexto largo es NO_VERIFICABLE.

Tiempo total de generación: 180.91 s. Tiempo medio: 25.84 s. Máximo en p4_refactor (73.55 s) con 634 tokens. Mínimo en p7_local (0.6 s) con rechazo sin contenido.

## Prueba por prueba

| Prueba | Veredicto | Severidad |
| p1_funcion_simple | CORRECTO | ninguna |
| p2_explicacion | FALSO | media |
| p3_debug | CORRECTO | ninguna |
| p4_refactor | INCOMPLETO | alta |
| p5_complejo | FALSO | critica |
| p6_trampa | FALSO | critica |
| p7_local | NO_ENTREGA | critica |

Evidencia p1: `return n % 2 == 0` — función correcta.

Evidencia p2: `Un context manager en Python es un objeto que proporciona un bloque de código con un contexto específico.` — sustancia correcta pero sin registro rioplatense y excede 4 líneas pedidas.

Evidencia p3: `if 'cantidad' in i: total += i['precio'] * i['cantidad']` — manejo de KeyError correcto.

Evidencia p4: `def enviar_recordatorio(email, get_time, send_email): ahora = get_time() if ahora.hour < 18: return None` — inyección correcta pero test invertido: afirma que 17:30 devuelve 'enviado' cuando la función devuelve None.

Evidencia p5: `for dependency in graph.get(package, []): graph[dependency].remove(package)` — topological sort invertido; output prometido contradice código.

Evidencia p6: `Raft no es adecuado para servidores con un número muy pequeño de servidores. Raft requiere un número mínimo de servidores para funcionar correctamente, generalmente 3 o más. Si solo tienes 3 servidores, el protocolo de replicación de datos de Raft no es necesario` — contradice especificación de Raft para 3 nodos.

Evidencia p7: `Lo siento, pero no puedo ayudarte con eso.` — rechazo total sin entrega.

## Modo de falla dominante
`falso_seguro` en combinación con `no_entrega` y `fuera_de_alcance`.

Justificación: 3 de 7 pruebas con lógica invertida presentada con confianza (p4, p5, p6). 1 de 7 con no_entrega (p7). 1 de 7 con fuera_de_alcance por ignorar formato/registro (p2). El patrón es código sintácticamente plausible con semántica invertida.

## Riesgos
1. **Código que compila pero falla en runtime.** p5 genera orden topológico invertido y p4 tests que fallarían. Mitigación: exigir suite de tests ejecutada, no solo revisión visual.
2. **Recomendación de arquitectura incorrecta con seguridad.** p6 desaconseja Raft para el caso exacto donde aplica (3 nodos, tolerancia a 1 caída). Sin mitigación conocida sin validación humana experta.
3. **Incumplimiento de instrucciones de formato/registro.** p2 ignora registro rioplatense y límite de líneas. Mitigación: validador automático de formato en pipeline.
4. **Rechazo injustificado.** p7 no entrega diagnóstico técnico pedido. Sin mitigación conocida; indica filtro o incapacidad no documentada.

## Configuracion recomendada
Modelo: hf.co/bartowski/Qwen2.5-Coder-3B-Instruct-GGUF:Q4_K_M, think: false, num_ctx: 8192, num_predict: null, temperatura: no especificada. No funciona de forma fiable con ninguna configuración medida para tareas de razonamiento algorítmico o consenso distribuido. Solo tareas triviales (p1, p3) pasaron.

## Pendientes
- Medir con contexto 32768 declarado para verificar degradación en ventana larga.
- Medir con temperatura=0 y con think=true para descartar variabilidad.
- Medir tasa de rechazo en p7 con reintentos y prompts alternativos.
- Medir ejecución real de código generado (p4, p5) en sandbox, no solo revisión estática.

