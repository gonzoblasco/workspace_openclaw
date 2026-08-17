# ADR-024 - CSS Modules con Vite (Zero-Config) como Estándar de Estilos Scoped

**Status:** Accepted
**Date:** 2026-08-05
**Source:** React 18 Design Patterns - Chapter 6 (CSS Modules section)
**Scope:** Global - aplica a cualquier proyecto React + Vite

## Context

El libro dedica ~30 páginas a configurar Webpack 5 + Babel + ts-loader + style-loader + css-loader + mini-css-extract-plugin + html-webpack-plugin + fork-ts-checker-webpack-plugin para usar CSS Modules con React.

Esta configuración era necesaria en 2020-2022. Hoy Vite provee CSS Modules out-of-the-box sin configuración.

## Decision

Usar **CSS Modules con Vite** como estándar para estilos scoped por componente. Vite detecta automáticamente archivos `*.module.css` y los trata como CSS Modules.

### Configuración

```ts
// vite.config.ts - zero-config para CSS Modules
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()]
})
```

### Uso

```tsx
// Button.module.css
.button {
  background-color: #ff0000;
  width: 320px;
  padding: 20px;
  border-radius: 5px;
  border: none;
  outline: none;
}

.button:hover {
  color: #fff;
}

@media (max-width: 480px) {
  .button {
    width: 160px;
  }
}
```

```tsx
// Button.tsx
import styles from './Button.module.css'

const Button = ({ children }: { children: React.ReactNode }) => (
  <button className={styles.button}>{children}</button>
)
```

### TypeScript declarations

```ts
// src/declarations.d.ts (o incluido en tsconfig)
declare module '*.module.css' {
  const classes: { readonly [key: string]: string }
  export default classes
}
```

## Rationale

1. **Zero-config:** Vite detecta `*.module.css` automáticamente. No requiere loaders, plugins, ni configuración extra.
2. **Scoping automático:** los class names se transforman en hashes únicos. No hay colisiones.
3. **CSS completo:** soporta pseudo-clases, media queries, animations, keyframes - todo lo que CSS Modules ofrece.
4. **Debugging en desarrollo:** Vite genera class names legibles (`button--hash`) sin configuración extra.
5. **Producción optimizada:** Vite extrae CSS a archivos separados, minifica, y cachea automáticamente.
6. **Composable con Tailwind:** CSS Modules y Tailwind se complementan - Tailwind para utility classes, CSS Modules para estilos scoped complejos.

## Consequence

- Elimina ~30 páginas de configuración de Webpack
- Proyectos nuevos arrancan con `npm create vite@latest` y ya tienen CSS Modules
- Cero dependencias extra para estilos scoped
- Para utility-first styling, agregar Tailwind CSS (sigue siendo compatible con CSS Modules)

## Referencias

- Vite - CSS Modules: https://vitejs.dev/guide/features.html#css-modules
- Vite - PostCSS: https://vitejs.dev/guide/features.html#postcss
- CSS Modules: https://github.com/css-modules/css-modules
- Tailwind CSS + Vite: https://tailwindcss.com/docs/guides/vite
