# ADRs Globales

Decisiones de arquitectura de alcance general, aplicables a cualquier proyecto del workspace.

## Cómo leer este índice

- El índice está **catalogado por concepto**. Un ADR puede aparecer en más de una categoría si gobierna más de un plano.
- Los **grupos conceptuales** (marcados con ⚠️ en la sección Conceptos) reúnen ADRs que **tocan el mismo concepto**: cada uno decide una cara distinta de ese objeto. Ninguno duplica a otro, y al tocar uno hay que leer el grupo completo antes de decidir.
- Decisiones específicas de una herramienta o rol viven en `docs/ecosystem/` (no están acá). Decisiones de un proyecto viven en el repo del proyecto (ADR-067). Ver secciones al final.

## Índice por categoría

### Ciclo de definición de producto
| ADR | Decide |
|---|---|
| ADR-001 | [Product Definition Cycle](./ADR-001-product-pipeline-integration.md) | El ciclo de 4 etapas (reconocimiento → discovery → specs → diseño) como forma de convertir una idea en producto, sin escribir código |
| ADR-002 | [kanam-spec Primary Doc Format](./ADR-002-openspec-primary-doc-format.md) | kanam-spec (7 secciones fijas) como formato primario de especificación |
| ADR-003 | [Product Definition Cycle - Stage Advancement Triggers](./ADR-003-product-reset-triggers.md) | Triggers y gates medibles para avanzar etapa; grow/pivot = decisión manual |
| ADR-005 | [OSS Contributions - Manual, Not Automated Pipeline](./ADR-005-oss-contribution-pipeline.md) | OSS = actividad manual de Gonzo, no pipeline automatizado |

### Arquitectura de agentes
| ADR | Decide |
|---|---|
| ADR-007 | [Patrones de Agente Autónomo - Goal-Oriented Architecture](./ADR-007-patrones-agente-autonomo.md) | Patrones de agente autónomo (goal-oriented) como marco de delegación |
| ADR-073 | [ADR-073 - Transición a Arquitectura de Orquestación Multi-Agente](./ADR-073-arquitectura-multi-agente.md) | Multi-agente por roles especializados (CORE/DEV/OPS/MIND/STUDIO + juicio) |
| ADR-074 | [Protocolo de Despacho y Coordinación Multi-Agente](./ADR-074-protocolo-despacho-multi-agente.md) | El CORE despacha, no ejecuta; contexto de traspaso entre agentes |
| ADR-083 | [Frontera de roles - el CORE orquesta y no escribe código](./ADR-083-frontera-de-roles-core-no-escribe-codigo.md) | ⚠️ Pipeline A/B (con 043/049/077/088/089/090) - frontera de roles enforced estructuralmente |
| ADR-078 | [La salida de un sub-agente es un auto-reporte, no un hecho](./ADR-078-salida-subagente-auto-reporte.md) | La salida de un sub-agente es un auto-reporte; el padre verifica el repo |
| ADR-086 | [El embudo de entrada conversacional - triaje, personas, borradores, escalación y límites de contexto](./ADR-086-embudo-de-entrada-conversacional.md) | Embudo de entrada conversacional (triaje, borradores, escalación, límites) |
| ADR-093 | [El plan de sesión como objeto persistente (session-planning-hooks se cablea)](./ADR-093-plan-de-sesion-persistente.md) | El plan de sesión como objeto persistente (cableado a hooks) |
| ADR-099 | [LangChain es la capa de ejecución de flujos, no el orquestador](./ADR-099-langchain-capa-de-ejecucion.md) | ⚠️ Arquitectura de agentes (con 073/074/083) - LangChain ejecuta flujos dentro de un proyecto; el gateway sigue orquestando |

