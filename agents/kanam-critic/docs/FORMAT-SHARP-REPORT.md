# format_sharp_report — publicar un veredicto donde el autor trabaja

**Qué resuelve:** el veredicto del Critic vive en `docs/reviews/*.md` y en `memory/verdicts.jsonl`.
El autor del cambio no entra ahí. Esta herramienta convierte un veredicto en el cuerpo de un
comentario de PR, sin editar nada a mano y sin inventar un número.

## Uso

```bash
python3 bin/format_sharp_report.py \
  --report docs/reviews/<fecha>-<artefacto>.md \
  --ledger memory/verdicts.jsonl \
  --artifact <slug> \
  [--dry-run] [--body-file <ruta>]
```

- Sin flags: imprime el cuerpo a stdout.
- `--dry-run`: imprime el cuerpo y el comando que se ejecutaría, y **no escribe nada**.
- `--body-file`: escribe el cuerpo para `gh pr comment <PR> --body-file`.

## Qué valida antes de emitir

| Condición | Resultado |
|---|---|
| El artefacto no existe en el ledger | exit 2, nombra el faltante |
| Hay más de una fila para el artefacto | exit 2 |
| La fila está invalidada | exit 2, con el motivo |
| El total del reporte no coincide con el ledger | exit 2 |
| El veredicto declarado no coincide con la matriz | exit 2 |
| Falta algún eje SHARP en el reporte | exit 2, nombra cuál |

## Estructura del cuerpo

1. `**Veredicto: <nombre> <total>/25** (S H A R P)` — una línea, siempre.
2. Tabla SHARP con la justificación textual del reporte.
3. Evidencia cruda del reporte en un `<details>` colapsado.
4. Fricciones. Si el reporte no las declara, lo dice: no afirma ausencia que no verificó.

Límite de 60 000 caracteres: se recorta **solo la evidencia**, con aviso explícito. El veredicto
y las fricciones nunca se truncan.

## Lo que no hace

- No puntúa: eso es del Critic.
- No publica: el `gh pr comment` lo corre un humano o el CORE con autorización explícita.
- No completa ejes desde el ledger salvo el caso declarado abajo, y lo avisa en el cuerpo.
