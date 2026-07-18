# BRIEF — Accessible UI

> Phase 0 — Idea Intake
> Fecha: 2026-07-16

## Raw Idea

Librería de componentes React headless, 100% accesibles. Diseño básico pero accesibilidad garantizada. Inspirada en Radix UI pero con foco exclusivo en accesibilidad WCAG 2.2.

## Estado actual

- Portfolio vivo — muestra capacidad en accesibilidad
- Componentes headless con Storybook + jest-axe
- Stack: React 19 + Vite + Storybook + jest-axe
- Repo: github.com/gonzoblasco/accessible-ui

## Contexto

- Complementa accessibility-auditor como ecosistema de accesibilidad
- Pensado inicialmente como "por tag" (componentes individuales) pero sin bloqueo en esa decisión
- Podría evolucionar a librería publicada en npm

## Preguntas a resolver

1. ¿Publicar en npm como librería independiente?
2. ¿Modelo headless puro o con estilos básicos?
3. ¿Integrarse con create-stack-next como template opcional?
