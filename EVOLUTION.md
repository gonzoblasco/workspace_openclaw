# EVOLUTION.md - Blueprint de Madurez de Kanam OS

Este documento define el camino de evolución técnica y organizativa del ecosistema Kanam. No es una lista de tareas, sino un **mapa de dependencias**: cada etapa debe estar validada antes de desbloquear la siguiente.

La meta final es la transición de una asistente única a **Kanam's Crew**, un equipo de roles especializados coordinados bajo un sistema de estándares críticos.

---

## 🗺️ El Camino de Madurez

### Etapa 1: El Suelo (Sistemas de Referencia) ✅ COMPLETADA
*Objetivo: Crear la "verdad" contra la cual se mide todo. Sin estándares, el equipo es solo una suma de opiniones.*
- **Design System (Paso 0):** Tokens semánticos y manifiesto Anti-Slop implementados.
- **Diccionario de Entidades:** Implementación de la capa de entidades (`.knowledge/entities/`).
- **Rúbrica de Gusto (SHARP):** Estándar de medición de calidad establecido.

### Etapa 2: El Ritmo (Ciclos de Vida y Gates) ✅ COMPLETADA
*Objetivo: Industrializar la calidad. Pasar de "escribir" a "gestionar la evolución" mediante el patrón `aeon`.*
- **Security-Scan:** Gate de seguridad contra inyecciones y exfiltración.
- **Skill Evals:** Sistema de assertions para estabilidad funcional.
- **Lifecycle Tracker:** Gestión de degradación y obsolescencia de skills.
- **Regression Control:** Freno de mano SHARP para evitar la caída de calidad.
- **Session Hooks:** Planificación persistente mediante `.session_plan.json`.

### Etapa 3: El Equipo (Kanam's Crew) ✅ COMPLETADA
*Objetivo: Desplegar roles especializados que operen sobre los estándares de las etapas 1 y 2.*
- **The Critic:** Guardián de la sustancia y el gusto (Sustancia).
- **The UI/UX Auditor:** Guardián de la coherencia y accesibilidad (Superficie).
- **The Crew Planner:** Orquestador de flujos y persistencia (Gobierno).
- **Validación Final:** Implementación exitosa de la 'Guía de Inicio Rápido' mediante orquestación completa.

### Etapa 4: Expansión y Refinamiento (En curso)
*Objetivo: Pasar de la base operativa a la especialización avanzada.*

| Componente | Descripción | Prioridad |
| :--- | :--- | :--- |
| **Módulo de Especialistas** | Implementar roles de dominio (Anthropologist, Geographer, etc.) basados en el Academic Multi-Agent System. | Media |
| **Validación A11y Técnica** | Integrar `axe-core` OSS para pasar de auditoría visual a medición técnica de accesibilidad. | Media |
| **Tablero de Control** | Implementar superficie visual para el backlog de tareas a largo plazo (Resolución de §2.5). | Alta |

---

## 🛠️ Metodología de Evolución

1. **No saltar etapas:** No se puede spawnear un `Critic` si no hay una rúbrica SHARP. Un agente sin estándar es ruido.
2. **Documentación como Código:** Cada paso de evolución se registra en un ADR y se implementa como una skill o script en el workspace.
3. **Validación Real:** Una etapa se considera "completada" solo cuando el Core puede verificar el cumplimiento del estándar de forma automatizada o semi-automatizada.

---

*Actualizado el 2026-10-01. Este documento es el norte de Kanam OS.*
