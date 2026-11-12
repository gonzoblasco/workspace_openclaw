# HANDOFF - Curso fullstack-developer-scratch

**Fecha:** 2026-11-12 01:52 GMT-3
**Proyecto:** fullstack-developer-scratch
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> Punto de entrada para continuar el curso. El informe detallado vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

**Sesion de estudio tutorado del Nivel 1**, con un formato nuevo que pidió Gonzo: estudiar *a través mío* (mis conocimientos + research verificado), no leer el video.

1. **`nivel-1-clase-1-html.md`** (550 líneas): 9 bloques — etiquetas básicas, `img`/void tags, nesting, DevTools, doctype/head/body, listas, `button` vs `a`, `input type`, `anchor`+`href`. Cada bloque con su LAB, banco de ejercicios y checklist de 10 preguntas de autoevaluación.

2. **Investigación verificada contra MDN**, en los cuatro puntos donde el video se queda corto o dice algo que ya cambió:
   - `<meta charset="utf-8">` y `<meta name="viewport">` — el video los omite («no vamos a usar el `<head>` mucho») y sin ellos se rompen los acentos y el celular.
   - `<label for>` en vez de `placeholder` como etiqueta.
   - `rel="noopener"`: **MDN confirma que `target="_blank"` ya lo implica**. Corregí mi propio texto, que lo presentaba como defensa necesaria: es convención, no protección.
   - `width`/`height` en píxeles reales para dar la proporción antes de cargar y evitar *layout shift*.

3. **7 labs ejecutables** en `nivel-1/labs/`: cada uno con `index.html` roto a propósito, su `SOLUCION.html`, `check.py` (parser HTML con reglas por lab) y `run.sh` (estado de todos).

---

## Estado actual

- **Módulo actual:** Nivel 1 — clase teórica completa, labs entregados. **Ningún lab resuelto todavía (0/7).**
- **Ejercicios hechos:** 0 de 7. Los labs están en rojo esperando a Gonzo.
- **Preguntas abiertas:** ninguna bloqueante. Queda ver si hace los labs seguidos o de a uno, y si quiere que revise cada solución antes de seguir.
- **Próximo bloque:** `lab1` en verde, después `lab2`. Cuando el Nivel 1 cierre, el bloque CSS (Módulo 2 del curso, 1:04:19).

---

## Proximos pasos

1. Gonzo corre `./run.sh` y reporta qué labs tiene en verde.
2. Revisar **sus** `index.html` propios, no la `SOLUCION.html` mía.
3. Al cerrar el Nivel 1, montar la clase de CSS con el mismo formato: teoría corta + labs verificables.
4. **Vane** está apagado a propósito (`toolbox up vane`). Conviene encenderlo para el Nivel 4 (IA) y el Nivel 6 (React/Next), donde las versiones se mueven.

---

## Decisiones y contexto que no debe perderse

- **Dos bugs míos corregidos antes de entregar, y la lección que dejan:**
  - El output del checker imprimía `OK` justo cuando una regla fallaba: las reglas devuelven `(ok, mensaje_de_error)` y el print usaba el mensaje como si describiera el éxito.
  - `lab9` pasaba con HTML roto porque el checker buscaba `about.html` en el texto crudo y **los comentarios del enunciado nombran los archivos**: el gate se auto-satisfacía con la respuesta. Ahora quita comentarios antes de parsear y mira sólo los `href`.
  - **Regla general:** un checker se valida en las dos direcciones (roto falla, solución pasa). Sin eso es decorativo. Verificado: los 7 ejercicios FALLAN, las 7 soluciones PASAN.
- **Formato de estudio:** las clases ahora tienen labs ejecutables con checker, no ejercicios en papel. Gonzo dijo que después vienen skills, scripts y workflows — necesita práctica real, y armar un árbol de `<div>` correcto es el mismo músculo que armar un árbol de pasos.

---

## Cerrados

- **Por dónde arranca el curso:** Gonzo eligió el **Nivel 1**, y además cambió el formato a estudio tutorado con práctica, no lectura del video.
- **Capítulos 16:27:18 y 17:41:43 son recaps:** verificado en el transcript, documentado en `outline.md` y en el cierre del 2026-11-11. No vuelve a abrirse.

---

## Como continuar

1. Leer este HANDOFF (estado actual + próximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesión.
3. Verificar el estado real antes de actuar: `cd nivel-1/labs && ./run.sh`.

---

*Regenerado a mano el 2026-11-12 (el generador frenó por el merge guard: los dos ítems heredados se declararon en `## Cerrados`).*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
