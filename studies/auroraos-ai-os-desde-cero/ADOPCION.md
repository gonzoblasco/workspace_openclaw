# Adopción: forzar a la IA a escribir un sistema operativo (AuroraOS)

Fecha de revisión: 2026-11-11
Curso: [outline.md](outline.md) · [transcripcion.md](transcripcion.md)
Caso usado: `agents/kanam-planner/.knowledge/programs/` (los 6 programas del Planner en este workspace)

## Veredicto

**Adopción con un artefacto.**

El video no enseña sistemas operativos: es un caso de delegación. De todo lo que muestra,
una sola cosa muerde un defecto real de este workspace, y es la del Módulo 4: **el agente
avisó de un riesgo antes de empezar, el aviso se ignoró porque no era parte del contrato, y
el costo apareció en la primera ejecución.**

## Tabla de adopción

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| «Remember that warning I ignored? Yeah, it was right.» (02:46) — el aviso existía antes de escribir y se perdió porque no era un campo del pedido, era una frase | Los pasos de los programas del Planner tienen `exit_criteria`, `gate`, `write_paths` y `evidence`, pero **ningún campo de riesgo**. Medido el 2026-11-11: 0 de 6 programas y 0 de 64 pasos declaran `risks`; 13 de esos pasos están abiertos (ABYA YALA 6, Critic v0.3 7). `dispatch_contract.py` no incluye riesgos en el prompt de despacho | `check-dispatch-risk.py` — corrido abajo, **falla** contra el repo actual (13 pasos) |

## El artefacto, corrido

```console
$ python3 studies/auroraos-ai-os-desde-cero/check-dispatch-risk.py
VIOLACION: 13 defecto(s) en 13 paso(s) no completados
  - abya-yala-05.json: paso 1: no declara `risks` (ausente != vacio)
  - abya-yala-05.json: paso 2: no declara `risks` (ausente != vacio)
  - abya-yala-05.json: paso 3: no declara `risks` (ausente != vacio)
  - abya-yala-05.json: paso 4: no declara `risks` (ausente != vacio)
  - abya-yala-05.json: paso 5: no declara `risks` (ausente != vacio)
  - abya-yala-05.json: paso 6: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 6: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 7: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 8: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 9: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 10: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 11: no declara `risks` (ausente != vacio)
  - critic-v0.3.json: paso 12: no declara `risks` (ausente != vacio)
EXIT=1
```

Salida pegada de la corrida real del 2026-11-11 sobre el workspace, EXIT `1`.

## Prueba de que el gate falla de verdad

Un gate que solo se corrió en rojo no probó que pueda pasar. Los tres estados se probaron
contra un árbol de programas descartable:

```console
$ python3 check-dispatch-risk.py <tmp>     # 4 programas: uno vacío, uno sin falsified_by, uno completed, uno sin risks
VIOLACION: 2 defecto(s) en 3 paso(s) no completados
  - ausente.json: paso 0: no declara `risks` (ausente != vacio)
  - nosin-falsify.json: paso 0 riesgo 0: falta `falsified_by`
  - agents/kanam-planner/scripts/dispatch_contract.py: el contrato de despacho no incluye riesgos
EXIT=1

$ # corrigiendo el contrato de despacho
APLICA: 1 paso(s) no completados declaran y propagan su riesgo
EXIT=0

$ # sin programas
NO-CORRIDO: no hay programas en <tmp>/agents/kanam-planner/.knowledge/programs
EXIT=2
```

Los tres códigos son distintos a propósito (regla de `verification-gates`): **cero casos
corridos no es verde**. Un `0` silencioso sobre una carpeta vacía es la peor forma de APLICA.

## Por qué el defecto es real y no teórico

En el video, el aviso de arquitectura viajó por **la conversación** (01:58, 02:07) y no por el
contrato. Cuando el humano volvió a mirar, veinte minutos y 6.000 líneas después, el dato ya
no estaba en el artefacto que se iba a ejecutar.

En el workspace la estructura es igual de frágil, pero medible:

1. Un paso del programa tiene `exit_criteria` — qué tiene que ser verdad al terminar.
2. No tiene `risks` — qué tiene que ser verdad para poder empezar.
3. `dispatch_contract.py` arma el prompt del agente con el primero y no con el segundo.
4. Si el supuesto se rompe a mitad de la tarea, el agente descubre solo el costo, como en el
   video, y el CORE se entera del fracaso en el auto-reporte.

El caso `reinos-de-la-frontera` lo muestra en carne propia: sus 24 pasos declarados sin una
línea de riesgo, y un supuesto tácito del proyecto (**caballería** sin modelo montado resuelto)
ya está anotado en el daily como problema de E3 — fuera del programa que lo va a ejecutar. Hoy
ese programa no tiene pasos abiertos, así que el gate no lo marca; la falta de campo sigue ahí
para el próximo paso que se agregue.

## Cómo se cierra

El gate pasa a verde cuando:

1. Cada paso no completado declara `risks`, o un `[]` explícito que signifique «evaluado, ninguno».
2. Cada riesgo trae `assumption` y `falsified_by` — sin forma de falsarse, no es riesgo, es preocupación.
3. `dispatch_contract.py` imprime los riesgos en el prompt que recibe el ejecutor.

Los tres son cambios en el Planner, no en este estudio. **No se aplican acá por la frontera de
roles (ADR-083):** gobernar el Planner es del CORE, implementarlo es de otra sesión con el
contrato de `planner-delegation`.

## Descartados (y por qué)

- **Escribir el prompt con cinco decisiones cerradas** (Módulo 1): `planner-delegation` ya impone una plantilla con objetivo, contexto, alcance, gates y entregable. No hay hueco que llenar.
- **Siete fases con boot después de cada una** (Módulo 2): los programas del Planner ya tienen pasos atómicos con `exit_criteria` verificable. La idea es la misma; el artefacto ya existe.
- **"No se puede" leído como propuesta de alcance** (Módulo 6): es buena práctica de conversación, pero no se convirtió en un artefacto que pueda fallar. Sin gate, queda como nota.
- **Ponerse nota con defectos al lado** (Módulo 7): el reporte de cierre ya exige la tabla de lo que se verificó y lo que no. Cobertura: `skills/verification-gates` + `session-lifecycle`.
- **QEMU / VirtualBox / kernel en C** (todo el resto): no aplica. Este workspace no compila sistemas operativos.

## Lo que sigue pendiente

El artefacto quedó **en rojo**, y eso registra el defecto real: 13 pasos listos para delegarse
sin un solo riesgo declarado. Se cierra cuando el Planner adopte el campo, no cuando el script
cambie. Si se toca el script para que pase, el gate estaba midiendo su propia forma.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
