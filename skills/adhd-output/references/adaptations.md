# Adaptaciones respecto al original

El skill original es [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT), pensado para agentes de codigo CLI (Claude Code). Estas son las diferencias y por que.

---

## Cambios

### "No recap" -> "Recap minimo de lo que cambio"

**Original:** sin recap en absoluto.

**Adaptado:** restatear solo lo que cambio (que corre, que falta, donde estamos).

**Por que:** en el workspace de Kanam la memoria es el punto. El recap no es ruido, es continuidad. En una sesion larga de horas, saber donde estamos parados es la diferencia entre retomar y re-descubrir. Pero el recap completo de todo si es ruido - de ahi "solo lo que cambio".

### "Cap a 5 items" -> con excepcion explicita

**Original:** cap duro a 5.

**Adaptado:** cap por default, excepcion cuando la lista ES el entregable.

**Por que:** en un inventario, catalogo o comparativa pedida, cortar a 5 destruye el valor. La regla existe para forzar priorizacion, no para mutilar entregables. Cuando la lista es el entregable, tabla en vez de bullets.

### "Restate state every turn" -> version workspace

**Original:** restatear estado cada turno en el mensaje.

**Adaptado:** el restateo puede vivir en el `progress_card` en vez del mensaje.

**Por que:** en sesiones largas el progress card es la superficie de estado; duplicarlo en el mensaje es ruido. El mensaje lleva la accion, el card lleva el estado.

### Contexto local

- Idioma: el workspace es en espanol, con regla de guion comun (nunca em dash).
- Se agrego seccion de interaccion con `anti-ai`, `adhd-assistant` y `session-lifecycle`.
- Se agrego script de lint de formato (`scripts/check-output.sh`), que el original no tiene.

---

## Lo que NO se cambio

- **Accion primero.** Sin excepcion.
- **Pasos numerados.** Sin excepcion.
- **Next step concreto.** Sin excepcion.
- **Time estimates en minutos.** Sin excepcion.
- **Errores matter-of-fact.** Sin excepcion.
- **Sin preambulo ni cierres.** Sin excepcion.
- **Hacer visibles las victorias.** Sin excepcion.
- **Suprimir tangentes.** Sin excepcion.

---

## Cuando NO aplicar este skill

| Situacion | Por que |
|---|---|
| Cierre de sesion / handoff | El recap ES el entregable |
| El usuario pide analisis exploratorio | La exploracion necesita el desarrollo, no solo la conclusion |
| Explicacion pedagogica | El paso a paso del razonamiento ES el valor |
| El usuario pide una lista larga | La lista es el entregable |
| Conversacion casual | No hay accion, hay charla |

La regla general: si el usuario pidio el proceso, dar el proceso. Si pidio el resultado, dar el resultado. Este skill es para lo segundo.

---

## Licencia

El original es MIT (c) ayghri. Esta adaptacion mantiene el espiritu y las 10 reglas; los cambios son de contexto (idioma, excepciones, scripts).
