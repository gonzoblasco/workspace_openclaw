# Despacho de juicio: cómo se convoca al Critic

**Nace de:** el programa `critic-v0.3` y una jornada (2026-11-19) en la que cuatro gates
consecutivos fueron inválidos por las mismas causas. Las fricciones F29–F34 de
`agents/kanam-critic/memory/frictions.jsonl` son el catálogo de lo que este contrato impide.

**Regla que ordena todo:** un veredicto del Critic es un **artefacto verificable**, no una
afirmación. Si no hay archivo, fila en el ledger y evidencia cruda, no hay veredicto.

---

## 1. Quién puede convocarlo

Cualquier rol del Crew, a través del CORE. La invocación es siempre:

```
sessions_spawn(agentId: "kanam-critic", context: "isolated", label, task)
```

- `context: "isolated"` es obligatorio: el agentId es distinto al del solicitante.
- **Rutas absolutas siempre.** El cwd del subagente es su propio workspace
  (`agents/kanam-critic/`), no la raíz del repo. Tres gates murieron llamando `ls agents`
  tres veces y cortando el turno.
- El modelo del Critic es `gpt-oss:120b-cloud` (ADR-090). Si se cambia, se declara en el
  reporte: el modelo del juez es parte del contrato, no un detalle (F8).

## 2. Qué debe traer la petición

Sin estos seis elementos, el Critic devuelve `PETICIÓN INCOMPLETA` y no puntúa:

| Elemento | Por qué |
|---|---|
| Ruta absoluta del artefacto | para leer el código real, no la descripción |
| Qué se afirma de él | la afirmación es lo que se evalúa, no el artefacto en abstracto |
| Señal de listo del ROADMAP | el criterio de aceptación es externo al juez |
| Spec de `gate-evidence` (si existe) | la evidencia mecánica se produce, no se narra |
| Si hay publicación externa involucrada | nada sale sin autorización humana explícita |
| Fricciones previas conocidas del artefacto | no re-descubrir lo ya registrado |

## 3. Qué devuelve siempre

Cuatro artefactos. Los cuatro o no hay veredicto:

1. **Reporte** en `agents/kanam-critic/docs/reviews/<fecha>-<slug>.md`, donde `<slug>` contiene
   el nombre del artefacto (si no, `verify-verdict` no lo encuentra y el veredicto queda huérfano).
   Debe incluir: tabla SHARP con los cinco ejes y su justificación, **evidencia cruda completa**,
   y ≥5 citas `ruta:línea` reales.
2. **Fila en el ledger** vía `bin/emit-verdict.py`, con la interfaz real:
   `--artifact --S --H --A --R --P --report --model`. No existen `--trace-table`, `--source`
   ni `--status`.
3. **`bin/verify-verdict.py`** con `GLOBAL=aprobado`.
4. **`git diff --stat` del ledger**, como prueba de que la fila se escribió.

## 4. Qué invalida una respuesta

Cada ítem de esta tabla ocurrió de verdad el 2026-11-19. No es teoría.

| Síntoma | Fricción | Cómo se detecta |
|---|---|---|
| Veredicto con score sin corridas | F29 | comparar el reporte contra comandos que el CORE repite |
| Flag o subcomando inventado | F29 | `--help` del binario citado |
| Integración en CI inexistente | F29 | `grep` del step en `.github/workflows/` |
| No saber invocar la herramienta que se juzga | F30 | reproducir el comando del reporte |
| Evidencia elidida (`(omitted)`, `...`) | F31, F32 | `grep` de elisiones en el reporte |
| Citas a relleno (líneas `# ---`, imports) | F33 | abrir cada cita y leer la línea |
| Reporte sin tabla SHARP | F33 | `grep Sharpness` |
| Reporte declarado y no escrito | F34 | `ls` de la ruta declarada |
| Caso de prueba que falla por otra razón | F34 | verificar el motivo del exit code |

**Regla del CORE:** un auto-reporte no es un hecho. Antes de aceptar, el CORE verifica en disco:
archivo existe, fila en el ledger, `verify-verdict` global, y abre cada cita. Si algo falla, el
gate se declara inválido y se registra la fricción con la evidencia.

## 5. Cuando el gate falla dos veces

**No se itera una tercera vez a ciegas.** Dos gates inválidos sobre el mismo artefacto significan
un problema del proceso, no del código. Salidas válidas:

1. **Cambiar el ejecutor** (modelo distinto para el juez), declarando el override.
2. **Cerrar por verificación del CORE**, con nota explícita en el reporte y en la evidencia del
   programa: *"NO hay veredicto del Critic"*.
3. **Parar y escalar a Gonzo**, con la evidencia de las dos fallas.

Lo que no se hace: emitir un veredicto "provisional", completar los ejes desde el ledger sin
declararlo, ni dar por bueno un reporte que no se abrió.

## 6. El límite que no se cruza

- El Critic **no publica**: comenta en un PR solo con autorización humana explícita, y el cuerpo
  lo genera `bin/format_sharp_report.py`, no una redacción libre.
- El Critic **no arregla** lo que juzga: si el artefacto está mal, devuelve fricciones.
- El CORE **no puntúa**: puede verificar mecánicamente y cerrar un paso con nota, pero el score
  es del juez. Cuando no hay juez, se dice, no se improvisa.

## 7. Herramientas del contrato

| Comando | Qué garantiza |
|---|---|
| `bin/gate-evidence.py --spec <spec.json>` | la evidencia la produce un programa; exit ≠ 0 si un caso falla |
| `bin/objective-extractor.py <doc.md>` | citas `ruta:línea` verificadas contra disco |
| `bin/emit-verdict.py ...` | el reporte se valida antes de escribir el ledger |
| `bin/verify-verdict.py` | cada veredicto real tiene reporte con respaldo |
| `bin/format_sharp_report.py` | el cuerpo del comentario sale del reporte y del ledger, no de una redacción |
| `agents/kanam-critic/docs/GATE-RUNBOOK.md` | cómo se opera todo lo anterior desde un subagente |
