# EVALUATION — Juego de Fútbol 3D (FIFA/PES PS2-like)

## 1. Análisis de Mercado

### Competidores directos (juegos de fútbol open source en Godot)

| Proyecto | Tipo | 3D | Estado | Estrellas |
|----------|------|----|--------|-----------|
| SuperSoccer (hanmi255) | Pixel art 2D | ❌ | Activo | ~3 |
| Godot Basic 3D Football | Prototipo 3D básico | ✅ | Abandonado 2018 | ~19 |
| Football Dribble Match 3D | Arcade 3D | ✅ | En desarrollo | - |
| AWC (nicosoftarg) | Arcade World Cups | ❌ 2D | Reciente | 0 |
| Soccer Online (AhkunTa) | 2D pixel art online | ❌ | Activo | ~1 |

**Conclusión:** No hay competencia directa. Nadie está haciendo un FIFA-like 3D serio en Godot. El espacio está vacío.

### Competidores indirectos (juegos de fútbol comerciales)

- EA Sports FC (antes FIFA) — el estándar, pero cerrado, caro, pesado
- eFootball (antes PES) — free-to-play, pero online-focused y cerrado
- **Ventana:** No hay alternativa open source que capture la experiencia de un partido de fútbol 3D

## 2. Viabilidad Técnica

### Godot 4 + Jolt Physics 3D

**Lo que Godot 4 nos da out of the box:**
- ✅ Motor 3D completo (luces, sombras, materiales, shaders)
- ✅ Jolt Physics 3D (colisiones, cuerpos rígidos, detección de contacto)
- ✅ Sistema de animaciones (AnimationTree, blend spaces, state machines)
- ✅ Input handling (teclado, gamepad)
- ✅ Audio 3D posicional
- ✅ Sistema de escenas y herencia (ideal para jugador, pelota, arco)
- ✅ Export a Windows, Mac, Linux, Web (WASM)

**Lo que necesitamos construir:**
- 🔧 Motor de físicas de fútbol (toque, pase, tiro, efecto, rebote)
- 🔧 IA de jugadores (posición, marcación, desmarque, pressing)
- 🔧 IA de equipos (formación, tácticas, cambios)
- 🔧 Cámara dinámica (sigue la pelota, rota, zoom)
- 🔧 Sistema de reglas (fuera de juego, faltas, saques, corners)
- 🔧 Modelos 3D (jugadores, cancha, arcos, pelota)
- 🔧 Animaciones (correr, patear, cabecear, tackle, arquero)
- 🔧 UI/UX (marcador, menús, selección de equipos)

### Riesgos técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|---------|------------|
| Físicas de pelota no se sienten reales | Media | Alto | Iterar con valores reales (masa, rozamiento, restitución) |
| IA de jugadores muy básica / robótica | Alta | Alto | Empezar con comportamientos simples, iterar |
| Animaciones se ven tiesas | Media | Medio | Usar blend spaces, captura de movimiento aproximada |
| Cámara dinámica mareosa | Baja | Medio | Suavizado, límites de rotación, opciones de cámara |
| Rendimiento en escenas con 22 jugadores | Baja | Medio | LOD, instancing, optimización de mallas |

### Tiempo estimado (proyecto personal, sesiones intermitentes)

- **MVP (partido jugable 1vs1 CPU):** ~2-3 meses
- **Versión completa (múltiples equipos, torneo, modos):** ~6-9 meses
- **Madurez (pulido, sonido, menús, equilibrio):** ~12+ meses

## 3. Fit Estratégico

### ¿Por qué este proyecto para Gonzo?

1. **Portfolio técnico:** Un juego 3D en Godot demuestra capacidades que ningún proyecto web puede: físicas, IA, animación 3D, optimización de rendimiento, game design
2. **Diferenciación:** Mientras otros devs tienen clones de Twitter o dashboards, vos tenés un FIFA-like. Eso se muestra.
3. **Aprendizaje:** Godot 4, GDScript, shaders, físicas 3D, IA de comportamiento — skills transferibles
4. **Diversión:** Es un proyecto que querés jugar. Eso mantiene la motivación.

### ¿Por qué ahora?

- Godot 4 está maduro (4.4+)
- Jolt Physics 3D ya viene incluido
- No hay competencia open source en este espacio
- Es un proyecto personal sin presión de deadlines — ideal para aprender

## 4. Veredicto

**GO.** El proyecto es técnicamente viable, no tiene competencia open source, y es un portfolio piece único. El riesgo principal es la complejidad de la IA y las físicas, pero se puede mitigar iterando desde un MVP muy chico.

**Próximo paso:** Definir el MVP mínimo (DEFINITION.md).
