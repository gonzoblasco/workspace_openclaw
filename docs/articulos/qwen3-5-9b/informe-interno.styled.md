<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; vertical-align: top; word-wrap: break-word; overflow-wrap: break-word; }
th { background: #f4f6f4; font-weight: 600; }
td:nth-child(1) { width: 40%; }
td:nth-child(2) { width: 38%; }
td:nth-child(3) { width: 22%; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; word-break: break-word; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; line-height: 1.45; }
pre code { background: none; padding: 0; }
img { max-width: 100%; height: auto; display: block; margin: 1.6em auto; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

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

| Prueba | Segundos | Tokens de salida |
|---|---|---|
## Prueba por prueba
| Prueba | Veredicto | Severidad |
|---|---|---|
| p1_funcion_simple | CORRECTO | ninguna |
| p2_explicacion | CORRECTO | ninguna |
| p3_debug | CORRECTO | ninguna |
| p4_refactor | CORRECTO | ninguna |
| p5_complejo | FALSO | alta |
| p6_trampa | FALSO | crítica |
| p7_local | CORRECTO | ninguna |

### Evidencia citada, prueba por prueba

**p1_funcion_simple.** `return n % 2 == 0`

**p2_explicacion.** "Lo usás para asegurar que archivos se cierren solos o conexiones se liberen sin tener que escribir código extra."

**p3_debug.** "se intenta acceder a `i['cantidad']`. Sin embargo, el diccionario pasado como argumento solo tiene la clave `'precio'` y le falta la clave `'cantidad'`."

**p4_refactor.** "pasaremos el objeto SMTP como argumento" / "Se añade un parámetro opcional `ahora`"

**p5_complejo.** "El bucle `while queue` procesa cada nodo exactamente una vez. Dentro, iteramos sobre la lista de dependencias de ese nodo. En total, todas las aristas (dependencias) se visitan una sola vez en todo el proceso."

**p6_trampa.** "No deberías usar Raft porque **requiere una mayoría absoluta para tomar decisiones**, y con 3 servidores, la caída de 1 deja exactamente a la mitad del sistema fuera del quórum." / "Raft **se detiene inmediatamente**"

**p7_local.** "verifica si el servicio de PostgreSQL está activo y reiniciado en tu máquina."

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
