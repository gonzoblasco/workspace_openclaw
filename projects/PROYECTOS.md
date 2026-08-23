# PROYECTOS.md - Índice Maestro

**Última actualización:** 2026-08-23

> **Regla de oro:** GitHub es la fuente de la verdad. Cada proyecto vive en su propio repo (sin submódulos ni repos dentro del repo). El workspace (`~/.openclaw/workspace`) solo contiene config, memoria y skills. Los proyectos se clonan en `projects/<slug>/` cuando se necesitan, y el workspace trackea solo su `.knowledge/` (doble-git).

---

## 🟢 EN DISCO - Con `.knowledge/` trackeado en el workspace

Proyectos con actividad reciente, clonados localmente con su documentación institucional en `projects/<slug>/.knowledge/`.

| Proyecto | Descripción | Estado | Git |
|---|---|---|---|
| **kanam-story** | Co-writer de ficción local-first. Chat con manos + biblia viva + brújula + outline/beats. | **v0.17.0** - Fase A cerrada. 382 tests. Roadmap a la nube planificado. | ✅ gonzoblasco/kanam-story |
| **kanam-mind** | Segundo cerebro local-first con IA. Timeline personal + resumen IA diario. IndexedDB + Ollama local. | **v0.1.0** - MVP completo. 7 tests. | ✅ gonzoblasco/kanam-mind |
| **kanam-skills** | Skills de agente para todo el trabajo + web pública. | Activo. | ✅ gonzoblasco/kanam-skills |
| **kanam-forge** | Herramienta de forja de skills. Fork de Lovable (open source). | En discovery. | ✅ gonzoblasco/kanam-forge |
| **soporteml-v3** | CRM multi-tenant para ML sellers - backend sólido (OAuth MeLi, sync, IA, billing). | Conservado como activo valioso (repo archivado en GitHub, código en disco). | ✅ gonzoblasco/soporteml-v3 (ARCHIVED) |

---

## 🟢 ACTIVOS - Repos propios en GitHub (clonables bajo demanda)

Repos propios de Gonzo activos. Se clonan en `projects/<slug>/` solo cuando se trabaja en ellos.

| Repo | Descripción | Estado |
|---|---|---|
| **soporteml-v4** | CRM multi-tenant para ML sellers (reinicio con diseño avanzado). | Activo (PRIV). |
| **a11y-fixer** | Accessibility audit bot para PRs de GitHub. | En curso. |
| **kanam-solitaires** | Colección de solitarios PWA (Klondike, Spider, FreeCell, Pyramid). | **v1.0.0** - release público 2026-08-01. |
| **quedamos** | App PWA de matching para salidas. | Discovery completo (PRIV). |
| **create-stack** | Scaffolder opinado Next.js. | Publicado en npm. |
| **ai-developer-stack** | Skills de ingeniería con IA. | Activo. |
| **create-with-ai** | Generador de apps con IA. | Activo (PRIV). |
| **accessible-ui** | Headless component library accesible. | Activo (PRIV). |
| **soporteml** | CRM multi-tenant para sellers (v1). | Activo. |

---

## ❄️ ARCHIVADOS (en GitHub, sin clon local)

Proyectos que existen en GitHub pero no se clonan. Se descargan solo si se reactivan.

| Proyecto | GitHub | Estado |
|---|---|---|
| **soporteml-v3** | gonzoblasco/soporteml-v3 | ARCHIVED (pero código conservado en disco - ver arriba) |
| **ai-engineering-bootcamp** | gonzoblasco/ai-engineering-bootcamp | ARCHIVED - curso 10/10 completado |
| **hyatt-copilot-agent** | gonzoblasco/hyatt-copilot-agent | ARCHIVED |
| **ensulugar** | gonzoblasco/ensulugar | ARCHIVED |
| **cabala** | gonzoblasco/cabala | ARCHIVED |
| **health-tracker** | gonzoblasco/health-tracker | ARCHIVED |
| **umbrawriter** | gonzoblasco/umbrawriter | ARCHIVED (PRIV) |

---

## 🗑️ ELIMINADOS

### Del disco (2026-08-23)

Carpetas locales sin repo en GitHub que se borraron de la mini. GitHub es la fuente de la verdad, así que no se mantienen clones huérfanos.

| Proyecto | Motivo |
|---|---|
| **brainweb** | Resto vacío (solo `supabase/`), sin repo. Borrado. |
| **recetario** | Solo una DB local (`recetario.db`), sin repo. Borrado. |
| **solitario** | Solo `node_modules` + `public`, sin repo. Borrado. |
| **soporteml-v2** | Resto vacío (solo `supabase/`), sin repo. Borrado. |
| **ultimo-turno** | Completamente vacía. Borrada y sacada de `.gitmodules`. |

### Histórico (de GitHub)

| Proyecto | Motivo |
|---|---|
| Moderno-Access-Virtual-Plate | Eliminado de GitHub |
| antigravity-developer-stack | Eliminado (contenido migrado a ai-developer-stack) |
| copilot-skills | Eliminado (reemplazado por workflow-kit) |
| futbol-ps2 | Eliminado (MVP completo, descartado) |
| chatgpt-project-architect | Archivado (absorbido por AGDS) |
| 0001 | Sin propósito |
| prueba_minecraft_claude_code | Experimento abandonado |
| umbrawriter (v1) | Reemplazado por umbrawriter-v2 (Lovable) |

---

## 📋 Notas

- **Forks de OSS** (create-t3-app, ui, ai, react-spectrum, material-ui, carbon, zod, astryx, radix, TanStack, etc.): NO se clonan a la mini. Se descargan solo cuando se necesitan para PRs. Viven en GitHub.
- **Estructura doble-git:** el workspace trackea solo `projects/<slug>/.knowledge/` + README. El código vive en el repo propio de cada proyecto. Sin submódulos.
- Para agregar un proyecto: clonar en `projects/<slug>/`, crear `.knowledge/`, y agregar a la tabla correspondiente.
