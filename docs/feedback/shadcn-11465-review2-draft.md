# Borrador respuesta - shadcn-ui/ui PR #11465 (review de shadcn)

> Review: https://github.com/shadcn-ui/ui/pull/11465#issuecomment-5514527235
> Fix pusheado: commit `1b97764` en `fix/message-scroller-drain-released-spacer`
> Estado: **RESPUESTA PUBLICADA** - https://github.com/shadcn-ui/ui/pull/11465#issuecomment-5517588705 (02/09 19:58)

---

## Comentario propuesto (en inglés, para el PR)

All three points are addressed in `1b97764`:

**1. Programmatic scrolls no longer drain.** `drainReleasedSpacer` now skips `anchored-to-message` and `settling-jump` modes and `autoscrollingRef`, so the scroll event fired by the placement scroll can no longer collapse the spacer and yank the anchored turn. The hold path (`reanchorToAnchoredMessage`) remains the only consumer of the spacer while anchored.

**2. Idempotent math.** The drain now recomputes the remaining room from absolute geometry on every event - `max(0, contentBottom + spacerHeight - (scrollTop + clientHeight))` - instead of subtracting an absolute overlap. Inertial scrolling converges instead of over-draining.

**3. Hand-off only at the real bottom.** The drain returns early when the reader is above the spacer zone (`overlap <= 0`), leaving the spacer untouched, and only calls `scrollToEnd` when the recomputed spacer hits zero - which by construction means the reader is at the live edge.

**4. Browser-mode regression tests.** Two tests in `message-scroller.browser.test.tsx` with `autoScroll` on: anchored placement does not yank to the bottom (the spacer stays reserved), and a manual scroll during an anchored stream releases the anchor, the reply drains the spacer without moving the reader, and scrolling to the real bottom re-engages following.

Verification: jsdom 51/51, browser mode 48/48, typecheck clean.

---

## Notas internas para Gonzo

- **Punto 1 (el crítico):** el guard de modos + autoscrollingRef es exactamente lo que pedía el maintainer. El yank de turnos anclados en browser real era el bug que jsdom no podía ver.
- **Punto 2:** la fórmula idempotente `contentBottom + spacer - (scrollTop + clientHeight)` converge en vez de sobre-drenar. Sirve para ambos paths (resize y scroll) - por eso se eliminó el flag `viaScroll`.
- **Punto 3:** el early return con `overlap <= 0` deja el spacer intacto si el reader está arriba de la zona - cubre el caso de resize con reader scrolleado arriba.
- **Punto 4:** los 2 tests browser mode nuevos son la evidencia que el maintainer pidió explícitamente ("add a browser-mode test with autoScroll on, since jsdom structurally can't catch this class of bug").
- **Proceso:** el agente A (DeepSeek) escribió el fix del controller + tests jsdom pero fue terminado por SIGTERM antes de terminar. Kanam verificó (jsdom 51/51, typecheck, browser 46/46), escribió los 2 tests browser mode, y verificó todo de nuevo (48/48). Commit + push hecho.
- **Tono:** directo a la sustancia, sin agradecer de más - el maintainer pidió cambios concretos y se responden con evidencia. Guion comun en todo.
