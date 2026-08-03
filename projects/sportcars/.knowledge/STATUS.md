# STATUS — Sport Cars Jeep

## Estado actual
Rediseño completo del sitio web implementado y verificado con build exitoso. El sitio fue evaluado visualmente y considerado **listo para deploy/preview**.

## Qué se hizo en este ciclo
- Paleta visual premium dark mode ajustada: fondo `#1A1A1A`, superficies `#2A2A2A`, acento naranja `#D97706`.
- Sistema de feature flags portable implementado (`showPrices` como primera flag) con persistencia en localStorage.
- Home rediseñada: hero con imagen de fondo, grid de modelos Jeep con fotos reales, sección de usados, diferenciadores, sucursales, CTA final.
- Catálogo `/vehiculos` rediseñado con filtros, búsqueda, grid de modelos (Jeep + Ram 1500) con imágenes reales y CTAs consistentes.
- Detalle de vehículo `/vehiculos/[slug]` adaptado a la nueva paleta.
- Páginas de usados, sucursales, contacto, test drive y cotiza-tu-usado rediseñadas.
- Header, footer, chat widget y panel de admin adaptados.
- Imágenes reales de vehículos descargadas desde Wikimedia Commons (CC-BY-SA) para Compass, Renegade, Commander, Gladiator, Grand Cherokee, Wrangler y Ram 1500.
- Build exitoso: `npx next build` sin errores.

## Screenshots actuales
- `sc_home_v9.png` — home final
- `sc_catalog_v9.png` — catálogo final

## Bloqueos resueltos
- Imágenes: se obtuvieron fotos reales de Wikimedia Commons (assets oficiales requieren acceso a Stellantis Media).
- Contraste bajo: corregido en navegación, badges, CTAs y footer.
- Inconsistencia de color: logo e iconos ahora usan el acento naranja consistentemente.

## Tareas pendientes críticas antes del lanzamiento real
1. Deploy a Vercel (`sportcars-pi.vercel.app` o dominio propio).
2. Reemplazar imágenes de Wikimedia Commons por fotos oficiales de Stellantis/Jeep Argentina o fotos propias del concesionario.
3. Configurar Supabase cloud (actualmente local).
4. Configurar LLM del chatbot para producción.
5. Obtener nickname/seller_id de Mercado Libre de Sport Cars para sync real de usados.
6. Validar Lighthouse: performance, accesibilidad, SEO, best practices.
7. Feature flags: extraer a lib portable en `workflow-kit` (`@workflow-kit/feature-flags`) ✅ — creado `@kanam/feature-flags` e integrado en Sport Cars via alias de webpack (publicar a npm para eliminar alias).

## Próximo hito
Deploy a preview en Vercel para validación en vivo.

## Última actualización
2026-08-02
