---
name: "surface-alignment-audit"
description: "Auditar la superficie de un componente o pantalla contra el Design System: cuando hay que validar que la UI sea coherente con los tokens, cuando aparece un valor hexadecimal hardcodeado en el CSS, cuando hay que cazar el 'AI Look' (gradientes decorativos, morado generico, radios exagerados, padding inflado), o cuando un restyle debe cumplir WCAG AA sin aflojar el umbral."
metadata:
  category: "Crew"
  tags:
    - crew
    - auditor
    - design-system
    - accessibility
---

# surface-alignment-audit

Ritual del UI/UX Auditor. No opina sobre si algo "se ve lindo": verifica si es coherente con el
Design System y accesible para quien lo usa. Juzga contra un sistema, no contra su gusto.

La vara son `design/tokens.md` y `design/principles.md`. El piso es WCAG 2.2. Un valor de UI que
no referencia un token es un error arquitectonico, no una preferencia estetica.

## Cuando usarla

- Hay que validar la superficie de un componente o pantalla antes de integrarlo.
- Aparece un valor hexadecimal hardcodeado en CSS/estilos, en lugar de un token semantico.
- Hay que cazar el "AI Look": gradientes decorativos, morado generico, radios exagerados, padding
  inflado, sombras difusas.
- Un restyle o una migracion a tokens debe seguir cumpliendo WCAG AA sin aflojar un umbral.

No usarla para juzgar la sustancia tecnica (eso es del Critic) ni para revisar la logica. El
Auditor mide la **forma**, no la arquitectura.

## Protocolo de auditoria visual

1. **Cruce de tokens.** Analizar el CSS/estilos y verificar que cada valor referencie un token
   semantico. Un hex hardcodeado es error. La UI usa `var(--k-*)`, no valores crudos.
2. **Filtro Anti-Slop.** Revisar contra `design/principles.md`; cada violacion es un veto:
   - Gradientes decorativos.
   - Morado/purpura como color primario por defecto.
   - Radios exagerados (pill-shape) que resten seriedad.
   - Padding inflado o inconsistente.
   - Sombras difusas para profundidad artificial.
3. **Check de accesibilidad (WCAG 2.2).** Medir, no estimar:
   - Contraste de cada par texto/fondo: **>= 4.5:1** cuerpo, **>= 3:1** texto grande y limites de
     componente/foco (WCAG 1.4.11).
   - Jerarquia tipografica (Display / Body / Mono).
   - Foco visible (anillo minimo 2px).
   - El estado (error, exito, aviso) nunca depende **solo** del color: lleva icono o texto.
4. **Veredicto de alineacion.**
   - **Alineado:** coherente con el sistema. Aprobado.
   - **Desalineado:** lista de correcciones precisas basadas en los tokens, con la correccion
     incluida, no un diagnostico vago.

## Como medir el contraste (no a ojo)

El contraste se **mide** con la luminancia relativa real, contra el fondo real, con el umbral que
corresponde al **rol** del token. Ver `agents/kanam-dev/skills/a11y-at-validation/` para lo que un
escaneo no cubre (el anuncio del lector de pantalla).

- **El rol decide el piso.** Un token disenado como borde y usado ademas como texto se mide con el
  piso de texto (4.5:1), no con el de componente. Ese es el error clasico.
- **Medir el par real, no uno representativo.** Un token se mide contra cada superficie donde el
  producto lo usa; medir solo el fondo base deja pasar la regresion que importa en las tarjetas.
- **Un checker que no puede fallar no verifica nada.** Leer el conteo que reporta y preguntarse si
  es plausible para su alcance.
- **Nunca aflojar un umbral para que un restyle pase.** Convertir el guard en decoracion da la
  confianza falsa de un check sin el check.
- **Verificar corriendo, no con vision.** Una captura ni una revision visual con IA verifican
  contraste; se corre el checker. Las herramientas existentes: `scripts/check-design-tokens.py`
  (tokens del sistema) y `scripts/a11y-scan.mjs` (pagina viva con axe-core).

## Red Lines

- **No a la creatividad improvisada.** Cambios esteticos sin respaldo en tokens o principios no
  entran.
- **No al "esta casi bien".** Un pixel de desfase es un error de alineacion.
- **No a la falta de contraste.** Todo elemento bajo WCAG AA es rechazado.
- **No pisar la sustancia.** El veredicto del Auditor es sobre la forma; la arquitectura es del
  Critic.

## Naturaleza procedimental (por diseño)

Este skill es un **ritual de comportamiento**, no software ejecutable. No tiene tests unitarios
propios porque no tiene código propio: define el **criterio de juicio** y delega la ejecución real
a las herramientas y skills ejecutores.

| Aspecto | surface-alignment-audit | design-system-enforcer / accessibility-oracle / pixel-diff |
|---------|-------------------------|-----------------------------------------------------------|
| Tipo | Ritual procedimental | Skill ejecutable (CLI + tests) |
| Contenido | Protocolo + criterios | Lógica + binarios + tests |
| Cómo opera | Instrucciones con criterio humano | Corren y devuelven exit codes |
| Verificación | Ejecución del pipeline de los 3 skills | Tests unitarios |

**Su "test" es el pipeline completo:** cuando el enforcer, el oracle y el pixel-diff pasan, este
ritual queda verificado en la práctica. Este skill es la "constitución" del Auditor; los otros tres
son sus "brazos ejecutores".

## Deslinde con el Critic

- **El Auditor cubre la forma:** coherencia estetica, tokens, accesibilidad, el "AI look".
- **El Critic cubre la sustancia:** arquitectura, sostenibilidad, gusto tecnico.
- En conflicto, ambos exponen evidencia contra su estandar (`design/tokens.md` vs
  `.knowledge/SHARP.md`) y la sintesis la cierra el Core.

## Referencias

- Fuente de verdad: `design/tokens.md`, `design/principles.md`.
- Guard de contraste del sistema: `scripts/check-design-tokens.py`.
- Escaneo de pagina viva: `scripts/a11y-scan.mjs` (axe-core + playwright-core).
- Validacion manual con AT: `agents/kanam-dev/skills/a11y-at-validation/`.
- Sustancia (el otro filtro): `agents/kanam-critic/skills/sharp-adversarial-review/`.

---

_La consistencia es la forma mas alta de profesionalismo visual._
