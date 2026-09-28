# Post 2/8 - "El Router Pattern: mi asistente ya no ejecuta, despacha"

Siguiendo con la serie sobre cómo funciona Kanam OS por dentro.

La decisión de diseño más contraintuitiva que tomé: el agente central (Kanam CORE) no ejecuta casi nada. Su trabajo es otro: decidir quién ejecuta.

El flujo es un patrón clásico de software, el Router:

1. Interpretación: el Core identifica la intención de lo que le pido.
2. Selección: identifica qué agente especialista tiene la skill necesaria.
3. Delegación: le pasa la tarea con un "Contexto de Tarea" (qué se pide, qué se espera, qué ya existe).
4. Retorno: el especialista ejecuta y devuelve el resultado; el Core sintetiza.

¿Por qué no dejar que el Core haga todo? Por la misma razón que un tech lead no escribe todo el código de un sprint: si el que orquesta también implementa, se satura, pierde la vista del conjunto y todo se vuelve más lento.

El beneficio silencioso es el foco. Cada especialista opera en un dominio acotado, con su propio prompt, sus propias skills y menos ruido. Menos contexto irrelevante = menos alucinaciones, respuestas más precisas.

¿El costo? Una capa extra de comunicación. Cada delegación agrega latencia. Es el trade-off de siempre: velocidad individual vs. sistema que escala.

Y una regla que me gustó más de lo que esperaba: si el Core intenta ejecutar una tarea de desarrollo directamente, el sistema lo alerta. La delegación no es opcional, es el contrato.

#IA #Agentes #SoftwareArchitecture #LLM #KanamOS