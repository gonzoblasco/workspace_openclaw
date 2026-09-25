# HANDOFF - kanam-story-bible

## Session Context

- **Ultima sesion:** 2026-09-25 00:54 (America/Buenos_Aires)
- **Branch:** `main` en `github.com/gonzoblasco/kanam-story-bible`
- **Ultimo commit:** `4676b13` fix(ui): spacing came out as 0.0px and wide tables stretched the document
- **Estado:** working tree limpio, todo pusheado

## What was done

Sesion que arranco como un fix puntual y termino cubriendo apply, recuperacion de datos y
layout. Cuatro commits en el proyecto mas dos de documentacion en el workspace.

1. **`fix(apply)` - el candado es por candidato, no por job.** Aplicar una propuesta
   cerraba el job entero y las demas devolvian `409`. Causa: `generation_job.aplicado`
   era un booleano del job para una operacion por candidato. Ahora
   `candidatos_aplicados` (jsonb) + `applied_candidates` en el contrato.
2. **Migracion 003 - recomputo de aplicados.** El backfill de 002 marcaba todos los
   candidatos como aplicados; los que nunca entraron quedaban bloqueados para siempre.
   El estado se deriva ahora de `card.generacion_id`.
3. **Recuperacion.** Historial de generaciones en la UI, Papelera + restore,
   `DELETE /projects/{id}` con confirmacion por titulo, campo `instruccion` en el job.
4. **Layout.** Tabs con `flex-wrap`; espaciado desde el contenedor (gap 0.0px -> 24px);
   `position: relative` en `.tablaWrap` para contener los `sr-only` absolutos.
5. **Herramienta: `scripts/ui-shot.mjs`** - Chromium por CDP, captura y medicion de
   layout/desborde al ancho pedido.

## Como verificar

```bash
# Stack (Colima corriendo)
make up && make init          # api en :8080

# Verificacion completa
python3 scripts/smoke.py      # 64 aserciones
python3 scripts/verify_apply.py  # 14 aserciones del ciclo de apply
docker compose -f compose.dev.yml exec -T api sh -c "cd /app && ruff check src tests && MYPYPATH=/app/src mypy --ignore-missing-imports src/kanam"

# UI
cd ui && npx vitest run       # 9 tests
npx tsc -b && npm run build

# Medir layout (reproduce el ancho del panel lateral del Control UI)
cd .. && W=420 TAB=Generar OUT=/tmp/g.png node scripts/ui-shot.mjs
```

## Estado del mundo (datos de Gonzo)

- **`Cartas sin Mandar`**: 3 fichas (restauradas tras el borrado accidental).
- **`Cloacopolis: Cronica de una Civilizacion Subterranea`**: 6 fichas, incluidos los 2
  lugares que el bug de apply tenia bloqueados y Gonzo aplico a las 02:32 UTC.
- No hay mundos de prueba: se limpiaron los 6 que habian quedado.

## Known issues

- **La base de test no esta separada de la real** (ADR-069). Es la causa del dano que
  hubo en esta sesion. Mitigado con la regla "un script no toca un mundo que no creo",
  pero el arreglo de fondo sigue pendiente.
- El borrado de un mundo es logico (primera fase). No hay endpoint de purga fisica.
- El dev server de Vite corre como proceso de sesion (`neat-bloom`), no como
  LaunchAgent: si se cierra la sesion, se pierde el HMR.

## What's next

1. **Separar la base de test** - es la deuda mas urgente; el dano de esta sesion salio
   de aca. Un `compose.test.yml` con su propio volumen, o un schema por test.
2. Editor visual del outline (hoy la vista lo lee).
3. Edicion de atributos de una ficha existente.
4. Worker ARQ real (el outbox se drena por endpoint).
5. Autenticacion `token` + scopes.

## Leer antes de tocar

- `.knowledge/DECISIONES.md` - contrato en ingles / dominio en espanol, presupuesto de
  tokens de razonamiento, y la seccion de recuperacion con la leccion comun.
- `.knowledge/STATUS.md` - estado real, deuda y como recuperar cosas.
- `CHANGELOG.md` - v0.3.0 con las causas raiz de cada fix.
- `docs/adr/ADR-069` y `ADR-070` en el workspace.
