---
title: ADR-072 - Front-matter enforcement for SKILL.md files
status: proposed
deciders:
  - Gonzo
date: 2026-09-25
---

## Contexto

El pre-commit del workspace falla cuando los archivos `SKILL.md` no contienen un bloque de front-matter válido (campo `---`). Durante la sesión de archivado se detectaron 12 archivos sin front-matter, lo que impidió que el commit pasara sin usar `--no-verify`.

## Decisión

1. Implementar el script `scripts/frontmatter_validator.sh` que recorra todos los `SKILL.md` y añada automáticamente un bloque mínimo de front-matter cuando falte.
2. Documentar esta práctica como ADR-072 y añadirla al índice de ADRs.
3. (Opcional) Integrar la ejecución del script en el hook de pre-commit para que la corrección sea automática antes de cualquier commit.

## Consecuencias

* Todos los `SKILL.md` tendrán ahora un bloque `---` que satisface el chequeo del pre-commit.
* Reduce fricción al contribuir al workspace, evitando la necesidad de `--no-verify`.
* Mantiene la coherencia de los metadatos de los skills (título y descripción).

## Próximos pasos

* Añadir la llamada a `./scripts/frontmatter_validator.sh` al archivo `.pre-commit` (si existe) o al script de lint interno.
* Revisar que el script sea idempotente: ejecutar varias veces no genera bloques duplicados.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

