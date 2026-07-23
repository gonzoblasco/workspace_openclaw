# DEFINITION — Sport Cars Jeep (Reinvención Digital)

## Resumen del producto

Plataforma web para concesionaria Sport Cars (Jeep/Ram) que reemplaza el sitio brochure actual por un sistema de generación y conversión de leads integrado con Pilot CRM y Mercado Libre, con chatbot de consultas automatizado.

## Personas

### P1 — El comprador curioso
- **Quién:** Persona que está considerando comprar un Jeep/Ram, investiga online
- **Necesita:** Ver modelos, precios, disponibilidad, comparar, preguntar sin compromiso
- **Fricción actual:** Tiene que llamar o mandar WhatsApp y esperar. No hay info de stock. No sabe qué financiación hay.
- **Lo que quiere del nuevo sitio:** Respuestas inmediatas, poder explorar sin presión, agendar un test drive sin hablar con nadie

### P2 — El comprador serio
- **Quién:** Ya decidió qué modelo quiere, necesita cerrar
- **Necesita:** Precio real, disponibilidad de stock, condiciones de financiación, turno para retirar
- **Fricción actual:** Le piden que llame. Le mandan info desactualizada. No hay transparencia en stock.
- **Lo que quiere del nuevo sitio:** Stock real, cotización con datos, reservar online, hablar con un vendedor ya calificado

### P3 — El vendedor del concesionario
- **Quién:** Empleado de Sport Cars que recibe leads
- **Necesita:** Leads pre-calificados con datos útiles (modelo de interés, rango de presupuesto, si tiene usado para entregar)
- **Fricción actual:** Le llegan leads sueltos por WhatsApp sin contexto. No sabe qué quiere el cliente hasta que habla con él.
- **Lo que quiere:** Leads en Pilot con datos completos, menos tiempo en respuestas básicas (las hace el chatbot), agendar test drives sin intermediación

### P4 — La hermana (insider/operations)
- **Quién:** Empleada de Sport Cars, contacto de Gonzo
- **Necesita:** Que el sitio no rompa nada que ya funciona, que sea fácil de explicar a sus jefes
- **Lo que quiere:** Algo que mejore su trabajo o al menos no lo complique, acceso a info de cómo funciona el proceso comercial

## Features core (MVP)

### F1 — Catálogo dinámico de vehículos
- Modelos Jeep (Compass, Renegade, Commander, Gladiator, Grand Cherokee, Wrangler) y Ram
- Fichas con specs, precios referenciales, imágenes
- Filtros por modelo, tipo, rango de precio
- **Diferenciación:** Info alimentada por Pilot (stock real cuando esté disponible) o por datos de Stellantis, no catálogo estático

### F2 — Chatbot de consultas
- Bot integrado en el sitio (widget flotante)
- Base de conocimiento: modelos, precios referenciales, financiación, test drive, sucursales, horarios, contacto
- Capacidades: responder preguntas frecuentes, derivar a vendedor humano cuando corresponde, capturar datos del interesado
- Derivación a WhatsApp cuando el usuario quiere hablar con alguien
- **Lead capture:** Todo contacto con datos va a Pilot CRM via API
- Stack del bot: a definir en 0.2 (opciones: LLM con RAG local, Cliengo existente, solución custom)

### F3 — Integración Pilot CRM (lead pipeline)
- Formularios del sitio (contacto, test drive, cotización de usados) envían leads a Pilot
- Usar app token + sub origen de Pilot (a obtener de la hermana)
- Webhook de Pilot para creación de leads
- Datos a capturar: nombre, teléfono, email, modelo de interés, sucursal preferida, tipo de consulta
- **Importante:** Pilot ya está en uso, solo necesitamos conectar el sitio como fuente de leads

### F4 — Integración Mercado Libre
- Mostrar publicaciones de MeLi del concesionario embebidas en el sitio (no link externo)
- Sincronización de inventario de usados desde MeLi (si publican ahí)
- Query a MeLI API para listings del seller
- Posible bidireccional: si un usuario consulta un auto de MeLi desde el sitio, el lead va a Pilot con referencia a la publicación
- **Nota:** Pilot está certificado por MeLi como integrador — probablemente ya hay un flujo MeLi↔Pilot que podemos aprovechar en lugar de construir uno paralelo

### F5 — Sucursales y contacto
- 3 sucursales con info real (direcciones, horarios, mapas, WhatsApp directos)
- Click-to-call y click-to-WhatsApp por sucursal
- Horarios de showroom y taller

### F6 — Agendamiento de Test Drive
- Formulario con selección de modelo, sucursal, fecha/horario
- Lead a Pilot con tipo "Test Drive"
- Confirmación por WhatsApp o email (a definir)

### F7 — Cotizador de usados
- Reemplazar el "cotizador" genérico actual
- Si tienen inventario de usados en Pilot o MeLi: mostrarlo
- Si no: formulario de evaluación que derive a Pilot como lead tipo "Tomo usado"

## Features futuras (post-MVP)

- **F8** — Dashboard interno para vendedores (ver leads del sitio en tiempo real)
- **F9** — Simulador de financiación (si hay API de bancos o se cargan tasas manualmente)
- **F10** — Comparador de modelos (side-by-side)
- **F11** — Blog / noticias del concesionario
- **F12** — Integración con redes sociales (Pilot ya tiene módulo)
- **F13** — SEO local por sucursal (landing pages por zona)
- **F14** — Reserva de turno de servicio (postventa) — Pilot tiene turnero web

