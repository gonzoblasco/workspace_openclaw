# NORTH.md - El norte de Kanam

**Fecha:** 2026-10-06 (reconstruido desde cero)
**Estado:** Vivo. Fija el "para qué" de largo plazo.
**Autor:** Kanam, a pedido de Gonzo. Reescrito contra el contexto real de **las últimas dos semanas** (dailies 2026-09-22 a 2026-10-06, `docs/ROADMAP.md`, ADRs, `~/projects/*/.knowledge/`) - no contra la memoria vieja.

> **Nota de la reconstrucción (2026-10-06):** la versión anterior era del 2026-09-14 y quedó anclada a proyectos e intereses que ya no son el eje: `kanam-story`/`kanam-studio` como línea narrativa *de producto*, `kanam-solitaires`/`kanam-tetris` como experimentos de portfolio, `kanam-forge` como apuesta. Esos ya no son lo que se trabaja. El norte actual se armó leyendo qué se hizo de verdad en las últimas dos semanas. Lo viejo queda en git.

---

## Por qué existe este documento

Tres documentos responden tres preguntas distintas:

| Documento | Pregunta |
|---|---|
| `docs/ROADMAP.md` | **¿Cómo trabajamos y en qué orden?** (capas + la ruta secuenciada) |
| `docs/NORTH.md` (este) | **¿Qué queremos que exista y para qué?** |

(El registro de apuestas era un doc aparte; se retiró el 2026-10-06 - su contenido de producto vive en `ROADMAP.md` §2.1. El viejo mapa de próximos pasos también se retiró: estaba stale.)

Sin un norte escrito, cada bifurcación se siente igual de válida. En las últimas dos semanas se tocaron, en simultáneo: pipeline de agentes, Kanam OS, OnWheels, CPACC, diseño UI, narrativa, OSS y ecosistema OpenClaw. Ocho frentes defendibles. Este archivo ordena cuáles importan y por qué.

---

## Qué es Kanam (la respuesta corta)

**Kanam es un sistema operativo personal de trabajo con IA, y las obras que salen de él.**

| Capa | Qué es | Hoy |
|---|---|---|
| **1. El sistema** | El OS de trabajo: workspace multi-agente (4 roles + Crew), memoria DB-first, apps propias, pipeline A/B, skills, decisiones documentadas | En producción diaria |
| **2. Las obras** | Lo que el sistema permite construir | `kanam-onwheels` (producto finito en curso), `kanam-os` (app), `soporteml` (version funcional de Lovable con cobro por Stripe) |
| **3. El oficio** | Lo que atraviesa todo y lo hace valioso | a11y + IA como infraestructura + **diseño UI/UX** (el frente más nuevo y más declarado) |

Kanam no "usa IA". Construye el sistema que hace posible usarla bien, y lo pone a producir obras concretas. El nombre viene del "segundo cerebro" original que Gonzo descartó en 2026 y que resucitó como `kanam-mind`; hoy nombra al ecosistema entero.

---

## El camino de madurez del sistema (Kanam OS, por etapas)

El sistema no se construyó de una: maduró por etapas, cada una habilitando la siguiente. Es un **mapa de dependencias, no una lista de tareas**. (Absorbido de `EVOLUTION.md` el 2026-10-06.)

| Etapa | Qué es | Estado (2026-10-06) |
|---|---|---|
| **1. El Suelo** - sistemas de referencia | Design system (tokens semánticos + Anti-Slop), diccionario de entidades (`.knowledge/entities/`), rúbrica de gusto (SHARP) | ✅ Completada |
| **2. El Ritmo** - ciclos de vida y gates | `security-scan` (pre-commit), session hooks (`session_plan.py`), skill evals, lifecycle tracker, regression control | 🟡 **Parcial:** 2 de 5 cableados (`security-scan` al pre-commit; session hooks a arranque/cierre). Los otros 3 quedan como experimentos **sin cablear a propósito**: no tienen qué medir todavía. Ver decisión abajo. |
| **3. El Equipo** - Kanam's Crew | `critic` (sustancia), `auditor` (superficie), `planner` (gobierno), + la guía de inicio rápido | ✅ Completada |
| **4. Expansión y refinamiento** | Módulo de especialistas, validación a11y técnica (`axe-core`), tablero de control del backlog | 🟡 **Parcial:** a11y técnica **medida** (`a11y-scan`, ADR-094); Tablero **cerrado** (es `kanam-os /todos`); especialistas **diferidos a propósito** |

