# Severidad de Incidentes — Referencia

## Clasificación

### SEV-1 — Crítico

**Definición:** Sistema caído, pérdida de datos, problema de seguridad.

**Características:**
- Servicio completamente no disponible
- Datos de usuarios comprometidos o perdidos
- Brecha de seguridad activa
- Impacto en todos los usuarios

**Acción:** Inmediata. Se interrumpe cualquier otra actividad. Respuesta 24/7.

---

### SEV-2 — Alto

**Definición:** Parte importante del sistema degradada.

**Características:**
- Funcionalidad crítica afectada
- Existe workaround pero es costoso
- Impacto en un subconjunto grande de usuarios
- Degradación severa de performance

**Acción:** Respuesta en horas hábiles. Se prioriza sobre trabajo planificado.

---

### SEV-3 — Medio

**Definición:** Problema localizado, impacto moderado.

**Características:**
- Funcionalidad no crítica afectada
- Existe workaround aceptable
- Impacto en pocos usuarios
- Degradación leve

**Acción:** Próximo sprint. Se agenda con el equipo.

---

### SEV-4 — Bajo

**Definición:** Incidente menor, puede esperar.

**Características:**
- Problema cosmético
- Funcionalidad alternativa disponible
- Sin impacto en usuarios
- Bug conocido sin consecuencias

**Acción:** Backlog. Se resuelve cuando hay capacidad.

## Escalamiento

| Severidad | Tiempo de respuesta | Tiempo de resolución | Notificación |
|---|---|---|---|
| SEV-1 | < 15 min | < 2 h | Todos los canales |
| SEV-2 | < 1 h | < 8 h | Slack / equipo |
| SEV-3 | < 1 día | < 1 semana | Issue tracker |
| SEV-4 | < 1 semana | Próximo sprint | Issue tracker |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Postmortem Template](./postmortem-template.md) — Plantilla de postmortem
