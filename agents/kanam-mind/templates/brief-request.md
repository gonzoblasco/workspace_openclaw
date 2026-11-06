# Template `brief-request` - el pedido que le llega a Kanam MIND

> Propuesta de MIND para el Hito 5.0 del `ROADMAP.md`. **No se aplica solo:** el `AGENTS.md` del
> CORE es gobierno del CORE; esto queda listo para que el CORE (o Gonzo) lo integre.
> Copia de esto vive en `agents/kanam-mind/templates/brief-request.md`.

## Cuándo se usa

Cuando el pedido cae en una de estas cuatro clases:

| Clase | Ejemplo | Qué devuelve MIND |
|---|---|---|
| `research` | "¿Cómo cobra Tempo y qué rol de Growth tiene?" | Brief con fuentes abiertas y fechas |
| `verify` | "¿Es cierto lo que reportó DEV sobre X?" | Veredicto con cita abierta, o incógnita explícita |
| `study` | "Procesá el capítulo 3 de <libro>" | Aprendizajes citados + acción (ADR/nota) |
| `audit` | "Auditá las citas de este documento" | `PASS`/`PARTIAL`/`FAIL` reproducible |

**No es de MIND:** redactar contenido o posts (STUDIO), tesis de UI (AUDITOR/DEV), implementar código
(DEV), automatizaciones o config (OPS).

## Cómo se pide

`sessions_spawn(agentId: "kanam-mind", context: "isolated")` con este cuerpo:

```md
Clase: research | verify | study | audit
Pregunta: <una sola pregunta, en imperativo>
Criterio de parada: <qué la resuelve; si no viene, lo propongo y lo confirmo antes de buscar>
Frescura: <sí/no - qué dato cambia con el tiempo (precio, versión, estado de PR, fecha)>
Fuentes obligatorias: <repo/doc/changelog a abrir; si no, yo elijo primarias>
Home del artefacto: <ruta exacta del .md; si no viene, agents/kanam-mind/reports/<slug>-<fecha>.md>
Presupuesto: <tiempo o número de fuentes; si no viene, corto cuando el criterio de parada se cumple>
Límite de aprobación: <qué NO está aprobado: publicar, salir del workspace, comprar, borrar>
```

Sin `criterio de parada` explícita, MIND **no empieza a buscar**: lo propone.

## Qué devuelve siempre (contrato de handoff)

- **Ruta exacta** del brief (o la pregunta por la que no se pudo cerrar).
- **Veredicto del gate** (`kb-audit.py`: `PASS`/`PARTIAL`/`FAIL`), no "quedó bien".
- **Fuentes abiertas**, con fecha las que caducan.
- **Incógnitas** declaradas como tales.
- **Entrada en el journal** (`brief-journal.py`) con el veredicto.

**Un "está verificado" de MIND es un reporte, no una prueba.** El estándar del CORE sigue siendo
reproducir la salida del gate.

## El límite que no se delega

MIND investiga y verifica; **no publica, no contacta, no manda nada hacia afuera**. Eso lo decide
Gonzo, aunque MIND tenga la herramienta.

## Bloque sugerido para el `AGENTS.md` del CORE (Hito 5.0)

> **Conocimiento: el CORE llama a MIND, y MIND no redacta.** La investigación de mercado/empresa/
> tecnología, la verificación de una afirmación ajena, la ingesta de material de estudio y la
> auditoría de citas son de `kanam-mind` (ADR-074). No las hago yo aunque parezcan un párrafo: las
> delego con `sessions_spawn(agentId: "kanam-mind")`. Qué pedir, qué devuelve y el límite de
> aprobación: **`docs/MIND-DISPATCH.md`**. Redacción y marca siguen siendo de `kanam-studio`; UI, de
> `kanam-auditor`; código, de `kanam-dev`.
