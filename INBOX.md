# 📥 Inbox

Ideas sueltas, recordatorios, cosas que se me ocurren mientras trabajo en otra cosa.

**Regla:** esto es captura, no organización. Después se triage a donde corresponda.

---

- Tenemos n8n corriendo en un VPS de Hostinger, casi nunca lo usamos. Evaluar si integrarlo al sistema de automatización a futuro.
- Skills de n8n revisadas: kowl64/n8n-workflow-automation (diseño de workflows) y thomasansems/n8n (API client + tester + optimizer). Si algún día integramos n8n, revisar ambas.
- **Tailscale Serve para el dashboard de OpenClaw:** pendiente de sesiones anteriores. El Control UI (webchat desde iPhone) requiere secure context (HTTPS o localhost). Solución: configurar Tailscale Serve en la MacBook Air para acceder por HTTPS desde cualquier dispositivo. Ver `memory/archive/2026-08-03-1157.md` y `2026-08-02-1627.md`.
- **Sistema de orquestación de agentes CLI desde OpenClaw (2026-08-13):** idea de Gonzo — conseguir versiones CLI de agentes de código (Qwen Code, Claude Code, OpenCode, Antigravity CLI) y que Kanam los maneje desde OpenClaw. Crear un sistema que orqueste todo el conjunto de agentes CLI para escribir código: Kanam planifica/documenta, lanza los agentes CLI, y coordina el pipeline de revisión cruzada (como el de la Fase 3 de kanam-story, pero generalizado). Investigar viabilidad: cómo invocar cada CLI headless, cómo capturar su output, cómo pasarles contexto. Ver `projects/kanam-story/.knowledge/PLAN-FASE-3.md` como referencia del patrón de revisión cruzada A/B.

