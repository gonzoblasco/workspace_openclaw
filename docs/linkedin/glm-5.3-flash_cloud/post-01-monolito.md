# Post 1/8 - "Mi asistente dejó de ser uno"

Hace unos meses tenía un asistente de IA con un problema: sabía demasiado.

No es una metáfora. Cada vez que iniciaba una sesión, el sistema cargaba decenas de definiciones de skills (instrucciones de cómo hacer cada tipo de tarea) en la ventana de contexto del modelo. Cualquier cosa que le pidiera - escribir código, organizar mi memoria, preparar un deploy - arrastraba todo ese conocimiento, aunque el 90% fuera irrelevante para la tarea.

El resultado era predecible:

- Contexto saturado: el modelo procesaba ruido antes de llegar a lo importante.
- Más alucinaciones: con tanto material cargado, la probabilidad de confundir instrucciones crecía.
- Respuestas más lentas y caras: cada token irrelevante se paga.

Es el mismo problema que tiene cualquier sistema que crece sin rediseñarse: el monolito. Funciona hasta que deja de funcionar.

La solución no fue "un modelo más grande". Fue repensar la arquitectura: en lugar de un solo agente que lo sabe todo, un equipo de agentes especializados, cada uno con su propio entorno y solo las skills de su dominio.

Un cerebro que coordina. Cuatro especialistas que ejecutan. Una memoria compartida que une todo.

En los próximos posts voy a contar cómo funciona por dentro: el router que decide quién hace qué, los cuatro especialistas, la memoria colectiva, y lo que aprendí construyendo esto.

Primera lección, para dejarla desde el arranque: cuando tu asistente de IA se vuelve lento y confuso, el problema rara vez es el modelo. Suele ser la arquitectura.

#IA #Agentes #ArquitecturaDeSoftware #OpenSource #KanamOS