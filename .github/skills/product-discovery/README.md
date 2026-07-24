# Product Discovery

De la idea a la definición del producto.

## ¿Para qué sirve?

Para **llevar una idea de producto a una definición lista para construir**. Fase 0 dividida en 0.1 (Brainstorming & Producto) y 0.2 (Arquitectura & Plan de Ataque). Incluye evaluación de mercado, definición de MVP, especificación OpenSpec y ADRs iniciales.

## ¿Cuándo usarlo?

- Cuando tenés una idea de producto y querés evaluarla
- Cuando necesitás definir MVP, features y métricas
- Cuando querés documentar una especificación formal antes de arrancar
- Para hacer retrospectiva post-lanzamiento

## ¿Cómo se usa?

### Fase 0.1 — Brainstorming & Producto
**Output:** `BRIEF.md`, `DEFINITION.md`

Técnicas: SCAMPER, First Principles, Inversion. Define problema, audiencia, features core, métricas de éxito.

### Fase 0.2 — Arquitectura & Plan de Ataque
**Output:** OpenSpec, ADRs, `ROADMAP.md`

Toma la definición y la baja a tierra: stack definitivo, patrones arquitectónicos, esquemas de DB, diagramas C4, epics y tasks.

### Scripts útiles

```bash
# Generar BRIEF.md
./scripts/generate-brief.sh --name "Mi App" --problem "Los devs pierden tiempo escribiendo tests"

# Generar OpenSpec de feature
./scripts/generate-openspec.sh --name "Login con Google" --epic "Auth"

# Validar que los outputs están completos
python3 scripts/validation-gate.py

# Generar story map interactivo
python3 scripts/generate_story_map.py --input data.json --output story_map.html
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/brainstorming.md` | SCAMPER, First Principles, Inversion, Problem Statement |
| `references/market-analysis.md` | Competitive matrix, market sizing, validation questions |
| `references/openspec-guide.md` | Estructura OpenSpec, delta vs as-built |
| `references/ubiquitous-language.md` | Glosario DDD, detección de ambigüedades |

## Skills relacionadas

- [Build & Scaffold](../build-scaffold) — Para construir el proyecto post-discovery
- [Technical Documentation](../tech-docs) — Para documentar decisiones de producto
