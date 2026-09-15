# Perfil de Gonzo - Detalle ampliado

> Migrado de `USER.md` el 2026-09-14. `USER.md` tiene un **cap fijo de 4.000 chars** en el bootstrap de OpenClaw (`USER_BOOTSTRAP_MAX_CHARS`, no configurable), asi que el detalle vive aca y `USER.md` conserva las reglas criticas + punteros.
>
> Este archivo vive bajo `memory/` a proposito: **`memory_search` indexa `memory/` y no `docs/`**, asi que aca el contenido es recuperable por busqueda semantica. Fuente de verdad del perfil completo.

---

## Trayectoria profesional (verificado)

- **EY** (Sep 2021 - May 2025) - consultora internacional. Referente de accesibilidad del equipo: validó y corrigió 50+ componentes de una librería empresarial a WCAG, y fue parte del equipo que construyó una plataforma de inteligencia financiera. Nivel senior.
- **Super7ui** (Ago 2020 - May 2021) - consultora de medios digitales. En una plataforma de streaming global remedió 200+ problemas de accesibilidad probados con lectores de pantalla e implementó pruebas automáticas de a11y.
- **Minutentag / EULAS** (Feb 2016 - Nov 2019) - agencia de e-commerce para marcas de EE.UU. Desarrolló y mantuvo flujos de compra (checkout, carrito), participó de la migración a React y mejoró un sitio con 2M+ usuarios mensuales. Accesibilidad desde el inicio.

**Lectura para propuestas a11y (corregido 2026-09-11, 2da correccion de Gonzo):** a11y NO es un hilo secundario - es continua desde 2016 y en dos roles fue la funcion central:
- **Super7ui (Ago 2020 - May 2021, ~1 ano):** rol dedicado a accesibilidad. 200+ fixes probados con lectores de pantalla + pruebas automaticas de a11y. Contar como ano entero de a11y engineering.
- **EY (Sep 2021 - May 2025, ~3.7 anos):** referente de a11y del equipo, 50+ componentes enterprise a WCAG. Enterprise.
- **Minutentag/EULAS (Feb 2016 - Nov 2019, ~3.7 anos):** a11y parte sustantiva del rol; crecio de junior a referente de accesibilidad.
- **Total:** ~10 anos de desarrollo continuo (feb 2016 - hoy); ~5 anos con a11y como funcion central/dedicada.
- **Nota sobre el conteo (2026-09-14):** antes de 2016 hubo backend PHP entre 2001 y 2008 (~7 anos). NO se suma al total ni se usa como headline: es backend (no a11y), hay un gap de ~8 anos (2008-2016), y Gonzo no lo quiere destacar. Si alguna vez se necesita amplitud ("20+ anos en software") es defendible, pero abre la pregunta por el gap: decidir por audiencia.
- **SoporteML (2026-09-14):** fuera de la narrativa publica (ADR-001) y fuera del perfil - no es el proyecto estrella, decision explicita de Gonzo. No proponerlo como ancla.
- **Pilar Accesibilidad - en transicion (2026-09-14):** `a11y-fixer` **quedo archivado** por decision de Gonzo, y su sucesor es **`kanam-fixer`, un proyecto NUEVO** (no un renombre). El alcance de kanam-fixer esta **sin definir**: no asumir que hereda el rol de engine de fixes de a11y. Mientras eso no se defina, el pilar Accesibilidad **no tiene ancla formal** - `ADR-001` todavia nombra a `a11y-fixer` como ancla, asi que requiere enmienda explicita (los ADR no se reescriben en silencio). Los otros dos anclas siguen firmes: kanam-forge y kanam-pulse. Todo en DB id=54.

**Gap real y unico: no tiene certificacion IAAP (CPWA / WAS / CPACC).** No volver a marcar su a11y como "reciente" ni JAWS como gap, ni omitir Super7ui del conteo.

## Perfil profesional (diferenciador)

1. **Metodología IA-asistida own** - trabaja con un sistema completo de IA como infraestructura: sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop. No usa IA como chat, la usa como copiloto metodológico. La mayoría de los devs no saben hacer esto.
2. **Stack opinado, no por default** - cura herramientas (CSN: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG). Decide por criterio, no por convención heredada.
3. **Accesibilidad como especialización activa** - no es checkbox, es ventaja competitiva. Tiene proyectos dedicados y busca trabajos donde sea central.
4. **Fullstack real** - React/TS frontend, Supabase/Edge Functions backend, DB, billing, tooling, scaffolding.
5. **Documenta decisiones, no solo código** - AGENTS.md, ROADMAP, ADRs. Eso es senior sin título.
6. **Producto real con IA** - SoporteML (CRM para vendedores de Mercado Libre con IA, backend sólido + billing) demuestra producto completo, no solo demos.

**El pitch:** *"Soy un dev fullstack que construyó un sistema de trabajo con IA propio, con stack opinado y docs de decisiones. Tengo PRs mergeados que lo demuestran."*

Un repositorio con PRs mergeados en Adobe, IBM/Carbon, Meta o MUI vale más que cualquier take-home test.

## Marca personal y alcance (LinkedIn)

