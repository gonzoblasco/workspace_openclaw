# Research Spike

Investigación técnica para reducir incertidumbre.

## ¿Para qué sirve?

Para **investigar tecnologías, librerías o arquitecturas** antes de tomar decisiones. No implementa soluciones, no escribe código de producción. Su misión es responder "¿qué necesitamos aprender antes de construir?".

**Filosofía:** Learn first. Build second. Un Spike compra conocimiento, no funcionalidades.

## ¿Cuándo usarlo?

- Tecnología nueva
- Librería desconocida
- API externa
- Arquitectura incierta
- Decisión importante entre alternativas
- Proof of concept
- Dudas sobre viabilidad

## ¿Cómo se usa?

### Workflow completo

1. **Research Question** — definir una única pregunta (ej: "¿Conviene Supabase o Neon?")
2. **Success Criteria** — ¿qué evidencia necesitamos?
3. **Scope** — qué investigamos, qué NO, tiempo máximo
4. **Information Gathering** — fuentes primarias > secundarias
5. **Experimentation** — prototipo mínimo, descartable
6. **Analysis** — comparar alternativas con weighted scoring
7. **Recommendation** — qué, por qué, evidencia, confianza
8. **Knowledge Capture** — SPIKE_REPORT.md, ADRs

### Scripts útiles

```bash
# Generar template de spike report
./scripts/generate-spike.sh --question "¿Conviene MCP o REST para esta integración?"

# Template de comparación de alternativas
./scripts/compare-alternatives.sh --options "Supabase,Neon" --criteria "perf,cost,ecosystem"
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/template.md` | Template de SPIKE_REPORT.md |
| `references/sources.md` | Fuentes de investigación |
| `references/research-methods.md` | Primary vs secondary, experiment design, decision framework |

## Skills relacionadas

- [Product Discovery](../product-discovery) — Para investigar viabilidad de producto
- [Task Execution](../task-execution) — Para implementar lo aprendido en el spike
