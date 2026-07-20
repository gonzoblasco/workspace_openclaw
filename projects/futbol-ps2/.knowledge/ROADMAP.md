# ROADMAP — Juego de Fútbol 3D (FIFA/PES PS2-like)

## Filosofía

Cada fase produce algo **jugable**. No hay fases de "infraestructura invisible" — siempre se puede abrir el juego y ver algo nuevo.

---

## Fase 0: Setup del proyecto ⏳ Pendiente

**Duración estimada:** 1 sesión

- [ ] Crear proyecto Godot 4 en `projects/futbol-ps2/`
- [ ] Configurar .gitignore de Godot
- [ ] Primer commit: proyecto vacío con README
- [ ] Configurar export templates (Mac, Windows, Web)
- [ ] Crear escena base (Main.tscn) con nodo raíz

**Output:** Proyecto Godot funcional, primer commit en GitHub

---

## Fase 1: La cancha 🟡 En progreso

**Duración estimada:** 1-2 sesiones

- [ ] Modelar cancha en Blender (rectángulo con césped, líneas, áreas, círculo central)
- [ ] Modelar arcos (postes, red)
- [ ] Modelar pelota (esfera con patrón de hexágonos)
- [ ] Importar a Godot como escenas 3D
- [ ] Iluminación básica (DirectionalLight + ambient)
- [ ] Cámara dinámica que sigue la pelota (Camera3D + interpolación)
- [ ] Texturas básicas (césped verde, líneas blancas)

**Output:** Cancha 3D visible con cámara que se mueve

---

## Fase 2: La pelota

**Duración estimada:** 1-2 sesiones

- [ ] Pelota como RigidBody3D con físicas Jolt
- [ ] Configurar masa, rozamiento, rebote (bounce)
- [ ] Detección de colisiones con el piso, arcos, bordes
- [ ] Gravedad realista
- [ ] La pelota se frena con el rozamiento del césped
- [ ] Rebote en los postes y el travesaño

**Output:** Pelota que se comporta como una pelota de fútbol real

---

## Fase 3: El jugador

**Duración estimada:** 2-3 sesiones

- [ ] Modelar jugador en Blender (cuerpo low-poly estilizado, sin rostro)
- [ ] Importar a Godot como CharacterBody3D
- [ ] Animaciones: idle, correr, patear
- [ ] Movimiento con teclado (WASD / flechas)
- [ ] Sprint (Shift)
- [ ] Colisión del jugador con la pelota (al acercarse, la pelota reacciona)
- [ ] Colisión entre jugadores (choques)

**Output:** Un jugador que corre por la cancha y puede tocar la pelota

---

## Fase 4: El equipo humano

**Duración estimada:** 2-3 sesiones

- [ ] 11 jugadores en la cancha (instancias del modelo)
- [ ] Formación inicial (4-4-2 o similar, posiciones fijas)
- [ ] Control: el jugador controla al miembro de su equipo más cercano a la pelota
- [ ] Pase (Z): la pelota viaja hacia otro jugador del mismo equipo
- [ ] Tiro (X): la pelota viaja hacia el arco contrario con fuerza
- [ ] Cambio automático de jugador controlado (al recibir pase, al acercarse a la pelota)
- [ ] Los otros 10 jugadores del equipo humano se mueven con IA básica (posicionamiento)

**Output:** Un equipo controlable que puede pasar y tirar al arco

---

## Fase 5: La IA (equipo CPU)

**Duración estimada:** 3-4 sesiones

- [ ] State machine por jugador: idle, perseguir pelota, correr a posición, patear
- [ ] Jugador CPU más cercano a la pelota → va hacia ella
- [ ] Jugadores CPU en posición → se mantienen en formación
- [ ] CPU puede pasar la pelota a un compañero
- [ ] CPU puede tirar al arco (cuando está cerca)
- [ ] Arquero CPU: se mueve lateralmente siguiendo la pelota, se lanza cuando hay tiro
- [ ] Dificultad básica (velocidad de reacción, precisión de pase/tiro)

**Output:** Partido jugable humano vs CPU

---

## Fase 6: Reglas básicas

**Duración estimada:** 2 sesiones

- [ ] Detección de gol (pelota cruza la línea de gol)
- [ ] Saque de centro (al iniciar, después de gol)
- [ ] Saque de banda (pelota sale por línea lateral)
- [ ] Saque de meta (pelota sale por línea de fondo, tocada por atacante)
- [ ] Saque de arco (pelota sale por línea de fondo, tocada por defensor)
- [ ] Gol de visitante → festejo básico, reinicio
- [ ] Gol de local → festejo básico, reinicio

**Output:** Partido con reglas de fútbol real

---

## Fase 7: UI y pulido MVP

**Duración estimada:** 2 sesiones

- [ ] Marcador en pantalla (HUD): tiempo, goles, minuto
- [ ] Reloj de partido (5 min, 2 tiempos de 2:30)
- [ ] Pantalla de entretiempo (pausa breve, cambian de lado)
- [ ] Pantalla de resultado final
- [ ] Pausa (Espacio)
- [ ] Sonidos: silbato inicial, silbato final, gol, pelota pateada
- [ ] Cámara: ajustar suavidad, límites de rotación, zoom

**Output:** MVP completo y jugable

---

## Fase 8+: Post-MVP

- Menú principal
- Selección de equipos
- Más equipos
- Offside, faltas, tarjetas
- Córners, tiros libres
- Efecto en la pelota
- Repeticiones
- Sonido completo (hinchada, ambiente)
- 2 jugadores locales
- Gamepad
- Modo entrenamiento
- Torneo / liga
- Export a Web (WASM)

---

## Timeline estimado

| Fase | Sesiones | Estado |
|------|----------|--------|
| 0 — Setup | 1 | ⏳ Pendiente |
| 1 — Cancha | 1-2 | ⏳ Pendiente |
| 2 — Pelota | 1-2 | ⏳ Pendiente |
| 3 — Jugador | 2-3 | ⏳ Pendiente |
| 4 — Equipo humano | 2-3 | ⏳ Pendiente |
| 5 — IA CPU | 3-4 | ⏳ Pendiente |
| 6 — Reglas | 2 | ⏳ Pendiente |
| 7 — UI y pulido | 2 | ⏳ Pendiente |
| **MVP** | **~14-19** | **⏳ Pendiente** |
