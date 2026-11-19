# gate-evidence

Evidencia de gate producida por un programa, no por el narrador. El juez corre
`bin/gate-evidence.py --spec <spec.json>` y pega la salida: si un caso no se
corrió, no aparece como PASS.

## Uso

```bash
python3 bin/gate-evidence.py --spec tests/gate-evidence/spec-objective-extractor.json
python3 bin/gate-evidence.py --spec <spec.json> --json
```

Exit codes: `0` todo pasa · `1` algún caso o suite de pytest falla · `2` spec
inválido (JSON roto, caso sin `expect_exit`, lista de expectativas vacía,
claves desconocidas).

## Spec

```json
{
  "name": "objective-extractor",
  "repo_root": "../../../..",
  "bin": "agents/kanam-critic/bin/objective-extractor.py",
  "pytest": ["agents/kanam-critic/tests/objective-extractor/"],
  "cases": [
    {
      "name": "pipe escapado",
      "cmd": ["python3", "{BIN}", "{TMP}/pipe.md"],
      "files": {"{TMP}/pipe.md": "contenido"},
      "expect_exit": 0,
      "expect_stdout_contains": ["verificado"],
      "expect_stderr_contains": ["RESUMEN: 1 filas"]
    }
  ]
}
```

- `repo_root` es relativo al archivo del spec.
- `{BIN}` = `repo_root/bin`; `{TMP}` = directorio temporal propio del caso;
  `{ROOT}` = `repo_root`. Se sustituyen en `cmd`, en las claves y en los
  valores de `files`.
- `files` se materializa antes de correr el caso; una clave relativa cae dentro
  de `{TMP}`.
- `expect_exit` es obligatorio. Un caso solo con exit esperado es válido; un
  caso sin él no.
- Los conteos de pytest salen del JUnit XML, no del texto: el repo configura
  `addopts = -q`, y `-q` extra daría `-qq` (summary suprimido).
- Una suite sin tests colectados es FAIL, no PASS: no se aprueba por ausencia.

## Demo

`spec-objective-extractor.json` cubre los 8 casos del extractor: pipe escapado,
tabla malformada (exit 2), dos bloques (exit 1), archivo inexistente, línea
vacía, sin marcadores, `1_0` y línea fuera de rango.
