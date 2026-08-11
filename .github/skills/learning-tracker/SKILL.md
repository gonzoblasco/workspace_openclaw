---
name: "learning-tracker"
description: "Study any topic in gamified levels (nivel → subnivel → topic), documenting in 3 artifact layers: master plan, per-level, progress tracker."
---

# Learning Tracker — Skill de OpenClaw

## Descripción

Estudia cualquier tema en **niveles gamificados**, documentando el conocimiento en **3 capas de artifacts** (plan maestro, artifact por nivel, registro de progreso). Reusable para cualquier curso o tema futuro: system design, un lenguaje nuevo, arquitectura, lo que sea.

**Patrón validado:** nivel → subnivel → topic. Cada topic es una unidad que se completa y verifica sola.

## Cuándo usar

- El usuario quiere estudiar un tema de forma estructurada y gamificada
- El usuario quiere que el aprendizaje quede documentado en artifacts reusables
- El usuario arranca un curso/bootcamp y quiere dejar un registro de lo que aprende
- El usuario quiere que futuras sesiones (o el mismo asistente) sepan cómo documentar su estudio
- El usuario quiere prepararse para una **entrevista / JD** específico (ver "Modo preparación de entrevista / JD")

## Los 3 principios del patrón

1. **Nivel → Subnivel → Topic** - cada nivel se divide en subniveles (bloques grandes) y cada subnivel en topics (piezas chicas). Cada topic es una unidad completa y verificable sola.
2. **Documentar en 3 capas** - no un documento gigante. Plan maestro (estático) + artifact por nivel (crece con el aprendizaje) + registro de progreso (se actualiza cada paso).
3. **Gamificar** - XP por topic, badges por nivel, streak de práctica, jefe final (mock interview / evaluación completa).

## Los 3 artifacts (la estructura de documentación)

### Capa 1 - Plan maestro (un solo artifact, estático)
La hoja de ruta completa: todos los niveles con sus subniveles y topics. Se actualiza POCO - solo cuando cambia la estructura del curso.

```
Nivel 1 - <Tema>
├── Subnivel 1.1 - <Bloque temático>
│   ├── Topic: <pieza chica>
│   └── Topic: <pieza chica>
├── Subnivel 1.2 - <Bloque temático>
└── ...
```

Contiene también: filosofía del curso, recursos externos (mapeados a niveles), gamificación, tabla de progreso.

### Capa 2 - Artifact por nivel (uno por nivel, crece con el aprendizaje)
El cuaderno del nivel: teoría completa, topics, prácticas, verificación, self-review. Se actualiza CUANDO AVANZAS.

```
# Nivel N - <Tema>
Badge: <emoji> <nombre> | Recursos: <mapeo>

## Subnivel N.1 - <Bloque>
### Topic: <pieza>
- Teoría (conceptos con nombre, vocabulario)
- Práctica (lo que se diseñó/hizo)
- Verificación (mini-preguntas, mock interview)
```

### Capa 3 - Registro de progreso (un solo artifact chico, gamificado)
El tablero: tabla de qué topics completaste, XP, badges, streak. Se actualiza DESPUÉS DE CADA topic (cambio chiquito).

```
# Progreso - <Curso>

| Nivel | Subnivel | Topic | Estado | XP |
|-------|----------|-------|--------|----|
| 1 | 1.1 | qué es system design | ✅ | 10 |

XP total: N | Badges: N | Streak: N días
```

## Workflow

### 1. Armar el plan maestro (inicio del curso)

1. Preguntar (o inferir) el tema, el objetivo, y si hay recursos externos (cursos, libros, videos)
2. Diseñar los niveles (5-10 típico, depende del tema)
3. Dividir cada nivel en subniveles y topics
4. Identificar los niveles críticos (el core del objetivo)
5. Crear el artifact del plan maestro (Capa 1)
6. Crear el artifact del registro de progreso (Capa 3) vacío

### 2. Por cada topic

1. Dar la teoría (conceptos con nombre, vocabulario)
2. Guiar la práctica (ejercicio, diseño, problema)
3. Verificar con una mini-pregunta o mock interview
4. Actualizar el artifact del nivel (Capa 2) con lo aprendido
5. Actualizar el registro de progreso (Capa 3) - marcar topic ✅, sumar XP

### 3. Por cada nivel

1. Completar todos los topics
2. Mock interview / evaluación completa del nivel
3. Self-review (rúbrica: qué salió bien, qué faltó)
4. Actualizar el artifact del nivel (Capa 2) con el cierre
5. Otorgar badge del nivel

### 4. Jefe final (al final del curso)

1. Evaluación completa estilo entrevista/examen (si aplica)
2. Cierre del registro de progreso (Capa 3)
3. Actualizar el plan maestro (Capa 1) si hace falta
4. Celebrar 🎉

## Modo preparación de entrevista / JD (validado 2026-08-11)

Cuando el usuario pide **"preparame para esta entrevista / puesto"**, el patrón base se enriquece con dos conceptos. La entrada puede venir de **dos fuentes**:

**Input A - JD formal** (job description): extraer stack, frameworks, niveles críticos y formato de evaluación del documento.

**Input B - Lista de temas externa** (de otra IA, un curso, un colega, el usuario mismo): no es un JD - es una lista de temas que alguien considera relevantes para la entrevista. El trabajo es:
- **Validar** la lista (¿cubre lo que realmente evalúa el puesto? ¿hay gaps?).
- **Estructurarla** en niveles → subniveles → topics (la lista cruda no tiene jerarquía).
- **Ampliarla** con el contexto del usuario (ej. "el rol usaba Pages Router → el App Router es el gap real a priorizar").
- **Verificar** temas antes de citar detalles (precios/fechas/specs se chequean con web_fetch - regla de Gonzo).

