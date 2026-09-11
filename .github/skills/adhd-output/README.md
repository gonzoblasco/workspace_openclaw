# ADHD Output

Formato de respuesta que no entierra la respuesta.

## Para que sirve?

Para cuando el agente te responde con tres parrafos de contexto antes de decirte que hacer. Este skill fuerza: **accion primero**, **pasos numerados**, **un next step concreto** al final.

## Cuando usarlo?

- Pedis "se directo", "sin vueltas", "accion primero"
- Sesion de debugging donde la respuesta esta enterrada en prosa
- Venis sobrecargado y necesitas el siguiente paso, no el analisis
- Reviews largos donde hay que separar hallazgo de accion

## Las 10 reglas

1. Liderar con la proxima accion
2. Numerar tareas multi-paso
3. Cerrar con un next step concreto
4. Suprimir tangentes
5. Restatear el estado cada turno
6. Time estimates en minutos
7. Hacer visibles las victorias
8. Errores matter-of-fact
9. Cap de listas a 5 items
10. Sin preambulo, sin recap, sin cierres

## Como se usa?

Es un skill de estilo, no de contenido. Se activa por pedido explicito o por contexto.

**Pedido explicito:**
> "Respondeme en formato ADHD"

**Por contexto:**
> "No puedo arrancar con este bug. Que hago?"

## Antes / despues

**Antes:**
> Gran pregunta! Tu flujo de auth tiene varias piezas. Mirando src/auth.ts, la funcion verifyToken parece usar una API vieja... Espero que ayude!

**Despues:**
> Correr `npm install jsonwebtoken@latest`, despues editar `src/auth.ts:42`.
>
> 1. Abrir `src/auth.ts`
> 2. Reemplazar `verifyToken` (42-58)
> 3. Correr `npm test -- auth.spec.ts`
>
> Next: pegame la primera linea del test que falla.

## Diferencia con `adhd-assistant`

| Skill | Que hace |
|---|---|
| `adhd-assistant` | Sistema de vida: planificar, desglosar, body doubling |
| `adhd-output` | Formato de la respuesta: como se comunica |

Complementarios. Uno puede estar activo sin el otro.

## Archivos

| Archivo | Que contiene |
|---|---|
| `references/rules.md` | Las 10 reglas en detalle, con racional y contraejemplos |
| `references/adaptations.md` | Que se cambio respecto al original de ayghri y por que |
| `templates/response.md` | Plantillas de respuesta + checklist de salida |
| `scripts/check-output.sh` | Lint heuristico: preambulo, cierres, disculpas, em dash, listas largas |

## Uso del script

```bash
skills/adhd-output/scripts/check-output.sh respuesta.md
echo "Gran pregunta! ..." | skills/adhd-output/scripts/check-output.sh
```

## Skills relacionadas

- [adhd-assistant](../adhd-assistant) - Sistema de vida y planificacion
- [anti-ai](../anti-ai) - Limpieza de modismos de IA
- [session-lifecycle](../session-lifecycle) - Estructura de sesiones

## Credito

Basado en [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd) (MIT), adaptado al workspace de Kanam.
