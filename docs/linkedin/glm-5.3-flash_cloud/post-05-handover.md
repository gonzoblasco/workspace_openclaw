# Post 5/8 - "El Context Handover: el arte de no repetir trabajo"

En sistemas de agentes, hay un costo invisible que nadie te cuenta: el re-descubrimiento.

Si el agente A termina una tarea y el agente B la retoma al día siguiente sin saber qué se hizo, pasa una de dos: o B vuelve a investigar desde cero (tokens y tiempo tirados), o B asume cosas que no son ciertas (bugs sutiles). Ambos escenarios los viví antes de formalizar una solución.

La solución es simple y es un contrato: cada tarea que termina debe incluir un bloque de Context Handover con cuatro campos fijos:

- Summary: qué se logró, en una o dos líneas.
- Status: estado actual del activo (Draft, Ready, Merged...).
- Next Steps: qué falta para completar.
- Resources: rutas a los archivos creados o modificados.

Nada de resúmenes creativos de párrafos. Campos fijos, siempre los mismos, legibles por otro agente sin ambigüedad.

Por qué funciona:

1. Elimina la ambigüedad: "casi listo" no es un estado; "Ready" sí.
2. Hace auditable el trabajo: podés reconstruir la historia de cualquier tarea leyendo los handovers.
3. Permite el salto entre agentes: MIND puede retomar donde DEV dejó, sin preguntar nada.

Es la misma idea que usan los equipos humanos serios: handoffs estructurados entre turnos, ADRs, runbooks. La diferencia es que aquí el lector es otro agente, así que el formato tiene que ser determinista.

Regla que aplico ahora en todo: si una tarea no puede resumirse en esos cuatro campos, probablemente está mal definida desde el inicio.

#IA #Agentes #Workflow #DevTools #KanamOS