### Pipeline A/B (un objeto, siete caras: leer el grupo antes de tocar)
| ADR | Cara que decide |
|---|---|
| ADR-043 | [Complexity-Driven Pipeline (Orquestación por T-Score)](./ADR-043-complexity-driven-pipeline.md) | CUÁNDO y con qué profundidad corre el pipeline (T-score 1-20) |
| ADR-049 | [Claude Code como Motor del Pipeline A/B (Qwen Code a Fallback)](./ADR-049-claude-code-motor-pipeline-ab.md) | EN QUÉ HARNESS corren los agentes (Claude Code; Qwen fallback) |
| ADR-077 | [Pipeline A/B asimetrico (ejecutor liviano, revisor grande)](./ADR-077-pipeline-ab-asimetrico.md) | LA FORMA: asimetría - el revisor ve más que el ejecutor |
| ADR-088 | [El pipeline A/B tiene enforcement, no buena voluntad](./ADR-088-pipeline-ab-enforcement.md) | EL ENFORCEMENT: el pacto A/B está verificado mecánicamente |
| ADR-089 | [Pre-filtro barato en el pipeline A/B (gemma4:cloud) con guard de falso negativo](./ADR-089-prefiltro-pipeline-ab.md) | EL PRE-FILTRO: gemma4 triagea, pero no autoriza solo |
| ADR-090 | [Política de niveles de pensamiento por agente y asignación de modelos por rol](./ADR-090-pensamiento-nivel-configuracion.md) | LOS MODELOS Y NIVEL DE THINKING por rol (política vigente, verificada contra runtime) |
| ADR-102 | [minimax-m3.1-flash:cloud como motor del CORE (main)](./ADR-102-minimax-m31-flash-motor-core-archived.md) | ⚠️ Modelos LLM (con 076/090/107) - el CORE pasó a minimax-m3.1-flash por cata de 8 roles x 5 clases (**superseded por ADR-107**; archivo con sufijo `-archived`) |
| ADR-107 | [Swap deepseek/minimax en CORE y defaults por ahorro de recursos](./ADR-107-swap-deepseek-minimax-ahorro-recursos.md) | ⚠️ Modelos LLM (con 076/090) - deepseek-v4.1-flash vuelve a primario del CORE y defaults; minimax queda alternativo; gemma4 sigue Helper; el pipeline no cambia |
| ADR-105 | [El pipeline pasa de A/B a A/B/C: el tercer agente es la red de tests](./ADR-105-pipeline-abc-tercer-agente-red-de-tests.md) | EL TERCER ROL: C escribe la red de regresión (minimax); el rework vuelve a A, con la condición de que todo finding de B se convierta en un test de C |
| ADR-106 | [Se retiran opencode y OpenHands; Claude Code queda como único harness](./ADR-106-retiro-opencode-y-openhands.md) | ⚠️ Herramientas transversales (con 104/105) - el criterio es "el que responda bien siempre", no el mejor promedio |

### Modelos LLM (política de asignación)
| ADR | Decide |
|---|---|
| ADR-076 | [Ningun agente hereda un modelo local (cloud primero, locales como ultimo recurso)](./ADR-076-ningun-agente-hereda-modelo-local.md) | Ningún agente hereda un modelo local (cloud primero); primary+fallbacks explícitos |
| ADR-090 | [Política de niveles de pensamiento por agente y asignación de modelos por rol](./ADR-090-pensamiento-nivel-configuracion.md) | ⚠️ Pipeline A/B (con 043/049/077/088/089) - asignación vigente de modelos por rol |
| ADR-102 | [minimax-m3.1-flash:cloud como motor del CORE (main)](./ADR-102-minimax-m31-flash-motor-core-archived.md) | ⚠️ Modelos LLM (con 076/090/107) - reasignación del rol `main` a minimax-m3.1-flash:cloud (**superseded por ADR-107**; archivo con sufijo `-archived`) |
| ADR-107 | [Swap deepseek/minimax en CORE y defaults por ahorro de recursos](./ADR-107-swap-deepseek-minimax-ahorro-recursos.md) | ⚠️ Modelos LLM (con 076/090) - `main` y los defaults vuelven a `deepseek-v4.1-flash:cloud`; minimax pasa a fallback; el pipeline A/B queda intacto |
| ADR-103 | [LiteLLM se descarta - la capa de router ya existe en el stack propio](./ADR-103-litellm-se-descarta.md) | ⚠️ Modelos LLM (con 076/090) - no se adopta un gateway LLM: el routing, budgets y guardrails ya están en el stack; queda el multi-tenant como deuda |
| ADR-104 | [La búsqueda laboral como proceso factorizado, no como odisea por puesto](./ADR-104-busqueda-laboral-proceso-factorizado.md) | La postulación es un skill con adaptadores por ATS: el know-how de formularios de terceros se paga una vez, y el envío siempre queda para Gonzo |

