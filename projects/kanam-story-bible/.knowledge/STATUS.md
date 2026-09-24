# STATUS - Kanam Story Bible

## Current Phase

Development - **v1 vertical completo y verificado end-to-end**.

## What's Working

Verificado con `make smoke-ai` (64 aserciones, modelo real) sobre el Mini:

- Proyecto y bloque base (braindump, genero, estilo, sinopsis, tono, POV, audiencia) con enums validados.
- Fichas tipadas: 8 tipos de sistema, atributos validados contra schema, duplicados por nombre normalizado devuelven 409.
- Relaciones con vocabulario controlado; duplicado y kind invalido rechazados.
- Outline: arbol completo, deteccion de ciclos (409), referencias inexistentes (422), proteccion de fichas referenciadas por nodos bloqueados.
- Concurrencia optimista `If-Match` -> 412.
- Indice: outbox transaccional, chunking por ficha con hash de idempotencia, embeddings locales (nomic-embed-text).
- Retrieval hibrido (vector + full-text con fusión por rank recíproco), citas con `entity_id` y `source`, `index_version`.
- Aislamiento entre proyectos verificado: el retrieval de un mundo no devuelve chunks de otro.
- Generacion asincrona: job con `Idempotency-Key`, candidatos que no persisten, `/apply` que crea con `source=ia`, apply repetido 409, duplicado de nombre existente 409.
- Gaps: tipos ausentes y referencias huerfanas.
- Export JSON y Markdown, sin chunks.
- Borrado en dos fases.

Calidad: ruff limpio, mypy limpio (20 archivos), 9 unitarios, 64 aserciones de humo.

## What's Blocked

Nada bloqueado.

## Next Up

1. Worker arq real: el outbox se drena hoy por endpoint, no por proceso.
2. UI web (React + Vite) para editar el mundo sin curl.
3. Autenticacion `token` + scopes (`bible:read/write/generate/retrieve/admin`).
4. Tests de contrato del paquete de export.
5. Decidir licencia del repo.

## Entorno

```bash
make up      # db + redis + api  (Colima: 4 CPU / 8 GB)
make init    # esquema + tipos de sistema
make check   # ruff + mypy + pytest
make smoke-ai
```
