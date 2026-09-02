---
name: "a11y-at-validation"
description: "Cuándo la validación manual de accesibilidad es obligatoria en OSS, y cómo ejecutarla."
---

# Skill: a11y-at-validation

## Objetivo

Saber **cuándo la validación manual de accesibilidad es obligatoria** (no solo recomendable) antes de considerar un PR de a11y terminado, y cómo ejecutarla y documentarla en un contexto de colaboración OSS.

## Regla central: cuándo es OBLIGATORIA la validación manual

La validación AT manual es **obligatoria** (no opcional) cuando el cambio altera **lo que un screen reader anuncia** (la frase hablada, no el atributo) y ese anuncio no es verificable por tests unitarios.

### Frontera: test unitario vs manual

| Verificable por test unitario | Solo verificable manualmente |
|---|---|
| Atributos ARIA en el DOM | Qué anuncia el screen reader (la frase) |
| Roles, `aria-labelledby`, `aria-selected` | Timing del anuncio (cuándo se dice, si se dice) |
| Estructura del árbol de accesibilidad | Interacción real (roving focus, `aria-activedescendant`) |

**Caso de oro (2026-08-12, radix-ui/primitives):** el PR #4109 agregó `aria-posinset`/`aria-setsize` calculados en `useLayoutEffect`. Los atributos estaban correctos en el DOM (51 tests verdes), pero la validación manual con VoiceOver+Chrome reveló que la primera opción sin preselección **no anunciaba nada** (#4110) por un race de timing entre el montaje del item y el anuncio del AT. Ningún test unitario podía atraparlo.

**Regla derivada:** si tu cambio toca `aria-*` que afecta anuncio, roles, roving focus o `aria-activedescendant`, la validación manual es obligatoria. Los tests verdes NO son suficientes.

## Cuándo aplicar

Aplicar este flujo en PRs de accesibilidad en repos de OSS (Radix, shadcn/ui, TanStack, astryx, etc.) cuando el cambio:

- Agrega/modifica atributos ARIA que afectan anuncio (posinset, setsize, live regions, labels dinámicos).
- Cambia roles o interacción (roving focus, activedescendant, combobox/listbox).
- Porta texto a nodos (ej. portaling de texto de opción al trigger).
- Maneja timing de montaje (useLayoutEffect, efectos que pintan atributos tras el primer paint).

## Pasos del flujo

### 1. Identificar si el cambio toca "anuncio" (no solo DOM)

Si el cambio cae en la columna "solo verificable manualmente" de la tabla, la validación AT es obligatoria. Documentar esto ANTES de dar el PR por terminado.

### 2. Ejecutar la validación manual

0. **Si el repo tiene tests de layout en browser real (`.browser.test.*` con vitest), correrlos primero** - es la evidencia automatizable que los maintainers piden (Adobe lo pidió explícitamente). En react-spectrum: `yarn vitest run --config=vitest.browser.config.ts --project=chromium-desktop <archivo>` y `--project=firefox-desktop`. Requiere `npx playwright install chromium firefox` la primera vez. Un test de layout mide el bounding box del input oculto contra el componente visible (lo que jsdom no puede validar) y es la prueba de que el SR focus ring coincide con el visual. Documentar la matriz (browser x resultado) en el PR.

1. Levantar el storybook/playground local apuntando a la rama del PR (workspace build, no main).
2. Activar el AT del sistema:
   - macOS: VoiceOver con **Cmd + F5**.
   - Activar **captions/live captions** (Preferencias del sistema -> Accesibilidad -> VoiceOver -> Detallado -> Usar subtítulos) para confirmar visualmente la frase anunciada.
3. Probar los casos límite, no solo el feliz:
   - Sin valor preseleccionado (la primera opción suele ser el caso roto).
   - Con valor preseleccionado.
   - Con agrupación (Select.Group) si aplica.
   - Opción "clear"/placeholder (value vacío) - suele ser intencional, ver paso 3.
4. Registrar en una tabla qué se esperaba vs qué se anunció, y si los captions confirman.

### 3. Si se detecta un hallazgo: verificar si es intencional o bug

ANTES de proponer cambiar el componente, buscar en el código si el comportamiento es deliberado:

- Guardas y comentarios que documenten el patrón (ej. "consumer may render an item with empty value to act as a clear option").
- Funciones tipo `shouldShowPlaceholder`.
- Patrones de diseño documentados del primitive (ej. APG).

