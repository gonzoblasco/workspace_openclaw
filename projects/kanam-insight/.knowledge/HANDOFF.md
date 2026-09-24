# HANDOFF: kanam-insight

## Session Context
- **Date:** 2026-09-24
- **Project:** kanam-insight
- **Fase:** 0.1.0 - Pattern Radar + Debt Detector operativos

## Estado actual

Apuesta 1 de `docs/APUESTAS.md` arrancada y con la capacidad completa funcionando. Stack reusado de `langchain-starter` (ADR-063).

| Pieza | Archivo | Verificación |
|---|---|---|
| Scanner de `.knowledge/` | `scripts/scan.py` | 122 archivos, 24 proyectos, 768.465 chars |
| Indexador | `scripts/index.py` | 1243 chunks en la colección `insight_knowledge` |
| Pattern Radar | `scripts/radar.py` | Cruzó 8 proyectos; 5 patrones; 2 verificados a mano |
| Debt Detector | `scripts/debt.py` | 26 proyectos analizados; reporte en `docs/insights/` |

## Decisiones registradas

- **ADR-063:** Python sobre LangChain, no TypeScript con Bun. El spec original (2026-08-30) quedó anterior a la construcción de `langchain-starter` (2026-09-22). Se reusa la capacidad en lugar de reconstruirla en otro lenguaje.
- **Colección propia** (`insight_knowledge`), separada de `starter_knowledge`: mezclar corpus degrada el retrieval, y separar por colección es el mismo mecanismo que después sirve para multi-tenant.
- **Chunking por unidad semántica** (ADR-062): secciones de markdown con el título al frente, no ventana ciega de caracteres.
- **Alcance:** solo `.knowledge/` de proyectos. `docs/` y `memory/` quedan afuera (los dailies son ruido para el retrieval; las entrevistas no aportan al cruce).

## Hallazgo que vale registrar

El radar destapó un patrón real que cruza proyectos: `kanam-fixer` y `kanam-story` coinciden, por vías distintas, en que **los tests verdes no alcanzan para validar el anuncio de un lector de pantalla**. Ese cruce no estaba escrito en ningún lado; emerge de leer los dos proyectos juntos. Es exactamente la señal que justifica el proyecto.

El Debt Detector destapó otro: el ADR de Lucide fue **renumerado de 030 a 037** (commit `1769ecc1`) y dos docs de `soporteml-v4` siguen apuntando al número viejo. Deuda invisible a la lectura manual.

## Trabajo de precisión del detector (vale para el próximo)

La primera corrida del Debt Detector reportó 27 hallazgos de severidad alta. Al verificar cada uno contra los archivos reales aparecieron **tres clases de falso positivo**:

1. Docs base en la raíz del proyecto contados como ausentes (existen, pero fuera de `.knowledge/`).
2. Refs con glob (`scripts/*.py`) tratadas como paths concretos.
3. Refs de proyectos sin repo clonado tratadas como rotas (pueden vivir en GitHub).

**Regla que quedó:** sin el repo del proyecto clonado no se puede afirmar que un doc falte. Solo la renumeración de ADR es señal inequívocamente nuestra, porque ese cambio ocurrió en el workspace. Un detector sin verificación propia produce deuda de credibilidad.

## Próximo paso

1. **Tests** de los caminos críticos (scanner, chunking, retrieval, detector).
2. **Handoff Synthesizer** (estructural: estado real vs ROADMAP).
3. **README + repo en GitHub**: ✅ HECHO el 2026-09-24 - https://github.com/gonzoblasco/kanam-insight (PRIVADO). El repo ya existia desde el 2026-08-30 pero **vacio**; ahora tiene el codigo. El workspace git sigue trackeando `projects/*/.knowledge/` (regla del triple git: el repo del proyecto excluye esa carpeta).

## Open Questions

- ¿El Debt Detector necesita el LLM, o alcanza con análisis estructural puro? El hallazgo del ADR-062 sugiere que la comparación de fechas y estados no requiere semántica.
- El `venv` del starter se reusa; conviene un `requirements.txt` propio antes de que el acoplamiento moleste.

## Lección de método

Un spec que declara un stack "confirmado" puede estar vencido si se escribió antes de construir la alternativa. Se detectó al revisar, no al ejecutar. **Los specs con fecha vencen; se revisan al arrancar.**

---

*Generado por session-lifecycle workflow*
