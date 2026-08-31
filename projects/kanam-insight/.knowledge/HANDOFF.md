# HANDOFF: kanam-insight

## Estado actual

Spec v1 cerrada. Tres pilares:
- Pattern Radar (cross-project)
- Handoff Synthesizer (project-aware)
- Debt Detector (ADR/code)

## Decisiones de diseño (Sesión 1, 2026-08-30)

- **Fuente ADRs:** escanear ambos paths: `.knowledge/adr/` y `docs/adr/`. Sin unificar.
- **Stack LLM:** Ollama (`glm-5.3-flash:cloud`) vía app local (mismo endpoint que API directa, usa config existente).
- **Salida:** CLI + reports Markdown en `docs/insights/YYYY-MM-DD.md`.
- **Local-first:** índice SQLite-vec local. Sin nube para embeddings.

## Próximo paso

1. `init-project` (repo privado en gh + scaffolding).
2. Spike: scanner de `.knowledge/` + `docs/adr/` (sin LLM todavía).
3. Spike: indexación con SQLite-vec.
4. Primer analizador (Pattern Radar MVP).
