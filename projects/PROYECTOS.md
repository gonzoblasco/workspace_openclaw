# PROYECTOS.md — Índice Maestro

**Última actualización:** 2026-08-23

> **Regla de oro:** GitHub es la fuente de la verdad. Cada proyecto vive en su propio repo (sin submódulos ni repos dentro del repo). El workspace (`~/.openclaw/workspace`) solo contiene config, memoria y skills. Los proyectos se clonan en `projects/<slug>/` cuando se necesitan.

---

## 🟢 ACTIVOS — Con código y actividad (en disco)

| Proyecto | Descripción | Estado | Git |
|---|---|---|---|
| **kanam-story** | Co-writer de ficción local-first. Chat con manos + biblia viva + brújula + outline/beats. | **v0.17.0** — Fase A cerrada. 382 tests. Roadmap a la nube planificado. | ✅ gonzoblasco/kanam-story |
| **kanam-mind** | Segundo cerebro local-first con IA. Timeline personal + resumen IA diario. IndexedDB + Ollama local. | **v0.1.0** — MVP completo. 7 tests. | ✅ gonzoblasco/kanam-mind |
| **soporteml-v4** | CRM multi-tenant para ML sellers. | Activo. | ✅ gonzoblasco/soporteml-v4 |
| **a11y-fixer** | Fixes de accesibilidad. | En curso. | ✅ gonzoblasco/a11y-fixer |
| **kanam-solitaires** | 4 juegos de solitario (Klondike, Spider, FreeCell, Pyramid) — PWA. | **v1.0.0** — 2026-08-01. Primer release público. | ✅ gonzoblasco/kanam-solitaires |
| **quedamos** | App PWA de matching para salidas. | Discovery completo. `.knowledge/` con 11 docs. | ✅ gonzoblasco/quedamos |
| **create-stack** | Scaffolder opinado Next.js. | Publicado en npm. `.knowledge/` con BRIEF, STATUS, ADRs, specs. | ✅ gonzoblasco/create-stack |
| **ai-developer-stack** | Skills de ingeniería con IA. | Clonado. | ✅ gonzoblasco/ai-developer-stack |
| **kanam-skills** | Skills propios de Kanam. | Activo. | ✅ gonzoblasco/kanam-skills |
| **kanam-forge** | Herramienta de forja de skills. | En discovery. | ✅ gonzoblasco/kanam-forge |
| **create-with-ai** | Generador de apps con IA. | Activo. | ✅ gonzoblasco/create-with-ai |
| **accessible-ui** | Headless component library accesible. | Activo. | ✅ gonzoblasco/accessible-ui |
| **soporteml** | CRM multi-tenant para ML sellers (v1). | Activo. | ✅ gonzoblasco/soporteml |

## ❄️ ARCHIVADOS (en GitHub, sin clon local)

Proyectos que existen en GitHub pero **no se clonan** a la mini. Se descargan solo si se reactivan.

| Proyecto | GitHub | Estado |
|---|---|---|
| **soporteml-v3** | gonzoblasco/soporteml-v3 | ARCHIVED |
| **ai-engineering-bootcamp** | gonzoblasco/ai-engineering-bootcamp | ARCHIVED — curso 10/10 completado |
| **hyatt-copilot-agent** | gonzoblasco/hyatt-copilot-agent | ARCHIVED |
| **ensulugar** | gonzoblasco/ensulugar | ARCHIVED |
| **cabala** | gonzoblasco/cabala | ARCHIVED |
| **health-tracker** | gonzoblasco/health-tracker | ARCHIVED |
| **umbrawriter** | gonzoblasco/umbrawriter | En Lovable, sin clon local |

## 🗑️ ELIMINADOS DEL DISCO (2026-08-23)

Carpetas locales sin repo en GitHub que se borraron de la mini. GitHub es la fuente de la verdad, así que no se mantienen clones huérfanos.

| Proyecto | Motivo |
|---|---|
| **brainweb** | Resto vacío (solo `supabase/`), sin repo. Borrado. |
| **recetario** | Solo una DB local (`recetario.db`), sin repo. Borrado. |
| **solitario** | Solo `node_modules` + `public`, sin repo. Borrado. |
| **soporteml-v2** | Resto vacío (solo `supabase/`), sin repo. Borrado. |
| **ultimo-turno** | Completamente vacía. Borrada y sacada de `.gitmodules`. |

## 🗑️ ELIMINADOS (histórico)

| Proyecto | Motivo |
|---|---|
| Moderno-Access-Virtual-Plate | Eliminado de GitHub |
| antigravity-developer-stack | Eliminado (contenido migrado a ai-developer-stack) |
| copilot-skills | Eliminado (reemplazado por workflow-kit) |
| futbol-ps2 | Eliminado (MVP completo, descartado) |
| chatgpt-project-architect | Archivado (absorbido por AGDS) |
| 0001 | Sin propósito |
| prueba_minecraft_claude_code | Experimento abandonado |
| umbrawriter (v1) | En Lovable, sin clon local. Reemplazado por umbrawriter-v2 |

---

## 📋 Notas

- **Forks de OSS** (create-t3-app, ui, ai, react-spectrum, material-ui, carbon, zod, etc.): NO se clonan a la mini. Se descargan solo cuando se necesitan para PRs. Viven en GitHub.
- Para agregar un proyecto: clonar en `projects/<slug>/`, crear `.knowledge/`, y agregar a la tabla de activos.
- Los proyectos en disco son submódulos del workspace (declarados en `.gitmodules`). Cada uno se sincroniza con su propio repo en GitHub.
