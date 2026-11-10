---
name: code-metrics
description: Metricas objetivas con umbral explicito: cobertura, complejidad ciclomatica, duplicacion, tamano de funciones y hotspots. Usar para decidir donde intervenir con numeros en vez de impresiones, y para detectar si un cambio empeoro la salud del codigo que toco.
metadata:
  owner: kanam-dev
  status: active
---
# code-metrics

Medir objetivamente la calidad y el tamaño del código con métricas verificables, y usar los números para decidir dónde intervenir.

## Pasos

1️⃣ **Definir las métricas y sus umbrales**  
   - Elegir qué se mide: cobertura de tests, complejidad ciclomática, duplicación, tamaño de funciones, deuda técnica, densidad de comentarios.  
   - Fijar un umbral objetivo por métrica (ej.: cobertura ≥ 80 %, complejidad ciclomática por función ≤ 10).  
   - Evidencia: `metrics/goals.md` con métrica, unidad, umbral y alcance (proyecto o módulo).

2️⃣ **Verificar la herramienta y medir**

   - Atajo ejecutable: `python3 ~/.openclaw/workspace/agents/kanam-dev/bin/metrics_scan.py <dir> --threshold 80` detecta el stack, corre la herramienta de cobertura que exista, normaliza a tabla y escribe `metrics/summary.md` y la salida cruda. Exit 0 cumple, 1 viola, 2 no pudo medir.  
   - Seleccionar la herramienta del ecosistema (por ejemplo Jest/c8 para cobertura JS, pytest-cov para Python, clippy y tarpaulin para Rust, SonarQube para análisis agregado).  
   - Confirmar que la herramienta y sus plugins están **instalados** antes de confiar en la salida: si el config declara un provider (p. ej. `coverage.provider: 'v8'`), el paquete correspondiente (`@vitest/coverage-v8`) debe estar presente. Una dependencia de medición ausente hace fallar el reporte en silencio.  
   - Si una suite de tests falla, la mayoría de los runners **suprimen el reporte de cobertura**: aislar la suite que rompe (excluirla o corregirla) para que el reporte se emita.  
   - Correr la medición sobre el estado actual y guardar la salida cruda.  
   - Evidencia: `metrics/raw/` con los reportes generados por la herramienta.

3️⃣ **Normalizar los resultados**  
   - Convertir las salidas heterogéneas a una tabla única por módulo o paquete.  
   - Marcar cada métrica contra su umbral: cumple, cerca del límite o viola.  
   - Evidencia: `metrics/summary.md` con la tabla por módulo y el estado frente al umbral.

4️⃣ **Localizar los puntos críticos**  
   - Identificar los archivos o funciones que concentran las violaciones (alta complejidad, baja cobertura, mayor duplicación).  
   - Ordenar por impacto sobre la métrica objetivo.  
   - Evidencia: `metrics/hotspots.md` con ranking y la métrica violada de cada punto.

5️⃣ **Decidir la intervención**  
   - Para cada punto crítico, definir la acción: refactorizar, agregar tests, dividir la función o aceptar con justificación documentada.  
   - Marcar lo que queda fuera de alcance y no se toca ahora.  
   - Evidencia: `metrics/plan.md` con punto crítico, acción y responsable.

6️⃣ **Trazar la tendencia**  
   - Comparar contra una medición anterior o la línea base para mostrar si la calidad mejora o empeora.  
   - Registrar la métrica por versión o por release para ver la evolución.  
   - Evidencia: `metrics/trend.md` con la serie histórica y su variación.

## Resultado esperado

- Un conjunto de métricas con umbral explícito y su estado contra ese umbral.
- Un ranking de puntos críticos ordenado por impacto, no por intuición.
- Un plan de intervención con acciones concretas y responsables.
- Una tendencia histórica que muestra si la calidad se mueve en la dirección correcta.

## Verificacion

- [ ] Cada metrica tiene unidad, umbral y alcance declarados en `metrics/goals.md`. Una metrica sin umbral no dice si el proyecto esta sano.
- [ ] La medicion corrio sobre el estado actual y su salida cruda esta en `metrics/raw/`. Comando exacto registrado, no "corri la herramienta". El ejecutable `metrics_scan.py` lo hace y sale 2 cuando no puede medir, nunca 0.
- [ ] La tabla de `metrics/summary.md` marca cada metrica contra su umbral: cumple, cerca o viola. Es el unico lugar donde un numero se interpreta.
- [ ] El ranking de `metrics/hotspots.md` esta ordenado por impacto sobre la metrica objetivo, y cada entrada cita el `file:line`.
- [ ] Cada punto critico tiene una accion decidida (refactorizar, testear, dividir, aceptar con motivo) en `metrics/plan.md`.
- [ ] La tendencia muestra la serie historica con su variacion; si es la primera medicion, esta declarado que la linea base arranca hoy.

Lo que NO es criterio: tener numeros. Un numero sin umbral no es una metrica, es una cifra.

## Prerequisitos

- Herramientas de análisis disponibles para el lenguaje del proyecto.
- Una línea base previa o la disposición a establecerla ahora para medir tendencia.

## Regla dura

- Nunca presentar una métrica sin su umbral y sin el estado contra ese umbral: un número suelto ("cobertura 65 %") no dice si el proyecto está sano. La métrica se interpreta contra un objetivo.
