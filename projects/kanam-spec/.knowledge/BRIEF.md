# BRIEF - kanam-spec

## What

Aplicacion web que genera especificaciones tecnicas completas a partir de un brief corto, usando IA local (Ollama) y un catalogo de plantillas de secciones.

## Why

Escribir una spec tecnica desde cero cuesta horas y suele salir incompleta. Gonzo trabaja con specs, ADRs y OpenSpec en todos sus proyectos: la spec es el primer artefacto y el que mas se posterga. Esta app convierte un brief de 5 campos en un documento estructurado, editable y exportable, sin depender de proveedores cloud.

## Stack

- React 19 + TypeScript + Vite (web-first, sin SSR)
- Ollama local (`http://localhost:11434`) para generacion, con streaming
- Servidor Node sin dependencias para servir el build y proxear `/api` (evita CORS y funciona en produccion)
- Persistencia local en `localStorage` (local-first, sin backend propio)
- Sin dependencias de UI: CSS propio con variables, tema claro/oscuro

## Status

- [x] Discovery
- [x] Definition
- [x] In Development
- [ ] Live
- [ ] Archived

## Key Decisions

- **IA local en vez de API cloud** - el brief puede contener informacion de clientes; nada sale de la maquina.
- **Catalogo de secciones fijo en vez de generacion libre** - una spec completa tiene secciones previsibles (alcance, requisitos, arquitectura, datos, API, seguridad, testing, riesgos). El catalogo garantiza cobertura y permite regenerar una seccion sin tocar el resto.
- **Plantillas + IA, no solo IA** - cada seccion arranca de un esqueleto de headings; si el modelo falla, el esqueleto sigue siendo util y editable a mano.
- **Proxy local en vez de fetch directo al 11434** - la app se sirve y consume desde un solo origen: sin CORS, sin `OLLAMA_ORIGINS`, y el puerto de Ollama queda configurable por entorno.
- **Sin dependencias de UI** - el proyecto es de porte chico; una libreria de componentes no se justifica (regla: el precedente no es un motivo).