**Si es intencional** (por diseño): NO tocar el componente con un PR. Documentar el hallazgo en un issue con diagnóstico + opciones, y dejar la decisión de dirección a los maintainers.

**Si es bug real**: proceder con un PR, idealmente con el hallazgo documentado.

### 4. Documentar la validación en el PR/issue

Comentar en el PR la evidencia de validación manual (qué anunció cada caso, captions confirmados). Si hay un hallazgo separado, abrir un issue aparte y referenciarlo - no mezclar con el PR principal.

## Antes de reworkear un PR de a11y que falla CI: verificar contra main

Cuando un maintainer reporta que un PR de a11y falla tests/lint, NO reworkear a ciegas. Verificar primero, con evidencia empírica, dos cosas:

1. **¿El bug reportado existe en main actual?** El issue puede ser viejo y ya resuelto por otro PR. Correr el test de regresión contra main (sin el fix) - si pasa, el fix es innecesario y el PR debe cerrarse con el hallazgo documentado, no reworkearse.
2. **¿La suposición del fix sobre el modelo de datos es cierta?** Ej. asumir que `item.index` reinicia por sección cuando en react-stately ya es global. Verificar con un test de debug que imprima los valores reales (index, parentKey) en la estructura real, no leyendo el código.

**Método:** escribir un test de debug que renderice la colección real y loguee los valores que el fix asume, correrlo contra main, y comparar con lo que el fix espera. Si el código original ya produce el resultado correcto, el fix rompe sin arreglar nada - cerrar el PR con comentario honesto en vez de insistir.

**Regla derivada:** un fix que "arregla" un bug que ya no existe, y que además rompe tests existentes por una suposición falsa, no se reworkea - se cierra documentando el hallazgo. La política AI-assisted de Adobe (y similares) exige además validación humana de SR, que no se puede fabricar.

**Rescatar el test de regresión como PR test-only:** si el fix es innecesario pero el test de regresión que lo acompaña tiene valor (pasa contra main y fija el comportamiento), no descartarlo con el PR cerrado. Extraerlo como PR test-only: `git checkout -b test/<desc> origin/main`, aplicar solo el diff del test con `git show <commit> -- <archivo-test> | git apply`, verificar que pasa contra main, abrir el PR (sin cambios de producción) y referenciarlo en el comment de cierre del PR original. Así el valor del test sobrevive sin arrastrar el fix roto.

### Distinguir "fix roto" de "test hermano sin actualizar"

Cuando un maintainer reporta CI rojo en un PR de a11y, antes de decidir entre cerrar o reworkear, buscar si el fallo viene de un **test hermano** que usa el mismo hook internamente pero quedó con el comportamiento viejo. Ej. react-spectrum: `SearchAutocomplete.test.js` usa `useComboBox` internamente, así que un cambio en el announcement de `useComboBox` rompe sus asserts aunque el fix sea correcto.

**Método:** `grep -rln "expect(announce)" packages/` (o el assert que cambió) para encontrar todos los tests que dependen del comportamiento modificado, no solo el del componente directo. Si el fix es una dirección válida y solo falta actualizar el test hermano al nuevo comportamiento (mismo patrón que el test del componente ya actualizado), se actualiza y se pushea - no se cierra. Si en cambio el fix rompe por una suposición falsa sobre el modelo de datos, se cierra (caso anterior).

## Errores comunes

- **Dar un PR de a11y por terminado con solo tests unitarios verdes.** Los tests verifican atributos, no anuncios.
- **Proponer cambiar un componente antes de verificar si el comportamiento es intencional.** Riesgo de PR que rompe el contrato del primitive.
- **Abrir un comentario en un issue propio con "Thanks for opening this".** Esa frase es para agradecer a otro que reportó; absurda cuando uno mismo abrió el issue. Arrancar directo con el análisis.
- **Subir PR de diseño sin consenso.** Cambios de diseño de un primitive maduro requieren discusión previa con maintainers, no un PR unilateral.

## Checklist de cierre

- [ ] ¿El cambio toca anuncio/rol/interacción? -> validación manual obligatoria hecha.
- [ ] ¿Probé los casos límite (sin preselección, placeholder, grupos)?
- [ ] ¿Captions confirman la frase anunciada?
- [ ] ¿Verifiqué si un hallazgo es intencional (guardas/comentarios/patrones) antes de tocar el componente?
- [ ] ¿Documenté la evidencia en el PR y separé hallazgos en issues propios?
