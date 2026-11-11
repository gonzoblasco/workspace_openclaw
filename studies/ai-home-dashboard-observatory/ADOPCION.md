# ADOPCIÓN — I Built an App for My House With AI

**Fecha:** 2026-11-11 · **Video:** 13:51 · Peter Lindgren · `studies/ai-home-dashboard-observatory/`

**Pregunta:** ¿qué hacemos hoy mal en el workspace que este video arregla?

## Veredicto

**Sí se adopta, con un artefacto:** `scripts/check-freshness-display.py`, un gate que falla cuando una vista de UI muestra un número medido sin declarar cuándo se midió.

Por qué esta idea y no otra: el video tiene una sola regla de producto que se puede convertir en algo que **falle**, y es la del brillo de los paneles: *«If they're making nothing, or we haven't had a fresh reading, the pulse stops»* (`00:05:36`). Es decir: **un dato viejo presentado como vivo es una mentira de la interfaz**, y distinguir «cero» de «no sé» es parte del diseño, no un detalle estético.

Eso aplica al workspace, no solo a una casa. `projects/preflight` es un escáner de accesibilidad: la portada muestra una lista de *Recent scans* con su `score`, y la vista de reporte muestra el resultado de un scan. Un score sin fecha se lee como «así está el sitio hoy», cuando puede ser de hace un mes. El dato existe (`scanned_at` se guarda en la tabla `scans`, y `recentScans` lo devuelve como `scannedAt`), pero ninguna de las dos pantallas lo renderiza.

## Tabla

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| Un indicador atado a una lectura tiene que apagarse cuando la lectura no es fresca: *«If they're making nothing, or we haven't had a fresh reading, the pulse stops»* (`00:05:36`) | Ninguna vista del workspace declara la antigüedad de un número medido. `preflight` guarda `scanned_at` y la portada de *Recent scans* nunca lo muestra; el reporte tampoco | **`scripts/check-freshness-display.py`** — falla (exit 1) si una vista renderiza un campo medido (`score`, `grade`, `blocking`, `durationMs`…) sin renderizar también su timestamp. Corrido abajo contra `projects/` |
| La lectura se guarda **con la hora en que se tomó**: *«We save each reading with the time it was taken»* (`00:03:10`) | `preflight` ya cumple: `created_at` es `NOT NULL` en la tabla `scans` y viaja al tipo `ScanSummary` como `scannedAt` | **Sin artefacto nuevo.** El dato está; lo que falta es mostrarlo, y eso lo cubre la fila anterior |
| No derivar una métrica de negocio hasta validar la unidad: *«We're getting a number»* (`00:03:23`) … *«check exactly what it measures»* (`00:03:23`) | `scripts/check-unsourced-claims.py` ya exige que una cifra de magnitud en `docs/adr/` y `.knowledge/` diga de dónde salió. No cubre la **unidad** (ms vs. s, kW vs. W) | **Sin adopción:** el problema de la unidad no está demostrado en el repo. El gate de fuente ya existe; ampliarlo sería otro curso con otro caso real |
| Separar el colector de la vista, y la app de su historial: *«The app and the saved history live separately»* (`00:08:36`) | No hay ningún servicio propio con captura continua en el workspace: no hay historial que perder | **Sin adopción.** No hay problema real que arreglar; aplicaría el día que exista un colector propio (hoy el scheduler es del gateway y su estado no es un dataset de producto) |
| Agregar por diferencia y no por suma (garage vs. total, cargador ya incluido) | No hay agregaciones jerárquicas de consumo en ningún proyecto | **Sin adopción.** Sin árbol de medidores, el gate sería un ejercicio teórico |
| Empezar con un equipo y una pregunta antes de la arquitectura: *«start small»* (`00:02:15`) | Ya es regla del workspace: `complexity-scorer` fija el alcance antes de spawnear, y `task-prep` obliga a definir el objetivo | **Sin adopción:** lo cubren `complexity-driven-pipeline` y `task-prep` |

## El artefacto, corrido contra el repo

```bash
$ python3 scripts/check-freshness-display.py --check projects
MISS  projects/preflight/src/app/page.tsx  <- muestra un dato medido sin declarar cuando se midio
MISS  projects/preflight/src/app/r/[id]/page.tsx  <- muestra un dato medido sin declarar cuando se midio

2 vistas revisadas, 2 sin fecha  (ok=0)
FALLA: una vista con dato medido tiene que declarar cuando se midio.
EXIT=1
```

Las dos que marca son reales, no falsos positivos:

- `page.tsx` renderiza `{scan.score}` en la lista *Recent scans* (`<span className={badge badge-${scan.grade}}>{scan.score}</span>`) y nunca `scan.scannedAt`, aunque el campo ya está en el objeto.
- `r/[id]/page.tsx` muestra el resultado del scan sin fecha de medición.

**Qué prueba esto:** el gate mide una ausencia concreta en el repo, no una idea del video. Hoy `preflight` incumple; el fix es de tres líneas (un `<time dateTime={scan.scannedAt}>` en la lista y la fecha en el reporte) y queda como tarea de su sesión, no se aplica desde acá.

**Casos de control** (archivos fuera del repo, para probar que el gate no es un `grep` de palabras):

```bash
$ python3 scripts/check-freshness-display.py --check /tmp/fr
ok    /tmp/fr/ok_page.tsx
MISS  /tmp/fr/bad_page.tsx  <- muestra un dato medido sin declarar cuando se midio

2 vistas revisadas, 1 sin fecha  (ok=1)
```

El `ok_page.tsx` muestra `score` **y** `toLocaleDateString()`: pasa. El `bad_page.tsx` es el mismo componente sin la fecha: falla. El gate distingue el par completo del incompleto.

## Limitación declarada

Es un gate **léxico**, no de comportamiento: detecta que el timestamp se renderice en el archivo, no que sea visible para el usuario. Sirve para que la ausencia sea imposible de olvidar, no para certificar la UI. Un `<time>` oculto con `display:none` lo engaña, igual que a cualquier gate de estático. Se prefiere eso a un gate que no existe.

Tampoco detecta la fecha en listas generadas por un componente distinto del que trae el dato: `page.tsx` lo encuentra porque usa el campo numérico y el timestamp en el mismo archivo. Si la UI se parte en dos, el gate vuelve a pasar en falso y hay que volver a correrlo sobre el componente hijo.

## Lo que el video no cubre

- **Qué es «fresco».** El ponente dice que el pulso se apaga sin lectura fresca, pero no da el umbral (¿2× el intervalo de muestreo? ¿5 minutos?). El gate no puede inventarlo: cada proyecto tiene que declararlo.
- **Retención y agregación del historial.** Cuánto se guarda, con qué granularidad, y qué se descarta. El starter es «the starter foundation, rather than my complete personal setup» (descripción).
- **Fallo del colector.** Qué hace el dashboard cuando el NAS está caído y no hay dato, distinto de cuando el dato es cero. Es el mismo problema que el punto 1, sin resolver en el video.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
