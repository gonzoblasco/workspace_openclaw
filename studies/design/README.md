# Diseño UI/UX - Plan de estudio

> Frente abierto por Gonzalo el **2026-09-14**: *"entrenarme en el arte del diseño y la UI de aplicaciones reales. Objetivo: diseños excelentes, funcionales y accesibles a la vez; generar diseños finales, iterar, y que UI/UX/diseño/estética importen SIEMPRE."*
> Armado **2026-10-05**, al cerrar la auditoría de 19 skills de diseño (que dejó como cimiento la skill `design-direction`).
> Este documento es la fuente de verdad del plan; el material de práctica vive en `studies/design/`.

## 1. Punto de partida (qué ya tenemos)

La auditoría del 2026-10-05 dejó cimientos reales. **No arrancamos de cero:**

| Ya está | Dónde |
|---|---|
| Criterio de dirección (4 preguntas, herramienta vs pieza memorable) | skill `design-direction` |
| Gates de verificación visual (grayscale, squint, alignment, spacing, contrast, rank-1) | skill `design-direction` |
| Jerarquía como ranking 1-3 + un canal por paso | skill `design-direction` |
| Calidad visual (neutros con tinte, dark mode, easing, medidas) | skill `frontend-ui-engineering` |
| Patrones CSS de producción (grid, clamp, container queries, surface layering) | skill `frontend-ui-engineering` |
| Implementación accesible WCAG 2.1 AA | skill `frontend-ui-engineering` |
| Validación con AT | skill `a11y-at-validation` |

**Lo que falta:** el otro 80% - **el ojo**. Las reglas están escritas; lo que no está entrenado es **ver**. Un plan de estudio de diseño no es leer más reglas: es **mirar mucho, juzgar mucho, y equivocarse con feedback**.

## 2. Diagnóstico honesto

**El problema no es información: es criterio.**

Kanam ya tiene las reglas del diseño por escrito (las escribimos hoy). Lo que no tiene es:
1. **La capacidad de JUZGAR** una interfaz - decir "esta composición funciona" o "esta no", y por qué.
2. **La memoria visual** de qué existe y qué se ve bien (repertorio).
3. **El hábito de iterar** con crítica, no de tirar un diseño de una.

Un plan que solo sume reglas **no resuelve esto**. La práctica deliberada sí.

## 3. Los dominios (qué hay que saber)

Cinco dominios, ordenados por orden de aprendizaje (no por importancia):

| # | Dominio | Qué cubre | Estado |
|---|---|---|---|
| D1 | **Percepción y composición** | Gestalt, jerarquía, balance, grid, espacio negativo | Cimiento escrito; falta ojo |
| D2 | **Tipografía** | Escala, ritmo, apareo, legibilidad, registro | Cimiento escrito; falta práctica |
| D3 | **Color** | Espacio (oklch/HSL), contraste, armonía, semántica, dark mode | Cimiento escrito |
| D4 | **Movimiento e interacción** | Easing, jerarquía de motion, micro-interacciones, feedback | Cimiento escrito |
| D5 | **Accesibilidad como diseño** | Contraste, foco, teclado, AT, motion-safe | Cubierto (CPACC + a11y-at-validation) |

**Observación:** de los 5, **D5 ya está cubierto** - de hecho Gonzalo está preparando CPACC. El plan se enfoca en **D1-D4**.

## 4. El método: práctica deliberada, no lectura

Tres componentes, en orden de valor:

### 4.1 Crítica de repertorio (el más valioso)
**Ejercicio:** tomar una interfaz real por sesión y **criticarla con los Output Gates**. No "me gusta / no me gusta": correr la batería (grayscale, squint, alignment, spacing, contrast, rank-1) y anotar qué pasa cada uno.
- Fuente de casos: sitios de Awwwards/Linear/Stripe (repertorio), nuestras propias UIs, y errores concretos.
- Salida: una ficha por caso en `studies/design/criticas/`.
- **Por qué:** entrena el ojo y el vocabulario a la vez. Y usa **lo que ya escribimos** en vez de teoría nueva.

