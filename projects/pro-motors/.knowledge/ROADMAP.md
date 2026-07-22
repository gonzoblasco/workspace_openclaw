# ROADMAP — Pro Motors

> Plan de fases para el sitio de Pro Motors.

## Fase 1: Fundación
**Objetivo:** Proyecto funcionando, Strapi configurado, layout base.

- [ ] Scaffold Next.js 15 + TypeScript + Tailwind
- [ ] Configurar Biome, linting, testing
- [ ] Strapi: instalar, configurar content types (vehículos, marcas, blog, páginas)
- [ ] Strapi: seed de datos inicial (marcas, algunos vehículos)
- [ ] Layout base: header, footer, navegación, responsive
- [ ] Home: hero, marcas, destacados, sobre nosotros
- [ ] Conexión Next.js → Strapi (API)
- [ ] Conexión Next.js → Supabase (auth, DB)
- [ ] Deploy: Vercel + Railway (Strapi) + Supabase
- [ ] Dominio y SSL

## Fase 2: Catálogo y Contenido
**Objetivo:** Catálogo de vehículos funcionando, blog, páginas de marca.

- [ ] Páginas de marca (x6) con identidad visual
- [ ] Catálogo de vehículos con filtros
- [ ] Página de vehículo individual
- [ ] Galería de imágenes (Supabase Storage)
- [ ] Blog: listado + página individual
- [ ] Página de contacto con formulario
- [ ] Integración WhatsApp (ventas, postventa, repuestos)
- [ ] SEO básico (meta tags, sitemap, robots.txt)

## Fase 3: Integraciones
**Objetivo:** ML y Tienda Nube integrados, datos sincronizados.

- [ ] API Mercado Libre: autenticación, obtener publicaciones activas
- [ ] Sección "También en Mercado Libre" en el sitio
- [ ] API Tienda Nube: autenticación, obtener productos
- [ ] Sección "Accesorios e indumentaria"
- [ ] Sincronización periódica (cron o webhook)
- [ ] Manejo de errores y fallback si las APIs no responden

## Fase 4: IA
**Objetivo:** Chat IA funcionando, consultas sobre vehículos.

- [ ] Configurar Vercel AI SDK + OpenAI
- [ ] Chat flotante en todas las páginas
- [ ] Entrenar con datos de Strapi (vehículos, precios, disponibilidad)
- [ ] Sistema de escalado a humano
- [ ] Rate limiting y control de costos
- [ ] (Post-MVP) Recomendaciones IA

## Fase 5: Polish y Testing
**Objetivo:** Sitio listo para producción.

- [ ] Performance: Lighthouse ≥ 90
- [ ] Responsive: 320px a 1440px+
- [ ] Testing: unit (Vitest), integration (Testing Library)
- [ ] E2E: Playwright (flujos críticos)
- [ ] Accesibilidad: WCAG AA
- [ ] SEO: audit completo
- [ ] Seguridad: npm audit, secrets, CORS
- [ ] Cleanup: console.logs, imports muertos, TODOs

## Fase 6: Deploy y Presentación
**Objetivo:** Sitio en producción, presentado al hermano.

- [ ] Deploy final a Vercel (producción)
- [ ] DNS: pro-motors.com.ar apuntando al nuevo sitio
- [ ] Monitoreo post-deploy (24-48h)
- [ ] Preparar presentación para el hermano
- [ ] Documentación para vendedores (cómo usar Strapi)
- [ ] Entregar: "te regalo el sitio, solo pagás el hosting"

---

*Creado: 2026-07-22*  
*Sesión: product-discovery — Fase 3 (Definición)*
