# Experimentos de Debug — Referencia

## Diseño de Experimentos

Cada experimento debe responder **una sola pregunta**.

### Reglas

1. **Una variable a la vez** — nunca cambiar múltiples cosas simultáneamente
2. **Hipótesis explícita** — "Si hago X, espero que ocurra Y"
3. **Resultado medible** — "El error desaparece" / "La latencia baja de 2s a 500ms"
4. **Reproducible** — cualquiera debería poder repetir el experimento
5. **Documentado** — registrar qué se hizo, qué se observó, qué se concluyó

### Tipos de Experimentos

| Tipo | Cuándo usarlo | Ejemplo |
|---|---|---|
| **Logging** | Cuando no hay visibilidad del flujo | Agregar `console.log` en puntos clave |
| **Mocking** | Cuando se sospecha de una dependencia externa | Reemplazar API call con mock |
| **Config change** | Cuando se sospecha de configuración | Cambiar timeout, feature flag, variable de entorno |
| **Data reduction** | Cuando se sospecha de volumen de datos | Reducir dataset a 1 registro |
| **Isolation** | Cuando se sospecha de interacción entre módulos | Ejecutar el módulo en aislamiento |
| **Replay** | Cuando el error es intermitente | Reproducir con los mismos inputs |
| **A/B** | Cuando hay dos posibles causas | Probar con y sin el cambio sospechoso |

## Related

- [SKILL.md](../SKILL.md) — Workflow principal
- [Techniques](./techniques.md) — Técnicas de debugging
