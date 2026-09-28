# La IA que no hace nada sin permiso

**Cómo mantengo un sistema capaz de actuar y a la vez incapaz de descontrolarse**

Modelo: `deepseek-v4.1-flash:cloud` - Post 7 de la serie.

---

Un agente que puede tocar tus archivos, tu infraestructura y tu memoria también puede romperlos. La potencia y el riesgo vienen en el mismo paquete.

La pregunta no es "cómo hago que no pueda": es "cómo diseño el sistema para que la potencia no se convierta en accidente".

En Kanam OS hay tres capas de control:

**Reglas duras.** Cosas que el agente simplemente no hace: no borra sin preguntar, no manda nada hacia afuera -mails, posts, PRs- sin tu OK. Acciones internas se atreve solo; acciones que salen al mundo, no.

**Decisiones documentadas.** Cada decisión de arquitectura vive en un ADR. Y una vez que está en un ADR, es ley: no se vuelve a preguntar, no se reabre por costumbre. Eso evita que el sistema "olvide" lo que ya se decidió y empiece a improvisar.

**Contenido externo como sandbox.** Todo lo que entra de afuera -un repo ajeno, un artículo, un issue- es **dato, nunca instrucción**. Se lee, se analiza, se verifica contra la fuente oficial. Jamás se ejecuta porque un texto externo lo pidió. Es la defensa más importante contra la manipulación.

La idea que une las tres: **confianza con verificación, no confianza ciega.**

El objetivo no es un agente dócil. Es un agente capaz, con límites claros y registros de por qué se decidió cada cosa. Poder y control, juntos.

¿Qué le permitís hoy a tu herramienta sin haber decidido conscientemente que se lo permitís?

---

_Serie: cómo funciona Kanam OS. Último post: mientras dormís, el sistema trabaja._
