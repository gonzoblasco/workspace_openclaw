# USER.md - About Your Human

- **Name:** Gonzalo
- **What to call them:** Gonzo / Gonza / Gonzalo / Lider Supremo (usar con criterio)
- **Pronouns:** él/he
- **Timezone:** America/Buenos_Aires (GMT-3, Argentina)
- **Notes:** Quiere honestidad por encima de todo. No le des la razón solo por ser quien tiene el botón de encendido/apagado. No le comentes el horario - trabaja cuando puede.
- **Búsqueda laboral:** entrevista con OpenSistemas confirmada (25/08, 9AM) - perfil AI-Native, colaboración freelance 100% remoto LATAM.
- **GitHub writing rule:** siempre usar guion comun (-), nunca guion largo (em dash, U+2014). El guion largo no esta en el teclado y se nota que no es un dev escribiendo.
- **Regla de escritura general:** mismo criterio - guion comun (-) siempre. NUNCA usar guion largo (em dash U+2014, en dash U+2013) en ningun contexto. Issues, PRs, comments, docs, memorias, todo.
- **Precios, fechas, vencimientos, specs:** verificar con web_fetch antes de responder. No inventar ni asumir.
- **Analizar antes de asumir (2026-09-02):** ante cualquier mensaje mío, no quedarse con la primera lectura. Pasar por tres lecturas antes de responder: (1) literal - qué dice el texto; (2) con tono - qué dice la relación, el humor, el contexto; (3) con intención - qué estoy buscando al decirlo (¿discusión? ¿desahogo? ¿validación?). Si la ambigüedad es real, preguntar en vez de asumir. Alcance TOTAL: aplica también a conclusiones técnicas (debugging, reviews, código ajeno) - la primera lectura suele ser la superficial y a veces la equivocada.
- **Canal remoto (2026-09-07):** Telegram bot @kanam_ai_bot (DM, allowFrom user ID 7921100122). Reemplaza Tailscale Serve + PWA (desinstalado). El chat DM no necesita Tailscale; solo el /dashboard (Mini App Control UI) lo requeriria.

## Context

- Desarrolla aplicaciones - Fullstack real (React/TS frontend, Supabase/Edge Functions backend, DB, billing, tooling)
- 9+ años como desarrollador (frontend React), ahora Fullstack con IA como copiloto metodológico. Accesibilidad como hilo continuo desde 2016 (ver Trayectoria).
- Quiere que maneje su vida, archivos y proyectos
- Trabaja entre dos máquinas (Mac Mini y MacBook Air), workspace sincronizado por git
- Usa IA como infraestructura de trabajo (no como chat): sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop
- Stack opinado: create-stack, OpenSpec, ADRs, AGENTS.md, HANDOFF, CHANGELOG
- Accesibilidad como especialización activa
- Open source contributions como portfolio vivo (PRs a shadcn/ui, TanStack, astryx, radix, vercel/ai, y más)
- Proyecto estrella: SoporteML (CRM multi-tenant para vendedores de Mercado Libre con IA)
- También: fotógrafo, comunicación social, quiere escribir novelas
- Quiere organizar actividad física y mejorar salud

## Trayectoria profesional (verificado)

- **EY** (Sep 2021 - May 2025) - consultora internacional. Referente de accesibilidad del equipo: validó y corrigió 50+ componentes de una librería empresarial a WCAG, y fue parte del equipo que construyó una plataforma de inteligencia financiera. Nivel senior.
- **Super7ui** (Ago 2020 - May 2021) - consultora de medios digitales. En una plataforma de streaming global remedió 200+ problemas de accesibilidad probados con lectores de pantalla e implementó pruebas automáticas de a11y.
- **Minutentag / EULAS** (Feb 2016 - Nov 2019) - agencia de e-commerce para marcas de EE.UU. Desarrolló y mantuvo flujos de compra (checkout, carrito), participó de la migración a React y mejoró un sitio con 2M+ usuarios mensuales. Accesibilidad desde el inicio.

**Lectura para propuestas a11y (corregido 2026-09-11, 2da correccion de Gonzo):** a11y NO es un hilo secundario - es continua desde 2016 y en dos roles fue la funcion central:
- **Super7ui (Ago 2020 - May 2021, ~1 ano):** rol dedicado a accesibilidad. 200+ fixes probados con lectores de pantalla + pruebas automaticas de a11y. Contar como ano entero de a11y engineering.
- **EY (Sep 2021 - May 2025, ~3.7 anos):** referente de a11y del equipo, 50+ componentes enterprise a WCAG. Enterprise.
- **Minutentag/EULAS (Feb 2016 - Nov 2019, ~3.7 anos):** a11y parte sustantiva del rol; crecio de junior a referente de accesibilidad.
- **Total:** ~8+ anos de desarrollo con a11y; ~5 anos con a11y como funcion central/dedicada.

**Gap real y unico: no tiene certificacion IAAP (CPWA / WAS / CPACC).** No volver a marcar su a11y como "reciente" ni JAWS como gap, ni omitir Super7ui del conteo.

## Perfil profesional (diferenciador)

1. **Metodología IA-asistida own** - trabaja con un sistema completo de IA como infraestructura: sesiones por proyecto, memoria persistente, handoffs, subagentes, skill workshop. No usa IA como chat, la usa como copiloto metodológico. La mayoría de los devs no saben hacer esto.
2. **Stack opinado, no por default** - cura herramientas (CSN: OpenSpec, Biome, ADRs, HANDOFF, CHANGELOG). Decide por criterio, no por convención heredada.
3. **Accesibilidad como especialización activa** - no es checkbox, es ventaja competitiva. Tiene proyectos dedicados y busca trabajos donde sea central.
4. **Fullstack real** - React/TS frontend, Supabase/Edge Functions backend, DB, billing, tooling, scaffolding.
5. **Documenta decisiones, no solo código** - AGENTS.md, ROADMAP, ADRs. Eso es senior sin título.
6. **Producto real con IA** - SoporteML (CRM para vendedores de Mercado Libre con IA, backend sólido + billing) demuestra producto completo, no solo demos.

**El pitch:** *"Soy un dev fullstack que construyó un sistema de trabajo con IA propio, con stack opinado y docs de decisiones. Tengo PRs mergeados que lo demuestran."*

Un repositorio con PRs mergeados en shadcn/ui, TanStack, o Vercel vale más que cualquier take-home test.

## Estilo en issues/PRs de terceros

- Natural y suelto, no como manual de programación
- Sonar a persona real, no a documentación técnica
- En inglés siempre en repos externos
- Bugs concretos sin competencia → PR rápido
- RFCs → comentario técnico que posiciona, no código