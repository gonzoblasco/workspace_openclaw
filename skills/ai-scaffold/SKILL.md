---
name: "ai-scaffold"
description: "Usar create-with-ai para analizar una idea y generar un proyecto completo con IA."
author: "Gonzo Blasco"
created: "2026-07-16"
---

# AI Scaffold — create-with-ai

## Overview

**create-with-ai** es un CLI que escucha en lenguaje natural, analiza con IA (BYOK — Bring Your Own Key), y genera proyectos **React + Supabase** completos y funcionales.

En lugar de arrancar con un template vacío, describís tu idea en lenguaje natural y el sistema la analiza, diseña la arquitectura, genera el código, y te entrega un proyecto que ya compila, pasa typecheck, tests y build.

## Prerrequisitos

- **Node.js 20+** (recomendado 22+)
- **npm** (viene con Node.js)
- **API key de IA** (opcional — si no se provee, el wizard guía con opciones gratuitas/de prueba)
- **Git** (opcional, para versionar el proyecto generado)

## Flujo principal — Proyecto nuevo

### Paso 1: Ejecutar el CLI

```bash
npx @gonzoblasco/create-with-ai
```

> Sin flags. Solo ejecutalo y seguí el wizard interactivo.

### Paso 2: Describir el proyecto en lenguaje natural

El CLI abre un prompt interactivo. Escribí tu idea con tanto detalle como quieras. Ejemplos:

- *"Una app de hábitos diarios con rachas, recordatorios push y estadísticas semanales"*
- *"Un dashboard para un SaaS de facturación con autenticación, roles (admin/usuario), y gráficos de ingresos mensuales"*
- *"Un clon minimalista de Trello con tableros, columnas, tarjetas drag & drop y compartir por link"*

### Paso 3: Elegir nombre y stack

El wizard te pedirá:
- **Nombre del proyecto** (slug, ej: `habit-tracker`)
- **Stack confirmado** (React + Vite + TS + Tailwind v4 + shadcn/ui + Supabase + React Router 7 + TanStack Query 5 + Biome + Vitest + CI)

### Paso 4: Configurar API key

Si no configuraste una API key antes, el wizard te guiará para:
1. Elegir provider (OpenAI, Anthropic, DeepSeek, Ollama Cloud)
2. Ingresar la key (o configurar URL custom para Ollama Cloud)
3. La key se guarda localmente para usos futuros

> **BYOK**: create-with-ai no tiene backend propio. Las llamadas van directo de tu máquina al provider que elijas.

### Paso 5: Generación del proyecto

El sistema:
1. Analiza tu descripción con IA
2. Diseña esquema de base de datos (SQL de migración)
3. Genera estructura de carpetas y componentes
4. Configura autenticación, routing, queries
5. Corre `typecheck`, `test` y `build` automáticamente

### Paso 6: Usar el proyecto

```bash
cd <nombre-del-proyecto>
npm install
npm run dev
```

El proyecto ya es funcional. No requiere configuración manual adicional.

## Modo iteración — `--iterate`

Para modificar un proyecto ya generado sin perder cambios existentes.

### Paso 1: Ejecutar con flag de iteración

```bash
npx @gonzoblasco/create-with-ai --iterate
```

### Paso 2: Indicar ruta del proyecto existente

El wizard te pedirá la ruta al proyecto que querés modificar (por defecto, el directorio actual).

### Paso 3: Describir el cambio

Describí en lenguaje natural qué querés agregar, modificar o eliminar. Ejemplos:

- *"Agregar un campo 'categoría' a las tareas con filtro por categoría"*
- *"Cambiar el tema de colores a modo oscuro con acento verde"*
- *"Agregar una tabla de auditoría que registre cada cambio en los hábitos"*

### Paso 4: El sistema aplica los cambios

- Genera migraciones SQL incrementales
- Actualiza componentes, rutas y queries
- Corre validaciones automáticas
- Preserva el código existente que no tocaste

## Providers soportados

| Provider | API Key | Notas |
|----------|---------|-------|
| **OpenAI** | `OPENAI_API_KEY` | Modelo: gpt-4o por defecto |
| **Anthropic** | `ANTHROPIC_API_KEY` | Modelo: claude-sonnet-4-20250514 |
| **DeepSeek** | `DEEPSEEK_API_KEY` | Modelo: deepseek-chat |
| **Ollama Cloud** | URL custom | Usa cualquier endpoint compatible con OpenAI API |

## Output

El proyecto generado es **funcional de entrada**:

- ✅ **typecheck** — Biome type-check sin errores
- ✅ **test** — Vitest con tests pasando
- ✅ **build** — Build de producción exitoso
- ✅ **CI** — Workflow de GitHub Actions incluido

## Stack generado

| Capa | Tecnología |
|------|-----------|
| Framework | React 19 |
| Bundler | Vite |
| Lenguaje | TypeScript 5 |
| Estilos | Tailwind CSS v4 |
| Componentes | shadcn/ui (Radix primitives) |
| Backend | Supabase (PostgreSQL, Auth, Storage, Realtime) |
| Routing | React Router 7 |
| Data fetching | TanStack Query 5 |
| Linter/Formatter | Biome |
| Testing | Vitest + Testing Library |
| CI/CD | GitHub Actions |

## Ejemplo rápido

```bash
# 1. Crear proyecto
npx @gonzoblasco/create-with-ai

# 2. Describir: "Un gestor de tareas con prioridades, fechas límite y colaboración en equipo"

# 3. Elegir nombre: taskflow

# 4. Esperar generación...

# 5. Usar
cd taskflow
npm run dev
```

## Notas

- create-with-ai **no almacena** tu descripción ni el código generado en ningún servidor externo
- Todo el procesamiento de IA ocurre entre tu máquina y el provider que elijas
- El proyecto generado es 100% tuyo — sin lock-in, sin branding oculto
- Para contribuir o reportar issues: https://github.com/gonzoblasco/create-with-ai
