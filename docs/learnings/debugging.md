# Learnings - debugging

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Error anidado: leer el cause antes de formular hipotesis

Cuando un error de una libreria de terceros no explica el fallo, revisar el `cause` anidado ANTES de formular una hipotesis. Caso real (kanam-fixer S3, 2026-09-15): `screenReader.start()` de Guidepup tiraba "VoiceOver cannot be started". Ese mensaje apunta a permisos o a un problema de arranque, y por ahi fui: escribi una receta de dos pasos de macOS (VoiceOver Utility + System Events) y se la pase a Gonzo. La causa real estaba en `error.cause.message`: "macOS version not supported" - Guidepup busca la version mayor de Darwin (os.release()) en su manifest.json y lanza si no hay asset para esa plataforma. La maquina es Darwin 27 y el manifest cubre 21-25. Costo: una receta equivocada escrita en la documentacion del proyecto y una accion manual pedida al usuario que no servia para nada. Senales que debieron alertarme antes: (1) `detect()` y `.default()` devolvian true y lo lei como confirmacion del diagnostico, cuando en realidad solo dicen que el lector esta INSTALADO, no que el driver pueda manejarlo; (2) el CLI hermano del mismo proyecto (`npx @guidepup/setup install voiceover`) daba el mensaje correcto y explicito - comparar con las herramientas vecinas del propio paquete es barato y resuelve. Regla: un mensaje de error que no nombra la causa concreta es una pista incompleta, no una conclusion. Protocolo: (a) imprimir el error completo con su cadena de `cause`; (b) si el mensaje externo admite dos hipotesis, no elegir la mas familiar - buscar cual el codigo puede descartar; (c) revisar que dice el resto del paquete sobre la misma condicion. Aplicado al codigo: `realReaderAvailability()` ahora aplana la cadena de causes y el skip del test muestra "VoiceOver cannot be started | macOS version not supported", que es lo que hubiera evitado el desvio.

**Tags:** debugging,errores,metodo

---

