# ADR-017: Hooks Sobre Hocs

**Status:** Aceptado
**Fecha:** 2026-08-05
**Origen:** testing-react-library

## Contexto

Los Higher-Order Components (HOCs) y Render Props fueron patrones populares en React pre-hooks para compartir logica con estado. Desde React 16.8 (2019), los Hooks son el mecanismo recomendado por el equipo de React.

Los HOCs tienen desventajas conocidas: prop drilling inverso, wrapper hell, dificultad de tipado en TypeScript, y naming collisions.

## Decision

Usar **Hooks** como mecanismo principal para compartir logica con estado en proyectos React. No implementar HOCs ni Render Props a menos que un caso de uso especifico lo requiera (documentando la excepcion).

## Alternativas consideradas

- **HOCs:** Patron valido pero obsoleto para la mayoria de los casos.
- **Render Props:** Similar, reemplazable por hooks + children como funcion.
- **Headless components:** Alternativa valida para componentes complejos (Radix, Ariakit).

## Consecuencias

- Positivas: Codigo mas legible, tipado mas simple, sin wrapper hell.
- Positivas: Los hooks se pueden componer y combinar libremente.
- Negativas: Los hooks tienen reglas estrictas (no en condicionales, no en loops).

