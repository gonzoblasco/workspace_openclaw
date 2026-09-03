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