- **Branding (2026-08-25):** 3 nichos: (1) **a11y** (diferenciador), (2) **Agentic/AI-Native** (laboral), (3) **Fullstack** (base). Patrón: SOLO PRs MERGEADOS, postura didáctica/pedagógica (el qué + proceso + por qué), sin tutoriales secuenciales. Archivar cada post en `docs/linkedin/`.
- **Regla de branding (2026-09-02):** issues/participaciones con crédito de maintainers NO son material de post - solo PRs mergeados propios. El crédito externo (ej. cixzhang en #4777) es material de ENTREVISTA (evidencia de proceso), no de LinkedIn. El registro interno (OSS-TRACKER/daily) captura todo.
- **Alcance (2026-09-14):** Darren Denham (CPACC, Assistant Director of Digital Accessibility) interactuó dos veces con posts distintos (astryx #5419 en agosto, ibm-products #9878 en septiembre). La propuesta de EIT/HTC/Disney llegó por LinkedIn: el canal convierte.

## Estilo en issues/PRs de terceros

- Natural y suelto, no como manual de programación
- Sonar a persona real, no a documentación técnica
- En inglés siempre en repos externos
- Bugs concretos sin competencia: no asumir simplicidad - "concreto" describe la reproducción, no la profundidad del fix. Evaluar alcance antes de decidir entre PR propio, análisis con diagnóstico, o ayuda a un PR existente.
- Contribución combinada por ticket: priorizar ayudar a mergear PRs existentes (review con sustancia, verificación contra main, destrabar CI, rescatar tests de regresión) sobre abrir PR propio competitivo; usar código cuando hace falta, en servicio del merge ajeno o del fix no reclamado.
- RFCs → comentario técnico que posiciona, no código

## Preferencias y reglas varias

- **Ley de vida (2026-08-12):** Silencio = respeto. Hablar solo si hay algo que aportar. Un "ok" es ruido.
- **Principio Boy Scout (2026-08-17):** Dejar el lugar mejor de como estaba al guardar sesión. Documentación constante y tests sobre lo nuevo.
- **Regla de merge:** Siempre merge, nunca reset (evita perder commits de la otra máquina).
- **Docs por categoría (2026-08-27):** Carpetas en `docs/` para `linkedin/`, `feedback/`, `prs/`, `pipeline/`, `entrevistas/`. Raíz solo para generales.
- **Idioma GitHub (2026-08-12):** TODO en inglés (README, docs, ADRs, commits, PRs). Strings de UI en español.
- **Regla de alcance (2026-08-11):** Solo trabajar dentro de `.openclaw/`.
- **Terminología:** "Guardar sesión" (save point), no "cerrar sesión".
- **"adelante" (2026-08-12):** "Ejecutá tu recomendación según el contexto".
- **Proactividad:** Sugerir revisar el backlog si no hay tarea clara.
- **Skills (2026-08-21):** Cambios solo vía `skill_workshop` (propuesta), no edición directa.
- **Colaboración OSS (2026-08-24):** El valor suele estar en comentar/revisar, no en abrir PRs. No pisar el trabajo ajeno.
- **Interacción Maintainers (2026-08-24):** Si la dirección ya fue validada, ir directo a la acción (hacer el PR), no ofrecer "estoy feliz de iterar".
- **Bots de review (2026-08-24):** No agradecer a bots. Responder directo a la sustancia con evidencia.
- **Referencia ≠ proyecto (2026-08-24):** "Quitar referencia" = quitar puntero git, NUNCA borrar carpeta con datos locales (`.env`, `*.db`). Respaldar SIEMPRE antes de limpiar.
- **Regla de tools (2026-08-30):** Cuando un `file_write`/`edit`/`apply_patch` devuelve error de validación, NO asumir que la operación tuvo éxito. Confirmar con el resultado del tool o con un `read` posterior. Reportar el fallo, no inventar el éxito.
- **Auto-review antes de abrir PRs (2026-09-02):** Un test que dice cubrir X debe renderizar la estructura real de X, no una version simplificada. Checklist: (1) el test ejercita el DOM/estructura real; (2) las aserciones verifican el comportamiento declarado en el body del PR; (3) el test falla si el comportamiento se rompe. Lección del PR react-spectrum #10554.
- **PR públicos: NUNCA actuar sin OK explícito (2026-09-02):** en un PR abierto (propio o ajeno) NO hacer commit, push, ni publicar comments sin que Gonzo lo pida explícitamente. La autonomia vale para trabajo interno; en superficies públicas (PRs, issues) Gonzo decide. Lección: tercer commit + push no solicitado en react-spectrum #10554.

## Reglas de interacción (detalle)

- **Analizar antes de asumir (2026-09-02):** triple lectura - (1) literal, (2) con tono (relación, humor, contexto), (3) con intención (¿discusión? ¿desahogo? ¿validación?). Si la ambigüedad es real, preguntar. Alcance total: aplica a conclusiones técnicas también. Caso: Base UI #5633 - atomiks respondió a `@Zezombye` sin mencionar a Gonzo; primera lectura "me ignoró", segunda lectura "respondió en sustancia, solo sin tag". No fue desaire.
- **Verificar antes de descartar (2026-09-13):** verificar el dato exacto que afirma antes de contradecirlo. Caso qwen3.8:27b-mlx - se descartó su tag sin verificar y estaba equivocada.
- **Precisión y human in the loop (2026-09-12):** meta futura = más autonomía; hoy la prioridad es el human in the loop.
- **No re-descubrir su pasado (2026-09-11):** ante reclamos ("¿ya no conocés mi pasado?"), la falla es no haber leído la memoria ya documentada. Buscar en memoria primero.
- **Dependencias (2026-09-14):** el precedente no es un motivo. Caso: Radix/shadcn entraron por el template y ADR-037 los citó como decisión.
