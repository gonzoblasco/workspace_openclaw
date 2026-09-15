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
| 4 - Stack real | 8 | 0 | 0 | 🔴 |
| 5 - Criterio | 4 | 0 | 0 | 🔴 |
| **Total** | **46** | **34** | **340** | - |

---

## Estado actual

**Pasada:** mapeo (Capa 1) completada el 2026-09-14. No suma XP.
**Nivel 1:** cerrado. Cuaderno `nivel-1-modelo-mental.md` con las 3 respuestas de verificacion incluidas (Gonzo no las tenia a mano; quedan como material de referencia).
**Nivel 2:** cerrado. Cuaderno `nivel-2-api.md` - instalacion, composicion (`asChild`), estado, estilos, y los 4 primitives clave (Dialog, Popover, Tooltip, Select) + helpers. Version verificada contra npm: `radix-ui@1.6.7` (2026-07-24).
**Nivel 3:** cerrado. Cuaderno `nivel-3-accesibilidad.md` - el contrato: base WAI-ARIA/APG (que significa "donde es posible"), nombres accesibles (`Label`, `Title`/`Description`, `VisuallyHidden`), teclado, foco (trampa + los 4 hooks de control) y lo que Radix NO alcanza. Incluye el callback del bug #9878 (las 4 superficies de "oculto").
**Siguiente:** Nivel 4 (Radix en el stack real - shadcn y nuestros proyectos). Requiere mirar los repos propios: es el primer nivel que no se cierra solo con la doc.

---

## Registro

| Fecha | Topic | Resultado | XP |
|---|---|---|---|
| 2026-09-14 | (mapeo) | Plan maestro con 5 niveles / 46 topics. Fuente: docs oficiales verificados. | 0 |
| 2026-09-14 | Nivel 1 (1.1.1 a 1.4.3) | Teoria + verificacion. Cuaderno `nivel-1-modelo-mental.md`. | 100 |
| 2026-09-14 | Nivel 2 (2.1.1 a 2.5.4) | Teoria cubierta. Cuaderno `nivel-2-api.md`. Verificacion propuesta (3 preguntas) pendiente de respuesta. | 140 |
| 2026-09-14 | Nivel 3 (3.1.1 a 3.5.2) | Teoria cubierta. Cuaderno `nivel-3-accesibilidad.md`. Verificacion propuesta (3 preguntas) pendiente de respuesta. | 100 |

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
- Sin confirmar aun: que primitives se usan de verdad en `kanam-pulse`, `soporteml-v4` y `kanam-forge`, y cuales llegan via shadcn. (Se resuelve en el Nivel 4.)
- **Verificacion de los Niveles 2 y 3 pendiente de respuesta:** las 3 preguntas al final de cada cuaderno. El XP ya se registro; si alguna respuesta no cierra, se revisa el topic.
- **Nivel 4:** requiere acceso a los repos de los proyectos (kanam-pulse, soporteml-v4, kanam-forge). Sin lockfiles ni node_modules en el workspace, hay que clonar o mirar los repos para saber que primitives se usan de verdad.
