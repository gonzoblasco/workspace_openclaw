# ADR-028: Biome Toolchain

**Estado:** Aceptado
**Fecha:** 2026-08-05
**Actualizado:** 2026-10-15
**Decisores:** Gonzo / Kanam
**Origen:** workspace (generalizado desde libro "React 18 Design Patterns")

## Contexto

El libro dedica secciones extensas a configurar ESLint con múltiples plugins (eslint-config-airbnb, @typescript-eslint, eslint-plugin-import, eslint-plugin-jsx-a11y, eslint-plugin-react, eslint-plugin-prettier) + Prettier + husky para mantener consistencia de código.

Esta configuración tiene varios problemas:
- **Dependencias múltiples:** 6+ paquetes solo para linting + formateo
- **Configuración redundante:** .eslintrc + .prettierrc + .husky/ + .editorconfig
- **Rendimiento:** ESLint + Prettier combinados son lentos comparados con alternativas modernas
- **Fricción:** reglas que se contradicen entre ESLint y Prettier (eslint-config-prettier existe para apagar reglas conflictivas)

## Decisión

Usar **Biome** como toolchain unificado para formateo, linting, y organización de imports. Biome reemplaza ESLint + Prettier + eslint-plugin-import en un solo binario.

### Configuración recomendada

```json
// biome.json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": {
    "enabled": true
  },
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "semicolons": "asNeeded",
      "trailingCommas": "all",
      "arrowParentheses": "always"
    }
  }
}
```

### Pre-commit hook con simple-git-hooks

```json
// package.json
{
  "simple-git-hooks": {
    "pre-commit": "npx biome check --fix --unsafe . && npx vitest run"
  }
}
```

## Rationale

1. **Un solo binario** - instalar `@biomejs/biome` y ya. No más 6+ dependencias de ESLint + Prettier
2. **Zero-config para React/TS** - las reglas recomendadas de Biome cubren React, TypeScript, accesibilidad, y estilo
3. **Rendimiento** - Biome es ~20x más rápido que ESLint + Prettier combinados (escrito en Rust)
4. **Sin conflictos** - formateo y linting son el mismo engine, no hay reglas que se contradigan
5. **Organize imports** - Biome tiene `organizeImports` nativo, no necesita `eslint-plugin-import` ni `simple-import-sort`
6. **`--unsafe` fixes** - Biome puede aplicar fixes automáticos que van más allá de lo seguro, incluyendo agregar/eliminar paréntesis de arrow functions

## Consecuencias

- Menos dependencias en package.json
- Configuración más simple (un solo archivo `biome.json`)
- CI más rápido (un solo paso de lint + format)
- Sin fricción entre formatter y linter
- Migración desde ESLint + Prettier requiere conversión de reglas (Biome tiene guía de migración)

## Verificación en proyectos actuales
- Verificar adopción de Biome en proyectos activos

## Referencias

- Biome: https://biomejs.dev
- Biome vs ESLint + Prettier: https://biomejs.dev/guides/why-biome/
- Migración desde ESLint: https://biomejs.dev/guides/migrate-eslint-prettier/
- simple-git-hooks: https://github.com/toplenboren/simple-git-hooks