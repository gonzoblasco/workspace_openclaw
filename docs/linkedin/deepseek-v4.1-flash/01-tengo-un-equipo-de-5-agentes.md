# Tengo un equipo de 5 agentes. Yo soy uno de ellos.

**Presentando Kanam OS: de un asistente generalista a un sistema de especialistas**

Modelo: `deepseek-v4.1-flash:cloud` - Post 1 de la serie.

---

Hasta hace poco usaba la IA así: abría un chat, escribía un prompt gigante, y rezaba.

El problema no era el modelo. Era que le pedía todo a la vez. Que programe, que recuerde, que investigue, que escriba. Un generalista saturado.

Entonces dejé de tener "un asistente" y construí un equipo.

Kanam OS son cinco roles con su propio espacio de trabajo aislado:

- 🌿 **CORE** - orquesta, guarda la memoria global y toma las decisiones de estrategia.
- 💻 **DEV** - código, specs, refactors.
- 🛠️ **OPS** - infraestructura, gateway, seguridad.
- 🔍 **MIND** - investigación y conocimiento.
- 🎨 **STUDIO** - redacción, comunicación, marca.

La regla que cambió todo: **el CORE no ejecuta tareas de ejecución. Las despacha.**

Interpreta la intención, elige al especialista que tiene la skill necesaria, le pasa un contexto acotado, y el especialista devuelve el resultado. El CORE sintetiza.

El resultado: cada agente carga solo las skills de su dominio. DEV hoy tiene 25 skills, OPS 4. Ninguno arrastra el ruido de los demás. Menos contexto basura, menos alucinación, más foco.

No es magia ni "una IA que hace todo". Es diseño de sistema: roles claros, contextos aislados, handoffs explícitos.

La pregunta no es cuánto sabe tu modelo. Es **cómo está organizado tu equipo**.

¿Cuántos "agentes" tenés sin darte cuenta, todos metidos en un solo prompt?

---

_Serie: cómo funciona Kanam OS. Próximo post: el CORE como orquestador._
