---
name: "knowledge-management"
description: "Workflow de Knowledge Management: gobernanza, sincronización y evolución de la base de conocimiento del proyecto. Mantiene una única fuente de verdad."
---

# Workflow: Knowledge Management

## Propósito

Gestionar el conocimiento persistente del proyecto durante todo su ciclo de vida.

No desarrolla features.

No modifica código de negocio.

Su responsabilidad es mantener la documentación consistente, actualizada y útil para humanos y agentes.

---

# Filosofía

> Every decision deserves a home.

La documentación no es un entregable.

Es una memoria compartida.

Todo conocimiento importante debe existir una sola vez y ser fácilmente descubrible.

---

# Cuándo usarlo

- al finalizar un workflow
- antes de iniciar una nueva sesión
- antes de crear un PR
- después de cerrar un epic
- después de una retrospectiva
- cuando cambian decisiones arquitectónicas
- cuando aparecen inconsistencias

---

# Artefactos conocidos

## Estratégicos

- BRIEF.md
- EVALUATION.md
- DEFINITION.md
- ROADMAP.md

## Arquitectura

- ARCHITECTURE.md
- DATA_MODEL.md
- DESIGN.md
- docs/adr/

## Estado

- STATUS.md
- TRACKER.md
- HANDOFF.md

## Proyecto

- README.md
- CHANGELOG.md
- CONTRIBUTING.md

## Memoria

- memory/YYYY-MM-DD.md

---

# Principios

Single Source of Truth.

No duplicar conocimiento.

Documentar decisiones, no conversaciones.

Preferir actualizar antes que crear nuevos archivos.

Eliminar conocimiento obsoleto.

Mantener trazabilidad.

---

# Fases

## 1. Discovery

Detectar:

- qué documentos existen
- cuáles faltan
- cuáles están vacíos
- cuáles parecen abandonados

Construir un mapa de conocimiento.

---

## 2. Ownership

Determinar el dueño de cada información.

Ejemplos:

Arquitectura

↓

ARCHITECTURE.md

Decisión técnica

↓

ADR

Estado actual

↓

STATUS.md

Historial

↓

CHANGELOG.md

Nunca duplicar.

---

## 3. Consistency Audit

Buscar contradicciones.

Ejemplos:

ROADMAP dice:

OAuth pendiente

STATUS dice:

OAuth terminado

↓

Inconsistencia.

Otro ejemplo:

ADR indica Hexagonal.

README describe MVC.

↓

Inconsistencia.

Generar reporte.

Nunca modificar automáticamente.

---

## 4. Freshness

Detectar conocimiento viejo.

Preguntas:

¿Hace cuánto no se actualiza?

¿Sigue siendo válido?

¿Hace referencia a archivos eliminados?

¿Habla de features que ya no existen?

Clasificar:

🟢 Vigente

🟡 Revisar

🔴 Obsoleto

---

## 5. Knowledge Graph

Relacionar información.

Ejemplo:

Feature

↓

Epic

↓

ADR

↓

PR

↓

CHANGELOG

↓

HANDOFF

↓

STATUS

Construir referencias cruzadas.

---

## 6. Compression

Reducir redundancia.

Buscar:

- texto repetido
- tablas repetidas
- ejemplos repetidos
- decisiones duplicadas

Proponer consolidación.

Nunca eliminar automáticamente.

---

## 7. Evolution

Detectar:

- documentos que deberían dividirse
- documentos demasiado pequeños
- nuevos documentos necesarios
- documentos innecesarios

Proponer mejoras.

---

## 8. Publishing

Actualizar índice.

Verificar enlaces.

Verificar referencias.

Actualizar fechas.

Generar reporte final.

---

# Outputs

KNOWLEDGE_REPORT.md

Knowledge Map

Inconsistencias encontradas

Documentos obsoletos

Documentos faltantes

Propuestas de consolidación

Knowledge Graph

---

# Decisiones

Puede:

✔ detectar inconsistencias

✔ recomendar consolidaciones

✔ construir mapa de conocimiento

✔ generar reportes

✔ actualizar índices

Nunca:

✖ inventar decisiones

✖ sobrescribir ADRs

✖ eliminar documentación

✖ cambiar STATUS automáticamente

✖ modificar conocimiento sin aprobación

---

# Checklist

¿Existe una única fuente para cada decisión?

¿Hay contradicciones?

¿Hay documentos abandonados?

¿Hay referencias rotas?

¿Hay duplicación?

¿Hay conocimiento sin documentar?

¿El proyecto puede entenderse sin leer el historial del chat?