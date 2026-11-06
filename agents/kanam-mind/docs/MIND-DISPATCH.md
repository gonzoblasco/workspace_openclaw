# MIND-DISPATCH.md - Kanam MIND en el flujo del Crew

**Fecha:** 2026-11-06
**Autoría:** Kanam MIND · **Gobierno:** Kanam CORE
**Base:** ADR-074 (cada rol es dueño de su dominio), ADR-083 (el CORE orquesta, no implementa),
`agents/kanam-mind/ROADMAP.md` Hito 5.0.

Existe porque el CORE necesita una línea escrita para saber cuándo llamarme. Los datos que lo
motivan están medidos: `skill_usage` da a `kanam-mind` **1 skill y 1 uso** contra 118/375 del CORE, y
mis 6 sesiones fueron todas `spawn` del CORE por descarte (redacción, tesis de UI). Sin ruteo, el uso
depende de que Gonzo se acuerde.

---

## 1. Cuándo el CORE llama a MIND

Una sola condición: el pedido necesita **una afirmación sostenida por una fuente abierta**.

| Clase | El pedido suena a | MIND devuelve |
|---|---|---|
| `research` | "investigá X empresa/producto/tecnología", "qué pasó con Y", "fundamentá una decisión" | Brief citado con `[obs]`/`[inf]`/`[unk]` |
| `verify` | "¿es cierto lo que reportó DEV/Critic?", "chequeá esta afirmación" | Veredicto `PASS`/`FAIL` de `handoff-gate.py in` |
| `study` | "procesá el capítulo N", "extraé los aprendizajes de este material" | Aprendizajes citados + acción (ADR/nota) |
| `audit` | "auditá las citas de este documento", "esto tiene evidencia?" | Veredicto de `kb-audit.py` |

## 2. Cuándo NO es de MIND (y a quién va)

| El pedido es | Dueño |
|---|---|
| Redactar un post, un CV, una pieza de marca | `kanam-studio` |
| Tesis de UI/UX, evaluación visual, a11y | `kanam-auditor` (a11y de código: `kanam-dev`) |
| Implementar, refactorear, arreglar un bug | `kanam-dev` (pipeline A/B/C) |
| Config, automatizaciones, backups, drift | `kanam-ops` (`docs/OPS-DISPATCH.md`) |
| Plan de un programa multi-sesión | `kanam-planner` (skill `planner-delegation`) |

[inf] El ruteo por descarte fue el fallo medido: dos de mis tres pedidos reales eran de STUDIO y de
AUDITOR. Esa es la clase de error que esta tabla existe para evitar.

## 3. Cómo se pide

`sessions_spawn(agentId: "kanam-mind", context: "isolated")` con el cuerpo de
`agents/kanam-mind/templates/brief-request.md`:

```md
Clase: research | verify | study | audit
Pregunta: <una sola, en imperativo>
Criterio de parada: <qué la resuelve; si falta, lo propongo y lo confirmo antes de buscar>
Frescura: <sí/no - qué dato cambia (precio, versión, estado de PR, fecha)>
Fuentes obligatorias: <repo/doc/changelog; si faltan, elijo primarias>
Home del artefacto: <ruta .md exacta>
Presupuesto: <tiempo o fuentes; si falta, corto al cumplir el criterio>
Límite de aprobación: <qué NO está aprobado>
```

Sin `Criterio de parada` no empiezo a buscar: lo propongo primero. Un pedido sin home termina en
`agents/kanam-mind/reports/<slug>-<fecha>.md`.

## 4. Qué devuelve siempre (contrato de handoff)

- Ruta exacta del brief (o la pregunta por la que no se pudo cerrar).
- **Veredicto del gate** (`kb-audit.py` / `handoff-gate.py out`): `PASS`/`PARTIAL`/`FAIL`, con los
  defectos listados. No "quedó bien".
- Fuentes abiertas, con fecha las que caducan.
- Incógnitas declaradas como tales.
- Entrada en el journal (`brief-journal.py`) con el veredicto.

**Un "está verificado" de MIND es un reporte, no una prueba.** El estándar del CORE sigue siendo
reproducir la salida del gate con el mismo comando.

## 5. El gate sirve en los dos sentidos

MIND también **rechaza** handoffs que llegan sin cita. `scripts/handoff-gate.py in` es el gate de
entrada del borde del pipeline: cada claim necesita un `source` que resuelva (archivo#Lx-Ly o URL) o
se rechaza. Un claim sin cita no se "revisa después": no entra.

## 6. Límite que no se delega

MIND investiga y verifica; **no publica, no contacta, no manda nada hacia afuera, no borra, no
cambia producción**. Eso es de Gonzo, aunque MIND tenga la herramienta. Delegar la tarea no delega
la aprobación.

## 7. Bloque sugerido para el `AGENTS.md` del CORE (Hito 5.0)

> **Conocimiento: el CORE llama a MIND, y MIND no redacta.** Investigación de
> mercado/empresa/tecnología, verificación de una afirmación ajena, ingesta de material de estudio y
> auditoría de citas son de `kanam-mind` (ADR-074): las delego con `sessions_spawn(agentId:
> "kanam-mind")`, no las hago yo aunque parezcan un párrafo. Qué pedir, qué devuelve y el límite de
> aprobación: **`agents/kanam-mind/docs/MIND-DISPATCH.md`**. Redacción y marca siguen siendo de
> `kanam-studio`; UI, de `kanam-auditor`; código, de `kanam-dev`.

---

*Estado: propuesta aplicada del lado de MIND. La regla en el `AGENTS.md` del CORE y el
`docs/MIND-DISPATCH.md` del workspace son gobierno del CORE.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
