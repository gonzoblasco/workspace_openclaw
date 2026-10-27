# Learnings - debugging

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Error anidado: leer el cause antes de formular hipotesis

Cuando un error de una libreria de terceros no explica el fallo, revisar el `cause` anidado ANTES de formular una hipotesis. Caso real (kanam-fixer S3, 2026-09-15): `screenReader.start()` de Guidepup tiraba "VoiceOver cannot be started". Ese mensaje apunta a permisos o a un problema de arranque, y por ahi fui: escribi una receta de dos pasos de macOS (VoiceOver Utility + System Events) y se la pase a Gonzo. La causa real estaba en `error.cause.message`: "macOS version not supported" - Guidepup busca la version mayor de Darwin (os.release()) en su manifest.json y lanza si no hay asset para esa plataforma. La maquina es Darwin 27 y el manifest cubre 21-25. Costo: una receta equivocada escrita en la documentacion del proyecto y una accion manual pedida al usuario que no servia para nada. Senales que debieron alertarme antes: (1) `detect()` y `.default()` devolvian true y lo lei como confirmacion del diagnostico, cuando en realidad solo dicen que el lector esta INSTALADO, no que el driver pueda manejarlo; (2) el CLI hermano del mismo proyecto (`npx @guidepup/setup install voiceover`) daba el mensaje correcto y explicito - comparar con las herramientas vecinas del propio paquete es barato y resuelve. Regla: un mensaje de error que no nombra la causa concreta es una pista incompleta, no una conclusion. Protocolo: (a) imprimir el error completo con su cadena de `cause`; (b) si el mensaje externo admite dos hipotesis, no elegir la mas familiar - buscar cual el codigo puede descartar; (c) revisar que dice el resto del paquete sobre la misma condicion. Aplicado al codigo: `realReaderAvailability()` ahora aplana la cadena de causes y el skip del test muestra "VoiceOver cannot be started | macOS version not supported", que es lo que hubiera evitado el desvio.

**Tags:** debugging,errores,metodo

---

## Indice vectorial abortado a medias: el conteo parcial reportado como exito

CONTEXTO: construí kanam-insight y reporté "2557 vectores indexados" como éxito. Horas después, un comando async devolvió una traza de ChromaDB por IDs duplicados.

QUÉ PASÓ: los IDs de chunk se generaban con el NOMBRE del archivo. Archivos homónimos en carpetas distintas colisionaban (docs/README.md vs docs/adr/README.md -> ambos docs::README.md::0). Eran 142 colisiones reales. Chroma rechaza IDs repetidos dentro de un lote y ABORTA el indexado. El índice quedó con 1920 vectores; yo reporté 2557, que era el número de una corrida PARCIAL leída a mitad de camino.

POR QUÉ NO LO VI: verifiqué que el comando terminara y leí el conteo, pero no verifiqué que el conteo fuera el correcto. "El comando terminó" y "el resultado es correcto" son dos afirmaciones distintas. Es el mismo error que ese día le señalé tres veces a la documentación del workspace: declarar un estado sin evidencia que lo respalde.

REGLA QUE ME LLEVO: cuando un proceso reporta un resultado agregado, verificar el ORDEN DE MAGNITUD esperado antes de reportarlo. Si el scanner dice N archivos y el índice dice M vectores, contrastar contra una cuenta independiente (chunks que el scanner generaría). Un índice que aborta a la mitad no avisa: reporta lo que alcanzó a escribir.

**Tags:** verificacion,autoevaluacion,chromadb,indices-vectoriales,reporte-de-resultados

---

## Cuando medir contradice la teoria: desborde por position:absolute sin ancestro posicionado

La tabla del historial medía 708px dentro de un panel de 420px y el documento se estiraba a 599px (scroll horizontal). El wrapper ya tenía `overflow-x: auto` y `min-width: 0`, y al volcar la cadena de ancestros con estilos computados TODOS los anchos estaban bien: 396/396, 420/420.

