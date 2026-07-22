# DEFINITION — Pro Motors

> Definición del producto: MVP, arquitectura, features y posicionamiento.

## Stack definitivo

| Capa | Tecnología |
|------|-----------|
| **Frontend** | Next.js 15 (App Router) |
| **CMS** | Strapi (headless, Node.js) |
| **Backend** | Next.js API Routes + Supabase |
| **Base de datos** | Supabase (Postgres) |
| **IA** | Vercel AI SDK + OpenAI |
| **Auth** | Supabase Auth |
| **Storage** | Supabase Storage (imágenes de vehículos) |
| **Hosting** | Vercel (frontend + APIs) + Supabase (DB) + Railway (Strapi) |
| **Dominio** | pro-motors.com.ar (o subdominio nuevo) |

## MVP — Features esenciales

### 1. Home
- Hero con imágenes rotativas de las marcas
- Grid de marcas (KTM, Husqvarna, Can-Am, Sea-Doo, Ski-Doo, Segway)
- Vehículos destacados (desde Strapi)
- Sección "Sobre nosotros" (historia, 25 años, 2200m²)
- Blog reciente (últimos 3 posts)
- CTA a contacto y WhatsApp

### 2. Páginas de marca (x6)
- Identidad visual propia por marca (colores, tipografía)
- Listado de vehículos de esa marca
- Información de la marca (historia, valores)
- CTA a test drive / consulta

### 3. Catálogo de vehículos
- Grid con filtros: marca, tipo (moto, ATV, jet ski, nieve), precio, año
- Vista rápida desde el grid
- Paginación

### 4. Página de vehículo
- Galería de imágenes (Supabase Storage)
- Ficha técnica (desde Strapi)
- Precio y financiación
- Botón "Consultar" → WhatsApp o formulario
- Vehículos relacionados (IA o manual)

### 5. Integración Mercado Libre
- Sección "También en Mercado Libre"
- Sincronización automática de publicaciones activas vía API de ML
- Redirección a ML para comprar

### 6. Integración Tienda Nube
- Sección "Accesorios e indumentaria"
- Embed o sincronización de productos vía API de TN
- Redirección a TN para comprar

### 7. Blog
- Listado de posts (desde Strapi)
- Página de post individual
- Categorías

### 8. Contacto
- Formulario de contacto (→ Supabase + notificación)
- WhatsApp directo (ventas, postventa, repuestos)
- Mapa con ubicación (Vicente López)
- Horarios

### 9. Chat IA
- Flotante en todas las páginas
- Responde sobre: vehículos en stock, financiación, horarios, ubicación
- Entrena con datos de Strapi (vehículos, precios, disponibilidad)
- Escala a humano si no sabe responder

### 10. CMS (Strapi)
- Gestión de vehículos (marca, modelo, año, precio, fotos, ficha técnica)
- Gestión de páginas de marca
- Gestión de blog
- Gestión de contenido del home (hero, destacados)
- Usuarios: admin + vendedores (permisos limitados)

## Post-MVP

- Simulador de financiación
- Agenda de test drive online
- Multilenguaje (ES/EN/PT)
- Dashboard de analytics para vendedores
- Notificaciones de leads nuevos

## Posicionamiento

**Para** compradores de vehículos premium (motos, ATV, jet ski, motos de nieve) en Argentina  
**Que** buscan una experiencia de compra confiable y asesorada  
**Pro Motors** es el concesionario multi-marca con 25 años de trayectoria  
**A diferencia de** otros concesionarios con sitios genéricos  
**Nuestro producto** es un sitio web que refleja la calidad de las marcas que representamos, integra todos los canales de venta y usa IA para asesorar al comprador

## Arquitectura (alto nivel)

```
Usuario → Next.js (Vercel) → Strapi API (Railway)
                            → Supabase (DB + Auth + Storage)
                            → OpenAI API (chat IA)
                            → API ML (stock sincronizado)
                            → API TN (productos sincronizados)
```

---

*Creado: 2026-07-22*  
*Sesión: product-discovery — Fase 3 (Definición)*
