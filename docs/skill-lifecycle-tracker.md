# Skill Lifecycle Tracker (Kanam OS) 🌿

Este sistema rastrea la salud y la obsolescencia de las skills integradas en el workspace. El objetivo es transformar la estabilidad estática en una **estabilidad dinámica**.

## 📊 Estructura del Registro (`.knowledge/skill_lifecycle.json`)

El tracker mantiene un registro de cada skill estabilizada con los siguientes campos:

| Campo | Descripción | Trigger de Acción |
| :--- | :--- | :--- |
| `last_stabilized` | Fecha del último PASS en `eval-engine`. | Si es > 30 días $\rightarrow$ Sugerir `Autoresearch`. |
| `failure_count` | Contador de fallos en el campo o en el CI. | Si $\ge 3$ fallos $\rightarrow$ Trigger automático de `Repair`. |
| `model_version` | Modelo utilizado para crear la skill. | Si el modelo es obsoleto $\rightarrow$ Trigger de `Autoresearch`. |
| `status` | `STABLE` / `DEGRADED` / `UNDER_REPAIR`. | Define la confianza del Core al delegar la tarea. |

## 🔄 Flujos de Reacción

### 1. El Flujo de `Repair` (Reparación)
Se activa cuando una skill entra en estado `DEGRADED`.
- **Acción:** El sistema dispara un subagente de reparación con el `eval.yaml` y los logs de error.
- **Meta:** Corregir el código hasta que el `eval-engine` vuelva a dar **PASS**.
- **Cierre:** Resetear `failure_count` a 0 y volver a `STABLE`.

### 2. El Flujo de `Autoresearch` (Evolución)
Se activa por obsolescencia o búsqueda de optimización.
- **Acción:** El sistema busca nuevas técnicas o prompts más eficientes para la misma tarea.
- **Meta:** Mejorar la puntuación SHARP (especialmente *Asymmetry* y *Parsimony*).
- **Cierre:** Actualizar la skill y su versión en el tracker.

---

*Actualizado el 2026-10-01. Cierre del Sprint 2.1 - Ciclo de Vida de la Skill.*
