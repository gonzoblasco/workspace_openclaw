# Por qué no uso un prompt gigante

**Cuatro especialistas, cuatro contextos aislados: DEV, OPS, MIND y STUDIO**

Modelo: `deepseek-v4.1-flash:cloud` - Post 3 de la serie.

---

La tentación es escribir un prompt enorme con todo lo que sabés. Contexto, reglas, skills, ejemplos. "Así no se olvida de nada".

En realidad lográs lo contrario: un modelo saturado de información irrelevante para la tarea. Más contexto no es más inteligencia. Es más ruido.

Mi solución fue partir el trabajo en cuatro especialistas, cada uno en su propio workspace:

- 💻 **DEV** - ingeniería, producto, specs, TDD. Hoy carga 25 skills.
- 🛠️ **OPS** - infraestructura, gateway, seguridad, tooling. Carga 4.
- 🔍 **MIND** - conocimiento, research, aprendizaje. Carga 7.
- 🎨 **STUDIO** - comunicación, redacción, marca personal, OSS. Carga 7.

Fijate el número: DEV tiene 25 skills, OPS 4. Eso no es un desbalance, es la realidad de cada dominio. Y **ninguno arrastra las del otro**.

Cuando el CORE le pasa una tarea a DEV, DEV no carga las skills de redacción ni las de infraestructura. Carga lo suyo. Nada más.

El efecto es medible: menos tokens de arranque, respuestas más enfocadas, menos alucinación. El modelo deja de dispersarse.

Y hay un bonus: puedo agregar un especialista nuevo sin tocar la estabilidad del núcleo. Si mañana quiero un agente para ficción, no se rompe nada.

La especialización no es dividir por dividir. Es darle a cada tarea el contexto exacto que necesita. Ni más, ni menos.

¿Cuánto de tu prompt actual es ruido que tu modelo tiene que ignorar en cada respuesta?

---

_Serie: cómo funciona Kanam OS. Próximo post: la memoria compartida._
