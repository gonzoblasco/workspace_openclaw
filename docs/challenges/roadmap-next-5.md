# Roadmap — próximas 5 tareas

**Fecha:** 2026-11-19
**Estado de partida (verificado, no de memoria):**
- `field-notes`: 8 tests verdes, HEAD `dcf6617`, repo público `gonzoblasco/field-notes`.
- `localdoc-agent` (directorio `localdoc-agent` desde la tarea 2): 25 tests verdes, eval 18/18, repo público `gonzoblasco/localdoc-agent`.
- `a11y-portfolio`: 18 artículos, ensayo bilingüe con `hreflang` + `x-default`, página `/profile/`, HEAD `8a5f983`.
- Post DEV.to id `5068920` con `canonical_url` al blog.
- `AGENTS.md` 18.847/20.000; `MEMORY.md` 19.997/20.000.

---

## Tarea 1 — Pinear los repos y ordenar el perfil de GitHub

**Por qué primero:** es el único trabajo de esta lista que no depende de código y desbloquea que todo lo demás se vea.

**Implementación**
1. Abrir `github.com/gonzoblasco` → *Customize your pins*.
2. Desmarcar los 6 actuales, marcar `field-notes` y `localdoc-agent`, guardar.
3. Verificar que las dos tarjetas muestran descripción y topics (ya cargados).

**Problemas previstos**
- **P1.1 La API no expone el pin.** Verificado: `updateUserPinnedItems` no existe en el schema GraphQL público. No hay atajo; es UI.
- **P1.2 Un repo sin topics se ve vacío.** Ya resuelto: ambos tienen 5 topics cada uno.
- **P1.3 El repo `field-notes` redirige desde `memoria-oral`.** Un pin nuevo toma la URL actual; el redirect sirve para links viejos pero no para el pin. Verificar la URL después de pinear.

**Criterio de cierre:** dos tarjetas visibles en el perfil, con descripción y topics.

---

## Tarea 2 — Cerrar la deuda de nombres entre repo y producto  ✅ HECHA 2026-11-19

**Por qué:** el repo `localdoc-agent` vive en el directorio `agente-local-amigo`. Cualquier agente que lo busque por nombre falla, y a mí ya me pasó dos veces esta sesión.

**Implementación**
1. `mv projects/agente-local-amigo projects/localdoc-agent`.
2. Actualizar el remote (ya apunta bien) y borrar `.venv`, `uv sync`, correr tests.
3. Buscar referencias en workspace: `grep -rn 'agente-local-amigo' --include='*.md' .`
4. Renombrar el programa del Planner `agente-local-lucia` → `localdoc-agent` (o marcarlo cerrado y dejar el archivo como historia).

**Problemas previstos**
- **P2.1 `.venv` roto después del `mv`.** Mismo síntoma que en `field-notes`: `uv run pytest` deja de encontrar el binario. Fix: borrar `.venv` y `uv sync`. **No** hay que recrear el venv a mano.
- **P2.2 Rutas absolutas escondidas en docs.** Buscar `/Users/gonzoblasco` antes de mover, no después.
- **P2.3 El programa del Planner no se puede renombrar por script.** `program_plan.py` no tiene `rename`. Decisión: dejarlo con el slug viejo y anotar el mapping en su HANDOFF, o crear uno nuevo y cerrar el viejo.

**Criterio de cierre:** el directorio `localdoc-agent` existe bajo `projects/`, 25 tests verdes, `grep` sin referencias al nombre viejo fuera de historia.

---

## Tarea 3 — Endurecer las dos apps: el modo "una sola máquina, sin red" deja de ser una promesa  ✅ HECHA 2026-11-19

**Por qué:** hoy la privacidad se demuestra con `lsof` en un momento. Eso es un experimento, no una garantía. Es el material de blog más fuerte de los cinco.

**Implementación**
1. **Prueba de privacidad automática** en ambos repos: script que corre la transcripción/consulta completa bajo un monitor de sockets, y **falla** si ve una conexión. En CI, con un test que lo invoque.
2. **Chequeo de bind:** la app rechaza arrancar si `--host` no es loopback. Falla ruidosa en vez de advertencia en el README.
3. **Prueba de borrado:** el botón "Delete everything" verifica por filesystem que no quedan `.db`, `output/` ni copias en `__pycache__`.

**Problemas previstos**
- **P3.1 `lsof` no es portable ni determinista en CI.** En GitHub Actions conviene `ss -tunap` o un LD_PRELOAD; en macOS, `lsof`. Diseñar el test para que **saltee con razón** si el monitor no está, pero falle si corrió y vio tráfico.
- **P3.2 Ollama escucha en 11434 y el test lo ve.** Hay que distinguir *loopback* de *saliente*. La regla correcta no es "cero sockets" sino "cero sockets **no-loopback**".
- **P3.3 El borrado deja `-wal`/`-shm` de SQLite.** Un `unlink` del `.db` no borra esos dos. Hay que chequearlos y borrarlos explícitamente.

