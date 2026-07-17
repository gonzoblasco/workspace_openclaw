---
name: "scaffold-verify"
description: "Verificar que un proyecto generado por scaffold compila: typecheck, test, build."
author: "Gonzo"
created: "2026-07-16"
---

# scaffold-verify

## Overview

No alcanza con que el CLI del scaffold funcione — hay que probar que el proyecto **generado** realmente compile, pase los tests y se pueda buildear. Esta skill captura el proceso de verificación post-generación.

El problema clásico: el scaffold genera archivos con TypeScript moderno (ESM, `allowImportingTsExtensions`, JSX), pero el `tsconfig.json` generado no está sincronizado, o el build script usa `tsc -b` que es incompatible con ciertas configuraciones, o los imports tienen extensión incorrecta (`.js` vs `.tsx`). Todo esto se detecta corriendo typecheck, test y build sobre el proyecto generado, no sobre el scaffold en sí.

## Prerrequisitos

- El proyecto generado debe existir en disco (producto del scaffold)
- Node.js >= 18 instalado
- El package manager del proyecto (npm, pnpm, yarn, bun) disponible

## Flujo

### 1. `cd` al proyecto generado

```bash
cd /ruta/al/proyecto/generado
```

### 2. Instalar dependencias

```bash
npm install
# o: pnpm install / yarn install / bun install
```

Si hay errores de instalación, revisar:
- `package.json` mal formado
- Versiones de dependencias incompatibles
- Falta de `packageManager` field si usa pnpm/yarn

### 3. Typecheck

```bash
npm run typecheck
# o: npx tsc --noEmit
```

**Problemas comunes:**
- `tsconfig.json` incompleto: falta `allowImportingTsExtensions`, `types`, `moduleResolution: "bundler"`, `jsx: "react-jsx"`
- Imports con extensión incorrecta: el scaffold genera `import Foo from './Foo.tsx'` pero el tsconfig espera `.js`
- Módulos ESM mezclados con CommonJS en el mismo proyecto
- `paths` o `baseUrl` mal configurados

### 4. Tests

```bash
npm test
# o: npx vitest run / npx jest
```

**Problemas comunes:**
- Test runner no configurado en `package.json`
- Dependencias de test faltantes (vitest, jest, @testing-library)
- Tests que importan archivos con extensión incorrecta
- Setup files faltantes

### 5. Build

```bash
npm run build
```

**Problemas comunes:**
- Build script incorrecto: `tsc -b` es incompatible con `allowImportingTsExtensions` (tsc -b no soporta esta flag correctamente)
- El build espera un entry point que no existe
- El output dir no está configurado o no se crea
- Dependencias de build faltantes (typescript, esbuild, vite)

### 6. Diagnóstico y fix

Si algo falla, diagnosticar en este orden:

1. **tsconfig.json** — ¿tiene `allowImportingTsExtensions: true`? ¿`moduleResolution: "bundler"`? ¿`types` correctos?
2. **Build script** — ¿usa `tsc -b`? Cambiar a `tsc` simple o a `vite build`/`esbuild` según corresponda
3. **Imports** — ¿los archivos generados importan con `.tsx`/`.ts` en vez de `.js`? El scaffold debe generar imports con la extensión que el tsconfig espera
4. **Dependencias** — ¿faltan paquetes en `dependencies` o `devDependencies`?

**Regla crítica:** los fixes van al **scaffold**, no al proyecto generado. Si el proyecto generado tiene un error, el fix es modificar el template/script que lo genera, no parchear el output.

## Ejemplo real

El scaffold de `create-with-ai` generaba un proyecto que fallaba en typecheck y build. Los fixes fueron al `scaffold/index.ts`:

- Se agregó `allowImportingTsExtensions: true` al tsconfig template
- Se cambió el build script de `tsc -b` a `tsc` simple
- Se corrigieron los imports generados para usar extensión `.js` en vez de `.tsx`
- Se agregaron `@types/react` y `@types/react-dom` a devDependencies

## Output

```
📦 Instalación: ✅
🔍 Typecheck:    ✅
🧪 Tests:        ✅
📦 Build:        ✅
```

O en caso de error:

```
📦 Instalación: ✅
🔍 Typecheck:    ❌ — allowImportingTsExtensions faltante en tsconfig.json
🧪 Tests:        ⏭️  (saltado por error anterior)
📦 Build:        ⏭️  (saltado por error anterior)

🔧 Fix aplicado: agregar allowImportingTsExtensions: true al tsconfig template en scaffold/index.ts
```

## Notas

- Si el proyecto generado usa un framework (Next.js, Astro, etc.), usar los comandos específicos del framework (`next build`, `astro build`)
- No asumir que `npm test` existe — verificar en `package.json` primero
- Si no hay tests, reportar como "no tests configured" en vez de fallar
- El orden importa: typecheck antes de test, test antes de build. Si typecheck falla, no tiene sentido correr tests
