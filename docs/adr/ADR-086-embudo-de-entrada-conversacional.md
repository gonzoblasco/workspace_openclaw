# ADR-086: El embudo de entrada conversacional - triaje, personas, borradores, escalación y límites de contexto

**Fecha:** 2026-09-30
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** Módulo 1 del curso "OpenClaw Use Cases" (roadmap.sh), procesado en la sesión del 2026-09-30; cierre de módulo en Laboratorio de Activos
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-074 (protocolo de despacho multi-agente), ADR-078 (la salida de un sub-agente es un auto-reporte), ADR-083 (frontera de roles - el CORE orquesta y no escribe código), ADR-084 (registros de sesión - un solo lugar)

---

## Contexto

Un agente expuesto a canales conversacionales (Slack, Discord, Telegram, webchat) recibe un flujo ruidoso: mensajes fragmentados, menciones irrelevantes, adjuntos de formato variable, charla que no requiere respuesta y, de tanto en tanto, una consulta que sí importa. Sin una capa de entrada, el agente gasta tokens en ruido, responde a fragmentos en vez de a ideas completas y puede filtrar contexto de una conversación a otra.

El Módulo 1 del curso "OpenClaw Use Cases" (roadmap.sh) define cinco patrones que resuelven ese problema de forma secuencial. El workspace ya implementaba **parte** de estos patrones sin tenerlos nombrados ni documentados:

- La **L2 (Personas)** existe como los agentes `kanam-dev`, `kanam-ops`, `kanam-mind` y `kanam-studio`, y la frontera de roles del ADR-083.
- La **L4 (Escalación)** existe como el handoff al humano cuando una tarea supera al agente.
- La **L5 (Límites de contexto)** existe como el heartbeat y los scripts de registro de sesión (`scripts/memory-end-session.py`, ADR-084).

Lo que faltaba no era la práctica sino el **marco**: un nombre y un documento que expliquen por qué esas piezas están separadas, y qué reglas las gobiernan. Esta es la deuda que cierra el ADR.

---

## Decisión

**El workspace adopta los cinco patrones del embudo de entrada conversacional como marco de referencia para el comportamiento del agente frente a canales externos.** No se trata de una reescritura de infraestructura, sino de fijar las reglas que gobiernan una arquitectura que ya existe en parte.

### 1. Triaje antes de razonamiento (L1)

Ningún mensaje entra al razonamiento del agente sin pasar por la cadena:

1. **Normalización** - todo payload de plataforma se convierte a una forma canónica; el agente es agnóstico a la plataforma de origen.
2. **Filtro determinista** - menciones, comandos y palabras clave se evalúan **antes** de gastar tokens. Si no hay coincidencia, el mensaje no se procesa.
3. **Debounce (ventana deslizante)** - mensajes fragmentados del mismo usuario se agrupan hasta una pausa.
4. **Techo duro (ceiling)** - la ventana de debounce tiene un tiempo máximo absoluto. Sin techo, un usuario que nunca deja de escribir mantiene el buffer abierto para siempre y el agente nunca responde.
5. **Clasificación** - un modelo liviano decide si el mensaje requiere al agente o es charla.

### 2. Especialización por Persona (L2)

Un agente monolítico que carga todas las instrucciones sufre **dilución del prompt**: cuantas más reglas en contexto, más probable es que ignore una regla pequeña pero importante. La decisión ya vigente (ADR-083) es delegar a roles especializados. Este ADR la refuerza: el enrutamiento a una Persona es la forma correcta de asignar una consulta, y el aislamiento de herramientas por Persona es lo que permite separar operaciones de lectura de las de escritura.

### 3. Borradores en vez de envío directo (L3)

Cuando el agente redacta **en nombre de Gonzo** hacia afuera, no envía: produce un **artefacto etapificado** (borrador) acompañado de una **justificación (rationale)** de por qué lo escribió así y qué datos usó. Gonzo aprueba o edita. **Cero suposiciones**: si un dato no está explícito en el contexto recuperado (por ejemplo, disponibilidad en el calendario), el borrador pregunta en lugar de afirmar.

Esta regla es coherente con `AGENTS.md` § Conducta ("Ask first: anything leaving the machine") y con SOUL.md § Límites ("Nunca mando respuestas a medio hacer a superficies de mensajería").

### 4. Escalación como entrega de mando (L4)

