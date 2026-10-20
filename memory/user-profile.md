# Perfil de Gonzo - Detalle ampliado

> Migrado de `USER.md` el 2026-09-14. `USER.md` tiene un **cap fijo de 4.000 chars** en el bootstrap de OpenClaw (`USER_BOOTSTRAP_MAX_CHARS`, no configurable), asi que el detalle vive aca y `USER.md` conserva las reglas criticas + punteros.
>
> Este archivo vive bajo `memory/` a proposito: **`memory_search` indexa `memory/` y no `docs/`**, asi que aca el contenido es recuperable por busqueda semantica.
>
> **Los hechos duros de la carrera (fechas, anos, titulos por rol, idioma, certificaciones) NO viven aca: su dueno es `memory/career-facts.md`.** Este archivo guarda la **lectura** de esos hechos - que significan, como contarlos, que destacar - y los cita. Si un numero de aca difiere de `career-facts.md`, gana `career-facts.md` y este archivo esta mal.

---

## Trayectoria profesional (verificado)

- **EY** (Sep 2021 - May 2025) - consultora internacional. Referente de accesibilidad del equipo: validó y corrigió 50+ componentes de una librería empresarial a WCAG, y fue parte del equipo que construyó una plataforma de inteligencia financiera. Nivel senior.
- **Super7ui** (Ago 2020 - May 2021) - consultora de medios digitales. En una plataforma de streaming global remedió 200+ problemas de accesibilidad probados con lectores de pantalla e implementó pruebas automáticas de a11y.
- **Minutentag / EULAS** (Feb 2016 - Nov 2019) - agencia de e-commerce para marcas de EE.UU. Desarrolló y mantuvo flujos de compra (checkout, carrito), participó de la migración a React y mejoró un sitio con 2M+ usuarios mensuales. Accesibilidad desde el inicio.

**Lectura para propuestas a11y:** a11y NO es un hilo secundario - es continua desde 2016 y en dos roles fue la funcion central. Los anos exactos, las fechas y los titulos por rol los declara `memory/career-facts.md`; aca va solo como contarlo:
- **Super7ui:** rol dedicado a accesibilidad. 200+ fixes probados con lectores de pantalla + pruebas automaticas de a11y. Cuenta como ano entero de a11y engineering.
- **EY:** referente de a11y del equipo, 50+ componentes enterprise a WCAG. Enterprise.
- **Minutentag/EULAS:** a11y parte sustantiva del rol; crecio de junior a referente de accesibilidad.
- **No sumar el backend PHP 2001-2008** al total ni usarlo como headline: es backend (no a11y) y hay gap 2008-2016. Solo defendible como amplitud ante audiencia que no pregunte por el gap: decidir por audiencia.
- **Años, backend, IA y nombre del rol:** su dueno es `memory/career-facts.md` (sección Años y Roles). Aca no se copian. Los tres datos que más se inflan por error, y que ese archivo fija: IA y backend desde 05/2025 (~1 año y medio, nunca 3 ni 4), y el rol se llama **freelance**, nunca "Independent" ni "Founder".
- **SoporteML - regla vigente (2026-10-20, decisión de Gonzo):** producto propio bajo el rol **Freelancer (05/2025-presente)**, con **Pro Motors como primer cliente** (`pro-motors.com.ar`, integración MeLi real). **SÍ va al CV y a las propuestas laborales.** Sigue fuera del portfolio público (repo privado) y no se propone como ancla de la estrategia de proyectos. **Derogadas:** la regla 2026-09-14 ("fuera de la narrativa pública… no proponerlo como ancla") y el arrastre 2026-10-06 ("fuera del CV"). Contexto de producto: v4 cerrado, sigue por la versión funcional de Lovable (v1) con **Stripe** habilitado en Argentina (ADR-091 / ADR-0002 de `soporteml`).
- **Pilar Accesibilidad - en transicion (2026-09-14):** `a11y-fixer` **quedo archivado** por decision de Gonzo, y su sucesor es **`kanam-fixer`, un proyecto NUEVO** (no un renombre). El alcance de kanam-fixer esta **sin definir**: no asumir que hereda el rol de engine de fixes de a11y. Mientras eso no se defina, el pilar Accesibilidad **no tiene ancla formal** - `ADR-001` todavia nombra a `a11y-fixer` como ancla, asi que requiere enmienda explicita (los ADR no se reescriben en silencio). Los otros dos anclas siguen firmes: kanam-forge y kanam-pulse. Todo en DB id=54.

