# HANDOFF - Curso godot-3d-rpg-curso

**Fecha:** 2026-11-12 01:47 GMT-3
**Proyecto:** godot-3d-rpg-curso
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Modulo 1 (GridMap + WorldEnvironment) estudiado en profundidad y practicado en la maquina.

Se armo practicas/m1/ con 4 scripts GDScript (build_mesh_library.gd, build_level.gd, test_mesh_library.gd, test_level.gd), un runner run.sh y una captura real m1_shot.png. 22 checks verdes en la corrida final.

Hallazgos:
(1) fog_density=0.2 del curso esta calibrado para una camara a 5 m del jugador; con la camara cenital a 30 m la transmision es 0.2% y el nivel sale gris uniforme. Medido con probe_fog.gd (exp(-0.2*30)=0.002) y bajado a 0.012. Un valor estetico es una tasa por unidad de distancia, no una constante.
(2) El curso crea UN solo GridMap en el modulo 1 y recien en el 11 descubre que las paredes pisan el piso. Se separaron Floor y Walls desde el arranque para no rehacer 40 minutos de nivel.
(3) Make Local es obligatorio al exportar la MeshLibrary: sin el el export guarda una referencia externa que se rompe. Y un item puede quedar sin shape sin error: se ve igual y atraviesa el piso.
(4) Colision visible != colision fisica: la escalera usa un BoxShape3D rotado, no la colision del mesh, para que el player corra suave.

## Estado actual

Modulo 1 cerrado con practica verificada. Modulos 0 y 1 estudiados; 2 a 13 pendientes. Ejercicios del curso ejecutados: 0 (el ejercicio del M1 se resolvio en codigo, no con el editor).

## Proximos pasos

1. Modulo 2 (Player: camara, movimiento, animacion, 00:19:15-01:11:07). Es el modulo mas largo del curso (52 min) y el primero con input real: ahi el test automatico se queda corto y hace falta captura o grabacion. Ojo con AnimationTree/BlendSpace.sync_mode, que cambio en 4.7.
2. [SIN TOCAR, heredado] Arreglar la ventana de ataque en projects/reinos-de-la-frontera: agregar windup_ticks, resolver el dano al llegar a 0 y cancelar (-1) si el atacante cambia de objetivo o se mueve. estudios/godot-3d-rpg-curso/check_attack_timing.py tiene que pasar a verde SIN tocar el script.
3. [SIN TOCAR, heredado] Si no se arregla ahora, el gate queda registrado como deuda con salida roja en ADOPCION.md.
4. [SIN TOCAR, heredado] El indice de git tenia trabajo de otra sesion (check-freshness-display.py, ai-home-dashboard-observatory); quedo intacto en el worktree. No stagear esos archivos.

## Decisiones y contexto que no debe perderse

- M1 confirmo la regla del M0 y la llevo mas lejos: los valores del curso no se copian, se verifican contra la version instalada Y contra la camara/arquitectura propia. fog_density=0.2 es correcto para el curso e inutil para nosotros; el numero no estaba mal, estaba fuera de contexto.
- El orden Floor/Walls en dos GridMap se adopta desde el inicio aunque el curso no lo diga hasta el modulo 11, porque descubrirlo tarde significa rehacer el nivel.
- [SIN TOCAR, heredado] El curso es de tercer-persona en tiempo real y el proyecto es un RTS por ticks: se adopta una sola idea (enmarcar la ventana del golpe) y el resto se descarta con motivo en ADOPCION.md. No se crea skill nueva: el artefacto tiene que sobrevivir a un uso real primero.

## Archivos tocados

```
studies/godot-3d-rpg-curso/PROGRESO.md
```

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
