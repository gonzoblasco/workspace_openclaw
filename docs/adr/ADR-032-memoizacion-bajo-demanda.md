# ADR-032: Memoizacion Bajo Demanda

**Status:** Accepted
**Fecha:** 2026-08-05
**Origen:** react-18-design-patterns
**Source:** React 18 Design Patterns - Chapter 8 (memo, useMemo, useCallback section)
**Scope:** Global - aplica a cualquier proyecto React

## Context

React provee tres herramientas de memoizacion: `memo` (componentes), `useMemo` (valores), y `useCallback` (funciones). Es tentador usarlas por default "por si acaso", pero esto tiene costos:

- `memo` hace shallow comparison de props en cada render
- `useMemo`/`useCallback` almacenan valores en memoria y comparan dependencias
- El costo de la comparacion + memoria puede superar el beneficio en componentes chicos

## Decision

No usar `memo`, `useMemo`, o `useCallback` a menos que se cumpla AL MENOS UNA de estas condiciones:

### Cuando usar `memo`

- El componente renderiza **listas grandes** (>100 items)
- El componente tiene **animaciones o layout pesado**
- Se detecta **rendundancia en renders** via React DevTools Profiler
- El componente es **profundo en el arbol** y recibe las mismas props frecuentemente

### Cuando usar `useMemo`

- **Procesamiento pesado** (filter, sort, map sobre arrays grandes, calculos matematicos)
- **Valores derivados** que se usan en dependencias de useEffect o como props a hijos memoizados
- **Referencias estables** para objetos que se pasan como props (evitar que cambien en cada render)

### Cuando usar `useCallback`

- La funcion se pasa como **prop a un componente envuelto en `memo`**
- La funcion se usa como **dependencia de `useEffect`**
- La funcion se pasa a un **context provider** (evitar re-renders innecesarios de consumidores)

### Cuando NO usar

- Componentes chicos con renders simples
- Valores calculados triviales (ej: `fullName = firstName + ' ' + lastName`)
- Funciones que no se pasan como props ni como dependencias de efectos
- "Por las dudas" - medir primero, optimizar despues

## Rationale

1. **Costo de comparacion:** `memo` hace shallow comparison de todas las props en cada render. Si el componente es chico, el costo de comparar puede ser mayor que el de simplemente re-renderizar.
2. **Costo de memoria:** `useMemo`/`useCallback` mantienen referencias en memoria. En componentes que se montan/desmontan frecuentemente, esto puede acumularse.
3. **Complejidad:** agregar memoizacion prematuramente introduce deuda cognitiva. El codigo es mas dificil de leer y razonar.
4. **React 19:** el compilador de React (React Forget) automatizara la memoizacion en el futuro. Invertir en memoizacion manual hoy puede ser trabajo descartable.

## Consequences

- Menos codigo de memoizacion en la base de codigo
- Rendimiento similar o mejor (sin overhead innecesario)
- Perfilamiento con React DevTools Profiler como paso previo a optimizar
- Cultura de "medir antes de optimizar"

## Referencias

- React docs - memo: https://react.dev/reference/react/memo
- React docs - useMemo: https://react.dev/reference/react/useMemo
- React docs - useCallback: https://react.dev/reference/react/useCallback
- React Compiler (React Forget): https://react.dev/learn/react-compiler
- Kent C. Dodds - When to useMemo and useCallback: https://kentcdodds.com/blog/usememo-and-usecallback
