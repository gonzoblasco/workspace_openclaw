# 🌿 Kanam's Crew: Ecosystem Resources

> **📌 Este es el DETALLE.** Para decisiones y estado consolidado, ver **`DECISIONS.md`** en esta misma carpeta. Acá vive la ficha completa de cada repo analizado.

> **⚠️ CRITERIO DE FILTRADO (Gonzo, 2026-10-01):**
> - **Diseño / UI / estética = PRIORITARIO:** todo recurso de diseño se saca primero y en detalle. **Pero NO es el único foco:** también importan el sistema, el desarrollo general, la arquitectura, la infraestructura y las demás áreas. El filtro es amplio; diseño es solo el primer orden de prioridad. Objetivo: mejorar la UI y la estética de nuestros proyectos, sin descuidar el resto.
> - **🚫 CRIPTO = FUERA.** No hacemos cripto/Web3/blockchain (tokens, wallets, DeFi, NFT, chains, predicción on-chain). Se descarta de plano, sin analizar. Aplica a toda fuente, presente y futura.
> - **🔑 CADA REPO SE LEE EN DOS CAPAS (Gonzo, 2026-10-01):** un repo se descarta como **implementación** solo si no aplica, pero **el diseño se extrae igual**. La pregunta nunca es solo "¿lo usamos?", sino **"¿qué aprendemos de cómo lo resuelve?"**. Un patrón, un modelo de datos, una separación de responsabilidades o una decisión de arquitectura valen aunque el código no se instale. **Descartar el repo ≠ descartar la lección.**

Este documento sirve como catálogo de recursos externos para expandir las capacidades de Kanam y su equipo de subagentes. En lugar de reinventar prompts o flujos, consultamos estos repositorios para adoptar patrones, roles y herramientas validadas.

## 📚 Repositorios de Referencia

### 1. [awesome-openclaw-usecases](https://github.com/hesamsheikh/awesome-openclaw-usecases)
**Tipo:** Catálogo de Inspiración y Patrones.
**Utilidad:** Identificar *cómo* resolver problemas mediante la orquestación de agentes.
- **Highlight:** El patrón de **Content Factory** (encadenamiento de agentes: Research $\rightarrow$ Writing $\rightarrow$ Design).
- **Aplicación:** Implementar "Investigation Factories" donde el trabajo se divide en *Explorador*, *Analista* y *Sintetizador*.

### 2. [awesome-openclaw](https://github.com/vincentkoc/awesome-openclaw)
**Tipo:** Índice Técnico de Infraestructura.
**Utilidad:** Fuente de consulta para componentes técnicos.
- **Utilidad:** Buscar servidores MCP (Model Context Protocol), plugins de integración y sistemas de memoria avanzados.
- **Uso:** Primera parada antes de desarrollar una herramienta desde cero.

### 3. [awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents)
**Tipo:** Librería de Plantillas de Identidad (`SOUL.md`).
**Utilidad:** Implementación rápida de roles especializados.
- **Highlight:** Más de 200 plantillas de `SOUL.md` listas para copiar y pegar.
- **Roles Clave para el Crew:**
    - **Técnicos:** `Trace` (Bug Hunter), `Forge` (Build Resolver), `Sentinel` (TS Reviewer).
    - **Investigación:** `Scout` (Competitor Watch).
    - **Soporte:** `Scribe` (Docs Writer), `Minutes` (Meeting Notes).

### 4. [awesome-openclaw-personas](https://github.com/TravisLeeeeee/awesome-openclaw-personas)
**Tipo:** Paquetes de Personas Completas (SOPs + Identidad).
**Utilidad:** Desplegar agentes con metodologías profesionales reales.
- **Highlight:** No son prompts, son directorios con `AGENTS.md` (SOPs) y `SKILL.md` (Frameworks).
- **Uso:** Ideal para roles que requieren procesos estrictos, auditorías o modelos de puntuación (ej. `E-Commerce Product Scout` con scoring de 6 dimensiones).

---

## 🎭 Plantillas de Rol (Crew Roster)

Filtrado de [mergisi/awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents) (199 agentes, 24 categorías).

**Criterio de filtrado:** solo lo que calza con nuestro stack (TS/Next.js, Drizzle/Prisma, gateway en Mac Mini) o con un rol real del crew. Todo lo de ecommerce, finance, education, freelance, personal y moltbook queda afuera.

**Cómo se usa:** copiar el `SOUL.md` del agente, adaptarlo (voz, contexto, reglas de Gonzo) y registrarlo. *No instalar la plantilla cruda* - viene con nombres genéricos.

### DEV - Revisión y Calidad (los más valiosos)

| Plantilla | Necesidad que cubre | Por qué aplica |
|-----------|---------------------|----------------|
| **[Sentinel](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/typescript-reviewer/SOUL.md)** (typescript-reviewer) | Fugas de tipo, frontera server/client, bug JSX de Turbopack, N+1 de ORM | Stack TS/Next.js de los proyectos |
| **[Keeper](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/database-reviewer/SOUL.md)** (database-reviewer) | Seguridad de migraciones, N+1, idempotencia de webhooks | Migraciones Drizzle/Prisma |
| **[Whisper](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/silent-failure-hunter/SOUL.md)** (silent-failure-hunter) | Errores tragados, eventos de analytics faltantes | El check de "no da falso verde" |
| **[Verdict](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/pr-test-analyzer/SOUL.md)** (pr-test-analyzer) | Merge-readiness: body vs diff, gaps de cobertura | Refuerza Verify-Before-Push |
| **[Forge](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/build-error-resolver/SOUL.md)** (build-error-resolver) | Diagnóstico de build rojo (Next/Vercel/Turbopack) | Cuando el pre-commit falla sin mensaje claro |
| **[Lens](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/code-reviewer/SOUL.md)** (code-reviewer) | Review general + security scanning | Cubre el rol de revisor B del pipeline |
| **[Beacon](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/seo-specialist/SOUL.md)** (seo-specialist) | Checklist de deploy de blog, SEO on-page | Si un proyecto publica contenido |

### DEV - Producción y Mantenimiento

| Plantilla | Necesidad que cubre |
|-----------|---------------------|
| **[Scribe](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/docs-writer/SOUL.md)** (docs-writer) | README, docs de API - el rol MIND/STUDIO |
| **[Test Writer](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/test-writer/SOUL.md)** | Generación de tests, cobertura |
| **[Migration Helper](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/migration-helper/SOUL.md)** | Migraciones de DB con rollback y safety nets |
| **[Changelog](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/changelog/SOUL.md)** | Release notes desde git |
| **[Dependency Scanner](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/development/dependency-scanner/SOUL.md)** | CVEs, licencias, supply chain |

### OPS

| Plantilla | Necesidad que cubre |
|-----------|---------------------|
| **[Incident Responder](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/incident-responder/SOUL.md)** | Respuesta a incidentes |
| **[Log Analyzer](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/log-analyzer/SOUL.md)** | Análisis de logs |
| **[Infra Monitor](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/infra-monitor/SOUL.md)** | Monitoreo de infra |
| **[Deploy Guardian](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/deploy-guardian/SOUL.md)** | Guardia de deploys |
| **[Cost Optimizer](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/cost-optimizer/SOUL.md)** | Optimización de costos - alineado a ADR-090 |

### MIND / Datos

| Plantilla | Necesidad que cubre |
|-----------|---------------------|
| **[SQL Assistant](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/data/sql-assistant/SOUL.md)** | Constructor/optimizador de queries - útil con `memory.db` |
| **[Report Generator](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/data/report-generator/SOUL.md)** | Reportes automatizados |
| **[Research Assistant](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/education/research-assistant/SOUL.md)** | Asistente de investigación |
| **[Radar](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/business/radar/SOUL.md)** | Monitoreo/radar de novedades |

### ⚠️ Advertencia

- Las plantillas vienen con **nombres genéricos** ("Your Business Name", "backend", "pihole") y algunos `SOUL.md` están vacíos o son de la comunidad sin auditar. **Revisar antes de adoptar.**
- Los "Deploy" links apuntan a **CrewClaw** (servicio pago de terceros). Ignorarlos: nosotros registramos local con `openclaw agents add`.
- El repo afirma 205 y luego 199 agentes. Contar antes de confiar en el número.

---

## 🎭 Personas Completas (Paquetes con SOP)