### Memoria y datos (una arquitectura, distintas caras)
| ADR | Cara que decide |
|---|---|
| ADR-038 | [Learnings con Mirror en DB (Categorías + Consulta Veloz)](./ADR-038-learnings-mirror-db.md) | Learnings: fuente de verdad en DB, markdown espejo regenerable |
| ADR-050 | [La memoria de Kanam OS sigue en SQLite local - umbral de migracion a Postgres/Supabase](./ADR-050-memoria-sqlite-local-umbral-migracion.md) | La memoria en SQLite local + los umbrales que justificarían migrar |
| ADR-055 | [Bloques managed - settings de la DB propagados a documentos de identidad](./ADR-055-bloques-managed-settings-db.md) | Los valores globales viven una vez (settings de la DB → bloques managed) |
| ADR-065 | [DB-first vs doc-only - que documentos viven en el ciclo de la DB y cuales no](./ADR-065-db-first-vs-doc-only.md) | Qué documentos entran al ciclo DB-first y cuáles son doc-only |
| ADR-057 | [El data-layer de memory.db - refactor integral en seis fases](./ADR-057-data-layer-memory-db-refactor-integral.md) | La campaña completa del data-layer: BLOB embeddings, taxonomía, contenido consultable, FKs activas, un eje por columna, rechunk semántico (absorbe 058-062) |

### Kanam OS (el visor)
| ADR | Decide |
|---|---|
| ADR-054 | [Kanam OS como app local de lectura sobre `memory.db` (Next.js + node:sqlite)](./ADR-054-kanam-os-app-local-memoria.md) | kanam-os = app local read-only sobre memory.db (el proyecto vive en `projects/kanam-os`) |

### Diseño (un sistema, tres decisiones complementarias)
| ADR | Decide |
|---|---|
| ADR-047 | [Kanam Design System como identidad transversal de todo producto](./ADR-047-kanam-design-system.md) | El Kanam Design System como identidad transversal (tokens, temas, contraste) |
| ADR-048 | [Radix/shadcn como capa de UI - adopcion con criterio, no por precedente](./ADR-048-shadcn-radix-stack-ui.md) | Radix/shadcn como capa de UI, con criterio explícito y disparadores de revisión |
| ADR-037 | [Lucide como Iconos Base](./ADR-037-lucide-iconos-base.md) | Lucide como librería de iconos; nunca emojis como iconografía |

### Stack de frontend
| ADR | Decide |
|---|---|
| ADR-011 | [Next.js como Plataforma Full-Stack por Defecto](./ADR-011-nextjs-fullstack-platform.md) | Next.js full-stack por defecto (web media complejidad) |
| ADR-012 | [Supabase como BaaS por Defecto](./ADR-012-supabase-baas.md) | Supabase como BaaS por defecto |
| ADR-013 | [El stack de testing - Vitest con TypeScript](./ADR-013-vitest-typescript-testing.md) | Vitest como runner + TypeScript en los tests (una decisión, dos caras; absorbe el viejo ADR de TS-tests) |
| ADR-015 | [Data Fetching con TanStack Query](./ADR-015-data-fetching-tanstack-query.md) | TanStack Query para data fetching en cliente |
| ADR-017 | [Hooks Sobre Hocs](./ADR-017-hooks-sobre-hocs.md) | Hooks como mecanismo de compartir lógica (HOCs legacy) |
| ADR-020 | [Vite Default Bundler](./ADR-020-vite-default-bundler.md) | Vite como bundler por defecto |
| ADR-025 | [Enfoque Iterativo para Tooling](./ADR-025-enfoque-iterativo-tooling.md) | Tooling se adopta iterativo (YAGNI), no por anticipación |
| ADR-028 | [Biome Toolchain](./ADR-028-biome-toolchain.md) | Biome como toolchain unificado (lint+format+imports) |
| ADR-034 | [Server Components como Estándar de SSR](./ADR-034-server-components-estandar.md) | Server Components / App Router como estándar de SSR |

### Herramientas transversales
| ADR | Decide |
|---|---|
| ADR-037 | [Lucide como Iconos Base](./ADR-037-lucide-iconos-base.md) | ⚠️ Diseño (con 047/048) - Lucide como iconos base |
| ADR-042 | [Stripe como proveedor de pagos unico reconocido](./ADR-042-stripe-pagos.md) | Stripe como único proveedor de pagos reconocido; un proyecto puede evaluar otro proveedor y registrarlo (punto 2 del ADR) |
| ADR-092 | [El CHANGELOG vive en una ventana activa de ~30 días, con rotación automatizada](./ADR-092-changelog-ventana-rotacion.md) | CHANGELOG en ventana de 30 días con rotación automatizada |

