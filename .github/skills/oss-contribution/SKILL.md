---
name: "oss-contribution"
metadata:
  category: "Contribution"
  tags:
    - open-source
    - contribucion
    - pr
description: "Workflow de OSS Contribution: contribución estratégica a repos externos. Reemplaza oss-contribute, sdd-brownfield."
user-invocable: false
---

# Workflow: OSS Contribution

## Skills que reemplaza
- `oss-contribute`
- `sdd-brownfield`

## Propósito
Contribución estratégica a repositorios externos con Spec-Driven Development.

## Cuándo usarlo
- Contribuir con un fix o feature a un repo open source externo
- Hacer triaje de issues en repos objetivo para encontrar oportunidades
- Dar seguimiento batch a PRs abiertos en repos externos
- Preparar una contribución estratégica con Spec-Driven Development

## Fases
1. **Pipeline** — selección de repos objetivo, tier ranking
2. **Triaje** — buscar issues sin PRs competidores, evaluar impacto
3. **Análisis** — entender el bug/feature, root cause analysis. Usar el análisis del reporter de issues. Complex issue ≠ complex fix. Revisar si el reporter ya identificó la causa raíz
4. **Implementación** — fork, branch, fix, tests, OpenSpec as-built/delta
5. **PR** — commit firmado SSH, descripción clara y humana (no generada). En repos Tier 0 (shadcn/ui, TanStack, Vercel): evitar trazas de automatización en commits y descripciones. Descripción humana, no generada
6. **Post-PR Watch** — monitorear el PR por 10 min: detectar comentarios de bots, cambios solicitados, merges. Usar `scripts/pr-watch.sh`
7. **Community** — comentar en issues relacionados, cross-referencing. Hacerlo después del PR, no antes, para evitar ruido si el PR no prospera
8. **Batch** — status check de PRs abiertos (🟢⚠️🔴). Se ejecuta automáticamente al cerrar sesión vía `session-lifecycle`
9. **Registry** — al abrir o trackear un PR (propio o de terceros), registrar la cadena completa en CONTRIBUTING.md:
   - Issue → PR de tercero (autor, estado) → Nuestro aporte (link al comment) → Nuestro PR (link, estado) → Contexto (cómo llegamos acá)
   - No registrar solo el PR final. La narrativa completa es lo que permite retomar sin perder contexto
   - Si el PR es de un tercero y solo comentamos, igual se registra — el comment es un activo

## Reglas de búsqueda de PRs

- Cuando Gonzo pide ver un PR por número + repo, buscar directamente en ese repo con `gh pr view <n> --repo <org/repo>`
- **No filtrar por autor propio** a menos que Gonzo especifique "mis PRs" o "PRs míos"
- Si el PR no se encuentra, verificar que el repo esté bien escrito (org/repo-name completo)

## Reglas de interacción en PRs/Issues de terceros

### Bots vs Humanos

- **Identificar al interlocutor:** antes de responder en un hilo, verificar si el autor del comment es un bot (github-actions, netlify, codecov, dependabot, etc.) o una persona.
- **A bots no se les responde como si fuesen personas.** No saludar por nombre, no hacer conversación social, no agradecer. Si hay que responderle a un bot (ej: un check automatizado que pide algo), ser directo y dejar claro que se está respondiendo al sistema, no a una persona. Ej: "Esto es para el bot — si algún humano necesita más contexto, avise".
- **A humanos se les habla como humanos.** Natural, sin vueltas, sin estructura de documento técnico.
- **No meterse en hilos cerrados/muertos.** Si un PR está closed y no hay una pregunta directa hacia Gonzo, no comentar. El silencio no es una invitación.
- **Menciones como referencia técnica ≠ llamado a la acción.** Si alguien menciona a Gonzo como referencia de un bug (ej: "como @gonzoblasco observó"), no requiere respuesta a menos que haya una pregunta explícita.
- **PRs cerrados por detección de automatización:** evaluar caso por caso. Por defecto no intervenir — el maintainer ya tomó una decisión y el autor del PR ya habló. Pero si hay una razón para mostrar empatía (ej: Gonzo pasó por lo mismo), se puede comentar con cuidado, sabiendo que el maintainer lo va a leer. No hacerlo sin consultar a Gonzo primero.

## Mirror de skills

- **Todos los cambios a skills en `/workspace/skills/` deben reflejarse en `/workspace/.github/skills/`** (el mirror público). Si se modifica un SKILL.md del workspace, copiar el cambio al mirror correspondiente.
- Esto aplica a cualquier skill que tenga mirror en `.github/skills/`. Verificar antes de dar por terminada la tarea.

## Outputs
- PRs a repos externos
- OpenSpec specs as-built o delta
- Reporte de estado de PRs abiertos

## Helper Scripts

Scripts en `skills/oss-contribution/scripts/`:

| Script | Uso |
|---|---|
| `pr-status-check.sh` | Muestra estado de PRs abiertos en un repo (checks, reviews, mergeable). Usar en Fase 6 (Post-PR Watch). |
| `pr-watch.sh` | Monitorea PRs abiertos por 10 minutos detectando comentarios de bots, cambios solicitados y merges. Usar en Fase 6. |
| `triage-issues.sh --repo org/repo` | Triaje de issues abiertos para encontrar oportunidades sin competencia. Usar en Fase 2 (Triaje). |
| `setup-fork.sh --repo org/repo` | Prepara un fork local listo para contribuir. Usar en Fase 4 (Implementación). |

Tambien ver [pr-batch-check.sh](../github/scripts/pr-batch-check.sh) para listar PRs propios en multiples repos.

## Related Skills

- [Review & Quality](../review-quality): Para revisar PRs antes de enviar
- [Technical Documentation](../tech-docs): Para documentar contribuciones
