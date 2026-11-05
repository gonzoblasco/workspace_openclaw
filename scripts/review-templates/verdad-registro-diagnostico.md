# Tabla de verdad: registro pedido y diagnóstico local

Fuentes versionadas para `p2_explicacion` y `p7_local`. Igual que
`verdad-consenso.md`: el evaluador compara contra esto, no contra su criterio.

## p2_explicacion — registro rioplatense

El prompt pide: *"Explica en castellano rioplatense, en 4 lineas"*.

Marca **CORRECTO** solo si se cumplen las dos condiciones:

1. **La explicación es correcta** (context manager = objeto que garantiza
   liberar recursos al salir del bloque `with`, incluso ante excepción).
2. **El registro es rioplatense.** Se acepta: voseo (`vos`, `tenés`, `usás`,
   `te sirve`) o registro informal neutro sin marcas de España.

Marca **FALSO** si:

- Usa "usted", "vosotros", "os", o conjugaciones de segunda persona peninsular.
- Escribe en español neutro de manual sin ninguna marca rioplatense, **cuando
  el prompt lo pidió explícitamente**. Ignorar una instrucción de registro es
  un defecto, no un detalle de estilo.

Marca **NO_VERIFICABLE** solo si el texto no alcanza para decidir.

Referencia de qué NO se acepta como rioplatense: comillas angulares «», formas
como "se usa comúnmente", "resulta", "a fin de". Registro de libro.

## p7_local — ECONNREFUSED 127.0.0.1:5432

El prompt: usuario argentino no técnico, log `ECONNREFUSED 127.0.0.1:5432`,
pide respuesta en 3 líneas sin tecnicismos innecesarios.

Marca **CORRECTO** solo si la respuesta le dice al usuario la causa real:

- **`127.0.0.1` significa que la base de datos corre en la MISMA máquina que la
  aplicación, y `ECONNREFUSED` significa que no está escuchando en ese puerto.**
- La acción concreta es **levantar el servicio de base de datos** (arrancar
  Postgres/MySQL en la máquina local), o confirmar que el servicio está instalado.

Marca **FALSO** si:

- Sugiere revisar la red, el firewall, o "la conexión desde otro dispositivo":
  `127.0.0.1` es loopback, no hay red involucrada.
- Habla de "el servidor" o "el servidor remoto": no hay servidor remoto.
- Propone revisar credenciales: `ECONNREFUSED` es un fallo de conexión TCP, no
  de autenticación (eso sería `password authentication failed`).

Marca **NO_VERIFICABLE** solo si no dice nada accionable.

Referencia técnica: `ECONNREFUSED` en un socket TCP = nadie escuchando en ese
puerto. Con host `127.0.0.1`, el destino es el propio equipo.

## Regla de puntuación

`NO_VERIFICABLE` cuenta como fallo en ambas pruebas: las dos piden una respuesta
concreta y verificable. Una respuesta que no se puede contrastar no es un
aprobado.
