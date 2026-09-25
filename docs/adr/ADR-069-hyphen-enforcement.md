---
title: ADR-069 – Enforce hyphen usage in markdown/spec files
status: proposed
deciders:
  - Gonzo
date: 2026-09-25
---

## Contexto

Durante la creación del archivo `spec.md` para el proyecto **kanam‑spec** se utilizó el carácter guion largo (en‑dash, U+2013) en varios lugares. Según la regla de estilo de Gonzo, siempre se debe usar el guion común (`-`) en la documentación y código fuente. El uso de guiones largos provocó que la herramienta de validación fallara y que los commits fueran bloqueados.

## Decisión

1. **Reemplazar todos los guiones largos por guiones comunes** en los archivos markdown que formen parte del repositorio.
2. **Implementar una verificación automática** antes de cada commit que detecte guiones largos y los convierta o indique al usuario que los corrija.
3. **Documentar la decisión** en este ADR y añadir una referencia a él desde el `CHANGELOG.md` y futuros documentos pertinentes.

## Consecuencias

* Mejora la consistencia del estilo de escritura en el proyecto.
* Evita errores de pre‑commit relacionados con el carácter de guion.
* Se necesita una herramienta o script (ej. `check_em_dash.py` ya existente) que se ejecute como parte del hook de pre‑commit, o crear un nuevo *skill* llamado `hyphen‑enforcer` que realice la sustitución automática.

## Próximos pasos

* Añadir este ADR al índice de ADRs (`docs/adr/README.md`).
* Evaluar la creación del *skill* `hyphen-enforcer` que pueda ser llamado manualmente o integrado al flujo de CI.
* Actualizar la política de pre‑commit si fuera necesario para incluir la verificación de guiones largos.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

