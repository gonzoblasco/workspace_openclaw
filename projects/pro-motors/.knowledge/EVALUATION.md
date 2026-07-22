# EVALUATION — Pro Motors

> Evaluación de mercado, competidores, viabilidad técnica y fit estratégico.

## Viabilidad Técnica

### Stack propuesto

| Capa | Tecnología | Justificación |
|------|-----------|---------------|
| **Frontend** | Next.js 15 (App Router) | SSR, SEO, rendimiento, React Server Components |
| **CMS** | WordPress headless (o Strapi) | Los vendedores manejan contenido sin tocar código. WP ya lo conocen. |
| **Backend** | Next.js API Routes + Supabase | Base de datos, auth, storage, RLS |
| **IA** | OpenAI API + Vercel AI SDK | Consultas sobre vehículos, recomendaciones, chat |
| **Hosting** | Vercel (frontend + APIs) + Supabase (DB) | Escalable, serverless, ~500 USD/mes |
| **Integraciones** | APIs de Mercado Libre + Tienda Nube | Sincronizar stock, precios, publicaciones |

### Riesgos técnicos

| Riesgo | Probabilidad | Mitigación |
|--------|-------------|------------|
| APIs de ML/TN cambian | Baja | Capa de abstracción, monitoreo |
| Vendedores no adoptan el CMS | Media | UI sencilla, capacitación mínima, soporte |
| Costo de IA se dispara | Baja | Rate limiting, caché de respuestas, presupuesto fijo |
| WordPress headless es overkill | Media | Evaluar Strapi o CMS más liviano como alternativa |

### Tiempo estimado

- **Fase 1 (Fundación):** Scaffold, CMS configurado, layout base, navegación — 2 sesiones
- **Fase 2 (Contenido):** Páginas de marcas, vehículos, blog, integración ML/TN — 3 sesiones
- **Fase 3 (IA):** Chat/consultas con IA, recomendaciones — 2 sesiones
- **Fase 4 (Polish):** SEO, performance, responsive, testing — 2 sesiones
- **Fase 5 (Deploy):** Dominio, hosting, certificados, presentación — 1 sesión

**Total estimado:** ~10 sesiones de trabajo enfocado.

## Mercado

### Sitios de referencia

- **KTM Argentina** — sitio oficial de la marca, buen diseño pero poco contenido local
- **Can-Am Argentina** — similar, falta personalización
- **Concesionarios multi-marca en USA/EU** — suelen tener mejor UX que los argentinos

### Oportunidad

En Argentina, los sitios de concesionarias multi-marca son en su mayoría templates WordPress genéricos. Un sitio custom con IA, integración de canales y diseño premium sería un diferenciador real.

## Competidores directos

| Competidor | Fortalezas | Debilidades |
|-----------|-----------|-------------|
| Pro Motors actual (WP) | Tiene contenido, marcas, blog | Template genérico, sin IA, sin integración |
| Otras concesionarias KTM/Can-Am | Presencia online | Misma plantilla, poco diferencial |

## Fit estratégico

✅ **Alineado con el perfil de Gonzo:** Fullstack React/TS, IA, Supabase, integraciones
✅ **Portfolio real:** Un sitio en producción para una empresa real vale más que cualquier demo
✅ **Diferenciador:** IA en concesionaria es algo que pocos hacen en Argentina
✅ **Regalo con costo operativo:** 500 USD/mes es viable para un concesionario de ese tamaño
⚠️ **Riesgo:** Depende de que el hermano acepte el costo mensual

## Decisión

**Veredicto:** ✅ GO — Proyecto viable, técnicamente factible, con valor real.

---

*Creado: 2026-07-22*  
*Sesión: product-discovery — Fase 2 (Evaluación)*
