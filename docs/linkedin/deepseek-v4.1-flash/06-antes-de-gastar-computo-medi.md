# Antes de gastar cómputo, medí

**Complexity scoring: cómo Kanam decide qué tarea merece qué esfuerzo**

Modelo: `deepseek-v4.1-flash:cloud` - Post 6 de la serie.

---

El error más caro del trabajo con IA no es usar el modelo equivocado. Es usar el modelo caro para todo.

Hay tareas que un modelo simple resuelve en segundos. Otras necesitan razonamiento profundo y varios agentes. Si tratás todo igual, pagás de más en lo trivial y arriesgás calidad en lo complejo.

En Kanam OS, antes de mover un solo agente, mido.

Un scorer evalúa cada tarea en cuatro dimensiones: alcance, abstracción, riesgo y ambigüedad. Devuelve un número de 1 a 20. Ese número decide el esfuerzo:

- **Bajo** - Kanam solo. Es trivial, no hace falta delegar.
- **Medio** - un agente, razonamiento alto.
- **Alto** - dos agentes con cross-review.
- **Crítico** - diseño del CORE, ejecución en paralelo, verificación obligatoria y tu confirmación.

El efecto es doble. Por un lado, ahorro real: la mayoría de las tareas no necesitan el tanque de guerra. Por el otro, disciplina: las tareas difíciles reciben el proceso completo, sin atajos por apuro.

Y hay un aprendizaje que me costó caro: **más razonamiento no es más calidad.** En algunos modelos, poner el nivel de pensamiento al máximo hacía que "filosofaran" en vez de resolver. El mejor output no venía del esfuerzo máximo, venía del esfuerzo correcto.

Medir antes de actuar no es burocracia. Es no pagar por músculo donde alcanzaba con cabeza.

¿Cuándo fue la última vez que mediste si tu tarea necesitaba realmente el modelo más caro?

---

_Serie: cómo funciona Kanam OS. Próximo post: la IA que no hace nada sin permiso._
