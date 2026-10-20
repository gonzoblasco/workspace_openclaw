# HANDOFF - workspace

**Fecha:** 2026-10-20 15:41 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-20). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-20.md`.

---

## Que se hizo en esta sesion

Sesion de la cata de minimax-m3.1-flash y su aplicacion como motor del CORE. (1) ALTA del modelo en OpenClaw: pull verificado (428B, 1.000.000 ctx, tools+thinking+vision), agregado a models.providers.ollama.models con num_ctx 1000000, modelPolicy.allow de main y agents.defaults.models; tool calling probado en vivo (schema ls, argumentos JSON validos); backup ~/.openclaw/openclaw.json.bak-20261020-1345-minimax-m31. (2) CATA formal: el pedido fue '5 prompts por agente' y lo converti en 5 CLASES DE ESTRES (canonico, ambiguo, premisa falsa, restriccion dura, fuera de rol) porque 5 variantes del caso feliz no discriminan. 8 roles x 5 clases = 40 prompts x 4 modelos = 160 corridas por POST /api/chat (nunca el CLI, que mezcla el thinking con el entregable), temperature 0, think low uniforme. (3) HALLAZGO CENTRAL: los 2 jueces ciegos fallaron la clase 'premisa falsa'. En main-C1, gpt-oss obedecio la regla falsa declarada en el prompt y el juez le dio el mejor puntaje (6.0), mientras minimax detecto la contradiccion y freno (5.0). Se detecto leyendo los artefactos, no el score. Las clases C y E se re-puntuaron A MANO celda por celda; los jueces ciegos quedaron para A, B y D. (4) RESULTADO (escala 0-10 corregida): deepseek 8.3, minimax 7.6 con 17 wins sobre 40, gpt-oss 6.7, gemma4 6.7. Por rol, minimax gana main 8.9 contra 7.8 de deepseek (su mejor rol y el que mas importa) y pierde ops (6.7 vs 8.2), critic (7.2 vs 9.1) y auditor (7.0 vs 8.4). En clase D (restriccion dura) minimax es el mejor de los 4 con 7.4. (5) FALLOS PROPIOS de minimax: espiral de thinking (7 de 40 celdas con 0 entrega y 44-56k caracteres de razonamiento; 6 recuperadas con num_predict x2, 1 irrecuperable en 3 intentos) y think:false NO apaga el razonamiento por API (medido 3 veces: 463/134/193 caracteres). Latencia 35x el mas rapido. (6) DECISION DE GONZO: aplicar minimax como default del CORE, sin K3 como juez (costo de recursos desmedido) y sin mirar el precio (gratis hasta el 22 a las 23.59). (7) APLICADO en las 4 fuentes que el ADR-090 exige que coincidan: openclaw.json, settings de memory.db, bloques managed de AGENTS.md y docs/SETUP.md, ADR-090 y ADR-102 nuevo. Gateway reiniciado y verificado: minimax figura como default y deepseek como fallback#1. (8) DRIFT corregido de paso: agents.defaults.model.primary decia nemotron-3-super:cloud, valor del benchmarking del 14/10 que fue propuesto y nunca adoptado y que la tabla del ADR-090 nunca declaro; config, DB y bloques estaban en tres valores distintos. (9) Commit 2244a9da1d.

## Estado actual

El CORE corre con minimax-m3.1-flash:cloud, con deepseek-v4.1-flash:cloud como fallback unico. Los demos 7 roles intactos. Config, DB, bloques managed y ADRs coinciden (managed-blocks check sin drift, check-single-source OK, check-adr-integrity 57 ADRs). Riesgo vivo conocido: la espiral de thinking de minimax (7 de 40 celdas sin entrega en la primera pasada), que en el CORE se cubre con el fallback.

## Proximos pasos

1) Cata de validacion en 2 semanas de uso real del CORE con minimax (corte 2026-11-03). 2) Reevaluar el balance si termina la gratuidad del modelo (2026-10-23). 3) K3 como juez: CANCELADO por Gonzo; los 160 artefactos crudos quedan en playground/model-cata-2026-10-20/ con prompt+content+thinking separados, por si se decide reevaluar sin re-correr nada. 4) memory/2026-10-19.md quedo con cambios sin commitear de otra sesion (hermes-agent): no se toco, no tocar.

## Decisiones y contexto que no debe perderse

- ADR-102: el rol main (CORE) pasa a minimax-m3.1-flash:cloud por evidencia de cata (main 8.9 vs 7.8). Se eligio el CORE y no otro rol porque orquesta: su latencia no esta en una ruta critica con otro agente esperando, y los roles de generacion (dev, critic, studio) si la tienen, y alli minimax no supera al titular por margen que lo justifique. Riesgo aceptado: espiral de thinking, mitigada por el fallback. LECCION METODOLOGICA REUTILIZABLE: la evaluacion de comportamiento (obedecer o frenar ante una premisa falsa) no es una tarea de prosa; un juez LLM puede fallarla igual que el modelo evaluado, y promediar jueces que no aplican la regla fabrica un ranking invertido. Por eso las clases C y E se puntuan leyendo el artefacto. Un score de juez es evidencia, no veredicto.

## Archivos tocados

```
openclaw.json (fuera del repo), memory/memory.db, AGENTS.md, docs/SETUP.md, docs/CHANGELOG.md, docs/adr/ADR-090-pensamiento-nivel-configuracion.md, docs/adr/ADR-102-minimax-m31-flash-motor-core.md, docs/adr/README.md, docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md, docs/ecosystem/cata-minimax-m31-flash-2026-10-20-battery.py, memory/model-history.md, memory/2026-10-20.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-20.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
