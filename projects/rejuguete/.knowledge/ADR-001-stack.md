# ReJuguete — ADR-001: Stack y Arquitectura

## Contexto

Necesitamos una plataforma web para compra/venta de juguetes usados. Debe ser rápida de desarrollar, fácil de mantener, y visualmente atractiva para familias.

## Decisión

Usar Next.js 15 con App Router + TypeScript + Tailwind CSS como stack principal. Datos mockeados en v1, migración a SQLite cuando sea necesario.

## Razones

- Gonzo tiene 9 años de experiencia en React/TS — stack natural
- Next.js 15 da SSR, routing, API routes en un solo paquete
- Tailwind permite diseño custom rápido sin fricción
- Datos mockeados permiten iterar diseño sin backend
- Migrar a base de datos real después es straightforward

## Consecuencias

- Positivas: desarrollo rápido, cero infraestructura, deploy fácil
- Negativas: datos no persisten entre sesiones (v1)
- Mitigación: estructura de datos pensada para migración a DB

## Estado

Aceptado.
