# Progreso del curso — Godot 3D RPG

> Estado de estudio por módulo. La clase (`outline.md`) es la referencia; esto es dónde estamos parados.

| Módulo | Capítulos oficiales | Clase montada | Estudiado | Práctica | Notas |
|---|---|---|---|---|---|
| **0** — Arranque y estructura | Intro, Starting The Project | ✅ | ✅ 2026-11-11 | `practicas/m0/probe.gd` | Ver `practicas/m0/LECCION.md`. Hallazgo: el curso es de 4.3, corremos 4.7.2 — la conversión automática no cubre cambios de comportamiento. |
| **1** — GridMap y WorldEnvironment | GridMap, World Environment | ✅ | ⬜ | — | Próximo. |
| **2** — Player: cámara, movimiento, animación | Adding The Player → Player Animation | ✅ | ⬜ | — | `AnimationTree` con `BlendSpace` cambió en 4.7 (`sync_mode`), ojo. |
| **3** — Monstruo y concepto de FSM | Monster Setup → Monster AnimationTree | ✅ | ⬜ | — | |
| **4** — FSM en código | State Machines → Changing States | ✅ | ⬜ | — | |
| **5** — Daño en ambos sentidos | Player Damaging Monsters → Monster Damaging Player | ✅ | ⬜ | `check_attack_timing.py` | Ya tiene artefacto propio (gate en rojo contra reinos). |
| **6** — GUI, tema y pausa | Custom Theme → GUI Setup | ✅ | ⬜ | — | |
| **7** — Items como Resource | Item Resources → Inventory Slot | ✅ | ⬜ | — | |
| **8** — Inventario vivo | Inventory Item → Equipment and using items | ✅ | ⬜ | — | |
| **9** — Perfil, stats y señales | Profile → Custom Health Signals | ✅ | ⬜ | — | |
| **10** — Items 3D, tienda, level up | 3D Item Objects → Level up | ✅ | ⬜ | — | |
| **11** — Forward+ y ambiente | Porting to Forward+ → Torch | ✅ | ⬜ | — | |
| **12** — VFX con Lelu | Lelu Intro → Lelu VFX Tutorial | ✅ | ⬜ | — | |
| **13** — Integración final | Applying The VFX → Outro | ✅ | ⬜ | — | |

## Método de estudio

Cada módulo se estudia con **cuatro fuentes**, en este orden:

1. **El transcript** — qué dice el curso, con timestamps verificados.
2. **El doc oficial de Godot 4.7** — qué cambió desde 4.3, porque el curso tiene dos años y medio.
3. **Conocimiento propio** — para lo que el curso asume y no explica (por qué el `AnimationTree` funciona así, qué es un `BoneAttachment3D`).
4. **Práctica en la máquina** — una sonda o test que corre y da salida real. Sin eso es apunte, no aprendizaje.

Los hallazgos del curso que no aplican a nuestra arquitectura (RTS por ticks, no tercer-persona) se registran igual con el motivo. Un «esto no aplica» escrito vale lo mismo que un «esto sí».

## Investigaciones pendientes de Vane

Si un módulo pide un dato que no puedo verificar sin navegar profundo (discusiones de issues, comparativas de addons, benchmarks de terceros), sale el prompt para que lo corra Vane y vuelve como fuente.

- Módulo 2 (cámara): ninguna pendiente.
- Módulo 5 (ventana de ataque): confirmar si algún addon de Godot resuelve hitboxes animadas en simulación por ticks — **no urgente**, el gate ya marca el defecto.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
