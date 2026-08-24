# Knowledge Check - Core Properties of Agentic AI Systems

**Curso:** Inside Agentic AI: Foundations and Frontiers
**Cubre:** Videos 1-3 (Overview, What Makes AI Agentic?, Core Properties)
**Fecha:** 2026-08-21

---

## Pregunta

**¿Qué acciones ilustran la capacidad de self-reflection de la agentic AI?** (Respuesta múltiple)

1. Re-ejecutar pasos automáticamente tras detectar un resultado defectuoso
2. Ejecutar tool calls basándose en prompts del usuario
3. Preguntarse "¿Este plan cumple el objetivo?" y ajustar si no
4. Evitar el uso de memoria para prevenir overfitting
5. Completar solo workflows pre-programados

## Respuestas correctas: 1 y 3

**✅ Opción 1** - "Re-ejecutar pasos tras un resultado defectuoso" es comportamiento reflexivo (feedback + re-ejecución). Correcta.

**✅ Opción 3** - "¿Este plan cumple el objetivo?" y ajustar si no es **self-reflection puro** (pre-acción): el agente evalúa su propio razonamiento antes de que el error cause daño. Es el ejemplo literal del video 3 ("a planning agent might pause and ask..."). Correcta.

**❌ Opción 2** - Ejecutar tool calls por prompts = **reactive behavior** (IA tradicional), no reflexión.

**❌ Opción 4** - Evitar memoria para "prevenir overfitting" es una trampa conceptual. Agentic AI usa memoria para continuidad y aprendizaje; overfitting es un concepto de ML sin relación con la memoria del agente.

**❌ Opción 5** - Completar solo workflows pre-programados es lo **opuesto** a agentic: los agentes van más allá adaptándose.

---

## Lección

Los quizzes de Codecademy pueden tener **múltiples respuestas correctas**. Leer todas las opciones antes de responder, y buscar las que ilustran **adaptación, reflexión y autonomía** - descartar las que describen comportamiento reactivo, pre-programado o estático.
