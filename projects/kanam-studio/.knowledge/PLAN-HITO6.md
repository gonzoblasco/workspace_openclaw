# Hito 6 - E2E integral del flujo completo (plan)

**T=16 (high)** | Pipeline: Kanam diseña → A escribe → B revisa → verificación

## Contexto (visión corregida 2026-09-01)

Kanam Studio es un taller de mundos: definir → explorar → decidir → escribir. Este hito valida la visión **de punta a punta** con un E2E integral que recorre el flujo completo del autor.

## Objetivo

Un E2E (o suite de E2E) que recorra la visión completa:

1. **Crear historia** (home → título → editor con start automático)
2. **Definir el mundo** (panel Mundo → crear personaje manualmente)
3. **Explorar** (modo jugar + panel Simular con cobertura)
4. **Verificar** (panel Canon con issues)
5. **Decidir** (panel Exportar → relato lineal + camino canónico)
6. **Escribir** (panel Exportar → prosa final)
7. **Exportar** (JSON versionable)

## Consideración clave: IA en E2E

Los endpoints de IA (`/api/chat`, `/api/world`, `/api/character`, `/api/canonical`, `/api/prose`) requieren Ollama. Un E2E determinista NO puede depender de la IA (lentitud, no determinismo). Estrategia:

- **Flujo local (determinista):** crear historia, personaje manual, simular, canon, relato lineal, exportar JSON - todo sin IA.
- **Paneles de IA (smoke):** abrir cada panel (IA, Mundo chat, Personaje, Camino canónico, Prosa) y verificar que la UI existe (selector, botones, input) - sin enviar mensajes.
- **Opcional (skip si no hay Ollama):** un test marcado que hace UNA llamada real a `/api/prose` y verifica que responde (smoke de integración).

## Arquitectura

```
tests/e2e/vision.spec.ts   - E2E integral del flujo completo
```

### Test 1: flujo completo local (determinista)

```
1. Home: crear "La casa rural" → editor con start automático
2. Agregar 2 pasajes + 1 final, conectar start → pasaje1 → final (drag)
3. Panel Mundo: crear personaje "El Padre" (form manual)
4. Panel Simular: ver cobertura (rutas, endings)
5. Panel Canon: ver issues (o sin problemas si está completo)
6. Panel Exportar: ver relato lineal (sucesos numerados)
7. Exportar JSON: descargar y verificar contenido
8. Volver a home → Admin: ver la historia con stats
```

### Test 2: paneles de IA (smoke, sin llamadas)

```
1. Abrir cada panel: IA, Personaje, Outline, Camino canónico, Prosa
2. Verificar que la UI existe (selector, botones, inputs)
3. NO enviar mensajes (determinismo)
```

### Test 3: smoke de integración con IA (opcional, skip si no hay Ollama)

```
1. POST /api/prose con un payload mínimo válido
2. Verificar que responde (200 o SSE con deltas)
3. Skip si Ollama no está (test.skip condicional)
```

## Criterios de done

- [ ] Test 1: flujo completo local verde (determinista, sin IA).
- [ ] Test 2: paneles de IA abren con su UI (smoke).
- [ ] Test 3: smoke de integración con IA (skip si no hay Ollama).
- [ ] Suite completa verde (13 existentes + nuevos).
- [ ] Lint, typecheck, build OK.
