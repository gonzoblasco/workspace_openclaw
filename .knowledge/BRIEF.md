# BRIEF: workspace_openclaw

## Qué es

El workspace de OpenClaw de Gonzo. Es su sistema operativo personal con IA: contiene la configuración del agente (AGENTS.md, SOUL.md, IDENTITY.md, USER.md), la memoria persistente (MEMORY.md, memory/), las skills operativas (skills/), el tooling de desarrollo (scripts/, tests/), y los proyectos activos (projects/).

## Por qué existe

Gonzo trabaja entre dos máquinas (Mac Mini y MacBook Air) y necesita un punto único de sincronización para todo su entorno de trabajo con IA. El workspace es el repositorio que orquesta skills, memoria, configuración del agente, y documentación de proyectos. No es un proyecto de código -  es la infraestructura de trabajo.

## Stack

- OpenClaw (gateway + agent runtime)
- Bash + Python (scripts de skills)
- bats + pytest (tests de scripts)
- Biome (linting de skills)
- Git + GitHub (sincronización entre máquinas)


## Estructura

```
~/.openclaw/workspace/
├── .knowledge/          ← Estado institucional del workspace
├── .github/            ← workflows CI (.github/skills/ eliminado 2026-09-28, ADR-079)
├── skills/              ← Skills operativas (~91)
│   ├── <skill>/
│   │   ├── SKILL.md
│   │   └── scripts/     ← Scripts auxiliares
├── scripts/             ← Tooling del workspace
│   ├── test-skills.sh
│   └── pre-commit.template
├── tests/               ← Tests de scripts
│   ├── bash/
│   └── python/
├── memory/              ← Diario personal, WAL, working buffer
├── projects/            ← Proyectos activos (cada uno con su repo)
│   └── <slug>/
│       └── .knowledge/  ← Estado del proyecto
├── AGENTS.md            ← Reglas de operación del agente
├── MEMORY.md            ← Memoria a largo plazo
├── SOUL.md              ← Personalidad
├── IDENTITY.md          ← Identidad
├── USER.md              ← Perfil de Gonzo
└── TOOLS.md             ← Notas locales del entorno
```

## Diferenciador

No es un dotfiles repo ni un monorepo de código. Es un **workspace de agente**: la configuración, memoria, skills y tooling que necesita un agente IA para operar como asistente personal full-stack. Cada proyecto tiene su propio repo; el workspace solo guarda la memoria institucional (`.knowledge/`) y la configuración global.

## Público

Gonzo (uso primario). El workspace es personal y privado.
