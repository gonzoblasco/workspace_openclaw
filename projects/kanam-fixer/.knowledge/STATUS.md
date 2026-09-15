# STATUS - kanam-fixer

**Actualizado:** 2026-09-15
**Ciclo:** 0.0.1
**Slice actual:** S2 completado, S3 por arrancar

## Donde estamos

| Slice | Estado | Evidencia |
|---|---|---|
| S1 - Esqueleto y decisiones | **Completado** | Commit `6044856`. Terna en verde, hook activo. |
| S2 - La asercion, solo virtual | **Completado** | Commit `fb931ea`. 7 tests. Criterio de salida verificado. |
| S3 - VoiceOver real en local | No iniciado | |
| S4 - El caso testigo (#4109) | No iniciado | |
| S5 - Cierre del ciclo | No iniciado | |

**Repo publico:** https://github.com/gonzoblasco/kanam-fixer (`fb931ea`). Verificado que `.knowledge/` no se filtra.

## S1: esqueleto y decisiones

- **Stack:** TypeScript (`nodenext` ESM), Biome 2.5, Vitest 5, build con `tsc`, pre-commit hook (`simple-git-hooks`).
- **Dependencia:** `@guidepup/virtual-screen-reader` (driver virtual). `jsdom` para el DOM en tests.
- **ADR-0001:** capa propia fina sobre Guidepup; su API nunca es el contrato publico. Incluye que pasa si Guidepup desaparece.
- **ADR-0002:** la matriz de lectores (lector x version x SO) se declara desde el dia uno.
- **README:** abre por el problema, no por la feature.

## S2: la asercion sobre el anuncio (driver virtual)

- **`expectAnnouncement(container, expected)`** - recorre el contenedor con el lector y compara la secuencia de frases habladas, en orden.
- **`readAnnouncements(container)`** - la observacion cruda, para que un fallo pueda mostrar que se anuncio de verdad.
- **La matriz viaja con el resultado** (ADR-0002), y su version se lee del paquete instalado en vez de escribirse a mano: no puede quedar desactualizada.
- **7 tests**, incluidos 3 de mutacion (nombre de grupo, estado pressed, heading) mas uno que verifica que TODAS las mutaciones fallan.

### Criterio de salida de S2: verificado

El criterio era "el test falla al mutar el componente". Se cumplio, y ademas se endurecio: los tests de mutacion **no** matchean contra las frases esperadas (que el mensaje de error repite siempre, asi que pasarian por cualquier mismatch), sino contra **lo que el lector efectivamente anuncia** en la variante rota. Ejemplos observados:

| Variante | Correcto anuncia | Roto anuncia |
|---|---|---|
| Sin `aria-label` en el grupo | `group, Channels` | `group` (sin nombre) |
| Sin `aria-pressed` | `button, Email, pressed` | `button, Email` |
| Heading reemplazado por contenedor con label | `heading, Notification settings, level 1` | `Notification settings` (sin nivel) |

**Dato que vale registrar:** la segunda fila es exactamente la clase de bug del PR #9879 en ibm-products (`aria-pressed` hace que VoiceOver anuncie un toggle). El driver virtual lo detecta igual que el lector real.

## El hook hizo su trabajo en los dos slices

- **S1:** bloqueo el primer commit. Biome encontro 2 errores en `dist/` (la config no excluia el directorio de build). Se corrigio con `files.includes`, mas el patron de ignore (`!**/dist` en lugar de `!**/dist/**`, que Biome 2.2+ marca como deprecado).
- **S2:** la terna encontro dos errores reales antes del commit. `tsc` fallaba por tipos faltantes (`Node` del DOM, `node:module`) y Biome por un import sin usar. Se corrigio `tsconfig.json` (`lib: ["ES2024", "DOM"]`, `types: ["node"]`) y se limpio el import.

El hook no es decorativo: en los dos casos freno un commit que no compilaba sin la correccion.

## Proximo paso (S3)

El mismo assert con VoiceOver real en local. Criterio de salida: la misma asercion pasa con el lector real, y el reporte muestra la frase que salio de verdad.

## Pendientes de decision (de Gonzo)

1. ~~Crear el repo y hacerlo publico~~ **HECHO:** `gonzoblasco/kanam-fixer`, publico.
2. ~~Archivar `a11y-fixer`~~ **HECHO:** `isArchived=true` (2026-09-15 12:46 UTC).
3. **Paquete npm `@gonzoblasco/a11y-fixer@0.6.0`:** dejarlo, deprecarlo o despublicar. **Sin decision.** `kanam-fixer` sigue libre en npm.
4. **`a11y-playground`:** migra, se archiva o se sostiene sola. **Sin decision.**

Seguimiento en la DB de memoria: todo id=54.
