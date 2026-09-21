# HANDOFF - kanam-lab

## Session Context
- **Date:** 2026-09-17 (guardado 2026-09-21)
- **Project:** kanam-lab
- **Branch:** main
- **Sesion:** webchat "pizza + model profiles" (18:13-19:00)

## Summary
Se creo la feature **Model Interaction Profiles**: convencion para fichar como interactua un modelo (no que tan bien responde), con probe estandarizado "Test de la Pizza" para comparabilidad entre modelos.

- `docs/model_profiles/README.md` - convencion: probe de 4 momentos (ensenanza por capas, correccion forzada, senal de contexto personal, pregunta de contraste) + 8 rasgos fijos con evidencia verbatim obligatoria.
- `docs/model_profiles/nemotron-3-ultra-cloud.md` - primera ficha (sesion real de pizza pepperoni). Debilidades honestas incluidas: sobre-entrega de volumen, recalibracion ADHD forzada por senal del usuario.
- Skill `model-interaction-profile` creado en el workshop (reutilizable en futuras sesiones).

## Decisions
- Ruta A (ficha narrativa) ahora; ruta B (rubrica con scores del juez) cuando haya 3+ modelos fichados con el mismo probe.
- La ficha corresponde al modelo que produjo la interaccion (nemotron-3-ultra:cloud), confirmado por Gonzo; el runtime del cierre no es evidencia de identidad (ver learning "Identidad del modelo" en DB).

## Commits
- `80e8264` docs(model-profiles): add interaction profile convention and first profile
- `179f222` docs(model-profiles): fix model identity to nemotron-3-ultra:cloud
- `5517291` docs: add KNOWN-PITFALLS (sesion paralela)

## Next Steps
1. [ ] Fichar 2 modelos mas con el mismo probe (habilita ruta B: rubrica comparable)
2. [ ] Evaluar integrar las fichas al catalogo de modelos del lab (tab existente)
3. [ ] Opcional: probe "Test de la Pizza" como prompt reutilizable en el Prompt Catalog

## Open Questions
- [ ] Donde viven las fichas en la UI del lab (docs hoy, tab despues?)