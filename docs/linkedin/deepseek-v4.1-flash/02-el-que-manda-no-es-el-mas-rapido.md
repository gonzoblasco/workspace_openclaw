# El que manda no es el más rápido: es el que sabe cuándo NO delegar

**Kanam CORE: el orquestador que se niega a hacer trabajo de otros**

Modelo: `deepseek-v4.1-flash:cloud` - Post 2 de la serie.

---

En un equipo de agentes, el error clásico es que el coordinador se ponga a trabajar.

Si el que orquesta también ejecuta, termina saturado, pierde la visión de conjunto, y las tareas operativas le comen la cabeza. Es el jefe que se pone a picar código y se olvida de que tenía que decidir la estrategia.

En Kanam OS lo resolví con una regla dura: **el CORE despacha, no ejecuta.**

El flujo es simple:

1. **Interpreta** la intención real del pedido.
2. **Selecciona** qué especialista tiene la skill necesaria.
3. **Delega** con un contexto de tarea acotado.
4. **Sintetiza** el resultado que vuelve del especialista.

Cuatro pasos. Ninguno es "hacer el trabajo".

¿Por qué importa? Porque el CORE cargado de detalles de implementación deja de ver el tablero. Y porque cada especialista, en su dominio restringido, es más preciso que el generalista.

Hay un detalle que casi nadie implementa: el **traspaso de contexto**. Cada especialista devuelve un bloque con qué hizo, en qué estado quedó el activo, qué falta, y las rutas de los archivos. Así el CORE no re-descubre lo que otro ya resolvió.

Delegar bien no es perder control. Es diseñar para no necesitar tener el control de todo.

¿Tu "orquestador" está orquestando, o está haciendo el trabajo que debería delegar?

---

_Serie: cómo funciona Kanam OS. Próximo post: los cuatro especialistas._
