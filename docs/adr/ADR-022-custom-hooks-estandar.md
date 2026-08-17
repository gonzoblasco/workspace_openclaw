# ADR-022 - Custom Hooks como Estándar para Compartir Lógica (Reemplazo de HOCs y Render Props)

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 4 (HOCs, FunctionAsChild, Container/Presentational)
**Scope:** Global - aplica a cualquier proyecto React

## Context

El libro presenta tres patrones para compartir lógica entre componentes:

1. **Container/Presentational** - separar lógica en un componente contenedor y UI en otro
2. **Higher-Order Components (HOCs)** - funciones que reciben un componente y retornan uno mejorado
3. **FunctionAsChild / Render Props** - el children es una función que recibe parámetros del padre

Estos patrones fueron creados en la era de class components (pre-React 16.8) para resolver problemas que hoy se resuelven con hooks.

## Decision

Usar **custom hooks** como estándar para compartir lógica entre componentes. HOCs y Render Props se consideran legacy y solo se usan cuando:

- Se mantiene código existente que ya los usa
- Se necesita un cross-cutting concern que hooks no pueden resolver limpiamente (muy raro)

### Ejemplo de migración

**HOC (libro):**
```tsx
const withInnerWidth = Component => props => {
  const [innerWidth, setInnerWidth] = useState(window.innerWidth)
  useEffect(() => {
    const handleResize = () => setInnerWidth(window.innerWidth)
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  return <Component {...props} innerWidth={innerWidth} />
}
```

**Custom hook (2026):**
```tsx
const useInnerWidth = () => {
  const [innerWidth, setInnerWidth] = useState(window.innerWidth)
  useEffect(() => {
    const handleResize = () => setInnerWidth(window.innerWidth)
    window.addEventListener('resize', handleResize)
    return () => window.removeEventListener('resize', handleResize)
  }, [])
  return innerWidth
}

// Uso en cualquier componente:
const MyComponent = () => {
  const innerWidth = useInnerWidth()
  // ...
}
```

**Container/Presentational (libro):**
```tsx
const GeolocationContainer = () => {
  const [latitude, setLatitude] = useState<number | null>(null)
  // ... lógica de geolocalización
  return <Geolocation latitude={latitude} longitude={longitude} />
}
```

**Custom hook (2026):**
```tsx
const useGeolocation = () => {
  const [coords, setCoords] = useState<GeolocationCoords | null>(null)
  useEffect(() => {
    if (!navigator.geolocation) return
    navigator.geolocation.getCurrentPosition(
      ({ coords }) => setCoords(coords),
      (error) => console.error(error)
    )
  }, [])
  return coords
}

// Uso:
const MyComponent = () => {
  const coords = useGeolocation()
  return <Geolocation latitude={coords?.latitude} longitude={coords?.longitude} />
}
```

## Rationale

1. **Composición natural:** los hooks se componen dentro del componente, no requieren wrapper components ni prop drilling.
2. **TypeScript-friendly:** los tipos fluyen naturalmente sin necesidad de inferencia compleja de HOCs.
3. **Sin wrapper hell:** los HOCs anidados crean árboles de wrappers en React DevTools. Los hooks no.
4. **Testing más simple:** el hook se testea como función, no necesita renderizar un componente.
5. **Tree-shaking:** los hooks no utilizados no afectan el bundle. Los HOCs importados sí.
6. **React 19:** los hooks son el mecanismo principal de React 19. use() y otros hooks nuevos refuerzan este paradigma.

## Consequence

- Código más legible y mantenible
- Menos componentes wrapper en el árbol
- Testing más directo
- Migración de código legacy requiere refactor de HOCs a hooks
- HOCs y Render Props se consideran deuda técnica en proyectos nuevos

## Referencias

- React docs - Reusing Logic with Custom Hooks: https://react.dev/learn/reusing-logic-with-custom-hooks
- React 19 - use() hook: https://react.dev/reference/react/use
- React 19 - useOptimistic, useFormStatus: https://react.dev/blog/2024/12/05/react-19
