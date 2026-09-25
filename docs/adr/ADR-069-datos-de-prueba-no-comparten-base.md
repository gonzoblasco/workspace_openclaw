# ADR-069: los datos de prueba no comparten base con los datos reales

**Fecha:** 2026-09-25
**Estado:** Aceptado (regla). La separacion fisica de bases: **pendiente** (deuda registrada)
**Decisores:** Gonzo / Kanam
**Origen:** Kanam destruyo datos reales de Gonzo corriendo un script de verificacion
**Relacionado:** ADR-070 (via de recuperacion), ADR-067 (verificar el sujeto antes de borrar)

---

## Contexto

Al verificar el fix de apply por candidato escribi
`projects/kanam-story-bible/scripts/verify_apply.py` y, en la
primera corrida, **apunte el script al mundo real de Gonzo** (`Cartas sin Mandar`) en
vez de crear uno descartable. Ese script creo 3 fichas ahi.

Despues, al limpiar lo que identifique como "basura de test", vi esas 3 fichas como
mias y las borre. Lo eran en origen, pero el efecto neto fue que **el mundo de Gonzo
quedo vacio sin que el hubiera hecho nada**. El sintoma que el reporto ("no veo ficha
alguna") era mi dano, no un bug del producto.

Segundo efecto del mismo problema: los scripts `smoke.py`, `seed_demo.py` y
`verify_apply.py` dejan sus mundos en la misma base. En una sola sesion se acumularon
**6 mundos de prueba** mezclados con los 2 reales. Gonzo los ve en el selector de
mundos: ruido que parece contenido.

El proyecto no tiene base de test. `compose.dev.yml` levanta un Postgres y los scripts
apuntan al mismo `kanam` que la UI.

## Decision

**Un script que escribe no toca un mundo que no creo el mismo.** Concretamente:

1. Todo script de verificacion crea su propio mundo (titulo identificable, con marca de
   test) y **registra el id que le devolvio la API**.
2. La limpieza borra **por id registrado**, nunca por heuristica sobre titulos o
   contenido. Un `DELETE ... WHERE title LIKE 'Los nombres del rio%'` puede borrar un
   mundo real con ese titulo.
3. Ningun script apunta a un id hardcodeado de un mundo real. Si un caso necesita datos
   reales, se **copian** a un mundo de test.
4. La API de borrado exige el titulo exacto en `X-Confirmar-Titulo` (implementado en
   esta misma sesion): ese candado protege contra el id mal copiado, no contra la
   heuristica mala. Ambos hacen falta.

## Evidencia

- Las 3 fichas borradas por error se recuperaron con `POST /projects/{id}/entities/{eid}/restore`
  (implementado en esta sesion, ver ADR-070). Sin esa via, el dano era irreversible.
- Los 6 mundos de prueba se borraron con `DELETE /projects/{id}` usando el titulo exacto.
- Estado final verificado: 2 mundos, los de Gonzo, con sus fichas.

## Consecuencias

- Los scripts de verificacion pasan a ser **autolimpiantes**: crean, verifican, borran su
  mundo al final (incluso si fallan, con `finally`).
- **La base separada es el arreglo de fondo y sigue pendiente.** Mientras no exista, la
  regla 1-4 es la unica proteccion, y depende de que cada script la respete. Queda como
  deuda en `.knowledge/STATUS.md` del proyecto.
- Corolario incomodo: el mismo patron aplica a los tests de UI, que hoy mockean `fetch`
  y por eso no escriben. Si alguno pasa a pegarle a la API real, cae en esta regla.

## Alternativas descartadas

- **Confiar en el `deleted_at` y limpiar despues:** es lo que hice, y fue exactamente el
  dano. Una heuristica de "esto parece basura" sobre datos que no distingue de quien son.
- **Borrar por titulo con patron:** descartado por la regla 2. El titulo no es un
  identificador de propiedad.
