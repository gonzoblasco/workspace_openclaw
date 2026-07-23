---
name: "incident-response"
metadata:
  category: "Workflow"
  tags:
    - incidentes
    - produccion
    - postmortem
description: "Workflow de Incident Response: gestión estructurada de incidentes en producción, desde la detección hasta el aprendizaje organizacional."
user-invocable: false
---

# Workflow: Incident Response

## Propósito

Gestionar incidentes de producción de forma rápida, ordenada y repetible.

Su prioridad es restaurar el servicio con el menor impacto posible.

No busca culpables.

Busca minimizar impacto y generar aprendizaje.

---

# Filosofía

> Restore service first. Understand later. Improve forever.

Los incidentes son inevitables.

La improvisación no.

---

# Cuándo usarlo

- caída de producción
- degradación severa
- pérdida de datos
- problemas de seguridad
- errores masivos
- aumento anormal de latencia
- alertas críticas
- rollback urgente

---

# Severidad

Ver [clasificación de severidad](./references/severity.md).

---

# Fases

## 1. Detection

Identificar:

- qué ocurrió
- cuándo comenzó
- quién lo detectó
- evidencia disponible

No asumir causas.

Registrar hechos.

---

## 2. Classification

Determinar:

- Severidad
- Alcance
- Usuarios afectados
- Riesgo

Asignar prioridad.

---

## 3. Containment

Reducir impacto.

Ejemplos:

- rollback
- feature flag OFF
- deshabilitar endpoint
- escalar infraestructura
- bloquear tráfico

Objetivo:

Evitar que el incidente empeore.

---

## 4. Service Restoration

Restaurar el servicio.

No optimizar.

No refactorizar.

No aprovechar para "mejorar código".

Solo devolver estabilidad.

---

## 5. Root Cause Analysis

Con el servicio estable.

Responder:

¿Qué ocurrió?

¿Por qué ocurrió?

¿Por qué no fue detectado antes?

¿Por qué llegó a producción?

Utilizar técnica de:

- Five Whys
- Timeline Analysis
- Fishbone (opcional)

Nunca buscar culpables.

Buscar causas sistémicas.

---

## 6. Corrective Actions

Definir:

Correcciones inmediatas

Correcciones permanentes

Automatizaciones

Tests nuevos

Alertas nuevas

Documentación necesaria

Cada acción debe tener responsable.

---

## 7. Knowledge Capture

Actualizar:

STATUS.md

CHANGELOG.md

HANDOFF.md

ADRs (si aplica)

Postmortem

Lessons Learned

---

## 8. Prevention

Preguntas:

¿Cómo evitamos que vuelva?

¿Qué workflow debería mejorar?

¿Qué test faltó?

¿Qué alerta faltó?

¿Qué documentación faltó?

Generar backlog.

---

# Outputs

INCIDENT_REPORT.md

POSTMORTEM.md

Timeline del incidente

Root Cause Analysis

Acciones correctivas

Acciones preventivas

Backlog de mejoras

---

# Plantilla de Postmortem

Ver [template de postmortem](./references/postmortem-template.md).

---

# Decisiones

Puede:

✔ clasificar

✔ priorizar

✔ recomendar rollback

✔ generar timeline

✔ generar postmortem

✔ proponer mejoras

Nunca:

✖ ocultar incidentes

✖ eliminar evidencia

✖ modificar historial

✖ cerrar incidentes sin RCA

---

# Checklist

¿El servicio fue restaurado?

¿Se preservó evidencia?

¿Existe Root Cause documentada?

¿Hay acciones preventivas?

¿Se actualizaron los documentos?

¿El incidente mejoró el sistema?

¿Podría repetirse mañana?

## Related Skills

- [Debug Investigation](../debug-investigation): Para investigar causa raíz post-incidente
- [Observability](../observability): Para mejorar detección y alertas