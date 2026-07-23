---
name: "observability"
metadata:
  category: "Governance"
  tags:
    - observabilidad
    - metricas
    - tracing
description: "Workflow de Engineering Observability: instrumentación, métricas, tracing y análisis del sistema y del AI Engineering OS."
user-invocable: false
---

# Workflow: Engineering Observability

## Propósito

Hacer observable el estado del producto, la infraestructura y el AI Engineering OS.

No corrige problemas.

No optimiza.

Su responsabilidad es responder:

> ¿Qué está ocurriendo?

> ¿Por qué ocurrió?

> ¿Cómo lo sabemos?

---

# Filosofía

> You can't improve what you can't observe.

Toda decisión importante debería poder respaldarse con datos.

La observabilidad no existe para generar dashboards.

Existe para reducir incertidumbre.

---

# Cuándo usarlo

- antes de optimizaciones
- después de incidentes
- antes de retrospectivas
- después de releases
- periódicamente (health checks)
- cuando aparecen degradaciones
- cuando un workflow parece ineficiente

---

# Capas de Observabilidad

## Producto

Responder:

- ¿Cómo usan el producto los usuarios?
- ¿Dónde abandonan?
- ¿Qué funcionalidades usan?
- ¿Qué errores encuentran?

---

## Aplicación

Responder:

- ¿Qué endpoints fallan?
- ¿Qué rutas son lentas?
- ¿Dónde hay excepciones?
- ¿Qué requests degradan?

---

## Infraestructura

Responder:

- CPU
- RAM
- Disco
- Red
- Base de datos
- Cache
- Workers
- Colas

---

## AI Engineering OS

Responder:

- ¿Qué workflows se ejecutan?
- ¿Cuánto tardan?
- ¿Cuáles fallan?
- ¿Cuáles generan retrabajo?
- ¿Qué agente intervino?
- ¿Qué costo tuvieron?
- ¿Qué decisiones produjo?

---

# Fases

## 1. Instrumentation Audit

Verificar cobertura de observabilidad.

Aplicación

Infraestructura

Base de datos

APIs

Agentes

Workflows

Eventos

---

## 2. Metrics

Definir KPIs.

### Ingeniería

- Lead Time
- Cycle Time
- MTTR
- Deployment Frequency
- Change Failure Rate

### Calidad

- Bugs post-release
- Cobertura
- Regresiones

### Performance

- Response Time
- Throughput
- Error Rate
- P95
- P99

### Agentes

- Tiempo por workflow
- Tokens consumidos
- Coste estimado
- Reintentos
- Hallucination Rate (manual)
- Tareas completadas

---

## 3. Logging

Verificar:

Logs estructurados

Correlation IDs

Request IDs

User IDs (anonimizados)

Sin información sensible.

---

## 4. Tracing

Seguir una operación completa.

Ejemplo:

Usuario

↓

Frontend

↓

API

↓

LLM

↓

MCP

↓

Supabase

↓

Respuesta

Detectar cuellos de botella.

---

## 5. Alerting

Clasificar alertas.

Critical

Major

Minor

Informational

Evitar alert fatigue.

---

## 6. Dashboard Review

Verificar que existan dashboards para:

Producto

Backend

Frontend

Infraestructura

AI

Workflows

Releases

---

## 7. Trend Analysis

Comparar:

Última semana

Último mes

Último trimestre

Responder:

¿Estamos mejorando?

¿Dónde empeoramos?

¿Qué tendencia preocupa?

---

## 8. Recommendations

Generar acciones.

Ejemplo:

Reducir latencia.

Agregar tracing.

Instrumentar endpoint.

Agregar métrica.

Eliminar dashboard inútil.

Nunca modificar automáticamente.

---

# Outputs

OBSERVABILITY_REPORT.md

Health Score

Lista de métricas

Alertas

Cuellos de botella

Recomendaciones

Dashboard Checklist

---

# Métricas mínimas

Ver [métricas mínimas](./references/metrics.md).

---

# Decisiones

Puede:

✔ detectar tendencias

✔ generar reportes

✔ proponer instrumentación

✔ identificar cuellos de botella

✔ recomendar alertas

Nunca:

✖ modificar código

✖ optimizar automáticamente

✖ borrar métricas

✖ cambiar dashboards

---

# Checklist

¿Podemos explicar cada incidente con datos?

¿Todos los workflows son medibles?

¿Hay métricas duplicadas?

¿Hay dashboards sin uso?

¿Las alertas generan acciones?

¿Las métricas ayudan a decidir?

¿Podemos demostrar que el sistema mejora?

## Related Skills

- [Performance Optimization](../performance-optimization): Para optimizar basado en métricas
- [Incident Response](../incident-response): Para detectar y responder a incidentes