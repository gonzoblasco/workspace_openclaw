# ADR-054: Kanam OS como app local de lectura sobre `memory.db` (Next.js + node:sqlite)

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo - "quiero ver tu conocimiento y memoria de un modo distinto al dialogo: en tablas, fichas y graficos"
**Relacionado:** ADR-038 (learnings con mirror en DB), ADR-050 (la memoria sigue en SQLite local), ADR-011 (Next.js full-stack), ADR-047/048 (design system y UI)

---

## Contexto

El patron "DB como fuente de verdad + markdown espejo regenerable" ya esta aceptado y en produccion para `todos`, `inbox`, `learnings` y `contributions` (ADR-038), y ADR-050 cerro que la memoria sigue en SQLite local.

Lo que faltaba no era una decision de datos: era **una superficie**. La unica via de acceso a la memoria era el dialogo con Kanam o comandos sueltos de `memory-db.sh`. No habia forma de *ver* el sistema como conjunto - que sesiones existen, que temas emergen, que vinculos hay entre ellos - ni un lugar donde un cambio global se propague sin reconfigurar cada sesion.

Tres preguntas concretas de arquitectura quedaron abiertas:

1. **Python o Next en el back.** La asociacion "Python = cosas de IA" sugiere meter FastAPI para los embeddings.
2. **`memory.db` sigue en git o se vuelve local.** Gonzo fue explicito: sacarla del repo **rompe la sincronizacion entre maquinas** (ADR-050 la habia marcado como el umbral de higiene a vigilar).
3. **La UI puede escribir.** El destino es CRUD; el arranque es solo lectura.

### Volumen real (verificado 2026-09-22)

| Tabla | Filas |
|---|---|
| `daily_notes` | 114 (55 daily + 59 session) |
| `sessions_relacional` | 59 |
| `learnings` | 118 |
| `contributions` | 66 |
| `topics` | 11 |
| `todos` | 54 (2 abiertos) |
| `session_vectors` | 136 |

`memory.db`: 12,5 MB, trackeado en git (`.gitignore` linea 25: `!memory/memory.db`).

---

## Decision

**Se construye `kanam-os`: una app local Next.js que lee `memory.db` en modo read-only con `node:sqlite`, y delega toda escritura a los scripts de Python que ya existen.**

### Arquitectura

```
memory/memory.db  ──read-only──▶  kanam-os (Next.js 16, App Router)  ──▶  navegador
      ▲
      │ escribe (unico escritor)
  scripts/memory-db.sh · scripts/memory-end-session.py · scripts/memory-catalog-v2.py
```

| Capa | Tecnologia | Rol |
|---|---|---|
| UI + lectura | Next.js 16 (server components) + Tailwind 4 | Un solo runtime. Los server components son el "back". |
| Acceso a datos | `node:sqlite` (built-in de Node 26) | Read-only, cero dependencias, cero binarios extra. |
| Brain / escritura | Python (`scripts/*.py`) | Embeddings (Ollama), clustering de topics, generadores de markdown. |

### Las tres decisiones, y por que

**1. Next.js y NO Python en el back.** FastAPI agrega un segundo runtime, un segundo puerto y un bridge HTTP para leer un archivo SQLite que Node 26 ya lee nativo (`node:sqlite` es built-in). La parte "IA" no la necesita la UI: el vector **ya esta persistido** en `session_vectors` / `learnings_enriquecido`; la UI lo proyecta, no lo calcula. Python se queda donde ya funciona y no se reescribe.

**2. `memory.db` SE QUEDA en git.** Es la razon por la que la memoria viaja entre el Mac Mini y el MacBook Air. Sacarla del repo resolveria el bloat pero rompe la sincronizacion, que es el uso real. El riesgo tecnico concreto (que `-wal`/`-shm` ensucien el repo) **no aplica si la app abre read-only**: verificado - tras el build y las 9 vistas servidas, no aparecio ningun archivo `-wal`/`-shm`. Y `readOnly` evita el riesgo de que dos maquinas escriban el mismo binario a la vez.

