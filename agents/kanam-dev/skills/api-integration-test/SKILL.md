---
title: api-integration-test
description: TODO: add description
---
# api-integration-test

Verificar que los contratos entre servicios se cumplen de extremo a extremo, no solo en aislamiento: esquema, comportamiento y flujos multi-servicio.

## Pasos

1️⃣ **Fijar los contratos**  
   - Recolectar el contrato de cada API involucrada: spec OpenAPI, schema GraphQL, esquema de mensaje **o interfaces TypeScript públicas** del módulo (exportadas desde el código).  
   - Identificar los campos obligatorios, tipos, códigos de estado y errores esperados.  
   - Evidencia: `integration/contracts/` con la spec de cada servicio y el hash de la versión **o una copia de las interfaces TS relevantes**.

2️⃣ **Definir los casos de integración**  
   - Enumerar los flujos que cruzan servicios: llamada directa, cadena A→B→C, caso de error propagado.  
   - Cubrir happy path, entradas inválidas, timeout y servicio caído.  
   - Evidencia: `integration/cases.md` con el flujo, los servicios implicados y el resultado esperado.

3️⃣ **Levantar el entorno de integración**  
   - Arrancar las dependencias reales o sus dobles (testcontainers, contenedores, mocks de contrato con Pact).  
   - Sembrar datos de prueba reproducibles y aislar el estado entre corridas.  
   - Evidencia: `integration/env.md` con cómo se levanta el entorno y `integration/seed/` con los datos.

4️⃣ **Ejecutar y validar contra el contrato**  
   - Correr los casos y validar cada respuesta contra el esquema declarado (no solo el status code).  
   - Verificar el código de estado, la forma del cuerpo, y que los campos obligatorios estén presentes y tipados.  
   - Evidencia: `integration/results/<caso>.json` con request, response y resultado de la validación de esquema.

5️⃣ **Detectar rupturas de contrato**  
   - Comparar la spec actual contra la anterior para detectar breaking changes (campos removidos, tipos cambiados, requeridos nuevos).  
   - Marcar cada cambio como compatible o breaking.  
   - Evidencia: `integration/contract-diff.md` con el diff y su clasificación.

6️⃣ **Fijar el gate de integración**  
   - Incorporar la suite al CI para que corra contra cada servicio antes del merge.  
   - Definir qué casos bloquean el merge y cuáles solo advierten.  
   - Evidencia: configuración del pipeline y `integration/README.md` describiendo el gate.

## Resultado esperado

- Los contratos de cada API fijados y versionados.
- Casos de integración que cubren happy path, errores y fallos de servicio.
- Validación de respuesta contra el esquema, no solo contra el status code.
- Un diff de contrato que marca breaking changes antes del merge.
- Un gate de CI que corre la suite de integración.

## Prerequisitos

- Acceso a las specs de las APIs involucradas.
- Herramienta de contract testing o validación de esquema (Pact, OpenAPI Validator, Dredd, o el runner del proyecto).
- Entorno capaz de levantar las dependencias reales o sus dobles.

## Regla dura

- Nunca declarar que una integración funciona porque el test pasó un status 200: la respuesta debe validarse contra el esquema del contrato. Un 200 con cuerpo roto sigue siendo una ruptura.
