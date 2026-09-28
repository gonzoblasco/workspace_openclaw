# ADR-074: Protocolo de Despacho y Coordinación Multi-Agente

**Date:** 2026-09-26
**Status:** Accepted
**Context:** Definir cómo el `kanam-core` coordina las tareas entre los agentes especializados para minimizar la latencia y el overhead de orquestación.

## Contexto
Con la implementación de la arquitectura modular, el `kanam-core` actúa como el cerebro estratégico. Para evitar que el core se sature procesando detalles de implementación, este ADR define el flujo de despacho de tareas.

## Decisiones
### 1. El Modelo de Despacho (Router Pattern)
El `kanam-core` no ejecuta tareas de ejecución; **despacha** tareas de ejecución. El flujo es:
1. **Interpretación:** El Core identifica la intención del usuario.
2. **Selección de Especialista:** El Core identifica qué agente posee la Skill necesaria.
3. **Delegación:** El Core invoca el agente especializado con un prompt de "Contexto de Tarea".
4. **Retorno:** El especialista ejecuta y devuelve el resultado al Core para síntesis final.

### 2. Protocolo de Despacho por Especialidad
| Especialidad | Agente Responsable | Criterio de Despacho |
|---|---|---|
| **Desarrollo / Ingeniería** | `kanam-dev` | Código, validación de specs, refactorización, implementación de skills. |
| **Infraestructura / Ops** | `kanam-ops` | Deploy, CI/CD, manejo de servidores, configuración de entorno. |
| **Memoria / Análisis** | `kanam-mind` | Análisis de corpus, minería de datos, resúmenes de contexto. |
| **Creatividad / Diseño** | `kanam-studio` | Diseño de UI, generación de activos, narrativa, prototipado. |

### 3. El "Context Handover" (Traspaso de Contexto)
Para evitar que un agente "re-descubra" lo que otro ya hizo, cada finalización de tarea debe incluir un bloque de **Estado de Contexto**:
- **Summary:** Qué se logró.
- **Status:** Estado actual del activo (ej. "Draft", "Ready", "Merged").
- **Next Steps:** Qué falta para completar la tarea.
- **Resources:** Caminos a archivos creados o modificados.

### 4. Gestión de Conflictos
Si una tarea requiere múltiples especialistas:
1. El Core identifica la **Tarea Primaria**.
2. El Core selecciona al especialista principal.
3. El Core solicita al especialista principal que identifique si requiere apoyo de otro especialista (ej. `kanam-dev` pide ayuda a `kanam-ops` para un deploy).
4. El Core coordina la intervención del segundo agente.

## Acciones de Implementación
- [ ] Actualizar el `SKILLS-INDEX.md` para reflejar que el Core es el único punto de entrada.
- [ ] Crear plantillas de "Context Handover" en el workspace de cada agente.
- [ ] Implementar validación de despacho: si el Core intenta ejecutar una tarea de `kanam-dev` directamente, el sistema debe alertar que la tarea debe ser delegada.

## Notas
Este protocolo asegura que el `kanam-core` mantenga una visión de alto nivel y que los agentes especialistas conserven su autonomía operativa dentro de sus dominios.
