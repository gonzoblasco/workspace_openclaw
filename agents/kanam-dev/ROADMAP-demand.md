# ROADMAP - Hacerme mas demandada (Kanam DEV)

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

Estado: borrador para aprobacion de Gonzo. Fecha: 2026-11-06.
Base: inventario real de `agents/kanam-dev/skills/` (49 skills), `scripts/` del
workspace (110+ scripts) y `skills/INDEX`. Cero dependencias nuevas de runtime.

## Principio rector

No me falta conocimiento: tengo **49 skills** y el workspace ya tiene el 70% de
los scripts que propuse el turno pasado (`a11y-scan.mjs`, `github-pr-risk.sh`,
`pr-dashboard.sh`, `check-contrast.py`, `pre-commit.template`,
`complexity-scorer.sh`). Lo que me falta es **una superficie de invocacion
barata**: hoy cada uso arranca con "leete el brief, el repo y el SPEC". Eso es
lento para vos y por eso me llamas menos.

El roadmap no agrega capacidad nueva: **empaqueta lo que ya se, en comandos de
una linea que no exigen contexto previo.** Ese es el criterio de "mas demandada".

Diagnostico explicito: si un pedido tarda mas en explicarse que en ejecutarse,
no me lo pedis. La metrica de exito del roadmap no es "tener mas skills", es
**subir el ratio pedidos-que-vuelven-a-mi**.

## Lo que ya existe y NO hay que construir

Verificado leyendo el arbol, no supuesto:

| Propuesta del turno anterior | Ya existe | Donde |
|---|---|---|
| a11y screenshot/contraste | si | `scripts/a11y-scan.mjs`, `scripts/check-contrast.py` |
| audit de riesgo de PR | si | `scripts/github-pr-risk.sh` |
| tablero de PRs | si | `scripts/pr-dashboard.sh`, `scripts/pr-thread-brief.sh` |
| pre-commit hook | si (template) | `scripts/pre-commit.template` |
| complejidad | si | `scripts/complexity-scorer.sh`, `complexity-parse.py` |
| bootstrap de proyecto | si | `scripts/init-project.sh` |
| review mecanico | si | `scripts/review-check.py`, `review-charts.py` |
| validacion de skills | si | `scripts/test-skills.sh`, `compare-skills.py` |
| gate de a11y por trigger | si | `scripts/check-a11y-trigger.py` |

Conclusion: el roadmap **no es un backlog de features**. Es de **envoltorios
finos sobre lo existente** mas tres huecos reales que si faltan.

## Huecos reales (lo unico que hay que construir de cero)

Verificado por grep: no existe ningun script que haga estas tres cosas.

1. **`docs-sync`**: nada mantiene en fase README/SPEC/CHANGELOG/ADR despues de un
   cambio de codigo. Hoy lo hago a mano cuando me lo pedis, y por eso solo me lo
   pedis cuando te acordas.
2. **`refactor-slice`**: no hay procedimiento mecanico de "extraer un slice
   atomico verificable". Lo hago a criterio; sin comando, no es reusable.
3. **`slice-commit`**: no hay nada que corte un working tree sucio en commits
   atomicos con mensajes en ingles. Hoy eso es 100% manual.

## Roadmap

### F0 - Superficie de invocacion (lo que hace que me uses) - chico

Construir **un solo punto de entrada**: `agents/kanam-dev/bin/kanam-dev`.

No es un CLI gigante: es un despachador de 8 subcomandos que **llama a los
scripts que ya estan** y devuelve una salida corta y accionable. Cero logica
duplicada, cero dependencias.

```
kanam-dev audit <dir>       -> build + test + lint + check_em_dash (un veredicto)
kanam-dev review <pr>       -> github-pr-risk.sh + review-check.py
kanam-dev a11y <url|dist>   -> a11y-scan.mjs + check-contrast.py
kanam-dev docs <dir>        -> F1 (hueco real)
kanam-dev slice <dir>       -> F2 (hueco real)
kanam-dev commit <dir>      -> F3 (hueco real)
kanam-dev status            -> que hay sucio, que esta verde, que falta
kanam-dev help              -> contratos y exit codes
```

