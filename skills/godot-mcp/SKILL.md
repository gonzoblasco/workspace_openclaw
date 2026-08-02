---
name: "godot-mcp"
description: "Build and modify Godot 4.x games from OpenClaw via MCP. Create scenes, scripts, resources, animations, and run/export projects."
---

# Godot MCP — Build games from OpenClaw

Control Godot 4.x desde OpenClaw usando el MCP server `@yanhuifair/godot-mcp` (282 tools, 26 categorías). Podés crear escenas, scripts, recursos, animaciones, y correr/exportar proyectos enteros sin abrir Godot manualmente.

## Requisitos

- Godot 4.x instalado (actual: `/Applications/Godot.app`)
- Node.js >= 18
- Proyecto Godot existente (con `project.godot`)

## Setup

### 1. Arrancar el MCP server

```bash
cd /path/to/godot/project
npx @yanhuifair/godot-mcp -t streamable-http --port 9877 -p .
```

El server queda escuchando en `http://127.0.0.1:9877/mcp` (Streamable HTTP).

### 2. Inicializar sesión MCP

```bash
# Initialize
curl -s -X POST http://127.0.0.1:9877/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-03-26","capabilities":{},"clientInfo":{"name":"openclaw","version":"1.0"}}}'

# Guardar el mcp-session-id del response header para usarlo en llamadas siguientes
```

### 3. Enviar initialized notification

```bash
curl -s -X POST http://127.0.0.1:9877/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id>" \
  -d '{"jsonrpc":"2.0","method":"notifications/initialized"}'
```

## Tools principales (las que más se usan)

### Escenas
| Tool | Args | Descripción |
|---|---|---|
| `create_scene` | `path`, `template` ("Node2D"\|"Control"\|"Node3D"), `root_name?` | Crear escena desde template |
| `add_node` | `scene_path`, `name`, `type`, `parent_path?`, `properties?`, `groups?` | Agregar nodo a escena |
| `remove_node` | `scene_path`, `node_path` | Eliminar nodo |
| `set_property` | `scene_path`, `node_path`, `property`, `value` | Cambiar propiedad de nodo |
| `read_scene` | `path` | Leer escena como JSON (árbol completo) |
| `modify_scene_node` | `scene_path`, `node_path`, `properties` | Modificar propiedades de nodo en archivo |
| `remove_scene_node` | `scene_path`, `node_path` | Eliminar nodo de archivo de escena |

### Scripts
| Tool | Args | Descripción |
|---|---|---|
| `write_script` | `path`, `content`, `create_backup?` | Escribir/sobrescribir script GDScript |
| `read_script` | `path` | Leer script con line numbers |
| `attach_script` | `scene_path`, `node_path`, `script_path` | Attachar script a nodo |
| `validate_script` | `path` | Validar sintaxis GDScript |
| `add_script_function` | `path`, `function_code`, `after_line?` | Agregar función a script existente |
| `add_script_export` | `path`, `export_code`, `after_line?` | Agregar @export a script |
| `search_in_scripts` | `pattern`, `path?` | Buscar en scripts |

### Recursos
| Tool | Args | Descripción |
|---|---|---|
| `create_resource` | `path`, `type`, `properties?` | Crear recurso .tres |
| `write_resource` | `path`, `properties` | Modificar recurso existente |
| `read_resource` | `path` | Leer recurso como JSON |

### Proyecto
| Tool | Args | Descripción |
|---|---|---|
| `list_project_files` | `pattern?`, `extension?` | Listar archivos del proyecto |
| `read_project_settings` | — | Leer project.godot como JSON |
| `write_project_config` | `key`, `value` | Escribir config en project.godot |
| `write_input_action` | `action_name`, `key`, `deadzone?` | Crear input action |
| `manage_autoloads` | `action` ("add"\|"remove"\|"list"), `path?`, `name?` | Gestionar autoloads |
| `manage_export_presets` | `action`, `name?`, `platform?` | Gestionar export presets |

