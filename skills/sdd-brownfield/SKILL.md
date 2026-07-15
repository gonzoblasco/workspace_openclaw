---
name: "sdd-brownfield"
description: "\"Apply Spec-Driven Development to existing projects with remote backends — write as-built specs, delta specs, and manage changes with OpenSpec.\""
---

# SDD Brownfield

Use when applying Spec-Driven Development to an existing project, especially one with a remote backend (Lovable Cloud, Supabase Cloud, etc.) where you can't run locally or access secrets.

## When to trigger

- "Vamos a poner OpenSpec en este proyecto"
- "Necesito specs del estado actual"
- "Quiero trabajar en un proyecto sin acceso al backend"
- "Escribí specs as-built"
- "Creá un delta spec para esta feature"

## Prerequisites

- OpenSpec installed (`npx @fission-ai/openspec`)
- Read access to the project's source code (even if it can't run locally)
- Understanding of the project's architecture (read README, CHANGELOG, types, schemas)

## Phase 1 — Initialize OpenSpec

1. Run `npx @fission-ai/openspec init --tools none --force` in the project root
2. Edit `openspec/config.yaml` with:
   - `schema: spec-driven`
   - `context:` block with tech stack, conventions, language, domain knowledge
   - `rules:` block with per-artifact rules (e.g., "Write in Spanish", "Use WHEN/THEN")
3. Verify structure: `openspec/specs/` and `openspec/changes/` directories created

## Phase 2 — Write as-built specs

For each major capability of the existing system:

1. **Read the code** — components, pages, edge functions, migrations, types
2. **Identify capabilities** — group related functionality into spec names (e.g., `inbox`, `ai-copilot`, `billing-mp`)
3. **Write `openspec/specs/<name>/spec.md`** with:
   - `## Purpose` (required by OpenSpec)
   - `## Requirements` with `### Requirement:` blocks
   - Each requirement MUST contain "SHALL" or "MUST" (not "debe" — OpenSpec rejects it)
   - Each requirement MUST have at least one `#### Scenario:` block
   - Scenarios use `- **WHEN** <condition>` and `- **THEN** <expected outcome>` format
   - `- **AND**` for additional conditions/outcomes
4. **Reference real names** — Edge Functions, tables, RPCs, components, files
5. **Validate:** `npx @fission-ai/openspec validate <spec-name>`
6. **List:** `npx @fission-ai/openspec list --specs` to confirm all specs are recognized

### Tips for as-built specs

- Read the actual code, don't guess from README alone
- Include edge cases you find in the code (error handling, fallbacks, rate limits)
- Note when something is NOT operational (e.g., "secrets not configured, code exists but never ran")
- Group 5-7 requirements per spec — too few means the spec is too narrow, too many means it's too broad

## Phase 3 — Check before writing a delta spec

**Critical:** Before writing a delta spec for a "planned" feature, check if it's already implemented.

1. Search the codebase for the feature (grep for component names, function names, table names)
2. Check the CHANGELOG for entries about the feature
3. Check git log for commits about the feature
4. If already implemented → write it as an as-built spec directly, skip the delta spec
5. If partially implemented → write as-built for what exists, delta spec for what's missing
6. If not implemented → proceed to Phase 4

## Phase 4 — Write a delta spec (change proposal)

For new features or modifications:

1. `npx @fission-ai/openspec new change <change-name>` (kebab-case)
2. Write `proposal.md`:
   - `## Why` — motivation
   - `## What Changes` — specific changes
   - `## Capabilities` — New (`<name>: <desc>`) and Modified (`<existing-name>: <what changes>`)
   - `## Impact` — affected code, APIs, dependencies
3. Write `design.md`:
   - `## Context` — current state
   - `## Goals / Non-Goals` — what's in/out of scope
   - `## Decisions` — key design decisions with rationale
   - `## Risks / Trade-offs`
4. Write delta specs in `specs/<name>/spec.md`:
   - `## ADDED Requirements` for new capabilities
   - `## MODIFIED Requirements` for changed capabilities
   - `## REMOVED Requirements` for removed capabilities
   - Same SHALL/MUST + Scenario format as as-built
   - For MODIFIED: include ALL scenarios from the as-built spec, not just the new ones (OpenSpec validates this on archive)
5. Write `tasks.md` — grouped task list with checkboxes
6. Validate: `npx @fission-ai/openspec validate <change-name>`
7. Check status: `npx @fission-ai/openspec status --change <change-name>` (should show 4/4 artifacts)

## Phase 5 — Implement with branch per feature

1. `git checkout -b feature/<change-name>` from the main branch
2. Implement following the tasks from the delta spec
3. Commit with semantic messages referencing the change name
4. When complete, push branch and open PR: `gh pr create --title "feature: <name>" --body "Implements OpenSpec change: <change-name>"`
5. After review/merge, archive the change

## Phase 6 — Archive the change

When the feature is complete and merged:

1. `npx @fission-ai/openspec archive <change-name> -y`
2. OpenSpec merges the delta into the as-built specs
3. The change moves to `openspec/changes/archive/`
4. Verify: `npx @fission-ai/openspec list --specs` shows updated requirements count
5. Verify: `npx @fission-ai/openspec list` shows no active changes
6. Commit the archive result

## OpenSpec gotchas (learned the hard way)

- "SHALL" or "MUST" required in every requirement — "debe", "should", "will" are rejected
- `## Purpose` section is mandatory, not optional
- Scenarios must use `#### Scenario:` header (4 hashes)
- WHEN/THEN format: `- **WHEN** <condition>` / `- **THEN** <outcome>` / `- **AND** <extra>`
- For MODIFIED requirements, include all existing scenarios + new ones, or archive fails
- `openspec init` only creates `config.yaml` — specs and changes directories are empty
- As-built specs for brownfield are written manually, not generated from changes
- `openspec archive` checks task completion — use `-y` to skip the warning if tasks aren't checked

## Working without backend access

When the project has a remote backend (Lovable Cloud, Supabase Cloud) and can't run locally:

- **Can do:** read code, write specs, write tests, refactor frontend, design migrations, write Edge Functions (for remote deploy)
- **Cannot do:** run locally, access secrets, deploy directly, run migrations
- **Workflow:** code locally → deploy via platform (Lovable, Supabase CLI) → verify remotely
- **Specs as source of truth:** when you can't test locally, specs fill the gap — they describe expected behavior precisely
- **Git as bridge:** commit locally, the platform pulls from the repo

## Remote-backend documentation

When you can't access the backend directly, document it from the code:

1. **Edge Functions:** for each function, document endpoint, input, output, auth model
2. **Database:** use generated types (e.g., `src/integrations/supabase/types.ts`) to map tables and RPCs
3. **Secrets:** list required env vars from the code (grep `Deno.env.get` or `process.env`)
4. **Note what's NOT operational:** if code exists but secrets aren't configured, say so explicitly in the spec