**Resultado real (2026-11-19):**
- El defecto peor no era el sidecar: `POST /delete` tampoco borraba `data/private/`, donde el ingest copia **los originales**. El boton decia "Delete everything" y dejaba los contratos en disco. Corregido en `src/agent/wipe.py` + test.
- La prediccion sobre `__pycache__` era falsa: el bytecode no guarda texto del usuario. El borrado se prueba sobre `.db`, `-wal`, `-shm`, `-journal`, `output/` y `data/private/`.
- El probe **no ve subprocesos**: `whisper-cli`, `afconvert` y el demonio de Ollama quedan fuera del audit hook. Peor: si falta un modelo, **Ollama va al registry**, fuera de Python. Se documenta en ambos README en vez de taparlo.
- El control positivo atrapo una direccion IPv6 real de Cloudflare: la prueba falla si el hook no ve el leak, no solo si ve trafico.

**Criterio de cierre:** un test que falla si aparece una conexión no-loopback, en los dos repos, con salida cruda en el README.

---

## Tarea 4 — Bilingüe de verdad en el blog: el ensayo es una pieza, faltan las demás

**Por qué:** el generador soporta pares y `hreflang`, pero hay **un solo par**. Un sitio bilingüe con un artículo en dos idiomas es una demostración, no un sitio.

**Implementación**
1. Elegir los 3 artículos de mayor valor (`the-quieter-announcement`, `the-bug-jsdom-could-not-see`, `aria-orientation-role-owners`).
2. Escribir la versión española de cada uno **reescribiendo**, no traduciendo: el ritmo cambia con el idioma (lección de esta sesión).
3. Declarar el mismo `pair` en ambas y dejar que el build emita los `hreflang`.
4. Actualizar el índice para que muestre el toggle cuando existe par.

**Problemas previstos**
- **P4.1 El índice no distingue un artículo con par.** Hoy muestra badge “En español” por `lang`, no por par. Hay que agregar la señal “también en español”.
- **P4.2 El feed Atom se duplica.** Un par son dos entradas con el mismo contenido. El feed tiene que emitir **solo el original** de cada par.
- **P4.3 Un par roto rompe el build.** Ya está cubierto: el generador falla si hay dos del mismo idioma o más de dos.

**Criterio de cierre:** 3 pares nuevos, `hreflang` verificado con `grep` en los 6 HTML, feed sin duplicados.

---

## Tarea 5 — El artículo de blog que sale de estas tareas

**Por qué:** es la tarea que convierte el trabajo en material público, y el pedido explícito de Gonzo.

**Implementación**
1. Fuente: esta sesión, no un resumen de README. Lo que pasó de verdad.
2. Tesis: **"un presupuesto de contexto no es un límite de tamaño, es una auditoría"** — el caso de `AGENTS.md`, que estaba en 20.131 cuando la deuda decía 19.997.
3. Anatomía del ensayo del blog: apertura fría, la escena, por qué nada lo detectó, la decisión, la regla.
4. Publicar en el blog primero (EN + ES, con `pair`), sindicar solo el inglés a DEV con `canonical_url`.

**Problemas previstos**
- **P5.1 Contar el número real puede quedar desactualizado.** Escribir "20.131 el 19 de noviembre", no "está en 20.131".
- **P5.2 El artículo se puede volver una lista de tareas.** La regla del blog: si el texto se puede leer como changelog, no es un ensayo.
- **P5.3 Publicar sin `canonical_url`.** Ya pasó una vez. El paso va en el checklist, no en la memoria.

**Criterio de cierre:** artículo en el blog en los dos idiomas, sindicado en inglés con canonical verificado por API.

---

## Riesgos que cruzan todas las tareas

| Riesgo | Por qué aparece | Prevención |
|---|---|---|
| **Auto-reporte de un subagente** | Ya pasó 3 veces esta sesión: archivos que no existían | Correr `git status` + tests antes de aceptar cualquier entrega |
| **`.venv` roto al mover un directorio** | Pasó con `field-notes` | Después de cada `mv`: borrar `.venv` + `uv sync` |
| **`AGENTS.md` al borde del cap** | 18.847 ahora, 1.153 de aire | Medir antes de agregar una regla, no después |
| **Commit con archivos ajenos** | Pasó dos veces el 2026-11-06 | `git diff --cached --name-only` antes de cada commit |
| **Un dato escrito a mano que se desincroniza** | `MEMORY.md` con tags de modelo; `check-claims` falló | El dueño del dato manda; los demás citan |

## Orden recomendado

1 → 2 → 3 → 4 → 5. La 1 es gratis y desbloquea visibilidad; la 2 evita que las siguientes se rompan por un nombre; la 3 y la 4 son el cuerpo técnico; la 5 se escribe con evidencia fresca de las cuatro.
