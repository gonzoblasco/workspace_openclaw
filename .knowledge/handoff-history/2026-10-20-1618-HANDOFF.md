# HANDOFF - workspace_openclaw

**Fecha:** 2026-10-20 16:18 GMT-3
**Proyecto:** workspace_openclaw
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Sesion de la cata de minimax-m3.1-flash y su aplicacion como motor del CORE, con una correccion posterior pedida por Gonzo. (1) ALTA del modelo: pull verificado (428B, 1.000.000 ctx, tools+thinking+vision), tool calling probado en vivo (schema ls, argumentos JSON validos), agregado a models.providers.ollama.models con num_ctx 1000000, modelPolicy.allow de main y agents.defaults.models. Backup ~/.openclaw/openclaw.json.bak-20261020-1345-minimax-m31. (2) CATA formal: el pedido fue '5 prompts por agente' y lo converti en 5 CLASES DE ESTRES (canonico, ambiguo, premisa falsa, restriccion dura, fuera de rol) porque 5 variantes del caso feliz no discriminan. 8 roles x 5 clases = 40 prompts x 4 modelos (los otros 3 son la VARA, no el objetivo) = 160 corridas por POST /api/chat (nunca el CLI, que mezcla el thinking con el entregable), temperature 0, think low uniforme. (3) HALLAZGO CENTRAL: los 2 jueces ciegos fallaron la clase 'premisa falsa'. En main-C1, gpt-oss OBEDECIO la regla falsa declarada en el prompt y el juez le dio el mejor puntaje (6.0), mientras minimax detecto la contradiccion y freno (5.0). Detectado leyendo los artefactos, no el score. Al re-juzgar con la regla explicita, un juez la aplico y el otro no, asi que promediar los dos fabrica un ranking invertido. Clases C y E re-puntuadas A MANO celda por celda; los jueces ciegos quedaron para A, B y D. (4) RESULTADO (escala 0-10 corregida): deepseek 8.3 > minimax 7.6 (17 wins sobre 40, el doble que cualquiera) > gpt-oss 6.7 = gemma4 6.7. Por rol minimax gana main 8.9 vs 7.8 de deepseek (su mejor rol y el que mas importa); pierde ops (6.7 vs 8.2), critic (7.2 vs 9.1) y auditor (7.0 vs 8.4). En clase D (restriccion) minimax es el mejor de los 4 con 7.4. (5) FALLOS PROPIOS de minimax: espiral de thinking (7 de 40 celdas con 0 entrega y 44-56k caracteres de razonamiento; 6 recuperadas con num_predict x2, 1 irrecuperable en 3 intentos) y think:false NO apaga el razonamiento por API (medido 3 veces: 463/134/193 chars). (6) DECISION DE GONZO: aplicar minimax como default del CORE, sin K3 como juez (costo de recursos desmedido) y sin mirar el precio (gratis hasta el 22 a las 23.59). (7) APLICADO en las 4 fuentes que el ADR-090 exige que coincidan: openclaw.json, settings de memory.db, bloques managed de AGENTS.md y docs/SETUP.md, ADR-090 y ADR-102 nuevo. Gateway reiniciado y verificado: minimax figura como default y deepseek como fallback#1. (8) DRIFT corregido de paso: agents.defaults.model.primary decia nemotron-3-super:cloud, valor del benchmarking del 14/10 que fue propuesto y nunca adoptado y que la tabla del ADR-090 nunca declaro; config, DB y bloques estaban en tres valores distintos. (9) CORRECCION 15:55 a pedido de Gonzo: la seccion de costo del informe afirmaba una consecuencia economica sin medir el consumo, y el unico '20x' del workspace era de otra sesion y otro modelo (nemotron vs deepseek, memory/2026-10-05.md). Verificado que el '20x' no estaba en nada escrito en esta cata, pero que el dato estaba disponible desde el principio: eval_count (output tokens), verificado incluyendo el razonamiento (4,3-4,5 chars/token con content+thinking; 1,31 con content solo, imposible). MEDIDO: minimax/deepseek 3,89x output tokens (2,95x en las 33 celdas limpias), 5,5x latencia, 19,5x contra gpt-oss. Y el dato que mas pesa: las 7 celdas fallidas consumieron 110.260 output tokens = 294% de todo lo que consumio deepseek en 33 celdas limpias; el gasto de minimax esta dominado por su modo de fallo, no por su razonamiento normal. Informe, ADR-102, model-history, CHANGELOG y daily corregidos: la inferencia quedo reemplazada por el numero medido, y se dejo explicito que el precio por 1M sigue sin fuente primaria consultada. (10) COMMITS: 2244a9da1d (cambio de motor), 56bd9fa093 (handoff), 2379040d28 (costo medido), f54faa3274 (daily). Todos pusheados, CI verde. GATES: check-single-source, check-refs --all (544 rutas), check-bootstrap-budget (39.568/60.000), check-adr-integrity (57 ADRs), managed-blocks sin drift. (11) LEARNINGS registradas: id 275 (una objecion economica se contesta con el campo medido) y 276 (un score de juez es evidencia, no veredicto). (12) EVIDENCIA commiteada en docs/ecosystem/ (informe + bateria congelada); los 160 artefactos crudos quedan en playground/ fuera de git por politica, con prompt+content+thinking+eval_count separados por celda para poder reevaluarlos sin re-correr nada. No se toco memory/2026-10-19.md: son cambios sin commitear de otra sesion (hermes-agent).

