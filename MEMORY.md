# MEMORY.md - Long-Term Memory

> Memoria curada de largo plazo. Detalle técnico en `docs/LEARNINGS.md`, OSS en `docs/OSS-TRACKER.md`, dailies en `memory/` y proyectos en `projects/<slug>/.knowledge/`.

## Sobre Gonzo

- Gonzalo, Argentina (GMT-3). Fullstack (React/TS, Supabase/Edge Functions, DB, billing, tooling).
- Búsqueda laboral: perfil AI-Native / a11y. Entrevista con OpenSistemas (25/08).
- Perfil: fotógrafo, comunicación social, escritor de novelas.
- Preferencias: honestidad absoluta, autonomía total, registro escrito crítico.
- Setup: Mac Mini + MacBook Air (workspace sincronizado por git).
- **PRs en sesiones (2026-08-25):** No se revisan automáticamente al inicio. Solo cuando Gonzo los comparte.
- **Branding LinkedIn (2026-08-25):** 3 nichos: (1) **a11y** (diferenciador), (2) **Agentic/AI-Native** (laboral), (3) **Fullstack** (base). Patrón: Solo PRs MERGEADOS, postura didáctica/pedagógica (el qué+proceso+por qué), sin tutoriales secuenciales. Archivo cada post en `docs/linkedin/`.
- **Ley de vida (2026-08-12):** Silencio = respeto. Hablar solo si hay algo que aportar. Un "ok" es ruido.
- **Principio Boy Scout (2026-08-17):** Dejar el lugar mejor de como estaba al guardar sesión. Documentación constante y tests sobre lo nuevo.
- **Regla de merge:** Siempre merge, nunca reset (evita perder commits de la otra máquina).
- **Regla de escritura:** Guion común (-) siempre. NUNCA guion largo (em/en dash). Validar con `scripts/check_em_dash.py`.
- **Docs por categoría (2026-08-27):** Carpetas en `docs/` para `linkedin/`, `feedback/`, `prs/`, `pipeline/`, `entrevistas/`. Raíz solo para generales.
- **Idioma GitHub (2026-08-12):** TODO en inglés (README, docs, ADRs, commits, PRs). Strings de UI en español.
- **Regla de alcance (2026-08-11):** Solo trabajar dentro de `.openclaw/`.
- **Terminología:** "Guardar sesión" (save point), no "cerrar sesión".
- **"adelante" (2026-08-12):** "Ejecutá tu recomendación según el contexto".
- **Proactividad:** Sugerir revisar el backlog si no hay tarea clara.
- **Skills (2026-08-21):** Cambios solo vía `skill_workshop` (propuesta), no edición directa.
- **Colaboración OSS (2026-08-24):** El valor suele estar en comentar/revisar, no en abrir PRs. No pisar el trabajo ajeno.
- **Interacción Maintainers (2026-08-24):** Si la dirección ya fue validada, ir directo a la acción (hacer el PR), no ofrecer "estoy feliz de iterar".
- **Bots de review (2026-08-24):** No agradecer a bots. Responder directo a la sustancia con evidencia.
- **Referencia ≠ proyecto (2026-08-24):** "Quitar referencia" = quitar puntero git, NUNCA borrar carpeta con datos locales (`.env`, `*.db`). Respaldar SIEMPRE antes de limpiar.
- **Diferenciador:** IA como infraestructura de trabajo (no chat), stack opinado, docs de decisiones.

## Metodología

- Stack opinado: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG.
- Sesión de OpenClaw por proyecto.
- Registro: MEMORY.md, dailies, HANDOFF, CHANGELOG.
- **Iconos (ADR-037):** Lucide (`lucide-react`) base. No emojis en UI.

## Pipeline de Programación (ESTÁNDAR)

Pipeline A/B con **Qwen Code vía Ollama** (motor: `glm-5.3-flash:cloud`, desde 2026-08-29; antes `deepseek-v4-flash:cloud`). Flujo: A escribe $\rightarrow$ Kanam pasa a B $\rightarrow$ B revisa $\rightarrow$ Verificar $\rightarrow$ Iterar.
- **Claude Code (Alternativa):** Para SIGKILL o tareas largas.
- **Lecciones:**
    - **SIGKILL:** Prompts cortos para revisiones; relanzar si muere.
    - **Cross-review:** Agente B puede introducir bugs. Verificar siempre contra la fuente real (API/Docs).
    - **Terminal Harnesses (2026-08-23):** Los CLIs TUI (como ForgeCode) no son orquestables sin TTY real. Usar solo herramientas que corran headless.

## Arquitectura de Agentes - Goal-Oriented

