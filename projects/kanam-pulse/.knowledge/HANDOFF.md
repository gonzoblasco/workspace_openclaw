# HANDOFF - kanam-pulse

## Session Context
- **Date:** 2026-08-29 23:27
- **Project:** kanam-pulse
- **Repo:** https://github.com/gonzoblasco/kanam-pulse (PUBLIC, MIT)
- **Workspace:** double-git (`.knowledge/` tracked as workspace blob, not in project repo)

## Summary (Sesion 1 del proyecto - 29/08 22:46-23:27)

M0 completo. Nace de la inversa del camino Breacorp: refactor web monolito -> CLI propio (`system-health-check`) -> vuelta a la web sobre el motor del CLI.

- Nombre decidido: **Kanam Pulse** ("Pulse" evoca salud/monitoreo, "Boost" suena a optimizador 2000s; elegi yo, aprobo Gonzo).
- Repo publico creado y confirmado: `gh repo edit` -> PUBLIC.
- Contenido publicado (`0f2b4b8`): README honesto (pre-alpha, roadmap M0-M5, creditos a Breacorp), LICENSE MIT, `docs/SPEC-v1.md` (arquitectura packages/core+server+web, consent-driven fixes, a11y AA como principio, open questions).
- BRIEF.md + STATUS.md de `.knowledge/` con contenido real.
- Fix estructural de paso: `scripts/init-project.sh` generaba un `.gitignore` que listaba `.knowledge/` - como git parsea los `.gitignore` anidados y el mas profundo gana, el workspace no podia trackear el `.knowledge` como blob (inexpugnable para `git add`, silencioso). Ahora el `.gitignore` del proyecto NO lista `.knowledge/` y la exclusion va en `.git/info/exclude` local (invisible al workspace). Registrado en CHANGELOG.md.

## Files Changed
- `projects/kanam-pulse/**` (repo propio: README, LICENSE, docs/SPEC-v1.md, .gitignore)
- `.knowledge/`: BRIEF.md, STATUS.md, HANDOFF.md
- `scripts/init-project.sh` (fix doble git), `CHANGELOG.md`, `projects/PROYECTOS.md`

## How to Verify
- `gh repo view gonzoblasco/kanam-pulse` -> PUBLIC
- `ls projects/kanam-pulse/` -> .gitignore LICENSE README.md docs (.knowledge/ presente)
- `bash -n scripts/init-project.sh` -> ok
- Workspace check-ignore: `git check-ignore -v projects/kanam-pulse/.knowledge/BRIEF.md` -> lin 66 negacion (NO ignorado)

## Known Issues / Risks
- **El codigo del motor CLI no esta en esta maquina** (`projects/system-health-check/` solo tiene `.knowledge/`; el CLI se hizo en la MacBook Air y no tiene repo GitHub). M1 requiere traer el codigo: pushear desde la MBA o copiar. Todo creado (#get done en DB).
- Ci/CD, hooks y lint todavia no existen en el repo (vienen con M1).
- Spec tiene 3 open questions marcadas (Linux depth, charts lib, i18n) - decidir en M1.

## Next Steps
1. Traer codigo de `system-health-check` desde la MacBook Air (sin repo, requiere push desde ahi o copia).
2. M1: extraer engine a `packages/core` (TS), 46 tests heredados en verde en este repo.
3. M1: server local (Fastify, bind 127.0.0.1) + dashboard read-only (checks + metricas en vivo).
4. Despues: M2 fixes con consentimiento -> M3 resumen IA con Ollama -> M4 a11y pass + CI -> M5 release + annuncio.