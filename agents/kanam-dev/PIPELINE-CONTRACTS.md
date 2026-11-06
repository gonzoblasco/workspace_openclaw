# PIPELINE-CONTRACTS - Kanam DEV

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

Contrato de plantillas y estaciones para tareas de ingenieria. Documento de
diseño: define el "que" una vez; F0 y F5 solo lo implementan.

Estado: borrador para aprobacion de Gonzo. Fecha: 2026-11-06.
Reemplaza la eleccion rigida de "un pipeline para todo" por **plantillas por tipo
de tarea**.

## 0. Correccion de un supuesto previo

En la conversacion dije que "guiones largos: bloqueante en todas". **El dueño
corrigio: esa regla ya se quito de AGENTS.md y ya no es traba.**

Verificado: `agents/kanam-dev/AGENTS.md` no contiene ninguna regla de guiones
largos. El script `scripts/check_em_dash.py` sigue existiendo y sigue siendo util
como criterio de estilo, pero **no es un gate del pipeline** ni lo sera salvo que
Gonzo lo reponga explicitamente. Queda registrado aca para que no vuelva por
inercia.

## 1. Principio

Una plantilla no es una lista de pasos: es **que gates son obligatorios para ese
tipo de tarea**. La perfeccion no es "todas las estaciones siempre"; es "ninguna
estacion que aplique se saltea, y ninguna estacion salteada queda sin registrar".

Tres niveles de obligatoriedad:

| Nivel | Significado | Efecto |
|---|---|---|
| **Bloqueante** | Si falla, no se avanza. | Exit 1 (hallazgo) o 2 (no se pudo medir) detiene el pipeline. |
| **Declarativo** | Si no se ejecuta, se declara y se funda. | El handoff exige el campo `skipped[]` con estacion + motivo. Sin campo, el handoff es invalido. |
| **No aplica** | La estacion no corre por plantilla. | El pipeline lo registra como `skipped-by-template`, distinto de olvido. |

La diferencia entre **Declarativo** y **No aplica** es la que sostiene la
honestidad del sistema: un gate salteado queda escrito, no desaparecido.

## 2. Estaciones

Siete estaciones, cada una con contrato de entrada, salida y exit code.

### S1 `intake`
- **Entrada**: pedido en prosa.
- **Salida**: `intake.json` con los 5 campos minimos: `objetivo`, `artefacto`
  (ruta exacta esperada), `verificacion` (comando que prueba el resultado),
  `convenciones` (repo + stack), `aprobacion` (que se puede tocar y que no).
- **Exit**: 0 completo; 1 falta algun campo (nombra cuales); 2 no se pudo leer el
  pedido.
- **Nota**: esta estacion es la que mas tiempo ahorra. Si falta un campo, el
  pipeline no avanza y no me hace leer codigo para descubrirlo despues.

### S2 `discovery`
- **Entrada**: `intake.json`.
- **Salida**: `discovery.md` con lo que existe hoy, evidenciado (archivo:linea).
- **Exit**: 0; 2 si el artefacto declarado en intake no existe (contradiccion entre
  el pedido y el repo, no es un fallo del pedido: es hallazgo).

### S3 `slice`
- **Entrada**: `intake.json` + manifiesto del slice.
- **Salida**: lista de archivos permitidos y criterio del cambio.
- **Exit**: 0; 1 si el trabajo real excede el manifiesto.

### S4 `build`
- **Entrada**: manifiesto del slice.
- **Salida**: el cambio aplicado.
- **Exit**: 0 siempre que el cambio se haya aplicado. **Build no juzga**: no es su
  estacion.

### S5 `verify`
- **Entrada**: el cambio + el comando de verificacion de intake.
- **Salida**: salida literal del comando, no un resumen.
- **Exit**: 0 verde; 1 rojo (incluye el error); 2 no se pudo correr (falta
  herramienta, entorno roto). **2 no es 0.**

