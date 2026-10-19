# ADR-005: OSS Contributions - Manual, Not Automated Pipeline

**Status:** Accepted
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-07-19
**Actualizado:** 2026-10-15
**Origen:** kanam-workflow

## Decision

Las contribuciones OSS son **actividad manual de Gonzo**, no un pipeline automatizado que alimente a `profile-positioning` (skill inexistente) ni a `product-orchestrator` (skill inexistente). No hay feedback loop automático.

## Contexto

El ADR original describía un pipeline OSS de 6 fases (Scout → Triage → Contribute → Amplify → Relate → Leverage) con integración automática via `kanam-pipeline --on-event PR_SUCCESS` disparando `profile-positioning` y `product-orchestrator`. Nada de eso existe:

- ❌ `vibe-prospecting` skill - no existe en ningún directorio
- ❌ `profile-positioning` skill - archivada/consolidada 2026-07, no existe
- ❌ `product-orchestrator` skill - archivada/consolidada 2026-07, no existe
- ❌ `kanam-pipeline --on-event` - comando ficticio
- ❌ Pipeline OSS de 6 fases automatizado - ficción

## Realidad Actual (2026-10)

| Actividad OSS | Cómo ocurre hoy |
|---------------|------------------|
| **Scout / Triage** | Gonzo busca repos manualmente (topics, good-first-issue, interés personal) |
| **Contribute** | PR manual, review manual, merge manual |
| **Amplify / Relate** | Gonzo comenta, comparte, conversa con maintainers - decisión personal |
| **Leverage** | Gonzo decide si/ cuándo mencionar en perfil, portfolio, conversaciones |

No hay tracking automático de PRs merged → no hay re-evaluación automática de nada.

## Por Qué No Automatizar Esto

1. **Contexto de negocio irreproducible** - Qué repo vale la pena, qué maintainer relacionar, qué narrativa construir: decisiones humanas
2. **Señal ruidosa** - Un PR merged en repo random ≠ señal de mercado para producto de Gonzo
3. **Costo > beneficio** - Mantener un pipeline que scrapea GitHub, parsea PRs, evalúa "fit" y actualiza perfiles: overhead que no paga
4. **Gonzo lo hace manual y bien** - 22+ PRs abiertos históricos demuestran que el proceso manual funciona

## Lo Que SÍ Existe Relacionado

- `spec-discovery-creation` / `spec-draft-creation` - Generan specs desde ideas (pueden venir de insights OSS)
- `product-definition-cycle` - Ciclo de definición que Gonzo dispara manualmente cuando hay señal real
- ADRs del proyecto - Documentan decisiones incluyendo "insight came from OSS contribution to X"

## Referencias

- [ADR-001](./ADR-001-product-pipeline-integration.md): Ciclo de definición (manual trigger)
- [ADR-003](./ADR-003-product-reset-triggers.md): Grow/pivot = decisión manual del owner
- `oss-contribution` skill (STUDIO, `agents/kanam-studio/skills/`): soporte a contribuciones OSS
- `spec-discovery-creation` / `spec-draft-creation` (workshop del CORE) - Generan specs desde ideas (pueden venir de insights OSS)
- `product-definition-cycle`: Gonzo dispara manualmente cuando hay señal real
- ADRs: Documentan decisiones incluyendo insights OSS
- `kanam-workflow` (origen histórico): Pipeline ficticio documentado para aprendizaje

---

*Reescrito 2026-10-15: elimina pipeline OSS automatizado ficticio, skills inexistentes, comandos ficticios; refleja realidad: OSS = actividad manual del owner sin automatización*