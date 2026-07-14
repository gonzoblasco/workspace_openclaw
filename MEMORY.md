# MEMORY.md - Long-Term Memory

## Sobre Gonzo
- Gonzalo, Argentina (GMT-3)
- 9 años como Frontend React, ahora aprendiendo Fullstack
- Desempleado, usando IA para todo ("me reemplazaron por IA, ahora uso IA para todo")
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud
- Quiere honestidad absoluta — sin darle la razón por ser quien manda
- Arranca conversaciones limpias con frecuencia — el registro escrito es crítico
- Tiene entrevista para trabajo fullstack especializado en accesibilidad

## Sobre Kanam
- Nombre: Kanam 🌿
- Asistente virtual para todo: desarrollo, vida, archivos, proyectos
- Vibe: directo, honesto, cálido pero no servil
- Marca paraguas para todos los productos de Gonzo

## Forma de trabajo
- Todo se registra: MEMORY.md, memory/YYYY-MM-DD.md, projects/PROYECTOS.md, HANDOFF.md por proyecto, CHANGELOG.md
- Al arrancar conversación limpia → leer MEMORY.md + PROYECTOS.md + HANDOFF.md del proyecto que toque
- Antes de cerrar o cuando algo cambie → actualizar HANDOFF, CHANGELOG, memoria del día
- Heartbeat cada 1 hora → mantenimiento general
- Cron job cada 3 días → consolidar diarios a MEMORY.md (job ID: a6b2adb8-4b77-436a-b73c-2c866ac512f3)
- No escribir placeholders vacíos — solo escribí si hay algo real
- Canales: por ahora webchat, después WhatsApp y Telegram

## Ecosistema Kanam — Productos principales

### SoporteML (PRIORIDAD #1)
- CRM multi-tenant para vendedores Mercado Libre, Beta con 3 clientes
- Stack: React+Vite+TS+Supabase+pgvector+OpenAI (en Lovable)
- Billing roto — pendiente Mercado Pago (Stripe no sirve en Argentina)
- DB y Edge Functions en Lovable Cloud — extraer con prompts cuando migre
- Meta: sacar de Lovable a futuro (sin apuro)
- Repo: github.com/gonzoblasco/soporteml, rama el-upgrade

### KanamAI
- **Identidad/motor de IA transversal** — NO es un producto de MeLi, es la definición de cómo actúa la IA en todos los productos
- Define 3 cosas: (1) identidad de Kanam, (2) guardrails, (3) enrutamiento de modelos
- Los productos no hablan con GLM/Gemini directo — hablan con KanamAI, que decide qué modelo usar por tarea (definido en desarrollo, no automático)
- Por ahora: documentación local. Cada producto copia `.kanam/` del repo kanamai (igual que template/ y template-api/ en create-stack-next)
- Evolución: (1) copia manual → (2) paquete npm @kanam/ai-config → (3) servicio deployed tipo OpenRouter
- Stack del repo: TanStack Start + React 19 + Lovable AI Gateway (Gemini)
- Etapa 0-1 (landing + demo), 8 ADRs, roadmap 6 etapas
- 100% independiente (ADR-008) pero evolución de SoporteML
- Repo: github.com/gonzoblasco/kanamai-330ca8a9 (clonado como kanamai)
- Al escalar a otros marketplaces se renombrará (NO definir nombre aún)

### UmbraWriter (PRIORIDAD #2)
- Plataforma AI para escribir ficción (estilo Sudowrite), identidad propia
- PoC con 9 fases en roadmap
- Gonzo lo usará para escribir sus historias + posible SaaS para terceros
- Repo: github.com/gonzoblasco/umbrawriter (clonado)

### ReActiva (PRIORIDAD #3)
- SaaS para clínicas — recupera pacientes inactivos con IA + WhatsApp
- Pitch armado: 49-99 USD/mes, 15 clientes = vivís, MVP 5-7 días
- Estado: solo landing
- Repo: github.com/gonzoblasco/reactiva (clonado)

### create-stack-next (base transversal)
- CLI scaffolder opinado para Next.js 15, ~1000 descargas npm
- v0.6.1, Fase 3 en progreso, 55 tests
- Base metodológica de todo proyecto nuevo
- Sueño: proyectos existentes adoptan su estructura (AGENTS.md, ROADMAP, HANDOFF, CHANGELOG, ADRs)
- Repo: github.com/gonzoblasco/create-stack-next

## Proyectos de soporte
- brainweb — gestor de notas PKM con graph view SVG (github.com/gonzoblasco/brainweb-your-second-mind)
- accessibility-auditor — auditoría accesibilidad web (para entrevista)
- accessible-ui — librería React headless accesible (para entrevista)
- --copilot-skills — candidato a integrar con create-stack-next
- pr_vscode_niveles — guía gamificada VS Code

## Visión
- Kanam = marca paraguas + yo como asistente
- 3 productos SaaS son "IA que recupera relaciones perdidas": vendedores, pacientes, escritores
- KanamAI = la IA que alimenta todos los productos (identidad + guardrails + enrutamiento de modelos)
- create-stack-next = base técnica/metodológica de todo proyecto nuevo
- KanamAI funciona igual que template/ y template-api/ en create-stack-next — contenedor y plantilla a copiar

## Canales
- Activo: webchat
- Pendiente: WhatsApp, Telegram

## Ideas congeladas
- `FREEZER.md` — productos ideados pero fuera de foco actual
- Marketplace de servicios domésticos (ex "mucamas-online") — idea de marketplace, espera a que los 3 SaaS maduren
- KanamAI definición ampliada: no solo retención, sino "IA que facilita conexiones humanas" (pre, post, durante, marketplace)

## Lecciones aprendidas
- (a medida que pasen cosas)