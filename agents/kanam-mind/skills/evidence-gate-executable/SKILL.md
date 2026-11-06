---
name: "evidence-gate-executable"
description: "Ejecutar el gate de evidencia (kb-audit), ingestar material citado (kb-ingest) y consultarlo con citas verificadas (kb-search) o registrar un brief (brief-journal). Usar SIEMPRE antes de entregar un brief, una nota de memoria o un handoff, y al estudiar un libro o corpus."
user-invocable: true
---

# evidence-gate-executable

Convierte `source-verification-gate` y `evidence-chain-audit` en algo que **corre**: un veredicto reproducible sobre el artefacto, no mi palabra.

Los cuatro scripts viven en `scripts/` de este workspace y no dependen de red ni de modelo (salvo el check de links, que se puede correr `--offline`).

## 1. Cerrar un brief (siempre)

```bash
python3 scripts/kb-audit.py <brief.md> --root .            # informe legible
python3 scripts/kb-audit.py <brief.md> --root . --json     # para el journal
python3 scripts/kb-audit.py <brief.md> --strict            # exit 1 si FAIL (usalo en entregas)
```

Veredictos:
- `PASS` - sin fallas ni incógnitas.
- `PARTIAL` - hay links sin verificar (`unknown`). No es PASS: decilo.
- `FAIL` - afirmación sin etiqueta, cita a archivo inexistente, cita fuera de rango, o link muerto.

**Regla:** un `FAIL` en `label` o `path` **no se entrega**. Se corrige el brief o se convierte la
afirmación en `[inf]`/`[unk]`. Un `unknown` en links no se convierte en "verificado": se declara.

## 2. Registrar el brief (journal)

```bash
python3 scripts/brief-journal.py add --brief <brief.md> --question "<pregunta>" \
    --run-audit --source <fuente1> --source <fuente2> --assignee main
python3 scripts/brief-journal.py list
python3 scripts/brief-journal.py stats
```

`--run-audit` guarda el veredicto del gate junto con el brief: la entrada del journal es la traza.

## 3. Ingestar material de estudio

```bash
python3 scripts/kb-ingest.py --db memory/knowledge.db --source <archivo.md> \
    --title "Libro X · Cap 3" --kind chapter --split h2 --tag obs
python3 scripts/kb-ingest.py --db memory/knowledge.db --source <url> --fetch --title "Doc oficial"
```

Cada sección queda con su cita (`archivo#Lx-Ly`, o `URL (consultado YYYY-MM-DD)`). Re-ingerir es
idempotente; `--replace` reemplaza las secciones de esa fuente. No borra otras fuentes.

## 4. Consultar con citas verificadas

```bash
python3 scripts/kb-search.py "consulta"              # FTS5, sin modelo, verifica la cita
python3 scripts/kb-search.py --sources               # corpus ingestado
python3 scripts/kb-search.py --stale                 # fuentes que cambiaron desde la ingesta
```

Cada resultado trae `✓ ok` / `✗ missing` / `✗ out-of-range`: **una cita rota se reporta, no se usa.**

## Orden correcto (no invertirlo)

1. Ingestar / abrir la fuente.
2. Escribir el brief con etiquetas y citas.
3. `kb-audit --strict`.
4. Corregir lo que el gate encontró.
5. `brief-journal add --run-audit`.
6. Entregar con el veredicto y las incógnitas declaradas.

## Errores que este skill previene

- Entregar un brief limpio pero sin etiquetas (el caso `sprint-9-validation.md`: FAIL por label).
- Citar `archivo#L200` en un archivo de 80 líneas (cita fuera de rango).
- Presentar un link que no abrí como "verificado" (sale `unknown`, no `ok`).
- Un journal que registra "entregado" sin veredicto (por eso `--run-audit`).

## Límites

- El check de `labels` es heurístico: no entiende semántica. Un falso positivo se resuelve
  etiquetando la oración o reformulándola; **no** se apaga el check para pasar.
- No publica, no commitea, no sale del workspace.
