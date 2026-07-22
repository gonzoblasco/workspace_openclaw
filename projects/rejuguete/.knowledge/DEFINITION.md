# ReJuguete — Definición Técnica

## Stack

- **Framework:** Next.js 15 (App Router)
- **Lenguaje:** TypeScript
- **Estilos:** Tailwind CSS
- **UI:** Componentes propios + Radix UI (Dialog, Select, Slider)
- **Iconos:** Lucide React
- **Utilidades:** class-variance-authority, clsx, tailwind-merge
- **Base de datos:** SQLite (via better-sqlite3 o Prisma + SQLite) — *decisión pendiente*
- **Auth:** Simplificada (nombre de vendedor + sesión local) — *v1 sin auth real*

## Estructura del proyecto

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── globals.css
│   ├── juguete/[id]/page.tsx
│   ├── publicar/page.tsx
│   └── vendedor/[id]/page.tsx
├── components/
│   ├── ui/           # Componentes base reutilizables
│   ├── Header.tsx
│   ├── Footer.tsx
│   ├── JugueteCard.tsx
│   ├── Filtros.tsx
│   └── SearchBar.tsx
├── lib/
│   ├── data.ts       # Datos mockeados (v1)
│   └── utils.ts
└── types/
    └── index.ts
```

## Diseño

- **Tono:** Colorido, infantil, cálido
- **Paleta:** Por definir (tonos pastel + acentos vibrantes)
- **Tipografía:** Sistema (Inter por defecto)
- **Responsive:** Mobile-first

## V1 Scope

### Incluido
- [x] Catálogo público con juguetes seed
- [x] Búsqueda y filtros (categoría, edad, precio)
- [x] Detalle de juguete
- [x] Publicar juguete (formulario)
- [x] Perfil de vendedor
- [x] Diseño colorido responsive

### Póstergado
- [ ] Auth real
- [ ] Base de datos persistente
- [ ] Pagos
- [ ] Chat / mensajería
- [ ] Imágenes reales (subida)
- [ ] Wishlist / favoritos
- [ ] Compartir por WhatsApp
