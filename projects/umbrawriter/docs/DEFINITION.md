# DEFINITION: UmbraWriter MVP v0.1

**Estado:** Definido — Listo para implementación  
**Fecha:** 2026-07-17  
**Equipo:** Kanam AI (Product Owner)

---

## 🎯 **PROPOSTA DE VALOR DEL MVP**

UmbraWriter MVP transforma la escritura narrativa de un proceso lineal ("escribir → editar") a uno dialógico e iterativo. El sistema no solo genera texto, sino que **gestiona capas narrativas activas** y **proponente ramificaciones creativas** en tiempo real al usuario.

---

## 🏗️ **ARQUITECTURA DEL MOTOR DIALÓGICO**

### Componentes Core

```
┌─────────────────────────────────────┐
│   Input Layer (Beats Parser)        │
│   - Markdown reader                  │
│   - Relative path resolution         │
│   - Character reference              │
└──────────┬──────────────────────────┘
           │
┌─────────────────────────────────────┐
│   Context Engine                     │
│   - State tracking                  │
│   - Plot point identification       │
│   - Tone analysis                   │
└──────────┬──────────────────────────┘
           │
┌─────────────────────────────────────┐
│   Generator Layer (Dialógica)        │
│   - Critic Creative model           │
│   - Ramification generator          │
│   - Divergence visualization        │
└─────────────────────────────────────┘
```

### Stack Técnico Definido

| Capa | Tecnología | Motivación |
|------|-----------|------------|
| Frontend | React 19 + TanStack Start | Control UI reactivo con router e hydrated state |
| Editor | Monaco Editor (Markdown) | Experiencia de edición profesional integrada |
| Build | Vite | Modularización rápida y bundle optimization |
| Styling | Tailwind v4 | Atomic design, responsive by default |
| Backend | Supabase + Edge Functions | Auth, realtime, escalabilidad sin serverless overhead |
| Export | PDFKit + libreoffice-wasm | Formatos estándar para distribución |

---

## 📋 **REQUISITOS FUNCIONALES (MVP)**

### R01 — Lectura de Beats Files
**Prioridad:** CRÍTICA  
**Desc.** El sistema debe leer archivos `.md` con soporte a:
- Rutas relativas (`beats/capitulo-03.md`)
- Referencias cruzadas entre capítulos
- Bloques de diálogo y descripción alternas
- Notas del autor (ocultas por defecto)

### R02 — Generación Dialógica
**Prioridad:** CRÍTICA  
**Desc.** Al recibir instrucción de alteración narrativa:
- Análisis del tono actual (sublime, cómic, trágico, etc.)
- Propuesta de 2-3 caminos con carga dramática distinta
- Indicación visual de divergencia (branch depth)

### R03 — UI Contextual
**Prioridad:** ALTA  
**Desc.** Componente que muestra:
- Estado actual del capítulo (scene number, current plot point)
- Ramificaciones disponibles con iconografía por tipo
- Historial de decisiones previas (timeline view)

---

## 🎭 **PERSONAJES DE LA HISTORIA**

| Arquetipo | Función | Comportamiento Esperado |
|-----------|---------|--------------------------|
| Crítico Creativo IA | Analiza intención del usuario y sugiere alternativas | Actúa como editor coleccionista, no como corrector de faltas ortográficas |
| Narrador Pasivo | Documenta cambios canon (con o sin atribución) | Silencioso: registra divergencias pero no las defiende |
| Director Creativo IA | Balance entre fiel al original y creativo | Sugiere alternativas "valiosas" con nota de riesgo emocional |

---

## 📊 **MÉTRICAS DE ÉXITO (KPIs)**

### KPI1: Frecuencia Dialógica
- Objetivo: Usuario interactúe en ≥30% de turnos de escritura
- Métrica: Número de ramas generadas / total de prompts narrativos

### KPI2: Retención Post-Sesión
- Objetivo: Usuario retorne al próximo día con 60%+ tasa de conversión
- Métrica: Devolución a sistema en 48h posteriores a último uso

### KPI3: Calidad Perceptiva
- Objetivo: 7/10 usuarios reporten "sentirse entendido" por el sistema
- Métrica: Feedback cualitativo post-señal de "¿Siente esto como co-creación?"

---

## 🚧 **DEPENDENCIAS CRÍTICAS**

| Dep. | Estado | Impacto en MVP |
|------|--------|----------------|
| Supabase Auth | 🔴 Pendiente (Lovable Cloud) | Sin auth, multi-tenant no escalable → freeze hasta operational |
| Edge Functions | 🔴 Pending deployment | Webhook Meli, cron jobs, billing requieren backend real |
| DEEPSEEK_API_KEY | 🔴 Configurar | Motor dialógico sin API key = PoC estático |
| MELI credentials | 🔴 Pendientes | Auto-learn no funcional → feature "MeLi Integration" sin value |

---

## 📝 **PLAN DE IMPLEMENTACIÓN (Fase 2)**

**Semana 1:** Arquitectura del prompt engine crítico  
**Semana 2:** Parser de beats + UI básico  
**Semana 3:** Generador dialógico + evals con Gonzo como beta user  
**Semana 4:** Hardening de seguridad + despliegue Supabase  

---
*Documento versionado. Última edición: 2026-07-17, Kanam AI.*