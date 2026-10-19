# ADR-003: Product Definition Cycle - Stage Advancement Triggers

**Status:** Accepted  
**Deciders:** Gonzo / Kanam  
**Fecha:** 2026-07-19  
**Actualizado:** 2026-10-15  
**Origen:** kanam-workflow / product-definition-cycle

## Decision

Definir triggers y criterios explícitos, medibles, para avanzar entre las **4 etapas del ciclo de definición** (reconocimiento → discovery → specs+knowledge → diseño), evitando avances prematuros o estancamiento. El ciclo termina en "listo para construir"; no incluye crecimiento post-launch.

## Contexto

La experiencia con `kanam-onwheels`, `soporteml`, `kanam-spec` muestra que:
- Sin criterios claros, el discovery se extiende indefinidamente "buscando más info"
- Las specs se escriben sobre decisiones no cerradas → reescritura completa
- El diseño contradice al discovery → dos verdades coexisten
- El handoff al equipo de build pierde contexto porque no hubo cierre formal

La ambigüedad sobre cuándo avanzar etapa lleva a:
- Trabajo de reconocimiento sin prior art citado
- Decisiones de negocio asumidas, no documentadas
- Specs sin Acceptance Criteria / Verification Plan
- Diseño sin trazabilidad a specs ni invariantes testables

## Etapas y Triggers (Ciclo de Definición)

| Etapa | Triggers de entrada | Criterios de salida (Gate) | Artefactos obligatorios |
|-------|---------------------|----------------------------|--------------------------|
| **1. Reconocimiento** | Idea / brief inicial | Prior art citado por capacidad; riesgos mapeados; capacidades [core]/[apoyo]/[a decidir] | `.knowledge/DISCOVERY.md` |
| **2. Discovery** | Reconocimiento gate passed | Decisiones D1..Dn cerradas (sin abiertas); asumidas marcadas; `ask_user` ≤3 por tanda | `.knowledge/BRIEF.md`, `.knowledge/STATUS.md` |
| **3. Specs + Knowledge** | Discovery gate passed | Cada capacidad core tiene spec kanam-spec completa (7 secciones); `openspec validate` pasa; KNOWLEDGE.md cierra decisiones de dominio | `.knowledge/specs/SPEC-*.md`, `.knowledge/KNOWLEDGE.md` |
| **4. Diseño** | Specs gate passed | Arquitectura con alternativa descartada + invariante + test; CONTEXT.md glosario único; data-model con excepciones declaradas; ADRs del proyecto creados; trazabilidad Spec→capacidad→contrato→invariante | rutas relativas al proyecto: `<proyecto>/docs/architecture.md`, `<proyecto>/docs/CONTEXT.md`, `<proyecto>/docs/data-model.md`, `<proyecto>/docs/adr/` |

## Gates de Validación (Obligatorios, Reproducibles)

```bash
# 1. Reconocimiento → Discovery
grep -c "Prior art:" .knowledge/DISCOVERY.md        # ≥ 1 por capacidad [core]
grep -c "\[core\]" .knowledge/DISCOVERY.md          # ≥ 1

# 2. Discovery → Specs
grep -c "^### D[0-9]" .knowledge/STATUS.md          # = número de decisiones cerradas
grep "abierta" .knowledge/STATUS.md                 # 0 resultados (o marcadas "asumida")

# 3. Specs → Diseño
openspec validate .knowledge/specs/                 # 0 errores
grep -c "^## 5\." .knowledge/specs/*.md             # = número de specs (Acceptance Criteria)
grep -c "^## 7\." .knowledge/specs/*.md             # = número de specs (Verification Plan)

# 4. Diseño → Listo para construir
grep -c "Alternativa descartada" docs/architecture.md   # ruta relativa al proyecto  # ≥ 1 por decisión arquitectura
grep -c "Invariante:" docs/architecture.md                  # ≥ 1 (ruta relativa al proyecto)
grep -c "Test que falla:" docs/architecture.md               # = número de invariantes (ruta relativa al proyecto)
grep -c "^\|" docs/CONTEXT.md                                 # ≥ 5 términos (ruta relativa al proyecto)                          # ≥ 5 términos (glosario)
grep -c "Excepción:" docs/data-model.md                      # 0 o declaradas (ruta relativa al proyecto)                # 0 o declaradas explícitamente
```

