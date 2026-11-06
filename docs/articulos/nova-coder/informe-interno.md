# hf.co/ModernoTech/Nova-Coder:Q4_K_M — evaluacion interna

**Fecha:** 2026-11-05
**Veredicto:** NO ADOPTAR
**Uso recomendado:** ninguno como modelo general; evaluable como especialista solo para codigo Python aislado bajo supervision

## Ficha
| Campo | Valor | Fuente |
|---|---|---|
| Modelo | hf.co/ModernoTech/Nova-Coder:Q4_K_M | declarado |
| Contexto maximo | 163840 tokens | declarado |
| Contexto de corrida | 32768 tokens | medido |
| Quantizacion | Q4_K_M | declarado |
| think | false | medido |
| num_ctx efectivo | 32768 | medido |
| num_predict | null (sin limite) | medido |
| Temperatura | no especificada | NO_VERIFICABLE |
| Fecha evaluacion | 2026-11-05 | medido |

## Mediciones

| Prueba | Segundos | Tokens de salida |
|---|---|---|
| p1_funcion_simple | 22.94 s | 105 |
| p2_explicacion | 13.42 s | 88 |
| p3_debug | 16.41 s | 354 |
| p4_refactor | 22.38 s | 455 |
| p5_complejo | 33.46 s | 817 |
| p6_trampa | 62.29 s | 573 |
| p7_local | 14.80 s | 201 |

**Contexto:** 32768 tokens en la corrida; el modelo declara 163840. -131072 tokens (80% debajo de declarado)
- **Tasa CORRECTO:** 3/7 (42.8%)
- **Tasa FALSO:** 3/7 (42.8%)
- **Tasa INCOMPLETO:** 1/7 (14.2%)

Si no hay valor declarado, la celda va vacia. Nunca se completa con estimaciones.

## Prueba por prueba
| Prueba | Veredicto | Severidad |
|---|---|---|
| p1_funcion_simple | CORRECTO | ninguna |
| p2_explicacion | FALSO | media |
| p3_debug | CORRECTO | ninguna |
| p4_refactor | INCOMPLETO | media |
| p5_complejo | CORRECTO | ninguna |
| p6_trampa | FALSO | critica |
| p7_local | FALSO | alta |

### Evidencia citada, prueba por prueba

**p1_funcion_simple.** `def es_par(n): return n % 2 == 0`

**p2_explicacion.** `Un context manager en Python es una herramienta que permite definir cómo un objeto debe ser utilizado con la sentencia "with"` — 0 marcas rioplatenses, ignora instruccion de registro

**p3_debug.** `cantidad = i.get('cantidad', 0)  # Usamos 0 como valor por defecto`

**p4_refactor.** `return datetime.datetime.now()` sin `import datetime`; codigo no ejecutable tal cual

**p5_complejo.** `if len(result) != len(packages): return None` — deteccion de ciclo correcta

**p6_trampa.** `Con solo 3 servidores, no podrás formar una mayoría mayoría necesaria para seguir operando si uno de ellos falla` y `no deberías usar Raft o Paxos directamente`

**p7_local.** `Esto podría deberse a varios problemas, como que el servicio de la base de datos no esté corriendo, el puerto esté incorrecto, o haya problemas de red` — 127.0.0.1 no implica red

## Modo de falla dominante
`falso_seguro`: responde con confianza y contenido invertido

Justificar con la cuenta: 2 de 7 pruebas son `falso_seguro` puro (p6_trampa, p7_local) con severidad alta/critica; si se incluye p2_explicacion como confianza sin cumplir instruccion, 3 de 7 pruebas.

p6 es el caso definitorio: invierte la verdad tecnica (afirma que Raft/Paxos no toleran 1 fallo con 3 nodos cuando requieren mayoria de 2 y estan disenados exactamente para eso) y recomienda ZooKeeper como alternativa valida, con redaccion impecable.

## Riesgos
1. **Riesgo:** Desinformacion critica en sistemas distribuidos. p6 invierte quorum (3 nodos = mayoria 2). **Mitigacion:** sin mitigacion conocida en este modelo; bloquear uso para arquitectura/distribuidos.
2. **Riesgo:** Diagnostico local incorrecto. p7 diluye causa real (servicio no escuchando en puerto local) con `problemas de red` en loopback. **Mitigacion:** no usar para troubleshooting de infra; requiere validacion humana.
3. **Riesgo:** Codigo no ejecutable. p4 omite `import datetime`. **Mitigacion:** exigir ejecucion en sandbox antes de entregar.
4. **Riesgo:** Incumplimiento de instruccion de formato/registro. p2 ignora rioplatense explicito. **Mitigacion:** sin mitigacion conocida; no usar donde el registro sea requisito.
5. **Riesgo:** Correlacion inversa calidad-correccion: respuestas mas largas y seguras (p6: 573 tokens, 62.29 s; p5: 817 tokens) no predicen correccion. **Mitigacion:** no usar longitud/confianza como proxy de calidad.

## Configuracion recomendada
Modelo: `hf.co/ModernoTech/Nova-Coder:Q4_K_M`, think: `false`, num_ctx: `32768`, num_predict: `null`, temperatura: NO_VERIFICABLE.

No funciona bien con ninguna configuracion para uso general: 42.8% CORRECTO y 1 fallo critico en conocimiento factual. Como especialista de codigo Python simple (p1, p3, p5) funciona con la configuracion medida, siempre con ejecucion y revision posterior.

## Pendientes
- Medir con `think: true` y con temperatura explicita (0.0 / 0.2 / 0.7) para verificar si p6/p7 persisten.
- Medir latencia y tasa de acierto con contexto >32768 hasta 163840 declarado.
- Medir p4 con ejecucion real en interprete (verificar NameError por falta de import).
- Medir pruebas adicionales de sistemas distribuidos y networking local para confirmar sistematicidad de `falso_seguro`.
- Medir cumplimiento de instrucciones de registro con prompt rioplatense reforzado.