### Gobernanza e higiene del workspace
| ADR | Decide |
|---|---|
| ADR-044 | [Methodology Audit - Marco de 8 Fases como Lente de Auditoría](./ADR-044-methodology-audit-framework.md) | Auditoría metodológica periódica (lente de 8 fases, no pipeline) |
| ADR-051 | [Regla de extraccion de `lib/ai` compartido (construir solo con divergencia real)](./ADR-051-regla-lib-ai-shared.md) | Extraer paquete compartido solo con divergencia real (4 condiciones) |
| ADR-056 | [Guardas de gobernanza en el pre-commit - guion comun y rutas citadas](./ADR-056-guardas-gobernanza-pre-commit.md) | Guardas del pre-commit (guion, rutas citadas) sobre todo markdown staged |
| ADR-079 | [La coleccion de skills deja de publicarse (kanam-skills archivado)](./ADR-079-skills-dejan-de-publicarse.md) | La colección de skills deja de publicarse (kanam-skills archivado) |
| ADR-082 | [La regla del guion comun deja de ser obligatoria](./ADR-082-fin-de-la-regla-del-guion.md) | La regla del guion común deja de ser obligatoria (el aparato queda) |
| ADR-084 | [Registros de sesion - un solo lugar, fuera del gate, con historia congelada](./ADR-084-registros-de-sesion-un-solo-lugar.md) | Registros de sesión: un solo lugar, historia congelada, fuera del gate |
| ADR-085 | [Una sola máquina - el workspace deja de sincronizarse entre equipos](./ADR-085-una-sola-maquina.md) | Una sola máquina (Mac Mini); sin sincronización entre equipos |

### Método de análisis y gobernanza de las decisiones mismas
| ADR | Decide |
|---|---|
| ADR-008 | [Patrón Convergente - Detectar Cuándo el Contexto Cambia](./ADR-008-patron-convergente.md) | Antes de repetir un patrón: ¿cambió el contexto? |
| ADR-009 | [Primitives, Conventions, Levers - Framework de Análisis de Tecnologías](./ADR-009-primitives-conventions-levers.md) | Framework para analizar tecnologías (primitivas/convenciones/palancas) |
| ADR-010 | [Server/Client File Convention - Naming como Contrato con el Tooling](./ADR-010-server-client-file-convention.md) | Naming por convención (server/client) como contrato con el tooling |
| ADR-066 | [los guardias del workspace no leen codigo de proyectos](./ADR-066-guardias-no-dependen-de-codigo-de-proyecto.md) | Los guardias del workspace prueban con fixtures, no con código de proyectos |
| ADR-067 | [los ADRs del workspace no pertenecen a un proyecto - verificar el sujeto antes de borrar](./ADR-067-adrs-del-workspace-no-son-de-un-proyecto.md) | Verificar SUJETO y blast radius antes de borrar ADRs; ADRs de proyecto viven en su repo |
| ADR-069 | [los datos de prueba no comparten base con los datos reales](./ADR-069-datos-de-prueba-no-comparten-base.md) | Los datos de prueba no comparten base con los reales |
| ADR-070 | [todo estado recuperable expone su via de recuperacion](./ADR-070-estado-recuperable-expone-su-recuperacion.md) | Estado recuperable = entrega su vía de recuperación en el mismo cambio |
| ADR-095 | [Re-evaluacion de las decisiones de diseno: el contraste se verifica, el sistema existe](./ADR-095-reevaluacion-decisiones-diseno.md) | Design system (con 047/088) - el contraste se mide, no se declara; recuperado el 2026-10-28 tras retirarse por error de clasificacion en 4d2796f6fe |
| ADR-098 | [Los proyectos vuelven al workspace, y `cwd` separa el hogar del agente de su zona de trabajo](./ADR-098-proyectos-vuelven-al-workspace-cwd.md) | Proyectos en `<workspace>/projects/`; `cwd` separa hogar del agente de su zona de trabajo |
| ADR-100 | [Fuente única de la verdad - un dato, un dueño, y un gate que lo verifica](./ADR-100-fuente-unica-de-la-verdad.md) | ⚠️ Duplicación de reglas: dueño por familia de dato + `check-single-source.py` (obligatorio leer antes de agregar un dato a otro archivo) |
| ADR-101 | [Hechos de carrera con dueño único y freno ante contradicción](./ADR-101-hechos-de-carrera-fuente-unica.md) | ⚠️ CVs y postulaciones: un perfil cambia el relato, nunca los hechos; `career-facts.md` + `check-cv-facts.py` |

## Decisiones específicas (no numeradas)

Viven en [`docs/ecosystem/`](../ecosystem/): decisiones sobre una herramienta o rol puntual, que no son ley transversal.

