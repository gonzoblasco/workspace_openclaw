# PROGRESO - radix-primitives

Capa 3. Se actualiza despues de cada topic. Fuente de verdad del avance.

**XP:** 10 por topic completado | **Badges:** 1 por nivel | **Jefe final:** ADR de adopcion.

---

## Tabla de progreso

| Nivel | Topics | Cubiertos | XP | Badge |
|---|---|---|---|---|
| 1 - Modelo mental | 10 | 10 | 100 | ✅ |
| 2 - La API | 14 | 14 | 140 | ✅ |
| 3 - Accesibilidad | 10 | 10 | 100 | ✅ |
| 4 - Stack real | 8 | 8 | 80 | ✅ |
| 5 - Criterio | 4 | 4 | 40 | ✅ |
| **Total** | **46** | **46** | **460** | - |

---

## Estado actual

**Pasada:** mapeo (Capa 1) completada el 2026-09-14. No suma XP.
**Nivel 1:** cerrado. Cuaderno `nivel-1-modelo-mental.md` con las 3 respuestas de verificacion incluidas (Gonzo no las tenia a mano; quedan como material de referencia).
**Nivel 2:** cerrado. Cuaderno `nivel-2-api.md` - instalacion, composicion (`asChild`), estado, estilos, y los 4 primitives clave (Dialog, Popover, Tooltip, Select) + helpers. Version verificada contra npm: `radix-ui@1.6.7` (2026-07-24).
**Nivel 3:** cerrado. Cuaderno `nivel-3-accesibilidad.md` - el contrato: base WAI-ARIA/APG (que significa "donde es posible"), nombres accesibles (`Label`, `Title`/`Description`, `VisuallyHidden`), teclado, foco (trampa + los 4 hooks de control) y lo que Radix NO alcanza. Incluye el callback del bug #9878 (las 4 superficies de "oculto").
**Nivel 5: CERRADO - ESTUDIO COMPLETO.** Cuaderno `nivel-5-criterio.md` (Radix vs alternativas con datos verificados + mantenimiento) y **jefe final entregado: `docs/adr/ADR-048-shadcn-radix-stack-ui.md`** - el ADR de adopcion que no existia. `ADR-037` (Lucide) ahora tiene un pointer: la cita al ecosistema shadcn/Radix dejo de ser circular.
**Estado:** 46/46 topics, 460 XP, 5 badges. Pendientes: verificaciones de los niveles 2-5 sin responder (quedan como material, no bloquean).

---

## Registro

| Fecha | Topic | Resultado | XP |
|---|---|---|---|
| 2026-09-14 | (mapeo) | Plan maestro con 5 niveles / 46 topics. Fuente: docs oficiales verificados. | 0 |
| 2026-09-14 | Nivel 1 (1.1.1 a 1.4.3) | Teoria + verificacion. Cuaderno `nivel-1-modelo-mental.md`. | 100 |
| 2026-09-14 | Nivel 2 (2.1.1 a 2.5.4) | Teoria cubierta. Cuaderno `nivel-2-api.md`. Verificacion propuesta (3 preguntas) pendiente de respuesta. | 140 |
| 2026-09-14 | Nivel 3 (3.1.1 a 3.5.2) | Teoria cubierta. Cuaderno `nivel-3-accesibilidad.md`. Verificacion propuesta (3 preguntas) pendiente de respuesta. | 100 |
| 2026-09-14 | Nivel 4 (4.1.1 a 4.4.2) | Verificado contra los repos con `gh api`: 2 de 4 proyectos usan Radix de verdad; dos generaciones de shadcn conviviendo; `kanam-pulse` como contraejemplo a11y-first sin primitives. Cuaderno `nivel-4-stack-real.md`. | 80 |
| 2026-09-14 | Nivel 5 (5.1.1 a 5.3.2) + jefe final | Comparacion con datos reales (Radix vs Base UI vs Ariakit vs HTML nativo) y **ADR-048 escrito**. Hallazgo: el dist-tag `latest` de Ariakit apunta a un prerelease de 2023. Cuaderno `nivel-5-criterio.md`. | 40 |

---

## Mapa de la divisoria (sintesis de los niveles 1-3)

| Radix se hace cargo | Queda de nuestro lado |
|---|---|
| Roles y atributos `aria` | El contenido de los nombres (`Title`, `Label`) |
| Foco: trampa en modal, autofocus, retorno | El foco del layout (tab order de la composicion) |
| Teclado basico del componente | Que no haya enfocables dentro de contenedores ocultos |
| Anuncios de screen reader en modales | Anuncios live, errores de formulario |
| Posicionamiento, colision, portales | Contraste, jerarquia, landmarks, prioridad del contenido |

---

## Deuda / dudas abiertas

- Verificar la version real de Radix instalada en los proyectos antes de afirmar comportamiento (la doc puede ir adelante de lo instalado). No hay lockfile en el workspace - el codigo vive en repos aparte.
- Sin confirmar aun: que primitives se usan de verdad en los proyectos propios. **Resuelto en el Nivel 4.**
- **Verificacion de los Niveles 2 a 5 pendiente de respuesta:** las 3 preguntas al final de cada cuaderno. El XP y los badges ya se registraron; si alguna respuesta no cierra, se revisa el topic.
- **Compromiso que deja el ADR-048:** reabrir la comparacion **cuando Base UI llegue a `1.0.0` estable**. Mientras siga en RC, no se reabre.
- **Deuda de actualizacion detectada en el barrido:** los componentes de shadcn son codigo propio y **no se actualizan solos**. `kanam-mind` quedo en la generacion vieja (`forwardRef` + `displayName`) y `kanam-forge` en la nueva (`data-slot`). No es un bug, pero si una decision pendiente: unificar o dejar conviviendo.
