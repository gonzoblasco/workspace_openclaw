# SoporteML V4 - Verificación del Backend (Fase 0)

**Fecha:** 2026-08-17
**Estado:** ✅ Backend de v3 verificado y funcionando de punta a punta

## Resumen

Antes de reconstruir el frontend con la identidad nueva, se verificó que el backend de v3 (que se conserva) está sano y funciona correctamente. El backend es el activo valioso: OAuth MeLi real, sync, IA, billing mock, schema 20+ tablas.

## Verificaciones realizadas

### Compilación y tipos
- ✅ `pnpm check-types` en `apps/api` - sin errores
- ✅ `pnpm check-types` en `apps/web` - sin errores
- ✅ Dependencias instaladas (turbo, tsx, vitest, hono, zod, @soporteml/db)

### Servidor arranca
- ✅ `pnpm dev` en `apps/api` - servidor escucha en `http://localhost:3001`

### Endpoints probados (curl)
| Endpoint | Método | Resultado |
|----------|--------|-----------|
| `/health` | GET | ✅ `{"status":"healthy"}` |
| `/auth/dev/setup` | POST | ✅ Crea usuario + empresa + membership admin |
| `/meli/sync` | POST | ✅ 6 preguntas mock creadas (modo mock) |
| `/questions` | GET | ✅ Devuelve preguntas con categorización IA + sugerencia |
| `/products` | GET | ✅ Devuelve productos del sync mock |
| `/meli/status` | GET | ✅ `{"connected":false}` (esperado en modo mock) |
| `/ai/suggest` | POST | ✅ Genera respuesta con contexto del producto (categoría Stock, confianza 0.9) |

### Verificación profunda de los mocks (2026-08-17)

> Pregunta de Gonzo: "si todo es mock, ¿cómo confirmamos que funciona? ¿no habría que confirmar que los mocks están bien implementados?"

Se verificó que los mocks NO son solo "responder algo" - están bien implementados:

**1. Categorización mock (AI service) - 6/6 correctas**
- P1 garantía → Garantía ✅
- P2 envío a Córdoba → Envío ✅
- P3 accesorios incluidos → Técnico ✅
- P4 cuotas sin interés → Precio ✅
- P5 stock disponible → Stock ✅
- P6 unidades vendidas → Stock ✅
- La lógica `mockCategorizar` mapea correctamente las 6 preguntas reales del sync a sus categorías esperadas.

**2. Multi-tenant (aislamiento) - correcto**
- Empresa A (con sync): 6 preguntas ✅
- Empresa B (sin sync): 0 preguntas ✅ (no ve las de A)
- El aislamiento por `company_id` funciona.

**3. Publish mock - correcto**
- Publicar respuesta → pregunta marcada `published` con `final_answer` guardada ✅

**4. Idempotencia del sync - correcta**
- 2do sync: 0 creadas, 6 actualizadas (no duplica) ✅
- Siguen siendo 6 preguntas (no 12) ✅
- La pregunta publicada no se duplicó ✅

### Hallazgo: el API no tiene tests
- `pnpm test` en `apps/api` → "No test files found"
- El backend de v3 **no tiene cobertura de tests**. Esto es un riesgo: el frontend V4 se va a construir sobre este backend, y sin tests no hay red de seguridad.
- **Acción para V4:** agregar tests del API (al menos los endpoints core: health, dev setup, sync, questions, products, ai/suggest) como parte del pipeline.
- **Nota:** la verificación manual de arriba (categorización, multi-tenant, publish, idempotencia) es exactamente lo que esos tests deberían automatizar.

## Cómo correr

```bash
# Terminal 1 - backend (puerto 3001)
cd apps/api && pnpm dev

# Terminal 2 - frontend (puerto 5173)
cd apps/web && pnpm dev
```

## Notas

- El `.env` de `apps/api` existe con las credenciales de MeLi (no committeado, en .gitignore).
- `MELI_MOCK=1` está activo: el sync genera data de ejemplo, no toca la cuenta real.
- El token real de producción MeLi sigue en la DB mientras no expire (GONZOBLASCO / MLA).
- El frontend de v3 se va a **reconstruir** con la identidad V4 (híbrido oscuro + color). El backend se conserva tal cual.