Objetivos claros + restricciones explícitas, feedback loops rápidos, logging completo y human-in-the-loop para acciones destructivas. (Ref: ADR-007).

## Reglas de Ingeniería

- **Pre-commit hooks:** Obligatorios en todo proyecto (Biome $\rightarrow$ Vitest $\rightarrow$ Build). Prioridad sobre features.
- **Validación UI (2026-08-27):** Fixes visuales se validan SOLO con browser real (Desktop). jsdom/headless no detectan problemas de layout/chrome nativo.

## Modelo de Agentes OpenClaw OS

- Unidad de aislamiento = AGENTE (workspace completo).
- Sesiones comparten todo. Mantener 1 agente `main`. `/new` para conversaciones limpias.

## Config de Tools

- **Modelos (2026-08-29):** Default de OpenClaw: `glm-5.3-flash:cloud`. Kanam en **thinking max**; agentes A/B en **high** (`glm-5.3-flash:cloud`). Default: pipeline A/B en HIGH.
- **Cambio de motor (2026-08-29):** DeepSeek V4 Flash → GLM 5.3 Flash, tras comparativa de 5 modelos con un mismo prompt pesado de arquitectura de agentes (DeepSeek V4 Flash xhigh, GLM 5.3 Flash, GLM 5.3, Kimi K2.7 Code xhigh, Kimi K3 xhigh). DeepSeek fue el más estructurado pero el menos agudo; GLM 5.3 Flash ganó en insights operativos y es multimodal nativo (imagen/video/PDF, 1M de contexto). Kimi K2.7 Code (xhigh) fue el mejor pensador: pendiente probarlo en high cuando haya GPU.
- **Niveles de razonamiento (2026-08-29):** el max NO es driver de calidad (DeepSeek en max filosofa, ADR-040; Kimi K3 en xhigh inventó números). Los mejores outputs vinieron sin razonamiento visible. Agentes de código siempre en high; max solo para diseño difícil puntual. Para GLM: CERO parámetros, default del servidor (ADR-041).
- **Regla de costo (2026-08-29):** 1 request de Kimi K3 = 41 requests de GLM 5.3 Flash en consumo real (medición Ollama). K3 = cirujano, nunca default. Precios verificados: GLM Flash $0.075/$0.25 - K3 $3.00/$15.00 por 1M.
- **DeepSeek V4 Flash fuera del ecosistema (2026-08-29):** sacado de la config de OpenClaw (default + lista estática de modelos). También fuera: `kimi-k3:cloud` y `deepseek-v4-pro:cloud` (los dos más caros - K3 razona always-on y cuesta 41x en consumo real). Volver solo en emergencia: backup `~/.openclaw/openclaw.json.bak-20260829` o re-agregar la entry (dinámico de Ollama también puede mostrarlo).
- **Search:** `DuckDuckGo Search (experimental)` (key-free).

## Proyectos (Detalle en `.knowledge/` de cada uno)

- **Regla (2026-08-28):** NO proponer SoporteML en estrategia de proyectos. Gonzo lo pidió explícitamente.

- **Kanam Story:** Co-writer de ficción. PWA, roles especializados. Local-first $\rightarrow$ Nube (en plan).
- **Kanam Mind:** Segundo cerebro local-first. Timeline, CRUD accesible, resumen IA. Local-first puro (IndexedDB).
- **SoporteML:** CRM MeLi. v4 es el reinicio actual (frontend avanzado, backend v3 sólido).
- **kanam-skills:** Repo público de skills. Sanitización obligatoria (Gonzo $\rightarrow$ usuario).
- **a11y-fixer:** Engine de fixes de accesibilidad. v0.6.0 reescrito.
- **kanam-forge:** Lovable self-hosted. Fusionado con `create-with-ai`. Fase 1 completa.
- **create-with-ai:** ARCHIVADO. Fusionado a kanam-forge. Deprecar en npm (requiere npm login).
- **daily-ink:** PWA prompts de escritura.
- **create-stack-next:** Scaffolder opinado Next.js (`@gonzoblasco/create-stack`). Vivo.
- **ai-engineering-bootcamp:** Curso completado 10/10. Archivados.

## Repos Propios (No forks)

### Activos
- workspace_openclaw (Privado)
- kanam-skills, kanam-story, kanam-mind, kanam-solitaires, soporteml, soporteml-v4 (Privado), a11y-fixer, ai-developer-stack, create-stack, accessible-ui (Privado), quedamos (Privado), kanam-forge.

### Archivados
- soporteml-v3 (Privado), ai-engineering-bootcamp, hyatt-copilot-agent (Privado), ensulugar, cabala, health-tracker, umbrawriter (Privado).
