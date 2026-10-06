# Session Planning Hooks (Kanam OS) 🌿

> **Estado: ADOPTADO (2026-10-06).** El script es portable (`SESSION_PLAN_PATH` sobrescribible) y vive en `.knowledge/session_plan.json`. **Cableado:** `session-start.sh` lo lee al arrancar (presenta el plan activo); `session-end.sh` lo cierra y archiva via `session_plan.py close`. Ver ADR-093. Implementación: `scripts/session_plan.py`.

Este sistema implementa la "Memoria de Intención". El objetivo es que la planificación de la sesión no sea efímera (que no viva solo en el historial del chat), sino que sea un objeto persistente del sistema que sobreviva a reinicios del Gateway o cambios de contexto.

## 📋 El Objeto `.session_plan`

La planificación reside en un archivo JSON estructurado en la raíz del workspace o en el directorio de estado.

### Estructura del Plan
```json
{
  "session_id": "uuid-de-la-sesion",
  "objective": "Meta global de la jornada",
  "status": "active | paused | completed",
  "steps": [
    {
      "id": 1,
      "task": "Descripción de la tarea",
      "status": "pending | in_progress | completed | blocked",
      "blocker": "Descripción del bloqueo (si aplica)",
      "timestamp": "ISO-date"
    }
  ],
  "metadata": {
    "started_at": "...",
    "last_update": "..."
  }
}
```

## 🔄 Flujo de Operación

### 1. Inicialización (Startup Hook)
Al iniciar una sesión o detectar un reinicio:
- El sistema busca un `.session_plan` con estado `active`.
- Si existe, el Core lee el plan y presenta un resumen: *"Retomando sesión: estábamos en el paso X del plan Y"*.

### 2. Actualización (Turn Hook)
Durante el desarrollo:
- Cada vez que se completa una tarea o se encuentra un bloqueo, se actualiza el estado del step correspondiente.
- El plan actúa como la "única fuente de verdad" sobre el progreso, eliminando la necesidad de preguntar *"¿en qué estábamos?"*.

### 3. Cierre (Shutdown Hook)
Al ejecutar `session-end`:
- El plan se marca como `completed` o se archiva.
- El resumen del plan alimenta el registro del Daily.

---

*Actualizado el 2026-10-01. Cierre del Sprint 2.3 - Hooks de Turno.*
