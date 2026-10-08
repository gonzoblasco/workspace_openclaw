# Métricas de madurez del Crew (M0‑M5)

> Este documento define **las métricas observables** que permiten evaluar la madurez de cada rol del Crew en las fases M0‑M5 descritas en `docs/ROADMAPS.md`.

| Fase | Descripción | Métrica clave | Umbral de éxito |
|---|---|---|---|
| **M0 - Diagnóstico** | El rol existe y tiene un `ROADMAP.md` con versión `v0.1`. | Presencia del archivo y encabezado `Versión actual: v0.1`. | Archivo presente y versión exacta. |
| **M1 - Nivelación** | Todas las secciones obligatorias están completadas y la tabla de capacidades está verificada. | Número de secciones (7) y salida sin errores de `check‑roadmaps.py`. | 7 secciones sin fallos. |
| **M2 - Tracking vivo** | Cada salto de versión está registrado y los criterios de listo están cumplidos. | Entradas en `CHANGELOG.md` para cada salto + auditoría sin drift de versión. | Cada salto tiene marca `✅` en el changelog. |
| **M3 - Escalada a v0.5** | Dependencias críticas resueltas; el rol opera sin supervisión línea‑por‑línea. | Resultados de CI sin `TODO` en el roadmap. | CI verde y sin tareas pendientes. |
| **M4 - Verificación externa** | Saltos de versión validados contra fuentes reales (filesystem, runtime). | Salida de `check‑roadmaps.py` sin warnings. | 0 warnings. |
| **M5 - v1.0** | Gates de calidad (`critic`, `auditor`) están en `v1.0` y pueden ser invocados por el resto del Crew. | Versión declarada `v1.0` en `ROADMAP.md` de `critic` y `auditor`. | Ambas versiones `v1.0`. |

> **Cómo usar**: Cada pipeline de CI ejecuta `scripts/check-roadmaps.py`. Si la salida indica `✅` para todas las etapas y no hay drift de versión, el rol ha superado la fase correspondiente.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->