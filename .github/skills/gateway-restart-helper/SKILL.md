---
name: "gateway-restart-helper"
description: "Automatic gateway restart with health checks and rollback safety."
---

# OpenClaw Gateway Restart Helper

## Descripción
Automatiza el reinicio del OpenClaw Gateway con validación de salud previa y posterior, evitando downtime innecesario.

## Funcionalidades
- Reinicio seguro del gateway con health checks previos y posteriores
- Rollback automático si la recuperación falla
- Monitoreo de estado durante el proceso de reinicio
- Logs de auditoría de operaciones de reinicio

## Uso
- Reinicio del gateway: `openclaw gateway restart` (ver skill `gateway-restart-helper` del sistema)



## Requisitos
- Gateway en estado estable (no en mantenimiento)
- Acceso a la API del gateway
- Docker (para la interfaz de control)
