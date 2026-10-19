# ADR-001: Product Definition Cycle

**Status:** Accepted
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-07-19
**Actualizado:** 2026-10-15
**Origen:** kanam-workflow

## Decision

Gestionar el ciclo de vida de producto mediante **Product Definition Cycle** (`product-definition-cycle`): cuatro etapas encadenadas que convierten una idea en un producto especificado y diseñado, sin escribir código. El CORE orquesta; DEV/OPS/MIND/STUDIO implementan.

## Contexto

El pipeline original (9 pasos, skills `profile-positioning`, `product-orchestrator`, `openspec-creator`, `product-reset`) era **ficción**. Esas skills nunca existieron: fueron documentadas en ADRs tempranos como parte de un diseño que no se construyó. Hoy el flujo real es un ciclo único de definición con artefactos en `.knowledge/` del proyecto y `docs/`.

**Skills reales que ejecutan el ciclo (verificado 2026-10-18):** las skills del ciclo viven en el **workshop del CORE** (`~/.openclaw/agents/main/agent/workshop-skills/`); el CORE las orquesta y delega la implementación a los roles (ADR-083).

| Skill (dónde vive) | Qué hace | Ejecuta |
|-------|----------|---------|
| `product-definition-cycle` (CORE workshop) | Orquesta las 4 etapas: reconocimiento → discovery → specs+knowledge → diseño | CORE |
| `spec-discovery-creation` (CORE workshop) | Genera specs kanam-spec desde una idea (endpoint kanam-spec-nextgen + Ollama) | CORE (delega verificación) |
| `spec-draft-creation` (CORE workshop) | Redacta drafts de specs desde discovery/brief | CORE |
| `spec-validation` (CORE workshop) | Corre el checker de specs (wrapper del validador de `spec-driven-development` de DEV) | CORE lo invoca; el validador vive en DEV |
| `spec-driven-development`, `openspec`, `hermes-*` (DEV) | Implementación según el spec: SDD, ADRs de proyecto, build/test/review (`agents/kanam-dev/skills/`) | DEV |
| `knowledge-management`, `research-brief-protocol` (MIND) | Discovery: prior art, reconocimiento del ecosistema | MIND |

**Lo que NO existe (y no se va a crear):**
- `adr-framework` - skill inexistente; ADRs se escriben manualmente o via `spec-driven-development`
- `profile-positioning` / `product-orchestrator` - nunca existieron; eran parte del pipeline OSS ficticio (ver ADR-005)
- `openspec-creator` / `product-reset` - nunca existieron

## Consecuencias

1. **Una sola skill para el ciclo completo** - `product-definition-cycle` ejecuta las 4 etapas en una tarea larga; no son 4 trabajos separados
2. **Decisiones de negocio ANTES de especificar** - Una spec sobre alcance supuesto se reescribe entera; cada etapa bloquea en decisiones del owner, no en info técnica
3. **Una sola verdad** - Si el diseño cambia una decisión del discovery, se reconcilia el artefacto anterior en el mismo movimiento
4. **Artefactos en el proyecto, no en el workspace** - `.knowledge/`, `docs/adr/` viven en `projects/<slug>/` (ADR-098); el workspace solo nombra el proyecto en `MEMORY.md`/`CHANGELOG.md`

## Ciclo Actual (4 etapas)

```bash
# Disparador típico:
"pasemos por la etapa de descubrimiento para luego escribir sus specs y definir su knowledge"

# Entregables por etapa:
1. .knowledge/DISCOVERY.md      # Problema, usuarios, capacidades [core]/[apoyo]/[a decidir], riesgos, prior art
2. .knowledge/BRIEF.md          # Contrato de pantalla: qué, por qué, stack, estado
3. .knowledge/STATUS.md         # Estado por etapa + decisiones (D1, D2...) con verificación
4. .knowledge/specs/SPEC-NNN-*.md  # Una spec por capacidad core (kanam-spec: Acceptance Criteria, Edge Cases, Verification Plan)
5. .knowledge/KNOWLEDGE.md      # Negocio, dominio, decisiones cerradas, qué se reutiliza, riesgos, preguntas abiertas
6. docs/architecture.md         # Decisiones CON alternativa descartada, invariantes + test que falla al violarlos, contratos
7. docs/CONTEXT.md              # Glosario autoritativo: un término por concepto, sinónimos rechazados
8. docs/data-model.md           # Esquema como contrato, excepciones declaradas (qué tablas no llevan company_id y por qué)
9. docs/adr/ADR-NNNN-*.md       # Una decisión durable por ADR + índice
```

## Gates de Validación (reales, medibles)

| Etapa | Gate | Verificación |
|-------|------|--------------|
| Reconocimiento | Prior art citado | `grep -ril "<dominio>" memory/ docs/ projects/` + evidencia por capacidad |
| Discovery | Decisiones cerradas | Tabla D1..Dn sin abiertas; asumidas marcadas como asumidas; `ask_user` en tandas de ≤3 |
| Specs | Contrato kanam-spec | Cada spec tiene `## 5. Acceptance Criteria`, `## 6. Edge Cases`, `## 7. Verification Plan` (verificar con `grep -c '^## 5\.'`) |
| Diseño | Trazabilidad completa | Tabla `Spec -> capacidad -> contrato -> invariantes` en `architecture.md`; `grep` por IDs de spec y capacidades devuelve referencias; cero decisiones abiertas para quien construya |

## Reglas de Decisión (del ciclo)

- **Decisión de negocio abierta bloquea la spec**, no la etapa siguiente
- **`ask_user` = máx 3 preguntas por llamada**; opciones en `options`, recomendada primero
- **Diseño ≠ descripción del stack** - Cada decisión con alternativa descartada + motivo; "es más simple" sin tradeoffs no es motivo
- **Precedente propio no es motivo** - El stack se justifica por lo que hace hoy (USER.md)
- **Diseño contradice a discovery → discovery se corrige** - Mantener versión vieja deja dos verdades
- **ADRs del proyecto van al repo del proyecto** (`docs/adr/`) - No al workspace (ADR-067); proyecto sin repo = artefactos solo en disco
- **Invariante sin test = intención** - Escribir regla y test juntos
- **Vocabulario en glosario del proyecto** (`CONTEXT.md`), no en prosa de cada doc
- **Ciclo termina en diseño, no en código** - Cierre dice "listo para construir"
- **Cada etapa cierra con verificación reproducida** (comando + salida), no resumen

## Referencias

- [ADR-002](./ADR-002-openspec-primary-doc-format.md): kanam-spec como formato primario de specs
- [ADR-003](./ADR-003-product-reset-triggers.md): Triggers de fase + grow/pivot = decisión manual del owner (re-definición via nueva corrida del ciclo)
- [ADR-083](./ADR-083-frontera-de-roles-core-no-escribe-codigo.md): CORE orquesta, no implementa
- [ADR-098](./ADR-098-proyectos-vuelven-al-workspace-cwd.md): Proyectos en `<workspace>/projects/<slug>/`

---

*Reescrito 2026-10-15: elimina skills ficticias (`adr-framework`, `profile-positioning`, `product-orchestrator`, `openspec-creator`, `product-reset`); refleja el ciclo real. Corregido 2026-10-18 (review K3): mapea las skills al sistema multiagente real (dónde viven, quién ejecuta) - las skills del ciclo viven en el workshop del CORE.*