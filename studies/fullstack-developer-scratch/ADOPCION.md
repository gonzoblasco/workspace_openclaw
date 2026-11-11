# ADOPCIÓN — Become a Fullstack Developer from Scratch

**Fecha:** 2026-11-11 · **Curso:** 47:29:20 · freeCodeCamp / Scrimba

## Veredicto

**Sin adopción en esta pasada.** El curso es una ruta de *aprendizaje de oficio* (HTML/CSS/JS/React/Node), no un curso que corrija una práctica del workspace. Nada de lo que enseña cambia cómo trabajamos hoy porque **no escribimos front-end ni back-end de producción en este workspace**: lo que hacemos es orquestar, documentar y gobernar.

Revisé las ideas que podrían morder contra el estado real del repo antes de descartarlas:

| Idea del curso (con t=) | Qué hacemos hoy | Veredicto |
|---|---|---|
| El event loop explica por qué `setTimeout(0)` no corre antes de la línea siguiente (`(17:00:07)`) | No hay código async propio en el workspace; los scripts son `exec` batch y los subagentes son del gateway | **Sin adopción** — cubierto por el runtime, no por nosotros |
| Un `WHERE` con `AND`/`OR` sin paréntesis filtra mal en silencio (`(25:50:01)`) | Las consultas a `memory.db` las escribe `sqlite3` directo con queries simples y los scripts de memoria | **Sin adopción** — el patrón de riesgo no existe en nuestras queries actuales |
| `setCount(c => c + 1)` cuando el nuevo valor depende del anterior (`(32:13:31)`) | No hay React en el workspace | **Sin adopción** — fuera de alcance |
| Un `default export` por archivo (`(15:58:20)`) | Los módulos ES del workspace ya siguen eso; no hay exports duplicados | **Sin adopción** — la clase no cambia nada porque ya está bien |
| El curso declara fuera de alcance auth, testing, deploy y DB real (`(22:42:51)`) | — | **Registro de límites**, no de adopción |

**Lo que sí vale del curso:** es el mapa más completo que tenemos de la ruta fullstack, y está registrado para cuando Gonzo se siente a hacer los ejercicios (que es el uso previsto: aprender haciendo, no leer). El outline y el banco de 30 preguntas son el material de esa práctica.

## Candidato a futuro (no escrito)

Si algún día escribimos front-end en el workspace (una UI de proyecto propio), el primer artefacto que saldría de acá es un **checklist de `useEffect`**: que todo `fetch` esté en el efecto con `[]`, que haya estado de carga y de error, y que ninguna dependencia falte. Hoy no hay a qué aplicarlo: sería un gate sin caso.

## Lo que este curso no cubre (y por eso no puede ser la base de nada que hagamos)

Testing, autenticación, deploy en producción y una DB conectada al backend. Un "fullstack" que sale sólo con este video sabe construir, no sabe operar. Si en algún momento el workspace necesita eso, la fuente es otra.
<!-- project: github.com/gonzoblasco/workspace_openclaw -->
