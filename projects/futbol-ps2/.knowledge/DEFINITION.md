# DEFINITION — Juego de Fútbol 3D (FIFA/PES PS2-like)

## Nombre tentativo

_Pendiente — se definirá cuando el juego tenga personalidad_

## Visión

Un juego de fútbol 3D que capture la sensación de los FIFA / Pro Evolution Soccer de PlayStation 2. Cámara dinámica, físicas creíbles, controles simples. Proyecto personal en Godot 4.

## MVP

**"Un partido. Una cancha. Una pelota."**

### Scope del MVP

| Feature | Incluido | Notas |
|---------|----------|-------|
| Cancha 3D (césped, líneas, arcos) | ✅ | Modelado básico, texturas simples |
| 2 equipos genéricos (Local/Visitante) | ✅ | Colores distintos, sin nombres reales |
| 11 jugadores por equipo | ✅ | Modelos 3D simples, sin rostros |
| Pelota con físicas | ✅ | Peso, rozamiento, rebote |
| Humano vs CPU | ✅ | 1 jugador controla un equipo |
| Controles teclado | ✅ | Flechas + teclas de acción |
| Pase | ✅ | A jugador más cercano en dirección |
| Tiro | ✅ | Al arco |
| Correr (sprint) | ✅ | Tecla de aceleración |
| Cámara dinámica | ✅ | Sigue la pelota, rotación suave, estilo PS2 |
| Marcador en pantalla | ✅ | Tiempo, goles, minuto actual |
| Arquero automático | ✅ | Controlado por IA, no por el jugador |
| Gol | ✅ | Detección, celebración básica, saque de centro |
| Saque de centro | ✅ | Al iniciar y después de cada gol |
| Saque de meta | ✅ | Cuando la pelota sale por línea de fondo |
| Saque de banda | ✅ | Cuando la pelota sale por línea lateral |
| Duración: 5 min (2T de 2:30) | ✅ | Configurable a futuro |
| Sonido básico | ⚠️ | Mínimo: silbato, gol, ambiente |
| Reglas avanzadas (offside, faltas) | ❌ | Post-MVP |
| Tarjetas | ❌ | Post-MVP |
| Cambios de jugadores | ❌ | Post-MVP |
| Formaciones / tácticas | ❌ | Post-MVP |
| Selección de equipos | ❌ | Post-MVP (equipos fijos) |
| Menú principal | ❌ | Post-MVP (arranca directo) |
| Repeticiones | ❌ | Post-MVP |
| Efecto (curva) en pelota | ❌ | Post-MVP (evaluar después) |

### Controles (teclado)

| Tecla | Acción |
|-------|--------|
| ↑ ↓ ← → | Movimiento del jugador |
| Z | Pase |
| X | Tiro |
| Shift (izquierdo) | Correr (sprint) |
| Espacio | Pausa |

### Flujo del partido

1. Arranca el juego → se posicionan los 22 jugadores en la cancha
2. Silbato inicial → saque de centro
3. La cámara sigue la pelota con movimiento suave
4. El jugador controla al jugador más cercano a la pelota de su equipo
5. Si la pelota sale del campo → saque de banda o de meta según corresponda
6. Gol → celebración breve, reinicio con saque de centro
7. A los 2:30 → entretiempo (pausa breve, cambian de lado)
8. A los 5:00 → fin del partido, pantalla de resultado

### Criterios de calidad

- **FPS:** 60 estables en Mac Mini (M1/M2)
- **Físicas:** La pelota se siente con peso, no flota, no va a velocidad absurda
- **Cámara:** Suave, no mareosa, siempre muestra la acción
- **IA:** La CPU corre, pasa, tira al arco. No es inteligente pero tampoco se queda quieta
- **Controles:** Responsivos, sin input lag perceptible

## Post-MVP (futuro)

- Menú principal con selección de equipos
- Más equipos (con nombres y colores reales)
- Torneo / liga
- Offside, faltas, tarjetas
- Córners, tiros libres
- Efecto en la pelota
- Repeticiones
- Sonido completo (hinchada, relator)
- 2 jugadores locales
- Gamepad support
- Modo entrenamiento (penales, tiros libres)

## Stack técnico

- **Motor:** Godot 4.4+
- **Lenguaje:** GDScript
- **Físicas:** Jolt Physics 3D
- **Modelado:** Blender (modelos simples, low-poly estilizado)
- **Animaciones:** Godot AnimationTree + blend spaces
- **IA:** State machine + steering behaviors
- **Cámara:** Godot Camera3D + interpolación suave