| Archivo | Sujeto |
|---|---|
| [engram-memoria-agentes-pipeline.md](../ecosystem/engram-memoria-agentes-pipeline.md) | Engram (memoria MCP de los agentes de código del pipeline) |
| [memory-wiki-capa-analitica.md](../ecosystem/memory-wiki-capa-analitica.md) | Plugin memory-wiki (modo isolated, política de ingesta) |
| [studio-modelo-visual.md](../ecosystem/studio-modelo-visual.md) | Modelo visual de STUDIO (la política transversal es ADR-090) |
| [cata-por-rol-modelos-2026-10-05.md](../ecosystem/cata-por-rol-modelos-2026-10-05.md) | Evidencia de la cata que fundó la asignación vigente (ADR-090) |
| [mcp-lovable-decision.md](../ecosystem/mcp-lovable-decision.md) | Cliente MCP de Lovable |

**ADRs de proyecto** viven en el repo del proyecto (ADR-067): `kanam-os` tiene 3 (etapas y design system) y `kanam-tetris` 1 (identidad visual) en sus `docs/adr/`.

## Formato

Cada ADR sigue el formato estándar (Contexto, Decisión, Consecuencias, Alternativas), sin referencias al proyecto que lo originó; el campo `Origen` del índice es solo trazabilidad.

### Campos del header

| Campo | Contenido |
|---|---|
| `Fecha` | `YYYY-MM-DD` |
| `Estado` | `Aceptado` / `Superseded por ADR-NNN` / `Rechazado` |
| `Decisores` | Quien decide (`Gonzo` / `Gonzo / Kanam`) |
| `Origen` | De dónde salió la decisión (workspace, proyecto, libro, evaluación externa) |
| `Relacionado` | ADRs vinculados (opcional) |
| `Supersede` / `Revierte` / `Reemplaza` | Solo si aplica, con el ADR referenciado (opcional) |
| `Actualizado` | Última revisión (opcional) |

**Idioma del header históricamente mixto:** los ADRs más viejos usan los campos en inglés (`Status`, `Deciders`, `Scope`); los más nuevos, en español (`Estado`, `Decisores`). No es una deuda a saldar con un barrido: un ADR nuevo usa la forma en español, y si se toca un ADR viejo por otro motivo, se normaliza su header de paso.

### Nombre del archivo: el sufijo `-archived` marca el ADR que ya no rige

El `Estado` dice si la decisión sigue vigente; **el nombre del archivo lo dice también, para quien lo ve en un `ls` o en un `grep` de rutas.** Un ADR cuyo `Estado` no es `Aceptado` (`Superseded por ADR-NNN`, `ARCHIVADO`, `Rechazado`) lleva el sufijo **`-archived`** antes de la extensión:

```
ADR-102-minimax-m31-flash-motor-core-archived.md
```

- **No cambia el número ni la cita.** `ADR-102` se sigue citando como `ADR-102` en prosa, headers y el índice; el sufijo es del archivo, no del identificador.
- **No mueve el archivo de directorio.** Sigue en `docs/adr/` para que el índice, `check-adr-integrity.py` y `check-adr-supersede.py` lo vean: los tres matchean `^ADR-(\d+)-.+\.md$`, que tolera el sufijo.
- **El renombre va con `git mv`** (preserva la historia) **y en el mismo cambio que el estado:** un ADR renombrado que sigue diciendo `Aceptado` en su header es peor que uno sin renombrar. Las dos marcas se ponen juntas o ninguna.
- **Hay que actualizar el link del índice:** las filas del `README.md` apuntan al nombre exacto; dejarlas apuntando al nombre viejo rompe `check-adr-integrity.py` ("LINK ROTO EN EL INDICE"), que es justo lo que se quiere.
- **Solo se renombra lo que ya no rige.** Un ADR `Aceptado` que tiene un apartado superseded (sigue gobernando su materia, con una sección reemplazada) **no** lleva sufijo: marcarlo como archivado sería la segunda ley de siempre.

## Cómo agregar

1. **¿Es transversal?** Si la decisión gobierna cualquier proyecto/rol, here. Si es de una herramienta o rol puntual, `docs/ecosystem/`. Si es de un proyecto, su repo (ADR-067).
2. **¿Toca un concepto ya decidido?** Identificar el grupo ⚠️ del índice y leerlo completo antes de decidir; si la nueva decisión reemplaza una cara, supersede explícito al ADR de esa cara.
3. Asignar el próximo número disponible y sumarlo al índice, en su categoría.
4. Dejar una nota en el ADR original linkeando al global.