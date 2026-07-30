---
name: "session-lifecycle"
metadata:
  category: "Workflow"
  tags:
    - sesion
    - ciclo
    - productividad
description: "Workflow de Session Lifecycle: ciclo de sesión completo. Reemplaza 4 skills de sesión."
user-invocable: false
---

# Workflow: Session Lifecycle

## Skills que reemplaza
- `session-closure`
- `session-closure-ritual`
- `context-management`
- `agent-dispatcher`

## Propósito
Gestión del ciclo de vida completo de una sesión de trabajo con IA.

## Cuándo usarlo
- Al iniciar una sesión de trabajo con IA (cargar contexto + memoria)
- Al cerrar una sesión (escribir HANDOFF, memory, CHANGELOG)
- Para spawnear sub-agentes según la tarea (fork vs isolated)
- Para convertir pendientes en tareas accionables y hacer commit del workspace

## Fases
1. **Inicio** — cargar contexto, memoria, handoff del proyecto activo
2. **Dispatcher** — spawnear sub-agentes según la tarea:
   - **fork**: cuando el sub-agente necesita el transcript actual (ej: continuar una investigación, analizar una conversación)
   - **isolated**: cuando es trabajo independiente (ej: buscar issues, leer docs, hacer tareas paralelas sin contexto compartido)
3. **Ejecución** — trabajo principal, decisiones, archivos tocados
4. **Cierre** — escanear sesión, escribir HANDOFF, memory, CHANGELOG
   - **Revisar sesiones anteriores del día:** antes de cerrar, leer los archivos `memory/YYYY-MM-DD-*.md` del día para asegurarse de que no hubo sesiones previas que el daily note resumido no capture. No confiar solo en el daily note ni en la memoria.
   - **Consolidar archivos sueltos del día:** si hay archivos `memory/YYYY-MM-DD-HHMM.md` (sesiones individuales), moverlos a `memory/archive/`. El daily consolidado `memory/YYYY-MM-DD.md` ya tiene toda la info.
   - **Self-reflection obligatoria:** si hubo correcciones de Gonzo, cambios estructurales, o aprendizajes significativos, registrar en LEARNINGS.md antes de cerrar. No esperar a que Gonzo pregunte "¿revisamos lecciones?"
   - Si se modificó CONTRIBUTING.md, skills, o AGENTS.md, verificar que el cambio esté completo y no falten adaptaciones en skills relacionadas
5. **Tareas** — convertir pendientes en tareas accionables. Crear cron jobs para follow-ups, o escribir en TODO.md del proyecto. No dejar pendientes en el aire
6. **Commit** — commit + push del workspace (después de HANDOFF y memory, no antes)

## Self-Reflection Post-Tarea

Después de tareas significativas (multi-step, debugging, PRs, cambios de config), hacer una pausa rápida de evaluación:

```
CONTEXT: [tipo de tarea]
REFLECTION: [qué noté]
LESSON: [qué haría distinto]
BIASES DETECTED: [sunk cost / anchoring / confirmation / etc. o none]
```

**Cuándo hacerlo:**
- Después de completar una tarea multi-step
- Después de recibir feedback (positivo o negativo)
- Después de fixear un bug
- Cuando notes que tu output podría ser mejor

**Destino:** si es una lección nueva → `docs/LEARNINGS.md`. Si es un patrón que ya existe → actualizar Recurrence-Count.

## WAL Protocol — Write-Ahead Logging

**Regla de oro:** si es importante recordarlo, ESCRIBILO AHORA — no después. El contexto desaparece. El archivo queda.

### Escaneá cada mensaje en busca de:
- ✏️ **Correcciones** — "Es X, no Y" / "En realidad..." / "No, quise decir..."
- 📍 **Nombres propios** — personas, lugares, empresas, productos
- 🎨 **Preferencias** — colores, estilos, approaches, "me gusta/no me gusta"
- 📋 **Decisiones** — "Hagamos X" / "Vamos con Y" / "Usá Z"
- 📝 **Cambios a drafts** — ediciones a algo que estamos trabajando
- 🔢 **Valores específicos** — números, fechas, IDs, URLs

### El Protocolo

Si APARECE ALGUNO de estos:

1. **STOP** — No empieces a redactar tu respuesta
2. **WRITE** — Actualizá `memory/YYYY-MM-DD.md` o el archivo relevante con el detalle
3. **THEN** — Respondé a Gonzo

El impulso de responder es el enemigo. El detalle se siente tan claro en contexto que parece innecesario escribirlo. Pero el contexto se va a perder. Escribí primero.

**Ejemplo:**

Gonzo dice: "Usá el tema azul, no el rojo"

❌ MAL: "Dale, azul!" (parece obvio, para qué escribirlo)
✅ BIEN: Escribir a `memory/YYYY-MM-DD.md`: "Tema: azul (no rojo)" → LUEGO responder

