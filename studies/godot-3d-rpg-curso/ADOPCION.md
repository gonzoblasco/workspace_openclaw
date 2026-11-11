# Adopción: Godot GameDev Tutorial – 3D RPG Game

Fecha de revisión: 2026-11-11
Curso: [outline.md](outline.md) · [transcripcion.md](transcripcion.md)
Proyecto usado como caso: `projects/reinos-de-la-frontera` (RTS medieval, Godot 4.7, simulación por ticks)

## Veredicto

**Adopción parcial, un artefacto.**

El curso es un tutorial de **tercer-persona en tiempo real**, y el proyecto que tenemos es un **RTS de simulación por ticks** con lógica headless separada de la vista. La mayor parte del curso no aplica: `CharacterBody3D` + `Input.get_vector` + `move_and_slide` es exactamente lo que *no* hace un RTS. Las secciones de GUI, tienda e inventario tampoco aportan nada que no esté ya decidido.

Lo que sí muerde es una idea concreta del **Módulo 5**: *el daño no se aplica cuando se decide atacar, sino en la ventana exacta del golpe, y esa ventana se puede cancelar.*

## Tabla de adopción

| Idea del curso (con t=) | Qué hacemos hoy | Artefacto verificable |
|---|---|---|
| «this is kind of a more accurate way of detecting for a specific frame» (02:01:19) — el `Area3D` del arma se habilita en el frame del impacto por un *property track*, y se deshabilita inmediatamente | En `projects/reinos-de-la-frontera/sim/sim_state.gd` el daño se aplica **en el mismo bloque** que decide atacar (`if ent.attack_timer <= 0:` → `ent.hp = max(0, ent.hp - dmg)`), sin ventana intermedia ni cancelación | `check_attack_timing.py` — corrido abajo, **falla** contra el repo actual |

## El artefacto, corrido

```console
$ python3 studies/godot-3d-rpg-curso/check_attack_timing.py projects/reinos-de-la-frontera
FAIL: la ventana de ataque no esta enmarcada
  - El dano se resuelve en el mismo tick que se decide atacar (sin windup). Un atacante que se mueve en el tick siguiente ya hizo dano igual.
EXIT=1
```

Salida pegada de la corrida real del 2026-11-11, EXIT `1`.

## Por qué el defecto es real y no teórico

El código de `sim_state.gd` ordena las fases así: primero movimiento, después `attack_timer -= 1`, después resolución de ataques. Cuando una unidad consigue `attack_target_id` y está en rango, **el daño se aplica en ese mismo tick** y el cooldown arranca después.

Consecuencia medible: una unidad que empieza a atacar y en el tick siguiente recibe una orden de `move` (o la IA le cambia el objetivo) **ya hizo daño completo**. No hay estado intermedio entre «voy a atacar» y «pegué».

El curso resuelve exactamente eso con una ventana explícita: el arma no está activa todo el tiempo, está activa *entre dos keyframes*. En la simulación, el equivalente es:

1. Un campo de windup (`windup_ticks`) que arranca cuando se decide atacar.
2. La resolución del daño recién cuando `windup_ticks` llega a 0.
3. Cancelación — `windup_ticks = -1` — si el atacante cambia de objetivo, se mueve, o el objetivo muere.

El gate pasa cuando las tres piezas existen y la cuarta (cancelación) está efectivamente cableada, no solo declarada.

## Descartados (y por qué)

- **Cámara `SpringArm3D` / movimiento relativo a cámara** (Módulo 2): un RTS usa cámara cenital ortográfica con scroll y zoom, no un brazo con colisión. No hay problema que arreglar. Cobertura: `view/` del proyecto ya lo resuelve.
- **`AnimationTree` con condiciones** (Módulo 3): el player 3D no existe en el juego; las unidades son sprites/glTF con animación simple. La FSM en código (Módulo 4) **sí** tiene una equivalencia parcial con el estado de la IA, pero el campo `ent.state` ya es un enum de strings y cubre lo mismo a esta escala.
- **Tema 9-patch / pausa / `process_mode`** (Módulo 6): el proyecto no usa pausa del `SceneTree` (la simulación avanza por tick con `clock.gd`); pausar el árbol no pausaría la simulación. La idea no aplica por arquitectura, no por falta de ganas.
- **Inventario con `Resource`** (Módulos 7-8): el RTS no tiene inventario de jugador; la economía vive en `economy.gd` con definiciones por JSON.
- **VFX con `VisualShader` y `GPUParticles3D`** (Módulo 12): Lelu es excelente y es refería real para efectos, pero hoy el proyecto no tiene pipeline de VFX y agregarlo no arregla un defecto. Queda como candidato para E4+, no como adopción de este curso.
- **Spawn sobre GridMap** (Módulo 13): el proyecto ya resuelve colocación con `pathfind.set_solid` y `_free_adjacent`; la validación de celda del tutorial es un caso más chico.

## Lo que sigue pendiente

El artefacto quedó **corriendo en rojo**. Eso es intencional: registra un defecto real del simulador. Se arregla en `reinos-de-la-frontera` cuando toque la iteración de combate (post-E3), no en la sesión que montó la clase.

Si se arregla, el mismo script tiene que pasar a verde sin cambiar el script: si hay que tocarlo, el gate estaba midiendo la forma y no la conducta.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
