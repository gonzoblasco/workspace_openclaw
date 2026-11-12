# Módulo 1 — De responder a hacer (0:02:38 - 0:22:01)

- Fuente: `../transcripcion.md` (rango 02:38 - 21:50), `../outline.md` § Módulo 1
- Claims externos verificados: ReAct (arXiv 2210.03629), Lost in the Middle (arXiv 2307.03172)

## Lo que enseña

El módulo no enseña «qué es un agente»: enseña **cuánto decide el modelo mientras corre, y qué precio se paga por eso.**

**1. La definición es por acción.** El mismo mensaje en un chatbot termina en una respuesta; en un agente sigue y emite el reembolso. El test del curso: *"Does it take real actions or only write text? Does the model choose the next step while it's running instead of following steps someone wrote in advance? And does it look at the results and change course?"* (05:34). Tres sí = agente.

**2. Workflow y agente son un rango, no dos cajas.** *"If a person wrote the steps ahead of time, and the model just fills in each one, that's a workflow. If the model chooses the next step while it's working, that's an agent."* (05:05). La línea es **quién escribe el próximo paso**. El loop es el *agentic loop*; el patrón conocido es ReAct (razona → actúa → observa).

**3. Cinco subsistemas como checklist, no como arquitectura.** Percepción (≠ grounding), razonamiento (incluye routing), acción (con aduana y aprobación humana), aprendizaje (adaptación en runtime, **no** reentrenar), comunicación (handoffs). *"These are useful capabilities to look for, not five boxes that every agent must have"* (06:48). En un diagrama real: modelo, tools, memoria, control loop, permisos.

**4. Multi-agente es un costo antes que un beneficio.** Empezar con uno. Escalar solo si el trabajo se parte, no cabe en un contexto, o hace falta revisión independiente. *"Splitting the work doesn't automatically improve the thinking."* (12:43). Costos: más llamadas, contexto perdido en handoffs, atribución de error difícil.

**5. Memoria en cuatro capas.** Short-term (la ventana), episodic (qué pasó y cuándo; los fallos valen doble), semantic (hechos sin fecha; vector DB es *herramienta*, no memoria), procedural (los pasos; autoactualizarlos sin revisión guarda juicios malos). **Memoria es lo que se guarda; contexto es lo que se arma para una llamada.** Diagnóstico de tres pasos cuando un agente olvida: ¿se guardó? ¿se encontró? ¿entró en el contexto?

**6. Lost in the Middle.** Un hecho enterrado en el medio de documentos largos se recupera peor que al principio o al final; graficado da una U. *"A long context doesn't guarantee the model uses every piece of it equally well. And a bigger context window doesn't automatically fix it."* (18:24). En agentes empeora: cada step agrega output y errores largos, y **una regla enterrada se ignora sin aviso** — la respuesta se degrada en silencio. Contramedidas: recortar, ordenar (fuerte primero, segundo al final), repetir la instrucción clave al final, menos y mejores piezas, partir documentos enormes.

## Lo que el curso no dice

- **Multi-agente no es solo un eje de arquitectura: es un eje de diagnóstico.** El costo real no es dinero, es **atribución de error**. Un auto-reporte de subagente no es un hecho; hay que ver el repo.
- **Lost in the middle permite confundir dos fracasos.** Cuando una skill bien escrita se ignora, la reacción es «la skill es mala». A veces la skill está bien y **quedó en el medio de un contexto grande**. Antes de reescribir un procedimiento: preguntar dónde estaba.

## Práctica — el ejercicio del módulo

Caso: **el cierre de sesión** (`skills/session-lifecycle/scripts/session-end.sh`), un flujo que hoy resuelve un agente.

| Subsistema | Qué hace hoy | ¿Existe? |
|---|---|---|
| Percepción | lee git status, archivos modificados, diálogo | Sí |
| Razonamiento | decide qué va al daily, al HANDOFF, qué fusionar | Sí |
| Acción | escribe daily, regenera HANDOFF, commitea | Sí |
| Aprendizaje | — no hay registro de qué falló en el cierre | **No** |
| Comunicación | el HANDOFF, mensaje a la próxima sesión | Sí |

**Hallazgo:** el paso 12 escrito en `video-transcription` el 2026-11-11 (`ADOPCION.md`, "el curso tiene que morder") es **exactamente el mecanismo de `learning` por reflection** del minuto 08:45: *"after a failure, the agent can write a short note about what went wrong and read it the next time."* Se escribió sin citar el curso y el curso lo nombra con el mismo nombre.

**Segunda brecha medida:** los parches automáticos de skills — 289 en `.archive/` entre el 27/10 y el 11/11 — no tienen ningún registro de cuáles funcionaron. Es `learning` ausente en el mismo sentido: se aplica el cambio, no se mide el resultado.

## Criterio de cierre

El módulo entrega un diagnóstico, no un gate. Su artefacto para el paso 12 todavía no está escrito: el candidato es un **registro de adopción de parches automáticos** (qué patch se aplicó, qué error decía corregir, si sobrevivió un uso real), que hoy no existe.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
