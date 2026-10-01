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
| **[Cost Optimizer](https://github.com/mergisi/awesome-openclaw-agents/blob/main/agents/devops/cost-optimizer/SOUL.md)** | Optimización de costos - alineado a ADR-053 |

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
- **[Cost Optimizer](https://github.com/TravisLeeeeee/awesome-openclaw-personas/tree/main/personas/devops/cost-optimizer)** - recursos idle + right-sizing (ADR-053).

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

**2. Run Ledger & Spend Caps - ADR-053 hecho mecánica**
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

## 🏁 Cierre de tanda (20 repos)

**Balance:** de 20 repos, muy pocos son "instalar y usar". El valor se repartió en:
- **4 candidatos reales a adopción:** MemOS local (memoria), PowerContext (handoff), Claw Orchestrator (orquestación+verificación), Crabwalk (observabilidad).
- **2 candidatos en seguridad:** guardspine (gate de tool calls) y ClawSec (drift + advisory) - **complementarios entre sí**.
- **Muchos "buenos como diseño, innecesarios como implementación":** los dos MCP (redundantes con el core), skillshare, MemoV, HomeAssistant, MCP adapter.
- **Reglas nuevas que salieron de la ronda:** cripto = fuera; dos capas (implementación vs diseño); **verificar qué hace el core antes de sumar tooling externo**.

**Patrón transversal:** tres de los candidatos (Claw Orchestrator, MemoV, ClawSec) resuelven el mismo problema de fondo - **trazar, verificar y proteger lo que hizo el agente**. El ecosistema está convergiendo ahí. Eso sugiere que *ese* es el hueco real de nuestro setup.

---

## 🛠️ Estrategia de Expansión (Crew Scaling)

Cuando se requiera un nuevo rol para el equipo, el flujo de trabajo es:
1. **Búsqueda:** Consultar `awesome-openclaw-agents` para ver si el rol ya existe.
2. **Adaptación:** Tomar el `SOUL.md` base y ajustarlo a las preferencias de Gonzo y el contexto del workspace.
3. **Despliegue:** Registrar el agente vía `openclaw agents add` y ejecutar la tarea mediante `sessions_spawn`.
