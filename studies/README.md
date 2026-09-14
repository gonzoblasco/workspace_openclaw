# STUDIES.md - Índice Maestro de Estudios

**Última actualización:** 2026-08-26

> Fuente de verdad unica para todo estudio (cursos y libros). Gestionado por la skill `study-tracker` (fusion de study-tracker + learning-tracker, 2026-08-26).
> **Regla dura:** todo vive en `studies/<slug>/`. NUNCA crear `study/` (singular) ni otra ruta.

---

## 🎓 CURSOS (online - estructura de lecciones)

| Curso | Plataforma | Estado | Estructura |
|---|---|---|---|
| **agentic-ai-mastery** | Codecademy | En curso - Track 1, Course 2 (video 1/10) | `agentic-ai-mastery/` |

## 📚 LIBROS (estudio gamificado - niveles/XP/badges)

| Libro | Autor / Editorial | Estado | Estructura |
|---|---|---|---|
| **openclaw-ai-in-production** | Ken Huang (Packt, 2026) | En curso - 3/13 capitulos mapeados | `openclaw-ai-in-production/` |

---

## 🧩 TEMAS TECNICOS (estudio gamificado - niveles/XP/badges)

| Tema | Motivo | Estado | Estructura |
|---|---|---|---|
| **radix-primitives** | Entro al stack por el template, sin decision documentada. Es la capa que resuelve foco, ARIA y teclado en nuestras UIs. | Nivel 1 abierto - mapeo (5 niveles / 46 topics) | `radix-primitives/` |

---

## 📋 Notas

- Todo estudio vive en `studies/<curso-slug>/` con su propio `README.md` (portada + progreso).
- **Cursos (lecciones):** `notes/NN-titulo.md` (espanol, guion comun), `exercises/`, `quiz/`.
- **Libros / entrevistas (gamificado):** `PLAN-MAESTRO.md` + `nivel-N-tema.md` + `PROGRESO.md` (3 capas, XP/badges/streak).
- Para agregar un estudio: crear `studies/<slug>/`, su `README.md`, y agregar a la tabla de arriba.
- Los apuntes son material personal de referencia - en espanol, no van a GitHub como portfolio.
- **Migracion 2026-08-26:** fusion de study-tracker + learning-tracker en `study-tracker`. Se movio el libro de Packt de `study/` (singular) a `studies/`. Ver skill y CHANGELOG.
