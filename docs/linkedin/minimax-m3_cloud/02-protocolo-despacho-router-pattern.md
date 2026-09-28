# Art. 2 - Cómo Kanam OS Despacha Tareas entre Agentes Especializados

> **Fuente:** ADR-074 (Protocolo de Despacho Multi-Agente)
> **Audiencia:** LinkedIn semanal - público técnico general
> **Formato:** post listo para pegar (≈ 2.200 caracteres)

---

## Versión LinkedIn (cuerpo del post)

Ya tenemos cinco cerebros. El problema ahora es otro: ¿quién habla con quién?

Si cada agente pudiera invocar cualquier otro, terminamos con un caos de idas y vueltas, contexto duplicado y un CORE saturado de detalles que no le corresponden.

La respuesta fue un protocolo explícito: el Router Pattern (ADR-074).

El CORE no ejecuta tareas de ejecución. Solo despacha.

El flujo es siempre el mismo, en cuatro pasos:

1. **Interpretación.** El CORE lee la intención del usuario. Si la tarea es ambigua, pregunta. Si es clara, sigue.
2. **Selección de especialista.** El CORE consulta su mapa de orquestación (derivado del antiguo `SKILLS-INDEX.md`) y elige el agente dueño de la skill.
3. **Delegación.** El CORE invoca al especialista - vía `sessions_spawn` para trabajo aislado, o `sessions_send` para turnos conversacionales - con un bloque de "Contexto de Tarea".
4. **Retorno.** El especialista termina y devuelve un "Context Handover": qué se hizo, estado actual, qué falta, dónde quedó el trabajo.

Ese handover es la pieza clave. Sin él, el siguiente especialista (o el CORE en una próxima sesión) tiene que re-descubrir todo de cero.

Cuando una tarea cruza dos especialidades - por ejemplo, "implementá esta feature" + "desplegala" - el protocolo define un orden: el CORE identifica la tarea primaria, delega al especialista principal, y le pide a ese especialista que solicite apoyo si lo necesita. El CORE vuelve a coordinar, pero no ejecuta nada.

El CORE mantiene así una visión de alto nivel. Los especialistas conservan autonomía operativa dentro de su dominio.

Y lo más importante: si el CORE intenta ejecutar algo que claramente corresponde a DEV, el sistema lo detecta y le avisa que debe delegar.

No es burocracia. Es una forma de mantener la cabeza fría cuando el sistema crece.

---

## Notas técnicas (no publicar)

- **Origen del flujo:** Router Pattern clásico aplicado a multi-agente.
- **Herramientas nativas mencionadas:** `sessions_spawn` (delega con contexto aislado) y `sessions_send` (delega conservando el hilo conversacional).
- **Bloque Context Handover - cuatro campos:** Summary, Status, Next Steps, Resources.
- **Por qué evitar "re-descubrimiento":** ahorra tokens, baja latencia, y mantiene la coherencia entre sesiones (cada sesión arranca sin memoria in-process).
- **Validación pendiente en el ADR:** "si el CORE intenta ejecutar una tarea de DEV directamente, el sistema debe alertar". Todavía no implementado al momento de escribir esto.
- **Para DEV/OPS de la audiencia:** este patrón se parece mucho a "API Gateway + microservicios", pero el contrato es un prompt, no un JSON Schema.

---

## Hashtags sugeridos

```
#MultiAgente #ArquitecturaDeSoftware #PatronesDeDiseño #LLM #IngenieríaDeSoftware #IA
```

---

## Por qué este post va segundo

El artículo 1 instaló la duda existencial. Este la cierra con un mecanismo concreto: el despacho. Una vez que entiendes el flujo, el resto (los 5 cerebros, la memoria compartida) tiene sentido.

Si tuvieras que explicar la serie en una sola imagen, este es el diagrama de flujo.
