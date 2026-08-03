# Godot Journey — Aprender Godot 4.7 juntos

## BRIEF

Gonzo quiere aprender Godot paso a paso, de modo interactivo. No es "construir un juego de un prompt" — es un viaje de aprendizaje compartido, hito por hito, prueba y error, descubriendo juntos qué hay de nuevo en Godot 4.7.

OpenClaw (Kanam) es guía, copiloto y compañera de debug. No construye el juego por Gonzo.

## Stack

- **Engine**: Godot 4.7.1 — `/Applications/Godot.app`
- **MCP Server**: `@yanhuifair/godot-mcp` v1.4.0 (282 tools, Streamable HTTP en port 9877)
- **Skill**: `skills/godot-mcp/SKILL.md` (filosofía learn-together)
- **Helper**: `/tmp/godot-mcp.sh` (wrapper de sesión MCP)

## Hitos

### Hito 1: Primer proyecto y editor
- [ ] Crear proyecto nuevo desde Godot
- [ ] Entender la interfaz: viewport, dock de escena, inspector, sistema de archivos
- [ ] Crear primera escena con un nodo visible
- [ ] Guardar y correr

### Hito 2: Nodos y escenas
- [ ] Árbol de nodos: parent/child
- [ ] Tipos de nodos: Node2D, Sprite2D, CharacterBody2D, StaticBody2D
- [ ] Instancing: reutilizar escenas dentro de escenas
- [ ] Transform: position, rotation, scale

### Hito 3: Scripts y GDScript
- [ ] Attachar script a un nodo
- [ ] _ready, _process, _physics_process
- [ ] Variables, @export
- [ ] Input handling
- [ ] Señales

### Hito 4: Física 2D
- [ ] Collision shapes
- [ ] CharacterBody2D vs StaticBody2D vs RigidBody2D
- [ ] Gravedad y move_and_slide
- [ ] Áreas (Area2D) para detección

### Hito 5: Cámara y UI
- [ ] Camera2D: seguimiento, límites, smoothing
- [ ] CanvasLayer y Control nodes
- [ ] Labels, Buttons, signals de UI

### Hito 6: Game feel
- [ ] Animación (AnimatedSprite2D o _draw)
- [ ] Particles
- [ ] Sound effects
- [ ] Screen shake

### Hito 7: Niveles y progresión
- [ ] TileMapLayer (nuevo en 4.7)
- [ ] Scene switching
- [ ] Save/load
- [ ] Export

## Log de sesión

### 2026-08-02
- Evaluamos 3 MCP servers de Godot, elegimos `@yanhuifair/godot-mcp` (282 tools).
- Instalamos Godot 4.7.1, verificamos que corre.
- Creamos un platformer básico de un prompt (player, ground, monedas, UI, cámara).
- **Gonzo recalibró el enfoque**: no quiere que construya todo. Quiere aprender paso a paso, juntos.
- Eliminamos el proyecto de prueba (`~/godot-test-project`).
- Creamos este documento para trackear el viaje.
- Skill `godot-mcp` reescrita a filosofía learn-together.

## Notas

- Los hitos son flexibles. Se ajustan sobre la marcha.
- Godot 4.7 trae cambios sobre 4.6 que vale la pena explorar (TileMapLayer, Metal backend, mejoras de renderizado).
- Verificar changelog oficial antes de enseñar algo que podría haber cambiado.
- Gonzo trabaja en el editor. OpenClaw asiste con MCP cuando es útil, pero no reemplaza la experiencia de usar Godot.