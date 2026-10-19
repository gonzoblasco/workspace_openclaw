# ADRs Globales

Decisiones de arquitectura de alcance general, aplicables a cualquier proyecto del workspace.

## Indice

| # | Titulo | Origen |
|---|---|---|
| ADR-001 | [Product Pipeline Integration](./ADR-001-product-pipeline-integration.md) | kanam-workflow |
| ADR-002 | [OpenSpec as Primary Doc Format](./ADR-002-openspec-primary-doc-format.md) | kanam-workflow |
| ADR-003 | [Product Reset Phase Triggers](./ADR-003-product-reset-triggers.md) | kanam-workflow |
| ADR-005 | [OSS Contribution Pipeline](./ADR-005-oss-contribution-pipeline.md) | kanam-workflow |
| ADR-007 | [Patrones de Agente Autonomo - Goal-Oriented Architecture](./ADR-007-patrones-agente-autonomo.md) | kanam-workflow |
| ADR-008 | [Patron convergente](./ADR-008-patron-convergente.md) | ai-engineering-bootcamp |
| ADR-009 | [Primitives, Conventions, Levers](./ADR-009-primitives-conventions-levers.md) | remix-book |
| ADR-010 | [Server/Client file naming convention](./ADR-010-server-client-file-convention.md) | remix-book |
| ADR-011 | [Next.js como Plataforma Full-Stack por Defecto](./ADR-011-nextjs-fullstack-platform.md) | workspace |
| ADR-012 | [Supabase como BaaS por Defecto](./ADR-012-supabase-baas.md) | workspace |
| ADR-013 | [Vitest como Test Runner por Defecto](./ADR-013-vitest-over-jest.md) | workspace |
| ADR-014 | [TypeScript en Archivos de Test](./ADR-014-typescript-for-tests.md) | workspace |
| ADR-015 | [Data Fetching con TanStack Query](./ADR-015-data-fetching-tanstack-query.md) | workspace |
| ADR-017 | [Preferir Hooks sobre HOCs y Render Props](./ADR-017-hooks-sobre-hocs.md) | testing-react-library |
| ADR-020 | [Vite as Default Bundler Over webpack](./ADR-020-vite-default-bundler.md) | fullstack-graphql-react |
| ADR-021 | [createRoot API for React Entry Point](./ADR-021-createroot-api.md) | fullstack-graphql-react |
| ADR-025 | [Enfoque Iterativo para Adopcion de Tooling](./ADR-025-enfoque-iterativo-tooling.md) | react-18-design-patterns |
| ADR-028 | [Biome como Toolchain Unificado](./ADR-028-biome-toolchain.md) | react-18-design-patterns |
| ADR-034 | [Server Components como Estandar de SSR](./ADR-034-server-components-estandar.md) | react-18-design-patterns |
| ADR-037 | [Lucide como iconos base](./ADR-037-lucide-iconos-base.md) | react-18-design-patterns |
| ADR-038 | [Learnings con mirror en DB (categorias + consulta veloz)](./ADR-038-learnings-mirror-db.md) | workspace |
| ADR-042 | [Stripe como proveedor de pagos unico reconocido](./ADR-042-stripe-pagos.md) | workspace |
| ADR-043 | [Complexity-Driven Pipeline (Orquestación por T-Score)](./ADR-043-complexity-driven-pipeline.md) | workspace |
| ADR-044 | [Methodology Audit - Marco de 8 Fases como Lente de Auditoría](./ADR-044-methodology-audit-framework.md) | workspace |
| ADR-047 | [Kanam Design System como identidad transversal de todo producto](./ADR-047-kanam-design-system.md) | workspace |
| ADR-048 | [Radix/shadcn como capa de UI - adopcion con criterio, no por precedente](./ADR-048-shadcn-radix-stack-ui.md) | workspace |
| ADR-049 | [Claude Code como motor del pipeline A/B (Qwen Code a fallback)](./ADR-049-claude-code-motor-pipeline-ab.md) | workspace |
| ADR-050 | [La memoria de Kanam OS sigue en SQLite local - umbral de migracion a Postgres/Supabase](./ADR-050-memoria-sqlite-local-umbral-migracion.md) | workspace |
| ADR-051 | [Regla de extraccion de lib/ai compartido (construir solo con divergencia real)](./ADR-051-regla-lib-ai-shared.md) | workspace |
| ADR-052 | [Engram como memoria persistente de los agentes de pipeline (standalone, no gentle-ai)](./ADR-052-engram-memoria-agentes-pipeline.md) | workspace |
| ADR-054 | [Kanam OS como app local de lectura sobre memory.db (Next.js + node:sqlite)](./ADR-054-kanam-os-app-local-memoria.md) | workspace |
| ADR-055 | [Bloques managed - settings de la DB propagados a documentos de identidad](./ADR-055-bloques-managed-settings-db.md) | workspace |
| ADR-056 | [Guardas de gobernanza en el pre-commit - guion comun y rutas citadas](./ADR-056-guardas-gobernanza-pre-commit.md) | workspace |
| ADR-057 | [Embeddings en BLOB float32, no JSON de texto](./ADR-057-embeddings-blob-float32.md) | workspace |
| ADR-058 | [Taxonomia normalizada, tabla gemela absorbida y una FK espuria](./ADR-058-taxonomia-normalizada-fk-espuria.md) | workspace |
| ADR-059 | [Contenido markdown descompuesto en campos consultables](./ADR-059-contenido-descompuesto-campos.md) | workspace |
| ADR-060 | [Foreign keys activas en todas las conexiones](./ADR-060-foreign-keys-activas.md) | workspace |
| ADR-061 | [Campos interpretados con revision, y un eje por columna](./ADR-061-campos-interpretados-con-revision.md) | workspace |
| ADR-062 | [Vectores re-cortados por unidad semantica, sin duplicar el texto](./ADR-062-vectores-rechunk-semantico.md) | workspace |
| ADR-063 | [kanam-insight en Python sobre LangChain, no en TypeScript con Bun](./ADR-063-kanam-insight-python-langchain.md) | workspace |
| ADR-064 | [memory-wiki como capa analitica de memoria (modo isolated)](./ADR-064-memory-wiki-capa-analitica.md) | workspace |
| ADR-065 | [DB-first vs doc-only - que documentos viven en el ciclo de la DB y cuales no](./ADR-065-db-first-vs-doc-only.md) | workspace |
| ADR-066 | [Los guardias del workspace no leen codigo de proyectos](./ADR-066-guardias-no-dependen-de-codigo-de-proyecto.md) | workspace |
| ADR-067 | [Los ADRs del workspace no pertenecen a un proyecto - verificar el sujeto antes de borrar](./ADR-067-adrs-del-workspace-no-son-de-un-proyecto.md) | workspace |
| ADR-069 | [Los datos de prueba no comparten base con los datos reales](./ADR-069-datos-de-prueba-no-comparten-base.md) | kanam-story-bible |
| ADR-070 | [Todo estado recuperable expone su via de recuperacion](./ADR-070-estado-recuperable-expone-su-recuperacion.md) | kanam-story-bible |
| ADR-073 | [Transicion a arquitectura de orquestacion multi-agente](./ADR-073-arquitectura-multi-agente.md) | workspace |
| ADR-074 | [Protocolo de despacho y coordinacion multi-agente](./ADR-074-protocolo-despacho-multi-agente.md) | workspace |
| ADR-076 | [Ningun agente hereda un modelo local](./ADR-076-ningun-agente-hereda-modelo-local.md) | workspace |
| ADR-077 | [Pipeline A/B asimetrico (ejecutor liviano, revisor grande)](./ADR-077-pipeline-ab-asimetrico.md) | workspace |
| ADR-078 | [La salida de un sub-agente es un auto-reporte, no un hecho](./ADR-078-salida-subagente-auto-reporte.md) | workspace |
| ADR-079 | [La coleccion de skills deja de publicarse](./ADR-079-skills-dejan-de-publicarse.md) | workspace |
| ADR-080 | [Modelo visual para Kanam STUDIO](./ADR-080-modelo-visual-studio.md) | workspace |
| ADR-082 | [La regla del guion comun deja de ser obligatoria](./ADR-082-fin-de-la-regla-del-guion.md) | workspace |
| ADR-083 | [Frontera de roles - el CORE orquesta y no escribe codigo](./ADR-083-frontera-de-roles-core-no-escribe-codigo.md) | workspace |
| ADR-084 | [Registros de sesion - un solo lugar, fuera del gate, con historia congelada](./ADR-084-registros-de-sesion-un-solo-lugar.md) | workspace |
| ADR-085 | [Una sola maquina - el workspace deja de sincronizarse entre equipos](./ADR-085-una-sola-maquina.md) | workspace |
| ADR-086 | [El embudo de entrada conversacional - triaje, personas, borradores, escalacion y limites de contexto](./ADR-086-embudo-de-entrada-conversacional.md) | workspace |
| ADR-087 | [Cata por rol - los modelos elegidos quedan validados con evidencia](./ADR-087-cata-por-rol-modelos-2026-10-05.md) | workspace |
| ADR-088 | [El pipeline A/B tiene enforcement, no buena voluntad](./ADR-088-pipeline-ab-enforcement.md) | workspace |
| ADR-089 | [Pre-filtro barato en el pipeline A/B (gemma4:cloud) con guard de falso negativo](./ADR-089-prefiltro-pipeline-ab.md) | workspace |
| ADR-090 | [Política de niveles de pensamiento por agente y asignación de modelos por rol](./ADR-090-pensamiento-nivel-configuracion.md) | workspace |
| ADR-092 | [El CHANGELOG vive en una ventana activa de ~30 días, con rotación automatizada](./ADR-092-changelog-ventana-rotacion.md) | workspace |
| ADR-093 | [El plan de sesión como objeto persistente (session-planning-hooks se cablea)](./ADR-093-plan-de-sesion-persistente.md) | workspace |
| ADR-094 | [Etapa 4 de Kanam OS: medir accesibilidad (a11y-scan), cablear tests/node, y cerrar el Tablero](./ADR-094-etapa-4-a11y-scan-tests-node-tablero.md) | workspace |
| ADR-095 | [Re-evaluación de las decisiones de diseño: el contraste se verifica, el sistema existe](./ADR-095-reevaluacion-decisiones-diseno.md) | workspace |
| ADR-096 | [kanam-os adopta el Kanam Design System (y el sistema gana su tema oscuro)](./ADR-096-kanam-os-adopta-design-system.md) | workspace |
| ADR-097 | [Identidad visual de un juego - monocromo por patrones, monocanal de identificacion](./ADR-097-identidad-visual-juego-monocromo-patrones.md) | kanam-tetris |
| ADR-098 | [Los proyectos vuelven al workspace, y `cwd` separa el hogar del agente de su zona de trabajo](./ADR-098-proyectos-vuelven-al-workspace-cwd.md) | workspace |

