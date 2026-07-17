---
name: "po-review"
description: "Revisar un producto como PO: cuestionar scope, recortar MVP, validar decisiones."
author: "Gonzo"
type: skill
---

# PO Review — Revisión de Producto como Product Owner

## Overview

Un Product Owner externo revisa el producto en desarrollo y cuestiona supuestos. No es una auditoría técnica ni un code review. Es una revisión de **qué se está construyendo, para quién, y por qué**.

El objetivo es encontrar:
- Features que no deberían estar en el MVP
- Promesas incumplidas (humo)
- Supuestos no validados
- Decisiones sin justificación
- Roadmaps irreales
- Falta de plan de distribución

**Tono:** directo, sin vueltas. La honestidad vale más que la cortesía. Si algo no tiene sentido, se dice.

---

## Checklist de Revisión

### 1. ¿El MVP es realmente mínimo?

Buscar features que se puedan diferir a fases posteriores. Preguntar:
- ¿Esta feature resuelve el problema central del usuario?
- ¿Qué pasa si la sacamos? ¿El producto sigue en pie?
- ¿Estamos construyendo para el 20% de usuarios que piden features avanzadas?

**Señal de alerta:** el MVP tiene más de 3-5 features principales.

### 2. ¿Hay humo?

Features prometidas pero no implementadas ni planificadas:
- Screenshots o demos de features que no existen
- "Pronto" en la documentación
- Features mencionadas en el BRIEF pero sin issues, tareas, ni código
- Funcionalidades que dependen de integraciones no confirmadas

**Señal de alerta:** el README o landing page describe más de lo que el repo implementa.

### 3. ¿El target está claro?

- ¿Para quién es realmente este producto?
- ¿Hay una persona de usuario definida? ¿O es "para todos"?
- ¿El problema que resuelve está validado con usuarios reales?
- ¿O estamos asumiendo que el problema existe?

**Señal de alerta:** "desarrolladores" o "usuarios" sin más especificación.

### 4. ¿Las decisiones técnicas están justificadas?

Revisar ADRs (Architecture Decision Records):
- ¿Cada decisión importante tiene un ADR?
- ¿El ADR explica el contexto, las alternativas consideradas, y por qué se eligió esta opción?
- ¿O son decisiones "porque sí" o "porque es lo que conozco"?

**Señal de alerta:** decisiones técnicas sin documento, o ADRs que solo dicen "usamos X".

### 5. ¿El roadmap es realista?

- ¿Las estimaciones consideran imprevistos?
- ¿Hay dependencias externas no controladas?
- ¿El roadmap tiene fechas o solo "Q1", "pronto"?
- ¿Hay margen para iterar después del MVP?

**Señal de alerta:** roadmap sin fechas, o con fechas que asumen que todo sale perfecto.

### 6. ¿Hay plan de distribución?

- ¿Cómo llega el producto a los usuarios?
- ¿Hay estrategia de lanzamiento?
- ¿Se necesita aprobación de stores, compliance, o socios?
- ¿Hay presupuesto para ads, hosting, o infraestructura?

**Señal de alerta:** "lo construimos y ya veremos".

---

## Output

La revisión produce dos cosas:

### Lista de Issues Encontrados

Cada issue incluye:
- **Severidad:** crítica | alta | media | baja
- **Descripción:** qué está mal
- **Evidencia:** dónde se ve (archivo, línea, conversación)
- **Recomendación:** qué hacer al respecto

### Recomendaciones

Priorizadas por impacto:
1. **Impostergable** — arreglar antes de seguir
2. **Alta prioridad** — resolver en este sprint
3. **Para el roadmap** — planificar para después del MVP
4. **Nice to have** — considerar si sobra tiempo

---

## Ejemplo Real: Revisión de create-with-ai

**Contexto:** El proyecto "create-with-ai" tenía un BRIEF que prometía 5 fases de generación de contenido con IA: blog posts, emails, landing pages, videos, y análisis.

**Lo que encontró la PO Review:**

| Issue | Severidad | Detalle |
|-------|-----------|---------|
| MVP inflado | Crítica | 5 fases de contenido es un producto completo, no un MVP. Ninguna fase estaba validada con usuarios. |
| Humo en BRIEF | Alta | El BRIEF mencionaba "generación de video" pero no había investigación sobre APIs de video, costos, ni factibilidad técnica. |
| Target difuso | Alta | "Creadores de contenido" es demasiado amplio. ¿Bloggers? ¿Marketers? ¿YouTubers? Cada uno necesita algo distinto. |
| Sin ADRs | Media | No había documentación de por qué se eligió OpenAI vs Claude, ni por qué React vs Vue. |
| Roadmap irreal | Alta | 5 fases en 3 meses asumiendo que cada fase sale en 2-3 semanas sin imprevistos. |
| Sin plan de distribución | Media | No había estrategia de cómo llegar a los primeros 100 usuarios. |

**Resultado:** El MVP se recortó de 5 fases a 1 (solo blog posts), con un target específico (desarrolladores que escriben contenido técnico), y se agregó un plan de distribución antes de escribir más código.

---

## Cuándo Usar Esta Skill

- **Antes de empezar a codificar** — para validar que el BRIEF tiene sentido
- **Durante el desarrollo** — para detectar scope creep a tiempo
- **Antes del lanzamiento** — para asegurar que el MVP es realmente mínimo
- **Después de feedback** — para decidir qué features priorizar

No usar para code review, debugging, o evaluación técnica. Eso es trabajo de otras skills.
