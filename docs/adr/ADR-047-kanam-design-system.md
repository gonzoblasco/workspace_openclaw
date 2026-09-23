# ADR-047: Kanam Design System como identidad transversal de todo producto

**Fecha:** 2026-09-14
**Estado:** Aceptado
**Decisores:** Gonzo (pedido explícito) + Kanam (diseño)
**Origen:** workspace (pedido explicito de Gonzo; integra `design/tokens.kitano` de julio 2026)
**Supersede:** `design/tokens.kitano` (borrador de julio 2026, integrado y evolucionado acá)

---

## Contexto

Hasta hoy, cada producto Kanam decidía su look por su cuenta: `tokens.kitano` (julio, borrador
suelto), el tema Terrario de kanam-lab (septiembre), las 3 direcciones comerciales del ejercicio de
diseño. Resultado: decisiones visuales dispersas, sin fuente de verdad, y riesgo de repetir el
"AI look" (gradientes, morado por defecto, radios exagerados) en cada proyecto nuevo.

El 2026-09-14 Gonzo pidió que el sistema de diseño "pueda avanzar y crecer" y "sea la identidad de
todo producto que creemos desde Kanam". Eso es una decisión de arquitectura, no un entregable de
diseño: necesita un ADR.

Antes de escribir, se verificó el terreno (fuente real, no memoria): `design/tokens.kitano` existía
con marca Kanam ya definida (teal `#0d9488`, Inter, focus naranja). No se descartó: se integró.

## Decisión

Se instituye el **Kanam Design System** en `design/` como la identidad visual única de todo
producto Kanam, con arquitectura de **3 capas + temas**:

1. **Primitivas** (`kanam.tokens.json`): valores crudos. Nunca se usan directo en producto.
2. **Semántica** (`kanam.tokens.json`): intención (`brand.primary`, `state.danger`). Es lo que usan
   los componentes.
3. **Componente**: tokens de un componente específico, viven en el proyecto.

Los **temas de producto** (`themes/*.tokens.json`) sobreescriben **solo la capa semántica**
(intent over value). Un producto nuevo o un cambio de marca redefine ~40 tokens y no toca ningún
componente.

El CSS se **genera** con `build-tokens.py` (fuente de verdad = JSON), y el build **falla** si alguna
referencia queda sin resolver. El `dist/` es generado: no se edita a mano.

## Temas registrados

| Tema | Uso | Paleta |
|---|---|---|
| **Kanam** (base) | El sistema, docs internas | Teal `#0d9488` |
| **Plaza** | Productos comerciales (Kanam Desk, SoporteML) | Cream + Navy + Sun |
| **Terrario** | Herramientas internas (kanam-lab, dashboards) | Sand + Verde |

## Consecuencias

**Positivas**
- Un producto nuevo arranca con identidad correcta sin re-decidir nada: aplica un tema y listo.
- Cambio de marca global = editar un JSON + rebuild. Los componentes no se tocan.
- Los no-negociables (contraste WCAG verificado, foco visible, estado nunca solo por color,
  semántica única) dejan de depender de la memoria de cada sesión: son parte del sistema.
- Portable entre stacks: el CSS generado sirve para React, HTML plano y Python/Gradio (kanam-lab
  ya es la implementación de referencia de Terrario).

**Negativas / costos**
- Agregar un tema requiere disciplina: definir la matriz de contraste, agregarlo al build,
  documentarlo. No es "copiar y pintar".
- Hay que mantener el `dist/` regenerado (o el build en CI) cuando cambian los tokens.
- El vocabulario de tokens (semántico, no literal) exige que quien escribe componentes piense en
  intención. Es la inversión que hace escalable al sistema.

**Reglas operativas**
- Ningún proyecto define colores hardcodeados si existe un token semántico equivalente.
- Todo tema nuevo declara su matriz de contraste en el JSON (`$contrast`) y en `design/README.md`.
- Componentes con ARIA/anuncio pasan por validación manual de screen reader (skill
  `a11y-at-validation`) antes de considerarse terminados.

## Alternativas consideradas

1. **Dejar cada proyecto con su propio estilo (statu quo).** Rechazada: es lo que produjo la
   dispersión actual y no hay forma de garantizar consistencia ni accesibilidad.
2. **Un CSS framework de terceros (Tailwind + shadcn) como fuente de verdad.** Rechazada como
   *fuente*: ataría la identidad a un vendor y a un stack. El sistema es stack-agnóstico; un
   proyecto puede usar Tailwind consumiendo estos tokens. (Relacionado: TODO #52, destino de
   Radix/shadcn - regla vigente: ninguna dependencia se cita como decisión por el solo hecho de
   estar presente.)
3. **Descartar `tokens.kitano` y empezar de cero.** Rechazada: ya tenía marca Kanam definida; se
   integró y evolucionó en vez de tirarla.

## Referencias

- `design/README.md` - portada y guía de uso del sistema.
- `design/tokens/kanam.tokens.json` - fuente de verdad.
- `projects/kanam-lab/design/propuestas/` - las propuestas que originaron los temas (Terrario,
  Plaza) y el manual de identidad PLAZA.
- `skills/frontend-ui-engineering` - anti-patrones y estándares de implementación.
- `docs/NORTH.md` - el sistema es la capa transversal "hilo" del norte de Kanam.
