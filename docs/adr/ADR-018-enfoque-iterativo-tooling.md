# ADR-018 - Enfoque Iterativo para Adopción de Tooling

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 1 (JavaScript fatigue section)
**Scope:** Global - aplica a cualquier proyecto que adopte tooling del ecosistema JS

## Context

Es común en el ecosistema JavaScript sentirse abrumado por la cantidad de herramientas disponibles: bundlers, transpiladores, linters, test runners, frameworks de estado, routers, etc. Esto se conoce como "JavaScript fatigue".

El error más frecuente es querer resolver todo el stack de tooling antes de escribir una línea de código de la aplicación.

## Decision

Adoptar un **enfoque iterativo** para incorporar tooling:

1. **Arrancar con lo mínimo** que permita escribir y ver la aplicación funcionando.
2. **Agregar tooling solo cuando el problema lo justifique** - no por moda, no por "vamos a necesitarlo después".
3. **Cada herramienta debe resolver un problema real y actual** del proyecto, no uno hipotético.

## Consequence

- Menos configuración inicial, más tiempo en código de producto
- Menos dependencias no utilizadas
- Curva de aprendizaje más gradual para nuevos miembros del equipo
- Riesgo bajo: si una herramienta se necesita después, se agrega cuando el problema existe

## Examples

- No instalar React Router hasta tener dos pantallas que navegar
- No configurar estado global (Zustand, Redux) hasta que dos componentes hermanos necesiten compartir estado
- No agregar testing hasta tener al menos un módulo que justifique un test
- No configurar CI/CD hasta tener un build que validar

## Referencias

- React 18 Design Patterns and Best Practices (4th Ed.) - Chapter 1, "Understanding JavaScript fatigue"
- You Aren't Gonna Need It (YAGNI) - principio de software engineering