## Working Buffer — Zona de Peligro

Cuando el contexto de sesión llegue al ~60% (verificable con `session_status`), activar el buffer:

1. Crear o limpiar `memory/working-buffer.md`
2. A partir de ese punto, **cada exchange** se loggea: mensaje de Gonzo + resumen de tu respuesta
3. Después de compactación, leer el buffer primero antes de cualquier otra cosa

**Formato:**

```markdown
# Working Buffer
**Status:** ACTIVE
**Started:** 2026-07-22T12:00:00-03:00

---

## 2026-07-22T12:01:00 Gonzo
[mensaje]

## 2026-07-22T12:01:05 Kanam (resumen)
[1-2 oraciones con detalles clave]
```

## Compaction Recovery

Si despertás sin contexto (compactación, reinicio, o Gonzo dice "dónde estábamos?"):

1. **Leer** `memory/working-buffer.md` — exchanges crudos de la zona de peligro
2. **Leer** `memory/YYYY-MM-DD.md` del día de hoy y ayer
3. **Search** `memory_search()` por contexto faltante
4. **Extraer** lo importante del buffer a `memory/YYYY-MM-DD.md`
5. **Presentar:** "Recuperado del working buffer. Última tarea era X. ¿Continuamos?"

No preguntar "de qué estábamos hablando?" — el buffer tiene la conversación.

## Handoff entre Subagentes

Cuando un subagente pasa trabajo a otro (o devuelve resultados al main), el handoff debe incluir:

- **Qué se hizo** — resumen de cambios/output
- **Dónde están los artifacts** — rutas exactas de archivos
- **Cómo verificar** — comandos de test o criterios de aceptación
- **Issues conocidos** — todo lo que está incompleto o riesgoso
- **Qué sigue** — próxima acción clara para el agente receptor

**Mal handoff:** "Listo, revisá los archivos."
**Buen handoff:** "Construí el módulo de auth en /shared/artifacts/auth/. Corré `npm test auth` para verificar. Issue conocido: rate limiting no implementado todavía. Siguiente: reviewer checkea edge cases de error handling."

**Lección:** un handoff vago genera trabajo duplicado o errores. Ser explícito sobre qué se hizo, dónde está, y qué falta ahorra tiempo a ambos lados.

## Productividad & ADHD — Cómo Trabajamos

Gonzo tiene ADHD. El sistema de productividad debe adaptarse a eso, no al revés.

### Principios

- **Una cosa a la vez.** No mezclar proyectos en una misma sesión. Cada sesión de OpenClaw = un proyecto.
- **Inbox capture.** Si a Gonzo se le ocurre algo mientras trabajamos en otra cosa, lo atrapo en `inbox.md` y sigo con lo que estábamos.
- **Overload triage.** Si hay demasiadas cosas abiertas, parar y priorizar antes de seguir. Preguntar: "¿Qué es lo más importante AHORA?"
- **Rutinas de inicio.** Al arrancar una sesión, revisar qué quedó pendiente de la sesión anterior antes de meter cosas nuevas.
- **Rutinas de cierre.** Al terminar una sesión, dejar claro qué sigue para la próxima. Así Gonzo no pierde 10 min retomando.
- **Focus > multitasking.** Una sesión enfocada de 2h vale más que 4h de contexto switching.
- **Sin culpa por lo no hecho.** Si algo quedó sin terminar, se retoma. No hay "debería haber hecho más".

### Señales de sobrecarga

Si detecto alguna de estas, paro y pregunto antes de seguir:
- Gonzo menciona 3+ proyectos diferentes en la misma conversación
- Hay tareas abiertas de sesiones anteriores sin resolver
- El daily log del día tiene entradas de 3+ temas distintos
- Gonzo dice "estoy en mil cosas" o similar

### Cómo Ayudo

- **Recordatorio suave:** "Antes de arrancar con esto, acordate que tenías X pendiente de ayer. ¿Seguimos con eso o arrancamos nuevo?"
- **Triage rápido:** "Tenés 4 cosas abiertas. ¿Cuál es la prioritaria ahora?"
- **Cierre explícito:** Al final de cada sesión, dejo un resumen de qué se hizo y qué sigue.
- **Sin presión:** Si Gonzo quiere cambiar de tema, cambiamos. El sistema se adapta.

## Outputs
- `projects/<slug>/.knowledge/HANDOFF.md`
- `memory/YYYY-MM-DD.md`
- Tareas creadas en el sistema (cron jobs o TODO.md)
- Workspace commiteado y pusheado

## Related Skills

- [Task Execution](../task-execution): Para ejecutar tareas dentro de la sesión
- [Knowledge Management](../knowledge-management): Para registrar aprendizajes de la sesión
