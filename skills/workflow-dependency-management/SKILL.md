---
name: "workflow-dependency-management"
description: "Workflow de Dependency Management: evaluación, actualización, gobernanza y salud del ecosistema de dependencias del proyecto."
---

# Workflow: Dependency Management

## Propósito

Mantener el ecosistema de dependencias saludable, seguro y sostenible durante todo el ciclo de vida del proyecto.

No instala dependencias automáticamente.

No actualiza versiones sin evaluación.

Su objetivo es minimizar el riesgo técnico mientras permite evolucionar el stack.

---

# Filosofía

> Every dependency is a long-term commitment.

Agregar una dependencia es incorporar código de terceros a nuestro proyecto.

Cada nueva dependencia debe justificar su existencia.

---

# Cuándo usarlo

- incorporar una nueva librería
- actualizar dependencias
- eliminar dependencias
- revisar vulnerabilidades
- preparar una release importante
- migraciones de framework
- auditorías periódicas

---

# Relación con otros workflows

Task Execution
↓

Dependency Management
↓

Review Quality
↓

Pre-Deploy QA

---

# Fases

## 1. Inventory

Construir inventario.

Registrar:

- dependencia
- versión
- uso
- tipo (runtime / dev)
- tamaño
- mantenedor
- licencia

Detectar:

- dependencias huérfanas
- duplicadas
- transitivas críticas

---

## 2. Health Assessment

Evaluar salud.

Responder:

¿Tiene mantenimiento activo?

¿Último release?

¿Cantidad de contributors?

¿Issues abiertos?

¿Tiempo promedio de respuesta?

¿Frecuencia de releases?

¿Está deprecada?

Clasificar:

🟢 Healthy

🟡 Watch

🔴 Risk

---

## 3. Risk Analysis

Evaluar:

- breaking changes
- CVEs
- compatibilidad
- lock-in
- dependencia crítica
- riesgo de abandono

Calcular nivel de riesgo.

---

## 4. Update Strategy

Clasificar actualizaciones.

Patch

Minor

Major

Para cada una:

beneficio

riesgo

esfuerzo

plan de rollback

---

## 5. Dependency Review

Antes de agregar una nueva librería responder:

¿Podemos resolverlo con el estándar del lenguaje?

¿Ya existe una librería equivalente?

¿Tenemos otra dependencia que haga lo mismo?

¿Cuánto código estamos importando?

¿El mantenimiento es confiable?

¿Qué costo tendrá migrar en el futuro?

Nunca agregar una dependencia sin justificación.

---

## 6. Compatibility Check

Verificar:

Framework

Node

TypeScript

Bundler

Testing

CI/CD

Cloud

No asumir compatibilidad.

---

## 7. Migration Planning

Si existe una actualización importante.

Generar:

plan

riesgos

pasos

rollback

tests necesarios

No implementar.

---

## 8. Knowledge Capture

Actualizar:

CHANGELOG

ADRs (si cambia arquitectura)

README (si cambia instalación)

Engineering Notes

Registrar:

por qué se adoptó

por qué se eliminó

por qué se postergó

---

# Outputs

DEPENDENCY_REPORT.md

Dependency Inventory

Risk Matrix

Health Report

Update Plan

Migration Plan

Recomendaciones

---

# Checklist

¿Hay dependencias sin uso?

¿Hay vulnerabilidades?

¿Hay versiones obsoletas?

¿Hay duplicación?

¿Existe lock-in innecesario?

¿La licencia es compatible?

¿La actualización tiene rollback?

---

# Decisiones

Puede:

✔ recomendar actualizaciones

✔ recomendar eliminación

✔ clasificar riesgos

✔ detectar duplicaciones

✔ proponer migraciones

Nunca:

✖ actualizar automáticamente

✖ instalar paquetes

✖ eliminar dependencias

✖ ignorar breaking changes

---

# Principios

Menos dependencias implican menos superficie de riesgo.

Toda dependencia debe justificar su existencia.

Actualizar de forma incremental reduce el riesgo.

Las vulnerabilidades críticas tienen prioridad.

La estabilidad vale más que tener la última versión.

Las decisiones sobre dependencias deben quedar documentadas.
