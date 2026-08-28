# ROADMAP - Sistema de trabajo con IA

> Hoja de ruta de decisiones, no lista de features. Cada item define qué es, por qué importa, el criterio de éxito, y la señal de que está listo. La prioridad no es "lo más importante", es **lo que desbloquea más camino por unidad de esfuerzo** en el contexto actual (ADHD, sesiones por proyecto, búsqueda laboral activa).

## Cómo leer este documento

- **Capas**: el sistema vive en 4 planos superpuestos (fundaciones, pipeline, portfolio, crecimiento). Cada capa tiene su propio tipo de optimización.
- **Prioridad**: P0 = desbloquea todo lo demás. P1 = alto valor, bajo riesgo. P2 = ganancia marginal, no urgente.
- **Estado**: 🔴 no iniciado / 🟡 en curso / 🟢 estable / ⚪ deprecado.
- **Señal de listo**: el criterio objetivo que confirma que el item está resuelto, no "se siente mejor".

---

## Capa 0 - Fundaciones (sostiene todo)

### 0.1 Estabilidad de la infraestructura (gateway) 🔴 P0
- **Qué**: el gateway de OpenClaw se reinicia suave bajo cadenas largas de exec en serie (diagnosticado 2026-08-28). Cada caída corta el contexto; retomar cuesta más que seguir.
- **Por qué**: es la deuda más cara del sistema. No se ve, pero todo lo demás se apoya en esto.
- **Criterio de éxito**: 0 caídas de gateway en una sesión de trabajo pesado (refactor + validación + browser).
- **Señal de listo**: una sesión completa de validación de endpoints (15+ POST + 11 GET) sin reinicio del bridge.
- **Acciones**:
  - [ ] Medir: contar caídas por sesión durante una semana (log del gateway).
  - [ ] Batchear exec: agrupar validaciones masivas en scripts `.sh` de un solo exec (ya aplicado en Moderno, formalizar como regla).
  - [ ] No mezclar browser tool con exec grande en la misma respuesta.
  - [ ] Revisar si el hot-reload de `~/.openclaw/openclaw.json` (cambios de model/context) contribuye; si sí, separar cambios de config de la corrida.

### 0.2 Higiene del workspace 🟡 P1
- **Qué**: `projects/*` sin trackear, gitlinks desincronizados, restos de merges, archivos basura (ej. el archivo con nombre de query SQL del 28/08).
- **Por qué**: un workspace que compila y se entiende de una mirada reduce fricción al arrancar cada sesión.
- **Criterio de éxito**: `git status` del workspace limpio y explicable (solo cambios intencionales).
- **Señal de listo**: `git status --short` no muestra nada inesperado al abrir una sesión.
- **Acciones**:
  - [ ] Auditar `projects/*`: cuáles son gitlinks válidos, cuáles son restos.
  - [ ] Decidir el destino de los candidatos a reset/archivar (accessible-ui, create-with-ai).
  - [ ] Verificar que `.gitignore` cubre los archivos de sesión (RECENT.md, .compaction-recovery-pending).

### 0.3 Consolidación de memoria 🟡 P1
- **Qué**: el daily + learnings ya existe; falta el patrón de *cuándo* se archiva y *qué* merece ser lección vs ruido.
- **Por qué**: la memoria es el sistema de continuidad; si se llena de ruido, deja de ser útil.
- **Criterio de éxito**: cada sesión termina con daily consolidado + lecciones relevantes en LEARNINGS, sin duplicar.
- **Señal de listo**: al retomar una sesión, el daily del día anterior responde "dónde estábamos" sin re-descubrir.

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
- **Acciones**:
  - [ ] Agregar telemetría de fallos por modelo (cuándo rotar).
  - [ ] Verificar que el router cubre los tipos de tarea reales (code/review/long/cheap/writing).

### 1.3 Stack opinado como sistema 🟢 P1
- **Qué**: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG. Está decidido.
- **Por qué**: el valor está en la consistencia, no en la elección.
- **Criterio de éxito**: se aplica siempre, no cuando lo recordamos.
- **Señal de listo**: pre-commit hooks presentes en todos los proyectos activos; ADRs para decisiones nuevas.
- **Acciones**:
  - [ ] Auditar proyectos activos: ¿todos tienen pre-commit hooks? (regla: prioridad sobre features).

