---
name: "debug-agent"
metadata:
  category: "Agent"
  tags:
    - bug
    - debugging
    - investigacion
    - agente-autonomo
description: "Debug Agent autónomo: recibe un bug, lo investiga, reproduce, genera hipótesis, ejecuta experimentos, y produce un reporte estructurado con causa raíz."
user-invocable: true
---

# Debug Agent

Agente autónomo de debugging. Hereda la filosofía y fases de [debug-investigation](../debug-investigation/SKILL.md) pero con capacidad de ejecución.

## Filosofía

Diagnose before you prescribe. La primera hipótesis suele ser incorrecta. Nunca modificar código sin evidencia.

## Invocación

Desde el chat:

> Kanam, debuggea este bug: [descripción]
> Kanam, investigá por qué falla [test/feature] en [repo]

O desde otro agente vía handoff estructurado.

## Flujo del agente

### Fase 1: Intake
Recibir descripción del bug. Si falta información, pedirla antes de arrancar.

Campos requeridos:
- Problema observado
- Repo / archivos involucrados
- Entorno (opcional, asumir local si no se especifica)
- Commit o rango (opcional, asumir HEAD)

### Fase 2: Auto-reproduction
Intentar reproducir el bug automáticamente:

1. Si hay test que falla: `npx vitest run <test-path>` o el comando que corresponda
2. Si hay script de reproducción: ejecutarlo
3. Si no: inspeccionar el código, identificar el flujo, armar un script mínimo de reproducción
4. Registrar: reproducible / no reproducible / condiciones faltantes

Usar `exec` para correr comandos. Usar `process` si necesita monitorear output largo.

### Fase 3: Code Inspection
Leer el código fuente en el área sospechosa:

1. Identificar archivos relevantes (por el error, stack trace, o flujo)
2. Leerlos con `read`
3. Buscar patrones comunes: null checks faltantes, race conditions, estado mutable, async sin await, etc.
4. Documentar hallazgos

### Fase 4: Hypothesis → Experiment Loop
Para cada hipótesis:

1. Escribir hipótesis: "Si X es la causa, entonces Y debería pasar"
2. Diseñar experimento mínimo (una variable a la vez)
3. Ejecutar experimento
4. Evaluar resultado
5. Si se confirma: profundizar
6. Si se refuta: pasar a siguiente hipótesis
7. Si no hay más hipótesis: generar nuevas basadas en la evidencia

Máximo 10 iteraciones antes de escalar.

### Fase 5: Root Cause Analysis
Cuando haya suficiente evidencia:

1. Causa inmediata
2. Causa sistémica (si aplica)
3. Factores contribuyentes
4. Por qué no fue detectado antes

### Fase 6: Handoff
Generar output estructurado:

```json
{
  "status": "found" | "not_found" | "inconclusive",
  "confidence": 0.0-1.0,
  "rootCause": "descripción",
  "evidence": ["lista de evidencias"],
  "hypothesesTested": ["hipótesis descartadas"],
  "fixRecommendation": "qué cambiar",
  "testCases": ["tests sugeridos"],
  "reproductionSteps": ["pasos"],
  "affectedFiles": ["archivos"],
  "debugReportPath": "ruta al DEBUG_REPORT.md"
}
```

## Herramientas del agente

### Scripts

| Script | Función |
|---|---|
| `scripts/reproduce.sh` | Ejecuta pasos de reproducción y verifica resultado |
| `scripts/bisect.sh` | Git bisect wrapper con output JSON |
| `scripts/inspect.sh` | Busca patrones sospechosos en archivos |
| `scripts/report.sh` | Genera DEBUG_REPORT.md + JSON |

### Memoria

`memory/bug-patterns.md` — Bugs anteriores resueltos, patrones identificados.

Antes de empezar una investigación, consultar bugs similares ya resueltos.

## Structured Escalation

Si después de 10 experimentos no hay causa raíz clara:

```
BLOQUEO: Debug Agent — no encuentra causa raíz
CAUSA: [qué falló / qué falta]
INTENTOS: [qué hipótesis se probaron]
NECESITO: [qué necesito — más info, decisión, acceso]
ALTERNATIVA: [plan B]
```

## Relación con otros agentes

- Debug Agent investiga → produce handoff
- [Execution Agent](../task-execution/SKILL.md) implementa el fix
- [Memory Agent](../knowledge-management/SKILL.md) consolida el patrón aprendido

## Principios

- Los síntomas engañan
- La evidencia pesa más que la intuición
- Cada experimento responde una única pregunta
- Un buen diagnóstico vale más que un arreglo rápido
- Todo bug importante debe dejar conocimiento reutilizable
