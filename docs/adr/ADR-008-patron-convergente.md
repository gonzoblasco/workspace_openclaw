# ADR-008: Patrón Convergente - Detectar Cuándo el Contexto Cambia

**Status:** Accepted  
**Deciders:** Gonzo / Kanam  
**Fecha:** 2026-08-05  
**Actualizado:** 2026-10-15  
**Origen:** ai-engineering-bootcamp ADR-001

## Contexto

Cuando un patrón se repite muchas veces (ej: crear carpeta nueva por nivel/módulo/feature), la tendencia natural es aplicarlo por inercia. Funciona mientras el contexto se mantiene igual.

El problema aparece cuando **el contexto cambia pero el patrón se aplica igual**.

## Decisión

Antes de aplicar un patrón repetido N veces, preguntar obligatoriamente:

1. **"¿Este caso es realmente igual a los que ya resolví?"**
2. **"¿Construyo algo nuevo o transformo lo existente?"**
3. **"¿El patrón sigue siendo válido con el contexto actual?"**

## Señal de Alerta

> **La señal no es "¿lo sé hacer?" sino "¿es este caso realmente igual a los que ya resolví?"**

## Lección General Validada

Se validó empíricamente en bootcamp de 10 niveles:
- **Niveles 1-7**: Lineales - cada uno creaba proyecto nuevo (patrón divergente)
- **Niveles 8-10**: Convergentes - extendían sistemas existentes (patrón convergente)

La predicción del patrón convergente se confirmó en los 3 niveles finales.

## Consecuencias

| Positivas | Negativas |
|-----------|-----------|
| Evita estructura innecesaria cuando el trabajo es transformar | Agrega fricción momentánea al workflow |
| Fuerza pausa reflexiva antes de actuar por costumbre | Requiere disciplina para no saltarse la pregunta |
| Documenta criterio para decisiones futuras similares | |

## Aplicación Práctica (2026-10)

En cualquier workspace que use este patrón:
- Crear `projects/<slug-new>/` cuando se debe extender `projects/<slug-existing>/`
- Duplicar skills cuando se debe extender una existente (`skill_workshop` vs nueva skill)
- Nuevo ADR cuando uno existente cubre la decisión (regla de oro: ADR resuelto no se revisa)

## Referencias

- [ADR-009](./ADR-009-primitives-conventions-levers.md): Framework de análisis de tecnologías
- [ADR-082](./ADR-082-fin-de-la-regla-del-guion.md): Fin de regla del guión (relacionado con inercia de naming)

---

*Actualizado 2026-10-15: ejemplos conectados a workspace actual*