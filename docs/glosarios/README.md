<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Glosarios

Vocabulario de dominio, reutilizable entre procesos.

## Qué entra acá

- **Vocabulario de un dominio**, con criterio de uso: cuándo se dice cada término, cuál no.
- **Frases hechas** que sirven en más de una situación (ej. narración en inglés para
  grabaciones).
- **Términos de un cliente o plataforma** que se van a repetir (ej. los tiers de Mercor).

## Qué NO entra acá

| No es glosario | Dónde va |
|---|---|
| Un procedimiento paso a paso | `skills/<slug>/SKILL.md` |
| El resumen de un documento puntual | `docs/entrevistas/<proceso>/` |
| Un registro de un proceso | `docs/entrevistas/<proceso>/` |
| Un ADR | `docs/adr/` |

El criterio: **si sirve fuera del proceso para el que se escribió, es glosario.** Si solo tiene
sentido dentro de una postulación, de una sesión o de un cliente, no lo es.

## Nombres

`glosario-<dominio>-<alcance>.md`. El alcance desambigua: `glosario-narracion-mercor.md` no es lo
mismo que `glosario-narracion-general.md`.

## Actuales

| Archivo | Qué cubre |
|---|---|
| `glosario-narracion-mercor.md` | Narrar en inglés mientras se graba una pantalla: frases de ubicación, de acción por fase, trampas del B2+, estructura de 3 minutos. Sirve para cualquier cliente que pida grabaciones narradas, no solo Mercor |
