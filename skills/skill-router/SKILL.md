---
name: skill-router
metadata:
  category: "Orchestration"
  tags:
    - skills
    - routing
    - seleccion
description: "Sugiere que skill usar para una tarea dada. Dado un prompt/objetivo, matchea contra las skills disponibles (por keywords y embeddings semantico local) y devuelve las top sugerencias. Usar al iniciar una tarea para saber cual skill aplicar."
user-invocable: false
---

# Skill Router

Sugerir que skill aplicar a una tarea, usando matching local (keyword + embeddings Ollama). Portado del concepto del plugin skill-ai-inject (ClawHub), adaptado a nuestro workspace.

## Cuando usar

- Al iniciar una tarea/objetivo y no estar seguro de cual skill(es) aplicar.
- Cuando hay multiples skills candidatas y se quiere priorizar.
- Para recordar que skills existen y cual encaja con la tarea actual.

## Como usarlo

### Listar skills disponibles

```bash
./scripts/skill-router.py --list
```

### Sugerir skills para una tarea

```bash
./scripts/skill-router.py "<descripcion de la tarea>"
./scripts/skill-router.py -n 5 "<tarea>"   # top 5
```

### Interpretar resultados

- Cada sugerencia muestra: nombre de skill, score, tipo de match (embed = semantico, keyword = por palabra), y L1 (cantidad de keywords coincidentes).
- El score de **embedding (semantico) domina** - refleja la intencion real de la tarea.
- El keyword (L1) es refuerzo: suma un bonus pequeno si la tarea contiene palabras clave de la skill.
- Si no hay coincidencias claras, reconsiderar la descripcion o ver `--list`.

## Ejemplos validados

| Tarea | Top skill sugerida |
|---|---|
| "review this code before merging" | code-review-and-quality |
| "set up a CI/CD pipeline" | ci-cd-and-automation |
| "validar accesibilidad de un componente antes de abrir PR en OSS" | a11y-at-validation, oss-contribution |
| "design a REST API for the module" | api-and-interface-design |

## Requisitos

- **Ollama local** corriendo con el modelo `qwen3-embedding:0.6b` (el modelo de embeddings del workspace, 1024 dims).
- Python 3 + urllib (estandar) + numpy (opcional, solo si se usa).

## Limites

- El matching no es perfecto: tareas internas de infraestructura (ej. "guardar sesion") pueden no matchear bien. Usar el criterio de Kanam para decidir, la skill router es una sugerencia, no una autoridad.
- Solo escanea `skills/` del workspace (no skills de plugins bundled ni de kanam-skills externo).
- Requiere Ollama corriendo para el embedding (si no, cae a solo keyword match).

## Related

- [Agent Orchestration Pipeline](../agent-orchestration-pipeline): el pipeline donde Kanam decide que skill usar por unidad.
- [Knowledge Management](../knowledge-management): gestion de la base de skills/conocimiento.
