# ADR-014 — SSE + EventEmitter Real-Time Pattern

**Fecha:** 2026-08-05
**Contexto:** Capitulo 14 de "Full Stack Web Development with Remix"
**Fuente:** Andre Landgraf / Remix team

## Decision

Adoptar el patron de Server-Sent Events (SSE) con EventEmitter de Node.js para notificaciones en tiempo real en aplicaciones Remix que corren en long-running servers.

## Detalle

### Arquitectura

```
Action (POST)          EventEmitter          SSE Resource Route        Client (EventSource)
    |                      |                       |                       |
    |-- emitter.emit() -->|                       |                       |
    |                      |-- listener fires ---->|                       |
    |                      |                       |-- send('event') ---->|
    |                      |                       |                       |-- revalidate()
```

### Componentes

1. **events.server.ts** — EventEmitter global + eventStream helper
2. **/sse.tsx** — resource route con requireUserId + event listener
3. **event-source.ts** — hook React con EventSource + useRevalidator
4. **emitter.emit(userId)** en cada action exitosa

### Implementacion

```ts
// events.server.ts
const emitter = global.emitter || new EventEmitter();
global.emitter = emitter;

export function eventStream(request, onSetup) {
  const stream = new ReadableStream({
    start(controller) {
      const send = (event, data) => {
        controller.enqueue(encoder.encode(`event: ${event}\n`));
        controller.enqueue(encoder.encode(`data: ${data}\n\n`));
      };
      const onClose = onSetup(send);
      request.signal.addEventListener('abort', close);
    },
  });
  return new Response(stream, {
    headers: { 'Content-Type': 'text/event-stream' },
  });
}
```

```tsx
// sse.tsx
export async function loader({ request }) {
  const userId = await requireUserId(request);
  return eventStream(request, (send) => {
    const handler = () => send('server-change', `Data change`);
    emitter.addListener(userId, handler);
    return () => emitter.removeListener(userId, handler);
  });
}
```

```tsx
// event-source.ts
export function useEventSource() {
  const { revalidate } = useRevalidator();
  useEffect(() => {
    const es = new EventSource('/sse');
    es.addEventListener('server-change', () => revalidate());
    return () => { es.close(); };
  }, [revalidate]);
}
```

### Cuando usar cada tecnologia

| Tecnologia | Cuando usar |
|---|---|
| Polling | Server sin streaming, prototipos, simplicidad |
| SSE | One-way notifications, mismo server, long-running |
| WebSocket | Bidireccional, baja latencia, juegos, chat |

## Consecuencias

**Positivas:**
- Tiempo real sin librerias externas
- Revalidation automatica de loaders
- Aislado por usuario (cada uno recibe sus eventos)
- Resource route = misma API que el resto de Remix

**Negativas:**
- Solo funciona en long-running servers
- Doble revalidation en el tab que muta
- EventEmitter no escala a multiple instancias (necesitaria Redis Pub/Sub)
- HTTP/1 limite de 6 conexiones concurrentes

## Notas

Para produccion con multiple instancias, reemplazar EventEmitter con Redis Pub/Sub. El resto del patron (SSE endpoint, EventSource hook) se mantiene igual.
