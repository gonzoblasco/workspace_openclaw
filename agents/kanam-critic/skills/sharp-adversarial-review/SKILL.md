---
name: "sharp-adversarial-review"
description: "Presion adversarial sobre un entregable con la rubrica SHARP: cuando hay que emitir un veredicto de sustancia (VETO, Aprobado u ORO) con evidencia citable, cuando el autor declara que termino y falta el ultimo filtro, cuando un resultado 'funciona' pero nadie probo que resista, o cuando hay que devolver los puntos de friccion obligatorios en lugar de un elogio."
metadata:
  category: "Critic"
  tags:
    - critic
    - sharp
    - adversarial-review
    - quality
---

# sharp-adversarial-review

Ritual del Critic. No busca bugs de sintaxis ni estilos de variable: eso es del linter y de los
tests. Busca la fisura que separa lo funcional de lo excepcional, y la mide con una vara, no con
una impresión.

El estándar completo vive en `.knowledge/SHARP.md`. Esta skill es el **procedimiento** para
aplicarlo: cómo se puntea, qué cuenta como evidencia, cómo se emite el veredicto y qué se
devuelve al autor cuando no pasa.

## Cuando usarla

- Hay que evaluar la sustancia de un entregable (código, diseño, documento, decisión) y emitir
  un veredicto.
- El autor del trabajo declara que terminó; falta el filtro de sustancia antes de integrarlo.
- Un resultado "funciona" pero no hay prueba de que sea sostenible, robusto o elegante.
- Aparece un "todo bien" que convive con escenarios que nunca se corrieron.

No usarla para: revisar la superficie visual (eso es del Auditor de UI/UX), correr el linter, ni
buscar defectos puntuales de correctitud. El Critic mide **Gusto Técnico**, no forma ni bugs.

## Entrada: qué se evalúa

Se evalúa el **artefacto real**, no el relato del autor. Antes de puntuar:

1. **Leer el entregable completo.** Un veredicto sin lectura completa es ruido.
2. **Contrastar contra el objetivo original**, no contra lo que el autor decidió que era el
   objetivo.
3. **Verificar el estado en disco o en el repo** cuando el entregable es un cambio: el diff real
   (`git status`, `git diff`) manda sobre la descripción. Un reporte de "done" que el disco
   desmiente no se evalúa como done, se evalúa por lo que hay.

## Los 5 ejes (escala 1 a 5)

Cada eje se puntea con evidencia citable. Un puntaje sin la causa que lo respalda no entra.

| Eje | Mide | 1 | 5 |
|---|---|---|---|
| **S - Sharpness** | Precisión, ausencia de ruido | Difuso, redundante, lleno de muletillas de IA | Quirúrgico: cada palabra y cada línea tiene razón de existir |
| **H - Horizon** | Anticipación y sostenibilidad | Parche que crea deuda inmediata | Visión sistémica: resuelve y prepara la etapa siguiente |
| **A - Asymmetry** | Esfuerzo a valor | Sobre-ingeniería para un problema trivial | Palanca: cambio mínimo, impacto masivo |
| **R - Resistance** | Robustez y casos borde | Frágil: funciona solo en condiciones perfectas | Indestructible: anticipa fallos, es a prueba de errores humanos |
| **P - Parsimony** | Simplicidad elegante | Complejidad innecesaria, dependencias superfluas | Minimalismo: la solución más simple que resuelve el 100% |

**Formato de la evidencia.** Por eje: el puntaje, la causa concreta y su ubicación. Ejemplo:
"2 en Parsimonia: se agregaron tres capas de abstracción para una función de diez líneas
(`archivo.ext:42`)". El sentimiento es ruido; la rúbrica y la ruta son el hecho.

## Veredicto

Sumar los cinco ejes (máx 25) y clasificar:

| Total | Clasificación | Acción obligatoria |
|---|---|---|
| **0 - 12** | Mediocre | Rechazo. Re-diseño total. |
| **13 - 18** | Funcional | **VETO** en el pipeline: se devuelve al autor con puntos de fricción obligatorios. |
| **19 - 23** | Alta calidad | Aprobado con anotaciones de mejora. |
| **24 - 25** | Excepcional | **ORO**. Se documenta como Best Practice del sistema. |

El umbral del pipeline es `<= 18` es VETO. Un entregable funcional que no eleva el nivel no pasa:
"lo suficientemente bueno" es el enemigo de lo extraordinario.

**Sin evidencia no hay veredicto.** Si un eje no se puede puntuar porque falta información, se
declara el hueco y el veredicto queda bloqueado hasta cerrarlo, no se rellena con una impresión.

## Punto de fricción (el entregable del VETO)

Un veredicto sin la ruta a la mejora es ruido. Todo VETO devuelve **puntos de fricción
obligatorios**: cada uno con el eje que ataca, la causa, la ubicación y el ajuste concreto. El
Critic no arregla el trabajo: señala la fisura y cómo cerrarla; el autor corrige y vuelve.

## Contrato de evidencia (prestado de `skills/trust-vocabulary-report/SKILL.md`)

Cada afirmación del veredicto cita dónde está su evidencia. Distinguir siempre:

- **verificado** - se reproduce en el repo real.
- **parcial** - parte verificada; el hueco declarado.
- **auto-reportado** - solo lo dijo el autor; no se reprodujo.
- **bloqueado** - no se pudo verificar, y se dice por qué.

Una evaluación de sustancia **nunca** cierra sobre un solo auto-reporte.

## Guarda de verde falso (prestada de `skills/verification-gates/SKILL.md`)

Antes de aprobar, revisar que los gates no den un falso verde:

- **Cero casos corridos no es verde.** "Nada falló" cuando todo falló al correr no es éxito.
- **Un SKIP no es un OK.** Saltear un caso es un resultado declarado, no un aprobado.
- **Archivo ausente no es "vacío".** Un lector que no encuentra su entrada debe reportarlo, no
  devolver vacío.

Un entregable que aprueba sobre un falso verde es un VETO, no un aprobado.

## Deslinde con el Auditor (no pisar terreno)

- **El Auditor cubre la forma:** coherencia estética, tokens, accesibilidad, el "AI look".
- **El Critic cubre la sustancia:** arquitectura, sostenibilidad, gusto técnico.
- En conflicto, ambos exponen evidencia contra su estándar (`design/tokens.md` vs
  `.knowledge/SHARP.md`) y la síntesis la cierra el Core.

## Red Lines

- **Prohibido el optimismo.** No se aprueba "porque el autor se esforzó mucho". Solo la evidencia
  del resultado.
- **Prohibida la subjetividad.** Todo lo que no se pueda atar a un eje de SHARP se descarta.
- **No es un linter.** No gastar tiempo en espacios en blanco ni nombres de variables, salvo que
  afecten Sharpness o Parsimony.
- **No se aprueba con bloqueantes abiertos.** Un veredicto de aprobación con huecos abiertos es un
  reporte falso.

## Referencias

- Estándar completo: `.knowledge/SHARP.md`.
- Camino de madurez del sistema: `docs/NORTH.md`.
- Base metodológica prestada: `skills/verification-gates/SKILL.md`,
  `skills/trust-vocabulary-report/SKILL.md`.
- Review adversarial de código (dominio de dev, no del Critic):
  `agents/kanam-dev/skills/hermes-reviewer/SKILL.md`.

---

_El Critic no busca el error, busca la excelencia._
