---
name: "model-cata"
description: "Ritual para comparar modelos LLM del sistema con un mismo prompt pesado, rubrica de analisis critico y decision de motor/especialistas documentada en ADR. Cuando el motor genera CODIGO, se agrega cata de tests ejecutables (suite oculta, pass/fail objetivo)."
---

# Skill: model-cata - Comparacion formal de modelos LLM

**Trigger:** cuando haya que elegir o renovar el motor LLM del sistema (nueva generacion de modelos, sospecha de regresion del actual, o ciclo programado de re-cata).

## Precondiciones
- Acceso a los modelos a probar (misma via si es posible: todos cloud o todos locales)
- Presupuesto/creditos confirmados ANTES de arrancar (anotar el costo esperado de la cabana de pruebas)
- Prompt de cata preparado y congelado (ver Fase 1)

## Fase 1 - Prompt pesado (el discriminador)
Un prompt debil hace catas inutiles. Requisitos minimos (si falta alguno, mejorar el prompt antes que correr los modelos):
1. Multi-seccion: 5-7 decisiones con trade-offs explicitos obligatorios
2. Restricciones tecnicas reales del dominio (no teoricas)
3. Adaptacion a presupuesto (10x menos / 10x mas) pedida en cada seccion
4. Pregunta-trampa con respuesta operativa (ej: "como se decide autonomia sin revision humana") - los modelos debiles la esquivan y eso es dato
5. Mismo prompt VERBATIM para todos los modelos; registrar el nivel de razonamiento real de cada corrida (ojo: algunas vias no exponen knobs - GLM via Ollama corre con el default del servidor; documentar exactamente que se mando)

## Fase 2 - Corridas
- Una corrida por modelo como baseline; segundas pasadas solo si hay sospecha de varianza
- Truncado en la misma seccion en todos = limite de salida del modelo, no del prompt: anotarlo y analizar lo visible; pedir continuacion solo si la seccion faltante es critica
- Registrar: duracion, tokens, y (si existe) consumo real de la plataforma

## Fase 3 - Rubrica de analisis (por modelo)
1. **Decision central:** que eligio, con que trade-offs, y SI refuta el argumento MAS FUERTE en contra (si solo lo ignora, bandera amarilla)
2. **Precision verificable:** numeros concretos sin fuente = descalificador (los inventa para sonar preciso)
3. **Dominio:** ejemplos con conocimiento real (quirks, edge cases) > ejemplos sospechosamente perfectos
4. **Fidelidad al prompt:** respondio lo preguntado o esquivo (ej: pedir merges autonomos y recibir "siempre humano" = esquivo)
5. **Anclaje a lo real:** referencia a comportamiento real de agentes > teoria de libro
6. **Estructura vs sustancia:** la prolijidad no puntua; lo accionable si
7. **Hallazgos de razonamiento:** comparar niveles del mismo modelo (el nivel puede cambiar el JUICIO, no solo la prosa - ver K2.7 xhigh vs high)

## Fase 4 - Costo real
- Verificar precios en fuentes primarias (por 1M tokens, input/output)
- Medir ratio empirico de consumo si la plataforma lo da (ej: 1 request de K3 = 41 de GLM Flash, medido en Ollama)
- Decision por calidad-POR-COSTO; lo caro tiene que justificar su brecha con algo no reemplazable

## Fase 5 - Decision y documentacion (el output)
1. **Veredicto de roles:** motor (default), especialistas convocados, retirados - con por que de cada uno
2. **ADR de motor** con manual del modelo ganador (plantilla en docs/adr/ADR-041): decision + regla de parametros + ficha de capacidades VERIFICADA (fuentes + fecha de consulta) + reglas de uso + riesgos/mitigaciones + rollback + pendientes con fechas
3. **Purga del ecosistema en DOS capas:** lista estatica de provider + catalogo del picker (agents.defaults.models) explicito sin wildcards (los wildcards cuelan por descubrimiento dinamico) + fallback = el no-consumible (free, nunca auto)
4. **Nombres literales del proveedor en config:** cero rebranding sin permiso (regla de Gonzo, 2026-08-29)
5. **Docs sync:** TOOLS.md, MEMORY.md, CHANGELOG, daily + commit/push del workspace
6. **Follow-ups como todos fechados** (validacion en tareas reales, input visual, re-cata a 30 dias)

