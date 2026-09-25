# STATUS - Kanam Story Bible

## Current Phase

Development - **v0.3.0: API completa, interfaz web con recuperacion de datos**.

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

**UI (verificado con `npx vitest run`: 9/9):**

- 9 secciones: Mundo, Fichas, Relaciones, Outline, Retrieval, Generar, Que falta, Papelera, Export.
- Crear, editar y borrar fichas; el formulario de atributos se arma desde el tipo.
- Panel de retrieval que muestra puntaje, origen y relevancia de cada fragmento.
- Generacion con propuestas aplicables de a una, mas **historial** de generaciones
  anteriores con boton para reabrir las propuestas sin volver a llamar al modelo.
- **Papelera**: lista las fichas borradas y las restaura.
- Estados vacio, de carga y de error en cada vista.

**Calidad:** ruff limpio, mypy limpio (20 archivos), 9 unitarios Python, 64 aserciones de humo, 9 tests de UI, `scripts/verify_apply.py` (14 aserciones), typecheck estricto y build de la UI limpios. Las 8 vistas medidas a 420px sin desborde horizontal (`scripts/ui-shot.mjs`).

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
- **Los scripts de prueba comparten base con los datos reales.** Es la deuda que mas
  dolio: `verify_apply.py` corrio contra un mundo real y lo dejo vacio (ADR-069).
  Mitigado con la regla "un script no toca un mundo que no creo", pero la separacion
  fisica de la base es el arreglo de fondo y sigue pendiente.
- El endpoint de purga fisica de un mundo ya borrado no esta expuesto (la funcion
  `purgar_bible` existe en `services.py`).
- `neat-bloom` (dev server de Vite) corre como proceso de la sesion: si se cierra la
  sesion, la UI queda servida desde el build pero sin HMR. Ver deuda del LaunchAgent.

## Como recuperar cosas

- **Una ficha borrada:** seccion Papelera, o `POST /projects/{id}/entities/{eid}/restore`.
- **Propuestas de una generacion anterior:** seccion Generar, tabla "Generaciones
  anteriores", boton "Ver propuestas".
- **Un mundo entero:** `DELETE /projects/{id}` con el header
  `X-Confirmar-Titulo: <titulo exacto>` (borrado logico, mismo esquema de dos fases).
