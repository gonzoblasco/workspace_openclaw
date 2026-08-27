---
name: "model-router-pro"
description: "Inteligent routing of models with fallback and load balancing between local and cloud instances."
---

# OpenClaw Model Router Pro

## Descripción
Esta skill automaically selecciona entre modelos locales (Ollama) y cloud (APIs) basados en disponibilidad, costo, latencia y calidad de respuesta. Proporciona fallback seguro y balanceo de carga inteligente.

## ¡Funcionalidades Intelijentes
- Detección en tiempo real de disponibilidad de modelos
- Balanceo de carga distribuido por carga (ej: modelos paralelo)
- Fallback automático cuando un modelo falla
- Priorización de modelos locales cuando sea económico o necesario
- Historial de selección de modelos para auditoría

## Uso Básico
```bash
# Iniciar el router
./scripts/model-router-pro start

# Forzar modelo local
./scripts/model-router-pro --local

# Forzar modelo cloud
./scripts/model-router-pro --cloud --model <clave-cloud>
```

## Requisitos
- Ollama local instalado (con modelos configurados)
- Acceso a APIs cloud con claves autenticadas
- Puerto 8000 estar libre para servidor

## Beneficios
- Optimización automática de recursos computacionales
- Redución de costos al preferir modelos locales
- Mayor resiliencia con detección de fallos
- Ajuste dinámico al tipo de tarea (ej: costo vs calidad)
