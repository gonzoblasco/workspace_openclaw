# SoporteML V4 - HANDOFF

> **Sesión:** 2026-08-17 (reinicio de SoporteML como V4)
> **Estado:** Fase 0 completa + UI V4 arrancada

---

## Qué se hizo

### Fase 0 - Fundamentos del reinicio (completa)
- **Decisión de Gonzo:** v3 quedó como template básico (features limitadas en la UI, UI/UX sosa). V4 = reinicio con estándar superior.
- **Conservar** backend + capa de datos de v3 (activo valioso: OAuth MeLi real, schema 20+ tablas, token de producción).
- **Reconstruir** frontend con diseño avanzado + desbloquear features que el schema ya modela.
- **Identidad visual (ADR-001):** híbrido oscuro + color por categoría. Base oscura premium + acento amarillo MeLi + color por categoría (precio=azul, stock=verde, técnico=violeta, envío=naranja, garantía=rosa).
- **Lucide (ADR-030, workspace):** librería de iconos base en todos los proyectos.

### Backend verificado + mock enriquecido + tests
- **Backend verificado a fondo** (pregunta de Gonzo: "si todo es mock, ¿cómo confirmamos que funciona?"): categorización mock 6/6, multi-tenant aísla empresas, publish marca como respondida, sync idempotente.
- **Mock enriquecido:** 13 preguntas (antes 6), 6 productos (antes 3), varias por producto, producto sin preguntas activas (Parlante agotado).
- **Refactor para testear:** `createApp(db)` en `app.ts` (factory con DB inyectable), `index.ts` solo hace `serve()`.
- **14 tests del API** (antes 0): health, auth, sync, multi-tenant, publish, idempotencia, productos, IA, billing. Todos pasan en 378ms.
- **Fix /ai/suggest:** en modo mock usa `sugerirMock` determinístico (consistente con el sync), no la IA real.

### UI V4 arrancada (el corazón)
- **`index.css`:** tokens V4 (base oscura premium + acento amarillo MeLi + colores por categoría).
- **`AppSidebar`:** logo con glow amarillo, navegación agrupada, item activo con barra lateral iluminada.
- **`App.tsx`:** stats por categoría, bandeja con barra lateral de color, cards con micro-interacciones, login premium.
- **Verificado en browser:** 13 preguntas con color por categoría, publicar respuesta funciona (badge cambia a Respondida, stats bajan).
- **Build de producción OK.**

## Cómo correr

```bash
# Terminal 1 - backend (puerto 3001)
cd apps/api && pnpm dev

# Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

Abrir http://localhost:5173 → "Entrar (modo demo)" → Sincronizar → ver 13 preguntas con color por categoría → Responder.

## Dónde está cada cosa

- **Código:** repo `gonzoblasco/soporteml-v3` (V4 se construye sobre v3, no es repo nuevo). Últimos commits: `d0b3f7f` (mock + tests + refactor), `a930cb9` (UI V4).
- **Memoria institucional:** `projects/soporteml-v4/.knowledge/` (BRIEF, PLAN, STATUS, ADR-001, BACKEND-VERIFICADO, LEARNINGS).
- **Mockup de identidad:** `projects/soporteml-v4/mockups/identidad-v4.html`.
- **ADRs:** `docs/adr/ADR-030-lucide-iconos-base.md` (workspace), `projects/soporteml-v4/.knowledge/ADR-001-identidad-visual.md`.

## Pendientes (próxima sesión)

- [ ] **Validación visual de Gonzo** - que vea la app corriendo y ajuste colores/espaciado/tipografía.
- [ ] **Definir el pipeline A/B** - la metodología de Kanam Story (agente A desarrolla unidades impares, B pares, cross-review a11y).
- [ ] **Desbloquear features** que el schema ya modela: KB (RAG), autopilot, SLA, plantillas, clientes, métricas.
- [ ] **Validar integraciones restantes:** Mercado Pago (nunca probado), email (Resend).

## Notas de decisión

- "adelante" a secas = seguir con mi recomendación según el contexto (regla acordada).
- El ecosistema de MDs es un sistema vivo: no fijar todas las fases con anticipación, definir la fase actual y evolucionar.
- V4 se construye sobre el repo de v3 (no es repo nuevo) - el backend es el activo valioso.
