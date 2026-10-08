---
title: threat-modeling
description: TODO: add description
---
# threat-modeling

Identificar, evaluar y mitigar riesgos de seguridad antes de que se materialicen mediante un proceso estructurado de modelado de amenazas.

## Pasos

1️⃣ **Definir el alcance y los activos críticos**  
   - Listar los componentes del sistema (APIs, bases de datos, UI, servicios externos).  
   - Clasificar cada activo por nivel de sensibilidad (público, interno, confidencial, altamente confidencial).  
   - Evidencia: archivo `threat-model/assets.md` con la lista y clasificación.

2️⃣ **Identificar actores y motivaciones**  
   - Enumerar posibles actores (usuarios malintencionados, atacantes automatizados, insiders, proveedores).  
   - Asociar a cada actor sus motivaciones típicas (robo de datos, denegación de servicio, escalada de privilegios, beneficio financiero).  
   - Evidencia: tabla en `threat-model/actors.md` con actor, motivación y capacidad.

3️⃣ **Enumerar vectores de ataque (STRIDE o PASTA)**  
   - Aplicar la metodología STRIDE (Spoofing, Tampering, Repudiation, Information Disclosure, Denial of Service, Elevation of Privilege).  
   - Para cada activo, generar al menos un escenario por cada categoría STRIDE.  
   - Evidencia: documento `threat-model/vectors.md` con matriz activo × amenaza.

4️⃣ **Evaluar impacto y probabilidad**  
   - Asignar una puntuación de impacto (1‑5) y probabilidad (1‑5) a cada escenario.  
   - Calcular la riesgo = impacto × probabilidad.  
   - Priorizar los riesgos con puntuación ≥ 12 (en escala 1‑25).  
   - Evidencia: hoja de cálculo `threat-model/risk-scoring.xlsx` o CSV equivalente.

5️⃣ **Definir y priorizar mitigaciones**  
   - Para cada riesgo priorizado, proponer al menos una mitigación (control preventivo, detector, respuesta).  
   - Clasificar la mitigación por tipo: arquitectónico, de código, operativo.  
   - Estimar esfuerzo y definir owner.  
   - Evidencia: archivo `threat-model/mitigations.md` con tabla riesgo → mitigación → owner → esfuerzo.

6️⃣ **Validar y actualizar el modelo**  
   - Revisar el modelo con al menos un stakeholder de seguridad y un desarrollador.  
   - Incorporar feedback y actualizar los artefactos.  
   - Programar una revisión trimestral o ante cambios significativos en la arquitectura.  
   - Evidencia: acta de revisión in `threat-model/review-log.md`.

## Resultado esperado

- Un conjunto de documentos (assets, actores, vectores, scoring, mitigaciones, log) que describen de forma explícita los riesgos de seguridad del sistema y las acciones para reducirlos.
- Un backlog de mitigaciones prioritarias listo para ser implementado por el equipo de desarrollo.
- Evidencia verificable de que se ha seguido un proceso proactivo de modelado de amenazas antes de que se materialicen incidentes.

## Prerequisitos

- Acceso a la arquitectura del diagramas (C4, arquitectura de componentes o similar).
- Conocimiento básico de metodologías de amenazas (STRIDE, PASTA, CVSS).
- Herramientas de edición de texto y hojas de cálculo (o su equivalente en formato Markdown/CSV).

## Salida de ejemplo

Al ejecutar la skill, se genera dentro de la carpeta `threat-model/`:
```
threat-model/
├── assets.md
├── actors.md
├── vectors.md
├── risk-scoring.csv
├── mitigations.md
└── review-log.md
```