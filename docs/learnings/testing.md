# Learnings - testing

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## Tests de integracion contra un MCP real: event loop scope y volumenes Docker

Al escribir tests de integracion contra un MCP real, hay dos trampas que cuestan horas:

(1) EVENT LOOP SCOPE. Con pytest-asyncio, el default de `asyncio_default_fixture_loop_scope` y `asyncio_default_test_loop_scope` es "function". Si un fixture module-scoped levanta un recurso que vive en un event loop (un cliente MCP stdio, una conexion, un server), y los tests corren en otro loop, el recurso queda colgado en el loop del fixture: la suite no falla, se CUELGA indefinidamente. Sin pytest-asyncio, un `pytest -q` de 41 minutos con 0% de CPU es la firma. El fix es `asyncio_default_fixture_loop_scope = module` + `asyncio_default_test_loop_scope = module`, para que fixture y tests compartan loop.

(2) RECURSOS COMPARTIDOS ENTRE CONTENEDORES. Un volumen Docker nombrado para el directorio de datos de un navegador (Chrome) NO es seguro: dos contenedores que lo comparten pelean por el `SingletonLock` del mismo `user-data-dir`, el segundo Chrome pierde, y el lock stale sobrevive entre corridas (el browser no limpia locks viejos). Lo que si funciona: que cada contenedor tenga su propio volumen ANONIMO, que Docker crea y destruye con el contenedor. La imagen puede declarar `VOLUME /data` y listo: sin montar nada, cada `docker run` recibe uno nuevo. Y un bind mount del directorio de datos del host es PEOR todavia: el host y el contenedor tienen uids distintos, el perfil no se puede abrir y el navegador muere al arrancar.

Sintoma diagnostico de ambos: "Browser process (PID n) exited before CDP became available" o "Expected at least one handler to return a non-None result" (esta ultima es de bubus: el handler devolvio None). Y aparece como un 502 en la API, no como un error de nucleo.

Regla general: antes de afirmar que un contenedor "funciona", probalo DOS veces seguidas. El primer arranque contra un volumen recien creado puede fallar una vez (arranque en frio) y el segundo pasa: un solo run verde no prueba nada.

---

