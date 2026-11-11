# Reinos de la Frontera

RTS medieval isométrico para un jugador contra la IA, en Godot 4.7.2 sobre macOS Apple Silicon. Proyecto personal, desde cero: no reutiliza código, arte, datos ni narrativa de otros proyectos.

## Estado

**Fase 0 cerrada.** Hay repo, estructura de carpetas, una escena mínima que abre y tests de humo. **No hay gameplay, ni assets, ni UI de juego.**

La escena mínima valida tres cosas: cámara ortográfica a 30° (pitch −30°, yaw 45°, `size=14`), una referencia de 1 tile = 1 m (cubo) y una referencia de personaje de 1,8 m (cápsula). La captura está en `docs/captures/fase0.png`.

## Requisitos

- Godot **4.7.2.stable.official.ed1daf0bf** (Apple Silicon).
- macOS con Metal 4.

## Abrir y ejecutar

```bash
cd /Users/gonzoblasco/.openclaw/workspace/projects/reinos-de-la-frontera

# Editor
godot -e --path .

# Juego (escena mínima)
godot --path .
```

No corras `godot --path .` desde otra carpeta: abre el project manager vacío y `res://` deja de resolver.

## Tests

```bash
# Afirma cámara ortográfica, escala del piso, cubo y cápsula
godot --headless --path . --script res://tests/scaffold_test.gd
# SCAFFOLD_OK

# Humo del motor
godot --headless --path . --script res://tests/headless_test.gd
# HEADLESS_OK
```

## Captura

```bash
godot --path . --write-movie docs/captures/fase0.png --quit-after 3 --fixed-fps 60
```

Genera frames numerados en `docs/captures/`; el último es el válido. La corrida de referencia dio 1600×900, Metal 4.0 Forward+.

## Estructura

```
reinos-de-la-frontera/
├─ project.godot          # Godot 4.7.2, 1600×900, forward_plus
├─ main.tscn              # escena mínima de referencia (sin gameplay)
├─ sim/                   # stubs: estado, comandos, economía, combate, edades, pathfind, IA, RNG
├─ view/                  # stubs: mundo, unidades, edificios, cámara, selección, niebla, barras
├─ ui/                    # stubs: HUD, minimapa, menús
├─ tests/                 # scaffold_test.gd, headless_test.gd + stubs de sim
├─ data/                  # units/buildings/techs/civs.json vacíos con schema_version
├─ assets/CREDITS.md      # regla "sin ficha no entra"; fuentes verificadas para E0
├─ docs/captures/         # evidencia visual
└─ .knowledge/            # BRIEF, DECISIONS, STATUS, HANDOFF
```

## Licencias

- El código no declara licencia pública: el proyecto es personal y no se distribuye.
- Los assets de terceros se registran en `assets/CREDITS.md` antes de entrar. Sin ficha no entra.
- Los binarios de Quaternius no se commitean: por peso y orden, no por licencia.

## Próximo paso

**E0 — spike gráfico de 5 días** (§4.9 del documento de arranque): cámara ortográfica, un modelo a escala, 200 unidades caminando y FPS medidos en la M4. El spike decide si el camino es 3D runtime o 2D pre-render. No se construye nada encima hasta que pase.

Documento que manda: `../../docs/reinos-de-la-frontera-documento-de-arranque.md`.
