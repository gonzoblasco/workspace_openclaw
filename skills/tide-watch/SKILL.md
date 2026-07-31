---
name: "tide-watch"
description: "Monitoreo proactivo de capacidad de sesión con alertas configurables"
---

# tide-watch

## Descripción
Monitorea los context windows de sesiones de OpenClaw y alerta antes de que se llenen. Thresholds configurables (75%, 85%, 90%, 95%) disparan alertas y backups automáticos de sesión. Dos modos: directive-only (sin instalación de código) o con CLI tools opcionales para gestión manual y archivado.

## Cuándo usarlo
- Para recibir advertencia antes de que una sesión larga llegue al límite de contexto
- Para backup automático de sesión al 90% de capacidad antes de que se lockee
- Para reanudar una conversación después de un context reset usando un prompt guardado
- Para configurar diferentes thresholds por canal (webchat vs DM)
- Para archivar sesiones viejas y mantener el directorio de sesiones limpio

## Workflow
1. Configurar thresholds deseados (default: 75%, 85%, 90%, 95%)
2. tide-watch corre en background monitoreando la capacidad
3. Cuando se alcanza un threshold, alerta y opcionalmente hace backup
4. Si la sesión se llena, usar el backup para reanudar

## Notas
- Sin dependencias externas
- Thresholds configurables por canal
- Backups automáticos opcionales