**Metodología de evolución:**
1. **No saltar etapas.** Un `critic` sin rúbrica SHARP es ruido. Un agente sin estándar no es un agente, es una suma de opiniones.
2. **Documentación como código.** Cada paso se registra en un ADR y se implementa como skill o script.
3. **Validación real.** Una etapa se considera completada solo cuando el Core puede verificar el estándar de forma automatizada o semi-automatizada.

> **Decisión abierta (Etapa 2):** de los cinco gates, **dos están cableados**: `security-scan` al pre-commit (el caso real: código de skills de afuera), y `session-planning-hooks` a arranque/cierre (ADR-093). Los otros tres - `skill-evals`, `lifecycle-tracker`, `regression-control` - quedan **sin cablear a propósito**: exigen un objeto que hoy no existe (`.eval.yaml` por skill, un baseline SHARP medido). Cablearlos sería un gate que no puede juzgar nada. Sus specs se conservan con su estado real; si el frente "ciclo de vida de skills" se retoma, ahí está el punto de partida.

---

## El norte, en tres horizontes

### Horizonte 0 - Construir y terminar (ahora, 0-3 meses)
**Para qué:** que el sistema produzca **una obra terminada** y que el oficio suba de nivel. Es lo que de verdad se está haciendo.

Tres frentes activos, todos verificados en las últimas dos semanas:

1. **`kanam-onwheels` - el primer producto "finito, final".** Palabras de Gonzo: *"busco ya lograr un producto finito, final, contigo... quiero poder darle a mi hermano Esteban el sitio completo"*. Sitio de un concesionario multi-marca con chatbot RAG que responde solo con evidencia citada, multi-concesionaria desde el diseño. Fase 1 en curso; Supabase conectado y verificado. Es el ancla de "producto terminado" del semestre.
2. **`kanam-os` - ver la memoria como aplicación.** Pedido: *"quiero poder usarte como una aplicación"*. Fases 1-2 hechas (8 vistas + CRUD). Fase 3 (bloques managed) y Fase 4 (búsqueda semántica) pendientes. Es el sistema mirándose a sí mismo.
3. **El oficio: diseño UI/UX.** Frente abierto por Gonzo el 2026-09-14 y con plan de estudio armado el 2026-10-05: *"entrenarme en el arte del diseño y la UI... que la estética importe SIEMPRE"*. Diagnóstico honesto del propio plan: **el problema no es información, es criterio** - falta el ojo, y eso se entrena mirando y juzgando, no leyendo. Cimiento: skill `design-direction`. **Los tokens y el design system propio YA EXISTEN** (`design/`, ADR-047; contraste verificado por ADR-095). Lo que queda es **aplicarlos** (adopción) y **empezar la semana 1** del plan de práctica (`studies/design/`).

**Criterio de listo (H0):** OnWheels entregado y corriendo para Esteban; Kanam OS con las 4 fases; el design system **aplicado** en las obras (sistema ya existe; falta adopción).

### Horizonte 1 - Capitalizar el oficio (3-12 meses)
**Para qué:** convertir el trabajo en reputación, credencial y trabajo remunerado.

