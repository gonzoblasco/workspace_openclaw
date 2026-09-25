# STATUS - Kanam Story Bible

## Current Phase

Development - **v0.2.0: API completa + interfaz web funcionando**.

## Como se levanta

```bash
# Stack (Colima debe estar corriendo: colima start)
make up      # db + redis + api   -> http://127.0.0.1:8080
make init    # esquema + tipos de sistema (solo la primera vez)
make seed    # mundo de demostracion: 9 fichas, 8 relaciones, outline de 6 nodos

# Interfaz web
cd ui && npm install && npm run dev   # -> http://127.0.0.1:5173
```

La UI habla same-origin con `/api` y Vite lo proxea al 8080, asi que no hay CORS.

## What's Working

**API (verificado con `make smoke-ai`: 64 aserciones, modelo real, 0 fallas):**

- Proyecto y bloque base con enums validados.
- 8 tipos de ficha con atributos validados contra schema por tipo; duplicados por nombre normalizado devuelven 409.
- Relaciones con vocabulario controlado.
- Outline: ciclos (409), referencias inexistentes (422), fichas protegidas por nodo bloqueado.
- Concurrencia optimista `If-Match` -> 412.
- Indice: outbox transaccional, chunking con hash de idempotencia, embeddings locales (nomic-embed-text).
- Retrieval hibrido (vector + full-text, fusion por rank reciproco) con citas, `index_version` y similitud coseno real como score.
- Aislamiento entre proyectos verificado en ambas direcciones.
- Generacion asincrona: candidatos que no persisten, `/apply` con `source=ia`, apply repetido 409, duplicado 409.
- Gaps, export JSON/Markdown, borrado en dos fases.

**UI (verificado con `npx vitest run`: 6/6):**

- 8 secciones: Mundo, Fichas, Relaciones, Outline, Retrieval, Generar, Que falta, Export.
- Crear, editar y borrar fichas; el formulario de atributos se arma desde el tipo.
- Panel de retrieval que muestra puntaje, origen y relevancia de cada fragmento.
- Generacion con propuestas aplicables de a una.
- Estados vacio, de carga y de error en cada vista.

**Calidad:** ruff limpio, mypy limpio (20 archivos), 9 unitarios Python, 64 aserciones de humo, 6 tests de UI, typecheck estricto y build de la UI limpios.

## What's Blocked

Nada bloqueado.

## Next Up

1. Editor visual del outline (hoy la vista lo lee; se carga por API).
2. Edicion de atributos de una ficha existente.
3. Worker arq real: el outbox se drena por endpoint.
4. Autenticacion `token` + scopes.
5. Decidir licencia del repo.

## Deuda tecnica

- El dev server de Vite y el stack de Docker no sobreviven un reinicio de la maquina: no hay LaunchAgent.
- Sin paginacion infinita en la UI (hay boton "Cargar mas" en Fichas).
- `chunk.embedding` es `vector(768)` fijo: cambiar de modelo de embeddings exige migracion.
