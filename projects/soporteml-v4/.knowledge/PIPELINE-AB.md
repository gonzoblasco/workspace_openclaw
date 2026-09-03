# SoporteML V4 - Pipeline A/B

> **Definido:** 2026-08-18
> **Metodología:** adaptada de la skill `agent-orchestration-pipeline` (validada en Kanam Story Fase 3, donde el cross-review atrapó un bug real que el orquestador no detectó).

## Qué es

Pipeline de desarrollo en cadena con **revisión cruzada multi-ronda** entre dos agentes implementadores (A y B), coordinados por un orquestador (Kanam). Cada unidad atómica la desarrolla un agente y la revisa el otro antes de avanzar.

## Roles

### Orquestador (Kanam)
- Planifica y divide el trabajo en **unidades atómicas** (U1, U2, ...) con criterios de aceptación.
- Asigna paridad: **A = unidades impares, B = unidades pares**.
- Define las reglas del pipeline y el flujo de cross-review.
- Coordina el cierre (release, changelog, tag).
- Documenta en `PLAN.md` + `STATUS.md` + `HANDOFF.md`.
- NO desarrolla unidades de los agentes (salvo tareas de orquestación: tests de infra, refactors, o cuando asume una unidad directamente).

### Agentes implementadores (A, B)
- Desarrollan su unidad asignada (commit atómico + push).
- **REVISAN la unidad que el otro agente acaba de completar** (cross-review) antes de empezar la suya.
- Corrigen bugs de la unidad revisada si los encuentran.
- Dejan mensaje claro de qué hicieron y qué necesita revisión.

## Reglas de oro

1. **Cada unidad = commit atómico + push.** Nada de commits monolíticos.
2. **Nadie avanza sin que el otro valide.** Pipeline en cadena.
3. **Cross-review multi-ronda.** Para calidad alta, el código puede pasar por varias rondas.
4. **Criterios de aceptación explícitos por unidad.** El orquestador los define; el agente los verifica al cerrar.
5. **Verificación obligatoria:** build + tests + lint verdes antes de commitear (el pre-commit hook ya lo enforcea).
6. **No romper invariantes del sistema** (multi-tenant, ADRs, identidad V4). Si una corrección los tocaría, señalarlo en vez de romperlos.
7. **Paridad A/B:** A desarrolla impares, B pares. Cada uno revisa la del otro.
8. **Docs al día:** al cerrar cada unidad, actualizar PLAN/STATUS/HANDOFF y commitear al workspace.

## Flujo (pipeline en cadena)

```
Orquestador: planificar + dividir en unidades + asignar paridad
   ↓
Agente A: desarrolla U1 + push
   ↓
Agente B: REVISA U1 + desarrolla U2 + push
   ↓
Agente A: REVISA U2 + desarrolla U3 + push
   ↓
Agente B: REVISA U3 + desarrolla U4 + push
   ↓
... (se alterna hasta la última unidad)
   ↓
Cierre: A y B revisan el conjunto + orquestador hace release
```

## Próximas unidades (Fase 1 - pulido + integraciones)

> Definidas al cerrar la Fase 0 (7 features core + SLA + lint + hooks). Se revisan y ajustan al alcanzarlas.

| Unidad | Descripción | Criterios de aceptación | Agente |
|--------|-------------|------------------------|--------|
| U1 | **Ajuste fino RAG** - subir minScore (0.2) o filtrar por similitud mínima para consultas sin match | "¿Aceptan cuotas?" no devuelve artículo irrelevante; tests del RAG actualizados | A |
| U2 | **Code-splitting** - resolver warning de chunk > 500kB (lazy load de vistas) | Build sin warning de chunk; las vistas cargan bajo demanda | B |
| U3 | **Validación visual de Gonzo** - ajustar colores/espaciado/tipografía según feedback | Ajustes aplicados + verificado en browser | A |
| U4 | **Email (Resend)** - integrar envío de alertas SLA + notificaciones | Alerta SLA dispara email real; config en .env | B |
| U5 | **Mercado Pago** - validar flujo de billing real (nunca probado) | Suscripción real funciona; manejo de errores | A |
| U6 | **OAuth MeLi real** - validar flujo con túnel persistente | Login OAuth real funciona; sync trae preguntas reales | B |

**Nota:** U3 (validación visual) requiere a Gonzo - es una unidad de orquestación que no puede delegarse a un agente sin su input. Se coordina directamente.

## Checklist de cierre

- [ ] Todas las unidades desarrolladas y revisadas (al menos 1 ronda de cross-review por unidad).
- [ ] Build + tests + lint verdes en el estado final.
- [ ] PLAN.md con todas las unidades marcadas (hecho + revisada por quién).
- [ ] STATUS.md y HANDOFF.md actualizados.
- [ ] CHANGELOG con la entrada del release.
- [ ] Lección aprendida registrada (si el cross-review atrapó un bug, documentarlo).

## Relación con el ecosistema

- **Skill base:** `agent-orchestration-pipeline` (orquestación multi-agente con cross-review).
- **Skills de Build/Review** (`incremental-implementation`, `test-driven-development`, `code-review-and-quality`) aplican a nivel de cada unidad.
- **Pre-commit hooks** (lint + test) enforcean la regla 5 automáticamente.
- **`.knowledge/` vivo:** PLAN, STATUS, HANDOFF se actualizan al cerrar cada unidad.
