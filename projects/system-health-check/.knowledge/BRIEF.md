# BRIEF - Project Overview

## What

CLI de diagnóstico y optimización de macOS. Corre una batería de tests de salud (disco, memoria, CPU, seguridad) y entrega un reporte con puntaje por categoría y sugerencias accionables.

## Why

Nace como mejora conceptual al sistema de limpieza/optimización de macOS visto en el stack de Breacorp (Moderno Tech Cleaner). En vez de copiar su app, se construye una herramienta propia, CLI-first, que audita la máquina y sugiere optimizaciones. Portfolio vivo: tomar la lección, hacerla propia.

## Stack

- Node.js + ESM (sin Electron - es un CLI, no una app de escritorio)
- Vitest para tests unitarios
- Técnica de `vm_stat` real de Activity Monitor para métricas de RAM (lección del stack de Breacorp)

## Status

- [x] Discovery
- [x] Definition
- [x] In Development
- [ ] Live
- [ ] Archived

## Key Decisions

- **CLI-first, no Electron** - el valor está en el diagnóstico rápido desde terminal, no en una UI de escritorio. Más simple, más testeable.
- **`vm_stat` real para RAM** - misma técnica que Activity Monitor (anonymous - purgeable = app memory), no aproximaciones.
- **Checks aislados** - un check que falla no tumba la batería; cada uno puntúa 0-100 y se pondera.
- **Sin acciones destructivas automáticas** - solo sugiere; borrar caches queda para una fase con confirmación explícita (regla: preguntar antes de destructivo).
