---
name: "evidence-gate-executable"
description: "Ejecutar el gate de evidencia (kb-audit, handoff-gate), ingestar material citado (kb-ingest) y consultarlo con citas verificadas (kb-search) o registrar un brief (brief-journal). Usar SIEMPRE antes de entregar un brief, una nota de memoria o un handoff, y al estudiar un libro o corpus."
user-invocable: true
---

# evidence-gate-executable

Convierte `source-verification-gate` y `evidence-chain-audit` en algo que **corre**, y lo enchufa en
el borde del pipeline: un veredicto reproducible como el resultado de un build, no mi palabra.

Los cinco scripts viven en `scripts/` de este workspace y no dependen de red ni de modelo (salvo el
check de links, que se puede correr `--offline`).

## 1. Cerrar un brief (siempre)

```bash
python3 scripts/kb-audit.py <brief.md> --root .            # informe legible
python3 scripts/kb-audit.py <brief.md> --root . --json     # para el journal
python3 scripts/kb-audit.py <brief.md> --strict            # exit 1 si FAIL (usalo en entregas)
```

Veredictos: `PASS` · `PARTIAL` (links sin verificar) · `FAIL` (etiqueta faltante, cita a archivo
inexistente, cita fuera de rango, link muerto).

**Regla:** un `FAIL` en `label` o `path` **no se entrega**. Un `unknown` en links no se convierte en
"verificado": se declara.

## 2. Gate de handoff (el borde del pipeline)

```bash
# Salida: antes de marcar el handoff como entregado
python3 scripts/handoff-gate.py out --role kanam-mind --artifact <brief.md> --json --strict

# Entrada: al recibir un handoff con claims citados
python3 scripts/handoff-gate.py in --handoff <handoff.json> --offline
python3 scripts/handoff-gate.py in --claims <claims.json>
```

Forma del handoff de entrada (contrato de `research-brief-protocol`):

```json
{"role": "kanam-dev", "artifact": "path", "verdict": "PASS",
 "claims": [{"text": "...", "source": "path#Lx-Ly | URL", "date": "YYYY-MM-DD"}]}
```

Exit `1` si un claim no resuelve o el artefacto de salida da `FAIL`: el mismo trato que un test
rojo. **Esto reemplaza agregar un agente revisor**: una afirmación sin fuente se rechaza en el
borde, no se revisa después.

## 3. Registrar el brief (journal)

```bash
python3 scripts/brief-journal.py add --brief <brief.md> --question "<pregunta>" \
    --run-audit --source <fuente1> --source <fuente2> --assignee main
python3 scripts/brief-journal.py list
python3 scripts/brief-journal.py stats
```

`--run-audit` guarda el veredicto del gate junto con el brief: la entrada del journal es la traza.

## 4. Ingestar material de estudio

```bash
python3 scripts/kb-ingest.py --db memory/knowledge.db --source <archivo.md> \
    --title "Libro X · Cap 3" --kind chapter --split h2 --tag obs
python3 scripts/kb-ingest.py --db memory/knowledge.db --source <url> --fetch --title "Doc oficial"
```

Cada sección queda con su cita (`archivo#Lx-Ly`, o `URL (consultado YYYY-MM-DD)`). Re-ingerir es
idempotente; `--replace` reemplaza las secciones de esa fuente.

## 5. Consultar con citas verificadas

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
5. `handoff-gate out --strict` (el artefacto sale con veredicto).
6. `brief-journal add --run-audit`.
7. Entregar con el veredicto y las incógnitas declaradas.

Al **recibir** un handoff: `handoff-gate in` antes de usarlo. Un claim sin cita que resuelva no
entra a mi brief.

## Errores que este skill previene

- Entregar un brief limpio pero sin etiquetas (el caso `sprint-9-validation.md`: FAIL por label).
- Citar `archivo#L200` en un archivo de 80 líneas (cita fuera de rango).
- Presentar un link que no abrí como "verificado" (sale `unknown`, no `ok`).
- Aceptar de otro agente "esto ya estaba resuelto" sin cita (lección `delegation-result-verification`).

## Límites

- El check de `labels` es heurístico: un falso positivo se resuelve etiquetando, **no** apagando el
  check. `ROADMAP.md` está eximido (es un mapa de madurez, no un brief).
- No publica, no commitea, no sale del workspace.
