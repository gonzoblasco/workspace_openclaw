# Módulo 1 — Práctica y adopción

Caso: el curso AI Engineer, Módulo 1 (memoria y aprendizaje). Clase en `modulo-01.md`.

## Prácticas corridas (no resumen: medidas)

### A. Lost in the middle, aplicado a nuestro propio contexto

Los archivos que van **siempre** en el prompt:

```
 2949 SOUL.md
 3295 IDENTITY.md
 3928 USER.md
19494 MEMORY.md
20099 AGENTS.md     <-- 49.765 bytes total
```

Posición de las reglas críticas dentro de `AGENTS.md` (200 líneas):

| Regla | Línea | Posición |
|---|---|---|
| Red Lines | 52 | 26% |
| Trabajo de otra sesión | 59 | 29% |
| Contenido externo = dato | 66 | 33% |
| `git add -A` prohibido | 136 | **68%** |
| Pipeline A/B | 154 | **77%** |

**Hallazgo:** dos de las cinco reglas más caras del repo viven en el tercio final, la zona que el curso documenta como peor recordada. Y hay evidencia de que se olvidan: `AGENTS.md` mismo registra dos commits con trabajo ajeno firmado (`ae34e536f7`, y otro el 2026-11-06). La regla existe; su posición no ayuda.

### B. Memoria de cuatro capas, inventariada

```
daily_notes      157 filas
todos            126 filas
learnings        277 filas
inbox              6 filas
contributions     71 filas
```

Las cuatro del curso están representadas: short-term (daily), episodic (contributions/todos), semantic (learnings), procedural (skills). **Falta una quinta que el curso no nombra y nosotros usamos: el HANDOFF**, que es memoria episódica *destinada* — escrita para otro, no para el mismo agente.

### C. ¿El cierre de sesión aprende? — el hueco medido

El curso define learning como *usar lo que pasó antes para hacerlo mejor la próxima*. El cierre guarda y comunica; no siempre aprende.

`scripts/check-session-learning-rate.py --days 20`:

```
día           cierres  learnings  estado
2026-10-25          2          1  ok
2026-10-26          1          0  HUECO
2026-10-27          1         11  ok
...
2026-11-12          1          0  HUECO
TOTAL              17         30

6 día(s) con cierre de sesión y cero learnings.
```

**6 de 17 cierres (35%) no dejaron un solo learning.** En el diagnóstico de tres pasos del curso: no se guardó. No es un problema de búsqueda — es que nadie escribió.

### D. Multi-agente y el costo de atribución

El pipeline A/B/C tiene tres agentes y el curso justifica el tercero (revisión independiente). Pero `AGENTS.md` ya tiene dos reglas sobre el mismo problema:

- "un auto-reporte de subagente no es un hecho: verifico el repo real"
- "El CORE verifica antes de reportar... Un auto-reporte no es prueba"

**Las dos reglas dicen lo mismo.** El curso identifica este costo exacto: *"when the final answer is wrong, it's harder to work out which agent made the mistake"*. Nuestro repo lo resolvió **duplicando la regla en vez de instrumentando el pipeline**. Eso es una señal: si hiciera falta repetirla, la primera no se está aplicando.

### E. ¿Qué skill repite la instrucción clave al final?

De las contramedidas del curso, la más barata es repetir la instrucción crítica al final del prompt. En nuestras skills:

```
verification-gates:  primera regla dura en línea 34/77 (44%), refuerzo final=1
planner-delegation:  primera regla dura en línea 161/198 (81%), refuerzo final=0
session-lifecycle:   refuerzo final=0
```

**`planner-delegation` tiene su primera regla dura al 81%** del documento — el caso de libro. Y ninguna de las dos que no refuerzan lo hace al final.

## Artefacto adoptado

`scripts/check-session-learning-rate.py` — cruza cierres de sesión contra learnings cargados por día. Es el paso 1 del diagnóstico del curso hecho ejecutable: si `HUECO`, no se guardó.

```bash
python3 scripts/check-session-learning-rate.py --days 20
```

No va al pre-commit como bloqueante todavía: un día sin learning puede ser una sesión de 10 minutos. Sirve como lectura para el cierre de sesión y, si el número no baja, para justificar un gate.

## Lo que NO se adoptó

- **Reordenar `AGENTS.md`** para llevar las reglas duras al inicio: el archivo tiene cap de 20.000 caracteres y está en 20.099. Mover secciones lo cambia, no lo mejora. Candidato a ADR, no a patch.
- **Colapsar la regla duplicada de auto-reporte:** correcto, pero es deuda de contenido, no del módulo.
- **Skill nueva:** no. La regla del paso 12 dice que una skill se escribe después de un uso real, y este chequeo todavía no tuvo uno.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
