# ADR-048: Radix/shadcn como capa de UI - adopcion con criterio, no por precedente

**Fecha:** 2026-09-14
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (jefe final del estudio `studies/radix-primitives`)
**Relacionado:** ADR-037 (Lucide), ADR-047 (Kanam Design System)

---

## Contexto

`shadcn/ui` entro al stack **por el template, no por decision**. Ningun proyecto eligio Radix explicitamente; el scaffold lo trajo, y como shadcn envuelve primitives de Radix, Radix entro detras. La eleccion quedo implicita.

El problema se materializo en `ADR-037` (Lucide), que cita *"el ecosistema shadcn/Radix"* como si fuera un hecho del stack para fundamentar otra decision. El propio ADR-037 admite el origen: *"cada proyecto usaba lo que traia el template (shadcn/ui incluye Lucide por default, pero no estaba documentado como decision)"*. Es decir: **un ADR fundo una eleccion en otra que nunca se tomo explicitamente** - precedente fabricado.

El 2026-09-14 Gonzo establecio la regla que lo prohibe (`USER.md` + `AGENTS.md`): ninguna dependencia se adopta, se mantiene ni se cita por estar ya presente o haberse usado antes. Orden obligatorio: **(1) que hace, (2) por que se elige hoy, (3) decision explicita (ADR), (4) recien entonces se cita.**

Este ADR es ese paso 3. Existe **porque el precedente no era razon suficiente**.

### Verificacion previa (fuentes reales, no memoria)

**Que hay de verdad en los proyectos** (barrido con `gh api`, 2026-09-14):

| Proyecto | Paquetes `@radix-ui/*` | Componentes shadcn | Estado |
|---|---|---|---|
| `kanam-forge` | 6 (avatar, collapsible, dialog, separator, slot, tooltip) | 11 | Codigo activo |
| `kanam-mind` | 3 (dialog, label, slot) | 5 | Codigo real, proyecto archivado del portfolio |
| `quedamos` | 0 | 0 | **Sin codigo**: declara shadcn como stack planeado |
| `kanam-pulse` | 0 | 0 | **Sin Radix a proposito** (a11y WCAG 2.2 AA) |

**Nota:** la familia `soporteml` queda fuera de todo barrido (ADR-001, decision de Gonzo). No se toca ni se lista.

**Que es cada pieza:**

- **Radix Primitives:** dependencia de **runtime**. `radix-ui@1.6.7` (2026-07-24), MIT, 55 dependencias internas `@radix-ui/*`, tree-shakeable. Componentes unstyled que resuelven roles ARIA, foco, teclado y anuncios de screen reader en modales.
- **shadcn/ui:** **no es una dependencia** - es una CLI que copia archivos al repo. El codigo vive en `components/ui/` y es propio: se edita libre, **no se actualiza solo**.

## Decision

**Se mantiene Radix como capa de comportamiento accesible y shadcn como codigo propio, con reglas de uso explicitas y disparadores de revision.**

### Fundamento (pasos 1 y 2 de la regla)

**Que hace (1):** resuelve la parte dificil y repetible de los patrones interactivos complejos - dialog, select, combobox, tooltip, menu - siguiendo los patrones WAI-ARIA/APG donde puede: roles, foco, teclado basico y anuncios de modal.

**Por que se elige hoy (2):**

1. **Cobertura y granularidad:** expone partes componibles (`Root`/`Trigger`/`Content`...), lo que permite integrarlo a un design system propio en vez de aceptar un componente cerrado. Es la condicion para convivir con el Kanam Design System (ADR-047).
2. **API estable:** `1.6.7` estable, no prerelease.
3. **La alternativa mas fuerte no esta lista:** Base UI (mismo equipo: Radix + Floating UI + Material UI) esta en **`1.0.0-rc.0`**. Adoptar un RC como base de accesibilidad cambia un problema de conocimiento por uno de estabilidad.
4. **Ya hay codigo real encima:** 2 proyectos con componentes shadcn escritos y traducidos. La migracion no se justifica mientras lo de arriba se sostenga.

### Reglas de uso