Filtrado de [TravisLeeeeee/awesome-openclaw-personas](https://github.com/TravisLeeeeee/awesome-openclaw-personas) (214 personas, 34 categorías).

**Qué lo hace distinto:** no es un `SOUL.md` suelto. Cada persona es un **directorio con `AGENTS.md` (SOPs, matrices de decisión) + `SKILL.md` (frameworks, templates de output)**. Es metodología empaquetada, no tono. **Cómo se usa:** copiar el directorio, auditar los `AGENTS.md`/`SKILL.md`, adaptar y registrar.

**Criterio:** solo lo que calza con nuestro stack, nuestras reglas duras o un rol real del crew. Todo lo de ecommerce/China/paid media/sales queda afuera.

### 🏆 Los tres que atacan un hueco real nuestro

| Persona | Necesidad que cubre | Por qué aplica |
|---------|---------------------|----------------|
| **[Reality Checker](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/reality-checker)** | Detiene aprobaciones fantasiosas; exige evidencia abrumadora antes de certificar a producción. Default: "NEEDS WORK". | Es exactamente nuestra regla de **no dar falso verde** (verification-gates). |
| **[Evidence Collector](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/evidence-collector)** | Exige prueba visual para cada afirmación; encuentra 3-5 issues en cualquier primer implementation. | El enforcement de "un auto-reporte de subagente no es un hecho". |
| **[Accessibility Auditor](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/accessibility-auditor)** | Auditoría WCAG 2.2 con tecnologías asistivas reales (VoiceOver, NVDA). | Directo a nuestras skills `a11y-*`. |

### 🔬 El Academic Multi-Agent System (el patrón Factory, ya construido)

El repo trae un **sistema multi-agente completo para investigación** - es la implementación en vivo del patrón "Factory" que venimos discutiendo. Vale estudiarlo entero como referencia arquitectónica:

| Rol | Función |
|-----|---------|
| **Planner** | Orquestador central (PM + advisor + ops). |
| **Ideator** | Genera ideas de investigación de nivel conferencia. |
| **Literature Scout** | Monitorea arXiv, Semantic Scholar, proceedings. |
| **Surveyor** | Revisiones sistemáticas de literatura + gap analysis. |
| **Critic** | Árbitro de gusto: "aceptable" vs "no listo". |
| **Reviewer** | Simula peer-review de ACL/NeurIPS/ICML. |
| **Writer** | Redacta papers publication-ready. |
| **Coder** | Convierte ideas en código de experimentos. |

> **Por qué importa:** nuestro catálogo de soluciones tenía "Factory de Investigación (Explorador → Analista → Sintetizador)" como idea. Acá está el diseño de 8 roles con SOPs reales. Cuando montemos la nuestra, empezamos desde acá y no desde cero.

### 🧪 Testing & QA

- **[Test Results Analyzer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/test-results-analyzer)** - convierte datos crudos de tests en insights de calidad con métodos estadísticos.
- **[Tool Evaluator](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/tool-evaluator)** - evalúa herramientas con scoring ponderado. Útil con la regla "Existing Solutions Preflight".
- **[Workflow Optimizer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/workflow-optimizer)** - optimiza procesos con Lean/Six Sigma.
- **[Performance Benchmarker](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/testing/performance-benchmarker)** - load testing y optimización.

### 🛠️ Engineering

- **[Nitpick](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/nitpick)** - "última línea de defensa": reviewer objetivo basado en evidencia que busca problemas, no aprobación.
- **[Github PR Reviewer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/github-pr-reviewer)** - review de PRs con comentarios inline y severidad. Candidato al rol revisor B.
- **[Debugger](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/debugger)** - encuentra bugs por evidencia, no intuición. Reproduce antes de tocar.
- **[Database Optimizer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/database-optimizer)** - piensa en query plans e índices. Útil con `memory.db`.
- **[Surgical Coder](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/surgical-coder)** - el mínimo código que resuelve, cero bloat.
- **[Script Builder](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/script-builder)** - CLI tools con dry-run incluido.
- **[Git Workflow Master](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/git-workflow-master)** - estrategia de branching e historial limpio.
- **[Software Architect](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/software-architect)** - diseña sistemas por bounded contexts.
- **[SRE](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/sre)** - SLOs y observabilidad con budget medible.
- **[Docs Writer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/docs-writer)** - docs testeada contra el código real.
- **[Github Issue Triager](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/engineering/github-issue-triager)** - labeling/routing de issues.

### 🏗️ DevOps & Infraestructura

- **[Deploy Guardian](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/deploy-guardian)** - vigila CI/CD, freeze windows, canary analysis, rollback. Complementa nuestra regla de esperar el CI.
- **[Self Healing Server](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/self-healing-server)** - detecta contenedores caídos/discos llenos y auto-remedia con backoff + log.
- **[Incident Responder](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/incident-responder)** - triage por severidad + post-mortems blameless.
- **[Log Analyzer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/log-analyzer)** - clustering de errores para cortar ruido.
- **[Cost Optimizer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/cost-optimizer)** - recursos idle + right-sizing (ADR-090).

### 🔒 Security

- **[Vuln Scanner](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/security/vuln-scanner)** - prioriza por explotabilidad/reachability, corta falsos positivos.
- **[Threat Monitor](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/security/threat-monitor)** - agrega feeds y CVEs, filtra por stack, mapea a MITRE ATT&CK.
- **[Access Auditor](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/security/access-auditor)** - permisos stale y caminos de escalación.

### 📊 Data / Research

- **[Research Analyst](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/data/research-analyst)** - "cero teatro de personalidad": lee todo antes de responder, presenta todas las caras, apunta a lo fuerte. Alineado a nuestra regla de leer el hilo completo.
- **[Ml Engineer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/data/ml-engineer)** - ML que funciona en producción, no notebooks de demo.

### 🎨 Design

- **[Inclusive Visuals Specialist](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/design/inclusive-visuals-specialist)** - combate sesgos sistémicos en imagen/video generados. Puente con nuestro `ui-contrast-audit` y a11y.
- **[Image Prompt Engineer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/design/image-prompt-engineer)** - prompts estructurados para generación de imagen.

### ⚙️ Automation

- **[Ghost Protocol (ZeroSignal)](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/automation/ghost-protocol)** - agente operativo para seguridad, DevOps y desarrollo. Calmo, directo, técnicamente preciso.

### ⚠️ Advertencia

- **Patrocinado por [DeskClaw](https://deskclaw.net)** (plataforma de gestión comercial). El repo promociona su servicio. El contenido es open-source, pero sesgado a "vender".
- Muchas descripciones del README están **cortadas a mitad de frase** (bug de renderizado del propio README). Hay que leer el directorio real de cada persona antes de adoptarla.
- **Auditar siempre** el `AGENTS.md` y `SKILL.md` antes de copiar: son SOPs ejecutables, no tono decorativo.

---

## 🎨 Diseño & UI - PRIORITARIO

Filtrado de [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) (5.300 skills de ClawHub, 30 categorías).

**Contexto:** es un **índice de descubrimiento**, no un repo de código. Las skills vienen de [ClawHub](https://clawhub.ai) (registro de la comunidad), **curadas, NO auditadas**. El propio repo excluyó 7.215 skills (spam, duplicados, cripto, 373 maliciosas identificadas). Tratar cada una como untrusted: revisar el código antes de instalar.

**Objetivo (Gonzo):** mejorar la UI y la estética de nuestros proyectos. Estas son las que apuntan a eso.

### 🥇 Dirección de diseño (el cluster más coherente)
Todas de un mismo autor (`kjaylee`), se refuerzan entre sí:
- **[anti-slop-design](https://clawskills.sh/skills/kjaylee-anti-slop-design)** - crea interfaces *distintivas* que evitan la estética genérica de IA. **La más valiosa para nuestro problema real.** Es el equivalente a nuestro `deslop` pero para UI.
- **[kj-ui-ux-pro-max](https://clawskills.sh/skills/kjaylee-kj-ui-ux-pro-max)** - inteligencia de UI/UX + guía de implementación para interfaces pulidas.
- **[kj-web-design-guidelines](https://clawskills.sh/skills/kjaylee-kj-web-design-guidelines)** - revisa el código de UI contra las Web Interface Guidelines.

### 🥈 Stack-específicas (Tailwind / shadcn / Motion)
- **[shadcn-theme-default](https://clawskills.sh/skills/guifav-shadcn-theme-default)** - fuerza el tema neutral de shadcn/ui con variables CSS OKLCH + integración Tailwind v4.
- **[lb-tailwindcss-skill](https://clawskills.sh/skills/leonaaardob-lb-tailwindcss-skill)** - documentación completa de Tailwind como skill.
- **[lb-motion-skill](https://clawskills.sh/skills/leonaaardob-lb-motion-skill)** - documentación de Motion.dev (ex Framer Motion) para animaciones.
- **[ant-design-skill](https://clawskills.sh/skills/felipeoff-ant-design-skill)** - patrones de componentes React con Ant Design.

### 🥉 Estética / dirección visual
- **[awwwards-design](https://clawskills.sh/skills/mkhaytman87-awwwards-design)** - sitios con animaciones avanzadas e interacciones creativas de nivel award.
- **[ui-ux-dev](https://clawskills.sh/skills/wing8169-ui-ux-dev)** - genera UI HTML/CSS/JS en vivo desde lenguaje natural (prototipado rápido).
- **[brand-guidelines](https://clawskills.sh/skills/seanphan-brand-guidelines)** - colores y tipografía de marca oficiales (modelo de referencia para definir la nuestra).
- **[canvas-design](https://clawskills.sh/skills/seanphan-canvas-design)** - arte visual en .png y .pdf.
- **[design-assets](https://clawskills.sh/skills/cmanfre7-design-assets)** - iconos, favicons, imágenes.

### ♿ Accesibilidad
- **[axe-devtools](https://clawskills.sh/skills/dylanb-axe-devtools)** - testing y remediación de accesibilidad con el MCP Server de axe.
- **[sovereign-accessibility-auditor](https://clawskills.sh/skills/ryudi84-sovereign-accessibility-auditor)** - audita HTML/CSS contra WCAG 2.1.
> Nota: ya tenemos skills propias de a11y (`a11y-at-validation`, `ui-contrast-audit`). Comparar antes de adoptar.

### 📌 Otras fuentes de diseño detectadas en el ecosistema
- **[Reality Checker / Evidence Collector](https://github.com/TravisLeeeeee/awesome-openclaw-personas)** (sección Personas) - para validar que la UI *realmente* quedó como se afirma, con screenshot.
- **[Inclusive Visuals Specialist](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/design/inclusive-visuals-specialist)** - combate sesgos en imagen generada.

### ⚠️ Veredicto honesto
El volumen (5.300) es engañoso: para diseño, el filtro da ~20 candidatas y **muchas son finas o solapan con lo que ya tenemos**. La jugada real no es instalar 10 skills, sino adoptar **2-3** (anti-slop-design + shadcn/tailwind + axe) y **definir un design system propio del workspace**. La estética de un proyecto no se resuelve con skills sueltas: se resuelve con tokens (color, tipo, espaciado) y un estándar.

---

## 🧩 Bankr Skills (filtrado: solo lo no-cripto)

Fuente: [BankrBot/skills](https://github.com/BankrBot/skills).
**Advertencia:** el repo es **~90% Web3/cripto**. Todo eso queda descartado por la regla anterior. Lo rescatado son las skills **stack-agnósticas** de investigación, meta-mantenimiento y confianza.

### 🔥 La suite `aeon` (24 skills) - lo más valioso del repo

**Meta-mantenimiento de skills (ataca nuestra deuda directa):**
- **[aeon-skill-security-scan](https://github.com/BankrBot/skills/tree/main/aeon-skill-security-scan)** - audita skills instaladas por shell injection, exfiltración de secretos, traversal y payloads de *prompt-override*. Directo a nuestra política de "contenido externo = sandbox".
- **[aeon-skill-evals](https://github.com/BankrBot/skills/tree/main/aeon-skill-evals)** - valida el output de una skill contra un manifiesto de assertions. Puente con `verification-gates`.
- **[aeon-skill-repair](https://github.com/BankrBot/skills/tree/main/aeon-skill-repair)** - auto-diagnostica y repara una skill degradada, con bloque de verificación.
- **[aeon-autoresearch](https://github.com/BankrBot/skills/tree/main/aeon-autoresearch)** - **evoluciona una skill instalada**: genera 4 variaciones con tesis distintas, las puntúa con rúbrica ponderada y aplica la ganadora.
- **[aeon-vuln-scanner](https://github.com/BankrBot/skills/tree/main/aeon-vuln-scanner)** - audita repos con Semgrep + TruffleHog + osv-scanner. Para el *preflight* de código de terceros.

**Investigación (el patrón Factory, madurado):**
- **[aeon-deep-research](https://github.com/BankrBot/skills/tree/main/aeon-deep-research)** - síntesis multi-fuente con **tiers de credibilidad por fuente**, confianza por hallazgo y sección adversarial obligatoria.
- **[aeon-rss-digest](https://github.com/BankrBot/skills/tree/main/aeon-rss-digest)** - roll-up diario de feeds con dedup por URL canónica, clustering temático y ranking ponderado. Nuestro "digest" ya resuelto.
- **[aeon-hacker-news-digest](https://github.com/BankrBot/skills/tree/main/aeon-hacker-news-digest)** · **[aeon-huggingface-trending](https://github.com/BankrBot/skills/tree/main/aeon-huggingface-trending)** · **[aeon-paper-pick](https://github.com/BankrBot/skills/tree/main/aeon-paper-pick)** - digests de fuentes técnicas.
- **[aeon-last30](https://github.com/BankrBot/skills/tree/main/aeon-last30)** - investigación social de los últimos 30 días en Reddit/X/HN/web.

### 🛡️ Confianza y gobernanza
- **[Polygraph](https://github.com/BankrBot/skills/tree/main/polygraph)** - **calificaciones de confianza (A-F) para MCP servers y Agent Skills.** Verifica antes de usar, corre un harness abierto (injection, permisos/egress, data-leak, inputs adversariales) y **puede bloquear CI**. Reproducible. Alineado con nuestro untrusted-by-default.

### 🤖 Orquestación
- **[CodeGrid](https://github.com/BankrBot/skills/tree/main/codegrid)** - canvas de macOS donde varios agentes de código corren en paralelo y colaboran por un bus local. Documenta **patrones de orquestación**: delegate, review, pipeline, parallel fan-out, monitor, debate.

### 📐 Formato de skill (referencia de estructura)
`SKILL.md` (frontmatter name+description + instrucciones) + `catalog.json` + `logo.svg` + `references/` + `scripts/`. Útil si estandarizamos nuestras skills.

### ⚪ Descartado
Todo el bloque Web3: Uniswap, Base, Alchemy, tokens/memecoins, staking, bridges, prediction markets, wallets, vesting, DeFi vaults, NFT, L2s.

> **Nota:** el propio repo recomienda tratar las skills como untrusted. Varias dependen de API keys y servicios externos. Auditar antes de cualquier uso.

---

## 🎯 jdrhyne/agent-skills - el más alineado a lo nuestro

Fuente: [jdrhyne/agent-skills](https://github.com/jdrhyne/agent-skills). Skills y prompts para OpenClaw / Claude Code / Codex / Cursor.

**Lo que lo hace destacar:** (1) **toca el filtro de diseño** con piezas serias; (2) tiene orquestación y automejora; (3) **cada skill está escaneada por [AgentVerus](https://agentverus.ai)** - scanner open-source de prompt injection, data exfiltration y amenazas ocultas, con badge de confianza publicado por skill. Es el único repo hasta ahora que publica evidencia de seguridad del propio contenido. **Eso es exactamente nuestro modelo de untrusted-by-default.**

### 🎨 Diseño (FILTRO PRIORITARIO - lo más importante acá)
- **[design-audit](https://github.com/jdrhyne/agent-skills/tree/main/skills/design-audit)** - **auditor premium de UI/UX con filosofía Jobs/Ive.** Es el recurso de diseño más serio que encontramos en toda la ronda. Directo a "mejorar la estética de nuestros proyectos".
- **[frontend-design](https://github.com/jdrhyne/agent-skills/tree/main/prompts/frontend-design)** (prompt) - guías de diseño frontend para UIs hermosas y modernas.
- **[web-design-guidelines](https://github.com/jdrhyne/agent-skills/tree/main/prompts/web-design-guidelines)** (prompt) - revisa código de UI contra las Web Interface Guidelines. Hermano directo del `kj-web-design-guidelines` de VoltAgent.
- **[elegant-reports](https://github.com/jdrhyne/agent-skills/tree/main/skills/elegant-reports)** - reportes PDF con estética nórdica/escandinava. Útil cuando entregamos un documento.

### 🧠 Memoria y automejora (ataca nuestra deuda)
- **[knowledge-graph](https://github.com/jdrhyne/agent-skills/tree/main/clawdbot/knowledge-graph)** - **sistema de memoria de 3 capas:** extracción automática de hechos + grafo de entidades + síntesis semanal. Es un diseño concreto para Kanam Mind.
- **[self-improving-agent](https://github.com/jdrhyne/agent-skills/tree/main/clawdbot/self-improving-agent)** - captura learnings, errores y correcciones para mejora continua. Puente con `skill_workshop`.
- **[autoresearch-loop](https://github.com/jdrhyne/agent-skills/tree/main/skills/autoresearch-loop)** - **loop de mejora guiado por métrica, agnóstico de dominio** (generaliza el autoresearch de Karpathy). Es la versión general de `gated-iteration-loop`.
- **[context-recovery](https://github.com/jdrhyne/agent-skills/tree/main/skills/context-recovery)** - recupera contexto tras compactación/truncado.

### 🤖 Orquestación
- **[task-orchestrator](https://github.com/jdrhyne/agent-skills/tree/main/skills/task-orchestrator)** - orquestación multi-agente con análisis de dependencias, ejecución paralela y **monitoreo de heartbeat auto-reparable**.
- **[planner](https://github.com/jdrhyne/agent-skills/tree/main/skills/planner)** + **[parallel-task](https://github.com/jdrhyne/agent-skills/tree/main/skills/parallel-task)** - planes estructurados + lanzamiento de subagentes en paralelo para tareas desbloqueadas. **Directo a nuestro pipeline A/B.**

### 🛠️ Ingeniería
- **[senior-engineering](https://github.com/jdrhyne/agent-skills/tree/main/prompts/senior-engineering)** (prompt) - principios para construir software como un senior.
- **[munger-observer](https://github.com/jdrhyne/agent-skills/tree/main/prompts/munger-observer)** (prompt) - revisa una decisión con evidencia acotada, contra-evidencia, alternativas, costo de oportunidad y próximos pasos verificables. Es un *devil's advocate* estructurado.
- **[humanizer](https://github.com/jdrhyne/agent-skills/tree/main/prompts/humanizer)** (prompt) - quita las marcas de escritura generada por IA.
- **[remotion](https://github.com/jdrhyne/agent-skills/tree/main/skills/remotion)** - video en React.

### 🔌 Integraciones de negocio (a futuro)
- **ga4** · **gsc** (Search Console) · **google-ads** · **jira** · **salesforce** · **zendesk** · **gong** - todas vía API/CLI. Se activan si un proyecto/cliente las usa.
- **[nutrient-openclaw](https://github.com/jdrhyne/agent-skills/tree/main/skills/nutrient-openclaw)** + MCP servers de Nutrient - conversión/OCR/redacción de PDF self-hosted.
- **[clawddocs](https://github.com/jdrhyne/agent-skills/tree/main/clawdbot/clawddocs)** - experto en la doc de OpenClaw con árbol de decisión y version tracking. Nos ahorraría buscar en docs a mano.

### 🔗 Extra
- **[lobster-workflows](https://github.com/jdrhyne/lobster-workflows)** (repo hermano) - plantillas de workflows con **approval gates, state tracking y pipelines repetibles**. Muy alineado a nuestra pausa obligatoria iterar→revisión→push.

> **Veredicto:** el repo más valioso de la ronda hasta ahora. `design-audit` + `knowledge-graph` + `task-orchestrator` + `autoresearch-loop` son cuatro piezas que atacan cuatro deudas reales. Es el que recomiendo revisar a fondo primero.

---

## 🔧 skillshare - herramienta de gestión de skills (no es contenido)

Fuente: [runkids/skillshare](https://github.com/runkids/skillshare). Binario Go, MIT, macOS/Linux/Windows, sin registry ni telemetría.

**Qué es:** una **fuente única de verdad** para skills, agents, rules, commands, MCP y hooks de 60+ CLIs de IA (OpenClaw, Claude Code, Codex, Cursor, OpenCode...). Sync por symlinks (o copia).

### 🎯 Por qué nos importa (ataca un dolor real)
Nuestro `AGENTS.md` documenta exactamente este problema: el mirror de skills (`.github/skills/`) se desincronizaba, y un `rsync --delete` **borró 111 archivos** (2026-09-28, ADR-079). La regla actual es "las skills viven en `skills/` y en `agents/<rol>/skills/`". Este tipo de herramienta es justo lo que evita que ese desastre se repita:
- **Una fuente → symlinks:** se edita en un solo lugar y se propaga. Nada de copias que divergen.
- **`.skillignore` + `targets` en el SKILL.md:** control fino de qué skill llega a qué target.
- **`skillshare audit`:** escanea prompt injection y data exfiltration **antes** de que la skill llegue al agente. Mismo modelo que AgentVerus/Polygraph.
- **Extras + MCP sync:** maneja MCP y hooks además de skills.
- **Sin telemetría, offline, un binario.** Alineado con nuestro perfil self-hosted.

### ⚠️ Punto de atención antes de adoptarlo
Es una **capa nueva de infraestructura** que pasa a mediar entre el workspace y mis skills. Eso tiene costo: si `skillshare` se rompe o cambia, queda en el medio. Y ya tuvimos una mala experiencia con un sync destructivo (ADR-079). **No adoptar a ciegas:** evaluar si resuelve más de lo que arriesga, y probar en un entorno aislado (no tocar `skills/` real de entrada).

### 📋 Complemento
- **`.skillignore` + SKILL.md `targets`** - concepto útil aunque no usemos la tool: declarar en cada skill a qué target corresponde evita el descontrol.

> **Veredicto:** relevante como **evaluación de tooling**, no como contenido. Resuelve un problema real nuestro (deuda de sync de skills), pero introduce una dependencia estructural. Candidato a prueba controlada, no a adopción inmediata.

---

## 📦 openclaw-manager-plugin (referencia documental, no para instalar)

Fuente: [ClariSortAi/openclaw-manager-plugin](https://github.com/ClariSortAi/openclaw-manager-plugin). MIT, plugin de **Claude Code**.

**Qué es:** convierte a Claude Code en un experto de OpenClaw conversacional - instalación, config de canales, troubleshooting y hardening de seguridad. Proyecto de fin de semana, no afiliado a OpenClaw.

### ⚪ Por qué NO lo adoptamos
- Es un plugin de **Claude Code**, no de OpenClaw. Nosotros corremos el Gateway nativo; meter Claude Code como capa de gestión sería un intermediario innecesario.
- La utilidad principal (guiar a un novato en la primera instalación) no nos aplica: el Gateway ya funciona en la Mac Mini.

### 📖 Lo que SÍ sirve: su documentación como referencia
Los `.md` internos valen como material de consulta:
- **`security-checklist.md`** - checklist de hardening + conciencia de CVEs + procedimientos de auditoría.
- **`troubleshooting.md`** - workflows de diagnóstico y fixes comunes.
- **`cli-reference.md`** - referencia completa de comandos y flags del CLI.
- **`channel-setup.md`** - guías por plataforma (23+ canales).
- **`journey-templates.md` + `feature-matrix.md`** - 7 plantillas de deployment por caso de uso (personal, familia, empresa, developer, Docker/K8s). Modelo interesante de "entrevista → plan personalizado".

> ⚠️ **Ojo con las versiones:** el plugin declara mínimo `v2026.3.1` y recomendado `v2026.5.12+`, y avisa que **Bun rompe WhatsApp/Telegram** (usar Node). Dato a verificar contra nuestra versión real antes de citar.

> **Veredicto:** descartado como instalación. Rescatado como **fuente de checklists** (seguridad/troubleshooting) para cuando armemos el nuestro.

---

## 🛡️ guardspine-openclaw - gobernanza con enforcement real

Fuente: [DNYoussef/guardspine-openclaw](https://github.com/DNYoussef/guardspine-openclaw). Apache-2.0. Plugin de OpenClaw que trae el sistema **GuardSpine** de gobernanza y evidencia.

**Qué es:** intercepta **cada tool call** con un clasificador de riesgo L0-L4 y decide qué pasa, qué se loguea y qué requiere aprobación.

| Tier | Gate | Ejemplos | Latencia |
|------|------|----------|----------|
| **L0** | no-op | `memory_search` | 0ms |
| **L1** | solo log | `web_search`, `read` | <1ms |
| **L2** | evidence pack | `bash`, `apply_patch`, `send_message` | <1ms |
| **L3** | consejo de 3 modelos | `rm -rf`, `curl`, `npm install` | 30-60s |
| **L4** | consejo + humano | `credential_access`, `chmod 777` | manual |

**Escalado dinámico:** los comandos `bash` suben de tier según su contenido, por regex sobre patrones destructivos/red/credenciales.

### 🎯 Por qué nos importa MUCHO
Nuestro `AGENTS.md` tiene las Red Lines en **prosa**, y el enforcement es: (a) mi buen juicio + (b) un único check (`check-agent-skill-boundary.py`). Eso es **auto-regulación**, no enforcement. GuardSpine convierte la regla en un **gate mecánico**:
- **Deny-by-default** con tiers de riesgo y blast radius.
- **Evidence packs hash-chained (SHA-256):** cada tool call L2+ genera una entrada con `chain_hash` que la liga a la anterior → **audit trail tamper-evident**. Es el enforcement del "verificar antes de afirmar".
- **Consejo L3 local:** 3 modelos Ollama (`qwen3:8b` 0.40 + `falcon3:7b` 0.35 + `qwen2.5-coder:7b` 0.25), puntúan 5 dimensiones (resistencia a prompt injection, blast radius, reversibilidad, exposición de secretos, claridad de intención). Agregación determinística: cualquier FAIL = FAIL.
- **Aprobación humana L4 out-of-band:** Discord DM + `/approve <id> allow-once`. **No hay aprobación in-band por el modelo** - el agente no puede aprobarse a sí mismo. Coherente con nuestra política de `/approve`.
- **Redteam harness:** 310+ ataques (jailbreaks Pliny L1B3RT4S, prompt injection, shell injection, bypass de RBAC).

### 🔄 Modos de despliegue (importante)
- **`shadow`** → clasifica y loguea pero **NO bloquea**. Es el modo de entrada obligatorio.
- **`enforce`** → gating activo.
- **`audit`** → pass-through solo dev (requiere env var).
- **`disabled`** → cargado pero inactivo.

> El flujo de adopción del README es sensato: instalar en `shadow`, observar logs, correr el smoke test de redteam, y **solo entonces** pasar a `enforce`.

### ⚠️ Puntos de atención (honestos)
1. **Requiere Ollama local + 3 modelos (~6GB, corren secuenciales).** Latencia 30-60s en L3. En una Mac Mini esto es carga real.
2. **El L4 depende de Discord.** Nosotros operamos por webchat/Telegram; habría que mapear el canal de aprobación.
3. **Es un ecosistema entero** (GuardSpine + spec + verify + kernel + council + webhook + n8n nodes + CI action). Adoptar el plugin es entar a un ecosistema, no a una tool suelta.
4. **README apunta a `github.com/nickarora/openclaw`** - URL que no es la oficial (`openclaw/openclaw`). Verificar provenance del repo antes de instalar.
5. **Todavía no probado por nosotros.** Un auto-reporte del README no es evidencia de que funcione en nuestro setup (nuestra propia regla).

### 📌 Complementos del ecosistema a mirar aparte
- **[guardspine-verify](https://github.com/DNYoussef/guardspine-verify)** - CLI offline para verificar evidence packs.
- **[codeguard-action](https://github.com/DNYoussef/codeguard-action)** - gobernanza en GitHub Actions (CI/CD). Puente con nuestra regla de esperar el CI.
- **[rlm-docsync](https://github.com/DNYoussef/rlm-docsync)** - documentación proof-carrying + lectura de contexto con evidencia. Interesante para la deuda de docs.

> **Veredicto:** el candidato más fuerte a **enforcement real** de nuestras Red Lines. Pero es infraestructura pesada (Ollama + ecosistema + dependencia de Discord) y sin verificar. Recomendación: **probar en `shadow`**, en un entorno aislado, y medir el overhead antes de considerarlo. No adoptar de una.

---

## 💬 clawdbot-feishu - plugin de canal (no aplica, pero patrón útil)

Fuente: [m1heng/clawdbot-feishu](https://github.com/m1heng/clawdbot-feishu). Plugin de canal Feishu/Lark (china).

### ⚪ Por qué NO lo adoptamos
Feishu/Lark es una plataforma empresarial china. No la usamos como canal, y el plugin es específico de ella (23+ permisos de API, scopes de docx/bitable/wiki/task, suscripciones de eventos). Sin valor directo.

### 📌 El patrón que SÍ vale extraer: modelo de control de acceso por canal
Es el ejemplo más detallado que vimos de **política de acceso por canal**, y es un modelo copiable:
- **`dmPolicy`: `pairing` | `open` | `allowlist`** - tres niveles de acceso a DMs. `pairing` (default): el usuario recibe un código y el owner lo aprueba (`openclaw pairing approve`). **Es el mismo modelo de "código de emparejamiento aprobado por el owner" que ya usamos en grupos.**
- **`groupPolicy`: `open` | `allowlist` | `disabled`** + **`requireMention`** - control de si el bot responde en grupos y si exige @mención.
- **Seguridad por defecto:** `allowMentionlessInMultiBotGroup: false` evita que el bot responda a mensajes sin mención cuando hay varios bots (riesgo de doble disparo).
- **`groupCommandMentionBypass`: `never` | `single_bot` | `always`** - permite comandos autorizados (ej. `/new`) sin @, pero **solo cuando hay un único bot**. Default conservador.
- **Aislamiento por cuenta:** `channels.<x>.accounts.<id>` con `dmPolicy` por cuenta, y fallback a los defaults de nivel superior.

> **Para nosotros:** no adoptamos el plugin, pero **el patrón de políticas (pairing/open/allowlist + mention gating + bypass acotado) es una referencia directa** para la regla de "Group Chats - participante, no proxy" del `AGENTS.md`. Si algún día sumamos canales, este es el modelo a seguir.

> ⚠️ Nota: el repo tiene contenido de sponsor (una plataforma de API keys en chino). Ignorar. Y los nombres de scopes están en chino/inglés mezclados.

---

## 🧠 MemOS Cloud Plugin - memoria persistente (⚠️ nube)

Fuente: [MemTensor/MemOS-Cloud-OpenClaw-Plugin](https://github.com/MemTensor/MemOS-Cloud-OpenClaw-Plugin). Plugin oficial de MemTensor. Apache/MIT segun repo.

**Qué hace:** plugin de ciclo de vida que **recall** memorias de MemOS Cloud antes de cada run y **agrega** mensajes después. Se engancha en `before_prompt_build` (recall) y `agent_end` (add). Auth por token.

### ✅ Lo que resuelve (y por qué tienta)
- **Memoria entre sesiones real:** inyecta `<memories>` recuperadas por relevancia antes del prompt. Es exactamente el problema de "despierto fresco cada sesión".
- **Multi-agente nativo:** `multiAgentMode` aisla memoria por `agent_id`, con `allowedAgents` y **`agentOverrides`** por agente (knowledge base, límites, umbral de relatividad, estrategia de captura). Diseño muy pensado para un crew.
- **Recall global vs por conversación:** `recallGlobal` decide si la búsqueda ignora el `conversation_id`.
- **Filtro de recall por modelo:** segunda pasada opcional que descarta candidatos irrelevantes antes de inyectarlos.
- **UI de config local** en `127.0.0.1:38463`.

### 🚧 El problema serio: es **CLOUD**
- Todo el ciclo de memoria sale a `https://memos.memtensor.cn/api/openmem/v1`. **Nuestra memoria es privada** (vida, proyectos, OSS, decisiones). Mandar eso a un servicio de terceros choca de frente con la Red Line de "don't exfiltrate private data".
- Alternativa a mirar primero: **`MemTensor/MemOS` (el core open-source)** para deploy **self-hosted**, no la variante cloud. Si se puede correr local, el cálculo cambia por completo.
- El plugin **no lee credenciales del entorno de proceso** por sandboxing; usa `~/.openclaw/.env`. Bien, pero igual manda datos afuera.

### 📌 Lo que SÍ vale robar (el diseño, no el servicio)
- **`agentOverrides` por agente:** cada rol con su propia knowledge base, límites de recall y umbral de relevancia. Es un patrón de diseño de memoria multi-agente que sí aplica a KanamMind.
- **Recall global vs conversación** + **filtro de segunda pasada** - conceptos útiles para nuestro `memory_search`.
- **Captura por `last_turn` o `full_session`** - decisión de granularidad.

> **Veredicto:** el diseño de memoria es lo más maduro que vimos (multi-agente + overrides + filtro). **Pero es cloud y nuestra memoria es privada.** No adoptar la variante cloud. Si el core `MemTensor/MemOS` permite self-hosted, ahí sí vale una evaluación seria. Pendiente: verificar si existe deploy local.

---

## 🏠 OpenClawHomeAssistant - add-on de Home Assistant

Fuente: [techartdev/OpenClawHomeAssistant](https://github.com/techartdev/OpenClawHomeAssistant). Add-on que corre OpenClaw **dentro de Home Assistant OS (HAOS)**.

### ⚪ Como implementación: no aplica
No usamos Home Assistant. Y nuestro gateway ya corre nativo en la Mac Mini (ADR-073); meterlo dentro de un add-on de HAOS sería una capa innecesaria.

### 🔑 Diseño: lo que enseña
- **Persistencia separada del runtime.** "Skills, config y workspace **sobreviven a las actualizaciones del add-on**." Es la separación correcta entre *código/versión* y *estado/datos*. Nuestro equivalente: `~/.openclaw/workspace/` (estado) vs el binario de OpenClaw (runtime). Principio aplicable cuando actualicemos y algo se pierda.
- **Superficie de integración estándar (OpenAI-compatible API).** El add-on expone OpenClaw como *conversation agent* vía una **API compatible con OpenAI**, para enchufarlo al pipeline Assist de HA. Lección: **exponer una interfaz estándar** deja que cualquier consumidor nos use sin integración a medida. Es el mismo argumento detrás de los MCP servers.
- **Empaquetado self-contained.** Trae Chromium, git, vim, ripgrep, jq, python3, pnpm, Homebrew - todo adentro. Lección de portabilidad: un entorno reproducible que no depende de lo que tenga el host.
- **Web Terminal embebida.** Da acceso a shell desde la UI del host. Nosotros ya tenemos `terminal`.

> **Veredicto:** descartado como add-on. Rescatados tres principios de diseño: **persistencia ≠ runtime**, **interfaz estándar como superficie de integración**, y **empaquetado self-contained**. El primero es directamente relevante para nuestras actualizaciones del Gateway.

---

## 🔌 MCP Adapter - puente MCP → tools nativas (candidato real)

Fuente: [androidStern-personal/openclaw-mcp-adapter](https://github.com/androidStern-personal/openclaw-mcp-adapter). MIT.

**Qué hace:** conecta a servidores MCP al arrancar el gateway, descubre sus tools y **registra cada una como tool nativa de OpenClaw** (con nombre, descripción y JSON Schema). Cuando el agente la invoca, proxea la llamada al server MCP. Reconexión automática.

### ✅ Por qué es candidato... pero **ya no hace falta**
> **VERIFICADO (2026-10-01):** OpenClaw **ya tiene soporte MCP nativo** - ver la doc oficial de OpenClaw sobre MCP (`tools/mcp.md` dentro del paquete npm `openclaw`). Definiciones en `mcp.servers`, alta por Control UI (Settings → MCP), CLI (`openclaw mcp add`) y config. Transportes **Streamable HTTP, SSE y Stdio**. Los tools pasan por **el mismo tool-profile y tool-policy controls** que todo lo demas (`connecting a server does not bypass your policy`). Verificación real con `openclaw mcp doctor <name> --probe` ("Saving a definition proves nothing about reachability - the probe does"). Hay hot reload, filtros de herramientas por sesión, y hasta el sentido inverso (`openclaw mcp serve` expone OpenClaw COMO server MCP).
>
> **Conclusión: este plugin es REDUNDANTE.** Agrega una dependencia para cubrir algo que el core ya resuelve mejor - con control de política integrado y verificación con probe.

**Lo que igual enseña (capa diseño):**
- **Registrar herramientas externas como tools de primera clase** - nombre, descripción y JSON Schema. Es el mecanismo que el core ya implementa.
- **`toolPrefix` para evitar colisiones** de nombres entre servers.
- **Interpolación `${VAR}`** para no hardcodear credenciales.

### ⚠️ Lo que SÍ hay que retener de todo esto
La lección no es el plugin: es que **el core ya expone MCP**, y que conectarse es una decisión de **política**, no de capacidad. Cada server MCP es superficie nueva y debe pasar por el tool-policy y por el modelo untrusted-by-default (es justo lo que `Polygraph` evalúa).

> **Veredicto FINAL: descartado por redundante.** El core ya hace esto, y mejor (política + probe + hot reload + doble sentido). Antes de sumar cualquier server MCP del ecosistema, usar `openclaw mcp add` + `openclaw mcp doctor --probe`, no este plugin.

---

## 🎛️ Claw Orchestrator - runtime de orquestación (alto candidato)

Fuente: [Enderfga/claw-orchestrator](https://github.com/Enderfga/claw-orchestrator). MIT, npm `@enderfga/claw-orchestrator`, CLI `clawo`. CI propio.

**Qué es:** un runtime que envuelve CLIs de código (Claude Code, Codex, Antigravity, Grok Build, OpenCode, o cualquier CLI custom) como **sesiones persistentes programables**, y le monta una capa de orquestación de 78 tools. Accesible por CLI, plugin de OpenClaw, MCP, ACP, o TypeScript directo.

### 🎯 Las cuatro features que atacan nuestras deudas

**1. Verification Plane - el enforcement de "no dar falso verde"**
> Contratos de aceptación que **el runtime ejecuta él mismo** (comandos, HTTP probes, screenshots, diff policy, asserts de archivos) y produce un evidence bundle. Un run con contrato **no puede llegar a `completed` si no pasa**. Uno **sin contrato termina como `unverified`, no como `success`**. Y los tests del contrato quedan fijados a lo que el run arrancó, así **no puede pasar editando los tests**.

Esto es exactamente el problema de nuestra `verification-gates`. Y va más lejos: distingue **self-report (`ok`)** de **medición del runtime (`verified`)**. Es la implementación de "un auto-reporte de subagente no es un hecho", hecha infraestructura.

**2. Run Ledger & Spend Caps - ADR-090 hecho mecánica**
Ledger JSONL durable: cada turno con engine, modelo, tokens, costo, duración. `maxBudgetUsd` **enforced por el runtime**, no por buena voluntad. Coherente con nuestro "no gastar recursos innecesarios".

**3. Durable Run Kernel - nuestra pausa obligatoria, como grafo**
Workflows declarativos sobre nodos `agent` / `fanout` / `council` / `verifier` / **`human_gate`** / `router` / `subflow` / `autoloop`. Cada transición se **checkpointed**, así un run **sobrevive un reinicio y retoma en el borde del nodo**. Tiene `human_gate` nativo - es nuestro iterar→revisión→push→borrador, formalizado.

**4. Orquestación multi-agente**
- **Council:** agentes paralelos en **worktrees de git aislados**, votando hasta consensuar.
- **Fan-out:** una tarea en N agentes (distinto engine/modelo) en paralelo + pasada de síntesis. Es el best-of-N cross-engine.
- **Autoloop:** subloop autónomo Planner / Coder / Reviewer con **engine y modelo independientes por rol**.
- **Session Handoff:** mover una conversación viva a otro engine/modelo ("una sesión Claude trabada → Codex", "modelo caro → barato"), y la nueva retoma donde la otra quedó.

### 📌 Detalles de diseño que valen por sí solos
- **Sweep semanal sin llamadas a modelo:** `scripts/sweep.ts` mide versiones instaladas/pinned/upstream, difea los flags del wrapper vs `--help` del binario, corre un turno real **por la clase wrapper real**, y valida precios contra las tablas de los vendors. **"The check that reports a wrapper as broken does not share the wrapper's failure modes."** - separar el verificador de lo verificado. Es la versión más elegante de nuestro principio que vimos.
- **El orquestador no edita su propio código unattended:** su propio workflow de sweep termina en un `human_gate`. Predica con el ejemplo.

### ⚠️ Puntos de atención
1. **`install.sh` con `curl | bash`** que registra el plugin y **reinicia el gateway**. Invasivo: tratar como untrusted, leer el script antes.
2. **Capa sobre capas:** nosotros ya usamos Claude Code vía Ollama en el pipeline. Esto envuelve CLIs de código - hay que ver si convive con nuestro setup (Ollama + deepseek) o lo reemplaza.
3. **78 tools + dashboard + server HTTP (`:18796`) + token en `~/.openclaw/server-token`** - superficie grande. Evaluar blast radius.
4. **No verificado por nosotros.** README extenso ≠ funciona en nuestro setup.

> **Veredicto:** el **candidato más fuerte a adopción** de la ronda junto con jdrhyne. `Verification Plane` + `Run Ledger` + `human_gate` + `durable kernel` son cuatro piezas que apuntan directo a deudas nuestras. Pero es infraestructura grande sobre un setup que ya tiene su pipeline - evaluar si **reemplaza** nuestro pipeline A/B (y vale) o si lo **duplica** (y no). Empezar por leer `verification.md` y `workflow.md` como diseño, antes de tocar el install.

---

## 🔁 openclaw-mcp-server - exponer OpenClaw COMO server MCP

Fuente: [Helms-AI/openclaw-mcp-server](https://github.com/Helms-AI/openclaw-mcp-server).

**Qué es:** el sentido inverso del adapter. Expone las tools del Gateway (messaging, sessions, cron, nodes, web, memory, TTS) a **clientes MCP externos** - Claude Code, Claude Desktop, Zed, Cline, Windsurf.

### ⚪ Veredicto: redundante (igual que el adapter)
> **VERIFICADO (2026-10-01):** el core ya lo hace - la doc oficial de OpenClaw lo dice explícito: *"For the reverse - exposing OpenClaw channel conversations to another MCP client - use `openclaw mcp serve`"*. (`openclaw mcp serve` / `openclaw-as-an-mcp-server`).
>
> El plugin agrega un server Node aparte + token + config por cliente, para cubrir algo que el CLI resuelve nativo.

### 🔑 Diseño: lo que enseña
- **`openclaw mcp serve` es la pieza que sí importa** de esta idea: OpenClaw no solo consume MCP, también **se expone como MCP**. Eso permite que Claude Code / cualquier cliente MCP maneje el Gateway (mandar mensajes por Telegram, criar crons, spawnear sesiones) desde afuera.
- **Caso de uso real:** si en algún momento queremos que un Claude Code (u otro harness) opere el Gateway sin pasar por el chat, la vía nativa es `mcp serve`. No hace falta este repo.
- **La superficie que expone** (messaging + sessions + cron + nodes + memory) es un buen inventario de *qué* de OpenClaw tiene sentido exponer, independiente de la tool.

> **Veredicto FINAL:** descartado por redundante. La capacidad existe nativa (`openclaw mcp serve`). Queda registrado el concepto: **OpenClaw es consumidor Y servidor MCP**, y eso abre la puerta a ser operado desde cualquier harness compatible.

---

## 🪄 MemoV - VibeGit: memoria Git-powered de sesiones de código (candidato real)

Fuente: [memovai/memov](https://github.com/memovai/memov). MIT. Python (requiere `uv`).

**Qué es:** una capa de memoria para agentes de código que versiona **prompts, contexto y diffs de código** usando Git por debajo. Lo llama **VibeGit**: cada interacción se snapshotea, se puede branch, rollback y replay.

### ✅ Por qué es candidato real
- **Local, sin DB, sin overhead.** (`Private-first`.) Alineado con nuestro perfil self-hosted.
- **Zero pollution del `.git`:** timeline shadow en `.mem`, separada del repo real. Resuelve el miedo de ensuciar el historial.
- **Agnóstico del agente:** se conecta por MCP a Claude Code, Codex, Cursor, VS Code. Nosotros tenemos el runtime MCP nativo.
- **Branch exploration + rollback que preserva:** el cuadro comparativo con "checkpoints" es sólido - rollback que no borra historia, y cada salto queda trazado.

### 🎯 El problema que ataca (y por qué nos duele)
Hoy, cuando corre el pipeline A/B o un subagente edita código, **el rastro de por qué se tomó cada decisión se pierde**. MemoV guarda, por interacción: el prompt del usuario, la respuesta del agente, el plan y los archivos cambiados. Es **la contraparte de datos de nuestra pausa iterar→revisión→push**: quedaría el *por qué* codificado junto al *qué*.

### 🔑 Diseño a robar (incluso sin instalarlo)
- **`snap(prompt, response, plan, files_changed)`** - un registro de interacción con **cuatro campos** que es un buen contrato: qué pedí, qué respondió, qué plan siguió, qué tocó.
- **Shadow timeline fuera del control de versiones real.** El principio: la trazabilidad del agente **no debe contaminar** el artefacto de producción. Aplicable a nuestra separación `.knowledge/` vs código.
- **`validate_commit` / `validate_recent` (RAG):** compara prompt/respuesta contra los cambios de código reales y **detecta "context drift"** - cuando lo que se hizo no coincide con lo que se pidió. **Eso es la versión máquina de nuestro `delegation-result-verification`.**
- **`vibe_debug`:** busca en el historial y consulta varios modelos en paralelo. Cruza con el patrón Fan-out de Claw Orchestrator.

### ⚠️ Puntos de atención
1. **Requiere `uv` + Python 3.10+** (cadena nueva de tooling).
2. **El modo RAG con VectorDB está `🚧 WIP`** - declarado, no terminado.
3. **`curl | bash`** en varias vías de install. Leer antes.
4. **No verificado por nosotros.** Y su foco declarado son *coding agents*, no un gateway multi-rol; hay que ver cómo convive con el nuestro.

> **Veredicto:** candidato real a **evaluación**, tercera posición después de Claw Orchestrator y jdrhyne. Dos ideas se llevan aunque no se instale: el **contrato `snap(prompt, response, plan, files_changed)`** y la **validación de context drift** (prompt vs diff real). Ambas responden a deudas nuestras de trazabilidad y verificación.

---

## 🧠 MemOS (core) - **RESUELVE el pendiente de la nube** ✅

Fuente: [MemTensor/MemOS](https://github.com/MemTensor/MemOS). `memos-local-plugin 2.0`, npm `@memtensor/memos-local-plugin`.

### 🔓 El pendiente que quedó abierto, cerrado
Cuando analizamos el plugin cloud, dejé un pendiente: *"¿existe deploy local?"*. **Sí existe, y es de primera clase.**

MemOS da **cuatro entry points**, y dos son locales:

| | Cloud | Self-Host | Cloud Plugin | **Local Plugin** |
|---|---|---|---|---|
| Infra | ninguna | Neo4j + Qdrant | ninguna | **ninguna (SQLite local)** |
| **El dato vive** | nube | tus servers | nube | **tu máquina** |

El **`memos-local-plugin`** es justo lo que necesitamos: **100% on-device, sin salir de la máquina**, con SQLite persistente.

### 🎯 Lo que lo hace candidato fuerte para KanamMind
- **Híbrido FTS5 + vector** - búsqueda de texto completo + semántica. Es exactamente la capa que le falta a nuestro `memory_search` sobre SQLite.
- **Memoria estructurada como grafo, "inspectable y editable, no un embedding store de caja negra"** - alineado con nuestro modelo de memoria auditable (DB como fuente de verdad).
- **Multi-cube:** bases de conocimiento como *cubes* componibles, con aislamiento y sharing controlado por usuario/proyecto/agente. Es el `agentOverrides` del cloud, pero local.
- **Skill evolution por tiers: L1 traces / L2 policies / L3 world model.** Un modelo de crecimiento de memoria en capas - coincide con nuestra idea de learnings → reglas → ADRs.
- **Feedback y corrección en lenguaje natural** - se corrige, suplementa o reemplaza una memoria con el tiempo.
- **Multi-agente + Memory Viewer dashboard** (UI para inspeccionar).

### 📊 Evidencia de impacto (del propio repo)
> *"With MemOS, **OpenClaw** improves average task completion from **36.63% to 50.87%** across five agent tasks."*

Números del vendor - **no verificados por nosotros**, pero es la mejora más concreta que reporta cualquier repo de la ronda sobre OpenClaw específicamente.

### ⚠️ Puntos de atención
1. **Es un proyecto de investigación** (arXiv, benchmarks propios, paper académico). Serio, pero orientado a academia/empresa. Ver si el plugin local es igual de mantenido que el cloud.
2. **`curl | bash`** en el install. Leer antes (nuestra regla).
3. **Aislamiento:** antes de instalar, correr en `mktemp -d` o con un workspace de prueba, no sobre la memoria real.
4. **Solapa con el plugin cloud** (misma casa). Elegir uno.

> **Veredicto: el candidato a memoria MÁS fuerte de la ronda.** Resuelve la objeción principal (privacidad) al ser local-first, y ataca directo el hueco de KanamMind (búsqueda semántica + multi-agente + evolución por tiers). **Prueba controlada recomendada:** instalar en entorno aislado, medir el recall contra nuestro `memory_search` actual, y evaluar el overhead de SQLite + vector.
>
> **Antes de instalar:** comparar con `tobi/qmd` (markdown-native) y con la opción de solo agregar embeddings a `memory.db`. Tres caminos, elegir uno.

---

## 🧠 MoltBrain - memoria local para agentes de código

Fuente: [nhevers/MoltBrain](https://github.com/nhevers/MoltBrain). **AGPL-3.0** (ojo: copyleft fuerte).

**Qué es:** capa de memoria de largo plazo para OpenClaw / Claude Code que aprende y recuerda contexto de proyecto automáticamente. Captura observaciones vía hooks de ciclo de vida, las guarda, y las inyecta antes de cada sesión.

### ✅ La parte útil (local)
- **Arquitectura simple y copiable:** hooks `SessionStart` (inyecta contexto) / `PostToolUse` (captura output, extrae hechos) / `Stop` (genera resumen) → Worker service (`localhost:37777`) → **SQLite (observaciones, resúmenes, sesiones) + ChromaDB (similitud semántica)** + Web Viewer.
- **Es exactamente el par que buscamos:** SQLite como fuente de verdad + **capa vectorial aparte**. Confirma el patrón que veníamos deduciendo (FTS5/vector sobre datos estructurados).
- **`OBSERVATIONS` (descubrimientos/decisiones/código), ANALYTICS (tokens/sesiones), EXPORT (JSON/CSV/MD), TAGS, FAVORITES** - un modelo de datos de memoria completo.
- **Todo local:** `~/.moltbrain/settings.json`, worker en localhost, viewer en `:37777`. Sin nube en esta capa.

### 🚫 La parte que se descarta (cripto - regla dura)
- **Storage Dapp:** blobs vía **x402 micropagos en USDC sobre Base**, "Agent Vault por wallet", Virtuals Protocol, integración con MoltBook. **Todo eso es Web3/cripto → fuera, sin analizar.**
- El README está muy cargado de eso; hay que separarlo a mano.

### 🔑 Diseño a robar (sin instalar)
- **El ciclo de 3 hooks con responsabilidades distintas:** inyectar contexto al arrancar / capturar hechos al usar tools / resumir al terminar. Es una separación limpia del ciclo de memoria, y usa los mismos momentos que ya conocemos (`before_agent_start`, `agent_end`).
- **`MOLTBRAIN_CONTEXT_OBSERVATIONS` (default 50)** - límite explícito de cuántas observaciones inyectar. Control de ruido, mismo problema que ataca el `recallFilter` de MemOS.
- **`export` a Markdown** - la memoria se puede volcar a texto legible. Alineado con nuestro modelo `.md` + DB.
- **`prune` con días configurables** - política de retención explícita.

### ⚠️ Puntos de atención
1. **AGPL-3.0** - copyleft fuerte. Si se integrara a algo distribuido, arrastra la licencia. Verificar implicancia antes de adoptar.
2. **Entrelazado con cripto** en el ecosistema (MoltBook, Virtuals, x402). Separar la capa local de la comercial.
3. **Solapa con MemOS local** (misma función: memoria persistente local con vector). **Son alternativas, no complementos.**
4. Repo personal, no oficial.

> **Veredicto:** la versión local es un **candidato a memoria**, en línea con MemOS local pero más simple y con SQLite+ChromaDB explícito. **La parte cripto se descarta por regla.** Elegir entre este y MemOS local - no ambos. Riesgo adicional: **licencia AGPL**.

---

## 🔄 PowerContext (OceanBase) - handoff de contexto entre humano y agente

Fuente: [oceanbase/powercontext](https://github.com/oceanbase/powercontext). Apache-2.0. PyPI `powercontext`, CLI + Server + Dashboard. Sucesor de **PowerMem**.

**Qué es:** *"Context for work that humans and agents hand off and continue."* Mantiene el contexto **pegado al trabajo** a través de conversaciones y handoffs, para que quien retome (humano u otro agente) no tenga que releer toda la historia.

### 🎯 Ataca exactamente un problema nuestro
> *"Work rarely ends with whoever starts it. You hand a task to an agent, the agent gets part of the way, and later you or someone else takes over. The reasoning and current state often stay behind in that conversation."*

Nuestro `AGENTS.md` tiene la regla del **HANDOFF** y el principio de "que el próximo yo pueda retomar sin re-descubrir todo". Esto es eso, convertido en sistema. **Y su modelo de datos calza con nuestras capas:**

| PowerContext | Nuestro equivalente |
|---|---|
| **Memory** | memoria durable (`MEMORY.md` / `daily`) |
| **Handoff** | HANDOFF.md - objetivo + estado actual |
| **Experience** | learnings |
| **Skill** | `skills/` / skill workshop |

Y agrega lo que nos falta: **conserva fuentes y revisiones anteriores** de cada ítem, y **todo queda dentro del *scope* del trabajo**.

### ✅ Por qué es candidato fuerte
- **Apache-2.0** (permisiva, sin el riesgo AGPL de MoltBrain).
- **Local:** `powercontext server run` en tu máquina. Dashboard propio. Storage local.
- **Integración OpenClaw de primera clase** (lista junto a Codex, Claude Code, DSH, Hermes, LangChain, Pydantic AI...). Codex es `official`; OpenClaw figura como `community`.
- **`doctor` + acceptance checks observables:** *"check that a real prompt becomes a Source, produces a Topic, evolves after a related prompt, and can be recalled in a new session"*. **Eso es verificación de que la memoria funciona, no autodeclaración.** Muy alineado a nuestra forma de trabajar.
- **Benchmarks públicos con limitaciones declaradas** (LoCoMo, SWE-bench Pro) y sección de methods/limitations.

### 🔑 Diseño a robar
- **La separación Memory / Handoff / Experience / Skill** como cuatro clases de artefacto con ciclo de vida distinto. Es más limpio que nuestro "todo va a memory/".
- **Scope del trabajo:** cada ítem vive dentro del ámbito de una tarea, con **fuentes y revisiones preservadas**. Es trazabilidad de memoria.
- **`Experience` → `Skill`** como promoción explícita: lo que se repite se vuelve skill. Formaliza algo que hoy hacemos intuitivamente.
- **`powercontext doctor <host>`** - un comando de verificación de integración. Patrón a copiar.

### ⚠️ Puntos de atención
1. **No es solo local-friendly: el wizard ofrece "Full memory" vs "Basic memory".** Full requiere **credenciales separadas de Generation + Embedding** (o sea, un modelo que provea). Basic guarda/recupera explícito sin APIs extra. Elegir bien.
2. **Entorno Python** (`uv`, Python 3.11+) - cadena nueva, como MemoV.
3. **`experimental` en Windows.** macOS/Linux ok.
4. **Repo de vendor** (OceanBase), aunque Apache-2.0 y open source. Es producto con respaldo, no side project - a favor y en contra.
5. **No verificado por nosotros.**

> **Veredicto: candidato fuerte, con el mejor *encaje conceptual* de toda la ronda.** No compite con MemOS/MoltBrain en "recall semántico" - **los complementa**: PowerContext es el *handoff y la organización del trabajo*, ellos son el *motor de retrieval*. Si fuéramos a adoptar algo de memoria, la pregunta es si PowerContext reemplaza parte de nuestro flujo de HANDOFF/daily, o si convive. **Segundo candidato real**, después de MemOS local.

---

## 👁️ Crabwalk - monitor visual en tiempo real (candidato real)

Fuente: [crabwise-ai/crabwalk](https://github.com/crabwise-ai/crabwalk). CLI + Docker. Conecta por **WebSocket al gateway**.

**Qué es:** un monitor en vivo de los agentes de OpenClaw. Grafo de nodos interactivo (ReactFlow) que muestra sesiones, cadenas de acciones, estados de "thinking" y tool calls **a medida que pasan**.

### 🎯 Ataca un problema que ya identificamos
> Cuando revisamos `mission-control` (vincentkoc), dije: *"nuestro pipeline A/B y los spawns corren a ciegas"*. **Crabwalk es la respuesta directa a eso.**

- **Live activity graph:** cada sesión y cadena de acciones como grafo navegable.
- **Action tracing:** expandir un nodo y **ver los args y payloads reales** de cada tool call. Eso es debug de orquestación, no logs de texto.
- **Multi-plataforma:** monitorea todos los canales a la vez.
- **Autodetección de token** desde `~/.openclaw/openclaw.json` → config cero en local.
- **QR code** para abrir el monitor en el teléfono.

### ✅ Por qué es candidato real
- **Local y liviano:** un binario, server en `:3000`, WebSocket a `127.0.0.1:18789`. Sin nube.
- **Se instala como skill:** hay un `skill.md` que el propio agente puede leer e instalar. (Ojo: instalar algo leyendo un `skill.md` remoto - auditar antes; es el patrón que nuestra política marca como untrusted.)
- **Docker-first**, con soporte documentado para `bind: loopback` + tailnet (`network host`).
- **Stack moderno** (TanStack Start, ReactFlow, Framer Motion, tRPC) → **calidad visual**, relevante al filtro de diseño.

### 🔑 Diseño a robar
- **Ver el *chain* de acciones, no líneas de log.** La visualización como grafo de dependencia entre nodos es mucho más informativa que un stream.
- **Payloads inspeccionables por nodo.** Poder abrir un tool call y ver exactamente qué se le pasó 
- **Cero-config por autodetección** del token del gateway.

### ⚠️ Puntos de atención
1. **Bind `0.0.0.0` por defecto** - expone el server en la red. Con el token del gateway, cambiar a loopback o asegurar el acceso.
2. **El token del gateway viaja al server de Crabwalk.** Es un componente más con acceso a credenciales - tratarlo con el mismo cuidado.
3. **Repo de tercero** (`crabwise-ai` / autor `luccast`) - no oficial.
4. **No verificado por nosotros.**

> **Veredicto: candidato real a evaluar, categoría *observabilidad*.** Responde directo al "corremos a ciegas". No solapa con los candidatos de memoria - es otra pata. **Prueba de bajo riesgo:** correrlo en loopback y ver si el grafo realmente hace visible lo que hoy inferimos del transcript.

---

## 🧰 Natilius - bootstrap de entorno de desarrollo en macOS

Fuente: [vincentkoc/natilius](https://github.com/vincentkoc/natilius). **GPL-3.0** (copyleft). Homebrew tap o script.

**Qué es:** *"Your Mac, ready to code. One command."* Bootstrap declarativo de entorno de desarrollo para macOS: instala Homebrew + 100+ paquetes, lenguajes versionados (Python, Node, Ruby, Go, Rust, Java), DevOps (Docker, Kubernetes, Terraform, cloud CLIs), IDEs, y ajustes de seguridad del sistema (FileVault, Firewall, Gatekeeper).

### ⚪ Como implementación: no aplica hoy
- Nuestra máquina ya funciona; no es una Mac nueva que necesita bootstrap.
- **GPL-3.0** - copyleft fuerte. Instalarlo como dependencia del flujo de trabajo arrastra implicaciones de licencia. A diferencia de AGPL, GPL aplica a distribución del binario - igual, verificar antes de integrarlo.

### 🔑 Diseño a robar (varios, buenos)
- **Perfiles:** `minimal`, `devops`, `developer`, o custom. **Un solo comando, varios entornos.** Es el mismo patrón que usamos con roles (CORE/DEV/OPS/MIND/STUDIO) pero aplicado a máquinas.
- **Idempotente:** *"safe to run repeatedly"*. Propiedad que deberíamos exigir a cualquier script de setup.
- **`setup --check` → dry-run.** Previsualizar cambios antes de aplicarlos. **Es nuestra regla de "inspeccionar antes de modificar" hecha comando.**
- **`natilius doctor`** - chequeo de estado del sistema. Segundo repo seguido con un comando `doctor` (también lo tiene PowerContext). **Patrón de verificación que se está volviendo estándar.**
- **Respeta políticas MDM** - no pisa configuración gestionada. Principio de "merge, no overwrite" que ya tenemos en AGENTS.md.
- **Todo declarativo y versionado** - el entorno es código, reproducible.

### 📌 Por qué vale igual (incluso sin instalar)
El problema que resuelve - **reproducibilidad del entorno** - es el mismo que tenemos a otra escala: la Mac Mini corre el gateway 24/7 y su estado importa. Tener un **manifiesto declarativo de qué tiene la máquina** es OPS básico. Hoy ese conocimiento está disperso.

> **Veredicto:** descartado como install (no hay Mac virgen que bootstrapear) y con licencia GPL a vigilar. **Rescatado como modelo:** `--check` dry-run, `doctor`, perfiles, e idempotencia. Es la referencia para cuando documentemos/aseguremos el entorno de la Mac Mini.

---

## 🛡️ ClawSec (Prompt Security / SentinelOne) - seguridad de runtimes de agente

Fuente: [prompt-security/clawsec](https://github.com/prompt-security/clawsec). **AGPL-3.0-or-later.** De Prompt Security (SentinelOne) - **vendor de seguridad con respaldo corporativo**. CI + pages + poll NVD.

**Qué es:** colección de skills de seguridad + **inteligencia de advisories firmada** para runtimes de agentes (OpenClaw, NanoClaw, Hermes, Picoclaw).

### 🎯 Las cuatro capas de protección
| Capa | Qué hace |
|---|---|
| **Signed intelligence** | Verifica el feed de advisories y el manifiesto de checksum **antes** de cruzar riesgo publicado contra las skills instaladas. |
| **Guarded installs** | Frena ante un match de advisory y **requiere una segunda confirmación explícita** antes de continuar. |
| **Integrity & drift** | Baselines por plataforma para archivos críticos, config, atestaciones y artefactos de release. |
| **Audits & reporting** | Auditoría, postura, self-test y reporte comunitario. |

> *"ClawSec recommends and gates actions; destructive removal and install overrides remain approval-controlled."*

### 🎯 Por qué es MUY relevante para nosotros
- **`soul-guardian`:** detecta **drift en archivos de agente** (cambia un archivo protegido → detecta el mismatch → guía la respuesta). **Eso es exactamente nuestra preocupación** por la integridad de `SOUL.md`/`AGENTS.md`/skills. Un cambio silencioso en el bootstrap sería un ataque o un accidente grave.
- **Advisory feed firmado** con Ed25519, key pinneada, runbook de firma. Modelo de confianza verificable, no "confiá en mí".
- **Guarded installs con doble confirmación** → es el `untrusted-by-default` de nuestra política, con gate real de aprobación.
- **Complementa a guardspine:** guardspine gatea *tool calls* por riesgo; ClawSec gatea *instalaciones de skills* y vigila *drift de archivos*. **Dos capas distintas del mismo problema.**

### 🔑 Diseño a robar
- **Separar "agregar el paquete" de "activar el hook persistente":** dos pasos, ambos revisables. El setup **imprime su preflight antes de cambiar config persistente**. Es nuestra regla de inspeccionar antes de modificar.
- **Feed firmado con clave pinneada** - para consumir advisories de terceros sin confiar ciegamente.
- **Baseline de archivos críticos** con detección de drift. Directamente aplicable a nuestro bootstrap y skills.
- **`wiki/` como fuente de verdad** con exports LLM-ready generados. Modelo de documentación.

### ⚠️ Puntos de atención
1. **AGPL-3.0-or-later** - copyleft fuerte. Igual que MoltBrain. Verificar implicancias antes de integrar.
2. **`npx skills add ... --global -y`** instala globalmente con `-y`. **No usar `-y` a ciegas** - leer preflight y revisar.
3. **Es de un vendor de seguridad** (SentinelOne). Producto comercial de fondo; open-source el código. Doble filo: respaldo y experiencia, pero interés comercial.
4. **No verificado por nosotros.** Y su instalación toca config persistente del gateway.

> **Veredicto: candidato fuerte en la categoría SEGURIDAD, y complementa a guardspine.** `soul-guardian` (drift de archivos de agente) y la inteligencia de advisories firmada son cosas que hoy no tenemos. Pero es AGPL y su installer modifica config persistente - **prueba aislada, preflight leído, sin `-y`**. Y es el **cuarto candidato real** de la ronda.

---

## 🏁 Cierre de la primera tanda (20 repos)

**Balance:** de 20 repos, muy pocos son "instalar y usar". El valor se repartió en:
- **4 candidatos reales a adopción:** MemOS local (memoria), PowerContext (handoff), Claw Orchestrator (orquestación+verificación), Crabwalk (observabilidad).
- **2 candidatos en seguridad:** guardspine (gate de tool calls) y ClawSec (drift + advisory) - **complementarios entre sí**.
- **Muchos "buenos como diseño, innecesarios como implementación":** los dos MCP (redundantes con el core), skillshare, MemoV, HomeAssistant, MCP adapter.
- **Reglas nuevas que salieron de la ronda:** cripto = fuera; dos capas (implementación vs diseño); **verificar qué hace el core antes de sumar tooling externo**.

**Patrón transversal:** tres de los candidatos (Claw Orchestrator, MemoV, ClawSec) resuelven el mismo problema de fondo - **trazar, verificar y proteger lo que hizo el agente**. El ecosistema está convergiendo ahí. Eso sugiere que *ese* es el hueco real de nuestro setup.

---

## 🗂️ Segunda tanda

### 🎛️ Mission Control (rdsthomas) - Kanban visual para el asistente

Fuente: [rdsthomas/mission-control](https://github.com/rdsthomas/mission-control). **MIT.** v2.2.1, estado *stable*. Construido para **Clawdbot**.

> **⚠️ Ojo con el homónimo.** Este es **otro** repo que el `mission-control` de [vincentkoc](https://github.com/vincentkoc/mission-control) que mencionamos al analizar Crabwalk. Aquel era un dashboard/observabilidad; este es un **tablero Kanban chat-to-task**, una generación anterior (época Clawdbot). No confundir.

**Qué es:** un tablero Kanban (Permanent / Backlog / In Progress / Review / Done) donde **el humano y el agente trabajan sobre la misma fuente de verdad**. El humano arrastra tarjetas en el dashboard; el agente crea, mueve y completa tareas por chat o por CLI. Trae además una pestaña **Brain** (memoria: edita `MEMORY.md`, hojas diarias, changelog) y una de **Skills** (ver/configurar capacidades).

**El problema que ataca:** exactamente el nuestro. *"Después de una semana tenés 50+ tareas dispersas en cientos de mensajes. ¿Dónde quedó aquel refactor?"* Nuestro backlog vive en `memory.db` (tabla `todos`) y **no es visible** - hay que pedirlo. Esto es el backlog **como objeto visual permanente**.

#### 🔧 La arquitectura (lo más valioso)

**GitHub como hub**, en tres roles a la vez: **almacén de datos** (`data/tasks.json` es la fuente de verdad), **bus de eventos** (webhooks) y **hosting estático** (GitHub Pages sirve el dashboard).

```
Dashboard (GitHub Pages)  --commit via API-->  GitHub (tasks.json)
                                                    |  webhook
                                                    v
                                            Tailscale Funnel (HTTPS)
                                                    v
                                     Gateway :18789  /hooks/github
                                                    v
                                     Transform (.mjs): valida HMAC + diff
                                                    v
                                              Agente (trabaja)
                                                    v
                                     mc-update.sh -> git commit + push
```

**Canal 1 (Dashboard -> Agente):** el humano mueve una tarjeta -> el dashboard hace commit a GitHub -> GitHub dispara webhook -> Tailscale Funnel -> gateway -> **transform** que valida HMAC, lee el estado previo del *snapshot*, fetchea el estado nuevo, **calcula el diff** y **solo si una tarea pasó a `in_progress`** despierta al agente con una *work order*.

**Canal 2 (Agente -> Dashboard):** el agente modifica `tasks.json` con `mc-update.sh`, hace commit + push, y GitHub Pages redespliega. El dashboard refresca.

#### 🔑 Diseño a robar (varios, muy buenos)

- **GitHub como hub de datos + bus de eventos + hosting.** Sin servidor propio, sin base de datos que mantener. La fuente de verdad es un archivo versionado, con historia, resolución de conflictos y auditabilidad **gratis**.
- **Trigger por diff, no por evento crudo.** El transform compara snapshot viejo contra estado nuevo y **solo despierta al agente si hay una transición relevante** (tarea a `in_progress`). No se despierta por cualquier push. Evita el ruido y el gasto.
- **Git Blob API para consistencia exacta por SHA.** Eligen los tres llamados de blobs (`commit -> tree -> blob`) porque la API de contenido **cachea** y `?ref=<sha>` puede devolver datos viejos. Obtener el archivo exacto en el commit exacto es el requisito. Detalle fino de ingeniería.
- **Snapshot de estado previo** (`data/.tasks-snapshot.json`, gitignored) para calcular el delta. El patrón mínimo para cualquier trigger reactivo.
- **Webhook directo, sin GitHub Actions intermedio** - *"no intermediate Action runner (saves 5-15 seconds)"* y cero minutos de Actions consumidos. Argumentado explícitamente.
- **`mc-update.sh` como superficie única del agente** (status, comment, subtask, complete, push). Una sola herramienta, verbos claros.
- **EPIC handling:** tareas padre con hijos (`MC-XXX-001`), y el timeout escala `base + (children x perChild)`. Modelo para nuestros spawns con dependencias.
- **HMAC con `timingSafeEqual`** y secreto en archivo aparte, no en el código.

#### ⚠️ Puntos de atención

1. **Es de la generación Clawdbot.** Configura en `~/.clawdbot/`, hooks en `~/.clawdbot/hooks-transforms/`. No está escrito para OpenClaw actual - habría que portar rutas y esquema de config.
2. **Tailscale Funnel expone el gateway a internet.** El webhook tiene token en el query string, pero eso es una superficie de ataque externa sobre el puerto del gateway. Nuestro setup es self-hosted cerrado; esto lo abre.
3. **PAT de GitHub con scope `repo` en `localStorage` del browser.** El token vive en el navegador. Aceptable para single-user, pero es una credencial de escritura expuesta al front.
4. **Nuestro backlog ya vive en `memory.db`.** Adoptar esto implicaría **mover** la fuente de verdad del TODO a un `tasks.json` en un repo de GitHub. Es un cambio de arquitectura de la memoria, no un plugin.
5. **El canal 2 (agente -> dashboard) depende de que el agente commitee y pushee** por cada cambio de estado. Cada movimiento de tarjeta es un commit en el repo de tareas.
6. **No verificado por nosotros.**

#### 🎯 Lo que enseña, aunque no se instale

El hallazgo importante no es el Kanban - es **cómo sincroniza dos actores sin un servidor compartido**. GitHub como hub, webhook para notificar en un sentido y git para sincronizar en el otro. Es un patrón de arquitectura completo, y aplica a cualquier cosa que queramos sincronizar entre el agente y una superficie visual.

> **Veredicto: descartado como instalación, rescatado como arquitectura.** Es de la era Clawdbot, expone el gateway por Tailscale Funnel, pone un PAT de escritura en el browser, y adoptarlo implicaría mudar nuestro backlog de `memory.db` a un `tasks.json` en GitHub - demasiado para lo que aporta. Pero **el patrón `GitHub-as-hub` (datos + eventos + hosting) y el trigger por diff valen oro**, y la idea de fondo -**que el backlog sea un objeto visible y no algo que hay que pedir**- es una deuda real nuestra.

#### 🚀 planning-with-files (OthmanAdi) - el plan que sobrevive al context window

Fuente: [OthmanAdi/planning-with-files](https://github.com/OthmanAdi/planning-with-files). **MIT.** v3.21.0. Instala en 60+ agentes vía el estándar Agent Skills.

**Qué es:** una forma de trabajar, empaquetada como skill + hooks. La idea en una frase: ***context window = RAM (volátil), filesystem = disco (persistente) -> todo lo importante se escribe a disco.*** El modelo Manus, explícito. Tres archivos en disco:

| Archivo | Para qué | Cuándo se actualiza |
|---|---|---|
| `task_plan.md` | Fases, estado, decisiones, errores | Después de cada fase |
| `findings.md` | Research, descubrimientos | Después de **cualquier** hallazgo |
| `progress.md` | Log de sesión, resultados de tests | Durante toda la sesión |

Los hooks del ciclo de vida **re-inyectan el plan al inicio de cada turno**, así que las fases quedan en la ventana de atención y el plan **sobrevive a `/clear`, crash y compactación**.

#### 🎯 Ataca un problema que conocemos de primera mano

Este es **el problema de nuestro HANDOFF.md**, pero resuelto con enforcement en vez de disciplina. Nosotros escribimos el HANDOFF al cerrar sesión - y depende de que yo me acuerde de hacerlo. Ellos **re-inyectan el estado cada turno desde disco**: no es una regla que hay que recordar, es un hook que dispara.

> **La conexión con ADR-083 es directa:** *"una regla sin enforcement se viola sola"*. Nuestro protocolo de sesión es prosa; esto es mecanismo.

#### 🔬 El tier de OpenClaw (importante)

El README trae una tabla de tres tiers. **OpenClaw está en el tier "Standard Agent Skills"**, junto a Continue, Pi, Kilocode, AdaL:

> *"SKILL.md discovery via npx skills add; **the pattern without lifecycle hooks**"*

Es decir: **en OpenClaw tenemos el patrón, NO los hooks.** Sin hooks, la re-inyección por turno y el gate de Stop no existen - queda como una skill que hay que invocar voluntariamente. **Que es exactamente lo que no funciona.** El hook es el mecanismo diferenciador, y ellos lo admiten: *"The hooks are the differentiating mechanism"*.

#### 🔑 Diseño a robar (muchísimo, y todo aplicable)

**Sobre el control del contexto:**
- **La metáfora RAM/disco, aplicada.** No es decorativa: decide qué se escribe y cuándo.
- **La "2-Action Rule":** después de cada 2 operaciones de view/browser/search, **guardar hallazgos a disco** - porque la información multimodal (imágenes, screenshots, PDFs) no persiste si no se pasa a texto. Nos pasa: analizamos un repo leyendo un README y si no lo anotamos ya, se pierde.
- **Matriz read-vs-write:** *¿acabo de escribir el archivo? NO lo leas, ya está en contexto. ¿Vi una imagen? Escribí AHORA.* Micro-decisión hecha tabla. Elegante.
- **El "5-Question Reboot Test":** ¿dónde estoy? ¿a dónde voy? ¿cuál es el goal? ¿qué aprendí? ¿qué hice? ¿qué voy a hacer? **Seis preguntas que definen si tu manejo de contexto es sólido.** Directamente nuestro protocolo de arranque de sesión, mejor formulado.

**Sobre el fallo y la verificación (lo más valioso):**
- **"3-Strike Error Protocol":** intento 1 diagnostica y arregla; intento 2 cambia de enfoque (*"NEVER repeat exact same failing action"*); intento 3 replantea las premisas; después de 3 fallos, **escalar al humano**. Esto es nuestra *"weak/empty result: vary query/path/command/source, then conclude"* pero con contador y criterio de escalada.
- **Tabla de errores con intento y resolución** (`| Error | Attempt | Resolution |`) - el error deja de ser incidente y se vuelve conocimiento.
- **SHA-256 attestation del plan** (`attest-plan.sh`): el cuerpo del plan se firma; si difiere del hash aprobado, los hooks **rechazan la inyección con `[PLAN TAMPERED]`**. Es el *"evidence packs hash-chained"* de guardspine, pero aplicado al plan. **Detecta que un tool result, un colaborador o un bug reescribió el plan en silencio.**
- **`/plan-doctor`:** self-check de los fallos que *fallan en silencio* - resolución del plan, inyección, attestation, superficies de instalación, latencia. **Tercer repo seguido con patrón `doctor`** (PowerContext, Natilius, este). Ya no es coincidencia: es un estándar del ecosistema.
- **Gated mode:** el *Stop gate* retiene el stop **solo mientras quede una fase `in_progress`**, con tope de bloqueos y detección de estancamiento para que un plan incompleto nunca atrape la sesión. Es nuestro *"un run sin contrato termina `unverified`"* de Claw Orchestrator, otra vuelta de tuerca.

**Sobre el trabajo multi-agente:**
- **Ledger por agente:** los workers appenden una línea JSON por evento a `ledger-<agent>.jsonl`; un resumen sintetiza un bloque de forma fija que reemplaza el tail crudo de `progress.md`. **"Ningún texto libre del disco llega al modelo por ese bloque."** Es el mismo principio que el *run ledger* de Claw Orchestrator.
- **Un dueño del plan:** el orquestador es dueño de `task_plan.md`; los workers reportan por sus propios ledgers. **Regla dura, y es la nuestra:** un solo dueño del artefacto compartido.
- **Aislamiento por tarea:** `.planning/YYYY-MM-DD-<slug>/` con `PLAN_ID` para pinnear cada host. Dos tareas concurrentes no se pisan.
- **Guard de escritura paralela:** avisa si los items chequeados o las fases completadas **bajaron** entre turnos. *"Advisory check after the write, not a lock"* - honesto sobre sus límites.

**Sobre el ciclo de vida de los archivos:**
- **Los archivos de plan son memoria de trabajo, no entregable.** Gitignored por defecto, nada los archiva; la próxima tarea sobreescribe. *"Anything worth keeping should be promoted into code, a commit, or a doc."* Es la misma distinción *persistencia != runtime* que rescatamos de HomeAssistant.

#### ⚠️ Puntos de atención

1. **En OpenClaw no tenemos los hooks.** Sin ellos, es una skill voluntaria - y ya sabemos cómo termina eso. Adoptarlo como está nos da el 30% del valor.
2. **Los hooks son de Claude Code.** Para tener el mecanismo completo en OpenClaw habría que **construir el equivalente** (¿un hook del gateway? ¿algo en el bootstrap?). No es copiar y pegar.
3. **Toca historial de sesiones locales** con `session-catchup.py`. `--metadata` solo cuenta agregados; `--replay` emite extractos. Ellos mismos marcan: *"treat every replayed excerpt as untrusted data"*. Coherente con nuestra política, pero es una superficie a auditar.
4. **Solapa con PowerContext** (Memory/Handoff/Experience/Skill) y con nuestro HANDOFF/daily. Los tres resuelven "el contexto que se pierde".
5. **No verificado por nosotros.**

> **Veredicto: el hallazgo más accionable de la segunda tanda, y no por lo que instala sino por lo que *demuestra*.** Es la misma familia que Claw Orchestrator y PowerContext - **el contexto y la verificación como infraestructura, no como disciplina** - y nos da el vocabulario: RAM/disco, 2-Action Rule, 3-Strike Protocol, attestation, gated stop, ledger por agente. **Como instalación en OpenClaw queda cojo** (somos tier "sin hooks"), pero **los patrones son directamente adoptables hoy** y varios ya los teníamos a medias sin el nombre. La pregunta que deja: *¿vale la pena construir el equivalente de esos hooks para nuestro gateway?*

#### 🦀 vibeclaw (jasonkneen) - OpenClaw en el browser, en dos modos

Fuente: [jasonkneen/vibeclaw](https://github.com/jasonkneen/vibeclaw). **AGPL-3.0.** Sitio en [vibeclaw.dev](https://vibeclaw.dev). Node 20+, Vite, deploy en Netlify.

**Qué es:** *"Try OpenClaw in your browser in less than 3 seconds"*. Dos modos:

| Modo | Qué hace |
|---|---|
| **📦 Sandbox** | Levanta un **OpenClaw real dentro del browser**. Un runtime Node embebido ([almostnode](https://github.com/nicholasgriffintn/almostnode)) carga el runtime de OpenClaw con un filesystem virtual (VFS), y chateás con **modelos gratis vía OpenRouter** (proxy serverless; sin API key). |
| **🔴 Live Gateway** | Te conectás a **tu** gateway corriendo y obtenés un dashboard: sesiones, agentes, archivos, skills, cron, métricas, presencia, logs y chat streaming. |

**"Flavours":** personalidades de sandbox intercambiables, cada una con sus agentes, skills, teams y system prompt. Viene con seis (OpenClaw, TinyClaw, ShipIt, R00t, Pixie, Professor). Se agrega una carpeta con `manifest.json` y se reconstruye. **Es el mismo patrón que nuestros roles (CORE/DEV/OPS/MIND/STUDIO), pero empaquetado como preset intercambiable.**

#### 🎯 El modo Sandbox: cero-fricción para *mostrar* OpenClaw

Levantar un agente real en el browser sin instalar nada - sin Docker, sin CLI, sin API keys - es una propuesta fuerte **para demo/onboarding**. Si alguna vez queremos mostrarle a alguien cómo trabaja un agente sin pedirle que instale el gateway, esto resuelve ese caso exacto. **Bajo el filtro de diseño, además, es una pieza visualmente cuidada.**

#### 🔴 El modo Live Gateway: acá está el riesgo

Es un **dashboard de terceros que recibe la URL y el token de tu gateway**. El token viaja al front, y desde ahí al gateway. **Es la misma superficie que marcamos en Crabwalk** - un componente externo con acceso a las credenciales del gateway. A diferencia de Crabwalk, acá **el código no corre en tu máquina: es un sitio hosteado en Netlify** (`vibeclaw.dev`). Conectar el gateway real a un sitio de terceros es una decisión de riesgo, no una comodidad.

**Y no aporta lo que ya tenemos:** el Control UI de OpenClaw **ya es** el dashboard del gateway (sesiones, agentes, archivos, skills, cron, logs). Adoptar este modo sería cambiar un dashboard nativo por uno externo con el token expuesto. **No.**

#### 🔑 Diseño a robar

- **El protocolo del gateway queda documentado en el README:** JSON-RPC por WebSocket, con `connect.challenge` (nonce) -> cliente firma con Ed25519 -> `connect`; métodos `status`, `agents.list`, `sessions.list`, `skills.status`, `cron.list`, `agents.files.get`, `logs.tail`, `usage.cost`, `chat.send`, `chat.history`. **Es una referencia técnica útil** del protocolo que OpenClaw expone - nos sirve para entender qué superficies hay.
- **Auth por challenge firmado con Ed25519** (con `@noble/ed25519`, que funciona incluso en orígenes HTTP). Modelo de autenticación **sin mandar el token en cada request** - la firma del nonce prueba posesión.
- **Cero-fricción como valor de producto:** "en menos de 3 segundos", sin instalar nada. El modelo a copiar si alguna vez hacemos una demo.
- **VFS + runtime Node en el browser** (almostnode + COOP/COEP para `SharedArrayBuffer`) - ingeniería notable, aunque fuera de nuestro alcance actual.

#### ⚠️ Puntos de atención

1. **AGPL-3.0** - copyleft fuerte. Tercer repo de la ronda con AGPL (MoltBrain, ClawSec).
2. **El modo Live Gateway manda tu token al sitio de terceros** (`vibeclaw.dev`). Superficie de riesgo, y **redundante con el Control UI nativo**.
3. **Los créditos apuntan a `nicholasgriffintn/openclaw`** - no a la URL oficial `openclaw/openclaw`. Mismo patrón que vimos en guardspine. No es concluyente, pero es una señal que conviene verificar antes de confiar.
4. **El sandbox corre OpenClaw + OpenRouter a través de un proxy serverless ajeno.** Lo que chateás pasa por su infraestructura. Aceptable para probar con datos falsos; inaceptable con información real.
5. **No verificado por nosotros.**

> **Veredicto: descartado como instalación; rescatado el protocolo y la lección de cero-fricción.** El modo Sandbox es una buena idea de *demo* (mostrar sin instalar) y el modo Live Gateway es un riesgo de seguridad que además duplica el Control UI nativo. Lo que vale es la **documentación del protocolo del gateway** (JSON-RPC + challenge Ed25519) y el principio de que **"probar en 3 segundos" es una feature**, no un adorno.

#### 🔗 context-sync (Intina47) - memoria de proyecto local vía MCP

Fuente: [Intina47/context-sync](https://github.com/Intina47/context-sync). Licencia **no declarada en el README** (verificar). npm: `@context-sync/server`. Se instala global y **auto-configura** los clientes MCP.

**Qué es:** *"Local-first project memory for AI coding tools over MCP"*. Una capa de memoria persistente **por codebase**, servida como **MCP**: identidad del proyecto y stack, trabajo activo, decisiones, constraints y caveats, exploración estructurada de archivos, contexto git-aware, y lookup opcional de Notion.

#### 🔌 La diferencia clave de esta ronda: es MCP

> **Acá se conecta con nuestro hallazgo anterior.** Descartamos dos repos (MCP adapter y MCP server) **porque el core ya expone MCP nativo**. Pues bien: **este servicio se enchufa por esa vía nativa** - `openclaw mcp add`, sin plugin, sin wrapper. Es el **primer candidato de memoria que entra por una puerta que ya tenemos abierta y verificada**.

#### 🎯 Ataca el eje de memoria... desde otro ángulo

No compite con MemOS/MoltBrain/qmd de igual a igual: **aquellos son memoria de *sesión/agente*; este es memoria de *codebase*.** Su scope es el proyecto, no la conversación. Eso lo acerca a otra cosa nuestra: **nuestro `.knowledge/` por proyecto** y el trabajo de discovery. La pregunta de solapamiento no es "¿reemplaza a `memory.db`?" sino **"¿reemplaza/complementa a `.knowledge/`?"**.

#### 🔑 Diseño a robar

- **Superficie MCP chica y por verbos:** `set_project`, `remember`, `recall`, `search`, `structure`, `git`. Ocho tools, nombres de acción. **Lo opuesto a los 78 tools de Claw Orchestrator** - y más fácil de razonar.
- **El protocolo de arranque de sesión es LITERALMENTE el nuestro:**
  ```
  1. set_project({ path: "..." })   -> fijar contexto
  2. recall()                        -> recuperar lo que sabemos
  3. structure({ depth: 2 })         -> orientarse en el código
  4. read_file({ path: "..." })      -> inspección enfocada
  5. remember({ type: "decision", content: "..." })  -> persistir lo que debe sobrevivir
  ```
  Es nuestro **"iniciar sesión"** (daily check -> memory search -> presentación) mecanizado, con el paso 5 explícito: **recordar es una decisión deliberada, no un efecto colateral.**
- **Tipos de memoria con nombre:** `decision`, y por extensión constraints/caveats. Categorizar al escribir mejora el recall.
- **Captura automática por hooks de git** (`post-commit`, `pre-push`, `post-merge`, `post-checkout`): el contexto se captura **en los límites naturales del trabajo**, no cuando alguien se acuerda. **Backupea los hooks existentes antes de tocar** - regla de merge, no overwrite.
- **Git-aware context:** `hotspots` (dónde está el calor del cambio), `coupling` (qué archivos cambian juntos), `blame`, `analysis`. Inteligencia de codebase que nosotros **no tenemos**, y que aplica directo a un repo de 2600+ líneas de changelog como el nuestro.
- **Notion read-only por diseño** en la superficie del tool (*"intentionally read-only"*). Limitar la escritura externa por diseño es una buena práctica de blast radius.

#### ⚠️ Puntos de atención

1. **Auto-configura durante el `-g`.** Un `npm install -g` que **escribe config en tus herramientas de IA** sin preguntar. Es exactamente la clase de comportamiento que nuestra política marca como untrusted. **Leer el preflight, no usar el instalador a ciegas.**
2. **Instala hooks en tus repos git.** `post-commit`, `pre-push`, etc. Aunque backupea, **toca `.git/hooks/` de cada repo donde corras `set_project`**. Con un pre-commit hook propio que ya aborta commits (guion común, rutas rotas), cualquier interacción hay que probarla aislada.
3. **Licencia sin declarar en el README.** Verificar antes de integrar.
4. **Notion = superficie externa.** Opt-in y read-only, pero es una dependencia de red.
5. **Segunda base SQLite paralela** (`~/.context-sync/data.db`) además de nuestra `memory.db`. Dos fuentes de verdad es lo que hay que evitar.
6. **No verificado por nosotros.**

> **Veredicto: candidato real, categoría *memoria de codebase*, y el más "instalable" de todos por venir como MCP.** No reemplaza nuestra memoria de sesión - cubre el eje que hoy ocupan `.knowledge/` y el discovery. **La pregunta que abre:** ¿`context-sync` reemplaza a `.knowledge/`, o se suma como una capa más de retrieval sobre el código? Antes de instalarlo hay que decidir el eje de memoria (DECISIONS.md §2.1), porque **una tercera base SQLite sin esa decisión es deuda, no capacidad.**

#### 🎨 OpenClaw Studio (grp06) - el dashboard que compite con el Control UI

Fuente: [grp06/openclaw-studio](https://github.com/grp06/openclaw-studio). Licencia **no declarada en el README** (verificar). Node 20.9+, Next.js, deploy con `npx openclaw-studio@latest`. Trae Discord propio y documentación de UI.

**Qué es:** un **dashboard web "limpio"** para OpenClaw - *"el"* del pitch. Se conecta al gateway, ve agentes, chatea, gestiona aprobaciones y configura jobs desde un lugar. **Es un reemplazo del Control UI nativo, hecho por un tercero.**

#### 🚨 La diferencia que importa con vibeclaw

vibeclaw live era **un sitio hosteado por un tercero** que recibía tu token. **Este es distinto: corre en tu propia máquina** (`npx`, `localhost:3000`). El token va al gateway local, no a un servidor ajeno. **Eso baja el riesgo de "exfiltración" - pero no lo elimina:** sigue siendo un **segundo front con acceso completo al gateway** (sesiones, agentes, archivos, aprobaciones de exec), y guarda su propio `runtime.db` (otra SQLite) y su token en `~/.openclaw/openclaw-studio/settings.json`.

> **El riesgo cambió de clase:** no es *"¿a quién le mando el token?"* sino *"¿cuánta superficie de escritura delego a una app que no audité?"*. Es un dashboard que **gestiona aprobaciones de exec** - es decir, puede aprobar comandos.

#### 🎯 Bajo el filtro de diseño: lo más relevante de la ronda

Es un producto **cuyo valor declarado es ser "limpio"** - la estética es el pitch. Y lo respalda con documentos:

- **`color-system.md` (doc del repo de Studio):** *"the semantic color contract, status mappings, and guardrails that keep action/status/danger usage consistent across the UI"*. **Un contrato semántico de color con guardrails** - acción vs estado vs peligro con reglas de uso. **Esto es exactamente lo que nos falta:** hablamos de "definir el design system propio", y acá hay un ejemplo concreto de cómo se especifica.
- **`permissions-sandboxing.md` (doc del repo de Studio):** cómo las decisiones de creación de agente (tool policy, sandbox, exec approvals) **fluyen desde el front hacia el gateway, y el gateway las aplica en runtime**. Modelo de cómo una UI **no debe** implementar seguridad - la delega al core.
- **`pi-chat-streaming.md` (doc del repo de Studio):** streaming de eventos por SSE con **replay/history determinista** y render de tool calls, *thinking traces* y transcript. **El mismo eje que Crabwalk** - observabilidad de lo que hace el agente - pero dentro de un dashboard.

#### 🔑 Diseño a robar

- **El contrato semántico de color como documento.** No "una paleta", sino **reglas**: qué color significa acción, cuál estado, cuál peligro, y por qué. **Directamente adoptable para nuestro design system.**
- **Arquitectura de dos saltos clara:** `Browser -> Studio` (HTTP + SSE) y `Studio -> Gateway` (un solo WebSocket del proceso Node). Un solo socket server-owned, no uno por browser. **Contrasta con vibeclaw**, donde el browser hablaba directo con el gateway.
- **Proyección durable + replay outbox en `runtime.db`:** el historial de runtime sobrevive refrescos y reinicios, y el replay es determinista. **Patrón de "la UI no pierde estado",** relevante porque nuestro dashboard también podría.
- **Guard de startup diferenciado:** `dev` corre `verify:native-runtime:repair` (repara), `start` corre `verify:native-runtime:check` (solo chequea, no muta dependencias). **Distinguir "modo desarrollo puede arreglar" de "modo producción no toca nada" es fino y correcto.**
- **`STUDIO_ACCESS_TOKEN` obligatorio solo fuera de loopback**, y **los bind públicos exigen segundo factor** (abrir `/?access_token=` una vez por browser para setear cookie). Postura de seguridad proporcional al blast radius.
- **Tres escenarios de deploy documentados** (local, gateway en cloud, todo en cloud) con el mismo comando. **"Elegí tu setup" en vez de un instructivo único** - buena forma de documentar.

#### ⚠️ Puntos de atención

1. **Es un front de tercero con acceso completo al gateway**, incluidas **aprobaciones de exec**. Auditarlo antes de conectarlo a datos reales.
2. **Licencia sin declarar en el README.** Verificar.
3. **Tercera SQLite paralela** (`runtime.db`) sumada a `memory.db` y a la de context-sync. **Las bases se acumulan sin una decisión de arquitectura.**
4. **Solapa de lleno con el Control UI nativo.** Es, literalmente, una alternativa a algo que ya tenemos. Adoptarlo es cambiar un componente mantenido por el core por uno de tercero, **a cambio de estética**.
5. **El `npx -y @latest`** ejecuta lo último publicado sin pin. Es el patrón que nuestra política marca como untrusted.
6. **No verificado por nosotros.**

> **Veredicto: descartado como instalación; el más valioso de la tanda para el FILTRO DE DISEÑO.** Solapa con el Control UI (que ya tenemos y mantiene el core), así que no hay razón fuerte para adoptarlo - **salvo que su calidad visual sea muy superior, y eso se decide mirando, no leyendo.** Lo que sí se lleva hoy: **el contrato semántico de color** (ejemplo concreto de cómo especificar un design system), la **arquitectura de socket server-owned**, y el **guard de startup dev-vs-prod**. Es el **segundo repo seguido que muestra que "dashboard de tercero" es un patrón vivo en el ecosistema** (vibeclaw, este) - y la pregunta de fondo es si el Control UI nativo se queda corto en diseño.

#### 🏭 Autensa (crshdn/mission-control) - "Autonomous Product Engine"

Fuente: [crshdn/mission-control](https://github.com/crshdn/mission-control). **Tercer repo con el nombre `mission-control`** (ya renombrado **Autensa**, [autensa.com](https://autensa.com)). Next.js 14 + TypeScript + SQLite, corre en el puerto 4000, se conecta al gateway por WebSocket. Node 18+, Docker. Licencia por confirmar.

> **Los tres homónimos, para no confundirlos jamas:** (1) `vincentkoc/mission-control` - dashboard/observabilidad; (2) `rdsthomas/mission-control` - Kanban chat-to-task de la era Clawdbot; (3) **este** - un motor de producto autónomo. Mismo nombre, tres productos distintos.

**Qué es:** el más ambicioso (y el más fuera de perfil) de la ronda. Apuntás a un producto (repo + URL en vivo) y corre un ciclo continuo: **Research -> Ideation -> Swipe -> Build -> Test -> Review -> PR**. Investigación de mercado, generación de ideas con scoring, una interfaz de swipe tipo Tinder para aprobar/rechazar, y el pipeline de agentes que construye y abre el PR. *"Tu único trabajo es el swipe."*

#### ⚪ Como producto: fuera de perfil

- **No hacemos productos que se auto-mejoran 24/7.** No hacemos research de mercado, ni ideation, ni swipe interfaces. Es de otro dominio.
- **Pesado:** Next.js + SQLite + 80+ endpoints + Docker + puerto propio. **Cuarta app con base SQLite paralela** (tras Studio y context-sync).
- **Otro front de tercero con el token del gateway**, y este **dispara trabajo autónomo**. Es la superficie de riesgo más grande de la tanda.
- **`Hetzner VPS` con link de referido en el README** - interés comercial declarado de forma sutil. No invalida nada, pero es un dato.
- "The world's first Autonomous Product Engine" - marketing fuerte. Y **no verificado por nosotros**.

#### 🔑 Diseño a robar (acá está el valor, y es mucho)

**Sobre gates y confianza:**
- **Automation Tiers: Supervised / Semi-Auto / Full Auto.** *"Elegí tu nivel de comodidad por producto"*: Supervised -> el PR se crea y vos mergeás; Semi-Auto -> auto-merge **si el CI pasa y el review agent aprueba**; Full Auto -> todo, idea a feature deployed. **Es la mejor formulación que vi del gradiente humano-en-el-loop.** Nosotros tenemos un gate binario (pausa o no); esto es un **espectro por contexto**.
- **Approval gate: el plan antes que el código.** *"You review the plan before any code is written."* Es nuestra pausa obligatoria (iterar -> revisión -> push) hecha paso del pipeline.
- **La lección es el nivel de autonomía como configuración, no como conducta.**

**Sobre sesiones (hallazgo que nos toca directo):**
- **v2.5.0: una sesión de OpenClaw por tarea.** Bug que encontraron y arreglaron: *"all tasks assigned to the same agent shared one session, causing context to accumulate across tasks until the model's context window was exhausted and the agent stalled"*. **Una sesión compartida entre tareas se degrada hasta atascar al agente.** Es exactamente la razón por la que nuestro modelo de sesión-por-tarea es correcto - y una advertencia concreta sobre lo que pasa si no lo respetamos.
- **Aislamiento de workspace por build:** git worktrees para repos, sandboxes de tarea para lo local, **asignación de puertos (4200-4299)**, **cola de merge serializada** con detección de conflictos, y **locking por producto** (los completados del mismo producto se encolan). **Una tarea, un espacio, sin colisiones** - el problema de la concurrencia resuelto en serio.

**Sobre orquestación y resiliencia:**
- **Convoy Mode: DAG de subtareas con scheduling por dependencias.** Grafo de dependencias visual, **health monitoring que detecta agentes estancados/zombie** y **auto-nudge** que reasigna o reinicia al agente que se quedó oscuro. *"Detects stalled, stuck, or zombie agents automatically."* **Es el problema "el subagente se colgó" resuelto como sistema.**
- **Checkpoint & crash recovery:** el progreso se guarda en checkpoints configurables; si la sesión crashea, *"work resumes from the last checkpoint, not from scratch"*. **Es el archivo `progress.md` de planning-with-files, pero automático por checkpoint.**
- **Repo Setup / preflight que verifica antes de construir:** acceso git autenticado, rama default, API de GitHub, estado de Actions, permisos del workflow token, secrets y variables. *"Verifies a repository is ready before agents create PR-bound work."* **Es nuestro `doctor` aplicado a un repo entero.**
- **PR checks recovery:** clasifica los checks fallidos en **retryable / repo setup / external provider** y ofrece la acción correcta. **Triaje del fallo de CI, no reintentar a ciegas.**

**Sobre costos y aprendizaje:**
- **Cost tracking con caps que auto-pausan el dispatch.** Costo por tarea, por producto, agregado diario/mensual, y **límites que frenan el despacho al excederse**. Es el *run ledger + spend caps* de Claw Orchestrator.
- **Agent Skill Creation Loop (v2.4.0):** *"agents learn reusable procedures from completed tasks; Bayesian confidence scoring promotes proven skills; matched skills injected at dispatch as primary instructions"*. **Es `skill_workshop` con un modelo de confianza.** El mismo eje: qué skill probó servir y cómo se promueve.
- **Product Program (patrón Karpathy AutoResearch):** un documento vivo que le dice a los agentes de research **qué mirar y qué ignorar**, y que **evoluciona con los datos**. Es nuestro `AGENTS.md` pero como instrucción evolutiva.
- **Operator Chat con dos modos:** *queued notes* (se entregan en el próximo checkpoint) y *direct messages* (inmediatos, corrección en tiempo real). **Distinguir "para después" de "ahora" en la intervención humana.**

#### ⚠️ Puntos de atención

1. **Superficie de riesgo máxima:** un front de tercero con el token del gateway que **despacha trabajo autónomo**. Es el opuesto a nuestro perfil self-hosted cerrado.
2. **Complejidad de despliegue alta** (Next.js, SQLite, Docker, puerto, 80+ endpoints).
3. **Link de referido** en el README (interés comercial).
4. **Cuarta SQLite paralela** sumada al ecosistema. Sin decisión de arquitectura, es acumulación.
5. **Licencia sin confirmar** en lo que leí.
6. **No verificado por nosotros.**

> **Veredicto: descartado como instalación (fuera de perfil y pesado); el más rico en DISEÑO de orquestación despues de Claw Orchestrator.** Como producto no aplica - no construimos features por swipe. Pero el motor tiene **cuatro patrones que deberiamos adoptar**: los **automation tiers** (autonomía como espectro configurable), el **checkpoint recovery**, el **health monitoring con auto-nudge**, y los **spend caps que auto-pausan**. Y sobre todo deja un hallazgo que nos toca de cerca: **una sesión compartida entre tareas se degrada hasta atascar al agente** - la confirmación externa de que nuestra sesión-por-tarea es la decisión correcta.

#### 🦞 ClawDeck (clawdeckio) - Kanban con cola de trabajo por API

Fuente: [clawdeckio/clawdeck](https://github.com/clawdeckio/clawdeck). **MIT.** Ruby 3.3.1 / **Rails 8.1**, PostgreSQL, Hotwire + Tailwind. Self-host (puerto 3000).

> **⚠️ Proyecto discontinuado en su parte hosteada.** *"The hosted version at clawdeck.io is shutting down May 30, 2026. This repo stays up - self-hosted installs keep working."* Evoluciono a **lst.so**, un producto distinto. **Se lee como diseño/patrón, no como algo a adoptar: no habria a quién seguir.**

**Qué es:** Kanban para agentes. Creás tareas y las organizás en boards; **cuando están listas se las asignás a un agente**; el agente **hace polling de las tareas asignadas**, las trabaja, y **reporta progreso por la API** (activity feed). Todo en tiempo real.

#### 🔀 El contraste que vale con el otro Kanban (rdsthomas)

Tuvimos **dos Kanban** en esta ronda, y resuelven la sincronización **al revés**:

| | rdsthomas/mission-control | ClawDeck |
|---|---|---|
| Transporte | **GitHub** (datos + webhook + Pages) | **REST propio + polling** |
| Dirección | **Push**: el webhook despierta al agente | **Pull**: el agente pregunta por su cola |
| Backend | Archivo `tasks.json` + GitHub | Rails + PostgreSQL |
| Estado hoy | Era Clawdbot | **Hosteado en cierre** (evoluciono a lst.so) |

Ninguno de los dos es adoptable, pero **juntos definen el espacio de diseño**: *¿el trabajo empuja al agente o el agente sale a buscar trabajo?* Nosotros hoy hacemos push (yo recibo la tarea en la conversación). **El modelo pull tiene una ventaja que no tenemos: el agente puede tomar trabajo sin que nadie le escriba.**

#### 🔑 Diseño a robar

- **Cola de trabajo por filtro:** `GET /api/v1/tasks?assigned=true` es *"your work queue"*. **La asignación no es un evento, es una consulta.** El agente decide cuándo y qué tomar.
- **Identidad de agente en headers:** `X-Agent-Name` y `X-Agent-Emoji`. Simple, y define **quién** actúa sin acoplarlo al token. **Directamente aplicable a nuestras APIs internas** si alguna vez exponemos una.
- **`activity_note` en el update de estado:** no solo cambia el status, **deja el porqué en el mismo request**: `{ "status": "in_progress", "activity_note": "Starting work on this" }`. Es el contrato `snap()` de MemoV, reducido a un campo.
- **Estados canónicos y chicos:** `inbox -> up_next -> in_progress -> in_review -> done`. Cinco, con el **`in_review` explícito** - el mismo valor que le damos a la pausa de revisión.
- **REST sobre WebSocket:** acá el agente habla por HTTP, no por el protocolo del gateway. **Contraste útil con context-sync**: dos formas de darle herramientas a un agente (MCP vs API propia).

#### ⚠️ Puntos de atención

1. **Hosteado en cierre, evoluciono a lst.so** → el repo queda como referencia histórica. **No adoptar.**
2. **Stack pesado para nosotros:** Rails + PostgreSQL + Solid Queue/Cache/Cable. **Otra base de datos más** (quinta de la ronda) y un runtime Ruby que no usamos.
3. **El agente hace polling** - a diferencia de un webhook, el trabajo se descubre por consulta periódica. **Latencia y gasto de sondeo** son el costo del modelo pull.
4. **Auth por GitHub OAuth o email/password** - pensado para multi-usuario; nosotros somos single-user.
5. **No verificado por nosotros.** Y no instalamos nada.

> **Veredicto: descartado (proyecto en cierre, stack ajeno y pesado); vale como pieza de diseño.** El aporte es el **modelo pull** (cola por consulta), la **identidad por headers**, y el **`activity_note` en el mismo update**. El contraste con el Kanban de rdsthomas (push por webhook vs pull por API) **mapea el espacio entero** de cómo una superficie visual y un agente se sincronizan, y es la parte que nos queda.

#### ☁️ OpenClaw Supermemory (supermemoryai) - memoria en la nube de un tercero

Fuente: [supermemoryai/openclaw-supermemory](https://github.com/supermemoryai/openclaw-supermemory). Plugin oficial de Supermemory. **Requiere plan Pro o superior** - es un producto comercial con capa gratuita.

> **🔴 DESCARTE POR REGLA, no por calidad.** *"all powered by Supermemory cloud. Everything runs in the cloud."* Cada turno de conversación **se manda a la nube de un tercero**, y las memorias recuperadas se inyectan con `allowPromptInjection: true` y `allowConversationAccess: true`. **Es el mismo caso que ya descartamos con MemOS Cloud Plugin** - y contra nuestra política es de los más claros: memoria privada completa (conversaciones, perfil del usuario) a infraestructura ajena.

**Qué hace:** memoria de largo plazo automática. **Auto-Recall** antes de cada turno (busca memorias relevantes y las inyecta), **Auto-Capture** después de cada turno (manda la conversación a extraer y guardar), y **perfil persistente del usuario**. Todo extracción, deduplicación y armado de perfil lo hace la nube.

**Lo único que salva al repo: `baseUrl` configurable.** El código permite apuntar a una instancia self-hosted (`baseUrl: http://localhost:8000`). **Pero el producto es la nube**, y eso no cambia lo que vende.

#### 🔑 Diseño a robar (hay algo, y es bueno)

- **Auto-Recall / Auto-Capture como hooks de turno.** Otra vez el mismo patrón: **recuperar antes, capturar después, automático**. Es la memoria como ciclo de vida del turno, no como acción manual. **Tercer repo de la ronda con este mecanismo** (planning-with-files re-inyecta, MemOS, este). Ya es un patrón del ecosistema, no una idea suelta.
- **`profileFrequency`:** inyectar el **perfil completo cada N turnos**, no la búsqueda semántica de cada turno. **Dos frecuencias distintas para dos necesidades distintas** - hechos estables vs contexto puntual. Fino.
- **Contenedores con instrucción de ruteo:** los tags (`work`, `personal`) vienen con **descripción**, y hay un `customContainerInstructions` que le dice **al modelo** qué va en cada contenedor. **Es `agentOverrides` de MemOS / los multi-cube, con el ruteo como instrucción de prompt.**
- **`captureMode: "all"` filtra textos cortos** por defecto. **No capturar el ruido** es una decisión de diseño explícita, no un detalle.
- **`supermemory-forget` como tool de primera clase.** Poder **borrar por query o ID** desde el agente, al lado de guardar y buscar. **Nuestro sistema de memoria no tiene olvido explícito.**
- **Nombres viejos deprecados con resolución:** documentan que `supermemory_store` sigue funcionando y resuelve al tool nuevo, y avisan que en 3.0 se van. **Migración con gracia** - buena práctica de versionado.
- **`/supermemory-index` como skill:** explora el codebase y guarda memorias enfocadas, **distinto de `/remember`**. Indexación de proyecto con criterio, no volcado.

#### ⚠️ Puntos de atención

1. **🔴 Cloud por diseño** - viola la Red Line de no mandar datos privados afuera. **Descartado.**
2. **`allowPromptInjection: true` + `allowConversationAccess: true`** en la config de ejemplo: el plugin **puede inyectar prompts** y **leer la conversación**. Es el permiso más alto que se le puede dar a un plugin, y se activa para que la memoria funcione. **Superficie máxima.**
3. **Plan pago (Pro+)** - es un producto comercial, no un proyecto comunitario.
4. **Solapa con toda la familia de memoria** (MemOS, MoltBrain, qmd, context-sync) y con nuestra `memory.db`.
5. **Tiene `baseUrl` self-hosted** - si algún día se quisiera el mecanismo, existe el camino local, pero **habría que auditar que no llame a casa**.
6. **No verificado por nosotros.**

> **Veredicto: DESCARTADO, y por la regla más clara de todas (datos privados a la nube de un tercero).** No es que sea malo: **hace bien cosas que nos faltan** - el ciclo auto-recall/auto-capture, las dos frecuencias (contexto vs perfil), el `forget` explícito, y el ruteo por contenedor como instrucción. **Es el quinto repo seguido que muestra que la memoria por hooks de turno es un patrón del ecosistema.** Todo eso se roba; **la implementación cloud se descarta.**

#### 🧠 Open Amnesia (vincentkoc) - local-first, de trazas crudas a contexto confiable

Fuente: [vincentkoc/openamnesia](https://github.com/vincentkoc/openamnesia). **Tercer repo de `vincentkoc`** en la ronda (mission-control, natilius, este). Python + TypeScript, FastAPI + SQLite, React + Vite + Tailwind. `pip install -e .`

**Qué es:** *"Local-first memory for agents. From raw traces to reliable context."* Un **motor de contexto con aprendizaje continuo** que convierte logs de sesión desordenados en **momentos, hechos y skills estructurados**.

> **La tesis, en una frase del propio repo:** ***"Data consistency beats prompt cleverness."*** La calidad de la memoria del agente depende del **preprocesamiento determinista** - normalización, filtrado, deduplicación - **antes de cualquier paso de LLM**. Una vez que la *forma* de los datos es confiable, extraer y resumir sale mucho mejor y más barato.

#### 🎯 Por qué es candidato fuerte para nosotros

**Exporta archivos de memoria por fecha: `YYYY_MM_DD.md`.** Es **literalmente** nuestro `memory/YYYY-MM-DD.md`. No hay que adaptar el formato: ya habla el idioma de nuestras daily notes.

Y ataca un problema que tenemos de verdad: **el contenido de nuestras sesiones vive en transcripts que nadie procesa**. Este repo lo ingestaría y lo convertiría en hechos y skills con estructura.

#### 🏗️ El pipeline (8 pasos, y el orden es la lección)

```
1. Connectors     -> ingesta logs de Codex, Claude, iMessage
2. Filtros+redaccion -> limpia y acota (ventanas de tiempo, tags de proyecto, patrones secret/PII)
3. Normalization  -> Event IR estable (turno a turno con tool call/result)
4. Sessionization -> agrupa eventos en "momentos" y threads
5. Enrichment     -> resumenes + extraccion LLM (SOLO despues de 3 y 4)
6. Storage        -> SQLite como system-of-record
7. Serving        -> API FastAPI read-only
8. UI             -> React: inspeccion, filtro, control de export
```

**El paso 5 despues del 4 es el diseño entero.** *"LLM noise + token budgets: enrichment is expensive and can amplify messy clusters if run too early."* Si le tirás logs crudos al LLM, el ruido se amplifica. **Primero se ordena determinísticamente, después se enriquece.** Es lo opuesto a "tírale todo al modelo y que se arregle".

#### 🔑 Diseño a robar (mucho, y todo aplicable)

- **El principio `determinism-before-LLM`.** Es una regla de arquitectura de memoria, no un detalle de implementación.
- **La segmentación en *momentos*, con forma fija:** `intent -> actions/tool calls -> outcomes -> artifacts`. **Cuatro campos que capturan la unidad real de trabajo.** Es el contrato `snap()` de MemoV, más rico.
- **Redacción ANTES del enrichment.** Los patrones de secret/PII se filtran **en el paso 2** - antes de que nada toque un LLM. **Es nuestra Red Line aplicada como paso de pipeline, no como promesa.**
- **Deduplicación explícita** de *"repeated banners, retries, and tool spam creating low-quality memories"*. **No capturar ruido** - mismo principio que el `captureMode: "all"` de Supermemory.
- **Filtros universales por dimensión:** `content` / `group` / `actor` / `time window`. Cuatro ejes de acotamiento aplicables a cualquier fuente. **`actor` es interesante:** permite separar por quién actuó, útil en multi-agente.
- **Tool call/result con evidencia preservada:** *"preserves evidence and artifacts (diffs, commands, links)"*. La memoria **no solo dice qué pasó, guarda la prueba**.
- **Storage SQLite + serving read-only separados.** Escribe el pipeline, lee la API, y **la API no puede mutar**. Separación de planos de lectura y escritura hecha arquitectura.
- **Exports multi-granularidad:** diario, semanal, mensual, **y `per_project`**. Cuatro cortes del mismo material.
- **Extracción de **skills** como candidatos con forma:** *"triggers, steps, checks"*. Y el roadmap agrega **métricas** y versionado ("Skill Gym"). **Es `skill_workshop` alimentado desde los logs reales.**
- **Roadmap de continual learning:** *"friction signals -> skill patches -> eval -> promote"*. **El ciclo completo que a nosotros nos falta:** detectar fricción, parchear la skill, evaluarla, promoverla.

#### ⚠️ Puntos de atención

1. **Es un proyecto de hackathon/v0** (el README tiene toda la estructura típica: *Inspiration, How we built it, Challenges, Accomplishments, What we learned, What's next*). **Madurez baja, no verificado.**
2. **Ingesta iMessage** - toca datos personales. El proyecto es local-first con redacción, pero es una superficie sensible que hay que auditar antes.
3. **Dependencias de terceros en el enrichment:** LiteLLM, **You.com**, **Composio**. Si el enrichment llama afuera, hay que decidir si sale el contenido o no.
4. **Tiene deploy a Render y Akash** - o sea, contempla correr la memoria fuera de la máquina. **Opt-in, pero existe.**
5. **Otra SQLite** (`data/amnesia.db`). Sexta de la ronda. **El patrón ya es evidente: cada herramienta trae su base.**
6. **En la config aparece `mode: openclawd`** como modo de export - está pensado para consumir desde OpenClaw. **Señal buena, pero es solo un flag de config: no verifica integración real.**
7. **Mismo autor que natilius** (que quedó descartado por GPL y por no haber Mac virgen). Acá no vi la licencia - verificar.

> **Veredicto: candidato real, y el cierre perfecto de la tanda - porque ataca el eje que menos exploramos.** No es "memoria de sesión" (MemOS) ni "memoria de codebase" (context-sync): es **memoria derivada de las trazas crudas de la propia actividad**, con preprocesamiento determinista antes de LLM. **Su tesis - `data consistency beats prompt cleverness` - es la más transferible de toda la ronda**, y aplica a cualquier cosa que hagamos con memoria. Exporta `YYYY_MM_DD.md` (nuestro formato exacto), filtra secretos **antes** del LLM, y su roadmap es el ciclo de continual learning que nos falta. **Madurez baja; el valor hoy es el diseño, no la instalación.**

---

## 🏁 Cierre de la segunda tanda (9 repos)

**Balance:** la segunda tanda no trajo candidatos de instalación tan fuertes como la primera, pero **bajó a tierra el eje de la memoria** y **produjo el mejor material de diseño**.

**Por categoría:**
- **Memoria:** context-sync (MCP, codebase), Open Amnesia (trazas crudas, local-first), Supermemory (descartado: cloud).
- **Observabilidad/dashboard:** OpenClaw Studio, vibeclaw, ClawDeck, Autensa, Mission Control (rdsthomas) - **cinco productos que compiten con el Control UI nativo**, todos descartados como instalación por solapar con el core o por riesgo de credenciales.
- **Planificación/contexto:** planning-with-files (el más accionable).

**Los patrones que se repitieron (y por eso son del ecosistema, no anécdotas):**
1. **Memoria por hooks de turno** (recuperar antes, capturar después): planning-with-files, MemOS, Supermemory, Open Amnesia. **Cuatro repos.**
2. **Patrón `doctor`** (self-check de fallos silenciosos): PowerContext, Natilius, planning-with-files, Autensa. **Cuatro repos.**
3. **Ledger/checkpoint de agente:** Claw Orchestrator, planning-with-files, Autensa. **Tres repos.**
4. **Preprocesamiento determinista antes de LLM:** Open Amnesia (explícito), todos los demás por implicación.
5. **`determinism-before-LLM` como regla:** el aporte más transferible de la tanda.
6. **Cada herramienta trae su SQLite:** Studio, context-sync, Autensa, ClawDeck, Open Amnesia. **Cinco bases paralelas** contadas en dos tandas. **Esto es una señal de que el ecosistema no tiene una respuesta canónica para la memoria del agente - cada uno inventa la suya.**

**El hallazgo transversal de la tanda:**
> **El ecosistema está convergiendo en "memoria del agente" sin converger en formato.** Todos hacen casi lo mismo (capturar, segmentar, extraer, recuperar) con piezas distintas y bases distintas. **Eso significa que el que defina un formato interoperable gana** - y que nosotros, si adoptamos, deberíamos adoptar el **formato** antes que la herramienta.

**Los dos hallazgos que nos tocan directo:**
- **Autensa v2.5.0:** una sesión compartida entre tareas **se degrada hasta atascar al agente**. Confirma nuestra sesión-por-tarea.
- **rdsthomas/clawdeck:** nuestro backlog vive en `memory.db` y **no es visible**. Es una deuda real.

## 🔬 Profundización - los que quedaron en directorio

De la primera parte quedaron cinco colecciones anotadas **solo como ítem**, sin abrir el contenido. Acá se abren de a una. Orden: el que más prometía primero.

### 1. `design-audit` (jdrhyne) - el rol de auditor de diseño

Fuente: [jdrhyne/agent-skills/skills/design-audit](https://github.com/jdrhyne/agent-skills/tree/main/skills/design-audit). **No es código: es un rol en prosa** (`SKILL.md` + `references/design-rules.md`). Escaneado por AgentVerus.

**Qué es:** un auditor premium de UI/UX con filosofía Jobs/Ive. No toca funcionalidad: **solo diseño**. Entrega un **plan por fases para aprobar antes de implementar**.

#### 🧠 La creencia central (una sola frase)
> *"If a user needs to think about how to use it, you've failed. If an element can be removed without losing meaning, it must be removed. **Simplicity is not a style - it is the architecture.**"*

Y el test: ***"Remove until it breaks. Then add back the last thing."***

#### 🔑 El protocolo (4 pasos, y el paso 4 es el que importa)

1. **Startup - leer ANTES de opinar:** design system/tokens, guidelines de frontend, rutas, PRD, constraints de stack, estado del build, **y lecciones/correcciones previas**. Después, **recorrer la app viva** en mobile -> tablet -> desktop. *"Screenshots are fallback only."*
2. **Auditoría por 15 dimensiones.** No es "se ve lindo": jerarquía visual, espaciado y ritmo, tipografía, color, alineación/grid, componentes, iconografía, motion, **empty states, loading states, error states, dark mode**, densidad, responsividad, accesibilidad. **Los estados vacíos/carga/error son de primera clase** - ahí muere la mayoría de las apps.
3. **Jobs Filter** - cinco preguntas por elemento: ¿habría que explicarle que existe? -> rediseñar. ¿Se puede quitar sin perder sentido? -> quitar. ¿Se siente inevitable? ¿El detalle está tan cuidado como los que nadie ve? (*"the back of the fence must be painted too"*) ¿Decís no a 1000 cosas para quedarte con las grandes?
4. **Compilar el plan y ESPERAR APROBACIÓN.** Fases: **Crítica** (jerarquía/usabilidad/responsividad) -> **Refinamiento** (espaciado/tipo/color) -> **Polish** (micro-interacciones, estados, dark mode). *"Do not implement. Present the plan."* Y el formato de instrucción es quirúrgico: *"Make softer" is not an instruction. "border-radius: 8px -> 12px" is.*

#### 🔑 Las 8 reglas de diseño (el núcleo reutilizable)

| # | Regla | La frase que la destila |
|---|---|---|
| 1 | **La simplicidad ES la arquitectura** | *"Complexity is a design failure, not a feature."* |
| 2 | **La consistencia no se negocia** | Encontrás una inconsistencia -> la marcás, **no inventás una tercera variación**. Todo valor referencia tokens - **nada hardcodeado**. |
| 3 | **La jerarquía manda** | **Una** acción primaria por pantalla, inconfundible. *"If everything is bold, nothing is bold."* |
| 4 | **La alineación es precisión** | *"If something is off by 1-2 pixels, it's wrong."* |
| 5 | **El whitespace es una feature** | *"Space is not empty - it is structure."* |
| 6 | **Diseñá la sensación** | *"Transitions should feel like physics, not decoration."* |
| 7 | **Responsive es el diseño real** | Mobile es el punto de partida; *"design for thumbs first, then cursors"*. |
| 8 | **Nada cosmético sin pensamiento estructural** | Prohibido decir "ponelo azul" o "agregá padding" **sin explicar qué logra en la jerarquía**. *"Every change must have a design reason, not just a preference."* |

#### 🎯 Por qué encaja con nosotros

- **Es un ROL, y encaja con nuestra estructura.** Se instala igual que un agente del crew (identidad + skill), y es **el enforcement del filtro prioritario de Gonzo** (diseño = prioritario). Hoy no tenemos ningún rol que audite diseño.
- **La pausa iterar -> revisión -> aprobación está adentro del propio protocolo.** El paso 4 es literalmente nuestra pausa obligatoria, aplicada a diseño. Y "ejecutá solo lo aprobado, presentá el resultado antes de la siguiente fase" es nuestro flujo.
- **La regla 8 es la más valiosa para nosotros.** Prohibir el cambio cosmético sin razón estructural es exactamente lo que hace que un agente no arruine una UI "porque queda más lindo". Y la regla 2 (flag, no tercera variación) evita que el agente invente su propio estilo.
- **El paso 1 ordena lo que hoy es intuición:** leer los tokens y las **correcciones previas** *antes* de opinar sobre diseño.

#### ⚠️ Puntos de atención

1. **La precondición es que exista un design system.** La regla 2 - *"all values must reference design system tokens, no hardcoded colors, spacing, or sizes"* - **no se puede cumplir sin tokens que referenciar.** Nosotros **no tenemos un design system propio**. **Sin tokens, esta skill es un buen auditor sin estándar contra el cual auditar.**
2. **Es prosa, no mecánica.** No hay verificación automática; la calidad depende del modelo. **Es una skill volitiva, no un gate.**
3. **Asume acceso a la app viva** (browser, viewports). Nosotros tenemos la tool `browser` y la skill `running-app-visual-review` - **la infraestructura existe. Hay que conectarlas.**
4. **Solapa en parte con `ui-contrast-audit`** (accesibilidad) y `running-app-visual-review` (ver visualmente). **No los reemplaza: los orquesta.** `ui-contrast-audit` es un check puntual; esto es la auditoría entera con plan por fases.
5. **No verificado por nosotros** (no lo corremos todavía).

> **Veredicto: adoptable como rol del crew, con una precondición - el design system.** Es exactamente el rol que nos falta (auditor de diseño), trae un protocolo que ya respeta nuestra pausa obligatoria, y sus 8 reglas destilan el criterio que hoy no tenemos escrito. Pero **su regla central (todo referencia tokens) exige el design system que todavía no existe.** Orden correcto: **primero definir los tokens** (color, tipografía, espaciado) - y ahí el **contrato semántico de color de OpenClaw Studio** (§2da tanda) es la mejor referencia que encontramos - **y recién entonces** el rol tiene contra qué auditar. Sin ese paso, adoptarlo da una skill que sabe mirar pero no tiene vara.

### 2. `knowledge-graph` (jdrhyne) - memoria sin base de datos nueva

Fuente: [jdrhyne/agent-skills/clawdbot/knowledge-graph](https://github.com/jdrhyne/agent-skills/tree/main/clawdbot/knowledge-graph). **MIT.** v1.1.0. Prosa + crons + archivos. Inspirado en un [artículo de @spacepixel](https://x.com/spacepixel) sobre sistemas de memoria para agentes.

**Qué es:** un grafo de entidades **append-only** que acumula hechos durables entre sesiones, con **resúmenes vivos** que se reescriben solos. Tres capas, y **reconoce explícitamente las dos que ya tenemos:**

| Capa | Qué | Dónde |
|---|---|---|
| **Entity Knowledge** | Hechos estructurados sobre personas, empresas, proyectos | `life/areas/` |
| **Daily Notes** | Log cronológico de sesiones | `memory/YYYY-MM-DD.md` |
| **Persistent Memory** | Patrones y preferencias de alto nivel | `MEMORY.md` |

> **Esto es lo primero que hay que notar: las capas 2 y 3 son NUESTRAS, con nuestros nombres exactos.** No propone reemplazar nada - **agrega la capa 1**, que es la que nos falta, y declara que convive con las demás.

#### 🧱 El modelo de datos (y por qué es el hallazgo)

```
life/areas/
  people/<slug>/     -> summary.md + facts.jsonl
  companies/<slug>/  -> summary.md + facts.jsonl
  projects/<slug>/   -> summary.md + facts.jsonl
```

Cada entidad son **dos archivos** de texto plano:
- **`summary.md`** - el snapshot corto y actual (3-8 líneas). **El camino rápido.**
- **`facts.jsonl`** - hechos atómicos, **append-only**, un JSON por línea.

```json
{"id":"alice-001","fact":"Frontend engineer at Acme Corp","category":"context","ts":"2026-01-15","source":"conversation","status":"active"}
{"id":"alice-002","fact":"Promoted to senior engineer","category":"milestone","ts":"2026-06-01","source":"conversation","status":"active","supersedes":"alice-001"}
```

Categorías: `relationship | milestone | status | preference | context | decision`.

#### 🔑 Diseño a robar (varios, y todos baratos)

- **Sin base de datos nueva. Sin embeddings. Sin servicio.** Es **markdown + JSONL en el workspace**. **Esto es lo que rompe la ecuación:** las seis opciones de memoria de la ronda traían cada una su SQLite; esta trae **dos archivos de texto**.
- **"Supersede, don't delete" - el patrón más fuerte.** Cuando un hecho cambia, **no se borra ni se edita el anterior**: se agrega uno nuevo con `supersedes: <id-viejo>` y el viejo pasa a `status: superseded`. **La historia queda completa y auditable.** Es lo opuesto a la memoria como overwrite.
- **La distinción `summary.md` vs `facts.jsonl` es el diseño entero.** El agente lee **primero el resumen** (5 líneas) y **solo abre los hechos crudos si el resumen está viejo o el usuario pide detalle**. *"5 lines vs potentially hundreds of raw facts."* **Es el recall con filtro de segunda pasada, pero hecho archivo.**
- **Recall disparado, no automático.** *"Recall should be triggered, not automatic."* Solo ante **nombre propio**, frase de "recordá/pensá", o **keyword de proyecto**. *"Most messages skip recall entirely, saving tokens."* **La política de tokens más explícita que vimos.**
- **Extracción cada 4h con el modelo más barato.** *"typically costs less than $0.01/day."* El costo declarado y minimizado. Y **el cron de síntesis semanal (domingos 9am)** reescribe los resúmenes y **marca contradicciones como superseded**.
- **La separación extracción vs síntesis.** Extraer es incremental y frecuente (cada 4h); sintetizar es periódico y caro (semanal). **Dos ciclos con dos costos distintos.**
- **Instrucciones al `AGENTS.md`:** dice explícitamente *"copiá la sección a tu AGENTS.md para que **todos** los agentes sepan usar el grafo"*. Y **symlink del `life/` entre workspaces** para que varios agentes compartan el mismo grafo. **Pensado para multi-agente - como nosotros.**
- **Límites de seguridad explícitos:** no guardar secretos ni credenciales; no crear entidades por charla casual; **no inyectar el grafo en cada conversación**; no borrar hechos históricos.
- **Qué NO guardar, enumerado:** ✅ cambios de rol, hitos, preferencias, decisiones, contexto estable. ❌ charla casual, estados temporales, hechos ya conocidos, info vaga.

#### 🎯 Por qué ataca la decisión pendiente

La pregunta de `DECISIONS.md` §2.1 era: *¿qué motor de memoria adoptamos, de los seis?* Y el criterio sugerido era *"menor dependencia que resuelva el retrieval"*.

> **Esta opción es la de menor dependencia posible que no sea "construilo de cero": cero infraestructura, dos formatos de texto que ya entendemos, y **reconoce las capas que ya tenemos** en vez de proponer reemplazarlas. No compite con `memory.db` - le agrega **la dimensión de entidad** que hoy no tiene.**

**El eje que abre:** las seis opciones anteriores resolvían **recall semántico** (encontrar por similitud). Esta resuelve **conocimiento de entidades** (*"¿qué sabemos de X?"*). **Son problemas distintos, y puede que la respuesta sea "no elegir uno, sino agregar esta capa".**

#### ⚠️ Puntos de atención

1. **Necesita dos crons** (extracción 4h + síntesis semanal). Nosotros ya usamos `automations`; agregar dos es barato - pero **son dos procesos más que pueden fallar en silencio**.
2. **La extracción de hechos depende del criterio del modelo.** El "¿qué es durable?" lo decide un LLM barato cada 4h. **Un mal extractor llena el grafo de ruido**, y ahí el `summary.md` deja de ser confiable.
3. **Crece sin podar.** Append-only, nunca se borra. Con el tiempo, `facts.jsonl` puede volverse grande - mitigado por "leer resumen primero", pero **el archivo sigue creciendo**.
4. **`life/areas/` es una ruta nueva en el workspace.** Hay que decidir si es la casa correcta o si esto va bajo `memory/` (donde ya vivimos).
5. **Requiere copiar una sección al `AGENTS.md`.** Nuestro `AGENTS.md` **está al límite de bootstrap** (20K) - ya migramos cosas a `docs/SETUP.md` por eso. **Meter esto requiere sacar algo.**
6. **No verificado por nosotros.**

> **Veredicto: el candidato de memoria más limpio de las dos tandas, y el que cambia la decisión.** No trae base de datos, no trae embeddings, no trae servicio: **trae dos formatos de texto plano y una política de tokens explícita**. Reconoce nuestras capas (`memory/YYYY-MM-DD.md`, `MEMORY.md`) y **agrega la que falta: la de entidades**. "Supersede, don't delete" es el mejor patrón de memoria durable que vimos. **Y redefine la pregunta de §2.1: quizá no haya que elegir entre los seis motores, sino agregar esta capa liviana encima de lo que ya tenemos.** Es la opción que menos riesgo introduce y la que más rápido se puede probar en `mktemp -d` sin tocar nada real.

### 3. La suite `aeon` (Bankr) - el ciclo de vida de una skill

Fuente: [BankrBot/skills](https://github.com/BankrBot/skills). **Recordatorio: el repo es ~90% cripto y todo eso queda afuera por regla.** Lo que se profundiza acá son las cuatro skills **stack-agnósticas** de meta-mantenimiento: `skill-security-scan`, `skill-evals`, `skill-repair`, `autoresearch`.

> **La idea que las une: una skill instalada no es un artefacto terminado, es algo que se audita, se mide, se repara y evoluciona.** Nosotros tenemos `skill_workshop` (que crea y actualiza) pero **no tenemos el ciclo de vida posterior**. Esto es ese ciclo, con nombre y apellido en cada etapa.

#### Las cuatro etapas

| Skill | Etapa | Qué hace |
|---|---|---|
| **skill-security-scan** | **Antes** | Audita SKILL.md y scripts por amenazas antes de correrlas. |
| **skill-evals** | **Durante** | Valida el output contra un manifiesto de assertions. |
| **skill-repair** | **Cuando falla** | Diagnostica y repara, con receta de verificación. |
| **autoresearch** | **Cuando quedó vieja** | Genera variaciones, las puntúa, aplica la ganadora. |

#### 🛡️ 1. `skill-security-scan` - la auditoría previa

Escanea `<skills-dir>/*/SKILL.md`, los scripts compañeros (`*.sh`, `*.py`) y los `references/`.

**Amenazas que caza** (y que nosotros deberíamos cazar, porque instalamos skills de afuera):
- **Shell injection:** expansión de variable sin comillas, `eval`, backticks, `$(...)` con datos del usuario.
- **Exfiltración de secretos:** env vars o contenido de archivos pipeados a HTTP saliente.
- **Path traversal:** cadenas `../..`, rutas absolutas que salen del directorio de la skill.
- **Prompt override:** *"ignore previous instructions"*, cambios de persona, **instrucciones dentro de contenido fetcheado**.
- **Comandos destructivos:** deletes recursivos con raíz en `/` o `~`.
- **Ofuscación:** caracteres Unicode invisibles (U+200B, U+FEFF), **bidi override (U+202E, "Trojan Source")**, pipes de base64-a-shell, hosts SSRF conocidos (ngrok, interact.sh, webhook.site).

**Diseño a robar:**
- **Code-fence downgrade:** un match dentro de un bloque de código **baja un nivel de severidad** (es documentación, no ejecución) - pero **los bloques `run:` reales nunca se bajan**. Distinguir "esto es ejemplo" de "esto se ejecuta" es fino.
- **Delta vs estado previo:** fingerprint por `sha256(file + línea + patrón)`, clasifica **NEW / RESOLVED / PERSISTENT**. **Solo reporta lo nuevo o lo resuelto** - no te repite el mismo hallazgo cada vez.
- **Silenciosa en no-op:** *"never notifies on a pure no-op week"*. Si no hay nada, no dice nada. **La regla del silencio aplicada a un scanner.**
- **Veredicto `CLEAN` / `ATTENTION` / `DEGRADED`**, más PASS/WARN/FAIL por skill.
- **Read-only, y con límites:** nunca auto-borra una supresión de baseline, nunca edita su propia biblioteca de patrones desde adentro.
- **Remediación por hallazgo:** cada patrón tiene su fix de una línea (comillar la variable, mover el secreto a prefetch, allow-list, borrar la skill si es payload).

#### 📊 2. `skill-evals` - la red de calidad

Cada skill declara un **manifiesto de assertions** en YAML, y el output se chequea contra él:

```yaml
narrative-tracker:
  min_words: 400
  required_sections: ["TRANSITIONS", "POSITIONS", "MAP"]
  forbidden_patterns: ["exciting", "consider"]
  must_cite_source: true
```

Assertions soportadas: `min_words`/`max_words`, `required_patterns`/`forbidden_patterns`, `required_sections`, `must_cite_source`, `min_distinct_items`, `output_pattern` (regex).

**Diseño a robar (muy bueno):**
- **Estados de regresión, no un simple pass/fail:**
  | Estado | Significado |
  |---|---|
  | `NEW_FAIL` | Pasaba, ahora falla. **La severidad escala con la racha de pases previos.** |
  | `NEW_PASS` | Fallaba, ahora pasa. **Se registra la victoria.** |
  | `CHRONIC` | Falla hace más de 3 corridas. **Recomienda revisión, no re-file.** |
  | `STABLE_FAIL` | Siempre falló. **Es un mismatch del manifiesto, no del output.** |
- **Distinguir regresión de test mal escrito.** `STABLE_FAIL` significa *"el manifiesto está mal"*, no *"la skill está rota"*. **Esa distinción evita el falso positivo permanente** - el mismo mal que ya nos mordió con checks que dan falso verde.
- **Bootstrap mode:** en vez de escribir las assertions especulativamente, **muestrea las últimas 5 corridas exitosas** y deriva el manifiesto (min_words en el p25 histórico, patrones de los headers comunes). *"Assertions are observations, not specifications."* **El contrato se deriva de la realidad, no se inventa.**
- **Nunca auto-commitea un manifiesto:** *"assertions need a human signoff"*.
- **Lista negra de patrones de relleno:** `"I cannot"`, `"as an AI"`, `"exciting"`, `"consider"` - marcadores de alucinación y de hedgeo. **Y la regla: mantenerla corta y no usarla para lintear estilo.**

#### 🔧 3. `skill-repair` - el diagnóstico con receta

Clasifica el fallo en **ocho categorías** y aplica el playbook correspondiente:

| Categoría | Detección | Fix |
|---|---|---|
| `api-change` | 404/410, schema mismatch | Actualizar endpoint/payload **citando la spec viva**. |
| `rate-limit` | 429 | **Agregar backoff. "Never raise the limit."** |
| `timeout` | Corte a mitad | Stagear el trabajo, early-return en éxito parcial. |
| `sandbox-limitation` | curl con auth falla | Convertir a patrón prefetch/postprocess. |
| `prompt-bug` | Alucinación, rechazo, sección faltante | **Mínima edición de especificidad, diff menor a 30 líneas.** |
| `output-format` | Ejecuta pero falla el parser | Editar hasta satisfacer la assertion que falla. |
| `missing-secret` | Env var sin setear | **CERO cambio de código.** Nombra la var faltante y sale `REPAIR_DIAGNOSED_NO_FIX`. |
| `unknown` | Ninguna de las anteriores | **No edita a ciegas.** Guarda el dossier y sale sin fix. |

**Diseño a robar:**
- **`missing-secret` no es un bug de código.** El instinto de un agente es "falta la var, la agrego" - **esto lo prohíbe explícitamente** y escala al operador. Exactamente nuestra regla de secretos.
- **Clases de riesgo con umbral de aplicación:** LOW (< 30 líneas, fallback) se auto-aplica; MED se auto-aplica **con receta de verificación**; **HIGH requiere revisión del operador, nunca auto-aplica**. Es el mismo gradiente que los automation tiers de Autensa, aplicado a reparar código.
- **Receta de verificación obligatoria en toda reparación:** (1) re-correr con la invocación exacta, (2) **señal esperada específica de la categoría** (*"no rate-limit in trace"*, *"≥ 200 words"*), (3) camino de fallback. **Reparar sin receta de verificación es el falso verde.**
- **Cooldown de 24h por skill:** evita loops de reparación sobre un fix que no pegó.
- **Chequeo de liveness de las fuentes:** hace WebFetch sobre las URLs referenciadas para detectar 404s o cambios de schema. **La skill se testea contra el mundo real, no contra sí misma.**

#### 🧬 4. `autoresearch` - la evolución

Toma un SKILL.md objetivo, genera **cuatro variaciones** en paralelo, las puntúa y aplica la ganadora.

**Las cuatro tesis (el diseño central):**
- **A - Mejores inputs:** reemplazar APIs deprecadas, agregar fallbacks, arreglar endpoints rotos.
- **B - Output más filoso:** formato más ajustado, señal sobre ruido, veredictos explícitos, relleno prohibido.
- **C - Más robusta:** manejo de datos vacíos, reintentos, dedup de estado, conciencia de rate-limit.
- **D - Replanteo:** **metodología fundamentalmente distinta para el mismo objetivo.**

**Scoring:** 1-5 por eje, total ponderado sobre 50:
| Eje | Peso |
|---|---|
| Mejora vs original | **3x** |
| Valor del output | 2x |
| Claridad, calidad de datos, robustez | 1.5x c/u |
| Convenciones | 1x |

Desempate (dentro de 2 puntos): **prefiere la variación con la mejora más grande en un eje** por sobre muchas mejoras chicas.

**Diseño a robar (y es el mejor de la suite):**
- **La garantía de seguridad: "never downgrades a working skill".** Si **todas** las variaciones puntúan ≤ el original en el eje *Mejora*, **aborta con `AUTORESEARCH_NO_IMPROVEMENT` y no escribe nada.** **Nuestro equivalente es el gate que no da falso verde: acá está como imposibilidad mecánica de empeorar.** El patrón general: *"el cambio solo se aplica si demuestra mejora respecto del estado actual"*.
- **La variación D es la más interesante:** obliga a incluir **un replanteo metodológico**, no solo mejoras incrementales. Evita el óptimo local.
- **Dos modos:** `evolve` (escribe el diff) y **`dry-run` (puntúa e imprime, no escribe nada)**. Nuestra regla de inspeccionar antes de modificar.
- **Versionado con rollback:** dentro de un repo git, va a una rama `autoresearch/<skill>` y **el operador revisa el diff antes de mergear**; fuera de git, preserva `SKILL.md.before-autoresearch`. **Nunca pisa directo.**
- **Output = el diff + la tabla de scoring de las cuatro + un párrafo de racional.** La decisión es auditable.

#### 🎯 Por qué encaja con nosotros

Es **el ciclo de vida completo de una skill**, y **la mitad ya la tenemos a medias**:
- `skill_workshop` cubre parcialmente **crear/actualizar** (≈ autoresearch), pero **sin scoring, sin cuatro tesis y sin garantía de no-empeorar**.
- No tenemos el **scan de seguridad previo** (crítico: instalamos skills de afuera).
- No tenemos **evals** (assertions contra output real).
- No tenemos **repair** con clasificación de fallo y receta de verificación.

**Y las cuatro comparten un valor transversal:** cada una tiene **un gate explícito de "no empeorar"** - scan no toca el baseline, evals no auto-commitea, repair no toca HIGH ni secrets, autoresearch aborta si no hay mejora. **Es la misma filosofía que nuestras Red Lines, hechas mecanismo.**

#### ⚠️ Puntos de atención

1. **Son del repo de Bankr** (90% cripto) - **no adoptar el repo, adoptar estas cuatro skills como referencia.** Auditar el código de cada una antes de copiarla: son skills que **escanean y escriben skills**, o sea que tienen permiso para tocar el árbol de skills. **Hay que leerlas con el mismo criterio que ellas exigen.**
2. **Dependencias:** `skill-evals` necesita que cada skill declare un manifiesto; `autoresearch` necesita un modelo para generar y puntuar (caro); `security-scan` asume `<skills-dir>`. **Ninguna es drop-in.**
3. **Escalan con la cantidad de skills.** Tenemos 78 en el índice (27 core + 51 de roles). Un scan de 78 skills y un autoresearch sobre una de ellas son costos reales.
4. **`skill-evals` necesita "el output más reciente"** de cada skill - nuestros skills no todos producen un output guardado. **Sin output persistido, no hay contra qué evaluar.**
5. **No verificado por nosotros.**

> **Veredicto: el hueco más grande que encontramos en las dos rondas, y con la solución más clara.** Tenemos `skill_workshop` para crear y actualizar, **pero nada que audite antes, mida después, repare cuando falla, ni evolucione con criterio.** Las cuatro etapas existen, son stack-agnósticas, y **cada una trae un gate de no-empeorar alineado a nuestras Red Lines**. No hay que instalarlas: **hay que construir el ciclo, y estas cuatro son el plano.** Prioridad sugerida: `skill-security-scan` primero (es el de mayor riesgo real, porque instalamos de afuera), después `skill-evals`. `autoresearch` es el más caro y el último.

### 4. El cluster de diseño de VoltAgent - el filtro prioritario, con sustancia

Fuente: [VoltAgent/awesome-openclaw-skills](https://github.com/VoltAgent/awesome-openclaw-skills) (= ClawHub, 5.300 skills). **Recordatorio del filtro: curan, NO auditan** - 7.215 skills quedaron fuera (4.065 spam, 373 maliciosas). Cada una es untrusted hasta que se lee.

**Del directorio, ~20 candidatas y ni una abierta hasta ahora.** Acá van las tres que importan.

#### 🥇 `anti-slop-design` (kjaylee) - el que ataca el problema real

**Qué hace:** previene la **estética genérica de IA** en frontends. Cubre tipografía, color, motion, layout y UI de juegos. *"Rather than general design advice, it names specific forbidden patterns and forces a deliberate aesthetic choice from a concrete list of styles each time."*

> **Las dos mitades de esa frase son el diseño entero:** (1) **nombra patrones prohibidos concretos** - no "usá buen tipografía", sino *"esto sí, esto no"*; (2) **fuerza una elección estética deliberada de una lista concreta** - no deja que el modelo caiga en el default.

Casos de uso declarados que nos tocan:
- **"Una landing que no se vea como cualquier otro sitio SaaS"** - es exactamente nuestro problema.
- **"Font pairings que evitan defaults sobreusados como Inter"** - el default de facto de la IA.
- **"Un dashboard con asimetría intencional y jerarquía visual"** - nuestro caso, cada vez que armamos una UI.

**Por qué es el más valioso del cluster:** es **el equivalente de `deslop` pero para UI**. Nosotros ya tenemos la skill `deslop` (limpia código slop de IA antes de un PR) - **esta es la misma idea aplicada a la estética.** Y es **la única que ataca la causa** (el default genérico) en vez del síntoma.

#### 🥈 `kj-ui-ux-pro-max` (kjaylee) - el generador con tokens

**Qué hace:** guía UI/UX para construir y refinar interfaces web y mobile. Cubre **layout, mapeo de flujos UX, tokens de design system, specs de componentes, microcopy y accesibilidad.** Puede producir artefactos de diseño, planes de implementación, o ambos en una pasada.

**Lo que importa:** *"Covers design decisions and frontend implementation together, so you don't have to context-switch."*

> **Y acá aparece lo que `design-audit` pedía y no teníamos: esta skill GENERA los tokens.** `design-audit` audita *contra* un design system; `kj-ui-ux-pro-max` **produce el design system**. **Son complementarias, no alternativas** - una crea la vara, la otra mide contra ella.

Casos de uso: generar un layout con **spacing y color tokens**, auditar un form para **WCAG AA**, especificar una librería de componentes **con estados y reglas de interacción**, mapear un flujo **con estados de error y vacío**, refactorizar Tailwind hacia una dirección de marca.

#### 🥉 `axe-devtools` (dylanb) - la accesibilidad medida, no declarada

**Qué hace:** corre escaneos de accesibilidad en **páginas vivas** usando el **MCP Server de axe DevTools vía Docker**. Devuelve violaciones con **rule IDs, nivel de impacto y selectores afectados**, y después **trae guía de fix por violación**. Sin página viva, aplica buenas prácticas estáticas.

**El diseño a robar:** *"devuelve fixes de código específicos en vez de solo una lista de nombres de reglas"*. **Detectar no alcanza: la herramienta trae la remediación.** Y permite **re-correr el scan tras los fixes para confirmar cero violaciones** - el ciclo cerrar-medir-verificar.

**⚠️ Punto de atención serio:** requiere `AXE_API_KEY`, **una suscripción PAGA** a Axe DevTools for Web, Docker corriendo y la imagen `dequesystems/axe-mcp-server`. **No es gratuito ni liviano.**

> **Y nosotros ya tenemos cobertura acá:** `a11y-at-validation` y `ui-contrast-audit` propias. **Comparar antes de pagar** - lo que axe agrega es el escaneo contra **página viva** (vs estático) y la guía de fix por violación. **Eso se puede cubrir con la tool `browser` + axe-core open source, sin suscripción.** Es el único del cluster que descarto por costo/beneficio.

#### 🎯 El cuadro completo (y por qué cierra el eje)

| Pieza | Rol en el eje | ¿La necesitamos? |
|---|---|---|
| **`anti-slop-design`** | **Evita** la estética genérica | ✅ **La más valiosa** - ataca la causa |
| **`kj-ui-ux-pro-max`** | **Genera** tokens y specs | ✅ Cubre el hueco que `design-audit` señaló |
| **`design-audit`** (jdrhyne) | **Audita** contra el sistema | ✅ El rol que falta |
| **`axe-devtools`** | **Mide** accesibilidad | ⚠️ Ya cubierto; pagar solo si el estático no alcanza |

> **La conclusión del eje de diseño:** no es "elegir una skill". **Es un pipeline de cuatro roles** - evitar el default, generar el sistema, auditar contra él, medir accesibilidad. Y el orden importa: **primero `kj-ui-ux-pro-max` produce los tokens** (es lo que desbloquea a `design-audit`), **`anti-slop-design` va desde el día uno** (evita el daño antes de que exista), y `axe-devtools` solo si el escaneo estático no alcanza.

#### ⚠️ Puntos de atención

1. **Vienen de ClawHub, curadas pero NO auditadas.** `anti-slop-design` y `kj-ui-ux-pro-max` hay que leerlas antes de instalar - **y son justamente las que escriben en nuestro árbol de skills.**
2. **`kjaylee` tiene tres skills del mismo autor** (`anti-slop-design`, `kj-ui-ux-pro-max`, `kj-web-design-guidelines`) - **se refuerzan entre sí, son un paquete.**
3. **`axe-devtools` es de pago** y ya tenemos cobertura propia; el open source lo cubre casi todo.
4. **Los defaults que atacan son de ecosistema web genérico** (SaaS, landing, dashboard). **Nuestro caso no es vender un producto** - es la UI del workspace y de los proyectos de Gonzo. El filtro sigue siendo bueno, pero **el tono de marca es una decisión, no un default a evitar.**
5. **No verificado por nosotros.** Ninguna instalada.

> **Veredicto: el cluster tiene sustancia real, y confirma el hallazgo del eje de diseño.** `anti-slop-design` es la joya (previene la causa), `kj-ui-ux-pro-max` **genera los tokens que `design-audit` necesita** (cierra el círculo), y `axe-devtools` se descarta por costo/cobertura. **El veredicto del directorio - "no instalar 10 skills, adoptar 2-3 y definir un design system" - se confirma, pero ahora con los roles exactos y el orden correcto.**

### 5. El Academic Multi-Agent System (13 roles) - el patrón Factory, ya construido

Fuente: [TravisLeeeeee/awesome-openclaw-personas/personas/academic](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/academic). **Es la implementación viva del "Factory de investigación"** que nuestro catálogo tenía como idea. **13 roles reales**, cada uno un directorio con `SOUL.md` + `AGENTS.md` + `SKILL.md`.

**Los 13 roles:** `planner` (orquestador), `ideator`, `literature-scout`, `surveyor`, `critic`, `reviewer`, `writer`, `coder`, + **cinco especialistas de dominio** (`anthropologist`, `geographer`, `historian`, `narratologist`, `psychologist`).

#### 🔌 La capa de agentes (el `AGENTS.md` del Planner)

Los `AGENTS.md` son **configuración operativa real**, no prosa. El del Planner define:
- **Modelo primario + fallback** por rol.
- **Tools asignadas:** `read, write, edit, exec, apply_patch` + **`sessions_list, sessions_history, sessions_send, sessions_spawn`**. Es **la capa de orquestación de subagentes de OpenClaw, cableada a nivel rol.**
- **Gestión de sesión:** mantener un **tablero de estado del proyecto persistente** entre conversaciones, trackear fases, blockers y asignaciones.
- **Comunicación inter-agente con direcciones explícitas:** *Upstream* (recibe del agente principal), *Downstream* (despacha a todos los sub-agentes), y **escalación: reporta conflictos sin resolver al principal después de 3 rondas.** **Un límite de rondas antes de escalar - nuestro 3-Strike Protocol, pero entre agentes.**

> **Lo que confirma: nuestro patrón de roles y spawns es el correcto.** Acá está validado por un sistema de 13 agentes que corre de verdad. Y agrega dos cosas que no tenemos: **el tablero de estado persistente entre conversaciones** y **la escalación con límite de rondas.**

#### 🎯 El `critic` - y acá está la joya

**El rol más valioso de los 13, y el que más tenemos que robar.** Su credo: ***"Good enough is the enemy of great."***

No es un reviewer: **es el guardián del *gusto*.** El propio repo marca la distinción:

| | **Reviewer** | **Critic** |
|---|---|---|
| Perspectiva | ¿Pasa el corte? | **¿Merece ser bueno?** |
| Foco | Corrección técnica, completitud | **Profundidad del insight, narrativa, impacto** |
| Output | Lista de fortalezas/debilidades | **"¿Cuál es el alma de esto?"** |
| Estándar | Umbral de aceptación | **Nivel excepcional** |

**El marco SHARP de evaluación de ideas** (5 ejes, 1-5 cada uno, total /25):
| Eje | Pregunta |
|---|---|
| **S** - Sharpness | ¿El insight central es filoso, da en el blanco? |
| **H** - Horizon | ¿Tiene valor de largo plazo o es efímero? |
| **A** - Asymmetry | ¿Tenés un ángulo o información que otros no? |
| **R** - Resistance | Ante el crítico más duro, ¿tu tesis se sostiene? |
| **P** - Parsimony | ¿Es elegante y simple, o sobre-complejo? |

**Veredictos:** Exquisito (25-23) / Refinado (22-18) / Crudo (17-13) / Insulso (<12).

**Y dos pruebas de una línea, geniales:**
- **"El test de la frase única":** *si no podés explicar por qué funciona en una frase, el insight no es filoso.*
- **"El test del bar":** *¿en 30 segundos, un colega en un bar diría "esto sí es interesante"?*

**El drill-down de presión simulada:** obliga a listar **las 3 objeciones más duras** y la respuesta preparada a cada una, más un veredicto de resistencia (sólido / aguanta / se rompe). **Es el adversarial review convertido en paso obligatorio.**

**Los seis anti-patrones que detecta** (con la frase exacta que dice):
| Anti-patrón | Lo que dice |
|---|---|
| **Innovación de envoltorio** | *"Sacá tu nombre de marca: ¿qué diferencia esencial tiene con X?"* |
| **Paper apilado** | *"¿Qué componente es tu insight? ¿Borrás los otros y sigue funcionando?"* |
| **El cómo sin el porqué** | *"¿Por qué funciona realmente? ¿Podés explicarlo teóricamente?"* |
| **Puntaje SOTA** | *"¿Subir 0.5% qué insight trae? ¿Qué nos dice?"* |
| **Ablación falsa** | *"¿Cuánto le saca al baseline más simple? ¿La diferencia es por tu innovación?"* |
| **Investigación follow-up** | *"Si el autor original lo ve, ¿creería que merece un paper propio?"* |

**Las "tres preguntas del alma":** ¿resuelve un problema real o uno inventado? ¿el lector va a cambiar algo después de leerlo? ¿cuántas veces se citará en cinco años y por quién?

> **Por qué esto es oro para nosotros:** es **un rol de gusto adversarial con criterio explícito y medible**, y su trabajo es **el que hoy nadie hace**: distinguir "esto pasó el gate" de "esto es bueno". Nuestro `verification-gates` verifica que algo **funcione**; el Critic verifica que algo **valga la pena**. **Son preguntas distintas, y la segunda no está cubierta.**

#### 🔑 Diseño a robar

- **El Reviewer y el Critic como roles separados.** Corrección técnica vs gusto. **Un solo revisor hace una sola de las dos cosas bien.** Es la separación de `verifier`/`verifier-of-verifier`, un nivel más arriba.
- **Criterio de gusto con rúbrica y número.** El SHARP convierte "esto es bueno" en **25 puntos con ejes ponderables**. **La subjetividad hecha medible.**
- **Los tests de una línea** (frase única, bar) - filtros baratos y rápidos para ideas.
- **Presión adversarial obligatoria:** las 3 objeciones más duras con respuesta preparada. **Antes de comprometerse, no después.**
- **Los anti-patrones con frase exacta.** No describe el problema: **da el guion de qué decir.**
- **Especialistas de dominio como capa.** `anthropologist`, `historian`, `psychologist` - **el mismo esqueleto (planner/critic/writer) con la lente del dominio encima.** Es el patrón "perfil" de Natilius aplicado a investigación.
- **Escalación con límite de rondas** (3) **y tablero de estado persistente** entre conversaciones.

#### ⚠️ Puntos de atención

1. **El `critic` está en chino.** Todo el `SOUL.md` está escrito en chino (con el español/inglés entremezclado en frases de citas). **El contenido es excelente, pero hay que traducirlo y adaptarlo** para usarlo.
2. **Es un sistema académico de papers** - arXiv, peer-review, Oral/Best Paper. **Nuestro caso es investigación de producto y de tools, no publicar papers.** El marco se adapta, pero **el tono academicista no calza directo.**
3. **Es de `awesome-openclaw-personas`** - el repo **patrocinado por DeskClaw** (plataforma comercial). Ya lo marcamos en la ficha del repo.
4. **Dice `anthropic/claude-sonnet-4-5`** como modelo - **de nuevo el sesgo a Claude.** Nuestros modelos son otros (ADR-090).
5. **13 roles son demasiados para nuestro caso.** El valor no está en copiar los 13, sino en **robar el esqueleto de tres** (planner/critic/writer) + el marco SHARP.
6. **No verificado por nosotros.**

> **Veredicto: el más valioso como REFERENCIA arquitectónica, y el `critic` es el rol que más nos falta.** No vamos a copiar los 13 roles ni el tono académico, pero **el triángulo Planner/Critic/Writer + el marco SHARP + los seis anti-patrones son directamente transferibles** a cómo revisamos nuestro propio trabajo (specs, ADRs, decisiones de producto). **La conclusión honesta:** nuestro catálogo de soluciones ya tenía "Factory de Investigación" como idea, y acá está **el diseño de 13 roles con SOPs reales.** Cuando montemos la nuestra, empezamos desde acá. **Y el rol `critic` debería existir en el crew, con o sin el resto.**

---

## 🏁 Cierre de la profundización (5 de 5)

Se abrieron los **cinco conjuntos** que habían quedado solo como directorio en la primera parte. El balance:

**Lo que se encontró, por orden de valor:**
1. **La suite `aeon`** - el **ciclo de vida de skills** (auditar/evaluar/reparar/evolucionar). **El hueco más grande de las dos rondas.**
2. **`knowledge-graph`** - memoria **sin base de datos nueva**, que **redefine la decisión de memoria pendiente**: quizá no haya que elegir entre los seis motores.
3. **El `critic`** (Academic System) - **el rol de gusto adversarial** que no tenemos, con rúbrica medible.
4. **El cluster de diseño** - `anti-slop-design` (previene la causa) + `kj-ui-ux-pro-max` (**genera los tokens que `design-audit` necesita**).
5. **`design-audit`** - el rol de auditor, con la precondición del design system.

**Los dos patrones que se repitieron en la profundización:**
- **El gate de no-empeorar:** `autoresearch` aborta sin mejora; el `critic` no aprueba mediocre; `design-audit` no cambia sin razón estructural. **Tres piezas distintas, el mismo principio.**
- **Roles con criterio explícito y medible** (SHARP / los 15 ejes de `design-audit` / el scoring de `autoresearch`). **El gusto se sistematiza, no se improvisa.**

**Y el hallazgo que cierra las dos tandas:**
> **Lo que nos falta no es una herramienta más, son tres roles y un sistema de tokens.** El auditor de diseño (con su design system), el crítico de gusto, y el ciclo de vida de skills. Y los tres tienen la misma forma: **alguien que dice "esto no alcanza" con un criterio que se puede auditar.**

---

## 🛠️ Estrategia de Expansión (Crew Scaling)

Cuando se requiera un nuevo rol para el equipo, el flujo de trabajo es:
1. **Búsqueda:** Consultar `awesome-openclaw-agents` para ver si el rol ya existe.
2. **Adaptación:** Tomar el `SOUL.md` base y ajustarlo a las preferencias de Gonzo y el contexto del workspace.
3. **Despliegue:** Registrar el agente vía `openclaw agents add` y ejecutar la tarea mediante `sessions_spawn`.