---

## Capa 2 - Portfolio (qué construimos)

### 2.1 Estrategia de proyectos 🟡 P0
- **Qué**: hay repos vivos, archivados, y candidatos a reset. La pregunta de fondo: ¿qué 2-3 proyectos sostienen el pitch "fullstack con IA como infraestructura"?
- **Por qué**: sin esto, el pipeline optimiza lo equivocado. Dispersión = portfolio que no cuenta una historia.
- **Criterio de éxito**: 2-3 proyectos claros que demuestran el pitch, el resto archivado o en pausa explícita.
- **Señal de listo**: una lista corta de proyectos "estrella" con su rol en el pitch, documentada.
- **Acciones**:
  - [ ] Definir los 2-3 proyectos ancla (candidatos: SoporteML, kanam-forge, a11y-fixer).
  - [ ] Decidir destino de accessible-ui y create-with-ai (reset con angle o archivar).
  - [ ] Documentar la decisión en un ADR.

### 2.2 Cadena OSS → LinkedIn 🟡 P1
- **Qué**: cada merge de a11y/agentic → post. El patrón está definido (2026-08-25); falta la cadencia real.
- **Por qué**: directamente ligado al objetivo laboral (nicho a11y/agentic).
- **Criterio de éxito**: cada merge de a11y/agentic genera un post en `docs/linkedin/` dentro de la semana.
- **Señal de listo**: 3+ posts publicados con el patrón didáctico, no solo drafts.
- **Acciones**:
  - [ ] Revisar si la cadencia se está cumpliendo o se definió y murió.
  - [ ] Verificar que cada post queda documentado en `docs/linkedin/`.

### 2.3 Búsqueda laboral 🟡 P0
- **Qué**: entrevista con OpenSistemas confirmada (25/08, 9AM) - perfil AI-Native, colaboración freelance 100% remoto LATAM.
- **Por qué**: es el objetivo activo; el roadmap debería capitalizar el resultado (entre o no).
- **Criterio de éxito**: resultado de la entrevista procesado y siguiente paso definido.
- **Señal de listo**: un track explícito de "preparar y capitalizar" el resultado.
- **Acciones**:
  - [ ] Preparar material (pitch, portfolio, PRs mergeados).
  - [ ] Definir el siguiente paso según el resultado (entra → onboarding; no entra → feedback + ajuste).

---

## Capa 3 - Crecimiento (hacia dónde vamos)

### 3.1 Evolución de las skills 🟡 P2
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
| 1 | 0.1 Estabilidad gateway | Fundaciones | P0 | 🔴 |
| 2 | 2.1 Estrategia de proyectos | Portfolio | P0 | 🟡 |
| 3 | 2.3 Búsqueda laboral | Portfolio | P0 | 🟡 |
| 4 | 0.2 Higiene workspace | Fundaciones | P1 | 🟡 |
| 5 | 0.3 Consolidación memoria | Fundaciones | P1 | 🟡 |
| 6 | 2.2 Cadena OSS→LinkedIn | Portfolio | P1 | 🟡 |
| 7 | 1.3 Stack opinado | Pipeline | P1 | 🟢 |
| 8 | 1.1 Pipeline A/B | Pipeline | P2 | 🟡 |
| 9 | 1.2 Ruteo de modelos | Pipeline | P2 | 🟡 |
| 10 | 3.1 Evolución skills | Crecimiento | P2 | 🟡 |
| 11 | 3.2 Segunda máquina | Crecimiento | P2 | 🟢 |

---

## Notas de creación

- Creado 2026-08-28 a partir de la sesión de refactor de Moderno AI Cleaner Pro (donde se diagnosticó la inestabilidad del gateway).
- La prioridad P0 de "Estrategia de proyectos" y "Búsqueda laboral" refleja que el pipeline optimiza lo equivocado si no sabemos qué construimos.
- Este documento es vivo: se actualiza cuando un item cambia de estado o se toma una decisión de prioridad.
