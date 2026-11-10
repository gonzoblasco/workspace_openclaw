---
name: performance-benchmark
description: Benchmark reproducible: linea base, comparacion tras el cambio y decision con evidencia. Usar cuando se afirma que algo es mas rapido o mas lento, cuando hay que elegir entre dos implementaciones, o cuando una optimizacion necesita demostrar que sirvio.
metadata:
  owner: kanam-dev
  status: active
---
# performance-benchmark

Medir el rendimiento de un sistema con datos reproducibles: establecer una línea base, comparar tras un cambio y decidir con evidencia si la optimización sirvió.

## Pasos

1️⃣ **Definir la métrica y el objetivo**

   - Atajo ejecutable: `python3 ~/.openclaw/workspace/agents/kanam-dev/bin/bench_compare.py --baseline base.json --candidate cand.json --threshold 200 --lower-is-better` compara las dos corridas, calcula el delta y decide. Exit 0 cumple, 1 no cumple o cumple con regresion, 2 no se pudo comparar (metricas o unidades distintas). Aprobar una regresion porque todavia esta bajo el umbral es como se acumula el problema.
   - Elegir qué se mide y su unidad: latencia p50/p95/p99, throughput (ops/s), uso de memoria, tiempo de build, TTI.  
   - Fijar un umbral objetivo explícito (ej.: p95 < 200 ms) y el escenario de carga.  
   - Evidencia: `bench/goal.md` con métrica, unidad, umbral y escenario.

2️⃣ **Fijar la línea base con entorno estable**  
   - Documentar hardware, versión de runtime, dataset y parámetros del benchmark.  
   - Correr la medición sobre el commit base (antes del cambio) y guardar el resultado crudo.  
   - Evidencia: `bench/baseline.json` con los resultados y `bench/env.md` con el entorno.

3️⃣ **Ejecutar la medición sobre el cambio**  
   - Correr el mismo benchmark, mismo dataset y mismos parámetros sobre el commit candidato.  
   - Repetir la medición al menos 3 veces para descartar ruido; reportar mediana y dispersión.  
   - En métricas sub-segundo (builds rápidos, micro-benchmarks), el ruido entre corridas puede superar el delta a medir: subir el número de repeticiones hasta que la dispersión sea menor que el cambio esperado.  
   - Evidencia: `bench/candidate.json` con los resultados y la cantidad de corridas.

4️⃣ **Comparar contra la línea base**  
   - Calcular la variación porcentual para cada métrica (baseline → candidato).  
   - Marcar cada métrica como mejora, sin cambio (dentro del ruido) o regresión.  
   - Evidencia: tabla comparativa en `bench/report.md` con valores antes, después y delta.

5️⃣ **Verificar la mejora y descartar regresiones**  
   - Confirmar que la métrica objetivo cruzó el umbral definido en el paso 1.  
   - Revisar que ninguna otra métrica haya empeorado más allá del ruido aceptado.  
   - Si hay regresión, no dar por válida la optimización: documentar la causa.  
   - Evidencia: sección de veredicto en `bench/report.md` (aprobado / rechazado / condicionado).

6️⃣ **Registrar el método para reproducir**  
   - Dejar el comando exacto, la versión de la herramienta y el dataset para que cualquiera repita la medición.  
   - Archivar baseline y candidato junto al cambio para comparaciones futuras.  
   - Evidencia: `bench/README.md` con el comando reproducible y la versión de la herramienta.

## Resultado esperado

- Una línea base medible y un resultado sobre el cambio, ambos crudos y archivados.
- Un informe con valores antes/después, delta porcentual y veredicto explícito.
- Un comando reproducible que permite repetir la medición en el futuro.

## Verificacion

- [ ] Existe una linea base medida **antes** del cambio, con su salida cruda archivada en `bench/runs/`. Sin linea base, no hay comparacion posible.
- [ ] El comando de medicion es reproducible: esta escrito en `bench/command.sh`, corre en un entorno declarado (hardware, version, carga) y da un resultado comparable al repetirlo.
- [ ] El informe tiene antes, despues, delta porcentual y veredicto. Un delta sin direccion ("cambio 12 %") no es veredicto.
- [ ] El veredicto respeta el umbral declarado al inicio: si el objetivo era p95 < 200 ms y el resultado es 210, es un fallo, no un exito parcial.
- [ ] La varianza esta declarada: cuantas corridas, cual es la dispersion. Una sola corrida puede ser ruido.

Lo que NO es criterio: que la optimizacion "se sienta mas rapido". Es exactamente lo que la skill existe para reemplazar.

## Prerequisitos

- Herramienta de benchmark del ecosistema (por ejemplo `k6`, `hyperfine`, `benchmark.js`, `wrk` o el runner integrado del proyecto).
- Entorno estable (misma máquina, mismo runtime, mismo dataset) entre baseline y candidato.

## Regla dura

- Nunca afirmar una mejora de rendimiento sin línea base medida y comparación reproducible. Una percepción de "va más rápido" no es evidencia; la medición archivada sí lo es.