## Anti-Patterns a Evitar

| Anti-pattern | Señal | Corrección |
|--------------|-------|------------|
| **Discovery sin cierre** | "Seguimos investigando" > 3 días | Forzar `ask_user` en tandas de ≤3; decisiones asumidas = documentadas como asumidas |
| **Specs sobre decisiones abiertas** | Spec escrita, STATUS.md tiene decisiones abiertas | Bloquear specs hasta Discovery gate; spec sobre decisión abierta se reescribe entera |
| **Diseño sin invariantes testables** | "Es más simple así" sin tradeoff | Cada decisión arquitectura = alternativa descartada + invariante + test que falla al violarlo |
| **Trazabilidad rota** | Spec ID no aparece en architecture.md | Verificar `grep SPEC-NNN docs/architecture.md` (ruta relativa al proyecto) antes de cerrar diseño |
| **Dos verdades** | Diseño contradice discovery; discovery no se corrige | Reconciliar en el mismo movimiento: diseño cambia → discovery se corrige |

## Grow / Pivot (Post-Definición)

El ciclo de definición **termina en "diseño → listo para construir"**. Lo que pase después (launch, métricas, grow, pivot) es decisión de **product management manual (Gonzo)**, no del ciclo automatizado.

| Qué | Cómo se decide hoy |
|-----|---------------------|
| **Continuar escalando** | Gonzo ve retention, revenue, feedback → decide invertir en features |
| **Pivot suave** | Gonzo identifica señal de mercado → corre de nuevo `product-definition-cycle` sobre el proyecto existente: re-usa el DISCOVERY.md vigente como base, actualiza BRIEF.md + decisiones, y re-escribe las specs afectadas |
| **Hard pivot** | Gonzo decide reset total → nuevo proyecto, nueva spec desde cero |

## Cómo se ejecuta un pivot (sin flags ficticios)

La skill no tiene flags ni modos automáticos: el pivot es una **nueva corrida del ciclo, orquestada por el CORE**, con una instrucción explícita de Gonzo:

1. **Reconocimiento:** se re-usa (el prior art ya está citado en DISCOVERY.md).
2. **Discovery:** el CORE actualiza `BRIEF.md` + `STATUS.md` con las nuevas decisiones D1..Dn (pidiendo las decisiones de negocio que falten, tandas de ≤3).
3. **Specs:** las specs afectadas se re-escriben; `openspec validate` pasa en 0 errores.
4. **Diseño:** se actualizan `architecture.md`, `CONTEXT.md`, `data-model.md` y los ADRs del proyecto.

Lo que NO hay: modos (`--mode PIVOT`), thresholds ni orquestación automática de crecimiento.

## Lo que NO hay (y no se va a hacer)

- ❌ Skill `product-orchestrator` evaluando métricas automáticamente
- ❌ Thresholds hardcodeados (retention > 70% = green) - cada producto es distinto
- ❌ Pipeline de crecimiento automatizado (Foundation → Sostenibilidad)
- ❌ `kanam-pipeline --flag PIVOT_HARD` - eso era ficción

## Referencias

- [ADR-001](./ADR-001-product-pipeline-integration.md): Ciclo de definición (4 etapas), reglas de decisión
- [ADR-002](./ADR-002-openspec-primary-doc-format.md): Formato kanam-spec (7 secciones), validación
- `product-definition-cycle` skill (workshop del CORE): ejecución del ciclo; el pivot es una nueva corrida orquestada, no un flag
- `spec-validation` skill (workshop del CORE): wrapper del validador de `spec-driven-development` (DEV), apuntando a `.knowledge/specs/`

---

*Reescrito 2026-10-15: elimina 5 fases de crecimiento ficticias; refleja 4 etapas reales del product-definition-cycle con gates medibles. Fusiona contenido del anterior ADR de estrategia de crecimiento (eliminado): grow/pivot = decisión manual del owner. Corregido 2026-10-18 (review K3): elimina la ficción `--mode PIVOT` (la skill no tiene flags); el pivot es una nueva corrida del ciclo orquestada por el CORE.*