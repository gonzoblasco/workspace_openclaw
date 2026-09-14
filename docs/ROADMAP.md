# ROADMAP - Sistema de trabajo con IA

> Hoja de ruta de **decisiones y estado por capa**, no lista de features ni segundo backlog. Cada item define qué es, por qué importa, el criterio de éxito, y la señal de que está listo. La prioridad no es "lo más importante", es **lo que desbloquea más camino por unidad de esfuerzo** en el contexto actual (ADHD, sesiones por proyecto, búsqueda laboral activa).

**Última revisión: 2026-09-14** (verificada contra git, GitHub, hooks y logs - no contra la memoria de la sesión anterior).

**Qué NO es este documento:**
- No define el "para qué" de largo plazo: eso es `docs/NORTH.md`.
- No es la lista de tareas: eso es `memory/memory.db` (tabla `todos`, espejo `memory/todos.md`). Si un item de acá se vuelve tarea concreta y fechada, vive en la DB, no acá.

## Cómo leer este documento

- **Capas**: el sistema vive en 4 planos superpuestos (fundaciones, pipeline, portfolio, crecimiento). Cada capa tiene su propio tipo de optimización.
- **Prioridad**: P0 = desbloquea todo lo demás. P1 = alto valor, bajo riesgo. P2 = ganancia marginal, no urgente.
- **Estado**: 🔴 no iniciado / 🟡 en curso o con deuda activa / 🟢 estable / ⚪ deprecado.
- **Señal de listo**: el criterio objetivo que confirma que el item está resuelto, no "se siente mejor".
- **Regla de estado**: un item solo pasa a 🟢 con evidencia de la señal de listo. El estado se revisa, no se arrastra.

---

## Capa 0 - Fundaciones (sostiene todo)

### 0.1 Estabilidad de la infraestructura (gateway) 🟡 P0
- **Qué**: el gateway de OpenClaw se reinicia suave bajo sesiones long-running (diagnosticado 2026-08-28). Cada reinicio corta el contexto; retomar cuesta más que seguir.
- **Por qué**: es la deuda más cara del sistema. No se ve, pero todo lo demás se apoya en esto.
- **Criterio de éxito**: 0 reinicios de gateway en una sesión de trabajo pesado (refactor + validación + browser).
- **Señal de listo**: una sesión completa de validación de endpoints (15+ POST + 11 GET) sin reinicio del bridge.
- **Diagnóstico histórico (2026-08-28)**:
  - 8 SIGTERM en la ventana 17:44-18:15 (sesión del refactor de Moderno).
  - NO es crash (sin dump), NO es OOM (sería SIGKILL), NO es el proyecto.
  - Disparadores correlacionados: `long-running session` + `auto-compaction succeeded ... retrying prompt` + `post-compaction guard armed`.
  - Causa dominante: AGENTS.md (30.439 chars) y MEMORY.md (22.706) sobre el límite de bootstrap de 20.000 -> truncado en cada arranque.
- **Estado al 2026-09-14 (reabierto, evidencia dura):**
  - **Regresión**: AGENTS.md volvió a **24.044 chars** (el 28/08 había bajado a 8.890). Está otra vez sobre el límite de 20.000. MEMORY.md en **16.099** (bajó a 5.966 el 28/08; dentro del límite, pero creció).
  - Reinicios registrados en `~/.openclaw/logs/gateway-restart.log` después del 28/08: **09-08, 09-11, 09-13 y 09-14**.
  - El **13/09** se generaron **4 dumps `gateway.restart_close_failed`** en `~/.openclaw/logs/stability/` (el gateway no cerró limpio durante el restart).
  - La señal de listo formal nunca se corrió.
  - **Conclusión**: la deuda de mayor impacto está de vuelta. 0.1 pasa de 🟢 a 🟡.
- **Acciones**:
  - [x] Reducir AGENTS.md a <20K (28/08: 8.890 chars) - **REGRESIÓN al 14/09: 24.044**.
  - [x] Reducir MEMORY.md a <20K (28/08: 5.966) - al 14/09: 16.099, dentro del límite.
  - [x] Batchear exec masivo en scripts `.sh` (aplicado y verificado en la sesión de higiene del 28/08).
  - [ ] Bajar de nuevo AGENTS.md a <20K (regresión verificada 14/09). Es la acción de mayor impacto.
  - [ ] Confirmar la señal de listo: validación de 15+ POST + 11 GET sin reinicio.
  - [ ] Revisar si el hot-reload de `~/.openclaw/openclaw.json` contribuye; si sí, separar cambios de config de la corrida.
