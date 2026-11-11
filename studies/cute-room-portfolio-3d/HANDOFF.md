# HANDOFF - Curso cute-room-portfolio-3d

**Fecha:** 2026-11-11 16:05 GMT-3
**Curso:** Create a Cute Room Portfolio with Blender, Three.js, JavaScript (Andrew Woan, 8:42:31)
**Fuente:** https://www.youtube.com/watch?v=tdsQwuyS6DQ

## Estado

- Clase montada y commiteada (`e90accbbac`): `transcripcion.md`, `outline.md`, `ADOPCION.md`, `video-meta.json`, `web-asset-gate.py`.
- Outline: 13 modulos alineados 1:1 con los 42 capitulos oficiales; 30 citas verificadas (script de barrido, `BAD: 0`).
- Adopcion: `web-asset-gate.py`, presupuesto de carga para assets 3D web. Corrido contra `projects/reinos-de-la-frontera` con dos presupuestos: exit 0 con 2 MB/2048px, exit 1 con 1 MB/768px. Hallazgo: `assets/quaternius/_download/` duplica 1,25 MB gzip de modelo y 677 KB de textura.

## Proximo bloque

- **Modulo 1** (vocabulario: tri/quad/n-gon) y **Modulo 8** (baking) son los dos de mayor rendimiento por tiempo invertido. El modulo 8 es el que justifica el curso completo.
- Si se sigue el curso de punta a punta: empezar por el modulo 2 (bloqueo + pared) para tener escena antes de modelar props.

## Pendientes

- Conversion PNG -> WebP en el pipeline web de `reinos-de-la-frontera`, cuando exista ese pipeline.
- Revisar si `assets/quaternius/_download/` se conserva o se retira (decision del proyecto, no de la clase).

## Lo que el curso no cubre

- Shader del toggle dia/noche (declarado por el autor en 0:01:40).
- Vapor del cafe.
- TypeScript, framework de UI, SEO, accesibilidad, dominio propio.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
