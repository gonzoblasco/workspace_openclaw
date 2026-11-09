# Veredicto SHARP: kanam-dev inventario de skills

Artefacto auditado: agents/kanam-dev/inventory.tsv + agents/kanam-dev/keep-merge-deprecate.md
Artefacto: kanam-dev-inventario-skills
Fecha: 2026-11-07

## Resumen
Se reviso el inventario de 44 skills y el plan keep/merge/deprecate del DEV+AUDITOR.
La evidencia de disco confirma el inventario (44 filas de datos mas header: agents/kanam-dev/inventory.tsv:1)
y 7 skills sin `name` en frontmatter (agents/kanam-dev/keep-merge-deprecate.md:9).
Tambien se confirmaron 4 pares candidatos a merge y 0 deprecated (agents/kanam-dev/keep-merge-deprecate.md:5, agents/kanam-dev/keep-merge-deprecate.md:6).
La evidencia-hunter no reconocio las afirmaciones numericas como tests/tokens y devolvio `bloqueado` en 5/5 (ver /tmp/evidence.json).
Se detectaron inconsistencias de conteo y claims no verificables en disco.

## Puntuacion por eje
- S (Sharpness) = 3 - inventario y plan son claros, pero la razon de cada fila es identica ("frontmatter gaps, see audit") y hay conteos cruzados inconsistentes.
- H (Horizon) = 3 - propone merges y guardrail, pero mantiene los 44 skills y no ejecuta consolidacion ni priorizacion.
- A (Asymmetry) = 3 - el inventario aporta valor para consolidar, aunque el costo de mantener 44 skills sigue alto.
- R (Resistance) = 2 - los conteos difieren entre archivos y el metadata count es inexacto en disco (1 skill sin metadata real vs 37 afirmados, y 37 skills con frontmatter completo).
- P (Parsimony) = 4 - formato TSV y markdown corto, sin dependencias nuevas.

Total = 15/25 -> VETO

## Evidencia
Comandos y citas:
- wc -l agents/kanam-dev/inventory.tsv -> 45 (header + 44 datos)
- awk state counts -> 44 keep, 0 deprecated
- frontmatter sin name -> 7 skills (api-integration-test, chaos-engineering, code-metrics, compatibility-testing, dependency-advisor, performance-benchmark, threat-modeling)
- metadata key missing in disco -> 1 skill (threat-modeling) (agents/kanam-dev/skills/threat-modeling/*)
- frontmatter completo (name+desc real+metadata) -> 37 skills
- evidence-hunter /tmp/evidence.json -> 5/5 bloqueado (sin detector para afirmaciones numericas)

Citas:
- agents/kanam-dev/inventory.tsv:1
- agents/kanam-dev/keep-merge-deprecate.md:4
- agents/kanam-dev/keep-merge-deprecate.md:5
- agents/kanam-dev/keep-merge-deprecate.md:6
- agents/kanam-dev/keep-merge-deprecate.md:9
- agents/kanam-dev/keep-merge-deprecate.md:10
- agents/kanam-dev/keep-merge-deprecate.md:14
- agents/kanam-dev/ROADMAP.md:18
- agents/kanam-dev/ROADMAP.md:104

## VOTO / Fricciones obligatorias
Veredicto: VETO (15/25)

1. R - conteo de metadata inexacto. Causa: keep-merge-deprecate.md:10 dice "metadata missing: 37 skills" pero en disco solo 1 skill no tiene la key metadata y 37 tienen frontmatter completo. Ajuste: corregir el conteo y distinguir "gap total" de "metadata key faltante".
2. S - claim "30 con metadata anadida" no aparece en el entregable ni en disco. Ajuste: eliminar o sustentar con una tabla de alcance por skill.
3. R - "37 skills listos en <30 ediciones" no coincide con las 7 skills que realmente tienen title/description placeholder. Ajuste: ajustar guardrail a las 7 ediciones minimas observadas.
4. H - los 4 pares candidatos no tienen criterio de canonicidad ni plan de migracion. Ajuste: agregar para cada par un skill canonico, pasos de merge y verificacion de refs.
5. S - ROADMAP.md cita 43 skills documentadas (ROADMAP.md:18) y 44 (ROADMAP.md:104). Ajuste: unificar el conteo o fechar el cambio.

## Accion del autor
Corregir contadores, agregar tabla de gaps por skill y definir canonicidad para los pares merge antes de re-someter.

Rutas:
- agents/kanam-dev/inventory.tsv
- agents/kanam-dev/keep-merge-deprecate.md
- /tmp/evidence.json
- agents/kanam-critic/docs/reviews/2026-11-07-kanam-dev-inventario-skills.md