- **Regla operativa (no es checkbox)**: no mezclar browser tool con exec grande en la misma respuesta.

### 0.2 Higiene del workspace 🟢 P1
- **Qué**: `projects/*` sin trackear, gitlinks desincronizados, restos de merges, archivos basura.
- **Por qué**: un workspace que compila y se entiende de una mirada reduce fricción al arrancar cada sesión.
- **Criterio de éxito**: `git status` del workspace limpio y explicable (solo cambios intencionales).
- **Señal de listo**: `git status --short` no muestra nada inesperado al abrir una sesión.
- **Acciones**:
  - [x] Auditar `projects/*`: 16 proyectos clasificados (10 blob, 4 gitlink, 1 repo-propio). Ver `docs/skills/portfolio-hygiene-notes.md`.
  - [x] Archivar en GitHub `accessible-ui` y `create-with-ai` (`gh repo archive`, verificado `isArchived: true`).
  - [x] Promover `portfolio-strategy` a doble git (ADR-001 trackeado por workspace).
  - [x] Limpiar `.DS_Store` trackeado en `create-with-ai`.
  - [x] Diagnóstico `ai-developer-stack`: `.knowledge` es symlink roto. Repararlo requiere decisión explícita de Gonzo.
  - [x] Verificar que `.gitignore` cubre los archivos de sesión (14/09: `RECENT.md` y `.compaction-recovery-pending` en las líneas 10-11).
  - [x] Cerrar la nota de `init-project.sh` (14/09: el script ya excluye `.knowledge/` del repo del proyecto vía `.git/info/exclude` y lo commitea al workspace git - líneas 26-28 y 203. La premisa de la nota era incorrecta: no hay nada que corregir).
  - [ ] Decidir destino de `kanam-skills` (repo público, hoy desactualizado y con referencias a sanitizar - ver `docs/NORTH.md`, decisiones abiertas).
- **Descartado (14/09)**: "resolver cambios sucios de `kanam-forge` (README) y `kanam-mind` (SettingsModal.tsx)" - ninguno de los dos tiene `.git` propio; el item partía de un supuesto que ya no aplica.
- **Restricción cerrada (no es acción)**: `soporteml` y sus versiones no se tocan - decisión cerrada en ADR-001.

### 0.3 Consolidación de memoria 🟢 P1
- **Qué**: el daily + learnings ya existe; falta el patrón de *cuándo* se archiva y *qué* merece ser lección vs ruido.
- **Por qué**: la memoria es el sistema de continuidad; si se llena de ruido, deja de ser útil.
- **Criterio de éxito**: cada sesión termina con daily consolidado + lecciones relevantes en LEARNINGS, sin duplicar.
- **Señal de listo**: al retomar una sesión, el daily del día anterior responde "dónde estábamos" sin re-descubrir.
- **Nota (14/09)**: el flujo DB-first se cortó el 12-14/09 (dailies editados a mano sin correr `session-end.sh`). Se agregó reconcile `.md`->DB antes del export (commit `d9e964e`), verificado con 6 escenarios. La señal de listo se sostiene.

---

## Capa 1 - Pipeline de ejecución (cómo trabajamos)

### 1.1 Eficiencia del pipeline A/B 🟡 P2
- **Qué**: A escribe, B revisa, Kanam verifica. Hoy funciona; falta medir el cuello de botella real.
- **Por qué**: optimizar sin medir es intuir. El SIGKILL de Qwen y la confianza en el cross-review son sospechosos conocidos.
- **Criterio de éxito**: tiempo por tarea medido y estable; tasa de fixes de B que introducen bugs < umbral.
- **Señal de listo**: métricas de duración por tarea registradas en 5+ sesiones.
- **Acciones**:
  - [ ] Registrar duración por tarea (inicio/fin) en el pipeline-track.
  - [ ] Contar cuántas veces B introduce bugs al "corregir" (cross-review no es infalible, 2026-08-21).
  - [ ] Decidir si el cross-review necesita verificación contra fuente real siempre, o solo en casos de riesgo.

