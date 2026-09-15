# STATUS - kanam-fixer

**Actualizado:** 2026-09-15
**Ciclo:** 0.0.1
**Slice actual:** S3 construido, **bloqueado en una accion humana** (permisos de macOS)

## Donde estamos

| Slice | Estado | Evidencia |
|---|---|---|
| S1 - Esqueleto y decisiones | **Completado** | Commit `6044856`. Terna en verde, hook activo. |
| S2 - La asercion, solo virtual | **Completado** | Commit `fb931ea`. 7 tests. Criterio de salida verificado. |
| S3 - VoiceOver real en local | **Codigo listo, criterio NO verificado** | Commit `b98bf1b`. Blocker: permisos de macOS (ver abajo). |
| S4 - El caso testigo (#4109) | No iniciado | |
| S5 - Cierre del ciclo | No iniciado | |

**Repo publico:** https://github.com/gonzoblasco/kanam-fixer (`b98bf1b`). Verificado que `.knowledge/` no se filtra.

## S3: el plano del lector real - BLOQUEADO

El codigo esta escrito y pusheado, pero **el criterio de salida NO se cumplio todavia**. No lo doy por hecho: el test se saltea con la causa a la vista, no pasa en falso.

### Que quedo construido

- **`ReaderDriver`**: contrato propio (ADR-0001). `virtualDriver` (CI) y `realDriver` (VoiceOver) lo implementan, asi que **la misma asercion corre en los dos planos**.
- **`expectAnnouncement(container, expected, { driver })`**: el driver es opcional; el default sigue siendo el virtual.
- **`realReaderAvailability()`**: arranca y para el lector una vez, para que el llamador pueda **saltear con la razon real** en vez de reportar un falso verde.
- **9 passed, 4 skipped**: los 4 skips son el plano real, con `REAL_READER_UNAVAILABLE: VoiceOver cannot be started` impreso.

### El blocker (necesita a Gonzo, no a un agente)

`screenReader.detect()` y `.default()` devuelven **true**, pero `start()` falla con `VoiceOver cannot be started`. Faltan dos pasos que solo se hacen a mano en macOS:

1. **VoiceOver Utility -> General -> tildar "Allow VoiceOver to be controlled with AppleScript".** Verificado que el archivo que lo habilita (`/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled`) **no existe** en esta maquina.
2. **System Settings -> Privacy & Security -> Accessibility**: agregar y tildar el proceso que corre los tests (la terminal / el host del agente).

### Lo que NO hice, y por que

`npx @guidepup/setup setup` existe y automatiza esto, **pero escribe directo en la base de permisos de privacidad de macOS** (`/Library/Application Support/com.apple.TCC/TCC.db` via `sqlite3`, mas el archivo de VoiceOver) y su propia lista incluye clientes que no son de este proyecto (`sshd`, `bash`, `zsh`, `osascript`, Terminal, System Events, navegadores). **No ejecute eso sin pedido explicito de Gonzo**: es un cambio de seguridad del sistema, no del proyecto. Ver "Requisitos de S3" en el BRIEF.

### Nota de honestidad

Este slice es el unico de los tres que **no puedo cerrar solo**. S1 y S2 se verificaron con evidencia real; S3 tiene el codigo y el diseno correctos, pero la evidencia del lector real **todavia no existe**. Se cierra cuando los permisos esten otorgados y el log de VoiceOver aparezca en la salida.

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

## Proximo paso

**S3 esta bloqueado, no terminado.** Se cierra cuando Gonzo otorgue los dos permisos de macOS y el log de VoiceOver aparezca en la salida del test. Pasa a S4 (el caso testigo #4109, que corre en el plano virtual y **no** depende de esos permisos) solo si se decide dejarlo bloqueado por ahora.

S4 puede hacerse ya: reproduce el bug de anuncio por timing en el plano virtual, que es el que funciona hoy.

## Pendientes de decision (de Gonzo)

1. ~~Crear el repo y hacerlo publico~~ **HECHO:** `gonzoblasco/kanam-fixer`, publico.
2. ~~Archivar `a11y-fixer`~~ **HECHO:** `isArchived=true` (2026-09-15 12:46 UTC).
3. **Paquete npm `@gonzoblasco/a11y-fixer@0.6.0`:** dejarlo, deprecarlo o despublicar. **Sin decision.** `kanam-fixer` sigue libre en npm.
4. **`a11y-playground`:** migra, se archiva o se sostiene sola. **Sin decision.**

Seguimiento en la DB de memoria: todo id=54.
