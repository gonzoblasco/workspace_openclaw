# Skill-Router / Capability-Index — Learnings

> Aprendizajes específicos del subsistema. Los dailies del CORE cubren historia. Acá lo que cambia cómo se construye y verifica.

## Trampas detectadas y su fix

- **El router levantaba el 20% del catálogo.** `skill-router.py` hacía `os.listdir(skills/)` hardcodeado; el CLI/runtime expone 171. Fix: `load_skills()` consume `openclaw skills list --agent main --json` con fallback al walk de disco. A partir de ahí, las nuevas skills nacen *visibles*.
- **Planner con cero créditos → plan vacío pero "validado".** El Planner devolvió JSON sin `task`, con roles inventados (`programmer`, `tester`) y path anidado `agents/kanam-planner/agents/...`; el `plan_lint` incluso pasó. Lección: auto-reporte ≠ hecho. Siempre verificar el repo real y correr el lint antes de tratar un plan como valido. Hoy lo hice a mano, es lo esperable cuando no hay créditos.
- **`check-adr-supersede` y `check-pipeline-enforcement` son consistentes internos, no contra la realidad.** ADR-049 decía "Claude Code es motor" y los modelos vigentes son gpt-oss/deepseek/minimax/gemma4. Los gates chocaban entre sí, no con el sistema. Fix: superseder el ADR, no "fix-and-add".
- **Borrar una skill rompe un gate que la cita.** `check-pipeline-enforcement` todavía exigía "la skill de arbitraje nombre A/B/C". Tuve que editarlo para que la fuente de verdad pase a ser `model-router.sh` + managed block. Lección: al eliminar un dueño, actualizar los gates que lo citaban.
- **`git add` con pathspec del archivo ya borrado no stagea la eliminación solo** — hay que usar el path del archivo tracked y re-intentar o `git rm`. Verificado al stagear los skills eliminados.
- **Pre-commit consume carga de créditos por tokens/modash (`ollama`) embedding loops.** 171 embeddings en un hook empeora la UX. Por eso el solapamiento quedó en AVISO y `--staged`.
- **Escritura del archivo se "contamina" si se encadenan comandos tras el heredoc.** Aparecieron líneas `chmod +x` / `py_compile` dentro del script. Verificado: siempre separar heredoc de comandos posteriores.

## Verificación sistemática

- Cada commit real se corrió con pre-commit (no `--no-verify`).
- Gates: `check-refs`, `check-single-source`, `check-pipeline-enforcement`, `check-adr-supersede`, `check-bootstrap-budget` (AGENTS.md cap 19994).
- `py_compile` para cada Python antes de commit.
- Commits atómicos + push solo después de OK.

## Distribución futura de la información

- Este directorio es el "lugar humano". Próxima iteración: tablas en la base.
- Candidate store: la misma `memory.db` del CORE (tablas `skill_router_*`) con un `agent_id` para aislar o, mejor, una DB exclusiva por agente para no contaminar la del CORE. Decisión pendiente — el CORE sugiere empezar por el schema mismo con namespace.

## Próximo movimiento verificado

Ver el paso 5 uno por uno antes de escribir.>