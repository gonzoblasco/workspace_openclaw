---
name: "model-comparison-cata"
description: "Correr una cata de modelos (o de harnesses) con fixture reproducible: suite oculta validada en las dos direcciones, dos tandas de razonamiento (low y apagado), runner con nonce anti-cache y auto-escalado de num_predict, evaluador ciego de CONTENT vs CLEANLINESS, y REPORT.md con la estructura probada. Usar cuando: 'hagamos una cata', 'compará estos modelos', 'probemos el skill de comparación', 'quiero el mismo nivel de detalle que la cata de mimo', 'dejá esto replicable para la próxima'. Distinta de model-cata (rúbrica de prosa y ADR de motor) y de model-capability-selection (requisito binario de un rol)."
---

# Cata de modelos: el kit reproducible

La metodología de la cata 2026-11-16, extraída a un kit que corre igual la próxima vez.
El **porqué** de cada regla (con la evidencia medida) vive en el skill
`harness-model-comparison`; acá está el **cómo**, ejecutable.

## Cuándo usarlo

- Comparar modelos sobre las mismas tareas y querés un veredicto con números, no impresiones.
- Comparar harnesses de agente (goose, opencode, Claude Code, Qwen Code): el kit corre igual,
  pero antes fijá modo de aprobación y toolset (ver `harness-model-comparison` steps 1 y 4).
- Probar un cambio en la metodología misma (como la política `low` por defecto).

No lo uses para elegir un modelo por una capacidad binaria (¿ve imágenes?) ni para presupuesto:
eso es `model-capability-selection` y la lente de `model-cata`.

## Definición de terminado (gate)

Una cata NO está terminada hasta que existan las nueve piezas del `REPORT.md`:

1. Suite validada en las dos direcciones (referencia PASS, defectuosa FAIL).
2. Tabla de la perilla por candidato, con el valor **efectivo** y el default de la carta.
3. Tanda `low` con pass/eval/thinking/tiempo.
4. Tanda `off` con el modo observado por celda.
5. Hallazgos del runner (lo que produjo un resultado falso).
6. Veredicto con costo y encaje, no solo "ganó".
7. Límites de la medición.
8. Comandos para reproducir.
9. Evaluador ciego y comparación de rankings (convergencia y divergencia por eje).

Si falta 1, no se mide. Si falta 9, no hay ranking, hay una opinión.

## Procedimiento

### 0. Crear el fixture

```bash
python3 scripts/cata-kit.py init bench/cata-<fecha>
```

Deja `cata.json`, `tasks.json`, `evaluate.py` (con la suite de ejemplo funcionando),
`reference/`, `defective/`, `REPORT.template.md` y `blind-eval-brief.md`.

### 1. Congelar todo menos lo que se mide

En `cata.json`: modelos y el **valor de la perilla por tanda** (`low` y `off`). El default de
la cata es `low`; el máximo es una tanda aparte que pide el owner. Si un modelo no permite
apagar el razonamiento, poné `null` en `off`: la celda sale **no medida**, nunca 0.

En `tasks.json`: 3–6 tareas, cada una con una trampa real y `kind` (`code` o `analysis`). Para
`analysis`, `result_anchor` es la línea donde debe empezar el resultado (ej. `TOTAL:`).

### 2. Escribir los asserts ocultos

En `evaluate.py`, reemplazá los checks de ejemplo. Reglas que costaron caro:

- Extraer el **último** bloque con `def `, nunca el primero.
- Correr el código del candidato en subproceso con timeout.
- Un assert no puede depender de un identificador que el enunciado no fija.
- Validar contra la referencia correcta Y contra una versión defectuosa.

```bash
python3 scripts/cata-kit.py check bench/cata-<fecha>   # debe decir SELFTEST OK
```

### 3. Correr

```bash
python3 scripts/cata-kit.py run bench/cata-<fecha> --dry   # ver celdas y valores
python3 scripts/cata-kit.py run bench/cata-<fecha>
```

El runner ya implementa: misma vía para todos, temperatura 0, `num_ctx` explícito, nonce
compartido por celda (sin él el daemon devuelve caché y la perilla "no viaja"), auto-escalado
de `num_predict` cuando el content vuelve vacío con thinking, warm-up separado y nombres de
archivo seguros (`mimo-v2.6-...` con `with_suffix` se trunca a `mimo-v2.md`).

