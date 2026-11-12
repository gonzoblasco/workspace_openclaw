# HANDOFF - Curso cute-room-portfolio-3d

**Fecha:** 2026-11-12 01:55 GMT-3
**Curso:** Create a Cute Room Portfolio with Blender, Three.js, JavaScript (Andrew Woan, 8:42:31)
**Fuente:** https://www.youtube.com/watch?v=tdsQwuyS6DQ
**Estado:** estudiando — módulo 3 de 13

## Estado

### Clase (2026-11-11)
- `transcripcion.md` (14.576 cues), `outline.md` (13 módulos, 42 capítulos, 30 citas verificadas BAD 0), `video-meta.json`. Commit `e90accbbac`.
- `web-asset-gate.py`: presupuesto de carga de assets 3D web. Corrido contra `reinos-de-la-frontera`.

### Estudio práctico (2026-11-12)
- **Módulo 1 ✅** — vocabulario tri/quad/n-gon, con prueba gráfica (render antes/después de subdividir: el cubo de densidad despareja colapsa, el cilindro se acartona, la esfera se afeita en los polos) y conteo de quads por objeto.
- **Módulo 2 ✅** — bloqueo, pared con `Solidify` + `Bevel` frente a `Extrude`, y la decisión de escena abierta en L (0:58:56).
- **Módulo 3 ⚠️ parcial** — teclado con taper/bevel/espaciador/flechas e inclinación rígida. Mouse sin resolver (dos intentos fallidos).

## Artefacto del curso

`scene-gate.py` — gate de escena con contrato declarado. Detecta HUNDIDO (profundidad),
FLOTANDO (gap), ORIENTACION (`front_axis` vs cámara) y DESPEGADO (`rests_on`).

```
Blender -b estudio.blend --python scene-gate.py            # sobre un .blend existente
Blender -b --python scene-gate.py -- --exec scripts/room.py # construye y chequea
```

Probado: escena rota → 3 hallazgos EXIT=1; escena limpia → 0 hallazgos EXIT=0;
teclado real → 63 HUNDIDO reales.

## Scripts

| Script | Qué hace |
|---|---|
| `scripts/room.py` | Cuarto completo: piso, paredes en L, escritorio 4 patas, silla gamer (6 ruedas, en ángulo), cuadro, cama de Benny, teclado, mouse |
| `scripts/keyboard.py` | Teclado: 63 teclas con taper, espaciador, flechas, inclinado 6° por `matrix_world` |
| `scripts/gate_test_broken.py` | Escena con los 3 errores, para probar que el gate falla |
| `scripts/gate_test_clean.py` | Escena correcta, para probar que no hay falsos positivos |

## Deuda declarada

1. **Teclado hundido 12 mm** en la carcasa. `KEY_HALF` no contempla el taper ni el bevel: hay que calcularlo con la altura real post-modificadores.
2. **Mouse sin forma.** Dos intentos: esfera estirada y tallado de vértices por fórmula. El método correcto es piezas compuestas (esferas unidas + remesh), no matemática a ciegas.
3. **Monitor y silla sin detalle** — siguen siendo bloques.

## Gotchas headless (no están en el video)

- **`bpy.ops.transform.rotate` no hace nada con `-b`.** Sin área 3D en el contexto, retorna sin error y sin efecto. Rotar por `matrix_world`.
- `BLENDER_EEVEE_NEXT` no existe en 5.3: el enum es `BLENDER_EEVEE`.
- `World.use_nodes` deprecado en 5.3 (se remueve en 6.0).
- **Una medición puntual no valida un apoyo.** El raycast decía GAP −0.0009; el conteo de vértices mostraba 12 mm adentro. Medir la pieza entera contra la superficie entera.

## Próximo bloque

**Módulo 4** — silla de oficina, estantes, plantas colgantes con `Particle System` (y por qué se hace `Copy` del sistema antes de tocarlo, 2:56:33). Antes de renderizar: correr el gate.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