## Fase 6 - Cata de codigo: tests ejecutables (pass/fail objetivo)

**Cuando:** la decision de motor incluye calidad de CODIGO generado (no solo prosa). El prompt pesado mide razonamiento escrito; la suite oculta mide codigo que corre.

### Escalera L1-L5 (dificultad creciente, mismo lenguaje y harness para todos)
1. **L1 - Funcion pura:** string/number in/out, sin estado externo ni I/O.
2. **L2 - Bordes ocultos:** edge cases que el modelo no ve (clamp, signos duplicados, espacios tras signo, corte en no-digito).
3. **L3 - Algoritmo eficiente:** restriccion explicita en el prompt (ej: O(1) u O(n)); falla si entrega O(n^2).
4. **L4 - DP con reconstruccion:** no solo el valor optimo, el camino. Si solo devuelve el valor, no pasa.
5. **L5 - Parser desde cero:** gramatica sin librerias de parsing.

### Reglas del harness
- **Suite oculta:** los casos NO se muestran al modelo; el prompt pide solo la funcion. El harness corre la solucion.
- **VALIDACION OBLIGATORIA del test del test:** ANTES de medir ningun modelo, correr la suite contra una solucion de referencia correcta (escrita a mano o de fuente confiable) y exigir pass 100%. Si la referencia no pasa, el harness esta mal: medir seria basura. Leccion del duelo atoi (13/09): "no puede" siempre es "no puede con ESTE harness"; el harness importa tanto como el modelo.
- **Overhead fijo separado del throughput:** medir el cold start (primera request, incluye carga del runner y descarga del modelo) POR SEPARADO de las requests sucesivas. Mezclarlos infla el tiempo atribuible al modelo.
- **Caveat de replicas:** en Ollama Cloud u runners con replicas, la primera request puede caer en una replica fria y la siguiente en otra caliente. Repetir el cold start 2-3 veces y registrar el RANGO, no un punto unico.

### Registro
- Pass/fail por modelo y por nivel (tabla). Un modelo que resuelve L1-L3 pero no L5 es distinto de uno que falla en L2.
- Tiempo por request: cold vs warm en columnas separadas, nunca sumadas.
- Si el modelo NO entrega (timeout, error, archivo invalido): es un fallo de INFRAESTRUCTURA distinto de un fallo de codigo. Documentar cual era (OOM del runner vs logica incorrecta). El duelo atoi lo demostro: qwen 27b paso 24/24 con speculative off pero OOM como agente completo - no es lo mismo "no sabe" que "no puede" con la RAM disponible.

### Dato de referencia verificable
Duelo atoi 2026-09-13 (24 casos edge): deepseek-v4-flash:cloud PASS 24/24 a ciegas. qwen3.8:27b-mlx: con speculative decoding fallo (cache restore); con num_speculative=0 paso 24/24 via API directa; NO corrio como agente completo (OOM Metal, 24GB). Harness reusable: /tmp/test_atoi.py.

## Anti-patrones vistos con costos reales
- Razonamiento max/xhigh como lever de calidad: no lo fue en ninguna cata (filosofa o inventa); decisivo fue la familia del modelo
- "Por amor al arte" sin medir costo: termina en ratios 41x
- Quedarse con el pulido: cifra inventada > precision falsa
- Comparar niveles distintos como si fueran comparables (xhigh vs default mide juicios distintos, no el mismo modelo a igualdad)

## Check de verdad
Antes de cerrar: la config real (openclaw config get o leido del archivo) matchea la documentacion, el picker no lista retirados, el rollback esta documentado (backup), y el ADR referencia fuentes con fecha.
