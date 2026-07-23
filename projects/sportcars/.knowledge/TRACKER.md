# TRACKER — Sport Cars Jeep

## Cómo usar este documento

Este tracker acompaña el avance del proyecto. Cada tarea tiene:
- ID
- Fase
- Estado: `backlog` | `in_progress` | `blocked` | `review` | `done`
- Owner
- Bloqueos / notas

Se actualiza al finalizar cada sesión de trabajo.

## Leyenda

- 🟡 `backlog`
- 🔵 `in_progress`
- 🔴 `blocked`
- 🟣 `review`
- 🟢 `done`

## Fase 0 — Discovery

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| D0.1 | Relevar sitio actual y competencia | 🟢 done | Kanam | Sitio template compartido confirmado |
| D0.2 | Investigar Pilot CRM y API | 🟢 done | Kanam | Lead creation vía webhook confirmado |
| D0.3 | Investigar Mercado Libre API pública | 🟢 done | Kanam | `/sites/MLA/search?nickname=` funciona sin auth |
| D0.4 | Definir problema y propuesta de valor | 🟢 done | Kanam | "Sitio que trabaja para el vendedor" |
| D0.5 | Escribir BRIEF.md | 🟢 done | Kanam | |
| D0.6 | Escribir DEFINITION.md | 🟢 done | Kanam | Validado con respuestas de Gonzo |
| D0.7 | Escribir ARCHITECTURE.md | 🟢 done | Kanam | Stack definitivo y ADRs |
| D0.8 | Escribir DATA_MODEL.md | 🟢 done | Kanam | |
| D0.9 | Escribir OPENSPEC.md | 🟢 done | Kanam | |
| D0.10 | Escribir EVALUATION.md | 🟢 done | Kanam | Modo detallado |
| D0.11 | Escribir DESIGN.md | 🟢 done | Kanam | Modo detallado |
| D0.12 | Escribir ROADMAP.md | 🟢 done | Kanam | |
| D0.13 | Escribir ADRs | 🟢 done | Kanam | 5 ADRs iniciales |
| D0.14 | Escribir STATUS.md | 🟢 done | Kanam | |
| D0.15 | Go/No-Go meeting con Gonzo | 🟢 done | Gonzo | Validado stack y presupuesto 300 USD/mes |
| D0.16 | Obtener nickname/seller_id de MeLi | 🟡 backlog | Gonzo | Hermana lo puede conseguir fácil |
| D0.17 | Confirmar acceso a DNS de sportcarsjeep.com.ar | 🟡 backlog | Gonzo | Para reemplazo final |
| D0.18 | Confirmar guidelines de Stellantis | 🟡 backlog | Gonzo | A través de la hermana |

## Fase 1 — Scaffold

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| S1.1 | Crear repo en GitHub | 🟡 backlog | Gonzo | |
| S1.2 | Scaffold Next.js 15 + Tailwind + shadcn/ui | 🟡 backlog | Gonzo | Puede usar create-stack-next |
| S1.3 | Configurar Biome, git hooks, commit signing | 🟡 backlog | Gonzo | |
| S1.4 | Configurar Vercel project | 🟡 backlog | Gonzo | |
| S1.5 | Configurar Supabase project + schema | 🟡 backlog | Gonzo | |
| S1.6 | Configurar environment variables | 🟡 backlog | Gonzo | Secrets en Vercel |
| S1.7 | Setup `.knowledge/` doble git | 🟡 backlog | Gonzo | |
| S1.8 | Deploy inicial en preview | 🟡 backlog | Gonzo | |

## Fase 2 — Contenido estático y diseño base

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| C2.1 | Implementar layout + navegación + footer | 🟡 backlog | Gonzo | |
| C2.2 | Home page con hero, modelos destacados, CTAs | 🟡 backlog | Gonzo | |
| C2.3 | Página `/vehiculos` con catálogo 0km hardcodeado | 🟡 backlog | Gonzo | |
| C2.4 | Página `/sucursales` con 3 sucursales | 🟡 backlog | Gonzo | |
| C2.5 | Formulario de contacto básico | 🟡 backlog | Gonzo | |
| C2.6 | SEO base: meta tags, sitemap, robots | 🟡 backlog | Gonzo | |

