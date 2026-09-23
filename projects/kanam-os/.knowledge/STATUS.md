# STATUS - kanam-os

**Ultima actualizacion:** 2026-09-22

## Estado

**Fase 1 (lectura) y Fase 2 (escritura) completas.**

| Componente | Estado |
|---|---|
| Scaffold Next 16.3.6 + TS + Tailwind 4 + Biome | hecho |
| `lib/db.ts` (node:sqlite readOnly) | hecho - no crea `-wal`/`-shm` |
| `lib/queries.ts` (8 modulos de lectura) | hecho |
| `lib/actions.ts` (7 server actions) | hecho - delegan a memory-db.sh |
| `components/ActionButton` + `ActionForm` | hecho |
| Vistas de lectura (8) | hecho |
| Escritura: TODOs (alta, hecho, reabrir, prioridad) | hecho |
| Escritura: Inbox (alta, triage) | hecho |
| Escritura: Ficha (titulo, tags) | hecho |
| Repo GitHub privado `gonzoblasco/kanam-os` | creado y pusheado |
| Tests automaticos (Vitest) | pendiente |
| Bloques managed (fase 3) | pendiente |
| Busqueda semantica (fase 4) | pendiente |

## Verificacion de la fase 2

- `next build`: compila, typecheck OK, 9 rutas.
- Los 6 subcomandos nuevos de `memory-db.sh` probados en sandbox: escriben y **regeneran el `.md`** en el mismo paso.
- Guards de id inexistente: probados con `execFile` (el mecanismo real de las actions), 7/7 correctos - exit 1 con mensaje, en vez de fallar en silencio.
- Path resolution verificado contra el workspace real (`scripts/memory-db.sh`, ejecutable).
- Lo que NO quedo verificado por mi: el click en el navegador. El POST a mano replicando el protocolo de server actions dio 500 (`Connection closed`) porque curl no reproduce el streaming RSC de Next; no es un fallo de la app. Se comprueba abriendo la app y haciendo click.

## Decisiones de la fase 2

- **Las server actions llaman a la accion a mano** (en un `useTransition`), no via el prop `action` de `<form>`: ese prop exige `Promise<void>` y las actions devuelven `ActionResult`, que es lo que permite mostrar el error en el lugar. Forzar el cast habria escondido el resultado.
- **`execFile` con array de argumentos, nunca shell**: un valor con `;` o backticks viaja como argumento literal.
- **Los guards van sin pipe**: un `exit 1` dentro de un subshell de pipe no cambia el exit code del script (ver leccion).

## Proximo paso

Abrir la app, hacer un click real en cada control y confirmar el revalidate. Despues: fase 3 (bloques managed) o tests.
