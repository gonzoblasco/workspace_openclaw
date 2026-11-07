---
name: "kanam-dev-surface"
description: "Use when a code task should run through the Kanam DEV pipeline: intake, template selection, station execution, verification and handoff. Covers the kanam-dev dispatcher, the six bin scripts, their exit codes and when to skip a station."
metadata:
  owner: kanam-dev
  status: active
---

# Skill: kanam-dev-surface

## Goal

Invocar el pipeline de Kanam DEV con costo bajo y sin perder rigor: un intake
que falla antes de leer codigo, una plantilla que decide que estaciones aplican,
y un handoff que no cierra sin evidencia.

Sin esta skill, cada tarea arranca con "leete el brief, el SPEC y el repo", que
es exactamente el costo que el pipeline existe para bajar.

## Cuando usarla

- Cualquier pedido de ingenieria con alcance cerrado (cambio, fix, feature, docs,
  auditoria).
- Cuando el pedido llega ambiguo y hace falta descubrir los datos faltantes
  **antes** de tocar codigo.
- Cuando hay que cerrar un trabajo y el reporte necesita separar verificado de
  inferido.

No usarla para: preguntas de una linea, lectura de codigo para responder algo, o
trabajo exploratorio sin artefacto esperado.

## Las piezas

| Pieza | Comando | Que hace |
|---|---|---|
| S1 intake | `bin/intake.py --file pedido.md` | Extrae los 5 campos y elige plantilla |
| Despachador | `bin/kanam-dev <sub>` | `audit`, `a11y`, `review`, `docs`, `handoff`, `status`, `intake`, `help` |
| S3/S4 slice+commit | `bin/slice_commit.py <dir>` | Working tree sucio a commits atomicos (dry run por defecto) |
| S5 docs verify | `bin/docs_sync.py <dir> --check` | Detecta docs que contradicen el repo |
| S7 handoff | `bin/handoff_gate.py handoff.json` | Rechaza handoffs incompletos o contradictorios |
| Runner | `bin/runner.py --intake intake.json` | Encadena estaciones segun plantilla |

## Los cinco campos del intake

S1 no inventa ninguno. Si falta uno, exit 1 y el pipeline no arranca.

```
Objetivo: <que hay que lograr, en una frase>
Artefacto: <ruta exacta esperada>
Verificacion: <comando que prueba que esta hecho>
Convenciones: <repo, stack>
Aprobacion: <que se puede tocar y que no>
```

Por que bloquea: un pedido sin `verificacion` no tiene criterio de terminado. Un
pedido sin `aprobacion` no tiene limite. Descubrirlo despues de escribir codigo
es el desperdicio que la estacion existe para evitar.

## Plantillas

`hotfix`, `task`, `feature`, `audit`, `docs`. La matriz completa esta en
`PIPELINE-CONTRACTS.md` seccion 3.

Regla practica de eleccion:

| Si el pedido... | Plantilla |
|---|---|
| arregla algo puntual, urgente, con alcance chico declarado | `hotfix` |
| cambia algo existente sin agregar capacidad nueva | `task` |
| agrega o implementa algo nuevo | `feature` |
| solo mide, audita o diagnostica, sin cambiar codigo | `audit` |
| solo toca documentacion | `docs` |

Ambiguedad resuelve a `task`, nunca a `hotfix`. El default honesto es el rigor.

## Exit codes (identicos en todas las piezas)

```
0  verde / sin hallazgos
1  hallazgos (el pipeline no avanza)
2  no se pudo medir (herramienta ausente, ruta invalida, entorno roto)
```

**Un 2 nunca es verde.** Es la regla que evita el "corrí los tests y quedó
verde" cuando en realidad pytest no existía.

## Flujo tipico

```bash
cd ~/.openclaw/workspace/agents/kanam-dev

# 1. El pedido se convierte en intake. Si falta algo, falla aca.
./bin/intake.py --file pedido.md --out /tmp/intake.json

# 2. Opcional: ver el plan antes de correrlo.
./bin/runner.py --intake /tmp/intake.json --dir /ruta/repo --dry-run

# 3. Correr las estaciones de la plantilla.
./bin/runner.py --intake /tmp/intake.json --dir /ruta/repo --out /tmp/run.json

# 4. Verificar docs (si el trabajo toco documentacion).
./bin/kanam-dev docs /ruta/repo --check

# 5. Cerrar: el handoff no pasa sin evidencia.
./bin/kanam-dev handoff --template > /tmp/handoff.json   # veredicto va a stderr
./bin/kanam-dev handoff /tmp/handoff.json
```

## Reglas que no se negocian

1. **Verify ejecutado, no afirmado.** Un `verificado` sin la salida del comando es
   invalido. El handoff gate lo rechaza.
2. **Un comando con exit distinto de 0 no verifica.** Va a `inferred` o a
   `openDecisions`, nunca a `verified`.
3. **Estacion salteada se registra con motivo.** `skipped[]` sin razon es un
   olvido disfrazado.
4. **Datos locales intocables.** `.env`, `*.db`, `.venv`, `node_modules`: bloquean
   cualquier plan de commits.
5. **`status: completo` con decisiones abiertas** es contradictorio y se rechaza.
6. **Sin guiones largos: NO es gate.** Retirado por decision del dueno. El script
   `check_em_dash.py` sigue existiendo como criterio de estilo opcional.

## Errores que ya se cometieron y esta skill previene

| Error | Como se detecto |
|---|---|
| Clasificar "correr el pipeline" como `feature` | Corrida real sobre preflight |
| Poner el exit 1 de un comando en `verified` | El handoff gate lo rechazo contra su autor |
| Template de handoff que el propio gate rechaza | Test `test_template_is_itself_valid` |
| `npm test --silent` oculta el conteo que hay que leer | Corrida real sobre kanam-fixer |
| Extractor de docs con 8 falsos positivos | Primera corrida sobre kanam-fixer |

El patron comun: los fixtures daban verde y la realidad no. Probar contra un repo
real, no solo contra un fixture.

## Verificacion de la superficie

```bash
cd ~/.openclaw/workspace/agents/kanam-dev
for t in test_intake test_kanam_dev test_slice_commit test_docs_sync test_handoff_gate test_runner; do
  python3 bin/$t.py 2>&1 | tail -1
done
```

134 tests, 0 fail. Si esa cifra baja sin que alguien haya borrado tests, algo se
rompio.

## Archivos

- `bin/kanam-dev` - despachador
- `bin/intake.py` - S1
- `bin/runner.py` - encadenador
- `bin/slice_commit.py` - S3/S4 salida
- `bin/docs_sync.py` - S5 docs
- `bin/handoff_gate.py` - S7
- `PIPELINE-CONTRACTS.md` - contrato completo
- `ROADMAP-demand.md` - porque existe esta superficie
