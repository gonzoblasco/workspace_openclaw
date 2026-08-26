---
name: "health-check-dashboard"
description: "Real-time health monitoring dashboard for the OpenClaw Gateway."
---

# OpenClaw Health Check Dashboard

A dashboard que monitorea el estado del OpenClaw Gateway en tiempo real, mostrando métricas clave como uso de memoria, CPU, conexiones activas y latencia.

## Funcionalidades
- Paneles de control en tiempo real
- Alertas por umbrales de salud
- Historial de métricas
- Integración con notificaciones (Slack, email)

## Uso
```bash
# Acceder al dashboard
# http://localhost:8080/health

# Monitorizar desde terminal
./scripts/health-check-dashboard.sh
```

## Scripts auxiliares
- `./scripts/health-check-dashboard.sh` - Dashboard principal
- `./scripts/health-check-dashboard.sh` - Versión con argumentos
- `./scripts/health-check-dashboard.sh` - Script principal

## Requisitos
- Gateway corriendo
- Acceso a métricas del sistema (PM2, systemctl, etc.)
- Opcional: integraciones de notificación

## Beneficios
- Prevención de SIGKILLs mediante detección temprana de problemas
- Visibilidad centralizada de la salud del sistema
- Reducción de tiempo de resolución de incidentes
