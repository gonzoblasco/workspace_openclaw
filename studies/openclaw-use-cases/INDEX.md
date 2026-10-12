# OpenClaw Use Cases - Estudio del Curso

**Curso:** Roadmap.sh × OpenClaw  
**Propósito:** Aprender mensajería contextual y escalada humana desde cero  
**Duración estimada:** 30 lecciones / 6 módulos  
**Fecha de actualización:** 2026-10-10  

---

## 📊 Progreso Actual

### Estado Global
```
Módulo 1: Asistentes de Mensajería Contextuales - 0/5 completado · 3 en curso
Módulos 2-6: En proceso
```

### Lecciones del Módulo 1 (borradores en curso)
1. **L01 - Conceptos Fundamentales de Asistentes de Mensajería** ⏳ En curso
   - Autonomía vs. Supervisión Humana
   - El principio "Safe First" en mensajería
   - De la intención a la acción
   → `L01-lesson-overview.md`

2. **L02 - Detección e Interpretación de Intenciones** ⏳ En curso
   - Clasificación de intenciones (FAQ, Escalación, Delegación, Error)
   - Confidence score y umbrales de decisión
   - Manejo de ambigüedades
   → `L02-intent-detection.md`

3. **L03 - Redacción de Respuestas Conscientes del Contexto** ⏳ En curso
   - Patrón "Draft → Review → Approve/Modify → Send"
   - Agregación contextual sin alucinaciones
   - Preservación de agencia humana
   → `L03-contextual-wrangling.md`

### Lecciones Pendientes ❌
- **L04** - Reglas de Escalación para Intervención Humana
- **L05** - Gestión de Límites de Contexto de Canal
- **L06** - (pendiente)
- ... 21 más pendientes en total

---

## 📚 Estructura del Curso: 6 Módulos, 30 Lecciones

### Módulo 1: Asistentes de Mensajería Contextuales (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| L01 | Conceptos Fundamentales | ⏳ En curso |
| L02 | Detección e Interpretación de Intenciones | ⏳ En curso |
| L03 | Redacción Contextual con Preservación de Agencia | ⏳ En curso |
| L04 | Reglas de Escalación para Intervención Humana | ❌ Pendiente |
| L05 | Gestión de Límites de Contexto de Canal | ❌ Pendiente |

### Módulo 2: Email Asistido con Clasificación Jerárquica (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| M2-L01 | Detección e Interpretación en Contexto de Email | ❌ Pendiente |
| M2-L02 | Enrutamiento por Prioridad y Urgencia | ❌ Pendiente |
| M2-L03 | Redacción de Respuestas Jerárquicas | ❌ Pendiente |
| M2-L04 | Escalación a Personas Especializadas | ❌ Pendiente |
| M2-L05 | Contexto Jerárquico en Threads de Email | ❌ Pendiente |

### Módulo 3: Social Media Automation (Contenido Consciente) (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| M3-L01 | Clasificación de Mensajes en Social Media | ❌ Pendiente |
| M3-L02 | Enrutamiento a Personalas de Contenido | ❌ Pendiente |
| M3-L03 | Redacción con Voz y Contexto del Brand | ❌ Pendiente |
| M3-L04 | Escalación a Community Managers | ❌ Pendiente |
| M3-L05 | Gestión de Crisis y Moderación | ❌ Pendiente |

### Módulo 4: Escalada Humana y Human-in-the-Loop (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| M4-L01 | Triaje y Priorización de Intervenciones | ❌ Pendiente |
| M4-L02 | Handoff Suave con Preservación de Hilo Conversacional | ❌ Pendiente |
| M4-L03 | Delegation Patterns (Agente → Humano → Agente) | ❌ Pendiente |
| M4-L04 | Post-Mortem de Intervenciones Humanas | ❌ Pendiente |
| M4-L05 | Learning Loops: Mejora Basada en Feedback | ❌ Pendiente |

### Módulo 5: Límites, Contexto y Memoria a Largo Plazo (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| M5-L01 | Gestión de Token Budget y Costos | ❌ Pendiente |
| M5-L02 | Memory Retrieval Optimizado por Intención | ❌ Pendiente |
| M5-L03 | Preventing Context Bleed Across Channels | ❌ Pendiente |
| M5-L04 | Razonamiento Profundo sin Sobrecarga de Costo | ❌ Pendiente |
| M5-L05 | Balance Autonomía ↔ Costo | ❌ Pendiente |

### Módulo 6: Integración, Operaciones y Mejora Continua (5/30 lecciones)
| Lección | Tema | Estado |
|---------|------|--------|
| M6-L01 | Orquestación Multi-Canal Centralizada | ❌ Pendiente |
| M6-L02 | Observabilidad y Logging Unificado | ❌ Pendiente |
| M6-L03 | Continuous Improvement Loop (A/B Testing) | ❌ Pendiente |
| M6-L04 | Scale Patterns: De 1 a 1000 Agentes | ❌ Pendiente |
| M6-L05 | Operación Day-to-Day, Health Checks y Maintenance | ❌ Pendiente |

---

## 🗺️ Roadmap del Curso

```mermaid
graph LR
    A[Módulo 1: Mensajería] --> B[Módulo 2: Email]
    B --> C[Módulo 3: Social Media]
    C --> D[Módulo 4: Escalada Humana]
    D --> E[Módulo 5: Contexto y Memoria]
    E --> F[Módulo 6: Integración y Ops]
    
    A -.-> "Principios base" -. B
    B -.-> "Jerarquía + Prioridad" -. C
    C -.-> "Content Conscience" -. D
    D -.-> "Human-in-the-loop patterns" -. E
    E -.-> "Context management at scale" -. F
    F -.-> "Production readiness" -. A
```

---

## 📝 Notas de la Actualización 2026-10-10

### Cambios Implementados en esta Versión

1. **Reestructuración completa** a 6 módulos × 5 lecciones = 30 lecciones totales
   - Cada módulo con un tema central claro
   - Escalable desde MVP hasta producción

2. **Llevado el contenido previo** de las lecciones L01-L03 originales a la nueva estructura:
   - `L01-lesson-overview.md` → Conceptos fundamentales
   - `L02-intent-detection.md` → Detección e interpretación de intenciones
   - `L03-contextual-wrangling.md` → Redacción contextual con preservación de agencia

3. **Nuevo enfoque** basado en:
   - "Safe first" responses (primero, no hacer daño)
   - Preservación de agencia humana
   - Context-aware wrangling sin alucinaciones
   - Escalada inteligente a humanos

---

## 🔗 Enlaces Útiles

- **SOUL.md**: Definición de voz personal y personalidad del agente
- **AGENTS.md**: Reglas operativas del asistente
- **docs/AGENTS-DETALLE.md**: Extensión detallada de AGENTS.md
- **docs/AGENTS-DETALLE.md**: Extensión operativa de AGENTS.md
- **docs/adr/ADR-086-embudo-de-entrada-conversacional.md**: Marco del embudo de entrada conversacional

---

*Documento generado siguiendo la reestructuración del curso OpenClase Use Cases (6 módulos, 30 lecciones totales)*
