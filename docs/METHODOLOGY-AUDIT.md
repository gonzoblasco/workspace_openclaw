# Methodology Audit - Termómetro de madurez (8 fases)

> **Qué es:** un lente de auditoría, no un workflow ni un pipeline. Los pipelines ya existen (A/B, complexity-driven). Esto responde otra pregunta: **"¿estamos cubriendo todo el ciclo de vida de nuestras propias metodologías?"**
>
> **Origen:** framework de adopción de IA empresarial (Identify Objectives → Map Processes → Prioritize Opportunities → Activate Training → Construct Pilots → Trace Governance → Accelerate Adoption → Iterate and Scale), adaptado a un sistema de trabajo personal con IA como infraestructura.
>
> **Uso:** check rápido al guardar sesión (solo si la sesión tocó metodología) + auditoría profunda trimestral. No es un gate obligatorio de cada sesión - sería ruido.

---

## Las 8 fases y su mapeo con nuestro sistema

| # | Fase | Qué tenemos hoy | Gap conocido | Señal de salud |
|---|---|---|---|---|
| 1 | **Identify Objectives** | Sesiones por proyecto, ADRs, ROADMAP, ritual "iniciar sesión" con Session Goal | Objetivos a veces implícitos; no hay contrato de sesión formal | Toda sesión arranca con objetivo + criterio de éxito explícitos |
| 2 | **Map Processes** | AGENTS.md, AGENTS-DETALLE.md, SKILLS-INDEX.md, PIPELINE-AB.md, docs/checklists/ | Documentación dispersa en varios archivos; no hay un mapa único de procesos | Un nuevo yo (o Gonzo) puede reconstruir un proceso sin re-descubrir |
| 3 | **Prioritize Opportunities** | Complexity scorer (T 1-20), backlog en memory.db, inbox triage | Priorizamos código, no priorizamos metodologías (qué skill crear/mejorar) | Existe una lista priorizada de mejoras metodológicas, no solo de features |
| 4 | **Activate Training** | Skill workshop, skills, lecciones en dailies, post-task-reflection | Skills nacen reactivas (de un incendio), no de un plan de capacidades | Hay respuesta a: "¿qué debería saber hacer el sistema en 3 meses que hoy no sabe?" |
| 5 | **Construct Pilots** | Spikes, Kanam Story Fase 3, proyectos piloto | Pilots de metodologías son implícitos (probamos skills en vivo sin criterio de éxito) | Toda skill nueva tiene un pilot definido con criterio de éxito antes de adoptarse |
| 6 | **Trace Governance** | ADRs, red lines, hooks, check_em_dash, verify-before-push, test-skills.sh | Gobernanza fuerte en código (automatizada), débil en procesos (depende de memoria) | Las reglas de proceso críticas tienen verificación automática, no solo memoria |
| 7 | **Accelerate Adoption** | Skills mirror, kanam-skills públicas, HEARTBEAT, dailies, session-start con contexto semántico | A veces el próximo yo re-descubre en vez de re-usar | Lo aprendido una vez se reutiliza sin re-descubrimiento |
| 8 | **Iterate and Scale** | Guardar sesión, CHANGELOG, retrospectivas, LEARNINGS.md | Escalar = reutilizar entre proyectos; es parcial y reactivo | Las lecciones de un proyecto se aplican a los demás de forma sistemática |

---

## Check rápido (al guardar sesión, solo si la sesión tocó metodología)

Si la sesión modificó skills, AGENTS.md, scripts, docs de proceso o creó una lección nueva, correr este check antes de cerrar. Si no tocó metodología, saltarlo.

- [ ] **1. Objectives:** ¿la sesión tenía objetivo explícito? ¿quedó registrado?
- [ ] **2. Map:** ¿el cambio de proceso quedó documentado donde se busca (no donde se crea)?
- [ ] **3. Prioritize:** ¿esto resuelve un problema real o es mejora aspiracional? ¿hay algo más importante esperando?
- [ ] **4. Training:** ¿el aprendizaje quedó en LEARNINGS.md / DB, o solo en el daily?
- [ ] **5. Pilots:** si es skill/script nuevo, ¿tiene un caso de uso real próximo donde se va a probar?
- [ ] **6. Governance:** ¿la regla nueva necesita verificación automática (hook/script/test)? Si sí, ¿se agregó?
- [ ] **7. Adoption:** ¿el próximo yo va a encontrar esto sin re-descubrirlo? (mirror, índice, referencias)
- [ ] **8. Iterate:** ¿esto se puede reutilizar en otro proyecto, o quedó atado a uno solo?

**Regla:** si 3 o más casillas quedan sin marcar, la sesión dejó deuda metodológica. Registrarla como pendiente, no ignorarla.

---

## Auditoría profunda (trimestral o a pedido)

Para cada fase, puntuar 0-2:

- **0** = no existe / no se practica
- **1** = existe pero es reactivo, manual o depende de memoria
- **2** = está automatizado, verificado o es parte del ritual

Total: 0-16.

| Banda | Estado | Acción |
|---|---|---|
| 0-5 | Incipiente | Elegir las 2 fases más bajas y atacarlas el próximo trimestre |
| 6-10 | Operativo | Funciona, pero depende de memoria. Automatizar lo más bajo |
| 11-13 | Maduro | Sólido. Buscar el gap más caro y cerrarlo |
| 14-16 | Excelente | Mantener. El foco pasa a posicionamiento externo |

### Preguntas guía por fase (auditoría profunda)

**1. Identify Objectives**
- ¿Toda sesión de trabajo arranca con Session Goal + criterio de éxito?
- ¿Los objetivos de proyecto están en ROADMAP/ADRs, no solo en cabezas?

**2. Map Processes**
- ¿Un agente nuevo (o Gonzo en otra máquina) puede reconstruir cada proceso clave sin preguntar?
- ¿Qué procesos existen solo en la memoria de Kanam y no en docs?

**3. Prioritize Opportunities**
- ¿Hay backlog de mejoras metodológicas (skills, scripts, hooks) priorizado?
- ¿El complexity scorer se usa para decidir pipeline, o se saltea?

**4. Activate Training**
- ¿Qué capacidad nueva necesitamos en 3 meses que hoy no tenemos?
- ¿Las skills cubren los patrones repetidos, o seguimos improvisando?

**5. Construct Pilots**
- ¿Las skills nuevas se prueban con criterio de éxito antes de declararse estándar?
- ¿Los spikes terminan con decisión documentada (adoptar/descartar)?

**6. Trace Governance**
- ¿Las reglas críticas tienen verificación automática (hooks, scripts, tests)?
- ¿Los ADRs se respetan o se re-preguntan? (Regla de Oro)

**7. Accelerate Adoption**
- ¿El mirror de skills está al día? ¿Las skills públicas están sanitizadas?
- ¿El próximo yo re-usa o re-descubre?

**8. Iterate and Scale**
- ¿Las lecciones de un proyecto se aplican a los demás?
- ¿La última auditoría generó acciones que se cumplieron?

---

## Resultado de la auditoría

| Fecha | Puntaje | Fases más bajas | Acciones | Estado |
|---|---|---|---|---|
| 2026-09-03 | - | - | Auditoría inicial creada | - |

---

## Nota de posicionamiento

Este framework también es **vocabulario presentable** (entrevistas, landing, consultoría): "adopción de IA en 8 fases" con evidencia concreta en cada fase. Si se quiere usar para eso, cada fila del mapeo es un claim verificable con links a docs, skills y commits reales. No es humo de consultora - es un sistema que ya corre.
