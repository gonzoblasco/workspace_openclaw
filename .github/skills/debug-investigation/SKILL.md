---
name: "debug-investigation"
metadata:
  category: "Workflow"
  tags:
    - bug
    - debugging
    - investigacion
description: "Workflow de Debug Investigation: investigación sistemática de bugs, degradaciones y comportamientos inesperados. Prioriza comprender antes de modificar código."
user-invocable: false
---

# Workflow: Debug Investigation

## Propósito

Investigar problemas de software de forma metódica hasta identificar la causa raíz.

No implementar fixes.

No refactorizar.

No optimizar.

Su única misión es responder:

> ¿Qué está pasando?

> ¿Por qué ocurre?

---

# Filosofía

> Diagnose before you prescribe.

La primera hipótesis suele ser incorrecta.

Nunca modificar código sin evidencia.

Los síntomas no son la causa.

---

# Cuándo usarlo

- bugs
- comportamiento inconsistente
- errores intermitentes
- degradación de performance
- race conditions
- problemas difíciles de reproducir
- regresiones
- errores reportados por usuarios

---

# Relación con otros workflows

Problema

↓

Debug Investigation

↓

Task Execution
(implementar el fix)

↓

Review Quality

↓

Pre-Deploy QA

---

# Fases

## 1. Intake

Registrar:

Problema observado

Entorno

Versión

Frecuencia

Impacto

Evidencia disponible

Nunca asumir la causa.

---

## 2. Reproduction

Objetivo:

Lograr reproducir el problema.

Registrar:

Pasos

Datos

Configuración

Navegador

Dispositivo

Usuario

Si no puede reproducirse:

documentar condiciones faltantes.

---

## 3. Scope Analysis

Determinar:

Siempre ocurre

A veces

Solo producción

Solo desarrollo

Solo ciertos usuarios

Solo ciertos datos

Responder:

¿Qué funciona correctamente?

Eso ayuda a reducir el espacio de búsqueda.

---

## 4. Evidence Collection

Recolectar:

Logs

Stack traces

Network

Database

Eventos

Screenshots

Videos

Telemetry

Nunca eliminar evidencia.

---

## 5. Hypothesis Generation

Generar múltiples hipótesis.

No enamorarse de la primera.

Ejemplo:

Hipótesis A

Hipótesis B

Hipótesis C

Ordenarlas por probabilidad.

---

## 6. Experiment Design

Diseñar experimentos mínimos. Ver [referencia de experimentos](./references/experiments.md).

Cada experimento debe responder una sola pregunta.

Nunca mezclar varios cambios.

---

## 7. Root Cause Analysis

Cuando exista evidencia suficiente.

Documentar:

Causa inmediata

Causa sistémica

Factores contribuyentes

Por qué no fue detectado

No buscar culpables.

Buscar mecanismos.

---

## 8. Handoff

Generar documentación para el workflow de implementación.

Debe incluir:

Resumen

Evidencia

Hipótesis descartadas

Root Cause

Recomendación de fix

Riesgos

Tests recomendados

---

# Outputs

DEBUG_REPORT.md

Pasos de reproducción

Timeline

Hipótesis

Experimentos

Root Cause

Recomendación

Casos de prueba sugeridos

---

# Técnicas sugeridas

Ver [técnicas sugeridas](./references/techniques.md).

---

# Checklist

¿El bug es reproducible?

¿Hay evidencia suficiente?

¿Se descartaron hipótesis?

¿Existe Root Cause?

¿El fix propuesto ataca la causa y no el síntoma?

¿Hay tests que eviten la regresión?

---

# Decisiones

Puede:

✔ generar hipótesis

✔ pedir evidencia

✔ recomendar experimentos

✔ documentar Root Cause

✔ proponer estrategia de solución

Nunca:

✖ modificar código

✖ implementar fixes

✖ refactorizar

✖ cerrar el bug sin evidencia

✖ asumir causas sin validación

---

# Principios

Los síntomas engañan.

La evidencia pesa más que la intuición.

Cada experimento debe responder una única pregunta.

Un buen diagnóstico vale más que un arreglo rápido.

Todo bug importante debe dejar conocimiento reutilizable.

## Related Skills

- [Performance Optimization](../performance-optimization): Para investigar degradaciones de rendimiento
- [Incident Response](../incident-response): Para bugs en producción con impacto
- [Vibe Code Cleanup](../vibe-code-cleanup): Para diagnosticar código generado por IA

## Relentless Resourcefulness

Antes de decir "no puedo" o pedir ayuda:

- Probá un approach distinto inmediatamente
- Después otro. Y otro más.
- Probá 5-10 métodos antes de considerar rendirte
- Usá TODAS las herramientas: CLI, browser, web search, subagentes
- Combiná herramientas de formas nuevas
- Buscá en memoria: "¿Hice esto antes? ¿Cómo?"
- Cuestioná los error messages — casi siempre hay workarounds
- Revisá logs de sesiones pasadas para patrones similares

"No puedo" = agoté todas las opciones, no "el primer intento falló".

Gonzo no debería tener que decirte que te esfuerces más.

## Structured Escalation — Cuándo y Cómo Escalar

Cuando estés stuck (no podés resolver algo, falta información crítica, o necesitás una decisión de Gonzo):

1. **Diagnosticá primero** — aplicá Relentless Resourcefulness (5-10 approaches)
2. **Si seguís stuck** — presentá un handoff estructurado:

```
BLOQUEO: [qué estoy intentando hacer]
CAUSA: [qué falló / qué falta]
INTENTOS: [qué probé ya]
NECESITO: [qué necesito de Gonzo — decisión, info, acceso]
ALTERNATIVA: [si no se puede, qué haría en su lugar]
```

**Nunca:** "No sé" o "No puedo" sin contexto.
**Siempre:** diagnóstico + qué necesitás + alternativa.

**Lección:** un handoff estructurado le ahorra a Gonzo tener que adivinar qué pasó. El bloqueo se resuelve más rápido cuando está bien definido.
