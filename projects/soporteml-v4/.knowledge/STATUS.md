# SoporteML v4 - STATUS

**Actualizado:** 2026-08-17

## Estado: 🟡 REINICIO - Fase 0 en curso

## Fase 0 - Fundamentos del reinicio

- [x] Crear `.knowledge/` de V4 (BRIEF, PLAN, STATUS)
- [x] **Decidir la identidad visual de V4** - dirección híbrido oscuro + color por categoría (ADR-001)
- [x] Mockup de identidad validado por Gonzo (`mockups/identidad-v4.html`)
- [x] Iconografía Lucide incorporada al mockup (ADR-030, workspace)
- [x] **Verificar que el backend de v3 funciona** - verificado de punta a punta (`BACKEND-VERIFICADO.md`)
- [x] **Enriquecer el mock** - 13 preguntas (antes 6), 6 productos (antes 3), varias por producto, producto sin preguntas activas
- [x] **Agregar tests del API** - 14 tests que cubren health, auth, sync, multi-tenant, publish, idempotencia, productos, IA, billing
- [x] **Arrancar la UI** (el corazón que le da vida al cuerpo) - layout + bandeja reconstruidos con identidad V4
- [x] **Slice 1 funcional: Plantillas de respuesta** - CRUD completo (repo, API, UI) + tests
- [x] **Plantillas conectadas al flujo de responder** - insertar plantilla en la respuesta desde la bandeja
- [ ] Definir el pipeline A/B para este proyecto

## Slice 1 funcional: Plantillas (2026-08-17)

Primera feature funcional desbloqueada (el schema ya la modelaba):
- ✅ `packages/db/src/repo/templates.ts` - CRUD de plantillas (create, list, getById, update, delete)
- ✅ Endpoints API: GET/POST /templates, PUT/DELETE /templates/:id (con multi-tenant)
- ✅ UI: vista de Plantillas en el sidebar (crear, listar, editar, eliminar)
- ✅ **Plantillas conectadas al flujo de responder**: cada card de la bandeja tiene botón "Plantilla" que inserta el contenido en el input de respuesta
- ✅ 2 tests nuevos (16 total): CRUD completo + 404 multi-tenant
- ✅ Verificado en browser: crear plantilla + insertarla en una respuesta de envío
- Commits `d7ab261` (CRUD) + `3d3be36` (conexión al flujo) en soporteml-v3

## UI V4 arrancada (2026-08-17)

El frontend de v3 se reconstruyó con la identidad V4 (híbrido oscuro + color por categoría):
- ✅ `index.css` - tokens V4 (base oscura premium + acento amarillo MeLi + colores por categoría)
- ✅ `AppSidebar` - logo con glow amarillo, navegación agrupada, item activo con barra lateral iluminada
- ✅ `App.tsx` - stats por categoría, bandeja con barra lateral de color, cards con micro-interacciones, login premium
- ✅ Verificado en browser: 13 preguntas con color por categoría, publicar respuesta funciona (badge cambia a Respondida, stats bajan)
- ✅ Build de producción OK
- Commit `a930cb9` en soporteml-v3

## Backend verificado (2026-08-17)

El backend de v3 (que se conserva) está sano y funciona de punta a punta:
- ✅ Typecheck pasa (api + web)
- ✅ Servidor arranca en `localhost:3001`
- ✅ Endpoints probados: health, dev setup, sync (13 preguntas mock), questions, products, meli/status, ai/suggest
- ✅ **Mocks verificados a fondo** (pregunta de Gonzo): categorización mock 6/6 correcta, multi-tenant aísla empresas, publish marca como respondida, sync idempotente (no duplica)
- ✅ **14 tests del API** (antes 0) - automatizan las verificaciones manuales
- ✅ **Mock enriquecido** - 13 preguntas, 6 productos, varias por producto, producto sin preguntas activas

Detalle completo: `BACKEND-VERIFICADO.md`

## Identidad visual decidida (2026-08-17)

**Dirección:** híbrido oscuro + color por categoría (ADR-001).

- Base oscura premium (`#0a0e1a`) + acento amarillo MeLi (`#ffe600`) con glow
- Color por categoría de consulta (precio=azul, stock=verde, técnico=violeta, envío=naranja, garantía=rosa)
- Iconografía Lucide (ADR-030)
- Micro-interacciones + a11y WCAG 2.1 AA integrada
- Mockup validado: `mockups/identidad-v4.html`

## Contexto del reinicio

**Motivo (decisión de Gonzo, 2026-08-17):** v3 quedó como template básico - features limitadas en la UI (solo 3 vistas genéricas) y UI/UX sosa (cards shadcn estándar, cero diseño avanzado). V4 reconstruye el frontend con diseño impactante y desbloquea las features que el schema ya modela.

**Activo conservado de v3:** backend (OAuth MeLi real, sync, IA, billing mock) + capa de datos (schema 20+ tablas, repositorios) + token real de producción MeLi.

**Metodología:** pipeline en cadena A/B, slices finos con release usable, `.knowledge/` vivo, a11y WCAG 2.1 AA integrada, diseño avanzado con CSS custom. Adaptada de Kanam Story/Forge, no fuente única de verdad.

## Próximo paso

Decidir la identidad visual de V4 con Gonzo (moodboard, dirección de diseño, tokens) antes de tocar código.