Reglas duras:
- Exit codes honestos: 0 ok, 1 hallazgos, 2 infraestructura ausente. Un gate que
  no puede correr nunca sale 0.
- Cada subcomando imprime **una linea de veredicto** y como maximo 10 lineas de
  detalle. El detalle completo va a `/tmp` o a `--verbose`.
- Sin color por defecto si la salida no es TTY.

Unidades atomicas:
- F0.1 Despachador + `help` + `status`. Criterio: `kanam-dev help` lista los 8
  subcomandos con su exit code; `kanam-dev status` corre en un repo limpio y en
  uno sucio y reporta correctamente. `test -x bin/kanam-dev` + test de salida.
- F0.2 `audit` cableado a los scripts existentes. Criterio: en
  `kanam-minesweeper` da 0; con un guion largo inyectado en un `.js` temporal da
  1 y nombra el archivo:linea.
- F0.3 `review` y `a11y`. Criterio: `a11y` sobre una URL muerta sale 2 (no 0),
  probando que el gate puede fallar.

Riesgo: que el despachador se convierta en un segundo lugar donde vive la logica.
Mitigacion: cada subcomando son menos de 40 lineas y delega; si necesita logica
propia, no entra en F0.

### F1 - `docs-sync`: que la documentacion deje de mentir - medio

Es el hueco mas caro del ecosistema: ya paso en `kanam-minesweeper` (STATUS.md
decia 156 tests cuando eran 168, y DESIGN.md declaraba un token que medía 1.40:1)
y en `kanam-critic` (README desactualizado).

Que hace: dado un repo, detecta las afirmaciones numericas/verificables en
README/STATUS/DESIGN y las compara con la realidad medida.

- conteo de tests: corrido real vs lo que dice el doc.
- tokens de color: valor del doc vs valor del CSS.
- comandos citados: existen como script o script npm?
- rutas citadas: existen en disco?

Salida: lista de desalineaciones con `archivo:linea`, doc dice X, realidad es Y.

Unidades atomicas:
- F1.1 Extractores puros (tests, tokens, comandos, rutas) con tests propios.
  Criterio: cada extractor tiene un test que falla por la razon correcta cuando
  el doc dice algo falso.
- F1.2 Integracion en `kanam-dev docs` con `--check` (exit 1 si hay drift) y
  `--fix` (solo reescribe conteos, nunca prosa). Criterio: sobre
  `kanam-minesweeper` con STATUS.md corregido a 156, sale 1 y nombra la linea.
- F1.3 Regla anti-falso-verde: si no puede medir (no hay suite, no hay tokens),
  sale 2 con la razon, no 0.

Riesgo: que `--fix` reescriba prosa. Mitigacion: `--fix` solo toca numeros
aislados y lineas de token; cualquier otro cambio requiere `--force` explicito.

### F2 - `refactor-slice`: convertir criterio en procedimiento - medio

Que hace: dado "extrae X de Y", ejecuta el slice con verificacion en cada paso:
leer el blanco, escribir el cambio minimo, correr la verificacion del repo, y
parar antes de seguir si queda rojo.

No es un agente: es un **contrato de ejecucion** que yo sigo y que el comando
hace cumplir (falla si se toca mas de lo declarado).

Unidades atomicas:
- F2.1 Manifiesto del slice (`slice.yaml`: archivos permitidos, criterio, comando
  de verificacion). Criterio: un cambio a un archivo fuera del manifiesto hace
  fallar el comando.
- F2.2 Ejecucion con verificacion intermedia. Criterio: en un repo de prueba con
  un test rojo, el comando se detiene y devuelve el diff, no sigue.
- F2.3 Reporte de handoff: archivos, verificacion, decisiones abiertas.
  Criterio: el reporte contiene los tres campos y ninguno vacio.

Riesgo: sobre-ingenieria. Mitigacion: F2 no implementa un agente de codigo; solo
verifica que el cambio respete el manifiesto. La escritura la sigo haciendo yo.

### F3 - `slice-commit`: de working tree sucio a historia limpia - chico

Que hace: agrupa archivos por intencion, propone mensajes `type(#issue): desc` en
ingles y commitea en slices, sin pushear jamas.

