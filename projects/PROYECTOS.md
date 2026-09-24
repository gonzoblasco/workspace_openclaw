# PROYECTOS.md - Índice Maestro Universal

**Última actualización:** 2026-09-24

> **Regla de oro:** GitHub es la fuente de la verdad. Cada proyecto vive en su propio repo (sin submódulos ni repos dentro del repo). El workspace (`~/.openclaw/workspace`) solo contiene config, memoria y skills. Este archivo es un **índice universal**: lista todos los proyectos de Gonzo en GitHub, sin importar en qué máquina estén clonados (Gonzo trabaja entre dos computadoras y no siempre el mismo proyecto en cada una).
>
> **Repo agregado (2026-09-02):** [`gonzoblasco/projects_openclaw`](https://github.com/gonzoblasco/projects_openclaw) (PRIVADO) contiene el código fuente completo de los 20 proyectos de `projects/` como snapshot consultable (sin `.git/`, sin node_modules/.env/*.db, cada proyecto respeta su propio `.gitignore`). No es la fuente de la verdad para trabajar - el historial de cada proyecto vive en su repo individual.

---

## 🟢 ACTIVOS

| Proyecto | Descripción | Priv | GitHub |
|---|---|---|---|
| **kanam-insight** | Motor de inteligencia transversal: cruza los `.knowledge/` de todos los proyectos para detectar patrones y deuda técnica. Pattern Radar + Debt Detector operativos. | PRIV | gonzoblasco/kanam-insight |
| **langchain-starter** | Starter kit de IA local sobre LangChain: RAG, agentes ReAct y API HTTP con streaming, todo contra Ollama local. Sin proveedores cloud. | PRIV | gonzoblasco/langchain-starter |
| **kanam-story** | Co-writer de ficción local-first. Chat con manos + biblia viva + brújula + outline/beats. | pub | gonzoblasco/kanam-story |
| **kanam-skills** | Skills de agente para todo el trabajo + web pública. | pub | gonzoblasco/kanam-skills |
| **kanam-forge** | Herramienta de forja de skills (fork de Lovable, open source). | pub | gonzoblasco/kanam-forge |
| **kanam-pulse** | Health monitor/cleaner macOS local-first, web-first, a11y de fabrica, IA local. Open source. | pub | gonzoblasco/kanam-pulse |
| **kanam-solitaires** | Colección de solitarios PWA (Klondike, Spider, FreeCell, Pyramid). | pub | gonzoblasco/kanam-solitaires |
| **soporteml** | CRM multi-tenant para ML sellers (v1). | pub | gonzoblasco/soporteml |
| **soporteml-v4** | CRM multi-tenant para ML sellers (reinicio con diseño avanzado). | PRIV | gonzoblasco/soporteml-v4 |
| **kanam-fixer** | Aserciones sobre el anuncio del lector de pantalla (no atributos), mismo contrato en dos planos: virtual (CI) y real (VoiceOver). Ciclo 0.0.1 cerrado 2026-09-15 (S3 limitado por upstream); ciclo 0.0.2: MCP companion server para agentes IA. | pub | gonzoblasco/kanam-fixer |
| **quedamos** | App PWA de matching para salidas. | PRIV | gonzoblasco/quedamos |
| **create-stack** | Scaffolder opinado Next.js. | pub | gonzoblasco/create-stack |
| **ai-developer-stack** | Skills de ingeniería con IA. | pub | gonzoblasco/ai-developer-stack |
| **create-with-ai** | Generador de apps con IA. | PRIV | gonzoblasco/create-with-ai |
| **accessible-ui** | Headless component library accesible. | PRIV | gonzoblasco/accessible-ui |

---

## ❄️ ARCHIVADOS

| Proyecto | Descripción | Priv | GitHub |
|---|---|---|---|
| **soporteml-v3** | CRM para ML sellers - backend sólido (OAuth MeLi, sync, IA, billing). Conservado como activo valioso. | PRIV | gonzoblasco/soporteml-v3 |
| **ai-engineering-bootcamp** | Curso 10/10 completado de AI-assisted development. | pub | gonzoblasco/ai-engineering-bootcamp |
| **umbrawriter** | Escritor de ficción con IA (Lovable). | PRIV | gonzoblasco/umbrawriter |
| **hyatt-copilot-agent** | Agente copilot. | PRIV | gonzoblasco/hyatt-copilot-agent |
| **ensulugar** | Tutor de cocina adaptativo con IA (BYOK). | pub | gonzoblasco/ensulugar |
| **cabala** | Proyecto cabala. | pub | gonzoblasco/cabala |
| **health-tracker** | PWA de monitoreo de salud personal. | pub | gonzoblasco/health-tracker |
| **kanam-mind** | Segundo cerebro local-first con IA. Timeline personal + resumen IA diario. IndexedDB + Ollama local. Archivado del portfolio (reemplazado por kanam-pulse como ancla Local-First). | pub | gonzoblasco/kanam-mind |
| **a11y-fixer** | Accessibility audit bot para PRs de GitHub (axe-core). Archivado 2026-09-14 (decisión de Gonzo); su sucesor es `kanam-fixer`. **Repo archivado en GitHub el 2026-09-15 (`isArchived=true`).** El paquete npm sigue publicado - deprecarlo requiere `npm login`. | pub | gonzoblasco/a11y-fixer |
| **a11y-playground** | Scaffold que nunca pasó de M0: un solo commit (`chore: initial scaffold`), size 0, cero código. Su única dependencia declarada era `a11y-fixer`. Archivado 2026-09-15. | PRIV | gonzoblasco/a11y-playground |

---

## 📋 Notas

- **Forks adoptados como propios:** `kanam-forge` (fork de Lovable) es el único fork que Gonzo adoptó como proyecto propio. Se lista porque es parte del catálogo actual (una versión 100% nuestra vendrá después).
- **Repos espejo OSS (`gonzoblasco-*`):** `gonzoblasco-payload`, `gonzoblasco-primitives`, `gonzoblasco-router` son repos OSS que Gonzo creó como workaround para contribuir con PRs (no son proyectos propios). Se usan solo para OSS.
- **Forks OSS para PRs** (create-t3-app, ui, ai, react-spectrum, material-ui, carbon, zod, astryx, radix, TanStack/query, TanStack/router, etc.): NO son proyectos de Gonzo, se descargan solo para PRs OSS. Viven en GitHub, no se listan aquí.
- **Doble-git:** cuando un proyecto se clona, el workspace trackea solo `projects/<slug>/.knowledge/` + README. El código vive en el repo propio. Sin submódulos.
- Para agregar un proyecto: crear repo en GitHub, clonar en `projects/<slug>/` donde se trabaje, y agregar a la tabla de activos.