- **OSS a11y** - sigue siendo el diferenciador público. PRs mergeados y vivos en Adobe (react-spectrum), IBM/Carbon, Meta (astryx), MUI. Alimenta la **narrativa** (LinkedIn, nicho a11y + agentic) y es **material de entrevista**.
- **`CPACC`** - meta **personal** de Gonzo (crecimiento propio en a11y). Objetivo de calendario: la sesión de examen cuya aplicación cierra el **9 de diciembre de 2026**. Es la palanca que desbloquea retomar el hilo laboral con un entregable.
- **Búsqueda laboral** - hoy **dormante**: sin procesos abiertos (todos cerrados al 2026-09-24). No es un fracaso, es una pausa. Se reactiva con la credencial CPACC y con el portfolio terminado.

**Criterio de listo (H1):** CPACC rendido, al menos una obra del H0 publicada como caso de estudio, y un proceso laboral nuevo (no el de Disney, que nunca existió) que avance.

### Horizonte 2 - Kanam como plataforma (1-3 años)
**Para qué:** que la infraestructura construida para uno mismo sirva para otros.

La apuesta de fondo, ya nombrada en el BRIEF de `kanam-forge`: empaquetar el pipeline -stack opinado, memoria persistente, a11y integrada, multi-agente con review cruzado- para que otros construyan con él. Los candidatos comerciales vivos (ver `docs/ROADMAP.md` §2.1): `soporteml` (producto privado, version funcional de Lovable con Stripe), `kanam-fixer` (a11y en CI).

**Criterio de listo (H2):** alguien que no sos vos construye algo real con Kanam, y le sale mejor que sin Kanam.

---

## Los frentes vivos (lo que se trabajó de verdad en dos semanas)

Verificado contra los dailies 2026-09-22 a 2026-10-06. **Esto es el norte real, no la aspiración.**

| Frente | Qué es | Estado (2026-10-06) |
|---|---|---|
| **Sistema multi-agente** | 4 roles (dev, mind, ops, studio) + Crew (critic, auditor, planner), ADR-073/074 | Operativo; pipeline A/B con enforcement (ADR-088) |
| **Memoria** | `memory.db` (fuente de verdad) + `kanam-os` para verla; catálogo de memorias del ecosistema | DB-first estable; app Fases 1-2 |
| **Modelos / pipeline** | Asignación por rol y nivel de pensamiento | ADR-090, aplicado y verificado en runtime |
| **`kanam-onwheels`** | Producto finito para Esteban (concesionaria + chatbot RAG) | Fase 1 en curso; Supabase conectado |
| **`kanam-os`** | App local para ver la memoria como fichas/tablas/grafos | Fases 1-2 entregadas |
| **Diseño UI/UX** | El oficio: criterio visual, tokens, design system | Sistema **existe** (ADR-047/095, contraste verificado); falta adopción + práctica (`studies/design/`) |
| **OSS a11y** | PRs en Adobe, IBM/Carbon, Meta, MUI | Continuo; 8 merges, PRs vivos |
| **Ecosistema OpenClaw** | Ronda de 29 repos; candidatos (memoria, skills, verificación) | `docs/ecosystem/DECISIONS.md`; nada instalado |
| **CPACC** | Certificación personal a11y | Plan de estudio; examen dic 2026 |
| **Narrativa / escritura** | Novelas (`Quienes Quedan`, `El Descenso`) + estudio de ingeniería narrativa | Personal; en `docs/stories/` y `studies/` |
| **Búsqueda laboral** | Procesos remunerados | Dormante (0 abiertos desde 09-24) |

---

## Qué ya NO es el norte (para no volver a confundirse)

- **`kanam-story` / `kanam-studio` como productos narrativos activos.** La ficción hoy vive como **literatura personal** (`docs/stories/`) y **estudio de método** (`studies/narrative-engineering/`), no como apuesta de producto. Hubo tres intentos fallidos de clonar Sudowrite; eso es señal de mercado, no de capacidad.
- **`kanam-solitaires` / `kanam-tetris` como vidriera de portfolio.** Fueron bancos de prueba del pipeline; su valor ya se cobró.
- **`kanam-forge` como apuesta vigente.** Último push 2026-08-30; sin actividad en la ventana.
- **La "segunda máquina".** Retirada el 2026-09-29 (ADR-085): el workspace vive solo en la Mac Mini.