### 1.2 Ruteo de modelos 🟡 P2
- **Qué**: deepseek-v4-flash vs kimi-k2.7-code vs local. El `model-router.sh` es un buen inicio.
- **Por qué**: el modelo correcto por tarea ahorra tiempo y presupuesto; el incorrecto lo quema.
- **Criterio de éxito**: el router elige el modelo correcto sin intervención manual en tareas estándar.
- **Señal de listo**: 0 casos de "este modelo no sirvió para esto" en tareas rutinarias durante una semana.
- **Nota (11/09)**: se detectó que los overrides sticky de `model-router.json` (no el ADR) eran el mecanismo real que forzaba v4.1. Una decisión de modelo no se cierra con el ADR; hay que revisar el runtime state del router.
- **Acciones**:
  - [ ] Agregar telemetría de fallos por modelo (cuándo rotar).
  - [ ] Verificar que el router cubre los tipos de tarea reales (code/review/long/cheap/writing).

### 1.3 Stack opinado como sistema 🟡 P1
- **Qué**: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Está decidido.
- **Por qué**: el valor está en la consistencia, no en la elección.
- **Criterio de éxito**: se aplica siempre, no cuando lo recordamos.
- **Señal de listo**: pre-commit hooks presentes en todos los proyectos activos; ADRs para decisiones nuevas.
- **Acciones**:
  - [x] Auditar proyectos activos (14/09): **0 de 21** proyectos tiene `pre-commit` hook o `simple-git-hooks`. Ninguno cumple la señal de listo.
  - [ ] Instalar pre-commit hooks (lint -> test -> build) en los proyectos activos. Regla: prioridad sobre features.

---

## Capa 2 - Portfolio (qué construimos)

### 2.1 Estrategia de proyectos 🟢 P0
- **Qué**: hay repos vivos, archivados, y candidatos a reset. La pregunta de fondo: ¿qué 2-3 proyectos sostienen el pitch "fullstack con IA como infraestructura"?
- **Por qué**: sin esto, el pipeline optimiza lo equivocado. Dispersión = portfolio que no cuenta una historia.
- **Criterio de éxito**: 2-3 proyectos claros que demuestran el pitch, el resto archivado o en pausa explícita.
- **Señal de listo**: una lista corta de proyectos "estrella" con su rol en el pitch, documentada.
- **Acciones**:
  - [x] Definir los proyectos ancla (ADR-001: kanam-forge, a11y-fixer, kanam-pulse). SoporteML queda EXCLUIDO - decisión cerrada, no se reabre.
  - [x] Decidir destino de accessible-ui y create-with-ai (ADR-001, sección 4: ambas archivadas).
  - [x] Documentar la decisión en un ADR (ADR-001, 2026-08-28).

### 2.2 Cadena OSS → LinkedIn 🟡 P1
- **Qué**: cada merge de a11y/agentic → post. El patrón está definido (2026-08-25); falta la cadencia real.
- **Por qué**: directamente ligado al objetivo laboral (nicho a11y/agentic).
- **Criterio de éxito**: cada merge de a11y/agentic genera un post en `docs/linkedin/` dentro de la semana.
- **Señal de listo**: 3+ posts publicados con el patrón didáctico, no solo drafts.
- **Acciones**:
  - [x] Revisar la cadencia (14/09): 9 posts en `docs/linkedin/` - 7 concentrados el 08/09, 1 el 10/09, 1 el 14/09. El mecanismo está vivo; la cadencia es irregular.
  - [ ] Sostener la cadencia: 1 post por merge de a11y/agentic dentro de la semana.
  - [ ] Verificar que cada post queda documentado en `docs/linkedin/` (mecanismo OK; falta el flip `draft` -> publicado en al menos un archivo, ej. `ibm-products-createfullpage-focus.md`).

