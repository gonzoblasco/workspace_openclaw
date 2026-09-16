# ADR-048: UI choice for kanam-lab

## Status
Accepted

## Context
kanam-lab is a playground for experimenting with AI model battles, RAG, STT, etc. It currently uses Gradio with several tabs. A discussion considered migrating to a React UI for a product‑like experience.

## Decision
Keep Gradio as the UI framework for kanam-lab for now. The backend is already decoupled, making future migration to React straightforward if a product need arises. Gradio provides rapid iteration speed, matches the current experimental nature, and avoids unnecessary development overhead.

## Consequences
- No immediate work required to rewrite the UI.
- Future migration path remains open; the backend can be reused by a React front end.
- Documentation will note this decision and the open possibility to migrate later.
- Any new UI features will continue to be built using Gradio components.
