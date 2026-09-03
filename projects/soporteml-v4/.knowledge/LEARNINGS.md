# SoporteML V4 - LEARNINGS

> Aprendizajes de la sesión de reinicio de SoporteML V4 (2026-08-17).

## 1. "Que responda" no confirma que funcione (2026-08-17)

**Contexto:** al verificar el backend de v3, confirmé que los endpoints respondían (health, sync, questions, products, ai/suggest). Gonzo preguntó: "si todo es mock, ¿cómo confirmamos que funciona? ¿no habría que confirmar que los mocks están bien implementados?"

**Lección:** un mock mal implementado da 200 con data inventada y esconde bugs reales. Que el endpoint responda valida el esqueleto (rutas, auth, DB, serialización), pero NO valida la lógica. Hay que verificar los mocks a fondo:
- ¿La categorización mock mapea correctamente las preguntas a sus categorías?
- ¿El multi-tenant realmente aísla las empresas?
- ¿El publish realmente marca la pregunta como respondida?
- ¿El sync es idempotente (no duplica)?

**Qué haría distinto:** en la primera verificación, probar los mocks a fondo desde el inicio, no solo los endpoints. La verificación profunda (categorización 6/6, multi-tenant, publish, idempotencia) es exactamente lo que los tests deberían automatizar.

## 2. Refactor para testear: factory con DB inyectable (2026-08-17)

**Contexto:** el API de v3 no tenía tests. Para testear con `app.request()` de Hono sin levantar servidor, extraje la creación del app a `createApp(db)` en `app.ts`, y `index.ts` solo hace `serve()`.

**Lección:** separar la creación del app (factory) del boot del servidor permite testear con `app.request()` usando una DB in-memory. Es un refactor limpio que no cambia comportamiento y habilita el testeo.

**Patrón:**
```ts
// app.ts - factory con DB inyectable
export function createApp(config: { db: Db; forceMock?: boolean }): Hono {
  // ... rutas
}

// index.ts - solo boot
const db = openDb({ filename: DB_PATH });
const app = createApp({ db, forceMock: FORCE_MOCK });
serve({ fetch: app.fetch, port });
```

## 3. El mock determinístico en /ai/suggest (2026-08-17)

**Contexto:** el endpoint `/ai/suggest` usaba la IA real de Ollama, que tardaba ~1.5s por llamada (2 llamadas: categorizar + sugerir) y dependía de que Ollama esté corriendo. En modo mock, esto causaba timeout en los tests.

**Lección:** en modo mock, el endpoint debe usar el mock determinístico (consistente con el sync), no la IA real. Esto evita timeout y dependencia de Ollama en dev. El patrón: `forceMock ? ai.sugerirMock(...) : await ai.sugerirRespuesta(...)`.

## 4. El ecosistema de MDs es un sistema vivo (2026-08-17)

**Contexto:** Gonzo definió la filosofía del proyecto: "el ecosistema de MDs será un sistema vivo que irá creciendo paso a paso. No fijaremos exactamente el contenido de cada fase con anticipación."

**Lección:** no congelar el plan completo con anticipación. Definir los requisitos y recursos de la fase actual, ejecutarla, y recién entonces definir la siguiente. El PLAN.md de V4 refleja esto: la Fase 0 tiene requisitos concretos, las fases futuras son "tentativas, se definen al alcanzarlas".
