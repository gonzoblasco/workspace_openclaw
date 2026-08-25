# Resumen de capacidades: Arquitectura y orquestación de IA con OpenClaw

> Documento de apoyo para la entrevista con OpenSistemas (puesto AI-Native, perfil Latam).
> Objetivo: mostrar evidencia concreta de criterio de arquitectura, guía de IA, creación de
> habilidades/agentes, orquestación, planificación y documentación. No es una lista de features,
> es evidencia de capacidades reales.

---

## 1. Criterio de arquitectura y toma de decisiones

No soy "un usuario de IA". Construí un sistema de trabajo donde la IA es infraestructura, no un chat.

**Decisiones que tomé con criterio (no por convención):**

- **Modelo de agentes:** evalué a fondo cómo OpenClaw aísla el trabajo. Descubrí que la unidad real
  de aislamiento es el *agente* (workspace completo), no la sesión. Decidí mantener UN solo agente
  principal con conversaciones limpias por proyecto, en vez de multiplicar agentes que duplican
  contexto y no comparten artefactos. Anti-patrón detectado y evitado por análisis, no por prueba y error.
- **Stack opinado:** curé herramientas por criterio (OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG),
  no por lo que "se usa". Cada elección está documentada como decisión, con su razón.
- **Router de modelos:** no uso un modelo para todo. Clasifico tareas por tipo (code/review/long/cheap/writing)
  y ruteo al modelo adecuado (DeepSeek Flash para el día a día, Kimi K para programación avanzada).
  Esto es gestión de costos y calidad, no "usar la IA más cara".

**Evidencia:** ADRs (registros de decisiones de arquitectura), CHANGELOG por proyecto, arquitectura
de agentes documentada.

---

## 2. Guiar la IA, no dejar que trabaje sola

El punto central que valoraron: sé cuándo la IA debe avanzar sola y cuándo debo intervenir.

**Cómo lo hago en la práctica:**

- **Pipeline A/B de programación:** un agente escribe, otro revisa/corrige, y YO orquesto el flujo.
  No es "la IA hace todo" - es control de calidad en cadena donde el humano decide.
- **Verificación contra la fuente real:** aprendí (por una lección dura) que el agente "revisor"
  puede INTRODUCIR bugs al corregir código correcto basándose en suposiciones falsas. Regla:
  nunca confío en el veredicto de un agente sin verificar contra la fuente real (doc/spec de la API).
- **Human-in-the-loop:** las acciones destructivas o externas siempre pasan por aprobación.
  La IA propone, yo decido. Nada sale al mundo sin revisión humana.

**Evidencia:** el flujo que mostré en la entrevista - tomar un issue de GH, analizarlo, armar el
plan, ejecutar, y dejar todo listo para revisión antes de avanzar.

---

## 3. Crear habilidades y agentes

Tengo cerca de 70 habilidades (skills) creadas a medida, todas diseñadas para tareas específicas
de nuestro flujo. No son prompts sueltos: son procedimientos estructurados y reutilizables.

**Qué construí:**
- Habilidades de pipeline (orquestación de agentes, revisión cruzada, modelo router).
- Habilidades de memoria (guardado de sesión, registro de decisiones, dailies).
- Habilidades de dominio (accesibilidad, PDF/OCR, seguridad, network).
- Un "skill workshop": proceso para crear, revisar y aprobar nuevas habilidades como propuestas
  (nunca edición directa - control de calidad sobre el propio sistema).

**Sobre agentes:** entiendo el modelo de aislamiento de agentes, cuándo conviene un agente
separado (aislamiento duro de cliente) y cuándo es un anti-patrón (duplicación).

---

## 4. Orquestar tareas y planificar todo

**Cómo orquesto:**
- Descompongo metas en tareas concretas para agentes.
- Encadeno trabajo en pipeline (agente A escribe -> orquestador pasa contexto a B -> B revisa ->
  verificar -> iterar).
- Gestiono el ciclo de vida de cada tarea: plan, ejecución, verificación, registro.
- Coordino trabajo en background en paralelo cuando corresponde.

**Cómo planifico:**
- Sesiones por proyecto (no mezclar contextos).
- Roadmaps, ADRs, OpenSpec (specs con requirements auditables).
- Registro de decisiones: por qué se eligió X, no solo qué se hizo.
- Backlog gestionado con datos estructurados (todos/inbox) persistidos en base.

---

## 5. Documentar (lo que más valoraron)

Documentar es parte central de mi método, no un afterthought.

**Qué documento y cómo:**
- **Decisiones de arquitectura** (ADRs): el "por qué" de cada elección.
- **Memoria persistente:** dailies, lecciones aprendidas, memoria curada de largo plazo.
- **Handoffs:** estado claro para retomar el trabajo sin re-descubrir todo.
- **CHANGELOG:** registro estructural de cada cambio.
- **Documentación viva:** AGENTS.md (reglas de operación), USER.md (contexto del humano),
  TOOLS.md (cheat sheet del entorno).

**Por qué importa:** porque el valor de un sistema con IA no está solo en lo que produce hoy,
sino en que el conocimiento no se pierde. Documentar es lo que hace que el sistema escale
y que cualquier persona (o el propio sistema) pueda retomarlo.

---

## 6. Lo que demostré en la entrevista

- Conozco la empresa y su sistema (SofIA) y su plataforma No Code (SOKIA) - investigado de antemano.
- Uso OpenClaw a diario como "sistema operativo inteligente" desde hace ~2 meses.
- ~70 habilidades creadas a medida para nuestras tareas.
- Demo en vivo: tomé un issue real de GitHub (de Facebook), lo analicé con IA, armé el plan,
  lo ejecuté y dejé todo preparado para revisión antes de avanzar.
- "Es justo lo que buscan": alguien que desarrolle end-to-end usando IA.

---

## Resumen en una frase

> No busco que la IA trabaje sola. Construyo la arquitectura, decido con criterio, guío la IA
> por el camino correcto, creo las habilidades y agentes necesarios, orquesto el flujo completo
> y documento cada decisión para que el sistema escale y no pierda conocimiento.