## Fase 3 — Inventario Mercado Libre

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| M3.1 | Implementar servicio `lib/services/meli.ts` | 🟡 backlog | Gonzo | |
| M3.2 | API route `/api/meli/inventory` con cache | 🟡 backlog | Gonzo | |
| M3.3 | Página `/usados` con grid de listings | 🟡 backlog | Gonzo | |
| M3.4 | Página de detalle `/usados/[id]` | 🟡 backlog | Gonzo | |
| M3.5 | Sync job cada 30 min | 🟡 backlog | Gonzo | Vercel cron o revalidate |
| M3.6 | Fallback si MeLi falla | 🟡 backlog | Gonzo | |

## Fase 4 — Chatbot con RAG

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| B4.1 | Configurar Vercel AI SDK | 🟡 backlog | Gonzo | |
| B4.2 | Conectar proveedor LLM (Ollama/DeepSeek) | 🟡 backlog | Gonzo | |
| B4.3 | Crear knowledge base inicial | 🟡 backlog | Gonzo + Hermana | |
| B4.4 | Generar embeddings y guardar en Supabase | 🟡 backlog | Gonzo | |
| B4.5 | API route `/api/chat` con RAG + streaming | 🟡 backlog | Gonzo | |
| B4.6 | Widget de chat en frontend | 🟡 backlog | Gonzo | |
| B4.7 | Captura de datos del usuario en conversación | 🟡 backlog | Gonzo | |
| B4.8 | Derivación a WhatsApp | 🟡 backlog | Gonzo | |
| B4.9 | Persistir conversaciones en Supabase | 🟡 backlog | Gonzo | |

## Fase 5 — Leads, Test Drive y Cotizador

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| L5.1 | Tabla `leads` + API `/api/leads` | 🟡 backlog | Gonzo | |
| L5.2 | Formulario `/test-drive` | 🟡 backlog | Gonzo | |
| L5.3 | Formulario `/cotiza-tu-usado` | 🟡 backlog | Gonzo | |
| L5.4 | Panel simple `/admin/leads` | 🟡 backlog | Gonzo | |
| L5.5 | Notificación de leads por email/WhatsApp | 🟡 backlog | Gonzo | |
| L5.6 | Exportación a CSV | 🟡 backlog | Gonzo | |

## Fase 6 — QA e Integración

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| Q6.1 | End-to-end testing de flujos críticos | 🟡 backlog | Gonzo | |
| Q6.2 | Accesibilidad audit WCAG 2.1 AA | 🟡 backlog | Gonzo | |
| Q6.3 | Performance optimization | 🟡 backlog | Gonzo | |
| Q6.4 | SEO final y structured data | 🟡 backlog | Gonzo | |
| Q6.5 | Configurar dominio sportcarsjeep.com.ar | 🟡 backlog | Gonzo | Depende de DNS |
| Q6.6 | Redirects del sitio viejo | 🟡 backlog | Gonzo | |
| Q6.7 | Documentación de deploy y handoff | 🟡 backlog | Gonzo | |

## Fase 7 — Lanzamiento y Post-MVP

| ID | Tarea | Estado | Owner | Notas |
|---|---|---|---|---|
| P7.1 | Deploy a producción | 🟡 backlog | Gonzo | |
| P7.2 | Setup analytics | 🟡 backlog | Gonzo | |
| P7.3 | Capacitación a vendedores | 🟡 backlog | Gonzo + Hermana | |
| P7.4 | Monitoreo primeras 2 semanas | 🟡 backlog | Gonzo | |
| P7.5 | v1.1: Integración automática Pilot CRM | 🟡 backlog | Gonzo | Necesita credenciales admin |
| P7.6 | v1.1: Panel admin mejorado | 🟡 backlog | Gonzo | |
| P7.7 | v1.2: Simulador de financiación | 🟡 backlog | Gonzo | |
| P7.8 | v1.2: SEO local por sucursal | 🟡 backlog | Gonzo | |

## Métricas de seguimiento

| Métrica | Baseline | Target MVP | Frecuencia |
|---|---|---|---|
| Leads por semana | 0 (sitio actual) | 5-10 | Semanal |
| Tasa conversión visitas → lead | ? | > 2% | Mensual |
| Conversaciones chatbot / semana | 0 | 20-50 | Semanal |
| LCP | > 4s | < 2.5s | Por release |
| Costo infraestructura | - | < 300 USD/mes | Mensual |

## Notas y decisiones

- 2026-07-23: Presupuesto ajustado de 400 a 300 USD/mes. LLM cubierto por Ollama/DeepSeek propio de Gonzo.
- 2026-07-23: Pilot CRM diferido al Post-MVP por falta de acceso admin.
- 2026-07-23: Go/No-Go positivo. Listo para Fase 1.