1. **Se usa Radix cuando hay un patron interactivo complejo** que no se quiere reimplementar: modal, select, combobox, tooltip, menu, disclosure con estado.
2. **No se usa Radix por inercia.** Si el HTML nativo resuelve -`<dialog>` con `showModal()`, `<details>`/`<summary>`, `<select>`, `<hr>`-, esa es la primera opcion a evaluar. Radix es para lo que el nativo no cubre bien.
3. **a11y-first no implica Radix.** `kanam-pulse` es WCAG 2.2 AA desde el dia uno y no lo usa: no tiene patrones interactivos complejos, y lo que necesita (contraste, jerarquia, landmarks, semantica limpia) **no es el contrato de Radix**. Sumar la dependencia ahi agregaria peso y una capa entre el equipo y el DOM, sin agregar accesibilidad.
4. **Instalacion en proyectos nuevos:** usar el paquete unico `radix-ui`. Evita duplicar las 55 dependencias internas en versiones distintas (Nivel 2 del estudio).
5. **Los componentes de shadcn son codigo propio:** se editan, se traducen (los strings de UI van en espanol) y **se mantienen a mano**. Si shadcn mejora upstream, no llega solo.
6. **Ningun ADR, doc o comentario vuelve a citar Radix/shadcn como "el stack" sin apuntar a este ADR.**
7. **La accesibilidad no se delega:** Radix cubre roles, foco, teclado basico y anuncios de modal. **Quedan nuestros** el contenido de los nombres, el contraste, la jerarquia, los anuncios live, los errores de formulario y el orden de tabulacion del layout.

### Disparadores de revision (cuando se reabre este ADR)

| Disparador | Umbral |
|---|---|
| **Base UI llega a `1.0.0` estable** | Reabrir la comparacion (es el candidato real) |
| **Radix sin releases durante un trimestre** | Revisar cadencia y plan de salida |
| **PRs propios sin review por inactividad** | Ya ocurrio (4 PRs cerrados 22/08); si se repite, pesa en la decision |
| **Nueva generacion de shadcn rompe componentes propios** | Decidir unificacion o congelamiento de version |

## Alternativas consideradas

1. **Base UI** (mismo equipo que Radix, Floating UI y Material UI). **Rechazada hoy, no descartada.** Repo activo (10.902 stars, push del 2026-09-15) y arquitectura comparable, pero npm publica **`1.0.0-rc.0`**: un release candidate. **Disparador: cuando llegue a `1.0.0`.** Es la alternativa con mas chance de reemplazar a Radix en el futuro.
2. **Ariakit.** Repo mas sano por actividad (8.611 stars, 44 issues abiertos vs 351 de Radix, push del 2026-09-15). **Rechazada:** el dist-tag `latest` de npm apunta a **`2.0.0-next.44`, publicada en abril de 2023** - un prerelease de hace mas de dos anos. Quien instala sin mirar, instala eso. Es el caso que prueba que **el estado del repo no es el estado del paquete**.
3. **HTML nativo solo, sin dependencia.** `<dialog>` cubre modal + foco + `Esc`; `<details>` el disclosure. **Rechazada como unica via:** no da personalizacion, posicionamiento ni los anuncios de screen reader de modal, y obligaria a escribir y verificar a mano lo que Radix ya tiene probado. **Pero se adopta como primera opcion a evaluar por caso** (regla 2).
4. **Construir primitives propios (headless in-house).** **Rechazada:** es exactamente el trabajo dificil y repetible que justifica la dependencia; hacerlo a mano en cada proyecto multiplica el costo y la superficie de bug.
5. **Seguir con el statu quo sin ADR.** **Rechazada** por definicion: es la opcion que produjo el precedente fabricado.

## Consecuencias

**Positivas**
- La eleccion deja de ser implicita: cualquier proyecto nuevo hereda criterio, no inercia.
- `ADR-037` queda respaldado: su cita al ecosistema ahora apunta a una decision real.
- Queda escrito **cuando no usar Radix**, que es la mitad que faltaba: sin eso, la tendencia natural es sumarlo a todo.
- Los disparadores de revision evitan que este ADR se convierta en dogma: tiene fecha de vencimiento condicional.

**Negativas / costos**
- Hay que mantener el codigo de shadcn a mano (traducciones incluidas) y decidir la convivencia de generaciones - hoy `kanam-mind` usa la vieja (`forwardRef` + `displayName`) y `kanam-forge` la nueva (`data-slot`).
- Radix tiene la cadencia mas lenta de las tres alternativas (ultimo push 2026-08-08) y los 4 PRs propios se cerraron sin review. Se acepta el riesgo con disparador de revision, no con optimism.
- Revisar el ADR cuando Base UI llegue a estable es trabajo futuro ya comprometido.

## Referencias

- `studies/radix-primitives/` - el estudio que produce esta decision (5 niveles: modelo mental, API, contrato de accesibilidad, stack real, criterio).
- `docs/adr/ADR-037-lucide-iconos-base.md` - el ADR que citaba el ecosistema sin respaldo.
- `docs/adr/ADR-047-kanam-design-system.md` - la identidad visual transversal con la que esta capa convive.
- `USER.md` / `AGENTS.md` - la regla "el precedente no es un motivo" (2026-09-14).
