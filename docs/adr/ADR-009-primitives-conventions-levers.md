# ADR-009: Primitives, Conventions, Levers - Framework de Análisis de Tecnologías

**Status:** Accepted  
**Deciders:** Gonzo / Kanam  
**Fecha:** 2026-08-05  
**Actualizado:** 2026-10-15  
**Origen:** remix-book ADR-001

## Contexto

Al evaluar tecnología nueva (framework, librería, herramienta), es fácil caer en análisis superficiales: "tiene X features", "es popular", "lo usa Y empresa". Falta un framework estructurado que compare tecnologías por su **filosofía de diseño**, no solo feature set.

## Decisión

Adoptar el mental model **Primitives, Conventions, Levers** como framework de análisis para evaluar cualquier tecnología.

---

### 1. Primitives
Herramientas que la tecnología expone para usar en código: funciones, hooks, componentes, tipos.

**Qué buscar:**
- ¿Son abstracciones delgadas o cajas negras?
- ¿Siguen estándares existentes o inventan los suyos?
- ¿Son composables o obligan a un solo camino?

### 2. Conventions
Contratos entre la tecnología y tu app: naming de archivos, estructura de carpetas, exports esperados. Reducen configuración/boilerplate a cambio de reglas predecibles.

**Qué buscar:**
- ¿Son intuitivas o crípticas?
- ¿Se pueden sobrescribir cuando es necesario?
- ¿La tecnología documenta claramente el contrato?

### 3. Levers
Opciones que la tecnología da para optimizar según tus prioridades. No hay talla única - vos decidís los tradeoffs.

**Qué buscar:**
- ¿Te deja elegir o decide por vos?
- ¿Los levers son explícitos o requieren workarounds?
- ¿Podés cambiar de opinión sin reescribir todo?

---

## Consecuencias

| Positivas | Negativas |
|-----------|-----------|
| Framework portable a cualquier tech (React, Vue, Svelte, Express, etc.) | No todas las techs se mapean limpiamente a 3 categorías |
| Identifica rápido si tech es opinionada en exceso o da control | Algunos features caen en múltiples categorías (ambiguo) |
| Útil para ADRs y docs técnicas: categorizar features | |

## Aplicación en Workspace Actual (2026-10)

| Tecnología | Primitives | Conventions | Levers |
|------------|------------|-------------|--------|
| **Biome** | `lint`, `format`, `check` | `biome.json` schema | `--apply`, `--unsafe`, formatter options |
| **OpenSpec** | Frontmatter keys (`type`, `slug`, `status`) | `specs/` folder, `.md` extension | `status` transitions, custom fields |
| **Vitest** | `test`, `expect`, `describe` | `*.test.ts`, `vitest.config.ts` | `run`, `ui`, `coverage`, `retry` |
| **Lucide** | Icon components (`<Icon />`) | `lucide-react` import | `size`, `strokeWidth`, `absoluteStrokeWidth` |
| **TanStack Query** | `useQuery`, `useMutation` | Query keys as arrays | `staleTime`, `gcTime`, `retry` |

## Uso en ADRs

Al escribir ADRs de adopción tecnológica, categorizar cada feature evaluada:
- **Primitive** → ¿Nos da building blocks composables?
- **Convention** → ¿Nos ahorra config o nos encierra?
- **Lever** → ¿Nos deja elegir tradeoffs críticos?

## Referencias

- [ADR-008](./ADR-008-patron-convergente.md): Patrón convergente (evitar inercia)
- [ADR-028](./ADR-028-biome-toolchain.md): Biome adopción (ejemplo aplicado)
- [ADR-037](./ADR-037-lucide-iconos-base.md): Lucide adopción (ejemplo aplicado)

---

*Actualizado 2026-10-15: tabla de ejemplos con stack actual*