# Post 2 - El orquestador que no ejecuta nada: cómo Kanam OS decide quién hace qué

Mi agente principal no escribe código. No deploya. No investiga. No redacta. Y sin embargo, todo funciona.

Su único trabajo real es saber quién sabe hacer cada cosa.

**El patrón Router aplicado a agentes**

En Kanam OS, el agente CORE opera bajo una regla estricta: nunca ejecuta tareas de especialidad. Despacha. El flujo siempre es el mismo, en cuatro pasos:

1. **Interpretación** - el CORE identifica la intención del usuario.
2. **Selección** - determina qué agente posee la skill necesaria.
3. **Delegación** - invoca al especialista con un prompt de contexto de tarea, mínimo y específico.
4. **Retorno** - el especialista ejecuta y devuelve el resultado al CORE, que sintetiza la respuesta final.

**La tabla de especialidades**

La decisión de a quién delegar no es improvisada. Hay un criterio explícito:

- Código, validación de specs, refactorización: va a **DEV**.
- Deploy, CI/CD, configuración de entorno: va a **OPS**.
- Análisis de corpus, minería de datos, resúmenes: va a **MIND**.
- Diseño, narrativa, generación de activos: va a **STUDIO**.

**Por qué esto importa más de lo que parece**

Sin un protocolo explícito, multi-agente se convierte en multi-caos: agentes que se pisan, tareas ejecutadas dos veces, contextos que se pierden.

El protocolo de despacho hace dos cosas al mismo tiempo:

- Le quita al CORE el peso de procesar detalles de implementación. Mantiene visión de alto nivel.
- Le da a cada especialista autonomía operativa dentro de su dominio. Nadie le dice a DEV cómo refactorizar; solo le dice qué tiene que lograr.

**Lo que protege el sistema**

Hay una regla de validación interesante que estamos implementando: si el CORE intenta ejecutar directamente una tarea que corresponde a un especialista, el sistema alerta. La tarea debe ser delegada.

Suena burocrático. Es lo contrario: es lo que evita que el orquestador se convierta de nuevo en un generalista saturado.

**El problema que falta resolver**

Todo esto funciona cuando una tarea es de un solo especialista. ¿Qué pasa cuando DEV termina un refactor pero OPS necesita deployarlo y MIND tiene que actualizar la memoria del proyecto?

Ahí entra el Context Handover. La próxima semana: cómo los agentes se pasan la posta sin perder información.

#AI #MultiAgent #SoftwareArchitecture #LLM #KanamOS

---
*Fuente: ADR-074 (Protocolo de Despacho y Coordinación Multi-Agente).*
