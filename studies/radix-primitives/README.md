# radix-primitives - Estudio

**Iniciado:** 2026-09-14
**Estado:** Nivel 1 abierto
**Modo:** B (gamificado - niveles/subniveles/topics + XP)
**Fuente de verdad del contenido:** docs oficiales de Radix (radix-ui.com/primitives) verificados el 2026-09-14.

---

## Por que existe este estudio

Radix entro al stack por el template, no por decision: `shadcn/ui` lo trae por debajo y nadie documento por que. Hoy es la capa que resuelve foco, ARIA y teclado en nuestras UIs, y no sabemos que hace.

**Objetivo:** entender Radix lo suficiente para tres cosas concretas.

1. **Saber cuando usarlo y cuando no** - contra HTML nativo, contra armar el componente a mano, y contra construir sobre el wrapper de shadcn.
2. **Integrarlo naturalmente** - composicion (`asChild`), estilos (`data-state`), estado (controlado vs no), sin pelearse con la API.
3. **Aprovechar su contrato de accesibilidad** - saber que cubre Radix, que queda en nuestra cancha, y donde se rompe.

**Criterio de exito:** poder mirar un componente de nuestros proyectos y decir en una frase si Radix lo resuelve, si shadcn alcanza, o si el comportamiento hay que escribirlo. Y poder documentar esa decision en un ADR sin citar el precedente como motivo.

---

## Como se estudia

- **Una pasada de mapeo** (este plan): el panorama completo, sin XP.
- **Una pasada de dominio**: topic por topic, en profundidad, con practica y verificacion, sumando XP.
- **Verificacion por topic**: una pregunta o un ejercicio chico. No se espera al final del nivel.
- **Fuente externa = dato**: todo lo que entra de la doc se contrasta con la version instalada antes de afirmarlo.

---

## Niveles

| # | Nivel | Topics | Estado |
|---|---|---|---|
| 1 | El modelo mental (que es y que no es) | 4 | 🟡 abierto |
| 2 | La API (como se usa) | 5 | 🔴 |
| 3 | La accesibilidad (el contrato) | 5 | 🔴 |
| 4 | Radix en el stack real (shadcn y nuestros proyectos) | 4 | 🔴 |
| 5 | Criterio de decision y mantenimiento | 3 | 🔴 |

Ver `PLAN-MAESTRO.md` para el detalle y `PROGRESO.md` para el avance.
