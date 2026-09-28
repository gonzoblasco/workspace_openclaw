# Mientras dormís, el sistema trabaja

**Skills reutilizables y automatizaciones: cómo Kanam OS escala sin vos**

Modelo: `deepseek-v4.1-flash:cloud` - Post 8 de la serie.

---

Un equipo de agentes que solo funciona cuando estás mirando no es un equipo. Es una herramienta.

La diferencia entre las dos es lo que pasa cuando no estás.

En Kanam OS hay dos mecanismos que hacen que el sistema trabaje solo:

**Skills reutilizables.** En vez de repetir instrucciones cada vez, cada capacidad está escrita como un procedimiento guardado. "Cómo hago un cierre de sesión", "cómo sanitizo un repo antes de publicarlo", "cómo reviso un PR ajeno". El agente no improvisa cada vez: sigue el procedimiento probado. Y esos procedimientos se versionan, se corrigen, mejoran con el uso.

**Automatizaciones.** Tareas que se disparan solas: un chequeo periódico de estado, un recordatorio, un resumen semanal que se genera sin que lo pidas. El sistema se despierta, hace su trabajo, y te avisa solo si hay algo que merece tu atención.

Hay un principio que aprendí a cuidar: **no automatizar el silencio.** Un sistema que te avisa por todo es tan inútil como uno que no te avisa nunca. La gracia está en que hable cuando importa y cierre cuando no.

La meta no es delegar y olvidarme. Es diseñar procesos que trabajan bien sin mi presencia, y que me devuelven el resultado, no la carga.

Empecé este recorrido con un asistente que arrancaba de cero cada chat. Lo termino con un sistema que recuerda, delega, se verifica, se controla y sigue andando cuando bajo la tapa.

Eso, para mí, es dejar de usar la IA como chat y empezar a usarla como infraestructura.

¿Qué de tu trabajo repetitivo todavía depende de que vos estés ahí para que pase?

---

_Serie completa: cómo funciona Kanam OS, en 8 posts. Gracias por leer._
