Bateria de evaluacion: modelo de CODIGO, categoria CHICO (<=1B)

Modelo evaluado: {{modelo}}
Fecha: {{fecha}}

Esta bateria esta calibrada para modelos de bolsillo (celular, edge, <=1B).
No es la bateria de un modelo de 16B: un parser recursivo desde cero no es
un objetivo razonable para 350M y pedirlo no mide capacidad, mide la pregunta.

Cada bloque empieza con la linea "### id". Corres las ocho, en orden.

==================================================================
### c1_funcion_simple
Escribe una funcion Python `es_par(n)` que devuelva True si n es par.
==================================================================
### c2_texto_corto
Explica en 2 lineas, en castellano rioplatense, que hace `git pull`.
==================================================================
### c3_debug_facil
Este codigo falla. Decime en una frase por que y escribi la version corregida.

```python
def promedio(nums):
    return sum(nums) / len(nums)

print(promedio([]))
```
==================================================================
### c4_completar
Completa la funcion. No agregues nada mas.

```python
def maximo(nums):
    # devuelve el mayor de la lista, o None si esta vacia
```
==================================================================
### c5_clasificar
Clasifica cada frase como POSITIVA, NEGATIVA o NEUTRA. Una por linea,
formato `frase | etiqueta`.

1. Me encanto el trato, volveria.
2. Tardo tres horas y nadie me aviso.
3. El local esta en la calle San Martin.
==================================================================
### c6_instruccion_exacta
Responde unicamente con la palabra OK y nada mas.
==================================================================
### c7_aritmetica
Cuanto es 47 * 23? Responde solo el numero.
==================================================================
### c8_resumen
Resumi en una sola frase: "El sistema se cayo tres veces durante la
madrugada y el equipo de guardia detecto que un disco estaba lleno; se
libero espacio y volvio a la normalidad a las 6 de la manana."
==================================================================
