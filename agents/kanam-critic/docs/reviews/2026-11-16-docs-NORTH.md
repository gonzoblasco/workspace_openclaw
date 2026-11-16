# Revisión SHARP de docs/NORTH.md

**Artefacto:** docs/NORTH.md (slug: docs-NORTH)

## Evidencia (citas)
- Línea 3-5: fecha, actualización y autor, indicando revisión contra fuentes reales. (`/Users/gonzoblasco/.openclaw/workspace/docs/NORTH.md:3-5`)
- Línea 7: nota de reconstrucción que corrige versiones anteriores y elimina frentes inexistentes. (`/Users/gonzoblasco/.openclaw/workspace/docs/NORTH.md:7`)
- Línea 22: enumeración de frentes activos y corrección de errores anteriores. (`/Users/gonzoblasco/.openclaw/workspace/docs/NORTH.md:22`)
- Línea 26-30: definición de Kanam y capas actuales, evidencia de estado vivo y enfoque. (`/Users/gonzoblasco/.openclaw/workspace/docs/NORTH.md:26-30`)
- Línea 40-45 (extracted later): tabla de etapas de madurez con estados y criterios. (`/Users/gonzoblasco/.openclaw/workspace/docs/NORTH.md:40-45`)

## Evidencia del hunter
```json
{ "details": [] }
```

## Puntuación SHARP
- **Sharpness (S): 4** – El documento está preciso, actualiza datos erróneos y cita fuentes reales (líneas 3-5,7,22).
- **Horizon (H): 3** – Define horizontes claros pero algunos frentes siguen sin criterio de listo (OnWheels, kanam-os), indicando visión a medio plazo.
- **Asymmetry (A): 3** – El valor entregado es informativo para el equipo, pero la carga de trabajo para alinearse es moderada.
- **Resistance (R): 4** – El contenido está bien estructurado, con referencias a ADRs y validaciones, lo que lo hace robusto ante cambios.
- **Parsimony (P): 3** – Incluye mucha tabla y detalle; podría simplificarse, pero la complejidad está justificada por la necesidad de claridad.

**Total:** 17 (≤18 → **VETO**)

## Fricciones obligatorias (VETO)
1. **Horizon:** Falta criterio de listo para *OnWheels* y *kanam-os*; se necesita definir métricas de finalización y asignar dueño.
2. **Asymmetry:** El valor del documento no justifica el esfuerzo de mantenerlo actualizado semanalmente; automatizar extracción de datos de dailies reduciría carga.
3. **Parsimony:** Redundancia en la tabla de etapas y horizontes; consolidar en una única sección.
4. **Sharpness:** Algunas afirmaciones sobre procesos laborales siguen desactualizadas (ej. procesos de Disney), requieren verificación continua.
5. **Resistance:** Falta enlace directo a fuentes de datos (scripts o dailies) que permitan reproducir la revisión automáticamente.

## Acción recomendada
- Añadir scripts que generen automáticamente la tabla de frentes activos desde `memory/` y `git log`.
- Actualizar criterios de Horizon con métricas medibles (e.g., número de PRs a11y merged, estado de OnWheels F0).
- Consolidar tablas para reducir complejidad.
