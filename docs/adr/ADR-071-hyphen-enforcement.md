---
title: ADR-071 - Hyphen enforcement in markdown/spec files
status: proposed
deciders:
  - Gonzo
date: 2026-09-25
---

## Contexto

Durante la creación del archivo `spec.md` para el proyecto **kanam-spec** se utilizó el carácter guion largo (en-dash, U+2013). La política de estilo del workspace (ADR-056) exige que en la documentación se emplee siempre el guion común (`-`). El uso del en-dash provocó fallos en el pre-commit y la necesidad de crear un script de corrección.

## Decisión

1. **Crear un script** `scripts/hyphen_enforcer.sh` que recorra todos los archivos markdown, spec y txt del repositorio y reemplace cualquier en-dash por guion común.
2. **Ejecutar el script** como parte del flujo de trabajo antes de realizar commits críticos que involucren documentación.
3. **Documentar la decisión** en este ADR y referenciarlo en el `CHANGELOG.md` para que futuros contribuyentes conozcan la existencia del script y la política asociada.

## Consecuencias

* Se garantiza la consistencia tipográfica en toda la base de código.
* Se evita que el pre-commit falle por guiones largos.
* El script es sencillo y no tiene dependencias externas; se puede invocar manualmente o integrar en los hooks.

## Próximos pasos

* Añadir la ejecución del script al hook de pre-commit (opcional, ya que el hook actual verifica los guiones como parte de ADR-056).
* Mantener el script actualizado si se añaden nuevos tipos de archivos que requieran la sustitución.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