No se borran: se marcan como lo que son. Un proyecto sin actividad no es el norte; es historia o material latente.

---

## Cómo decidir (el criterio)

Cuando aparezca un frente nuevo, tres preguntas **en orden**:

1. **¿Termina algo o suma dispersión?** Ya hay ocho frentes vivos. Sumar un noveno proyecto es dispersión; **profundizar uno de los ocho hasta terminarlo es capacidad**. El criterio del H0 es *terminar*, no empezar.
2. **¿Sube el oficio o solo agrega trabajo?** Si alimenta a11y, diseño o el sistema -> capacidad. Si es una herramienta suelta que no atraviesa nada -> ruido.
3. **¿La puedo sostener?** Una persona, una máquina, el foco puesto en terminar OnWheels y Kanam OS. Si no hay energía para mantenerla viva, no se abre.

**La regla del norte:** si un frente nuevo no pasa las tres, se anota en `memory/inbox.md` y se sigue con lo que estaba. No se descarta: se posterga con registro.

<details><summary>Nota honesta sobre la tensión de fondo</summary>

Hay una tensión real entre **terminar** (OnWheels, Kanam OS) y **el oficio** (diseño, CPACC, OSS). Ambas son correctas y compiten por el mismo tiempo. La resolución no es elegir una para siempre: es que el oficio **se aplique dentro de las obras** - el design system se construye haciendo OnWheels, la a11y se ejercita en los PRs sobre componentes reales. El oficio que no se aplica a una obra no se aprende; la obra sin oficio sale mediocre.

Y la verdad incómoda: el frente que paga las cuentas (trabajo remunerado) está dormante, y el que está activo (construir) no factura todavía. Eso está bien por un trimestre. Conviene tenerlo escrito para no confundir actividad con progreso.

</details>

---

## Decisiones abiertas (que este documento NO cierra)

1. **`kanam-fixer`:** alcance sin definir. Es lo que desbloquea el ancla formal del pilar *Accesibilidad* en ADR-001.
2. **La métrica del H1:** "usuarios reales" es vago. Falta el número concreto.
3. **`soporteml`:** v4 cerrado (ADR-091); el producto sigue por la version funcional de Lovable, con cobro por Stripe, y **se queda en Lovable** (no migra). Sin pendientes abiertos.
4. **Respaldo de `~/projects`:** los `.knowledge/` viven solo en disco, sin respaldo en git.
5. **Ecosistema:** decisión de memoria (6 caminos solapados) y de seguridad (guardspine vs ClawSec) - ver `docs/ecosystem/DECISIONS.md`.

---

## Notas de creación

- Creado 2026-09-14, en la sesión donde Gonzo preguntó "¿cuál era el objetivo, el para qué de este proyecto?".
- **Reconstruido 2026-10-06** contra las últimas dos semanas de trabajo real. Motivo: la versión previa describía una constelación de productos narrativos y experimentos que ya no son el eje. Fuentes: dailies 2026-09-22 a 2026-10-06, `docs/ROADMAP.md`, ADRs del workspace, `~/projects/*/.knowledge/`, `docs/studies/` (`design/`, `narrative-engineering/`), `docs/stories/`.
- **Absorbido `EVOLUTION.md` el 2026-10-06.** El blueprint de madurez de Kanam OS (etapas + metodología) pasó a la sección "El camino de madurez del sistema": un solo documento de norte, no dos. Las referencias de los agentes (`critic`, `planner`) se reapuntaron a este archivo.
- Principio: no inventar. Lo que este documento afirma sobre un proyecto sale de su BRIEF/ROADMAP real o del daily donde se trabajó. Las aspiraciones están marcadas como tales (Horizontes 1 y 2).
