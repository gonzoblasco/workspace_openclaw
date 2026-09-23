# BRIEF - kanam-os

## Que es

App local para ver y gestionar la memoria de Kanam OS como **fichas, tablas y grafos**, en vez de por dialogo. `memory/memory.db` es la fuente de verdad; la app la lee.

## Problema que resuelve

Hoy la unica via de acceso a la memoria es el dialogo con Kanam o comandos sueltos (`memory-db.sh`). No hay forma de *ver* el sistema: que sesiones hay, que temas emergen, cuanta evidencia tiene cada learning, que quedo pendiente. Tampoco hay un lugar donde hacer cambios globales sin reconfigurar cada sesion.

## Alcance

- **Fase 1 (hecha):** lectura de todas las tablas con vistas propias + grafo de topics.
- **Fase 2:** CRUD por fichas, delegando toda escritura a los scripts de Python.
- **Fase 3:** bloques managed (settings en DB propagados a USER.md/AGENTS.md/.knowledge).
- **Fase 4:** busqueda semantica sobre los vectores ya persistidos.

## Decisiones tomadas

1. **Next.js + `node:sqlite`** en vez de Python en el back (2026-09-22). Un solo runtime; Node 26 lee SQLite nativo.
2. **`memory.db` sigue en git.** Quitar la DB del repo rompe la sincronizacion entre maquinas. El riesgo de bloat se mitiga leyendo en `readOnly` (no crea `-wal`/`-shm`), no sacando la DB.
3. **La UI nunca escribe SQL crudo.** Las acciones disparan los generadores de Python, que son el unico escritor.

## Limites

Los documentos narrativos (MEMORY.md, SOUL.md, AGENTS.md, USER.md) no se editan desde aca (ADR-038).