Cuando la medicion contradice la teoria, no hay que insistir con la teoria: hay que medir otra cosa. El dato que faltaba era la POSICION de los elementos, no su tamano. Los `<span class="sr-only">` de los encabezados son `position: absolute`, y sin ningun ancestro posicionado su bloque contenedor es el documento: el `overflow-x` del wrapper nunca los recortaba, asi que estiraban el ancho del documento aunque el wrapper midiera bien.

Regla: para encontrar un desborde horizontal, filtrar los elementos que pasan el viewport EXCLUYENDO los que tienen un ancestro que recorta (`overflow-x: auto|hidden|scroll`). Si esa lista queda vacia y el documento igual desborda, el culpable es un descendiente `position: absolute|fixed` sin ancestro posicionado. Un solo `position: relative` en el contenedor lo resuelve.

Corolario: una heuristica de "elementos que desbordan" sin el filtro de recorte devuelve falsos positivos (todo lo que vive dentro de un scroller) y hace imposible ver la causa.

**Tags:** layout,css

---

## Separacion vertical 0.0px: margenes por elemento que anulan el gap del contenedor

Gonzo reporto "las cards se pisan con el filtro de arriba". Medido, no interpretado: el filtro terminaba en 670.7 y la primera card empezaba en 670.7. Gap de 0.0px exacto.

La causa: el espaciado vertical estaba repartido en margenes por elemento (`.field` con `margin-bottom`, `.alerta` y `.ayuda` con el suyo) mientras el contenedor no aportaba ninguno. Los margenes y el `gap` se anulaban entre si. Ademas habia parches inline (`marginBottom: 0` en los hijos de la fila) que delataban el sintoma sin arreglar la causa.

Regla: el espaciado entre hijos de un contenedor sale del CONTENEDOR (`display: flex; flex-direction: column; gap`), no de margenes en cada elemento. Un margen en un componente reutilizable es una decision del consumidor disfrazada de decision del componente. Al quitar el margen, hay que revisar TODOS los contenedores donde ese componente se usa: si alguno no es flex con gap, los campos quedan pegados.

Verificacion: medir el gap antes y despues (0.0px -> 24px) sobre la UI viva. Un cambio de CSS sin medicion antes/despues no prueba que arreglo.

**Tags:** layout,spacing

---

## Un mock de test desactualizado esconde el bug que el test busca

Al agregar `instruccion` y `applied_candidates` a la respuesta del job, los mocks de `fetch` en los tests de UI quedaron con la forma vieja. Los tests fallaron, y al revisar aparecio algo mejor: la vista hacia `job.instruccion.slice(...)` y un objeto donde se esperaba una lista rompia el componente entero a pantalla en blanco.

Dos lecciones:
1. El mock es parte del contrato. Cuando se agrega un campo a la respuesta de la API, los mocks hay que actualizarlos en el mismo cambio, o los tests dejan de representar la realidad y fallan por una razon que no es la que parecen denunciar.
2. Una respuesta con la forma equivocada no debe poder romper la vista. Se agrego guarda explicita (`Array.isArray(...) ? ... : []`) en el consumidor. Pantalla en blanco ante un payload inesperado es el peor modo de falla: no dice nada.

Corolario de verificacion: los tests que fallan al cambiar el contrato son utiles, pero solo si se lee POR QUE fallan. Si se los hubiera "arreglado" solo actualizando los mocks, el crash por forma invalida quedaba en el codigo.

**Tags:** mocks,contrato

---

## LECCIONES DURABLES DE ESTA SESIÓN