**3. La UI nunca escribe SQL crudo.** La fase CRUD no agrega un escritor nuevo: agrega *botones que disparan los scripts existentes*. Un `UPDATE` directo desde la UI dejaria los markdown mintiendo respecto de la DB, que es exactamente el anti-patron que ADR-038 cerro.

### Por que `journal_mode=WAL` esta descartado

WAL mejora la concurrencia lector/escritor, pero crea `memory.db-wal` y `memory.db-shm` al lado del `.db`. Con la DB trackeada en git, eso son dos archivos binarios nuevos que aparecen y desaparecen en cada sesion. A esta escala (un proceso escritor, uno lector, 12,5 MB) el journal por defecto alcanza.

---

## Consecuencias

### Positivas
- **Ver el sistema, no consultarlo.** Fichas de sesion, grafo de topics, tablas de OSS/learnings/TODOs, daily navegable.
- **Cero infraestructura nueva:** sin Docker, sin Postgres, sin segundo server. `npm run dev` y listo.
- **Ningun escritor nuevo:** la invariante "la DB manda, los markdown se regeneran" queda intacta.
- **La DB sigue viajando:** el uso entre dos maquinas no se rompe.
- Consistencia con ADR-011 (Next.js como plataforma full-stack) sin forzar Supabase (ADR-012, que es para productos multi-usuario).

### Negativas
- **El repo git sigue con un binario de 12,5 MB que cambia por sesion.** Aceptado con los ojos abiertos: es el precio de sincronizar memoria entre maquinas. El umbral de ADR-050 queda vigente y este ADR no lo re-abre.
- **Un runtime mas en la maquina** (el server de Next mientras se usa la app). Se levanta on-demand, no como servicio permanente.
- **Riesgo de que la UI se convierta en un segundo escritor.** Mitigado por regla explicita: solo dispara scripts.

---

## Alternativas consideradas

1. **FastAPI (Python) + Next/React separados.** Dos runtimes, dos puertos, un bridge HTTP y dos lenguajes para leer el mismo archivo. El unico argumento era "Python es para IA", pero la IA ya dejo su resultado en la DB. Rechazado.
2. **Solo Python (Streamlit/Gradio).** Menos codigo, pero UI pobre para fichas/grafos y sin el design system de casa (ADR-047). El viewer no compite con una app: rechazado.
3. **Solo widget HTML en el dashboard del Control UI.** Las capabilities de un widget pinneado exigen origenes HTTPS; no puede leer una DB local. Sirve para reports nativos (como el OSS tracker, 2026-09-12), no para esto. Rechazado.
4. **Sacar `memory.db` de git y sincronizar la DB por otro medio** (iCloud/Syncthing/backup). Resuelve el bloat pero agrega un mecanismo de sync nuevo para reemplazar uno que ya funciona. Rechazado por decision explicita de Gonzo.
5. **Escribir SQL crudo desde la UI.** Rompe la invariante de ADR-038. Rechazado.

---

## Implementacion

| Pieza | Path |
|---|---|
| App | `projects/kanam-os/` |
| Conexion read-only | `lib/db.ts` (`new DatabaseSync(path, { readOnly: true })`) |
| Proyecciones por tabla | `lib/queries.ts` |
| Vistas | `app/{page,fichas,topics,learnings,todos,inbox,oss,daily}` |
| Grafo de topics | `components/TopicGraph.tsx` (SVG, sin dependencias) |
| Portal | `.openclaw/portals.json` (puerto 4317) |

**Fases:** 1 lectura (hecha) → 2 CRUD delegando a scripts → 3 bloques managed (settings en DB propagados a `USER.md`/`AGENTS.md`/`.knowledge/`) → 4 busqueda semantica sobre los vectores persistidos.

## Referencias

- ADR-038: "DB como fuente de verdad + markdown espejo regenerable" (patron que este ADR extiende a una UI)
- ADR-050: SQLite local y su umbral de migracion (vigente, no revisado)
- `docs/architecture/kanam-os-layers-evaluacion.md`
- Leccion 14/08: los documentos narrativos (MEMORY.md, SOUL.md, AGENTS.md) no se migran a DB - tampoco se editan desde esta app