### 4.2 Recreación con variación
**Ejercicio:** tomar un componente o vista y **recrearlo** en 2-3 direcciones distintas (una herramienta funcional, una pieza memorable). Comparar y decidir cuál gana y por qué.
- Salida: el código + una línea de por qué.
- **Por qué:** obliga a elegir dirección de verdad, y expone el precio de cada una.

### 4.3 Rediseño con restricciones
**Ejercicio:** agarrar una UI propia que ya existe y **rediseñarla** con una restricción dura (sin bordes, un solo canal de jerarquía, etc.).
- Salida: antes/después + rationale.
- **Por qué:** el diseño real es bajo restricciones, no en el vacío.

### Lo que NO va en el plan
- **Más listas de reglas.** Ya tenemos ~500 líneas de reglas. Sumar es ruido.
- **Leer libros sin ejercicios.** Si algún libro entra, que sea con un caso a criticar.
- **Herramientas nuevas.** Nada de Figma, GSAP, etc. - eso es de otro problema.

## 5. Calendario propuesto (flexible, sin presión)

Sin urgencia. Ritmo: **una sesión de estudio por semana**, ~45-60 min.

| Semana | Foco | Entregable |
|---|---|---|
| 1 | D1 - Criticar 3 interfaces con los Output Gates | 3 fichas |
| 2 | D2 - Tipografía: recrear un hero en 3 registros | 3 versiones + decisión |
| 3 | D1+D2 - Rediseñar una vista nuestra con restricción | antes/después |
| 4 | D3 - Color: derivar una paleta de un tema de IDE y aplicarla | paleta + tokens |
| 5 | D4 - Motion: planificar con micro-sintaxis y verificar reduced-motion | spec de motion |
| 6 | Repaso: criticar nuestros propios diseños de las semanas 1-5 | autocrítica escrita |

Al final de la semana 6: **evaluar** si el ojo cambió. Si no, revisar el método, no sumar dominios.

## 6. Estructura de archivos

```
studies/design/
  README.md            # este índice + estado
  criticas/            # D1: fichas de crítica de repertorio (+ APRENDIZAJE-<fecha>.md)
  casos/               # renders por caso: _view / _gray / _squint
  scripts/             # critica-renders.py: renders + contraste por peor píxel
  recreaciones/        # D2/D3: versiones y decisiones
  redisenos/           # rediseños de UIs propias
```

Formato de ficha de crítica (por caso):
```markdown
# [Caso] - [Fuente]
**Fecha:** YYYY-MM-DD
**Dirección juzgada:** herramienta funcional | pieza memorable
**Gates:** grayscale [ok/falla] · squint [ok/falla] · alignment [n líneas] · spacing [ok/falla] · contrast [ok/falla] · rank-1 [ok/falla]
**Qué funciona:**
**Qué falla y por qué:**
**Qué me llevo:**
```

## 7. Cómo se relaciona con las skills

- El plan **usa** `design-direction` (dirección + gates) y `frontend-ui-engineering` (implementación).
- **No crea skills nuevas.** Si algo del estudio merece codificarse, se evalúa aparte.
- El objetivo no es "más documentación": es **que el criterio esté en el ojo, no solo en el markdown**.

## 8. Estado

- **2026-10-05:** plan creado. Cimientos (skills) listos. Pendiente: **empezar la semana 1**.
- **2026-11-06 (Kanam MIND):** semana 1 en curso - **2 de 3 fichas** de crítica de repertorio
  (`criticas/2026-11-06-linear-og.md`, `criticas/2026-11-06-stripe-og.md`), renders y medición de
  contraste reproducibles con `scripts/critica-renders.py`, y aprendizaje del día en
  `criticas/APRENDIZAJE-2026-11-06.md`. Falta una ficha para cerrar la semana.

---
_Armado 2026-10-05 al cerrar la auditoría de 19 skills de diseño. Fuente de verdad de este frente._
