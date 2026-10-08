---
title: chaos-engineering
description: TODO: add description
---
# chaos-engineering

Probar la resiliencia de un sistema inyectando fallos controlados, midiendo cómo se degrada y si se recupera, antes de que el fallo ocurra en producción.

## Pasos

1️⃣ **Definir la hipótesis de estado estable**  
   - Medir el comportamiento normal del sistema con una métrica observable (tasa de éxito, latencia p95, throughput).  
   - Escribir la hipótesis explícita: "el sistema mantiene X bajo el fallo Y".  
   - Evidencia: `chaos/hypothesis.md` con la métrica, el valor estable y el fallo a inyectar.

2️⃣ **Elegir el experimento y su alcance**  
   - Seleccionar el fallo a inyectar: latencia, caída de red, caída de instancia, error de dependencia, saturación de CPU/memoria.  
   - Acotar el blast radius: qué servicio, qué porcentaje de tráfico, cuánto tiempo, y cómo detenerlo.  
   - Evidencia: `chaos/experiment.md` con el fallo, el blast radius y el botón de aborto.

3️⃣ **Preparar la observabilidad y el aborto**  
   - Confirmar que la métrica de la hipótesis se está midiendo en vivo y es visible durante el experimento.  
   - Definir la condición de aborto automático (ej.: tasa de éxito < umbral) y probar que funciona.  
   - Evidencia: `chaos/watch.md` con la métrica observada y la condición de aborto verificada.

4️⃣ **Ejecutar en entorno no productivo primero**  
   - Correr el experimento en staging sobre la misma topología que producción.  
   - Registrar el comportamiento observado con timestamps durante toda la inyección.  
   - Evidencia: `chaos/runs/<fecha>.json` con la serie temporal y el fallo inyectado.

5️⃣ **Evaluar la resiliencia**  
   - Comparar el comportamiento durante el fallo contra la hipótesis: ¿se mantuvo el estado estable?  
   - Identificar los modos de fallo reales: degradación, error en cascada, recuperación, punto único de fallo.  
   - Evidencia: `chaos/findings.md` con hipótesis vs. observado y los modos de fallo encontrados.

6️⃣ **Corregir y convertir en guardia permanente**  
   - Priorizar los puntos únicos de fallo y las degradaciones no aceptadas como work items.  
   - Convertir el experimento que encontró un fallo real en un test continuo o un game day recurrente.  
   - Evidencia: `chaos/backlog.md` con hallazgo → fix → owner, y `chaos/README.md` con la cadencia del game day.

## Resultado esperado

- Una hipótesis de estado estable explícita y su valor medido.
- Un experimento acotado con blast radius controlado y botón de aborto probado.
- Evidencia temporal de cómo se comportó el sistema bajo el fallo, no una impresión.
- Modos de fallo identificados y priorizados como work items.
- Experimentos que encontraron fallos reales, convertidos en guardias permanentes.

## Prerequisitos

- Observabilidad en vivo de la métrica de la hipótesis.
- Herramienta de inyección de fallos (Chaos Mesh, Gremlin, Toxiproxy, o equivalente del stack).
- Un entorno no productivo con la misma topología que producción.

## Regla dura

- Nunca injertar un fallo sin una condición de aborto probada y sin blast radius acotado. La inyección sin control no es chaos engineering: es un incidente autoprovocado.