## Formato

Cada ADR sigue el formato estandar (Contexto, Decision, Consecuencias, Alternativas), sin referencias al proyecto que lo origino; el campo `Origen` del indice es solo trazabilidad.

### Campos del header

| Campo | Contenido |
|---|---|
| `Fecha` | `YYYY-MM-DD` |
| `Estado` | `Aceptado` / `Superseded por ADR-NNN` / `Rechazado` |
| `Decisores` | Quien decide (`Gonzo` / `Gonzo / Kanam`) |
| `Origen` | De donde salio la decision (workspace, proyecto, libro, evaluacion externa) |
| `Relacionado` | ADRs vinculados (opcional) |
| `Supersede` / `Revierte` / `Reemplaza` | Solo si aplica, con el ADR referenciado (opcional) |
| `Actualizado` | Ultima revision (opcional) |

**Idioma del header historicamente mixto:** los ADRs mas viejos usan los campos en ingles (`Status`, `Deciders`, `Scope`); los mas nuevos, en español (`Estado`, `Decisores`). No es una deuda a saldar con un barrido: un ADR nuevo usa la forma en español, y si se toca un ADR viejo por otro motivo, se normaliza su header de paso.

## Como agregar

Cuando un ADR de proyecto se identifique como de alcance general, migrarlo aca:
1. Copiar el contenido.
2. Remover referencias especificas del proyecto.
3. Asignar el proximo numero disponible.
4. Agregar al indice.
5. Dejar una nota en el ADR original del proyecto linkeando al global.
