# PROGRESO - radix-primitives

Capa 3. Se actualiza despues de cada topic. Fuente de verdad del avance.

**XP:** 10 por topic completado | **Badges:** 1 por nivel | **Jefe final:** ADR de adopcion.

---

## Tabla de progreso

| Nivel | Topics | Cubiertos | XP | Badge |
|---|---|---|---|---|
| 1 - Modelo mental | 10 | 10 (verificacion pendiente) | 0 | 🔴 |
| 2 - La API | 14 | 0 | 0 | 🔴 |
| 3 - Accesibilidad | 10 | 0 | 0 | 🔴 |
| 4 - Stack real | 8 | 0 | 0 | 🔴 |
| 5 - Criterio | 4 | 0 | 0 | 🔴 |
| **Total** | **46** | **10** | **0** | - |

---

## Estado actual

**Pasada:** mapeo (Capa 1) completada el 2026-09-14. No suma XP.
**Nivel 1:** teoria cubierta (10/10 topics) en `nivel-1-modelo-mental.md`. **Verificacion pendiente** - los 3 puntos del final del cuaderno. El XP del nivel y el badge se otorgan al verificar.
**Siguiente:** Nivel 2 (la API) una vez cerrada la verificacion del Nivel 1.

---

## Registro

| Fecha | Topic | Resultado | XP |
|---|---|---|---|
| 2026-09-14 | (mapeo) | Plan maestro con 5 niveles / 46 topics. Fuente: docs oficiales verificados. | 0 |
| 2026-09-14 | Nivel 1 (1.1.1 a 1.4.3) | Teoria cubierta: problema que resuelve, 6 propiedades, anatomia, limites. Cuaderno `nivel-1-modelo-mental.md`. Verificacion pendiente. | 0 |

---

## Deuda / dudas abiertas

- Verificar la version real de Radix instalada en los proyectos antes de afirmar comportamiento (la doc puede ir adelante de lo instalado). No hay lockfile en el workspace - el codigo vive en repos aparte.
- Sin confirmar aun: que primitives se usan de verdad en `kanam-pulse`, `soporteml-v4` y `kanam-forge`, y cuales llegan via shadcn.
