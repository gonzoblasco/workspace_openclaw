# Ollama Cloud: plan legacy vs pricing por token

**Fecha:** 2026-09-16
**Estado:** decision tomada (quedarse en legacy), plan de contingencia registrado

## Contexto

- La cuenta Ollama Pro de Gonzo sigue en el pricing LEGACY: facturacion por GPU-time / quote mensual de uso de procesador (la barra % se monitorea semanalmente). No es por token.
- El 2026-08-31 Ollama lanzo el pricing transparente por token (blog "Transparent pricing"): Pro USD 20/mes con USD 60 de uso incluido por mes. Aplica solo a signups nuevos o upgrades voluntarios; los suscriptores legacy existentes siguen con el esquema viejo mientras auto-renueven.
- Regla dura: NO tocar billing settings. La FAQ oficial confirma que cambiar el ciclo (mensual<->anual) o el tier convierte la cuenta al pricing por token de forma automatica. Revertir requiere contacto con soporte y solo si habia suscripcion activa al momento del lanzamiento.

## Los dos medidores y sus modelos baratos

| Criterio | Modelo barato | Fuente |
|---|---|---|
| Por CPU (plan legacy) | deepseek-v4-flash (menor consumo por request medido 11/09: 1.631 requests, barra mas baja de los tres) | medicion interna |
| Por token (pricing nuevo) | deepseek-v4.1-flash (ver tabla de precios) | pagina oficial de precios |

## Precios por token oficiales (no-peak y peak 12-18 UTC)

| Modelo | Input | Cached | Output | Peak input | Peak output |
|---|---|---|---|---|---|
| deepseek-v4.1-flash | USD 0.15 | USD 0.003 | USD 0.60 | USD 0.30 | USD 1.20 |
| deepseek-v4-flash | USD 0.22 | USD 0.007 | USD 0.66 | USD 0.44 | USD 1.32 |

v4.1-flash: -32% input, -57% cached, -9% output vs v4-flash.

## Por que v4.1-flash es candidato a primary

Arquitectura CED (pagina oficial del modelo): 552B backbone, MoE multimodal, 8B activos en prefill / 16B en decode, KV cache 890 B/token (~1/4 del v4-flash). "Cuts costs significantly for agentic workloads that process a lot of input": patron exacto del pipeline A/B.

Benchmarks oficiales agentic (v4.1-flash vs v4-flash):
- Terminal-Bench 2.1: 90.6 vs 82.7
- DeepSWE v1.1: 74.2 vs 54.4
- CyberGym: 88.1 vs 76.7
- AutomationBench: 54.8 vs 37.7
- Agent's Last Exam: 31.8 vs 25.2
- Razonamiento parejo: GPQA 90.9 vs 89.9 | HLE 36.8 vs 37.8

## Correccion registrada (2026-09-16)

deepseek-v4-flash NO figura en la tabla de retiros oficial (docs cloud.mdx, verificado contra el source). El "v4 anunciado para dejar de existir" de la nota del 11/09 no se confirma con fuente oficial. Al contrario: v4-flash es hoy la alternativa recomendada para los retirados deepseek-v3.1, deepseek-v3.2 y cogito-2.1.

## Estimacion mensual en tokens (supuestos declarados)

- Volumen: ~19.5K requests/mes (extrapolacion de ~4.500 en la semana del 11/09).
- 5/8 del trafico en horario pico (12-18 UTC = 09-15 en Argentina; jornada de Gonzo 10-18).
- Precios blended de v4.1-flash: USD 0.244 in / USD 0.975 out.

| Escenario | Tokens/request | Costo/mes | vs pool USD 60 |
|---|---|---|---|
| Ligero | 2K in + 0.5K out | ~USD 19 | Sobra |
| Medio | 5K in + 1K out | ~USD 43 | Entra con margen |
| Pesado | 10K in + 2K out | ~USD 86 | Excede ~USD 26 (overage al mismo rate, sin bloqueo) |

Con caching de prompts de sistema (tipico en loops de agente), el escenario medio baja a ~USD 36-40.

Nota: es una estimacion, sin conteo real de tokens por request. Se afina con capturas de usage.

## Matriz de decision

| Criterio | Quedarse en legacy | Migrar a tokens |
|---|---|---|
| Costo hoy | Minimo (v4-flash barato en CPU) | Similar o mayor |
| Modelo optimo | v4-flash (medido) | v4.1-flash (precio + benchmarks) |
| Puerta de una via | - | Cambio tier/ciclo = conversion automatica; revertir solo via soporte |
| Disparador | Ninguno | La barra aprieta o el legacy muere |

## Decision y plan

1. HOY: quedarse en legacy. Primary `ollama-cloud/deepseek-v4-flash:0731`. No tocar billing.
2. PENDIENTE: re-medicion controlada de deepseek-v4.1-flash (release oficial; la medicion del 11/09 fue sobre la preview). Protocolo: A/B de un dia contra v4-flash, comparar barra por request. Si el release oficial consume parecido o menos, queda listo como primary para el dia del switch.
3. DISPARADORES DE MIGRACION: (a) retiro del pricing legacy, (b) dos semanas seguidas tocando ~90% de la barra, (c) decision de correr modelos pesados (kimi-k3, qwen3.5:397b) de forma sostenida.
4. EN LA MIGRACION: conversion via billing settings + primary a v4.1-flash (sin escalar a kimi-k3, no hace falta).