### Editor (requiere Godot abierto)
| Tool | Args | Descripción |
|---|---|---|
| `editor_play` | — | Correr escena (F5) |
| `editor_stop` | — | Detener (F8) |
| `editor_screenshot` | `path?` | Screenshot del editor |
| `editor_select_node` | `node_path` | Seleccionar nodo en editor |
| `editor_set_breakpoint` | `script_path`, `line` | Poner breakpoint |
| `editor_run_gdscript` | `code` | Ejecutar GDScript en editor |

### Godot Engine
| Tool | Args | Descripción |
|---|---|---|
| `launch_editor` | — | Abrir Godot editor |
| `run_project` | — | Correr proyecto |
| `export_project` | `preset_name`, `output_path` | Exportar build |
| `get_godot_version` | — | Versión de Godot |

## Workflow: construir un juego

### Fase 1: Setup del proyecto
1. Crear carpeta del proyecto con `project.godot` básico
2. Arrancar MCP server
3. Inicializar sesión MCP
4. Configurar proyecto (resolución, input map, autoloads)

### Fase 2: Escena principal
1. `create_scene` con template adecuado (Node2D/Node3D/Control)
2. Agregar nodos: `add_node` con tipo y nombre
3. Configurar propiedades: `set_property` o `modify_scene_node`
4. Crear scripts: `write_script` con contenido completo
5. Attachar scripts: `attach_script`

### Fase 3: Iteración
1. `read_scene` para ver estado actual
2. `read_script` para ver código
3. Modificar con `write_script`, `add_script_function`, `add_script_export`
4. Agregar más nodos, recursos, animaciones

### Fase 4: Prueba y export
1. `launch_editor` para abrir Godot
2. `editor_play` / `editor_stop` para probar
3. `export_project` para build final

## Notas importantes

- **Sesión MCP**: el session-id se obtiene del header `mcp-session-id` en el response de `initialize`. Usar el mismo para todas las llamadas.
- **Streamable HTTP**: usa POST a `/mcp` con header `Accept: application/json, text/event-stream`. Las responses vienen como SSE `event: message\ndata: {...}`.
- **Nombres de parámetros**: usar snake_case exacto del schema. El server normaliza camelCase a snake_case para 30+ parámetros comunes, pero no confiar en eso.
- **Parser propio**: las tools de archivo (scene, script, resource) no necesitan Godot abierto — el server parsea .tscn/.tres/.gd directamente en TypeScript.
- **Editor bridge**: para tools del editor, el server spawns Godot automáticamente si no está corriendo.
- **Backups**: `write_script` y `write_resource` crean `.bak` por defecto. Pasar `create_backup: false` para evitar.
- **Path traversal**: todas las operaciones de archivo validan que la ruta esté dentro del proyecto.
- **Read-only mode**: flag `--read-only` para operaciones seguras.

## Referencia rápida de curl

```bash
# Llamar a cualquier tool
curl -s -X POST http://127.0.0.1:9877/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id>" \
  -d '{
    "jsonrpc": "2.0",
    "id": <id>,
    "method": "tools/call",
    "params": {
      "name": "<tool_name>",
      "arguments": { ... }
    }
  }'

# Listar todas las tools disponibles
curl -s -X POST http://127.0.0.1:9877/mcp \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <session-id>" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "tools/list",
    "params": {}
  }'
```

## Categorías completas (282 tools)

El server tiene tools en 26 categorías. Las principales además de las listadas arriba:

- **Animation**: add_animation_library, add_animation_track, add_keyframe, etc.
- **Audio**: add_audio_bus, add_audio_effect, set_bus_volume, etc.
- **Physics**: create_physics_material, set_collision_layer, etc.
- **Navigation**: create_navigation_region, bake_navmesh, etc.
- **TileMap**: read_tileset, write_tilemap_layer, etc.
- **Shader Graph**: add_shader_node, connect_shader_nodes, set_shader_param, etc.
- **Mesh**: create_mesh_instance, set_mesh, etc.
- **Environment**: read_environment, write_environment, apply_preset, etc.

Para ver la lista completa en cualquier momento: `tools/list` y filtrar por nombre.
