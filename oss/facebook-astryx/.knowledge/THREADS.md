# THREADS - facebook/astryx

> Hilos abiertos con upstream: que se dijo, que quedo pendiente y **quien tiene la pelota**.
> Se actualiza en cada cierre. A diferencia de `HANDOFF.md` (estado del trabajo), esto es el
> estado de la **conversacion**: quien debe responder y cuando conviene volver a mirar.

**Repo:** https://github.com/facebook/astryx
**Ultima actualizacion:** 2026-11-03
**Verificado con:** `scripts/pr-thread-brief.sh facebook/astryx <n> gonzoblasco`

---

## Como leer esta tabla

- **PELOTA** - `NOS` (tenemos que hacer algo), `ELLOS` (esperamos respuesta), `NADIE` (dormido).
- Una fila se cierra cuando el hilo se resuelve o cuando decidimos abandonarlo. No se borra: se marca.
- **No inferir la pelota de memoria.** Correr `pr-thread-brief.sh` antes de afirmar quien debe
  responder: el 2026-11-03 el primer borrador de este archivo tenia dos filas mal por escribir de
  memoria en vez de leer el hilo.
- Regla dura de `docs/AGENTS-DETALLE.md` (§8): autoria por `user.login` verificado. **Nuestro =
  `gonzoblasco`.** Todo otro login es tercero, incluidos maintainers que revisan nuestro trabajo.

---

## Hilos abiertos

| # | Tipo | Titulo | Ultimo acto | PELOTA | Desde | Notas |
|---|---|---|---|---|---|---|
| **4690** | PR | Table drop tree ARIA / treegrid | `humbertovirtudes`: `changes_requested` | **ELLOS** | 2026-10-22 | Ver detalle. Es el hilo mas activo. |
| **3335** | Issue | TabMenu sin lugar valido en `role=tablist` | **Nuestro** comentario `6499306768` | **ELLOS** | 2026-10-29 | Esperando a `duytbp` o `cixzhang`. No volver a comentar para empujar. |

---

## #4690 - Table drop tree ARIA (treegrid)

**Estado: PR abierto, NO dormido.** Cuatro pedidos de cambios de terceros, el ultimo el 2026-10-22.

**Linea de tiempo relevante:**

| Fecha | Actor | Acto |
|---|---|---|
| 2026-08-13 | cixzhang | `changes_requested` - "si incluimos tree data la tabla..." |
| 2026-08-23 | cixzhang | referencia `useTreeFocus`, deja row-focus-vs-cell-nav para maintainer |
| 2026-08-24 | **nosotros** | marco AT para la decision row-focus-vs-cell-nav |
| 2026-08-27 | cixzhang | ruling: row focus para v1 |
| 2026-08-27 | **nosotros** | comentario sobre el scope de v1 |
| 2026-08-30 | rubyycheung | `changes_requested` |
| 2026-09-22 | humbertovirtudes | `changes_requested` |
| 2026-10-20 | astracat-bot | comentarios inline sobre wording (APG) |
| 2026-10-22 | kentonquatman | `changes_requested` |
| **2026-10-22** | **humbertovirtudes** | **`changes_requested`** - ultimo acto |

**Nuestro aporte:** marco AT para la decision `row-focus-vs-cell-nav`, que cixzhang cito para el
ruling del 27/08. Quedo incorporado a v1. **No hay nada nuestro pendiente.**

**Riesgo de leer mal este hilo:** el primer borrador de este archivo lo marco `NADIE` (dormido). Falso:
hubo cinco reviews de terceros entre agosto y octubre. Si alguna vez se retoma, el trabajo es de
`AKnassa` (autor), no nuestro.

**Cuando volver a mirar:** solo si vuelve a aparecer en el radar de Gonzo. **No intervenir sin que nos
lo pidan:** ya dimos lo nuestro y el PR es de otro autor.

---

## #3335 - TabMenu dentro de `role=tablist`

**Estado:** comentario publicado el 2026-10-29. **Esperando respuesta** de `duytbp` (autor del
follow-up del 28/10) o de `cixzhang` (maintainer que lleva el tema desde julio).

**Que se afirmo** (verificado en codigo, no opinion):

1. `TabListContext` vive en el wrapper (`TabList.tsx:669`): un slot hermano del strip conserva
   `value`, `size` y `onChange` (`TabMenu.tsx:276/345/349/352`).
2. `TabMenu` tira error fuera de `TabList`.
3. `useScrollOverflow` mide solo el elemento scrolleable (`hooks/useScrollOverflow.ts`), asi que el
   menu fuera del strip no participa de `overflowStart` / `overflowEnd`.
4. El warning de `TabList.tsx:628` mira `strip.children` del DOM y se resuelve sacando el menu.

**Verificacion alcanzada:** 5 probes propias verdes (Q1 warning inside, Q1b slot inexistente, Q2
contexto, Q2b boundary, Q3 medicion) + los 81 tests originales del repo.

**Decision abierta con ellos:** overlay vs celda, segun `overflow`.

**Deuda declarada:** el nivel "browser real" (Playwright) **no se corrio** para `overflow=visible`.
Si el hilo avanza hacia un RFC, correrlo antes de opinar.

**Antecedentes del mismo issue:** nuestro comentario del 2026-08-22 (el interim `#3434` fue la
decision correcta; recomendaba Option 2 gateado por `href`). El tema esta trackeado en el programa de
accesibilidad como `#4475`.

**Cuando volver a mirar:** si aparece un RFC de TabMenu, o si responden. Recrear el clone
(`clones/astryx` ya no existe), baseline `0.7.4` (main estaba roto: `core@0.7.5` sin publicar).

**Que NO hacer:** no volver a comentar para "empujar". Sin respuesta nueva ni trabajo nuevo, un
segundo comentario es ruido (regla 4 de `AGENTS-DETALLE.md`).

---

## Hilos cerrados (para no repetir)

| # | Desenlace | Fecha | Leccion |
|---|---|---|---|
| **5204** | Cerrado por `cixzhang` como **SUPERSEDED CON CREDITO**. Ambas mitades landed: read-only vs disabled en `#6980`, naming de RichTextView en `#6977`. Follow-ups con `AKnassa` como co-author: `#7215`, `#7216`, `#7217`. Cierre textual: *"Your audit stack laid out most of the path RichText took toward a stable release."* | 2026-10-09 | Mejor desenlace de los tres casos. Se publico un borrador con notas internas por error: origen de la regla 5. |
| **5373** | Popover: **mergeado**. Nuestro review del 24/08 con 4 puntos tecnicos, 2 cambiaron el diseno (coalescing rAF + story AT). | 2026-08-30 | Un review con sustancia no es ruido. |
| **4611** | RFC de scoping (*plugin para grid focus + variant-aware grid semantics*, @humbertovirtudes). **Publicado:** comentario nuestro del 2026-08-24 senalando que el RFC se superpone con lo ya en marcha en #4690. Sin respuesta de terceros. Pelota en nosotros si se retoma. | 2026-08-24 | Un solo comentario, sin actividad posterior. El borrador vive en `docs/feedback/astryx-4611-draft.md`. |

---

## Regla de actualizacion

Antes de tocar este archivo:

1. `bash scripts/pr-thread-brief.sh facebook/astryx <n> gonzoblasco` para cada hilo abierto.
2. Actualizar **PELOTA** y **Desde** con lo que devuelve el script, no con memoria.
3. Si un hilo cerro, moverlo a la tabla de cerrados con el cierre textual.

---

*Mantenido por Kanam (CORE). Se actualiza en cada cierre de sesion sobre este repo.*