1. **Los tests encontraron un bug real de unidades.** El normalizador devolvía la unidad **de origen** (`cm`, `l`, `lb`) en vez de la canónica: `96 cm` no llegaba a `960 mm`. Sin los tests, el filtro por cilindrada y el comparador habrían quedado inservibles **en silencio**. Moraleja: normalizar unidades es donde se esconden los bugs silenciosos. 2. **La revisión visual encontró DOS FUENTES DE VERDAD.** La ficha de unidad calculaba "Ficha técnica parcial" con un umbral propio del componente (`specs.length < 8`), mientras `public_catalog` lo derivaba en SQL. Dos reglas para lo mismo, que tarde o temprano se contradicen. Se extrajo `model_spec_state()` (migración 6): **la base es la única definición**. **Ningún test lo agarraba - solo mirar la pantalla.** Validar visualmente los sitios de marca es tan obligatorio como el build. 3. **El constraint atrapó un error en mi propio seed.** Cargué specs de texto sin `value_text` y el `check` del esquema lo rechazó. El esquema defiende lo que dice defender. 4. **El esquema no puede confiar en que los roles existan.** En Postgres pelado hay que stubear `auth.users`, `auth.uid()` y los roles `anon`/`authenticated`/`service_role` **ANTES** de las migraciones (las policies los referencian). Y hay que replicar los **grants** que Supabase da por defecto, porque allí RLS es lo que restringe, no la ausencia de permisos: si no, el test de aislamiento mide la cosa equivocada. 5. **El navegador del gateway bloquea localhost por política SSRF** (`browser navigation blocked by policy`). La validación visual se hace con **Playwright headless** (`scripts/visual-check.mjs`, 12 capturas / 2 viewports). Las capturas deben copiarse a un directorio permitido (`~/.openclaw/workspace/tmp/`) para poder verlas con `view_image` - `/tmp` no está permitido. 6. **Servidores en background:** el patrón `(cmd &)` y `nohup ... & disown` **mueren al terminar el comando**. Lo que funciona es el modo `background: true` del propio `exec`. 7. **El build no debe depender de datos vivos.** `getCatalogGateway()` no lanza: si no hay backend configurado, devuelve un gateway que **falla al usarse**, así el build y el render funcionan y las páginas muestran su estado de error honesto en vez de romper el build. 8. **El hook del pre-commit valida rutas citadas en markdown.** Citar `projects/kanam-onwheels/scripts/verify-schema.sh` (del proyecto) en `MEMORY.md` (del workspace) lo detecta como ruta rota. **Regla: calificar con `~/projects/<slug>/` toda ruta de código de proyecto.**

---

## Moderno Diffusion: dos fallas propias - el harness mataba la app, y un DELETE massivo borro 9 lecciones reales

Dos fallas propias de las ultimas horas con Moderno Diffusion (2026-10-27), generalizables a cualquier trabajo con un harness de ejecucion.

Lesson - "la app crashea" era mi harness, no la app:
- Diagnostico: el log de Electron mostraba `stateeee` (guardado de posicion de ventana) y CERO eventos de crash. Un SIGKILL no dispara `process.on('exit')`. Conclusion: el proceso lo estaba matando mi propio `exec`, porque al terminar el shell mataba el grupo de procesos completo.
- Regla: cuando un proceso "muere solo" sin traza, sospechar primero del harness. Senal concreta: un handler de salida que nunca se ejecuta mas un log que muestra actividad normal hasta el corte = muerte por senal, no crash. Solucion: lanzar la app como servicio independiente (setsid / nohup) para que sobreviva al cierre del shell que la lanzo.
- Fallo mio: perdi una horaonga de debugging persiguiendo un crash inexistente porque la primera hipotesis ("crash de Electron") era la mas familiar y no descarte la alternativa que el codigo permitia descartar.

Lesson - borrar en la DB de memoria sin leer el esquema destruyo 9 lecciones reales:
- La tabla `learnings` guarda la leccion en la columna `title`, no en `content`. `content` esta vacia en las 249 filas. Ejecute un DELETE buscando `content IS NULL OR length(content)<5` creyendo que detectaba entradas vacias: borro 9 lecciones TICAS, incluida una sobre OAuth/PAT de GitHub.
- Recuperacion: la copia previa de `memory.db` permitio restaurar las 9 con INSERT por id, y un script de verificacion fila por fila confirmo 0 diferencias contra la copia.
- Regla: ANTES de un DELETE masivo sobre la DB, leer el esquema (`PRAGMA table_info`) y hacer una copia. Un `SELECT` de conteo no alcanza: hay que ver la forma de la fila, no el numero. Y verificar el restaurado con una comparacion fila a fila contra la copia, no con un count.
- Regla relacionada (ya estaba en AGENTS.md y la ignore): preferir `trash` antes que `rm`, y sobre todo no usar SQL destructivo como atajo de limpieza.