## Métricas de éxito

### Norte
- **Leads generados al mes** via el sitio web (objetivo: 2-3x vs. sitio actual)

### Secundarias
- **Tasa de conversión** visitante → lead (% del tráfico que deja datos)
- **Leads que llegan a Pilot con datos completos** (nombre + teléfono + modelo de interés)
- **Consultas resueltas por chatbot sin intervención humana** (% de conversaciones que no requieren derivación)
- **Test drives agendados** via el sitio por mes
- **Tiempo de respuesta a consultas** (de "horas/días" a "instantáneo" para chatbot)

### Proxies de engagement
- Tiempo en sitio
- Páginas por sesión
- Clics en "hablar con vendedor" / WhatsApp

## Stack tecnológico asumido

**Propuesta inicial (a confirmar en 0.2):**

- **Frontend:** Next.js 15 + TypeScript + Tailwind + shadcn/ui (stack de Gonzo)
- **Hosting:** Vercel
- **Backend/BaaS:** Supabase (auth, DB para contenido propio, edge functions para webhooks)
- **CMS:** Payload CMS o Sanity (para contenido editorial del sitio — modelos, promociones)
- **Chatbot:** A definir — opciones:
  - LLM (GPT/Claude/DeepSeek) con RAG sobre base de conocimiento del concesionario
  - Cliengo (ya tiene integración Pilot + chatbot)
  - Solución híbrida (chatbot simple para FAQ + LLM para preguntas complejas)
- **Integraciones:**
  - Pilot CRM API (JWT auth, lead creation webhook)
  - Mercado Libre API (listings del seller)
  - WhatsApp Business API (para derivación y confirmaciones)

## Restricciones conocidas

1. **Branding Stellantis/Jeep:** Puede haber guidelines de marca que respetar (colores, logos, tipografía). A confirmar con la hermana.
2. **Acceso a Pilot API:** Necesitamos credenciales reales (app token, sub origen, company_code). La hermana puede conseguirlos.
3. **Acceso a MeLi API:** Necesitamos el seller_id de Sport Cars en MeLi y posiblemente un app registrada en MeLi Developers.
4. **Dominio:** sportcarsjeep.com.ar ya existe. ¿Lo reemplazamos o usamos subdominio?
5. **Presupuesto:** Si Gonzo lo hace como portfolio, el costo principal es hosting + LLM para chatbot. Si cobra, cambia el scope.

## Posicionamiento

**"El primer concesionario Jeep con un sitio que trabaja para vos."**

Sport Cars no compite por ser el concesionario más grande, compite por ser el más fácil de comprar. Mientras otros tienen brochures estáticas, Sport Cars tiene un sistema que responde, agenda y conecta — 24/7.

## Suposiciones validadas (respuestas de Gonzo)

| # | Suposición | Estado | Nota |
|---|---|---|---|
| 1 | El concesionario está abierto a reemplazar el sitio actual | 🟢 Confirmado | Reemplazo total de sportcarsjeep.com.ar |
| 2 | Pilot API permite lead creation desde sitios externos | 🟢 Confirmado técnicamente | Diferido al Post-MVP por falta de acceso admin |
| 3 | Pilot API expone stock/inventario | 🔴 No confirmado | No relevante para MVP; inventario viene de MeLi |
| 4 | Sport Cars publica en MeLi | 🟢 Confirmado | Publica directamente; datos viajan a Pilot automáticamente |
| 5 | Hay guidelines de Stellantis para sitios de concesionarios | 🟡 Pendiente | A confirmar con la hermana/gerencia |
| 6 | El template actual es shared entre concesionarios | 🟢 Confirmado | Neostar, Motorville, Guini usan el mismo template |

## Preguntas respondidas en Fase 0.1

1. **¿Stack de chatbot?** → Custom con LLM + RAG
2. **¿Pilot API endpoints?** → Lead creation vía webhook confirmado; resto desconocido sin acceso admin
3. **¿MeLi: API pública o Pilot↔MeLi?** → API pública de MeLi; Pilot↔MeLi es interno suyo
4. **¿CMS?** → No para MVP; hardcodear contenido inicial
5. **¿Reemplazo o convivencia?** → Reemplazo total
6. **¿Supabase o backend custom?** → Supabase + Next.js full-stack
7. **¿Mobile-first?** → Sí, tráfico de concesionarias es mayoritariamente mobile

## Decisiones de arquitectura derivadas

- Pilot CRM se integra en **Post-MVP** (falta acceso admin)
- Leads se capturan en **Supabase** y se notifican por email/WhatsApp
- Inventario real proviene de **Mercado Libre API pública**
- Chatbot propio con **Vercel AI SDK + LLM (Ollama/DeepSeek propio de Gonzo) + RAG en Supabase**
- SaaS a **300 USD/mes todo incluido** cubre hosting, DB, dominio y soporte; el LLM lo cubre Gonzo con su infraestructura

## Go/No-Go criteria para pasar a 0.2

- [x] Problema definido en una frase ✅
- [x] Público objetivo identificado (P1-P4) ✅
- [x] Features core listadas (F1-F7) ✅
- [x] Métricas de éxito definidas ✅
- [x] Stack asumido y restricciones técnicas documentadas ✅
- [x] Preguntas abiertas para el arquitecto ✅

**Fase 0.2 completada.** Documentos generados:
- ARCHITECTURE.md
- DATA_MODEL.md
- OPENSPEC.md
- ROADMAP.md
- STATUS.md
- ADRs (5)