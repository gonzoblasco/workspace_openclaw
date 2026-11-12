# Adopción — Design Software Systems Like a Senior Engineer

**Fecha:** 2026-11-11
**Regla aplicada:** un curso cierra cuando cambia algo del workspace, no cuando queda transcripto.

## Veredicto de utilidad

**Se adopta, un solo artefacto.** El curso no enseña tecnologías nuevas — PostgreSQL, Redis, Kafka,
Elasticsearch y WebSockets ya los conocemos. Lo que aporta es un **procedimiento explícito con presupuesto de
tiempo** y la exigencia de justificar cada elección contra sus alternativas descartadas.

El curso **no aplica** a los tres proyectos de juego (`reinos-de-la-frontera`, `godot-3d-rpg-curso`,
`platformer-tiempo`): son single-player, sin servidor y sin carga concurrente. Forzar sus cuentas de capacidad
ahí sería resumir el curso disfrazado de gate.

### Qué ya está cubierto (y no se toca)

- **Rate limiting por token bucket** — `projects/preflight/src/lib/ratelimit.ts` ya lo implementa con tres capas
  (burst en memoria, cap diario en SQLite, cuota por licencia), leídas de env. El módulo 19 del curso explica el
  mismo mecanismo; no hay nada que agregar.
- **Límite de concurrencia con cola visible** — `src/lib/scan.ts:36-55` implementa un semáforo que encola en vez
  de degradar a todos. Verifiqué su correctitud con un harness de 6 jobs concurrentes contra `MAX=2`: nunca
  corrió más de 2 a la vez. El curso enseña el patrón; el código ya lo tiene bien.
- **Health endpoint que separa liveness de detalle** — `/health` sin auth y `/status` con token, con el
  razonamiento de que el detalle operativo «no puede usarse como reconocimiento gratis» (`src/lib/mcp-cli.ts:111-136`).
  Es exactamente la distinción que pide el módulo 20.
- **Idempotencia** — no aplica: Preflight no tiene una operación de escritura de negocio que pueda duplicarse
  (un scan es idempotente por naturaleza).

### La única fila que muerde

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| El paso 4 exige monitoreo con latencia, errores y **umbrales de alerta**, y el curso lo marca como «a strong signal that you think like a senior engineer» (0:18:11). En el sistema 3, la cola de mensajes esperando procesamiento es la señal que se publica; sin ella no se distingue «ocupado» de «saturado». | `src/lib/scan.ts` encola (`waiters.push`) cuando se alcanza `PREFLIGHT_MAX_CONCURRENT`, y **la longitud de esa cola nunca se lee** (`grep -rn waiters src/` → sólo push y shift). El `/status` publica `activeScans` y `maxConcurrent`, pero cuando los 4 slots están ocupados los dos números se quedan quietos mientras la cola crece sin límite visible. Una saturación real es indistinguible de una operación normal. El type literal `'queued'` de `ScanJob` (`src/lib/types.ts:130-137`) **nunca se asigna** y la interfaz no se usa en ningún archivo: parece una señal, no lo es. | `check-observability-gaps.py` corrido contra `projects/preflight` → **exit 1**, cola PARCIAL. Ver salida abajo. |

## El artefacto, corrido contra el repo

El gate se construyó **fallando dos veces primero**, y las dos fallas quedan registradas porque son la lección:

**v1 — verde falso por prosa.** Buscaba `waiting` en todo el texto y lo encontró dentro de un comentario de
`scan.ts:384` que explicaba el flapping de un banner de cookies. Un gate que se satisface con un comentario no
mide nada. Corrección: se descartan comentarios antes de buscar.

**v2 — verde falso por nombre de señal.** Buscaba `queued` y lo encontró en `status: 'queued' | 'running' | ...`,
un type literal que nunca se asigna y cuya interfaz `ScanJob` no importa ningún archivo. Corrección: la señal
tiene que llegar a una respuesta HTTP (`json(`, `res.write`, `NextResponse.json`), que es donde un operador
realmente la puede leer, y se descartan las líneas que son declaración de tipo pura.

**Salida final:**

```
repo: /Users/gonzoblasco/.openclaw/workspace/projects/preflight
archivos de código: 33 (comentarios descartados, type literals descartados)

  OK      saturación  src/lib/scan.ts:59                 (scans activos contra el máximo)
  PARCIAL cola        aparece en src/lib/types.ts pero no llega a una respuesta
  OK      latencia    scripts/experiment.mjs:148         (cuánto tarda un request)
  OK      umbral      src/lib/mcp-cli.ts:136             (el número contra el que se alerta)

RESULTADO: 1 de 4 señales no son observables.
El paso 4 queda incompleto: sin cola publicada y sin umbral, la
saturación se descubre cuando el cliente ya la reporta.
EXIT=1
```

**Lo que el gate NO dice, y conviene no confundir:** las señales de latencia y umbral dan OK por archivos
distintos (`scripts/experiment.mjs` y el `/status`), no por un sistema de métricas del servicio. El gate mide
presencia de la señal, no un pipeline de alertas. Un `latencyMs` en un script de experimento no alerta a nadie,
y ése es el próximo hueco — anotado abajo como candidato, no escrito.

## Por qué no se aplicó el artefacto al código

El curso pediría publicar la cola en `/status` y fijar el umbral. Eso es **implementación**, y el arreglo vive en
`projects/preflight`, que es de DEV. El CORE entrega el gate y el diagnóstico con evidencia; el fix se delega.
Además una fila de diagnóstico no se resuelve escribiendo el fix en el mismo turno: el valor de este `ADOPCION.md`
es que **la próxima vez que alguien abra Preflight sepa qué falta y por qué**, con el comando listo para correr.

## Candidatos listados, sin escribir

1. **Pipeline de métricas real** — latencia p95 medida por el servicio y errores por código de estado, expuesto
   en `/status` con un `alertAt` por señal. Hoy `latencyMs` sólo existe en un script de experimento.
2. **La pirámide aplicada al workspace** — el curso argumenta (0:48:43) que el mid-level empieza a codear sin
   plan ni tech selection. No es accionable como gate sin inventar una métrica; se deja como criterio de lectura
   para las sesiones de planificación.
3. **Carpeta de práctica de entrevistas** — el curso no da problemas para resolver solo. Un banco de 3
   enunciados con solución de referencia sería el complemento honesto, pero es material de estudio,
   no un gate del workspace.

## Lo que el curso no cubre (y la clase no debe pretender que sí)

- **Práctica deliberada.** Cero problemas asignados. Se resuelve mirando, no produciendo.
- **Back of the envelope con calculadora prohibida.** El curso hace las cuentas en voz alta pero no ejercita el
  cálculo bajo presión.
- **Cómo se comunica el trade-off cuando no hay una respuesta correcta.** Lo menciona como dimensión de
  evaluación; no lo muestra en un caso donde el candidato se equivoque y se recupere.
- **Concurrencia práctica.** El doble booking se explica entero y bien (módulo 13), pero no se implementa. Por eso
  el ejercicio del módulo 13 es el más valioso del curso y el único que obliga a correr algo.

## Uso

```bash
python3 studies/system-design-interview-guide/check-observability-gaps.py projects/preflight
```

Aplicable a cualquier servicio del workspace que exponga estado operativo. Los tres proyectos de juego no
tienen HTTP y el gate los reportaría como *falta todo*, que es cierto y ruidoso: no se corre ahí.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