**Variante de Input B - URL de índice de libro:** si el usuario pasa una URL (ej. Packt, O'Reilly, mirror), hacer `web_fetch` para extraer el índice real y usarlo como **fuente de verdad de qué cubrir** (los capítulos definen la jerarquía). Notas:
- Los sitios de editoriales suelen bloquear con 403 anti-bot (Cloudflare) - si falla el fetch directo, buscar el TOC en mirrors o con web_search.
- El índice es el mapa de contenidos; la teoría la genera el agente (puede tener huecos - verificar specs finos).
- Agrupar los capítulos en niveles lógicos (no todos los capítulos son un nivel - agrupar por bloque temático).
- Preguntar el **objetivo** del curso del libro (entrevista / aprender completo / complementar) porque define los niveles críticos.
- **Validado 2026-08-11:** "Full-Stack React, TypeScript, and Node" 2nd ed (Packt) - se extrajo el TOC de 15 capítulos de un mirror y se estructuró en 8 niveles temáticos.

### 1. Driver explícito condiciona todo el diseño

- El **objetivo de la entrevista/puesto es el input** del diseño del curso, no un tema genérico.
- Del driver (JD o lista + contexto) se extrae: qué evalúa (stack, frameworks, patrones), los **niveles críticos** (el core del objetivo), y el **formato de evaluación** (mock interview técnica, quiz, etc.).
- El diseño apunta a cubrir lo que evalúa el puesto, no a ser exhaustivo en el tema.
- Ej: puesto de consultora que pide Next moderno → niveles de App Router, estado, testing; el gap real (Pages Router legacy del rol) se prioriza.

### 2. Dos pasadas: mapa → profundidad

**Primera pasada (mapeo):** documentar TODO el contenido en los artifacts (panorama + vocabulario + verificación por topic), creando el **mapa completo de referencia**. No suma XP - es el "qué hay".

**Segunda pasada (dominio):** reiniciar topic por topic **en profundidad** - práctica real (ejercicios, migraciones, diseño), verificación en voz alta con respuesta esperada, sumando XP por cada topic. Es el "dominarlo".

**Por qué dos pasadas:**
- La primera pasada deja toda la referencia documentada y un listado general del contenido.
- La segunda pasada profundiza cada pieza sin re-descubrir el mapa - ya está todo referenciado.
- Separa **documentar ≠ dominar**: el XP se gana al dominar, no al mapear.
- El jefe final (mock interview completa) cierra el curso.

### Workflow del modo preparación de entrevista

1. **Recibir el driver** - JD formal (extraer stack/niveles críticos) O lista de temas externa (validar + estructurar + ampliar con contexto del usuario)
2. Armar plan maestro (Capa 1) + registro de progreso (Capa 3) vacío
3. **Primera pasada:** documentar todos los subniveles/niveles en los artifacts de nivel (Capa 2) - panorama + vocabulario + verificación. Sin XP.
4. **Segunda pasada:** reiniciar topic por topic en profundidad con práctica + verificación en voz alta. Sumar XP.
5. **Jefe final:** mock interview completa estilo la evaluación real.
6. Actualizar progreso (Capa 3) + daily note en cada hito.

**Validado en:** System Design Bootcamp (primera versión) + Curso Stack React/Next para Entrevista EY (2026-08-11, donde se formalizaron las dos pasadas y la entrada por lista de temas de otra IA).

## Reglas

- **Nivel → Subnivel → Topic**, no al revés (el subnivel es el bloque grande, el topic la pieza chica)
- **Cada topic se verifica solo** - no esperar a terminar todo el nivel
- **3 capas de artifacts**, no un documento gigante (escalabilidad de edición + repaso dirigido)
- **El plan maestro se actualiza poco** - solo cuando cambia la estructura
- **Los artifacts del nivel crecen** con el aprendizaje
- **El progreso se actualiza después de cada topic** - cambio chiquito
- **Vocabulario con nombre** en cada topic (los términos que separan al que sabe del que improvisa)
- **Verificación por mock interview / pregunta en voz alta** cuando el formato final es entrevista
- **Gamificar** - XP, badges, streak, jefe final
- **Idioma:** documentar en el idioma de la sesión del usuario (español en el caso de Gonzo)
- **Guion comun (-)** nunca em dash (regla de Gonzo)
- Los artifacts NO se comparten públicos (son material de estudio personal)

## Relación con otros skills

- **technical-book-processor** - procesa libros capítulo por capítulo. learning-tracker es más general: estudiar cualquier tema en niveles, no solo libros.
- **curriculum-builder** - construye tutores con IA (frontend + motor). learning-tracker documenta el estudio del usuario en artifacts, no construye un tutor.
- **content-serializer** - serializa contenido. learning-tracker es sobre la estructura de documentación del aprendizaje.

## Ejemplo (validado - System Design Bootcamp)

- **Tema:** system design para entrevista de Greenhouse
- **Niveles:** 10 (fundamentos → arquitectura → data → SaaS integrations → escalabilidad → observabilidad → AI/agentic → sistema completo → mock interview → proyecto real)
- **Niveles críticos:** N4 (SaaS integrations) y N7 (AI/agentic) - el core del JD
- **Estructura:** nivel → subnivel → topic, con topics verificables solos
- **Documentación:** 3 artifacts (plan maestro, uno por nivel, registro de progreso)
- **Verificación:** mock interview por nivel (el formato que evalúa la entrevista)
- **Recursos externos:** Udemy (system design de entrevista) + LinkedIn Learning (arquitectura de software), mapeados a niveles
