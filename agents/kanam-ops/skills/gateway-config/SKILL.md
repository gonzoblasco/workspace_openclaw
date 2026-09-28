---
name: "gateway-config"
description: "Gateway configuration management with runtime editing, health checks, and change tracking."
---

# OpenClaw Gateway Config

## Descripción
This skill provides a web-based interface and API to view and edit the OpenClaw Gateway configuration at runtime without requiring restarts. It allows safe configuration management for agents and operations teams.

## Funcionalidades clave
- Ver configuración actual del gateway en tiempo real
- Editar/actualizar archivos de configuración
- Guardar cambios con confirmación
- Monitorear estado del gateway
- Logs de auditoría de cambios de configuración

## Requisitos
- Tener acceso de escritura al directorio de configuración del gateway
- Docker corriendo (para la interfaz web)

## Uso
- Interfaz web: `http://localhost:8080/config` (requiere Docker)
- La configuración del gateway se edita con `openclaw` (ver skill `gateway-config` del sistema)

## Auditoria de plugins (ahorro de recursos)
Cuando pidan revisar que plugins activar/desactivar o reducir el footprint del gateway:

1. Correr `openclaw status` para el overview (plugins habilitados, sesiones, heartbeat).
2. Obtener el inventario real con `openclaw plugins list --json` y parsearlo con python (campos `id` + `enabled`). El subcomando `openclaw plugins enabled` NO existe, y parsear la tabla con grep/awk pierde campos: usar siempre `--json`.
3. Leer `openclaw.json` y extraer las claves de `models.providers` - es la lista real de proveedores configurados.
4. Cruzar ambos: todo plugin de proveedor habilitado cuyo id NO este en `models.providers` ni tenga credenciales en `~/.openclaw/credentials/` es candidato a desactivar (inyecta tools al catalogo del agente sin uso real).
5. Revisar ademas: plugins de SO incorrecto para el host (ej. `linux-node` en macOS), stack de voz no usado (`azure-speech`, `talk-voice`, `tts-local-cli`), y experimentales sin uso (`cua-computer`).
6. Entregar la recomendacion en tabla: desactivar (con motivo especifico), activar (solo si una skill existente del workspace lo justifica, ej. `memory-wiki` con la skill `memory-wiki-workflow`), y dejar como esta (core: `ollama`, `memory-core`, `workboard`, `browser`, `file-transfer`, `device-pair`, `web-readability`, `document-extract`, `canvas`).
7. Los cambios requieren OK del usuario y se aplican con `openclaw plugins disable/enable` (via oficial), que reinicia el gateway - nunca editar plugins a mano en el JSON.