**Lanzalo como job de fondo independiente**, no con `nohup` dentro de una sesión de shell: el
proceso muere a mitad de corrida sin traza.

### 4. Agregar

```bash
python3 scripts/cata-kit.py analyze bench/cata-<fecha>
```

Imprime la tabla para el reporte y escribe `results_analyzed.json`.

### 4-bis. Corregir un assert NO invalida la corrida

Si después de medir aparece un assert demasiado estrecho (un regex que exigía la redacción de la
referencia y rechazó "id 4: moneda no válida (EUR)"), se corrige el assert, se corre `check`
otra vez, y se **re-evalúa desde el `content` guardado en `results.json`** — no se re-corre la
cata. `results.json` guarda el texto completo de cada celda justo para esto. Registrar en el
reporte qué celdas cambiaron de veredicto y por qué.

### 5. Evaluador ciego

Spawnear un subagente con **modelo distinto de todos los candidatos**, `context: isolated`, y
el brief de `blind-eval-brief.md` (con `{{DIR}}` resuelto). Prohibido leer `results*.json`,
`evaluate.py` y `analyze.py`.

Después comparar casilla por casilla: dónde coincide (convergencia) y dónde no. La divergencia
es el dato. Medido 2026-11-16: el análisis mecánico marcó CLEANLINESS perfecta y el ciego
encontró comentarios de razonamiento y código muerto dentro del bloque; la métrica medía
formato, no limpieza.

**Ninguna frase del ciego se acredita sin auditar contra el archivo — y ninguna se descarta sin
abrirlo.** En esa misma cata el ciego también dijo cosas imprecisas (llamó "exclusiones bien
hechas" a una lista que no lo estaba). El padre descartó primero un hallazgo válido con un grep
que buscaba otra cosa y reportó "comentarios inexistentes": el error fue del padre, no del ciego.
Regla: abrir el archivo **citado con su línea** y confirmar o refutar con lo que dice el archivo;
un descarte por búsqueda mal hecha es un falso negativo disfrazado de auditoría.

### 5-bis. La tanda `off` puede no estar apagada, y el runner lo dice

Si un modelo devuelve `thinking` no vacío con `think:false`, la columna `off` es otra corrida con
la perilla ignorada. Medido 2026-11-16: `minimax-m3.1-flash` devolvió 349/546/357 chars de
thinking en sus tres celdas apagadas, y `glm-5.3-flash` rechazó el valor con HTTP 400. Esa fila
va como **no medida** o como observación etiquetada, nunca como evidencia de comportamiento sin
razonamiento.

### 6. Escribir el REPORT.md

```bash
cp bench/cata-<fecha>/REPORT.template.md bench/cata-<fecha>/REPORT.md
```

Completar las nueve secciones. Regla de estilo: **cada afirmación se apoya en un artefacto**
(celda, archivo, número), y el fallo se cita del entregable, no del resumen del candidato.

### 7. Commitear el fixture completo

La suite, la referencia, la defectuosa, el runner, las salidas y el informe son **un solo
activo reproducible**. Sin el fixture, el reporte es una afirmación sin respaldo.

## Trampas ya medidas (no re-descubrirlas)

| Trampa | Síntoma | Fix |
|---|---|---|
| Caché del daemon | `think:false` devuelve el mismo `eval_count` que `true` | nonce por celda, igual entre candidatos |
| `with_suffix` | artefactos `mimo-v2.md` pisados | nombre concatenado, no `with_suffix` |
| `nohup ... &` | corrida muerta sin traza | job de fondo del runtime |
| Default de la carta | `muse-spark-open` mide `xhigh` sin avisar | fijar la perilla por candidato |
| `false` ignorado | mistral-large-4 razona igual con `think:false` | fila `off` = no medida, con motivo |
| `content` vacío | truncación propia, no defecto del modelo | auto-escalar `num_predict` y reintentar |
| Todos empatan | 3 tareas y 5 modelos, todo PASS | el empate es el resultado; desempatar por costo y latencia, y decirlo |

## Archivos del kit

- `scripts/cata-kit.py` — `init`, `check`, `run`, `analyze`.
- `skills/model-comparison-cata/templates/` — plantillas + suite de ejemplo validada.
- Ejemplo real: `bench/cata-2026-11-16/` (5 modelos, 27 celdas, `REPORT.md`).
