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

---

## Cuando medir contradice la teoria: desborde por position:absolute sin ancestro posicionado

La tabla del historial medía 708px dentro de un panel de 420px y el documento se estiraba a 599px (scroll horizontal). El wrapper ya tenía `overflow-x: auto` y `min-width: 0`, y al volcar la cadena de ancestros con estilos computados TODOS los anchos estaban bien: 396/396, 420/420.

Cuando la medicion contradice la teoria, no hay que insistir con la teoria: hay que medir otra cosa. El dato que faltaba era la POSICION de los elementos, no su tamano. Los `<span class="sr-only">` de los encabezados son `position: absolute`, y sin ningun ancestro posicionado su bloque contenedor es el documento: el `overflow-x` del wrapper nunca los recortaba, asi que estiraban el ancho del documento aunque el wrapper midiera bien.

Regla: para encontrar un desborde horizontal, filtrar los elementos que pasan el viewport EXCLUYENDO los que tienen un ancestro que recorta (`overflow-x: auto|hidden|scroll`). Si esa lista queda vacia y el documento igual desborda, el culpable es un descendiente `position: absolute|fixed` sin ancestro posicionado. Un solo `position: relative` en el contenedor lo resuelve.

Corolario: una heuristica de "elementos que desbordan" sin el filtro de recorte devuelve falsos positivos (todo lo que vive dentro de un scroller) y hace imposible ver la causa.

---

## Separacion vertical 0.0px: margenes por elemento que anulan el gap del contenedor

Gonzo reporto "las cards se pisan con el filtro de arriba". Medido, no interpretado: el filtro terminaba en 670.7 y la primera card empezaba en 670.7. Gap de 0.0px exacto.

La causa: el espaciado vertical estaba repartido en margenes por elemento (`.field` con `margin-bottom`, `.alerta` y `.ayuda` con el suyo) mientras el contenedor no aportaba ninguno. Los margenes y el `gap` se anulaban entre si. Ademas habia parches inline (`marginBottom: 0` en los hijos de la fila) que delataban el sintoma sin arreglar la causa.

Regla: el espaciado entre hijos de un contenedor sale del CONTENEDOR (`display: flex; flex-direction: column; gap`), no de margenes en cada elemento. Un margen en un componente reutilizable es una decision del consumidor disfrazada de decision del componente. Al quitar el margen, hay que revisar TODOS los contenedores donde ese componente se usa: si alguno no es flex con gap, los campos quedan pegados.

Verificacion: medir el gap antes y despues (0.0px -> 24px) sobre la UI viva. Un cambio de CSS sin medicion antes/despues no prueba que arreglo.

---

## Un mock de test desactualizado esconde el bug que el test busca

Al agregar `instruccion` y `applied_candidates` a la respuesta del job, los mocks de `fetch` en los tests de UI quedaron con la forma vieja. Los tests fallaron, y al revisar aparecio algo mejor: la vista hacia `job.instruccion.slice(...)` y un objeto donde se esperaba una lista rompia el componente entero a pantalla en blanco.

Dos lecciones:
1. El mock es parte del contrato. Cuando se agrega un campo a la respuesta de la API, los mocks hay que actualizarlos en el mismo cambio, o los tests dejan de representar la realidad y fallan por una razon que no es la que parecen denunciar.
2. Una respuesta con la forma equivocada no debe poder romper la vista. Se agrego guarda explicita (`Array.isArray(...) ? ... : []`) en el consumidor. Pantalla en blanco ante un payload inesperado es el peor modo de falla: no dice nada.

Corolario de verificacion: los tests que fallan al cambiar el contrato son utiles, pero solo si se lee POR QUE fallan. Si se los hubiera "arreglado" solo actualizando los mocks, el crash por forma invalida quedaba en el codigo.

---

