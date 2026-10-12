# OpenClaw Use Cases - Estudio del Curso

**Fuente:** roadmap.sh
**Alcance:** 30 lecciones
**Actualizado:** 2026-10-12

> **Reinicio (2026-10-12):** la carpeta anterior se borro (acumulaba tres planes de módulos contradictorios). Este índice arranca de cero con **un solo plan**, anclado a la numeración real del curso.

---

## Progreso

| Lección | Tema | Estado |
|---|---|---|
| M1 · L01 | Respuestas Autónomas en Canales de Chat Activos - `L01-respuestas-autonomas.md` | ✅ Completada |
| M1 · L02 | Filtrado Selectivo de Notificaciones y Menciones - `L02-filtrado-selectivo.md` | ✅ Completada |
| M1 · L03 | Configuración del Tono Asistido con SOUL.md - `L03-soul-tono.md` | ✅ Completada |
| M1 · L04 | Generación Dinámica de Resúmenes de Conversaciones - `L04-resumenes-dinamicos.md` | ✅ Completada |
| M1 · L05 | Derivación Segura de Mensajes a Operadores (Human-in-the-Loop) - `L05-handoff-operadores.md` | ✅ Completada |
| M2 · L06 | Configuración de Tareas Periódicas con Cron - `L06-cron-tareas-periodicas.md` | ✅ Completada |
| M2 · L07 | Monitorización del Sistema Mediante Heartbeats Periódicos - `L07-heartbeats.md` | ✅ Completada |
| M2 · L08 | Rutinas Nocturnas para Depurar Archivos Temporales (teaser del curso) | ⏳ Próxima |
| ... | (se completa con cada lección que pase Gonzo) | ❌ Pendiente |

**Completadas:** 7 / 30.

> ✅ **Módulo 1 completo** (*Asistentes de Mensajería Contextuales*, L01-L05). **Módulo 2 en curso** (*Tareas Programadas y Rutinas Autónomas*): tras la L07 el propio curso indica *"3 lessons left"* → Módulo 2 = 5 lecciones (L06-L10).

---

## Nota sobre el plan

El curso declara **30 lecciones**. Confirmado por el material:

- El nombre del Módulo 1: **Asistentes de Mensajería Contextuales**.
- Tras la L07 el curso indica *"3 lessons left in Tareas Programadas y Rutinas Autónomas"* → el Módulo 2 tiene **5 lecciones** (L06-L10).
- La Lección 8 anticipada: *Rutinas Nocturnas para Depurar Archivos Temporales*.

Los módulos 2-6 y las lecciones restantes **no se inventan**: se registran a medida que Gonzo comparte cada lección. El error del reinicio anterior fue fabricar un mapa de 6 módulos x 5 lecciones que no correspondía al curso.

---

## Procedencia del material

Las lecciones las **genera IA** (así funciona roadmap.sh). Patrón observado en las 7 primeras: **concepto/arquitectura correcta + detalles técnicos plausibles pero inventados** (comandos CLI, campos de config y APIs que no existen en OpenClaw real). Por eso cada ficha lleva una seccion **"Notas de verificacion (Kanam)"** que separa lo que mapea a la instalacion real de lo que es fachada pedagogica. Si una leccion viniera demasiado mal, se avisa a Gonzo para regenerarla (acuerdo 2026-10-12).

---

## Convención de archivos

- Un archivo por lección: `L<NN>-<slug>.md`.
- Cada archivo registra el contenido **fiel** de la lección, con una sección final de notas de verificación (qué del material es ilustrativo, qué es ejecutable, qué se contrastó contra la instalación real).
- El material del curso y los apuntes van en **español**.

---

## Relacionado

- `docs/adr/ADR-086-embudo-de-entrada-conversacional.md` - marco de los 5 patrones del embudo de entrada conversacional (deriva del Módulo 1 del curso).
- `docs/learnings/pipeline-agentes.md`, `docs/learnings/metodologia.md` - learnings del Módulo 1.
