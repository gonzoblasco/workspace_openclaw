# Post 8/8 - "Lo que aprendí construyendo un equipo de agentes"

Último post de la serie sobre Kanam OS. Cierro con lo que me llevo, incluyendo lo que haría distinto.

Lo que funcionó:

1. Un punto de entrada único. Toda conversación arranca en el Core. Cero ambigüedad sobre dónde vive cada cosa.
2. Dominios con límites duros. La pregunta "¿de quién es esta tarea?" tiene una sola respuesta correcta. Eso valió más que cualquier optimización de prompts.
3. Handovers estructurados. Cuatro campos fijos entre tareas eliminó el re-descubrimiento, que era mi mayor costo invisible.
4. Memoria compartida con RAG. Los agentes no cargan memoria: la consultan. Es lo que convierte cinco agentes en un equipo.

Lo que haría distinto:

1. Empecé por las skills y terminé por la arquitectura. El orden correcto es al revés: definir dominios y responsabilidades primero, y las skills después. La migración incluyó tirar skills obsoletas que existían solo porque el monolito las había acumulado.
2. Subestimé el costo de la delegación. Para tareas chicas, el overhead del despacho se nota. Un buen sistema necesita una vía rápida para lo trivial.
3. La coordinación entre agentes necesita más automatización de la que imaginé. El protocolo manual funciona, pero cada "el principal pide refuerzo" es un momento donde algo puede perderse. Siguiente iteración: hacerlo explícito en el sistema, no en la costumbre.

Lo que viene:

- Nuevos agentes especializados (la estructura está pensada para crecer sin tocar el núcleo).
- Más automatización del despacho y del handover.
- Y todo esto, eventualmente, documentado como arquitectura de referencia para quien quiera armar su propio sistema.

Si llegaste hasta acá: esta serie salió de la práctica, no de la teoría. Cada patrón que conté existe porque un problema real lo exigió.

Gracias por leerla. ¿Vos tenés un sistema de agentes? ¿Qué problema te está frenando?

#IA #Agentes #LessonsLearned #SoftwareArchitecture #KanamOS