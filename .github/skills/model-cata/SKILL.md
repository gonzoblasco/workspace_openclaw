---
name: "model-cata"
description: "Ritual para comparar modelos LLM del sistema con un mismo prompt pesado, rubrica de analisis critico y decision de motor/especialistas documentada en ADR"
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

## Anti-patrones vistos con costos reales
- Razonamiento max/xhigh como lever de calidad: no lo fue en ninguna cata (filosofa o inventa); decisivo fue la familia del modelo
- "Por amor al arte" sin medir costo: termina en ratios 41x
- Quedarse con el pulido: cifra inventada > precision falsa
- Comparar niveles distintos como si fueran comparables (xhigh vs default mide juicios distintos, no el mismo modelo a igualdad)

## Check de verdad
Antes de cerrar: la config real (openclaw config get o leido del archivo) matchea la documentacion, el picker no lista retirados, el rollback esta documentado (backup), y el ADR referencia fuentes con fecha.
