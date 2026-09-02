# Ritz-Carlton One-Pager (keep on screen during the call)

## Story 1 - MP billing audit (SoporteML)
- Multi-tenant CRM for Mercado Libre sellers. Billing "written but never tested".
- Audited 4 Edge Functions against official MP docs.
- Found 4 real bugs: corrupted token, userData undefined (test mode), missing notification_url (webhook never fired), webhook data.id in query param.
- Rule: verify against the real source, never assume written code works.
- Result: all pass deno check + setup guide. Billing that actually works.

## Story 2 - react-spectrum #10517 (Adobe maintainer)
- My PR fixing RAC Checkbox/Radio focus ring. Rob Snow asked for a named prop instead of 4 style props.
- Full rework: hiddenInput="stretch-to-label", 7 files, +81/-209. Tests + real browser tests (Chromium + Firefox).
- Iterating with maintainers is part of the job.
- Closed #10487 as unnecessary after verifying against main (bug already fixed upstream) + offered regression test as separate PR = technical honesty.

## Story 3 - The work system (THE one)
- 9y frontend, now fullstack. AI as infrastructure, not chat.
- A/B pipeline (agent writes, agent reviews, I verify against source), complexity scorer, ADRs for every decision, pre-commit hooks everywhere.
- "The model accelerates; the judgment is mine."
- Merged PRs: MUI, astryx (Facebook), react-spectrum (Adobe). Reviewer TanStack Query. kanam-pulse: 118 tests, gated CI.
- This IS the Principal role: process engineering, not "using AI".

## Answers (keywords)
- AI daily: system behind it (complexity score -> A/B -> verify vs source). Never "AI does the work".
- Architecture decisions: ADR = context, decision, discarded alternatives, why. Documented = not reopened without new evidence.
- Principal expectation: 50/50 hands-on + technical direction (standards, unblocking, decisions others execute).
- Why Ritz-Carlton: the JD asks for what I already do (ADRs, standards, OSS). Fit, not leap.

## Questions for them (pick 2)
1. What do you expect from a Principal in the first 90 days?
2. Biggest project the team has right now?
3. How do you make architecture decisions today?
4. What hurts most in the current stack?

## If asked
- Retest: "preparation matters; classic JS is solid (event loop, promises, algorithms)."
- Salary: no number first. Ask their range. If pushed: $95k-$105k.
- Language: ENGLISH. Always.
