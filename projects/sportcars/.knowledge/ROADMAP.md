# ROADMAP — Sport Cars Jeep

## Visión
Lanzar en 4-6 semanas un MVP que reemplace sportcarsjeep.com.ar y empiece a generar leads digitales para el concesionario. Luego iterar para integrar Pilot CRM y agregar funcionalidades comerciales.

## Fases

### Fase 0 — Discovery (en curso)
**Duración:** 1-2 semanas
**Estado:** 0.1 completado, 0.2 en progreso

**Entregables:**
- [x] BRIEF.md
- [x] DEFINITION.md
- [x] ARCHITECTURE.md
- [x] DATA_MODEL.md
- [x] OPENSPEC.md
- [x] ADRs (5 iniciales)
- [ ] Go/No-Go meeting con Gonzo
- [ ] Obtener nickname/seller_id de MeLi de Sport Cars
- [ ] Confirmar acceso al dominio sportcarsjeep.com.ar

### Fase 1 — Scaffold & Setup (1 semana)
**Objetivo:** Proyecto base listo para desarrollar.

**Epics/tasks:**
- E1.1 Crear repo del proyecto en GitHub
- E1.2 Configurar `create-stack-next` o scaffold manual con Next.js 15 + Tailwind + shadcn
- E1.3 Configurar Biome, git hooks, commit signing
- E1.4 Crear proyecto en Supabase + tablas iniciales (leads, conversations, messages, knowledge_chunks, vehicles, events)
- E1.5 Configurar Vercel project + environment variables
- E1.6 Setup de `.knowledge/` doble git (workspace + repo del proyecto)
- E1.7 Diseño base: colores, tipografía, componentes iniciales

**Definition of Done:**
- `npm run dev` funciona
- CI básico pasa (lint + typecheck)
- Supabase schema creado
- Deploy en preview de Vercel exitoso

### Fase 2 — Contenido estático & Diseño (1 semana)
**Objetivo:** Sitio navegable con contenido del concesionario.

**Epics/tasks:**
- E2.1 Home page con hero, modelos destacados, CTA
- E2.2 Página `/vehiculos` con catálogo 0km (hardcode inicial)
- E2.3 Página `/sucursales` con 3 ubicaciones
- E2.4 Componente de navegación y footer
- E2.5 Formulario de contacto básico
- E2.6 SEO base: meta tags, sitemap, robots.txt

**Definition of Done:**
- Navegación completa sin errores
- Responsive en mobile y desktop
- Lighthouse score > 80 en performance y accesibilidad

### Fase 3 — Inventario Mercado Libre (1 semana)
**Objetivo:** Usados reales sincronizados desde MeLi.

**Epics/tasks:**
- E3.1 Implementar servicio `lib/services/meli.ts`
- E3.2 API route `/api/meli/inventory` con cache
- E3.3 Página `/usados` con grid de listings
- E3.4 Página de detalle `/usados/[id]`
- E3.5 Sync job (cron o revalidate) cada 30 min
- E3.6 Fallback si MeLi falla

**Definition of Done:**
- `/usados` muestra publicaciones reales de Sport Cars
- Cache funciona
- Detalle de cada auto renderiza correctamente

### Fase 4 — Chatbot con RAG (1-2 semanas)
**Objetivo:** Bot conversacional funcional.

**Epics/tasks:**
- E4.1 Configurar Vercel AI SDK + proveedor LLM
- E4.2 Crear knowledge base inicial (modelos, precios, FAQs, sucursales)
- E4.3 Generar embeddings y guardar en Supabase
- E4.4 API route `/api/chat` con RAG + streaming
- E4.5 Widget de chat en frontend
- E4.6 Captura de nombre/teléfono durante conversación
- E4.7 Derivación a WhatsApp
- E4.8 Persistir conversaciones en Supabase

**Definition of Done:**
- El bot responde preguntas básicas correctamente
- Captura datos y genera lead
- Derivación a WhatsApp funciona
- Costo de prueba < 10 USD

### Fase 5 — Leads, Test Drive y Cotizador (1 semana)
**Objetivo:** Convertir tráfico en contactos accionables.

**Epics/tasks:**
- E5.1 Tabla `leads` + API `/api/leads`
- E5.2 Formulario `/test-drive`
- E5.3 Formulario `/cotiza-tu-usado`
- E5.4 Panel simple `/admin/leads` protegido
- E5.5 Notificación de leads por email/WhatsApp
- E5.6 Exportación a CSV

**Definition of Done:**
- Cada formulario genera un lead en Supabase
- Vendedor recibe notificación
- Panel permite ver y exportar leads

### Fase 6 — Integración y QA (1 semana)
**Objetivo:** Todo funciona junto y listo para producción.

**Epics/tasks:**
- E6.1 End-to-end testing de flujos críticos
- E6.2 Accesibilidad audit (WCAG 2.1 AA)
- E6.3 Performance optimization (images, fonts, caching)
- E6.4 SEO final (structured data, sitemap)
- E6.5 Configurar dominio sportcarsjeep.com.ar en Vercel
- E6.6 Redirects del sitio viejo
- E6.7 Documentación de deploy y handoff

**Definition of Done:**
- 0 bugs críticos
- Lighthouse > 90
- Dominio apunta al nuevo sitio

### Fase 7 — Lanzamiento + Post-MVP
**Objetivo:** Publicar, medir e iterar.

**Epics/tasks:**
- E7.1 Deploy a producción
- E7.2 Setup analytics (Vercel + Plausible/PostHog)
- E7.3 Capacitación a la hermana/vendedores
- E7.4 Primeras 2 semanas de monitoreo
- E7.5 Plan v1.1: Integración Pilot CRM automática
- E7.6 Plan v1.2: Financiación, WhatsApp Business API, SEO local

**Definition of Done:**
- Sitio online
- Leads entrando
- Roadmap v1.1 definido

## Estimación total

- **Fase 1:** 1 semana
- **Fase 2:** 1 semana
- **Fase 3:** 1 semana
- **Fase 4:** 1-2 semanas
- **Fase 5:** 1 semana
- **Fase 6:** 1 semana
- **Total MVP:** **6-7 semanas** (tiempo parcial de Gonzo)

## Riesgos y dependencias

1. **Obtener seller_id/nickname de MeLi** — Bloquea Fase 3
2. **Acceso al DNS de sportcarsjeep.com.ar** — Bloquea Fase 6
3. **Proveedor LLM y costo** — Bloquea parcialmente Fase 4
4. **Contenido de knowledge base** — Depende de input de la hermana/vendedores
5. **Guidelines de Stellantis** — Puede afectar diseño; a confirmar

## Métricas de seguimiento

- Leads por semana
- Conversaciones de chatbot por semana
- Tasa de conversión (visitas → lead)
- Tiempo de carga (LCP)
- Costo de infraestructura vs. presupuesto de 400 USD

## Notas

- Las fechas son estimaciones. Gonzo maneja el ritmo.
- Si alguna dependencia externa se resuelve antes, se puede adelantar la integración correspondiente.
- La Fase 4 (chatbot) es la más incierta en esfuerzo; recomendamos hacer un spike técnico de 1 día antes de comprometer 2 semanas.