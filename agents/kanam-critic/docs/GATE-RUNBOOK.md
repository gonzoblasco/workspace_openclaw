# GATE-RUNBOOK — cómo operar el kit desde una sesión de subagente

**Para:** el Critic cuando corre como subagente (gate de un paso de programa).
**Motivo:** dos gates de T4.1 (2026-11-19) fueron inválidos por razones operatorias, no de criterio: F29 inventó evidencia, F30 no supo invocar la herramienta. Este runbook existe para que la tercera no sea una cuestión de suerte.

---

## 0. La regla que ordena todo

**Un gate sin evidencia producida por un comando es inválido, sin importar el puntaje.**

Si no podés pegar la salida cruda y el exit code, no podés puntuar. Se declara `GATE INVÁLIDO` y se explica qué faltó. Declararse incompetente es aceptable; inventar no.

---

## 1. Tu cwd no es la raíz del workspace

Cuando corrés como subagente, tu directorio de trabajo es **tu** workspace (`agents/kanam-critic/`), no la raíz del repo. Consecuencias:

- Usá **rutas absolutas** siempre: `/Users/gonzoblasco/.openclaw/workspace/...`
- Si una ruta falla, **no la repitas igual**. Cambiala o pará. OpenClaw corta el turno tras 3 fallos idénticos y el gate se pierde.

---

## 2. Cómo se invoca cada cosa (interfaces reales)

| Herramienta | Invocación correcta | Error típico |
|---|---|---|
| `bin/objective-extractor.py` | `python3 <ABS>/bin/objective-extractor.py <archivo.md>` | pasar el contenido por **stdin**. El argumento es posicional y obligatorio. |
| `bin/emit-verdict.py` | `--artifact NAME --S N --H N --A N --R N --P N --report RUTA.md [--notes] [--model]` | inventar `--trace-table`, `--source`, `--status`: no existen. |
| `bin/verify-verdict.py` | `python3 <ABS>/bin/verify-verdict.py` | esperar argumentos: corre sin ninguno y valida todo el ledger. |
| suite de tests | `cd <ABS_ROOT> && python3 -m pytest <ruta>` | agregar `-q`: `pytest.ini` ya lo agrega y duplica la salida. |

Ante la duda: `--help` **antes** de suponer.

---

## 3. Formato de entrada de `objective-extractor.py`

Solo lee tablas entre marcadores. El resto del documento se ignora.

```markdown
<!-- objetivos:begin -->
| Objetivo | Entregable | Cita |
|---|---|---|
| Reducir el fraude | regla nueva | `src/fraud/rules.py:42` |
<!-- objetivos:end -->
```

Estados: `verificado` (archivo + línea + contenido existen), `auto-reportado` (cualquier falla, con motivo).
Exit: `0` todo verificado o sin filas · `1` hay auto-reportadas · `2` documento malformado o ilegible.

**Construí tus propios fixtures en `/tmp`, no en el repo.** Los del autor no son evidencia: si el test está escrito para pasar, no prueba nada.

---

## 4. Evidencia obligatoria del gate

Corré y pegá, en este orden:

1. `python3 <ABS>/bin/gate-evidence.py --spec <spec.json>` → imprime `GATE-EVIDENCE: PASS|FAIL` con la tabla de casos y sus exit codes. Es la evidencia canónica; si no la corrés, el gate es inválido.
2. La salida de la suite de tests, con la línea `N passed` o `N failed`.
3. Después de emitir: `git -C <ROOT> diff --stat agents/kanam-critic/memory/verdicts.jsonl` (prueba de que el ledger cambió).
4. `python3 <ABS>/bin/verify-verdict.py` → el `GLOBAL=` final.

---

## 5. Qué invalida un veredicto (casos ya vistos)

- Afirmar "veredicto emitido" sin fila nueva en `verdicts.jsonl`.
- Citar un flag o un subcomando que no existe.
- Atribuir integración en CI sin un workflow que la mencione.
- Puntuar un eje con 5 cuando no hay evidencia de ese eje. `H (Horizon)` en particular: sin CI ni uso real, no es 5.
- Correr solo los tests del autor y llamarlo "verificación completa".

---

## 6. Si el artefacto no se puede ejecutar

Decilo y pará. Un gate inválido con motivo escrito es mejor que un ORO inventado: el segundo contamina el ledger y obliga a anular el veredicto después (`invalidate-verdict.py` existe justamente para eso).