**Una alerta no es una escalación.** La alerta notifica; la escalación cambia el estado del canal: el agente se silencia y cede el control al humano. El mecanismo se denomina **Atomic Channel Lock** - una marca persistente que impide que el agente siga respondiendo mientras el humano interviene, evitando que dos voces compitan por el mismo canal.

Disparadores: umbral de sentimiento (frustración), detección de loops (el mismo intento fallando repetidamente), pedido explícito del usuario, o fallo crítico de una herramienta.

### 5. Límites de contexto con filtro determinista primero (L5)

El contexto se aísla por **identidad → canal → hilo**. Dos reglas duras:

- **TTL / olvido programado:** la memoria inmediata de un canal se resetea por inactividad, para no asumir que una conversación de hace días sigue vigente.
- **El filtro por identidad y permisos es determinista y va ANTES de cualquier búsqueda semántica.** El orden inverso (buscar por significado y luego filtrar) es una fuga de datos, no una optimización.

**Equivalencia operativa:** en el workspace, esta capa es el heartbeat más los scripts de registro de sesión. La práctica ya existía; el ADR la nombra y explica su fundamento.

---

## Consecuencias

### Positivas
- **El workspace deja de redescubrir patrones que ya usa.** La L2, L4 y L5 existían sin documentación que explicara su porqué; ahora tienen un marco de referencia único.
- **Regla accionable y verificable:** "el filtro determinista va antes del semántico" y "un borrador con rationale precede a todo envío externo en nombre de Gonzo" son comprobables, no aspiracionales.
- **Vocabulario compartido:** llamar "escalación" al cambio de estado (y no a la alerta) elimina una ambigüedad que ya había generado confusión en sesión.

### Negativas
- **El techo de debounce agrega latencia** en canales de alto tráfico. Aceptado: la alternativa (responder a fragmentos) es peor y más costosa.
- **El laboratorio de activos por módulo agrega una fase de trabajo al estudio.** Aceptado por Gonzo: el objetivo no es terminar el curso sino extraer capacidad instalada.

### Lo que NO cambia
- No se introduce ningún componente nuevo de infraestructura. Los cinco patrones describen y gobiernan piezas que el workspace ya tiene o que puede adoptar cuando conecte canales que hoy no usa (Gmail, iCloud).
- **El agente no tiene acceso a las cuentas personales de Gonzo** (Gmail, iCloud). Este ADR describe la arquitectura de seguridad *para cuando* esos conectores existan, no habilita su conexión.

---

## Alternativas consideradas

1. **Dejar el curso como apunte sin convertirlo en ADR.** Rechazado: repetiría el defecto que ADR-085 documenta - una decisión/enseñanza que solo vive en una conversación no viaja, y el sistema sigue sin nombrar una práctica que ya ejecuta.
2. **Adoptar solo las lecciones nuevas (L1, L3) y descartar las que ya estaban implementadas (L2, L4, L5).** Rechazado: documentar el conjunto es lo que da coherencia al embudo. Las piezas aisladas no explican por qué el embudo funciona.
3. **Implementar los cinco patrones como un único componente monolítico de "gateway conversacional".** Rechazado: contradice la separación de responsabilidades que ya sostienen la arquitectura multi-agente (ADR-073) y la frontera de roles (ADR-083).

---

## Implementación

| Superficie | Cambio |
|---|---|
| `docs/adr/ADR-086-*.md` | este ADR |
| `docs/learnings/pipeline-agentes.md`, `docs/learnings/metodologia.md` | 3 learnings nuevos (marco del Módulo 1, TTL=heartbeat, método módulo→activos) |
| `studies/openclaw-use-cases/` | registro de las lecciones (retirado 2026-10-12; el curso se reinicia desde cero) |
| `AGENTS.md` | sin cambio en esta fase (la regla dura de borradores ya está bajo "Ask first") |

---

## Referencias

- Módulo 1 del curso "OpenClaw Use Cases" - el registro en `studies/openclaw-use-cases/` se retiro (2026-10-12, curso reiniciado desde cero); la decision del ADR (el marco de los 5 patrones del embudo) sigue vigente
- ADR-073 / ADR-074: arquitectura y despacho multi-agente (origen de la equivalencia con L2)
- ADR-083: frontera de roles (el enrutamiento por Persona como enforcement)
- ADR-084: registros de sesión (fundamento de la equivalencia con L5)
- `memory/2026-09-30.md`: la sesión de estudio