**Gap real y unico: no tiene certificacion IAAP (CPWA / WAS / CPACC).** No volver a marcar su a11y como "reciente" ni JAWS como gap, ni omitir Super7ui del conteo.

## Perfil profesional (diferenciador)

1. **Metodología IA-asistida own** - trabaja con un sistema completo de IA como infraestructura: sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop. No usa IA como chat, la usa como copiloto metodológico. La mayoría de los devs no saben hacer esto.
2. **Herramientas curadas por criterio, no por default** - (CSN: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG). Cada una se adopta por lo que sirve hoy, no por convención heredada ni por precedente.
3. **Accesibilidad como especialización activa** - no es checkbox, es ventaja competitiva. Tiene proyectos dedicados y busca trabajos donde sea central.
4. **Fullstack real** - React/TS frontend, Supabase/Edge Functions backend, DB, billing, tooling, scaffolding.
5. **Documenta decisiones, no solo código** - AGENTS.md, ROADMAP, ADRs. Eso es senior sin título.
6. **Producto real con IA** - SoporteML (CRM para vendedores de Mercado Libre con IA, backend sólido + billing con cobro operativo) demuestra producto completo, no solo demos.

**El pitch:** *"Soy un dev fullstack que construyó un sistema de trabajo con IA propio, con herramientas curadas por criterio y docs de decisiones. Tengo PRs mergeados que lo demuestran."*

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

- **Inglés: B2 (dato duro, 2026-10-20).** Nivel definido por Gonzo y reafirmado por él tras un error mío que lo declaró C1 en un screening. **Nunca declarar C1 ni otro nivel superior** en formularios, screenings, CVs ni entrevistas: va B2. Él escribe y trabaja en inglés a diario, pero el nivel declarado es B2. Si aparece la duda, preguntar antes de escribir el número.
- **El gap es oral, no escrito (2026-10-20, precisión de Gonzo).** Lo que le falta es un poco de **práctica hablada**; lectura, escritura y trabajo diario en inglés están aceitados. No tratarlo como "inglés flojo" ni sugerirle cursos generales, academias o gramática: el pedido es práctica de conversación. No confundir el nivel declarado (B2, para formularios) con su desempeño real, que en escrito es más alto.

> **Reglas de trato y preferencias:** su dueno es `MEMORY.md` (y `AGENTS.md` para las reglas
> duras). Aca no se copian: una regla en dos archivos es una regla que se puede citar
> convenientemente. Este archivo guarda el perfil: trayectoria, diferenciador y estilo.

## Reglas de interacción (detalle)

- **Analizar antes de asumir (2026-09-02):** triple lectura - (1) literal, (2) con tono (relación, humor, contexto), (3) con intención (¿discusión? ¿desahogo? ¿validación?). Si la ambigüedad es real, preguntar. Alcance total: aplica a conclusiones técnicas también. Caso: Base UI #5633 - atomiks respondió a `@Zezombye` sin mencionar a Gonzo; primera lectura "me ignoró", segunda lectura "respondió en sustancia, solo sin tag". No fue desaire.
- **Verificar antes de descartar (2026-09-13):** verificar el dato exacto que afirma antes de contradecirlo. Caso qwen3.8:27b-mlx - se descartó su tag sin verificar y estaba equivocada.
- **Precisión y human in the loop (2026-09-12):** meta futura = más autonomía; hoy la prioridad es el human in the loop.
- **No re-descubrir su pasado (2026-09-11):** ante reclamos ("¿ya no conocés mi pasado?"), la falla es no haber leído la memoria ya documentada. Buscar en memoria primero.
- **Dependencias (2026-09-14):** el precedente no es un motivo. Caso: Radix/shadcn entraron por el template y ADR-037 los citó como decisión.
