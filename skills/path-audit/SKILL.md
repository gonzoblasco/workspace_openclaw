---
name: "path-audit"
metadata:
  category: "Governance"
  tags:
    - auditoria
    - rumbo
    - version
    - status
    - kimi
description: "Auditoria de CAMINO (no de codigo) sobre un proyecto: dice si va por buen rumbo, cual es el proximo paso y que afirmaciones del STATUS no estan probadas. Se dispara por HITO DE VERSION (0.1, 0.5, 1.0) y antes de decisiones de producto, no por calendario."
user-invocable: true
---

# Skill: path-audit - Auditoria de camino

> **Que audita:** el **rumbo**, no el codigo. No lee la implementacion: lee lo que el equipo
> **afirma** sobre ella. Su valor es detectar el falso verde de direccion - el proyecto que se
> siente sano porque su propio STATUS lo dice.

## Trigger: cada MINOR release (regla de Gonzo, 2026-11-04)

Se corre **en cada bump minor**: 0.1 → 0.2 → 0.3 → ... → 0.6 → 1.0. Sin excepciones, sin
"hitos selectos". El owner acepta el costo: *un request de K3 por minor release es un costo que
estoy dispuesto a pagar*, y la primera vez que lo usó encontró mejoras que se le habían pasado.

| Disparador | Cuando |
|---|---|
| **Minor release** | **cada** bump minor: `0.1`, `0.2`, `0.3`, `0.4`, `0.5`, `0.6`, … `1.0` |
| **Antes de una decision de producto** | deploy, precio, pivot, publicar |
| **Etapa nueva** | cambio de fase (F1→F2, S3→S4, discovery→build) |
| A pedido | Gonzo dice "auditemos como viene" |

**NO se dispara:** en cada commit, ni en **patches y fixes** (`0.0.1` → `0.0.2`, `0.1.1` → `0.1.2`).
Un `0.0.x` de puro fix no genera hito.

> **Costo asumido:** ~1 request de `kimi-k3.1-pro` por minor. Medido: 4,7% de una sesion por request.
> Con un minor cada varios dias, es despreciable; y el valor es alto porque agarra el desvio de
> rumbo cuando todavia hay margen para corregirlo.

## Deteccion del hito (leer lo que haya, no imponer formato)

Los `STATUS.md` no comparten formato. Leer el primero que exista, en este orden:

```bash
grep -m1 -E '^\*\*(Version|Versión|Ciclo|Etapa actual|State):' projects/<slug>/.knowledge/STATUS.md
```

Ejemplos reales: `**Version:** 0.1.0` (preflight), `**Ciclo:** 0.0.1 **CERRADO**` (kanam-fixer),
`**Etapa actual:** F1-F4 implementadas` (oss-post-graph).

**El numero de version es el que decide.** Si un proyecto no declara version, usar la etapa.
La comparacion es **minor a minor**: `0.1.0` y `0.1.7` son el mismo hito (no re-auditar);
`0.1.x` → `0.2.0` si es un hito nuevo.

## Input (lo que lee)

1. `.knowledge/STATUS.md` - el estado declarado
2. `.knowledge/HANDOFF.md` - el traspaso
3. `git log --oneline -20` - que **ocurrio** de verdad
4. `.knowledge/AUDIT.md` anterior, si existe - para no repetir hallazgos ya cerrados

**NO lee:** el codigo fuente. Si necesita el codigo para responder, la pregunta era de
`verification-gates`, no de esta skill.

## Modelo

`sessions_spawn(agentId: "kanam-mind", model: "ollama/kimi-k3.1-pro:cloud")`

Kimi K3.1 Pro: 1 request = **4,7% de una sesion** (medido 2026-11-04). Justificado solo porque
corre pocas veces al año (uno por hito). **Nunca** en pipeline ni por turno.

## La pregunta central: afirmaciones no probadas

Esta es la parte que distingue la skill de un resumen. El modelo debe listar, para cada
afirmacion fuerte del STATUS, **si la evidencia es independiente o circular**.

Casos que SIEMPRE son sospechosos:

| Patron en el STATUS | Por que es circular |
|---|---|
| "self-audit: 100/100" | el mismo motor se evalua a si mismo |
| "N tests en verde" sin el comando | ausencia de reproduccion |
| "0 regressions" re-escaneado con la misma herramienta | la herramienta no puede ver lo que no ve |
| "verified" sin decir por quien | auto-reporte disfrazado |
| "95% de hallazgos cerrados" | cerrados **segun el que los definio** |

**Caso testigo (PreFlight, 2026-10-28):** el STATUS decia *"Self-audit: own landing 100/100 A"*
y *"95.8% of findings closed, 0 regressions"*. Las dos son verificacion circular: el mismo engine
que detecta define y mide. La auditoria lo marco, y ademas encontro que el SSRF guard solo probaba
los casos listados (no DNS rebinding, redirects, IPv6 exoticas).

## Output obligatorio: `.knowledge/AUDIT.md`

```markdown
# AUDIT - <slug> @ v<version>
**Fecha:** YYYY-MM-DD
**Version auditada:** x.y.z
**Modelo:** kimi-k3.1-pro:cloud
**Veredicto:** EN CAMINO | EN CAMINO CON RESERVAS | FUERA DE CURSO

## 1. Veredicto y por que
(3-5 lineas. Si es "en camino", decir en que direccion.)

## 2. Proximo paso real
(uno solo, accionable. No una lista de deseos.)

## 3. Afirmaciones NO probadas
| Afirmacion del STATUS | Por que no esta probada | Como se probaria |
|---|---|---|

## 4. Riesgo principal
(el que puede costar mas caro si no se atiende)

## 5. Hallazgos previos
(que se cerro desde el AUDIT anterior; que se repite - si se repite, escalar)
```

## Reglas duras

- **No escribe codigo. No toca el repo.** Su unico write es `.knowledge/AUDIT.md`.
- **No propone features nuevas.** Si el proximo paso es "construir mas", la auditoria fallo:
  revisar el punto 3 del STATUS.
- **No opina de estilo.** Opina de direccion.
- **Si el veredicto es positivo, lo dice.** Una auditoria que siempre encuentra problemas es
  tan inutil como una que nunca los encuentra.
- **Un hallazgo repetido se escala**, no se re-lista: si algo del AUDIT anterior sigue abierto,
  va en §5 marcado como **pendiente de hito anterior**.

## Como seguir el hito (para Gonzo)

Despues de cada audit, anotar en el STATUS:

```markdown
**Ultima auditoria:** v0.6 - 2026-11-04 - EN CAMINO CON RESERVAS (ver `.knowledge/AUDIT.md`)
```

Asi el proximo minor (0.7) sabe contra que comparar. El AUDIT.md se **sobrescribe** cada vez, pero
§5 conserva los pendientes del anterior: un hallazgo que se repite dos minor seguidos se escala.