### S6 `review`
- **Entrada**: el diff + el criterio de intake. Contexto limpio: sin la sesion que
  construyo.
- **Salida**: hallazgos con archivo:linea y severidad.
- **Exit**: 0 sin hallazgos; 1 hallazgos; 2 no se pudo revisar.

### S7 `handoff`
- **Entrada**: todo lo anterior.
- **Salida**: `summary`, `status`, `verified[]` (comando + salida),
  `inferred[]` (lo que no se verifico), `openDecisions[]`, `skipped[]`
  (estacion + motivo), ruta del artefacto.
- **Exit**: 0 completo; 1 falta un campo obligatorio.

## 3. Las cinco plantillas

| Plantilla | S1 intake | S2 discovery | S3 slice | S4 build | S5 verify | S6 review | S7 handoff |
|---|---|---|---|---|---|---|---|
| `hotfix` | bloqueante | no aplica | bloqueante | bloqueante | **bloqueante** | declarativo | bloqueante |
| `task` | bloqueante | no aplica | bloqueante | bloqueante | **bloqueante** | bloqueante | bloqueante |
| `feature` | bloqueante | **bloqueante** | bloqueante | bloqueante | **bloqueante + ampliado** | bloqueante | bloqueante |
| `audit` | bloqueante | **bloqueante** | no aplica | no aplica | bloqueante (reproducibilidad) | declarativo | bloqueante |
| `docs` | bloqueante | no aplica | bloqueante | bloqueante | **bloqueante (docs-sync --check)** | declarativo | bloqueante |

### 3.1 `hotfix`
Arreglar algo roto en un lugar puntual.
- **Limite duro**: maximo 3 archivos y 80 lineas de diff. Si lo excede, el
  pipeline se rehusa y escala a `task`. No es advertencia: es exit 1 en S1.
- Verify sigue bloqueante: un fix sin prueba de que arregla algo no es un fix.

### 3.2 `task`
El caso normal.
- Sin limites duros de tamano, pero el manifiesto del slice debe declarar que
  toca.

### 3.3 `feature`
Algo nuevo que toca varias capas.
- Verify ampliado: tests nuevos + build + el comando real del feature.
- Exige una nota de decision (ADR o archivo de decisiones) cuando la feature
  cambia un contrato o una forma de dato.

### 3.4 `audit`
No se cambia codigo, se mide.
- Sin slice, sin build, sin verify de build.
- El equivalente de verify es **reproducibilidad**: el informe trae el comando
  exacto que produjo cada numero, y correrlo de nuevo da lo mismo.
- Es la plantilla que faltaba en el trabajo de `kanam-minesweeper`: era
  diagnostico puro y se trato como implementacion.

### 3.5 `docs`
Solo documentacion.
- Sin build ni tests.
- Verify es `kanam-dev docs --check`: lo que escribo debe coincidir con la
  realidad medida. Es exactamente el hueco F1 del roadmap.

## 4. Reglas transversales

Estas no se negocian por plantilla, porque son donde el verde falso aparece
siempre:

1. **Verify ejecutado, no afirmado.** Un `verificado` sin la salida literal del
   comando es invalido, en todas las plantillas.
2. **Exit 2 nunca es verde.** Si una estacion no pudo medir, el pipeline no avanza
   y lo dice. Un gate que no puede correr y devuelve 0 es la barrera que no corre
   y no lo dice.
3. **Datos locales intocables.** `.env`, `*.db`, `.venv`, `node_modules`: bloqueante
   en `hotfix`, `task`, `feature`. Se detecta por ruta, no por contenido.
4. **Handoff con campos completos.** Lo que no esta escrito no existe.
5. **Sin guiones largos: NO es gate.** Retirado por decision del dueño
   (seccion 0). El script puede seguir usandose como criterio de estilo puntual,
   pero ningun pipeline lo exige.

## 5. Eleccion de plantilla

Regla propuesta (a confirmar por Gonzo): **el pipeline propone, CORE confirma.**