Unidades atomicas:
- F3.1 Clasificador de archivos por tipo de cambio (feat/fix/docs/test/chore) con
  tests sobre casos sinteticos.
- F3.2 Dry run por defecto: imprime el plan de commits; `--apply` lo ejecuta.
  Criterio: en un tree con 3 archivos de 2 categorias, propone 2 commits y el dry
  run no modifica el indice.
- F3.3 Guarda de seguridad: nunca `git add -A` si detecta `.env`, `*.db`, `.venv`,
  `node_modules`; sale 1 y lista cada archivo peligroso.

Riesgo: commitear datos locales irrecuperables. Mitigacion: F3.3 es bloqueante,
no advertencia, y tiene test propio con un `.env` de fixture.

### F4 - Empaquetado como skill y memoria de uso - chico

Que hace: que el roadmap persista. Dos piezas.

- F4.1 `skills/kanam-dev-surface/SKILL.md`: la skill que documenta el despachador,
  cuando usarlo y sus exit codes. Criterio: `python3 scripts/compare-skills.py` o
  `test-skills.sh` no reporta drift; frontmatter valido.
- F4.2 Nota de memoria con decision + metricas base: cuantos pedidos por dia recibi
  en la semana previa. Criterio: la nota existe y tiene fecha; la metrica se
  remide a las dos semanas.

Riesgo: documentar antes de tener uso real. Mitigacion: F4 va despues de F0-F1,
cuando hay al menos un uso real medido.

## Lo que NO entra

- **Un CLI monolitico con toda mi logica adentro**: duplica los scripts del
  workspace y crea una segunda fuente de verdad. El despachador delega, no absorbe.
- **Agentes autonomos de codigo**: no estoy autorizada a publicar ni desplegar; un
  agente que escribe sin supervision es exactamente el "verde falso" que la v1 de
  minesweeper ya pago.
- **Skills nuevas de contenido**: con 49 skills, sumar una 50 no me hace mas
  demandada. El cuello es invocacion, no conocimiento. Cualquier skill nueva
  necesita un pedido real repetido que la justifique.
- **Dependencias nuevas**: nada de pyyaml, typer, click, rich. Argument parsing con
  stdlib, como el resto del workspace.
- **Telemetria de uso**: medir "cuanto me usan" tocando cada invocacion agrega
  superficie de fallo. La metrica se saca de la memoria/sesiones, no del CLI.

## Orden recomendado y por que

```
F0 (despachador)  ->  F1 (docs-sync)  ->  F3 (slice-commit)  ->  F2 (refactor-slice)  ->  F4 (skill + memoria)
```

- **F0 primero**: sin superficie, todo lo demas no se invoca. Es ademas la fase mas
  chica y la que te da retorno inmediato (un comando, ocho tareas).
- **F1 segundo**: es el hueco mas caro y el mas medible; ya hay dos casos reales
  donde la doc mintio. Es el que mas me va a hacer llamar porque duele hoy.
- **F3 tercero**: chico, util en cada tarea, y convive con el repo sucio actual
  (hay cambios sin commitear que llevan tiempo).
- **F2 cuarto**: el mas riesgoso de sobre-ingenieria. Necesita que F0 y F3 ya
  funcionen para no duplicar el despachador.
- **F4 ultimo**: documentar cuando hay uso real, no antes.

Dependencias explicitas: F1, F2 y F3 dependen de F0 (cada uno es un subcomando).
F2 depende de F3 para no reimplementar el reporte de diff. F4 depende de F0 y F1
para tener algo medido que documentar.

Estimacion total: 2 chicas + 2 medias + 1 chica. El volumen real esta en F1 y F2.

## Decision abierta para Gonzo

**Que metrica define exito.** Mi propuesta: pedidos por semana que vuelven a mi
sobre un total de pedidos que podrian ser mios. Si en dos semanas el despachador
existe y la metrica no sube, el diagnostico estaba mal y hay que cambiar el
principio, no agregar fases.

Alternativa: contar invocaciones del CLI. Es mas facil de medir y mas facil de
falsificar (un cron puede inflarla). Por eso no la propongo como metrica principal.
