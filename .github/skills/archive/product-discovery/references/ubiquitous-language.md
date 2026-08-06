# Ubiquitous Language — Product Discovery Reference

Extraer y formalizar terminología de dominio en un glosario consistente.

## Proceso

1. **Escanear la conversación** en busca de sustantivos, verbos y conceptos del dominio
2. **Identificar problemas:**
   - Misma palabra usada para diferentes conceptos (ambigüedad)
   - Diferentes palabras para el mismo concepto (sinónimos)
   - Términos vagos o sobrecargados
3. **Proponer glosario canónico** con términos opinados
4. **Escribir a `UBIQUITOUS_LANGUAGE.md`**
5. **Output un resumen** inline en la conversación

## Formato de Salida

```markdown
# Ubiquitous Language

## Order lifecycle

| Term | Definition | Aliases to avoid |
|------|------------|------------------|
| **Order** | A customer's request to purchase items | Purchase, transaction |
| **Invoice** | A request for payment after delivery | Bill, payment request |

## People

| Term | Definition | Aliases to avoid |
|------|------------|------------------|
| **Customer** | Person/org that places orders | Client, buyer, account |
| **User** | Authentication identity in the system | Login, account |

## Relationships

- An **Invoice** belongs to exactly one **Customer**
- An **Order** produces one or more **Invoices**

## Flagged ambiguities

- "account" was used to mean both **Customer** and **User** — distinct concepts
```

## Reglas

- **Ser opinado.** Cuando existan múltiples palabras, elegir la mejor y listar las otras como aliases a evitar.
- **Solo términos del dominio.** Saltar conceptos genéricos de programación (array, function, endpoint).
- **Agrupar en tablas** por subdominio, ciclo de vida o actor.
- **Incluir diálogo de ejemplo** que muestre los términos en uso natural.

## Related

- [SKILL.md](../../product-discovery/SKILL.md) — Workflow principal
- [Brainstorming](../brainstorming.md) — Técnicas de brainstorming