Lesson - el repositorio clonado era el unico hogar de cambios no publicados:
- El branch `fix/macos-arm64-stability` (3 commits) nunca se pusheo: el remoto es el repo de Jose y no habia OK explicito para publicar. Al descartar el proyecto, esos commits se perdieron con el repo. Regla: un trabajo que no se publico no tiene existencia durable; el precio de no publicar (o de descartar) es el trabajo completo, no solo el tiempo.

**Tags:** memoria,harness,debugging,trash

---

## Auditoria de la tabla learnings: el cuerpo de la leccion no tiene un lugar fijo, y el truncado del catalogo era una decision

Auditoria de la tabla `learnings` (2026-10-27), hecha porque un DELETE mio borro 9 lecciones reales. No fue un error puntual: son 4 defectos estructurales que el esquema permitia y nada impedia.

Defecto 1 - el cuerpo de la leccion no tiene un lugar fijo. Hay filas donde esta en `content` (lo normal), en `title` y en `tags`. El export a docs/learnings/*.md lee el cuerpo de `content` y el titulo de `title`, asi que las otras dos clases se veian como seccion vacia y nadie lo notaba. Origen: `migrate-learnings.py` derivaba los tags del titulo, y la absorcion de la tabla gemela (commit 0518cdf3f3) descarto la prosa de `tags` asumiendo que era "el titulo duplicado". Suposicion falsa: en 5 filas la prosa era el CUERPO.

Defecto 2 - `add-learning` escribia en la columna `tags` y nunca en la junction `learning_tags`, que es lo UNICO que lee el export. 79 filas con tags reales que no aparecian en ninguna vista. Todo lo agregado por ese comando desde la taxonomia normalizado quedo invisible.

Defecto 3 - `memory-catalog-v2.py` cortaba el cuerpo a 500 chars con el mismo valor que usaba para el embedding: `content_text = learning.get("content","")[:500]`. 34 filas quedaron con el cuerpo a la mitad. 20 eran recuperables del corpus (`sessions_relacional.content_bare` / `daily_notes.content`, buscando el fragmento del MEDIO, no el prefijo) y se recuperaron; 14 no existen en ningun lado.

Defecto 4 - el truncado del catalogo no era un error de codigo, era una decision: el tope de 500 chars es del embedding, y se aplicaba tambien al dato guardado. La regla que sale: un tope de la API no es un tope del dato.

Reglas que salen, generales:
1. ANTES de un DELETE masivo sobre la DB, leer el esquema (`PRAGMA table_info`) y hacer una copia. Un SELECT de conteo no alcanza: hay que ver la FORMA de la fila. La tabla `learnings` guarda la leccion en `title` y deja `content` vacio en las filas viejas: leer el codigo de escritura (`memory-db.sh add-learning`) es mas seguro que inferir del promedio de una columna.
2. Un guard que reporta 169 filas no se lee y no se respeta. El gate nuevo separa PERDIDA (bloquea: el cuerpo no esta donde debe) de RUIDO HISTORICO (avisa: prosa en tags, titulo largo). Con el recalibrado: 0 perdidas, 70 avisos.
3. Cuando el codigo y los datos discrepan, el codigo es la fuente. Para reconstruir como se genero una fila, leer el extractor (`extract_learnings` acumula lineas hasta el proximo `###` y las une con ESPACIOS) en vez de inventar un corte. Con un corte inventado, una leccion de 500 chars salia como una de 72.174.
4. Verificar el efecto, no la intention: "movimos el cuerpo a content" hay que comprobarlo con un diff de la vista exportada, no con un UPDATE que dijo exito.

Resultado de la auditoria: 9 cuerpos recuperados (5 de `tags`, 4 de `title`), 20 truncadas recuperadas del corpus, 79 filas con los tags repoblados en la junction. Los .mdunque stingieron +15.912 chars de cuerpo que estaba perdido. Causas raiz corregidas: `add-learning` escribe en la junction, y el catalogo ya no trunca el cuerpo (el tope de 500 queda solo para el embedding). Gate nuevo: `scripts/check-learnings-integrity.py`, en el pre-commit.

**Tags:** memoria,db,schema,integridad,guard

---

