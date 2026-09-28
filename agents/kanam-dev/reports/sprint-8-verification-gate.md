# Sprint 8 - Gate de verificacion de tareas delegadas (reporte backfill)

Fecha del trabajo: 2026-09-28
Ejecutado por: sub-agent de `kanam-dev`; **reescrito y endurecido por el agente padre**
tras el code review adversarial.

## El problema que resuelve

Un sub-agent puede cerrar con `status=done` habiendo producido otra cosa o nada. El runtime
valida que el proceso termino limpio, no que el resultado sea cierto.

Medido el mismo dia, tres veces:

| Reportado | Real en disco |
|---|---|
| "43 specs importados" | 83 |
| "9 skills, 9 sub-agents, 9 paginas wiki" | 0, 0, 1 archivo ajeno al repo |
| OPS: evidencia JSON | campos inventados, 2 jobs dados por fallidos que estaban `ok` |

El gate convierte "el hijo dijo que lo hizo" en una condicion binaria sobre el disco.

## Entregable

`scripts/verify-delegation.sh` + `scripts/test-verify-delegation.sh`

```
Uso: bash scripts/verify-delegation.sh <patron> <conteo_esperado> [comando_extra]

Codigos de salida:
  0 - el criterio se cumple
  1 - el criterio falla (conteo distinto, o comando extra fallo)
  3 - no se pudo correr (cero artefactos, o patron inutilizable)
```

**Regla dura: cero artefactos nunca es un pase.** Un check que no corrio nada no puede
reportar exito.

## Lo que encontro el code review adversarial

El primer entregable del sub-agent tenia tres formas de evadirse, y ninguna estaba cubierta
por su propia suite:

| Evasion | Como se manifestaba | Estado |
|---|---|---|
| Patron con forma de path (`sub/*.md`) | `find -name` matchea basenames, asi que un patron con path **no matchea nada** y se leia como "cero artefactos" | rechazado con exit 3 |
| Patron universal (`*`) | satisfacia **cualquier** conteo esperado; verificaba nada | rechazado con exit 3 |
| cwd distinto | el script busca desde `.`, y el cwd no se declaraba | documentado: la busqueda es desde el cwd |

Ademas, la suite original tenia `set -e`, y **se auto-abortaba en el primer test que esperaba
un exit distinto de cero**. El "output" que el sub-agent entrego era una corrida cortada en
el test 2 de 5.

## Verificacion

| Criterio | Comando | Resultado |
|---|---|---|
| Script ejecutable | `test -x scripts/verify-delegation.sh` | si |
| Sintaxis | `bash -n` en ambos | ok |
| Suite interna | `bash scripts/test-verify-delegation.sh` | 8/8, exit 0 |
| Suite bats | `npx bats tests/bash/verify-delegation.bats` | 8/8 ok |
| Guiones largos | scan U+2014/U+2013 | 0 |

## El gate ya no es huerfano

El entregable original era un script que **nadie corria**. Ahora vive tambien en
`tests/bash/verify-delegation.bats`, y el pre-commit hook ejecuta `npx bats tests/bash`
cada vez que cambian `skills/` o `scripts/`. El gate esta enganchado al flujo real.

## Pendiente

- El gate verifica **conteos relativos al cwd**. No verifica contenido ni fidelidad. Para eso
  hace falta pasar el `comando_extra` (por ejemplo un `diff` contra el origen).
