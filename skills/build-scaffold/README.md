# Build & Scaffold

Scaffolding y construcción de proyectos desde cero.

## ¿Para qué sirve?

Para **arrancar un proyecto nuevo** con todo configurado y funcionando: TypeScript, Tailwind, Biome, testing, linting, CI/CD. También para **agregar CI/CD** a un proyecto existente o **iterar** sobre uno ya armado.

## ¿Cuándo usarlo?

- Cuando arrancás un proyecto nuevo
- Cuando querés estandarizar la configuración entre proyectos
- Cuando necesitás CI/CD y no lo tenés

## ¿Cómo se usa?

### Verificar que el scaffold está bien

```bash
./scripts/verify-scaffold.sh
```

Corre typecheck + lint + test + build. Modo `--fix` para auto-corregir.

### Configurar Biome con shadcn/ui

```bash
./scripts/setup-biome.sh --shadcn
```

Instala Biome, genera configuración óptima, agrega shadcn/ui al ignore, corre formato inicial.

### Inicializar git

```bash
./scripts/init-git.sh mi-proyecto
```

`git init` + `.gitignore` + `.knowledge/` + commit inicial. Opcionalmente con submodule.

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/stack-templates.md` | Templates de stack: Next.js + shadcn, Vite, Express, Supabase, Turborepo |
| `references/biome-setup.md` | Config óptima de Biome, shadcn ignore, VS Code, pre-commit |
| `references/ci-templates.md` | GitHub Actions para cada stack |

## Skills relacionadas

- [Task Execution](../task-execution) — Para implementar features post-scaffold
- [Technical Documentation](../tech-docs) — Para documentar decisiones de scaffolding