### 2.3 Búsqueda laboral 🟢 P0
- **Qué**: procesos abiertos y su estado. La fuente de verdad es `docs/entrevistas/job-search-tracker.md`; acá va solo el resumen.
- **Por qué**: es el objetivo activo del Horizonte 0 (`docs/NORTH.md`); situación económica urgente.
- **Criterio de éxito**: al menos un proceso avanza a oferta/onboarding.
- **Estado al 2026-09-14:**
  - **EIT / HTC / Disney (Lead Digital Accessibility) - OFERTA ACEPTADA (11/09)**: USD 4.000/mes, contractor US sin visa, 40h/semana 10-18 Argentina, arranque **01/10**. Pendientes: papeleo (contrato / W-8BEN) y vigilar el gate de certificación (IAAP sigue en Preferred). **El criterio de éxito está cumplido.**
  - **Cruceros / Ritz-Carlton**: 🟡 esperando. Manager interview 02/09, feedback "24-48h" incumplido. Pasa a pasivo el 15/09 si no escriben ellos.
  - **Kake**: video asincrónico enviado (pasó el primer filtro).
  - **Koin Limited (AI Product Engineer)**: 🟢 activo, mejor stack match del lote.
  - **Aliancers / Ciklum**: aplicados, sin señal humana.
  - **OpenSistemas**: cerrado 11/09 (avanzaron con otro candidato).
- **Señal de listo**: onboarding efectivo el 01/10.
- **Acciones**:
  - [ ] Completar el papeleo de EIT antes del 01/10.
  - [ ] Mantener `docs/entrevistas/job-search-tracker.md` como única tabla de procesos (no duplicar acá).

---

## Capa 3 - Crecimiento (hacia dónde vamos)

### 3.1 Evolución de las skills 🟢 P2
- **Qué**: las skills maduran; el skill_workshop es el mecanismo.
- **Por qué**: falta el criterio de *cuándo* una skill merece promoverse a estándar del workspace.
- **Criterio de éxito**: skills promovidas solo cuando demuestran valor repetido, no por entusiasmo.
- **Señal de listo**: cada skill estándar tiene evidencia de uso en 3+ sesiones.

### 3.2 La segunda máquina como activo 🟢 P2
- **Qué**: el sync por git entre Mac Mini y MacBook Air funciona.
- **Por qué**: vale la pena revisar si el flujo es óptimo o si hay fricción.
- **Criterio de éxito**: cambio de máquina sin fricción (pull --rebase, merge, no reset).
- **Señal de listo**: 0 conflictos de merge no resueltos en un mes.

---

## Prioridad consolidada

| # | Item | Capa | Prioridad | Estado |
|---|------|------|-----------|--------|
| 1 | 0.1 Estabilidad gateway | Fundaciones | P0 | 🟡 |
| 2 | 2.1 Estrategia de proyectos | Portfolio | P0 | 🟢 |
| 3 | 2.3 Búsqueda laboral | Portfolio | P0 | 🟢 |
| 4 | 0.2 Higiene workspace | Fundaciones | P1 | 🟢 |
| 5 | 0.3 Consolidación memoria | Fundaciones | P1 | 🟢 |
| 6 | 2.2 Cadena OSS→LinkedIn | Portfolio | P1 | 🟡 |
| 7 | 1.3 Stack opinado | Pipeline | P1 | 🟡 |
| 8 | 1.1 Pipeline A/B | Pipeline | P2 | 🟡 |
| 9 | 1.2 Ruteo de modelos | Pipeline | P2 | 🟡 |
| 10 | 3.1 Evolución skills | Crecimiento | P2 | 🟢 |
| 11 | 3.2 Segunda máquina | Crecimiento | P2 | 🟢 |

---

## Notas de creación y mantenimiento

- Creado 2026-08-28 a partir de la sesión de refactor de Moderno AI Cleaner Pro (donde se diagnosticó la inestabilidad del gateway).
- Revisado 2026-09-14: se contrastó cada item contra el estado real (git, GitHub, hooks, logs). Se tacharon 4 acciones ya resueltas, se borraron 4 obsoletas, se agregó la regresión de AGENTS.md y el resultado de la auditoría de hooks. Los estados que estaban todos en 🟢 se corrigieron a su valor real.
- La prioridad P0 de "Estrategia de proyectos" y "Búsqueda laboral" refleja que el pipeline optimiza lo equivocado si no sabemos qué construimos.
- Este documento es vivo: se revisa cuando un item cambia de estado o se toma una decisión de prioridad. **Regla: la revisión se hace contra fuentes reales, no contra lo que creíamos recordar.**
