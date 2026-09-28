# Kanam OS: Automatizaciones y pipelines entre agentes

**Hook**
> "¿Te imaginas que tus agentes trabajen como una línea de montaje sin que levantes la mano?"

## ¿Qué son las automatizaciones?
- Jobs programados con la herramienta **automations**.
- Pueden dispararse por **cron**, **at**, **every** o **stream**.
- Cada job lleva un **payload** que típicamente es un `agentTurn` dirigido a un agente específico.

## Pipeline típico (ADR-074)
1. **Core** agenda una automatización semanal (`cron` los lunes) que envía un mensaje a **Dev** para generar el artículo de la semana (`sessions_send`).
2. **Dev** genera el borrador y lo guarda en `docs/linkedin/…`.
3. **Ops** es notificado (`sessions_send`) y publica el post en LinkedIn vía API externa (requiere `secrets`).
4. **Core** registra la publicación en la **memory vault** y actualiza el **daily log**.

## Configuración de un job
```json
{
  "schedule": {"kind":"cron","expr":"0 10 * * MON","tz":"America/Buenos_Aires"},
  "payload": {
    "kind":"agentTurn",
    "message":"Generar artículo semanal Kanam OS",
    "model":"deepseek-v4-flash:cloud",
    "thinking":"high"
  },
  "enabled": true,
  "name": "Kanam-OS-Weekly-Post"
}
```
- **Entrega**: `mode":"announce"` para que el agente anuncie al canal cuando termine.
- **Alertas**: `failureAlert` activado (2 fallos → alerta).

## Triggers y watch
- Un **trigger script** puede inspeccionar la salida de un pipeline y decidir si lanzar un job de seguimiento (p. ej. si los tests fallan, crear una tarea de corrección).
- Uso de `next_check` dentro del job para ajustar la frecuencia dinámica.

---
**CTA**: Próximamente veremos los roles especializados de los cinco agentes de Kanam OS.
