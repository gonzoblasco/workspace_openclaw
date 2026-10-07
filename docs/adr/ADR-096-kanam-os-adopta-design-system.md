# ADR-096: kanam-os adopta el Kanam Design System (y el sistema gana su tema oscuro)

**Fecha:** 2026-10-06
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam (CORE orquesta; DEV ejecuta)
**Origen:** sesión 2026-10-06 - Gonzo: *"migra"* (tras la re-evaluación ADR-095, cuyo hueco real era la adopción: kanam-os usaba un tema paralelo).
**Relacionado:** ADR-047 (design system), ADR-083 (el CORE no escribe código de proyecto), ADR-088 (pipeline A/B), ADR-094 (a11y medida), ADR-095 (re-evaluación)

---

## Contexto

La re-evaluación (ADR-095) confirmó que el design system **existe** (ADR-047) pero su **adopción es ~0**: sólo kanam-lab lo consume; **kanam-os usa un tema paralelo hecho a mano** (`app/globals.css`, ~164 variables `--bg`, `--text`...). Gonzo pidió migrarlo.

Al planificar apareció un bloqueo real: **el design system es solo claro** (kanam.css = modo claro). kanam-os es **dark-first** con un toggle dark/light resuelto en el servidor (`data-theme` + cookie, sin flash). Migrar sin un tema oscuro en el sistema rompería la app.

## Decisión

### 1. El sistema gana su tema oscuro (CORE, artefacto de gobernanza)

`design/tokens/themes/dark.tokens.json`: sobreescribe **solo la capa semántica** del sistema base, con la paleta del tema oscuro de kanam-os (probada en uso real) recalculada al piso WCAG. Se suma a `REGISTRY` del build y al `theme_contexts` del guard.

- **Modo vs marca:** `dark` es el eje de **modo** (oscuro/claro), no de marca (plaza/terrario). Hoy comparten el atributo `data-theme` por simpleza; separarlos se evalúa cuando exista una marca que necesite su propio modo oscuro.
- **El modo claro no necesita archivo:** `kanam.css` (semántica base) **es** el claro, en `:root`. Una app con `data-theme="light"` cae al `:root`. `dark.css` es `[data-theme="dark"]`.
- **Verificado:** los 11 pares del tema oscuro pasan el piso por rol (text.primary 12.83:1, danger 7.50:1, brand 4.85:1...).

### 2. kanam-os migra a consumir los tokens del sistema (DEV, pipeline A/B)

El trabajo de código lo ejecuta **DEV** (ADR-083). Contrato:

- **Fuente de verdad externa:** los tokens viven en el workspace (`~/.openclaw/workspace/design/tokens/dist/`). kanam-os **no** redefine colores: consume `kanam.css` (claro, `:root`) + `dark.css` (`[data-theme="dark"]`).
- **Mecanismo anti-drift:** como el `dist/` es generado, kanam-os lo **sincroniza** en build (script que corre `build-tokens.py` y copia el CSS generado), no lo copia a mano. Fallback: copia versionada si el workspace no está presente.
- **Preservar:** el toggle dark/light (server-side, sin flash), el layout y los componentes existentes. El cambio es de **color/tipografía a tokens**, no de estructura.
- **Cierre:** el guard de contraste del sistema (ADR-095) + `a11y-scan.mjs` (ADR-094) sobre las páginas vivas.

## Consecuencias

- **Positivas:** kanam-os pasa a tener la identidad Kanam (no un tema propio); el sistema gana su modo oscuro, útil para toda app interna. La adopción del design system sube de 1 a 2 consumidores.
- **Riesgo:** el acoplamiento kanam-os ↔ workspace (los tokens viven en el workspace). Se mitiga con el sync en build y el fallback versionado.
- **Deuda:** si el sync es frágil, promover a un paquete/artefacto publicado. Se evalúa si aparece fricción real.
- **Verificación (CORE):** el repo real, no el auto-reporte - `git status`/diff de kanam-os, el CSS generado, el guard de contraste, y `a11y-scan` sobre las rutas.

## Alternativas consideradas

1. **No agregar el tema oscuro y migrar solo a claro.** Rechazada: borra el dark de kanam-os (feature existente y preferida).
2. **Reemplazar solo los valores de color en globals.css (sin consumir el sistema).** Rechazada: sería "aplicar el sistema" de nombre, sin fuente de verdad única - la dispersión que el ADR-047 vino a resolver.
3. **Publicar los tokens como paquete npm.** Rechazada por ahora: infra extra (publish, versionado) para 2 consumidores. El sync en build alcanza; se promueve si escala.