1. S1 `intake` infiere la plantilla por: archivos que el pedido nombra, si pide
   codigo nuevo o cambio, si nombra documentacion, y si el pedido es de medicion.
2. La plantilla inferida se escribe en `intake.json` con su razon.
3. CORE puede cambiarla antes de S2. Despues de S2, cambiarla exige reiniciar el
   pipeline y el motivo queda registrado.
4. Si la inferencia es ambigua, **escala a `task`**, no a `hotfix`: el default
   honesto es el rigor mayor, no el atajo.

## 6. Riesgos y mitigaciones

| Riesgo | Mitigacion |
|---|---|
| `hotfix` se convierte en atajo universal | Limite duro de 3 archivos / 80 lineas, exit 1 en S1 |
| Proliferacion de plantillas | Una plantilla nueva solo entra con un pedido real que no encaje en las cinco |
| Gate salteado en silencio | `skipped[]` obligatorio en el handoff; sin campo, handoff invalido |
| S6 review contaminada por el contexto de S4 | Contexto limpio: solo diff + criterio, sesion separada |
| Exit 2 tratado como 0 | Regla transversal 2, con test propio por estacion |
| Reglas retiradas que vuelven por inercia | Seccion 0 de este documento como registro de lo retirado |

## 7. Que NO entra

- **CLI monolitico con logica propia**: cada estacion delega en los scripts
  existentes (`a11y-scan.mjs`, `check-contrast.py`, `github-pr-risk.sh`,
  `review-check.py`, `pipeline-queue.sh`).
- **Motor de pipeline nuevo**: el workspace ya tiene `pipeline-queue.sh` (cola
  durable, reintentos, huerfanos, telemetria) y `pipeline-track.sh`. Se conecta,
  no se reescribe.
- **Agentes autonomos de codigo**: no estoy autorizada a publicar ni desplegar.
- **Telemetria dentro del CLI**: la metrica de demanda se saca de sesiones y
  memoria, no de instrumentar cada invocacion.
- **Mas de cinco plantillas** en la primera version.

## 8. Orden de implementacion (revisado por este contrato)

```
F5 (intake + eleccion de plantilla)  ->  F0 (despachador con las 7 estaciones)
   ->  F3 (slice+commit como salida de S3/S4)  ->  F1 (verify + docs-sync en S5)
   ->  S6 review (contexto limpio)  ->  S7 handoff (gate de campos)
```

Cambios respecto al roadmap anterior, y por que:

- **F5 primero** (antes era despues): intake es la estacion S1 y sin ella no hay
  contrato de plantilla que valga.
- **F2 `refactor-slice` desaparece como fase propia**: el manifiesto del slice es
  el contrato de S3, ya cubierto.
- **Se agregan S6 y S7 como trabajo explicito**: en el roadmap anterior el review y
  el handoff eran "practica". Aca son estaciones con exit code.

Estimacion: F5 chico, F0 medio, F3 chico, F1 medio, S6 y S7 chicos.

## 9. Decisiones abiertas para Gonzo

1. **Que tan duro es el limite de `hotfix`**: 3 archivos / 80 lineas es una
   propuesta. Si te parece que un fix legitimo puede excederlo, decime el numero y
   lo pongo.
2. **Quien confirma la plantilla**: propongo "el pipeline propone, CORE confirma".
   La alternativa es que CORE la fije siempre, y entonces el intake no infiere.
3. **Si el review de S6 es obligatorio en `task`**: hoy propuse bloqueante. Si lo
   bajas a declarativo, el pipeline gana velocidad y pierde independencia, que es
   justo lo que evito el verde falso en `kanam-minesweeper`.

## 10. Verificacion de este documento

- Secciones 0 a 9 presentes.
- Afirmacion de la seccion 0 verificada contra `agents/kanam-dev/AGENTS.md` y
  `scripts/` (grep, no memoria).
- No se toco codigo ni tests de ningun proyecto.
