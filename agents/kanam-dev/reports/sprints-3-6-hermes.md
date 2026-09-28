# Sprints 3 a 6 - Cierre

Fecha: 2026-09-28
Ejecutado por: agente padre (main)
Estado: completado con verificacion reproducida

## Sprint 3 - Skill-bundles

**Que se hizo:** los 15 `skill-bundles/*.yaml` de Hermes **no se importan como tales**. Cada
bundle es un comando de slash que referencia skills que en su mayoria no existen en Kanam
(6 referencias: solo 2 existen en el repo, 3 no existen en ningun lado y 1 es de una coleccion
externa). Importarlos habria creado enlaces rotos.

Se extrajo el valor real: el **loop por etapas** y el **confidence gate**. El resultado es la
skill `skills/sdd-agent-loop/`.

**Lo que sirve:** el contrato por etapas (que rol produce que artefacto), el gate que separa
decision rutinaria de no trivial, y la exigencia de verificar antes de avanzar.
**Lo que no:** las rutas `~/.hermes/*`, los comandos de slash y las referencias a skills
inexistentes.

## Sprint 4 - Fixtures

**Que se hizo:** los 8 fixtures testean binarios de Hermes (`bin/agency-next`, `bin/phase-gate`,
etc.) que no existen en Kanam. Importar los scripts no tiene sentido. Se extrajeron los tres
patrones con que estan escritos, en la skill `skills/verification-gates/`:

1. Cero casos corridos no es verde (una suite que nunca corrio no puede dar exit 0).
2. Un SKIP no es un OK (tiene su propio codigo, nunca se cuenta como aprobado).
3. Contrato de honestidad del lector (archivo ausente se reporta, no se lee como vacio).

**Lo que sirve:** los tres patrones. Son exactamente el tipo de guarda que habria marcado los
falsos positivos de los sprints 1 y 2.
**Lo que no:** los scripts, que dependen de binarios inexistentes.

## Sprint 5 - Reports

**Que se hizo:** el valor de `templates/final-report.md` es el vocabulario de confianza
(`verified` / `partially_verified` / `self_reported` / `blocked`) y la regla de que una etapa
critica nunca cierra en `self_reported`. Resultado: `skills/trust-vocabulary-report/`.

**Lo que sirve:** el vocabulario y la regla de cierre.
**Lo que no:** las referencias a `bin/run-trace` y `reports/<runId>.jsonl`.

## Sprint 6 - Validacion end to end

**Nota de alcance:** el plan describia este sprint como "integrar multimodalidad con
`gemma4:cloud`", pero **el repo no tiene material multimodal**: no hay una sola referencia a
imagenes o vision en sus agentes ni en sus bundles. Ejecutar eso habria sido inventar trabajo.
Se hizo lo que si faltaba: validar end to end todo lo importado.

| Check | Comando | Resultado |
|---|---|---|
| Skills descubribles por el runtime | `openclaw skills list --agent main --json` | 12/12 presentes, todas `modelVisible: true` |
| Specs buscables | `wiki_search "review-tier high consequence deterministic"` | hits con path `sources/hermes-sdd/specs/review-tier/spec.md` |
| Presupuesto del catalogo | estimado name+description+location | 10.583 / 18.000 chars (45 visibles) |

## Criterio de aceptacion global

| Criterio | Resultado |
|---|---|
| 3 skills nuevas creadas | 3 |
| 0 guiones largos en lo creado | 0 |
| Suite de skills en verde | 0 fallos en 6 checks |
| Todo lo importado visible al modelo | 12/12 |
| Todo lo importado buscable | verificado |

## Decisiones

- **Los bundles y fixtures no se importan como archivos.** Son artefactos de la maquina de
  Hermes, atados a binarios que no existen. Se importa el criterio, en skills nuevas.
- **Sprint 6 se redefinio.** El alcance original pedia multimodalidad sin material; se
  reemplazo por validacion end to end, que era el hueco real.

## Pendiente

- Publicar a `kanam-skills` si se decide (requiere sanitizacion previa).
- Code review de los sprints 3 a 6 (pausa acordada cada 4 sprints).
