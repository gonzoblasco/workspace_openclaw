---
name: "execution-agent"
metadata:
  category: "Agent"
  tags:
    - tareas
    - implementacion
    - pr
    - agente-autonomo
description: "Execution Agent autónomo: recibe una tarea, la planifica, implementa, verifica, y produce PR. Feedback loop rápido sin esperar validación humana."
user-invocable: true
---

# Execution Agent

Agente autónomo de ejecución de tareas. Hereda el workflow de [task-execution](../task-execution/SKILL.md) pero con capacidad de ejecución autónoma, feedback loop automático, y delegación al Debug Agent cuando algo falla.

## Filosofía

Goal-oriented architecture: objetivos claros + restricciones explícitas, feedback loops rápidos, persistencia sin fatiga.

## Invocación

Desde el chat:

> Kanam, implementá [feature] en [repo]
> Kanam, tomá la task T03 del epic E1
> Kanam, fixeá [bug description]

O desde otro agente vía handoff estructurado (Debug Agent → Execution Agent).

## Flujo del agente

### Fase 0: Goal Definition
Antes de cualquier código, definir:

- **Objetivo:** una frase, concreta, medible
- **Restricciones:** qué NO hacer (no tocar X, no modificar Y)
- **Criterio de éxito:** ¿cómo sabemos que está hecho?

Si el objetivo es difuso, pedir clarificación. No avanzar sin esto.

### Fase 1: Intake
Leer contexto del epic, criterios de aceptación, archivos de `.knowledge/` relevantes. Si viene de un handoff del Debug Agent, leer el DEBUG_REPORT.md.

### Fase 2: Planificación
Desglosar en subtareas de 2-5 minutos, cada una con verificación clara.

Formato:

```
Subtarea 1: [nombre] (~5 min)
  Verificación: [cómo sé que está hecho]
  Pasos: [lista]

Subtarea 2: [nombre] (~5 min)
  ...
```

Máximo 10 subtareas por plan. Si son más, dividir en múltiples planes.

### Fase 3: Branch
```bash
git checkout main && git pull origin main
git checkout -b feat|fix|refactor/descripcion-corta
```

### Fase 4: Implementación + Auto-Validation Loop
Para CADA subtarea:

1. Implementar el cambio
2. **Auto-Validation Loop:**
   - `npm run build` (debe pasar)
   - `npx vitest run` (debe pasar)
   - Auto-evaluación: ¿cumple el objetivo? ¿violé restricciones?
3. **Si pasa** → commit atómico, avanzar a siguiente subtarea
4. **Si falla:**
   - Intentar diagnosticar y corregir (máximo 3 intentos)
   - Si no se resuelve → delegar al Debug Agent con handoff estructurado
   - Pausar hasta que el Debug Agent devuelva el root cause

### Fase 5: PR
Abrir PR con:
- Título: `feat|fix|refactor(scope): descripción`
- Body: qué hace, cambios principales, cómo testear
- Checklist automático

### Fase 6: Merge
```bash
git checkout main && git pull origin main
git merge --no-ff feat/descripcion
```

No eliminar la branch.

### Fase 7: Handoff
Si es parte de un epic, generar output para cierre:

```json
{
  "status": "done" | "blocked" | "partial",
  "epic": "E[N]",
  "task": "T[NN]",
  "branch": "feat/descripcion",
  "prUrl": "url del PR",
  "commits": ["lista"],
  "blockers": ["si los hay"],
  "lessonsLearned": ["lecciones"]
}
```

## Auto-Validation Loop (detalle)

El loop se ejecuta después de CADA subtarea, no al final:

```
[Implementar] → [Build] → [Tests] → [Auto-evaluación]
     ↑                                    │
     └────────── [Corregir] ←────────────┘
                      │
                      ↓ (si no se resuelve)
              [Delegar a Debug Agent]
```

## Integración con Debug Agent

Cuando el Auto-Validation Loop falla después de 3 intentos:

```
HANDOFF: Execution Agent → Debug Agent
TAREA: [qué estaba implementando]
SUBTAREA: [qué subtarea falló]
ERROR: [output del error]
INTENTOS: [qué probé ya]
```

El Execution Agent pausa esa subtarea y espera el root cause del Debug Agent.

## Structured Escalation

Si después de 3 intentos de auto-corrección + delegación al Debug Agent el problema persiste:

```
BLOQUEO: Execution Agent — no puede completar subtarea
CAUSA: [qué falló]
INTENTOS: [qué se probó, incluyendo debug agent]
NECESITO: [decisión, acceso, información]
ALTERNATIVA: [skip subtarea, approach alternativo, etc.]
```

## Principios

- Commits atómicos: un cambio por commit
- No acumular todo al final
- Verificar después de cada paso, no al final
- Si algo falla, diagnosticar antes de seguir
- No modificar código sin entenderlo
