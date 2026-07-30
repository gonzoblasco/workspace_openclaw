---
name: "engineering-governance"
metadata:
  category: "Governance"
  tags:
    - gobernanza
    - auditoria
    - mejora-continua
description: "Workflow de Engineering Governance: evolución continua del AI Engineering OS. Audita workflows, consolida aprendizajes, elimina duplicaciones y propone mejoras sistémicas."
user-invocable: false
---

# Workflow: Engineering Governance

## Propósito

Mantener y evolucionar el sistema de workflows, principios y estándares de ingeniería.

No desarrolla features.
No escribe código de producto.

Su cliente es el propio AI Engineering OS.

---

# Filosofía

> Build the system that builds the system.

El objetivo no es optimizar un proyecto.

El objetivo es mejorar continuamente la organización que desarrolla proyectos.

---

# Cuándo usarlo

- después de cerrar un milestone
- después de cerrar un epic importante
- después de varios PRs similares
- después de una retrospectiva
- cuando aparecen bugs repetitivos
- cuando varios workflows empiezan a duplicar responsabilidades
- cuando cambian las mejores prácticas de la industria

Nunca durante la implementación de una tarea.

---

# Inputs

- todos los workflows
- ADRs
- retrospectives
- STATUS.md
- CHANGELOG.md
- HANDOFF.md
- métricas de ejecución
- bugs
- incidentes
- feedback humano
- **incidentes externos** (ej: OpenAI/Hugging Face julio 2026) — lecciones de seguridad, arquitectura de agentes, patrones de ataque/defensa

---

# Fases

## 1. System Health Check

Responder:

- ¿Qué workflows casi nunca se usan?
- ¿Qué workflows generan más valor?
- ¿Qué partes del proceso generan fricción?
- ¿Dónde aparecen cuellos de botella?
- ¿Qué tareas siguen siendo manuales?

---

## 2. Pattern Mining

Buscar patrones repetitivos.

Ejemplos:

- mismo checklist copiado
- mismas validaciones
- mismas decisiones
- mismos prompts
- mismos errores
- mismas soluciones
- **mismos patrones de incidentes externos** (ej: agentes escapando sandboxes, zero-days en infraestructura compartida)

Si un patrón aparece repetidamente:

proponer extraerlo.

---

## 3. Workflow Audit

Auditar cada workflow. Ver [audit checklist](./references/audit-checklist.md).

Clasificar:

🟢 Healthy

🟡 Needs Review

🔴 Needs Refactor

---

## 4. Knowledge Consistency

Buscar inconsistencias entre:

- ADRs
- STATUS
- ROADMAP
- TRACKER
- HANDOFF
- CHANGELOG

Detectar documentos contradictorios.

Nunca modificar automáticamente.

Generar recomendaciones.

---

## 5. Industry Review

Comparar el AI Engineering OS con el estado del arte.

Buscar nuevas prácticas relacionadas con:

- AI Engineering
- Agentic Systems
- MCP
- RAG
- Testing
- Accessibility
- DevOps
- Architecture
- OSS

Responder:

¿Qué deberíamos adoptar?

¿Qué deberíamos abandonar?

---

## 6. Governance Review

Verificar:

- workflows obsoletos
- workflows muy grandes
- responsabilidades mezcladas
- skills que deberían fusionarse
- skills demasiado genéricas

Proponer:

- merge
- split
- deprecación
- nueva versión

Nunca modificar automáticamente.

---

## 7. Engineering Principles

Auditar los principios.

Preguntas:

¿Siguen siendo válidos?

¿Hay contradicciones?

¿Falta alguno?

Ejemplos:

- Accessibility First
- Security by Default
- Progressive Disclosure
- Small Commits
- Spec Driven Development
- HTML before ARIA
- Documentation as Code

---

## 8. Improvement Proposal

Generar RFCs. Ver [template de RFC](./references/rfc-template.md).

Nunca aplicar cambios automáticamente.

---

## Outputs

- GOVERNANCE_REPORT.md

- RFCs

- propuestas de nuevos workflows

- propuestas de deprecación

- mejoras de Engineering Principles

- backlog de mejoras del AI Engineering OS

---

# Decisiones

Puede:

✔ recomendar

✔ priorizar

✔ detectar

✔ comparar

✔ generar RFCs

Nunca:

✖ modificar workflows automáticamente

✖ editar ADRs

✖ cambiar principios

✖ eliminar documentación

Todo cambio requiere aprobación humana.

---

# Principios

La estabilidad vale más que la novedad.

No optimizar sin evidencia.

Eliminar complejidad antes que agregar funcionalidades.

Cada workflow debe tener una única responsabilidad.

Las mejoras deben ser incrementales.

Las decisiones deben quedar documentadas.

La gobernanza existe para reducir la entropía del sistema.

---

# Checklist final

- ¿Hay duplicación?

- ¿Hay contradicciones?

- ¿Hay deuda de proceso?

- ¿Hay workflows obsoletos?

- ¿Hay conocimiento sin documentar?

- ¿Hay nuevos patrones que merecen un workflow?

- ¿El sistema es hoy mejor que hace un mes?

## Related Skills

- [Knowledge Management](../knowledge-management): Para mantener la base de conocimiento actualizada
- [Observability](../observability): Para medir la salud del sistema

## Growth Loops — Ciclos de Mejora Continua

Cuatro ciclos que mantienen el sistema evolucionando:

### 1. Curiosidad
Periódicamente, preguntarse: "¿Qué no sé que me ayudaría a hacer mejor mi trabajo?" Investigar skills de ClawHub, leer documentación, explorar tools nuevas.

### 2. Reconocimiento de Patrones
Cuando una situación se repite 3+ veces, no es coincidencia — es un patrón. Documentarlo en LEARNINGS.md y considerar promoverlo a SOUL/TOOLS/AGENTS.

### 3. Expansión de Capacidades
Cuando una tarea se hace 2+ veces y requiere el mismo proceso manual, considerar: ¿se puede skill-izar? ¿se puede automatizar? ¿se puede documentar como workflow?

### 4. Seguimiento de Resultados
Después de implementar una mejora, verificar: ¿realmente mejoró algo? ¿O solo agregó complejidad? Si no hay mejora medible, revertir.

**Lección:** la mejora continua no es automática — necesita ciclos explícitos. Sin ellos, el sistema se estanca o empeora.

## Evaluación de Skills Externas — Cómo Decidir

Cuando revisemos skills de ClawHub (o cualquier skill externa), seguir este proceso:

1. **Leer el SKILL.md completo** — entender qué hace realmente
2. **Identificar qué pisa** — ¿ya tenemos algo equivalente? ¿en AGENTS.md, LEARNINGS.md, MEMORY.md?
3. **Identificar qué aporta** — ¿tiene patrones, frameworks o ideas que no tenemos?
4. **Decidir:**
   - **Instalar** — solo si aporta algo que no tenemos Y no podemos integrar como convención
   - **Robar ideas** — si tiene patrones útiles que podemos adoptar en nuestro sistema
   - **Pasar** — si pisa lo que tenemos o no es relevante
5. **Si robamos:** documentar en LEARNINGS.md, actualizar AGENTS.md/MEMORY.md según corresponda

**Regla:** preferir integrar patrones como convención propia antes que instalar skills externas. Menos skills = menos contexto quemado = sistema más rápido y predecible.