## Estado actual

El CORE corre con minimax-m3.1-flash:cloud, con deepseek-v4.1-flash:cloud como fallback unico. Los otros 7 roles intactos. Config, DB, bloques managed y ADRs coinciden (managed-blocks check sin drift, check-single-source OK, check-adr-integrity 57 ADRs). El consumo MEDIDO de minimax es 3,89x output tokens contra deepseek (2,95x sin el sesgo del retry) y 5,5x en latencia; el gasto real esta dominado por su modo de fallo (7 celdas sin entrega consumieron 294% de lo que deepseek consumio en 33 celdas limpias), lo que el fallback cubre. El precio por 1M sigue sin fuente primaria consultada, pero Gonzo decidio que no es un factor (gratis hasta el 22/10 23:59).

## Proximos pasos

1) Cata de validacion en 2 semanas de uso real del CORE con minimax (corte 2026-11-03). 2) Reevaluar el balance de consumo si termina la gratuidad del modelo (2026-10-23): el ratio medido es 3,89x de output tokens y lo que falta es el precio por 1M, no una estimacion. 3) K3 como juez: CANCELADO por Gonzo; los 160 artefactos crudos quedan en playground/model-cata-2026-10-20/ con prompt+content+thinking+eval_count separados, por si se decide reevaluar sin re-correr nada. 4) memory/2026-10-19.md quedo con cambios sin commitear de otra sesion (hermes-agent): no se toco, no tocar. 5) Pendiente de metodo (no de esta sesion): la tool 'openclaw' fallo dos veces con 'prepared model runtime plugin generation was superseded', asi que los cambios de config se hicieron por edicion directa del openclaw.json + launchctl kickstart, con backup previo.

## Decisiones y contexto que no debe perderse

- ADR-102: el rol main (CORE) pasa a minimax-m3.1-flash:cloud por evidencia de cata (main 8.9 vs 7.8). Se eligio el CORE y no otro rol porque orquesta: su latencia no esta en una ruta critica con otro agente esperando, y los roles de generacion (dev, critic, studio) si la tienen, y alli minimax no supera al titular por margen que lo justifique. Riesgo aceptado: espiral de thinking, mitigada por el fallback. LECCION METODOLOGICA REUTILIZABLE 1: la evaluacion de comportamiento (obedecer o frenar ante una premisa falsa) no es una tarea de prosa; un juez LLM puede fallarla igual que el modelo evaluado, y promediar jueces que no aplican la regla fabrica un ranking invertido. Por eso las clases C y E se puntuan leyendo el artefacto. Un score de juez es evidencia, no veredicto. LECCION METODOLOGICA REUTILIZABLE 2: cuando una afirmacion economica es challenging, el numero esta en los registros: mirar el campo antes de pedir opinion o dejar un pendiente. Segunda leccion de la misma correccion: en esa seccion del daily el .md es la FUENTE y la DB se regenera desde el, asi que editar la DB directo se pierde en el reconcile siguiente.

## Archivos tocados

```
docs/learnings/README.md
docs/learnings/metodologia.md
docs/learnings/pipeline-agentes.md
memory/2026-10-19.md
memory/memory.db
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
