# Post 6/8 - "Cuando DEV necesita a OPS: coordinación multi-agente"

Todo lindo hasta que una tarea no le pertenece a un solo especialista.

Ejemplo real: terminar una feature no es solo escribir código. Es código (DEV) + deploy y configuración de CI (OPS) + quizás documentación (STUDIO). ¿Quién manda? ¿Cómo se coordinan sin caos?

El protocolo que uso tiene una regla central: siempre hay un especialista principal, y los refuerzos se piden, no se imponen.

El flujo:

1. El Core identifica la tarea primaria (en el ejemplo, es una tarea de código: DEV lidera).
2. Delega al especialista principal.
3. El principal identifica si necesita apoyo de otro (ej: "esto requiere un deploy, necesito a OPS").
4. El Core coordina la intervención del segundo agente.

La diferencia con otros enfoques es sutil pero importante: no es el Core adivinando todas las dependencias por adelantado. Es el especialista - el que tiene el contexto técnico de la tarea - quien declara qué necesita.

Porque en la práctica, quien está escribiendo el código sabe mejor que nadie si su fix requiere tocar la infraestructura. El Core no tiene por qué saberlo: solo tiene que saber a quién preguntarle.

Lo que esto resuelve:

- Dependencias ocultas que aparecen tarde y rompen plazos.
- El anti-patrón del "todo lo coordina el centro", que convierte al orquestador en cuello de botella.
- Responsabilidades claras: si algo se rompe entre dos dominios, el handover (post anterior) muestra exactamente quién tocó qué.

Multi-agente no es "muchos agentes corriendo en paralelo". Es un sistema de responsabilidades con un protocolo de cooperación.

#IA #Agentes #SoftwareArchitecture #DevOps #KanamOS