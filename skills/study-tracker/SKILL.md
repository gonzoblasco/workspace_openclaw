---
name: "study-tracker"
description: "One skill to rule them all: estructura de cursos + gamificacion (niveles/XP/badges) en una sola fuente de verdad bajo studies/<slug>/."
metadata:
  category: "Learning"
  tags:
    - estudios
    - cursos
    - libros
    - documentacion
    - progreso
    - gamificacion
user-invocable: true
---

# Study Tracker - One Skill to Rule Them All

Skill unica de estudio. Fusiona lo que antes eran dos skills (study-tracker y learning-tracker) en una sola fuente de verdad bajo `studies/`. Sirve para CUALQUIER estudio: cursos online (Codecademy, Udemy, etc.), libros tecnicos (Packt, O'Reilly), bootcamps, preparacion de entrevistas, temas sueltos.

## Fuente de verdad unica (IMPORTANTE)

**TODO estudio vive en `studies/<slug>/`.** Nunca usar `study/` (singular) ni ninguna otra ruta. El indice maestro es `studies/README.md` - todo curso/libro se registra ahi.

Razones:
- `studies/` es la convencion que ya documentaba el indice maestro (era la de study-tracker).
- learning-tracker era agnostico de rutas y eso causo la inconsistencia: el libro de Packt quedo en `study/` (singular) mientras el curso de Codecademy estaba en `studies/`.
- Al fusionar, la regla es una sola: **todo en `studies/<slug>/`**.

## Dos modos de estudio

La skill fusiona las dos capacidades:

### Modo A - Estructura de curso (viene de study-tracker)
Para cursos con lecciones/videos/quizzes (ej. Codecademy, Udemy):
```
studies/<slug>/
├── README.md          # portada + tabla de progreso
├── <track>/           # opcional, solo si el curso tiene tracks
│   └── <course>/
│       ├── notes/NN-titulo.md      # notas por leccion/video (espanol, guion comun)
│       ├── quiz/NN-pregunta.md      # knowledge checks + respuestas modelo
│       └── exercises/               # ejercicios practicos
```

### Modo B - Estructura gamificada (viene de learning-tracker)
Para estudio profundo con niveles, XP y badges (libros, preparacion de entrevista, temas estructurados):
```
studies/<slug>/
├── PLAN-MAESTRO.md    # Capa 1: todos los niveles + subniveles + topics (estatico)
├── nivel-N-tema.md    # Capa 2: cuaderno por nivel (crece con el aprendizaje)
└── PROGRESO.md        # Capa 3: tabla de progreso, XP, badges, streak
```

Los dos modos **no son excluyentes**: un curso online tambien puede gamificarse con niveles/XP (Modo B sobre la estructura del Modo A). Y un libro puede llevar notas de leccion. La regla es que **todo vive bajo `studies/<slug>/`** - lo demas es formato.

## El patron de gamificacion (de learning-tracker)

**Nivel → Subnivel → Topic**, no al reves. Cada topic es una unidad que se completa y verifica sola.

1. **Nivel → Subnivel → Topic** - nivel en bloques grandes, subnivel en piezas chicas.
2. **Documentar en 3 capas** - plan maestro (estatico) + artifact por nivel (crece) + registro de progreso (se actualiza cada paso).
3. **Gamificar** - XP por topic, badges por nivel, streak de practica, jefe final (mock interview / evaluacion completa).

## Workflow

### 1. Arrancar un estudio nuevo
1. Determinar el **objetivo** (aprender un curso / preparar entrevista / leer un libro / complementar).
2. Crear `studies/<slug>/` con su `README.md` (portada + progreso).
3. Si es gamificado: crear `PLAN-MAESTRO.md` (Capa 1) + `PROGRESO.md` (Capa 3) vacio.
4. Registrar en el indice maestro `studies/README.md`.

### 2. Por cada unidad (leccion, video, capitulo)
1. Dar la teoria (conceptos con nombre, vocabulario) - espanol, guion comun.
2. Guiar la practica (ejercicio, diseno, problema) si aplica.
3. Verificar con una pregunta / mock interview.
4. Actualizar la nota / artifact de nivel (Capa 2) con lo aprendido.
5. Actualizar el progreso (Capa 3) - marcar, sumar XP.

### 3. Por cada nivel
1. Completar todos los topics.
2. Mock interview / evaluacion completa del nivel.
3. Self-review (rubrica: que salio bien, que falto).
4. Otorgar badge del nivel.

### 4. Jefe final (fin del estudio)
1. Evaluacion completa estilo entrevista/examen (si aplica).
2. Cierre del progreso (Capa 3).
3. Actualizar el plan maestro (Capa 1) si hace falta.
4. Registrar el hito en el daily.

## Modo preparacion de entrevista / JD (viene de learning-tracker)

Cuando el objetivo es prepararse para un puesto, se enriquece:

**Dos fuentes de entrada:**
- **Input A - JD formal** (job description): extraer stack, frameworks, niveles criticos, formato de evaluacion.
- **Input B - Lista de temas externa** (de otra IA, un curso, el usuario): validar la lista, estructurarla en niveles/subniveles/topics, ampliarla con contexto del usuario, verificar temas antes de citar detalles (web_fetch si son precios/fechas/specs - regla de Gonzo).

**Variante de Input B - URL de indice de libro:** si el usuario pasa una URL (Packt, O'Reilly, mirror), hacer `web_fetch` para extraer el indice real y usarlo como fuente de verdad de que cubrir. Si el fetch directo falla (403 anti-bot/Cloudflare), buscar TOC en mirrors o con web_search. Agrupar los capitulos en niveles logicos.

**Dos pasadas (mapa → profundidad):**
- **Primera pasada (mapeo):** documentar TODO el contenido (panorama + vocabulario + verificacion), creando el mapa de referencia. No suma XP.
- **Segunda pasada (dominio):** reiniciar topic por topic en profundidad - practica real, verificacion en voz alta, sumando XP.

## Reglas

- **Todo bajo `studies/<slug>/`** - NUNCA `study/` ni otra ruta. Una sola fuente de verdad.
- **Nivel → Subnivel → Topic**, no al reves.
- **Cada topic se verifica solo** - no esperar a terminar el nivel.
- **3 capas de artifacts** para el modo gamificado, no un doc gigante.
- **El progreso se actualiza despues de cada paso** - cambio chiquito.
- **Vocabulario con nombre** en cada topic.
- **Gamificar** - XP, badges, streak, jefe final.
- **Idioma:** documentar en el idioma de la sesion (espanol con Gonzo).
- **Guion comun (-)** nunca em dash (regla de Gonzo).
- **Los artifacts NO se comparten publicos** (material de estudio personal).
- Si un ejercicio crece a "proyecto demo" con complejidad real, moverlo a `projects/` (vive con su propio repo).

## Relacion con otros skills

- **technical-book-processor** - procesa libros tecnicos cap por cap generando ADRs y un proyecto de portfolio en `projects/`. study-tracker es para el estudio personal del usuario (en `studies/`); technical-book-processor es para dejar un trail publico/portfolio. Se complementan.
- **curriculum-builder** - construye tutores adaptativos con IA (frontend + LLM). study-tracker documenta el estudio del usuario; curriculum-builder construye un tutor para otros.
- **content-serializer** - serializa contenido. study-tracker es sobre la estructura de documentacion del aprendizaje.

## Migracion desde las skills anteriores

Este skill reemplaza a `study-tracker` (estructura de cursos) y `learning-tracker` (gamificacion), fusionadas. Al migrar:
- Mover cualquier cosa en `study/` a `studies/<slug>/` (git mv) y eliminar `study/`.
- Mantener `studies/README.md` como indice maestro, actualizado con todos los estudios.
- Los artifacts de gamificacion (PLAN-MAESTRO, PROGRESO, niveles) viven igual bajo `studies/<slug>/`.
