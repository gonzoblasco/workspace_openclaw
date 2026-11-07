---
name: compatibility-testing
description: TODO: add description
metadata:
  owner: kanam-dev
  status: active
---
# compatibility-testing

Verificar que un cambio funciona en la matriz real de entornos objetivo: navegadores, motores, sistemas operativos y dispositivos, con evidencia por cada combinación.

## Pasos

1️⃣ **Definir la matriz de compatibilidad**  
   - Enumerar los entornos objetivo: navegadores y sus motores (Chromium, WebKit, Gecko), sistemas operativos y tipos de dispositivo (desktop, tablet, móvil).  
   - Justificar cada entrada por los usuarios reales o los requisitos del proyecto, no por "porque existe".  
   - Evidencia: `compat/matrix.md` con la lista de combinaciones y la justificación de cada una.

2️⃣ **Priorizar la matriz**  
   - Marcar cada combinación como soportada, degradada o fuera de alcance.  
   - Identificar los entornos de mayor tráfico o criticidad para correrlos primero.  
   - Evidencia: columna de prioridad y nivel de soporte en `compat/matrix.md`.

3️⃣ **Ejecutar la suite en cada entorno**  
   - Correr los tests funcionales y visuales en cada combinación priorizada, usando automation multi-motor (por ejemplo Playwright, Selenium Grid o el runner del proyecto).  
   - Capturar el resultado por entorno, incluyendo screenshot o artifact en caso de fallo.  
   - Evidencia: `compat/results/<entorno>.json` con estado y artifacts por test.

4️⃣ **Aislar las diferencias específicas de motor**  
   - Para cada fallo, confirmar la causa: ¿es del código del proyecto, del motor, o del test?  
   - Reproducir el fallo en el motor mínimo afectado y descartar falsos positivos del harness.  
   - Evidencia: `compat/findings.md` con fallo, motor afectado y causa aislada.

5️⃣ **Clasificar y decidir**  
   - Marcar cada diferencia como bug a corregir, limitación aceptada o incompatibilidad conocida documentada.  
   - Si es un bug, dejar el fix propuesto o el issue de seguimiento.  
   - Evidencia: tabla en `compat/findings.md` con clasificación y acción.

6️⃣ **Fijar la cobertura como gate**  
   - Incorporar al CI la matriz priorizada para que cada cambio se pruebe contra los entornos de mayor criticidad.  
   - Definir qué combinaciones bloquean el merge y cuáles solo advierten.  
   - Evidencia: configuración del pipeline y `compat/README.md` describiendo el gate de merge.

## Resultado esperado

- Una matriz de compatibilidad explícita, priorizada y justificada por los usuarios reales.
- Resultados por entorno con evidencia, no una afirmación genérica de "funciona".
- Diferencias específicas de motor aisladas y clasificadas como bug, limitación aceptada o incompatibilidad conocida.
- Un gate de CI que cubre los entornos críticos.

## Prerequisitos

- Automation multi-motor o multi-navegador disponible (Playwright, Selenium Grid, WebDriver por motor).
- Suite de tests funcionales y, si aplica, de regresión visual.

## Regla dura

- Nunca declarar compatibilidad sin haber ejecutado el entorno concreto. Que funcione en el navegador de desarrollo no dice nada sobre el resto de la matriz.
