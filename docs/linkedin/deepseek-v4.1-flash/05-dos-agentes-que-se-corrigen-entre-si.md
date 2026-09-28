# Dos agentes que se corrigen entre sí

**El pipeline A/B: cuando la IA revisa la IA, y por qué no alcanza**

Modelo: `deepseek-v4.1-flash:cloud` - Post 5 de la serie.

---

Un solo agente escribiendo código tiene un problema estructural: no tiene con quién discutir.

Acepta su primera respuesta. No duda de sí mismo. Y los bugs entran sin que nadie los mire desde otro ángulo.

Por eso en Kanam OS el código no lo escribe un agente. Lo escribe un pipeline:

1. **Agente A escribe** la implementación.
2. **Agente B revisa** con ojo crítico, buscando lo que A no vio.
3. **Verificación** contra la fuente real: docs, API, el comportamiento del sistema.
4. **Iterar** alternando roles hasta que aguanta.

Lo interesante es lo que aprendí en el camino. Un agente revisando a otro **no es garantía**. B puede introducir sus propios bugs al "mejorar" algo que estaba bien.

La lección: el cross-review sirve, pero la verdad la decide la fuente externa, no el consenso entre agentes. Dos IAs de acuerdo no son una verificación. Son dos opiniones alineadas que pueden estar las dos equivocadas.

Por eso el paso 3 no es opcional. Verificar contra la realidad, no contra la confianza del modelo.

Esto es lo más contraintuitivo de todo el sistema: la parte más valiosa no es el agente que escribe, es el que se anima a decir "esto está mal".

Un equipo donde nadie disciente no es un equipo. Es un eco.

¿Quién revisa lo que tu IA produce, además de tu IA?

---

_Serie: cómo funciona Kanam OS. Próximo post: medir antes de gastar cómputo._
