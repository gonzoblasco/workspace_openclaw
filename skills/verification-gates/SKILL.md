---
name: "verification-gates"
description: "Guardas de verificacion que no dan falso verde: cuando un check pasa pero no probo nada, cuando 0 casos corridos se lee como exito, cuando un SKIP se confunde con OK, o cuando falta el archivo y el reporte lo lee como vacio en lugar de reportarlo."
metadata:
  category: "Hermes SDD"
  tags:
    - hermes-sdd
    - imported
    - verification
---

# verification-gates

Patrones de guardas de verificacion extraidos de `mcabreradev/hermes-sdd-agency`
(`fixtures/*/check.sh`). Los scripts originales testean binarios de Hermes que no existen
en Kanam; lo que se conserva es el criterio con que estan escritos.

## Cuando usarla

- Un check pasa pero no probo nada.
- Cero casos corridos se lee como exito.
- Un SKIP se confunde con un OK.
- Falta el archivo de entrada y el reporte lo lee como vacio en lugar de reportarlo.

## Las tres reglas

### 1. Cero casos corridos no es verde

Una suite cuyo pass es "nada fallo" queda verde cuando **todo fallo al correr**. Hay que
separarlo: si no se corrio ningun caso, no es exito, es un estado distinto y ruidoso.

```
# mal:  exit 0 cuando checked=0
# bien: checked=0 -> exit 3 (no se pudo correr), nunca 0
```

Si el check no pudo correr, tiene que decirlo con un codigo propio. Un `0` silencioso es la
falsa alarma mas cara, porque nadie la mira.

### 2. Un SKIP no es un OK

Saltear un caso es un resultado declarado, con su propio codigo. Nunca se cuenta como
aprobado. El reporte tiene que poder distinguir: corrio y paso / corrio y fallo / no corrio.

### 3. Contrato de honestidad del lector

Un lector de datos que no encuentra el archivo o encuentra una linea ilegible **tiene que
reportarlo**, jamas devolver "vacio". "Vacio" y "no se pudo leer" son hechos distintos y el
segundo es el que importa.

```
# mal:  archivo ausente -> resultado vacio -> "0 entradas, todo bien"
# bien: archivo ausente -> ERROR reportado, distinto de "vacio legitimo"
```

## Como se escribe una guarda

Cada caso es un root real en disco con su resultado esperado, y se verifica **el veredicto y
el codigo de salida**, uno por fila de la tabla contractual. Una fila de la tabla cuyo
patron no matchea es un caso que falla, no un hueco silencioso.

- Un caso por fila de la tabla de contrato, incluyendo los "near miss" que deben quedar limpios.
- Los roots de prueba se construyen en un directorio temporal, nunca dentro del repo.
- El suite limpia lo que creo, incluso si falla en el medio.

## Por que importa aca

Medido el 2026-09-28: dos tandas de sub-agents reportaron `status=done` con tablas de exito
sobre artefactos que el disco desmintio (43 vs 83 reales; 9 vs 0 reales). El runtime valida
que el proceso termino limpio, no que produjo el resultado. Una guarda con estas tres reglas
habria marcado ambos casos como "no probado", en lugar de "verde".

## Origen

`fixtures/run-trace/check.sh` (contrato de honestidad), `fixtures/phase-gate/check.sh`
(codigo de salida distinto para no-corrible), `fixtures/review-tier/check.sh`
(una fila de tabla = un caso).
