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
```bash
# Reiniciar el gateway de forma segura
./scripts/gateway-restart-helper --force

# Verificar estado antes de reiniciar
./scripts/gateway-restart-helper --status
```

## Scripts auxiliares
- `./scripts/gateway-restart-helper.sh` - Lógica principal de reinicio
- `./scripts/gateway-restart-helper.sh` - Versión con argumentos
- `./scripts/gateway-restart-helper.sh` - Script principal

## Requisitos
- Gateway en estado estable (no en mantenimiento)
- Acceso a la API del gateway
- Docker (para la interfaz de control)
