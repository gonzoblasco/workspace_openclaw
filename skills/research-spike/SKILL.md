---
name: "research-spike"
description: "Workflow de Research Spike: investigación técnica para reducir incertidumbre antes de tomar decisiones o implementar soluciones."
user-invocable: false
---

# Workflow: Research Spike

## Propósito

Reducir incertidumbre técnica mediante investigación estructurada.

No implementar soluciones.

No escribir código de producción.

No tomar decisiones definitivas.

Su misión es responder:

> ¿Qué necesitamos aprender antes de construir?

---

# Filosofía

> Learn first. Build second.

Un Spike compra conocimiento.

No funcionalidades.

Su éxito se mide por la incertidumbre eliminada, no por las líneas de código escritas.

---

# Cuándo usarlo

- tecnología nueva
- librería desconocida
- API externa
- arquitectura incierta
- decisión importante
- benchmark entre alternativas
- integración compleja
- proof of concept
- dudas sobre viabilidad

---

# Relación con otros workflows

Product Discovery

↓

Research Spike

↓

Engineering Decision

↓

Task Execution

---

# Fases

## 1. Research Question

Definir una única pregunta.

Ejemplos:

¿Conviene MCP o REST?

¿Conviene Supabase o Neon?

¿Podemos soportar 100k usuarios?

¿Qué limitaciones tiene esta API?

Nunca investigar sin una pregunta clara.

---

## 2. Success Criteria

Responder:

¿Qué evidencia necesitamos para considerar respondida la pregunta?

Ejemplos:

- benchmark
- documentación oficial
- prototipo
- prueba de integración
- experimento

---

## 3. Scope

Definir límites.

Qué investigamos.

Qué NO investigamos.

Tiempo máximo.

Profundidad esperada.

Evitar investigación infinita.

---

## 4. Information Gathering

Recolectar evidencia.

Fuentes sugeridas:

Documentación oficial

RFCs

Repositorios

Issues

Discusiones técnicas

Blogs de ingeniería

Benchmarks

Experimentos propios

Priorizar fuentes primarias.

---

## 5. Experimentation

Si es necesario.

Construir un prototipo mínimo.

No reutilizar código.

No convertir el Spike en producción.

Objetivo:

Responder preguntas.

No desarrollar producto.

---

## 6. Analysis

Comparar alternativas.

Para cada opción documentar:

beneficios

riesgos

coste

mantenimiento

escalabilidad

complejidad

madurez

---

## 7. Recommendation

Responder:

¿Qué recomendamos?

¿Por qué?

¿Qué evidencia respalda esa decisión?

¿Qué incertidumbre permanece?

Ser explícito sobre el nivel de confianza.

---

## 8. Knowledge Capture

Actualizar:

Research Notes

ADRs (si la decisión se toma)

Knowledge Base

Lessons Learned

No perder el conocimiento generado.

---

# Outputs

SPIKE_REPORT.md

Research Notes

Comparativa de alternativas

Resultados de experimentos

Recomendación

Preguntas abiertas

Riesgos identificados

---

# Plantilla

Ver [template de reporte](./references/template.md).

---

# Checklist

¿Existe una pregunta concreta?

¿Hay evidencia suficiente?

¿Las fuentes son confiables?

¿El experimento respondió la pregunta?

¿La recomendación está respaldada?

¿Quedó conocimiento reutilizable?

---

# Decisiones

Puede:

✔ investigar

✔ comparar alternativas

✔ ejecutar experimentos pequeños

✔ generar recomendaciones

✔ identificar riesgos

Nunca:

✖ implementar producción

✖ convertir el Spike en feature

✖ prolongar indefinidamente la investigación

✖ tomar decisiones sin evidencia

---

# Principios

La investigación tiene límite de tiempo.

Una buena pregunta vale más que cien búsquedas.

La evidencia pesa más que las opiniones.

Los prototipos son descartables.

El conocimiento generado debe permanecer en el proyecto.

No toda investigación termina en una implementación.
