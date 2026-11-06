# Tabla de verdad: bateria de modelos chicos (<=1B)

Fuentes versionadas para la bateria `bateria-chico.md`. Cada prueba tiene una
respuesta objetiva; el evaluador compara contra esto y no contra su criterio.

## c1_funcion_simple — `es_par(n)`

**CORRECTO** si `n % 2 == 0` es el criterio de retorno (con `return`).
**FALSO** si usa `n % 2 == 1`, invierte el resultado, o no devuelve booleano.

## c2_texto_corto — explicar `git pull` en rioplatense

**CORRECTO** si (a) dice que trae/baja los cambios del remoto y los fusiona
o integra en el branch local, y (b) usa alguna marca rioplatense (voseo,
registro informal).
**INCOMPLETO** si explica bien pero ignora el registro pedido.
**FALSO** si describe mal el comando (lo confunde con `git push`, con `clone`,
o dice que borra cambios locales).

## c3_debug_facil — `promedio([])`

Causa real: division por cero (`len([]) == 0`) o `ZeroDivisionError`.
**CORRECTO** si nombra la division por cero Y la version corregida maneja la
lista vacia (retorna 0, None, o lanza un error explicito controlado).
**INCOMPLETO** si identifica la causa pero el fix no cubre el caso.
**FALSO** si atribuye el fallo a otra causa, o su explicacion menciona
verificaciones o guardas que no estan en el codigo original.

## c4_completar — `maximo(nums)`

**CORRECTO** si devuelve el mayor y `None` (o equivalente) para lista vacia,
sin agregar funciones extra.
**FALSO** si falla con lista vacia (devuelve 0, lanza excepcion, o
`max([])` sin guarda).

## c5_clasificar — tres frases

Respuesta esperada:
- "Me encanto el trato, volveria." -> **POSITIVA**
- "Tardo tres horas y nadie me aviso." -> **NEGATIVA**
- "El local esta en la calle San Martin." -> **NEUTRA**

**CORRECTO** si las tres etiquetas coinciden, **en cualquier formato**
(numeradas, con pipe, con salto de linea, con el texto repetido).
El formato pedido era `frase | etiqueta`, pero un formato distinto con las
tres etiquetas correctas es CORRECTO: la tarea mide clasificacion, no
formato. Si se quiere medir formato, eso es c6.
**INCOMPLETO** si dos de tres.
**FALSO** si una o ninguna, o si inventa frases que no estaban.

## c6_instruccion_exacta — responder solo `OK`

**CORRECTO** si la salida completa, quitando espacios y puntuacion final, es
exactamente `OK`.
**FALSO** en cualquier otro caso. `OK nada`, `OK.` con texto agregado,
`Claro, OK` son FALSO. Esta prueba mide obediencia literal, no cortesia:
agregar una palabra es fallar, y es un fallo medible.

## c7_aritmetica — 47 * 23

Respuesta correcta: **1081**.
**CORRECTO** si el unico numero de la respuesta es 1081.
**FALSO** con cualquier otro numero, aunque muestre el procedimiento.
Nota: 529 es 23^2, no 47*23.

## c8_resumen — una sola frase

El texto fuente esta en el prompt de la prueba. El resumen debe incluir:
caida repetida (tres veces), causa (disco lleno) y resolucion (liberado, ~6am).

**CORRECTO** si es una sola frase y contiene las tres piezas.
**INCOMPLETO** si es una frase pero pierde una pieza, o si son dos frases con
las tres piezas.
**FALSO** si agrega hechos que no estan en el original (causa inventada,
cantidades que no aparecen, culpables).
**NO_VERIFICABLE** solo si la salida no es un resumen.

## Regla de puntuacion

`NO_VERIFICABLE` cuenta como fallo en todas las pruebas de esta bateria:
cada una tiene respuesta objetiva. Una respuesta que no se puede contrastar
no es un aprobado.
