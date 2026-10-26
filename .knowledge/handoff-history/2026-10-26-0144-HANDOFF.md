# HANDOFF - workspace

**Fecha:** 2026-10-26 01:44 GMT-3
**Proyecto:** workspace
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-10-26). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-10-26.md`.

---

## Que se hizo en esta sesion

Cata de beam:cloud (Reflection Beam 501B-A23B MoE, 1M ctx, nuevo en Ollama Cloud) que derivo en un cambio de pipeline: el A/B pasa a A/B/C con un tercer agente que escribe la red de tests de regresion, y la regla de que solo A toca el codigo de produccion. CONTEXTO: Gonzo pidio la cata de beam y despues la comparacion con MiniMax M3.1 Flash (nuestro motor del CORE, ADR-102). MEDICIONES: (1) Recall de revisores sobre el mismo artefacto con 4 bugs sembrados (ground truth en bench/GROUND_TRUTH.md): deepseek-v4.1-flash 4/4 con 9 hallazgos en 52s, minimax-m3.1-flash 4/4 con 10 en 180s, beam:cloud 3/4 con 3 en 17s y se auto-aprobo con un defecto vivo (el hit del cache devolvia la lista interna, contaminable). beam es 3,5x mas rapido pero es la velocidad de no mirar. (2) Eficiencia de razonamiento: beam 169 tokens de thinking vs 524 de minimax en el mismo puzzle (3,1x menos), 1,0s vs 4,7s. (3) Contexto largo: beam clavo el needle a 233k tokens donde minimax fallo con HTTP 500 a 140k y se comio un guion a 225k. (4) Triage: beam NO sirve - 1 request por tarea, igual que gemma4, pero 478 tokens de eval contra 18 (26x mas) con la misma accuracy 6/6. (5) Costo en requests: el 429 de Ollama Cloud es POR CUENTA, no por modelo - saturar beam hace fallar a minimax (28/40) y a deepseek (27/40); cambiar de modelo no abre presupuesto. Secuencial 30/30 OK, concurrencia 2-4 al 100%, 6 al 100%, a 20 en vuelo falla el 70%. (6) Pipeline ABC sobre 3 casos extremos (cache concurrente, bisiestos, token bucket): 3/3 verdes con 49+69+29 tests. Los bugs que cazaron B y no A fueron de invariantes que el spec declaraba explicitamente. (7) Rework (A corrige con el reporte de B): mismo recall 4/4 que B corrigiendo directo, pero cubre 7 de 9 findings, y el que se le escapo tampoco quedo como test - se perdio dos veces. (8) Cadena pura con B PROHIBIDO de editar produccion: B reporto 10 findings (mas que los 9 cuando editaba) y reports.py quedo intacto (md5 identico al sembrado); A corrigio 7 de los 10 y dejo 3 para C con el detalle de por que cada test original no aforcia nada; C refuerzo los 3 y agrego 29 tests de regresion: 43 tests verdes, 12 mutaciones, todas detectadas. DECISIONES: solo A toca el codigo de produccion; B reporta con evidencia ejecutable (probe_*.py) sin editar; C escribe la red de tests validada por mutacion; el rework vuelve a A con la condicion de que todo finding de B termine como un test de C. beam queda FUERA del pipeline (recall 3/4 como revisor, sin ahorro de requests como pre-filtro) y entra como modelo de contexto largo. GATES: 23/23 tests del gate, suite completa OK, check-single-source OK, check-adr-integrity (60 ADRs), CI remoto en verde (Skill Scripts CI, run 40255480475). Commits b09fd2fd55, 622f3c1e63, 3a9d34c736, b5ea553672, 416c7f7a1e, 5f3b794390, 66a1d0aa06. PENDIENTES: dos ambiguedades del spec sin resolver (borde del TTL: 'mas viejo que ttl_seconds' admite edad exactamente ttl y el codigo usa la ventana estricta; copia superficial del cache: copia la lista pero comparte los dicts internos) y el push pendiente de esta sesion.

## Estado actual

Pipeline A/B/C operativo: ADR-105 con el pacto de tres roles (A gpt-oss:120b-cloud escribe y corrige, B deepseek-v4.1-flash:cloud solo revisa, C minimax-m3.1-flash:cloud red de tests), ruta pipeline_abc en el router, setting model_pipeline_c, bloques pipeline-abc en AGENTS.md y model-pipeline-abc en SETUP.md (este ultimo estaba huerfano en el REGISTRY y nadie lo mantenia), skill de arbitraje actualizada, gate extendido que verifica los tres roles distintos entre si y con canon, 23 tests del gate que siembran cada defecto. El bench completo queda en bench/ con ground truth, seeder y verificador de recall, mas la cadena pura en bench/abc-puro/. beam:cloud NO entra al pipeline: queda como modelo de contexto largo. Todo commiteado; el push de esta sesion queda pendiente.

## Proximos pasos

1) Push del workspace: git pull --rebase antes de cada push (regla del ADR-073, una sola maquina) y esperar el CI en verde. 2) Decidir las dos ambiguedades del spec que quedaron visibles: el borde del TTL ('no devuelve un valor cacheado mas viejo que ttl_seconds' admite servir edad exactamente ttl; el codigo usa la ventana estricta 0 <= edad < ttl) y la copia superficial del cache (copia la lista pero comparte los dicts internos, asi que mutar resultado[0][amount] contamina el cache). 3) Si aparece un 429 de cuota, mirar primero que el limite es POR CUENTA: cambiar de modelo no abre presupuesto; mantener la concurrencia efectiva del pipeline en 2-6. 4) Probar el pipeline ABC sobre trabajo real (un ADR o un spec de un proyecto), no solo sobre el bench sintetico, y medir si la red de C atrapa defectos en codigo de verdad.

## Decisiones y contexto que no debe perderse

- El pipeline es A/B/C y el reparto de trabajo es una frontera, no una sugerencia: SOLO A toca el codigo de produccion. B es el profesor que devuelve el trabajo practico con las correcciones indicadas y la evidencia ejecutable (probe_*.py), no el que las aplica: medido, B encuentra MAS cuando no edita (10 findings vs 9) porque editarlo lo distrae de reportar. C escribe la red de regresion y la valida por mutacion. La REGLA DEL REWORK: cuando B reporta un defecto, A corrige el codigo y C testea el defecto - todo finding de B tiene que terminar como un test de C, porque sin eso el hallazgo se pierde dos veces (medido: el rework de A cubrio 7 de 9 findings y el que se le escapo tampoco estaba testteado, asi que sobrevivio a la suite completa). La asimetria se mantiene con tres modelos: A != B, B != C, A != C, verificado por el gate. C no es un revisor: su alcance es la red de regresion, no el juicio sobre el diseno. El slot B se decide por RECALL, no por velocidad: beam:cloud es 3,5x mas rapido y dio 3/4 recall con cero hallazgos extra y se auto-aprobo con un defecto vivo; deepseek y minimax dieron 4/4. UN DATO, UN DUENO: el ADR-105 es el dueno del pacto A/B/C y el bench/ es el dueno de la evidencia medida. La ruta pipeline_ab se conserva para trabajo donde la red de regresion no aporta (cambios mecanicos, docs, scripts de un solo uso). Y una leccion de metodo que se aplico contra mi propia sesion: un auto-reporte de subagente que declara 'todo verde' con 5 tests en rojo es PEOR que ningun reporte, y por eso el gate tiene que verificar el repo real, no la salida del agente.

## Archivos tocados

```
docs/CHANGELOG.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-10-26.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
