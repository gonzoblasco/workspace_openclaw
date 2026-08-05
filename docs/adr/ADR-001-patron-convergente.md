# ADR-001 — Patron convergente: cuando un patron se repite, verificar si el contexto cambio

**Status:** Aceptado
**Origen:** ai-engineering-bootcamp ADR-001
**Fecha:** 2026-08-05

## Contexto

Cuando un patron se repite muchas veces (ej: crear carpeta nueva por nivel/modulo/feature), la tendencia natural es aplicar el mismo patron por inercia. Esto funciona mientras el contexto se mantiene igual.

El problema aparece cuando el contexto cambia pero el patron se aplica igual.

## Decision

Antes de aplicar un patron repetido N veces, preguntar:

- "Este caso es realmente igual a los que ya resolvi?"
- "Construyo algo nuevo o transformo lo existente?"
- "El patron sigue siendo valido con el contexto actual?"

## Leccion general

**Cuando un patron se repite muchas veces, el riesgo no es equivocarse en el patron — es aplicarlo por inercia cuando el contexto ya cambio.**

La senial de alerta no es "lo se hacer?" sino "es este caso realmente igual a los que ya resolvi?".

## Consecuencias

### Positivas
- Evita crear estructura innecesaria cuando el trabajo es transformar, no construir.
- Fuerza pausa reflexiva antes de actuar por costumbre.
- Documenta el criterio para futuras decisiones similares.

### Negativas
- Agrega friction momentanea al workflow.
- Requiere disciplina para no saltarse la pregunta.

## Notas

Este patron se valido empiricamente en un bootcamp de 10 niveles: los niveles 1-7 eran lineales (cada uno creaba proyecto nuevo), los niveles 8-10 eran convergentes (extendian sistemas existentes). La prediccion del patron convergente se confirmo en los 3 niveles finales.
