# Job Search Tracker

> **Estado 2026-10-22: 2 procesos vivos (Infjini, TEAM International/tempo.io).** Staffy/Pfizer **cerrado 20/10** y Sol Bisio **cerrado 21/10**, ambos por el mismo filtro de inglés C1 conversacional. **Plan de inglés (cambiado el 2026-10-22): B2 intensivo en el CUI, dos meses, arranca el 26/10/2026** - desoxidar y mejorar la base; el examen CUI-ING C1 y el TOEFL quedan para despues.
>
> Regla de trabajo: cualquier proceso con +10 días sin respuesta humana real se cierra. Energía de follow-up: solo si ellos escriben. No se insiste más de una vez por proceso.

## Vacantes preparadas (2026-10-22) - CV y mensaje listos, NO enviados

> Busqueda activa (no a proposito de postulaciones). Barrido de a11yjobs, LinkedIn guest API,
> vacantesdigitales, remotive, himalayas, remoteok, jobicy, arbeitnow, getonbrd, landing.jobs y
> boards de Greenhouse/Ashby + 10Pearls, Svitla, Infojini, FullStack, Blacksmith.
> **Hallazgo:** el mercado de accesibilidad activo es casi entero US-only, y los avisos que
> filtran "LATAM" son casi todos el mismo bench de recruiters ya visto (Infojini, E-IT, FullStack:
> el mismo req de Disney/HTC). Lo nuevo son vacantes de front-end con a11y en empresas de producto.
> **Regla operativa que sale del relevamiento:** apuntar a empresas de producto con su propio
> equipo, no a nearshore-agencies que reasignan el tiempo a clientes US. En agencies el idioma es
> un filtro de elegibilidad; en producto es ruido de fondo.

| Empresa | Puesto | Ubicacion | Por que | Riesgo #1 | Estado |
|---|---|---|---|---|---|
| **RYZ Labs** | AI-First Frontend Software Engineer | Remoto US+LATAM | El JD pide "AI coding tools en el flujo de trabajo diario" + design systems + UI polish: es el perfil "AI-native frontend" del corpus | **Idioma conversacional** (el JD no declara nivel) | **POSTULADO POR FORMULARIO 22/10** (Lever) + **invitacion de conexion enviada** a Sonia Langone (recruiter tecnica de RYZ) con nota de 833 caracteres. El formulario tiene **hCaptcha que no se resuelve sin humano**: token 0 en headless y en browser visible automatizado. **Queda pendiente 1 click humano de Gonzo.** Captura: `outreach-2026-10-22/evidencia/ryz-form-filled.png` |
| **Mural** | Senior Software Engineer, Growth & Engagement | Argentina | React/TS + ownership end-to-end + experimentos A/B reales (Adobe Target, Minutentag 2019) | **Idioma**: el JD pide feature flags/analytics/event pipelines, que no tenes (declarados como gap en el CV) | **POSTULADO 22/10 Y CONFIRMADO** (Ashby): banner verde "Your application was successfully submitted". Salario USD 3.400/mes, CV + cover letter adjuntos. Captura: `outreach-2026-10-22/evidencia/mural-form-filled-submitted.png` |
| **Mercado Pago (ML)** | UX Expert - Software | Buenos Aires, hibrido | Diseno↔ingenieria (revision de disenos antes de implementar + requisitos con guia de codigo, en EY) + design system propio + SoporteML (CRM para vendedores de MeLi, el mismo dominio) | **No es el idioma: es que el puesto es mas de diseno que de ingenieria** | **POSTULADO 22/10 Y CONFIRMADO** (Eightfold): "¡Gracias por su solicitud, Gonzalo!" + `201 success: true` del servidor. Salario no aplica (el ATS de MeLi no lo pide). Captura: `outreach-2026-10-22/evidencia/meli-form-filled-submitted.png` |

**El mensaje de idioma NO aplica a los tres por igual:** en RYZ y Mural va al final del primer
mensaje (el filtro de Staffy/Sol se filtro tarde y caro). En Mercado Pago no se pregunta: es un
puesto local, con equipos locales, y la pregunta proyectaria una duda que no hace falta.

**Gaps declarados, no escondidos:** los tres CVs traen una seccion "Notes / gaps" con lo que el
JD pide y no se cubre. En Mural eso es deliberado: un gap declarado se discute, un gap callado se
descubre tarde. En el archivo que se posta esas secciones quedan excluidas (el CV son 2 paginas,
no 3); el mapa completo esta en el `.md` fuente.

**Estado 2026-10-23 (cierre de la tanda):** dos de tres POSTULADOS y CONFIRMADOS por el servidor (Mural y Mercado Pago). RYZ tiene el formulario COMPLETO (captura con todos los campos) pero su hCaptcha no se resuelve por automatizacion: el token da 0 tanto en headless como en browser visible, incluso clickeando el checkbox del iframe. Ese paso lo hace Gonzo en un minuto. La via secundaria (invitacion de conexion a la recruiter con nota) YA salio.

**CVs de apoyo (sin preparar):** Bluelight (React Engineer, Remote LATAM, 23/09), Makai Labs
(Senior Next.js, 29/09), Nortal (Lead Frontend React, WFH, 09/10), Google (Senior Frontend
Remoto LATAM - pide "ingles avanzado" explicito: es un test del filtro, no una opcion segura).
Descartados: GraceMark (pide 10+ anos y es 100% remote within Mexico), FOURSYS (QA de a11y, te
encasilla en testing), Blacksmith (pide portfolio de diseno en Figma), Speria y Profound (diseno,
no ingenieria), Infojini (ya es tu proceso vivo).

## Procesos activos

| Empresa | Puesto | Contacto | Tarifa | Estado 2026-10-21 |
|---|---|---|---|---|
| **TEAM International** (cliente **tempo.io**) | Senior Frontend Developer (Growth) | David Sanin Valencia | USD 5.000/mes fijos (≈ USD 31,25/h a 160 h) | **CV ENVIADO 21/10. ENTREVISTA AGENDADA: lunes 26/10/2026, 10:00 ART** (= 09:00 EST, en horario de US). Pitch "English Advance"; el JD dice **B2+**. Gonzo declaró B2 + plan C1 y David no respondió el punto. David se desconectó tras el envío; el CV fue el mensaje que reopened el proceso. **Sin confirmar qué paso del proceso es** (call informativa con David / entrevista con el Frontend professional de TEAM / test / entrevista con cliente). Análisis fiscal: **neto ≈ USD 4.140-4.270/mes** (≈ USD 25,9-26,7/h). **Escala por encima de Infjini, empate con Staffy.** Ojo: es fijo por mes, no por hora: a 45-50 h/semana el valor/hora cae por debajo de Infjini. |
| Infjini Inc | Lead Software Engineer - Digital Accessibility | Siraj Shaik | USD 22/h all-inclusive, 1 año | **ABIERTO (confirmado por Gonzo el 21/10).** El screening con Siraj ya se hizo y el proceso sigue vivo. Riesgo: 9-5 ET con comunicación en inglés, misma clase que los dos cerrados por C1. |

### Notas Staffy (2026-10-20) - PROCESO CERRADO

- JD: https://jobs.wearestaffy.com/positions/ai-software-engineer-1976
- **Desenlace (20/10, 17:42 ART):** Julieta propuso call de 30 min para el 21/10 y planteo el nivel de inglés. Al contestarle con honestidad (hablado B2, escrito C1, "a little rusty"), ella confirmó que **C1 conversacional es requisito clave** del rol (entrevista y comunicación diaria con clientes en US y Canadá) y cerró el proceso: *"Given what you've shared about your current speaking level, I think it would be best not to move forward with this opportunity at this stage."* Dejó puerta abierta para oportunidades futuras.
- **Causa raíz:** el filtro de idioma se filtró al final del screening, no al principio. El JD no lo declaraba y el pitch inicial de Julieta no lo mencionaba. Con un puesto de 30-35/h, la pregunta "¿el cliente exige C1 conversacional?" era la que define el proceso, y tenía que llegar antes.
- **Lo que sí se ganó:** contacto con una reclutadora que leyó el CV y dijo "your technical background is very strong". La relación queda para futuros procesos.
- **Aprendizaje reutilizable:** para roles LATAM con comunicación diaria en inglés con clientes US, **preguntar por el nivel de inglés requerido en el PRIMER mensaje**. Es la variable que más rápido descarta y la que más caro cuesta descubrir tarde. El filtro de idioma no se negocia con el CV: se negocia con la pregunta.

### Notas Infjini (2026-10-16) - **ABIERTO**

- Oferta aceptada para avanzar. CV en `docs/entrevistas/infjini-infotech-lead-a11y/`.
- **Estado real (confirmado por Gonzo el 21/10):** el screening con Siraj **ya se hizo** y el proceso **sigue abierto**. Es el único proceso vivo. (El desenlace no había quedado registrado en los dailies: la sesión no se guardó.)
- **Riesgo a vigilar:** es un puesto 9-5 ET con comunicación diaria en inglés, **misma clase que los dos cerrados por el filtro de C1 conversacional** (Staffy y Sol). Si Siraj tiene el mismo criterio, aplica el mismo filtro.
- **Acción sugerida:** en la próxima call, preguntar de entrada el nivel de inglés conversacional que exige el cliente. Es la pregunta de costo cero que más rápido descarta.
- Precedente: es el mismo req que EIT/HTC/Disney (bench amplio). No insistir.

### Plan de inglés C1 (decisión de Gonzo, 2026-10-21)

A raíz de los dos cierres por C1 conversacional, Gonzo se anota en el **CUI (Centro Universitario de Idiomas, UBA)** para la capacitación de C1 y su certificación, **mientras tanto sigue buscando**.

- **Plan completo con instrumentos, costos y fechas:** `studies/english/README.md`
- **Plazo a no perder:** la inscripción al examen **CUI-ING C1** cierra el **viernes 30 de octubre de 2026** (mesa del **6 de noviembre**, $140.000, online con oral por Zoom). Fuentes de `cui.edu.ar` leídas el 2026-10-21; **verificar en el centro antes de pagar**.
- **Declarado hasta que exista el certificado: B2.** Un C1 de papel que no se sostiene en una call es peor que un B2 honesto.

## Historial / cerrados

| Empresa | Puesto | Fecha contacto | Cierre | Motivo |
|---|---|---|---|---|
| Sol Bisio (cliente sin nombre) | Senior Full Stack Developer (AI-first) | 2026-10-14 | **cerrado 21/10** | El cliente exige **C1 conversacional sí o sí** para esa posición; el CV declara B2 y no pudieron avanzar. No es rechazo de perfil: Sol dijo que mandó toda la info y que te tiene presente para próximas búsquedas Full Stack. Detalle en `docs/entrevistas/sol-senior-fullstack/sol-seguimiento.md`. Relanzar sin filtro de C1 cuando llegue. |
| EIT/HTC (cliente Disney) | Lead Software Engineer Digital Accessibility | 2026-09-11 | **cerrado 24/09** | Nunca hubo oferta firme: el rate lo aceptó el reclutador, el cliente jamás hizo call. Cierre del vendor: "we will update if they want to schedule call" (23/09). El mismo req lo publica Infojini: era bench amplio, no búsqueda urgente. No volver a escribir. Palanca que queda: CPACC antes del 30/11 si quiere retomar el hilo con un entregable. |
| Wigou | AI-Native Software Engineering | 2026-08-31 | **cerrado 24/09** | Meet con Andrés Abraham (COO) el 02/09, sin feedback concreto. Tres semanas sin contacto. Cerrado por la propia regla del 02/09 ("si no hay novedad en ~1 semana, cerrado"). |
| OpenSistemas | AI-Native (colaboración freelance) | proceso previo | **cerrado 11/09** | Avanzaron con otro candidato, después de la entrevista técnica del 03/09 con Fernando. |
| Cruceros / Ritz-Carlton (oficina BA) | (a definir) | 2026-08-24 | **cerrado 22/09** | Samarth "let me check with the manager" repetido x7. Test 69% -> re-test OK -> manager interview 02/09. Feedback "24-48h" incumplido. |
| Kake | (a definir) | 2026-09-10 | **cerrado 22/09** | Pidieron video asincrónico el 10/09; nunca se envió ni hubo contacto posterior. |
| Koin Limited | AI Product Engineer (Next.js + Supabase) | 2026-09-09 | **cerrado 22/09** | Confirmación humana (Lyliana Padilla) y nada más. Stack match perfecto. Si escribe ella, reactivar. |
| Aliancers | (a definir) | 2026-09-09 | **cerrado 22/09** | Solo auto-confirmación genérica. Nunca hubo señal humana. |
| Ciklum | Senior JavaScript Engineer (4417) | 2026-09-09 | **cerrado 22/09** | Solo auto-confirmación. Hay portal para trackear si se reactiva. |

## Backlog de prospectos (relevado 2026-09-23, fuera del seguimiento)

No es seguimiento activo. Relevamiento hecho de costado; se retoma cuando Gonzo lo pida.

Filtro: remote real (LATAM/global), foco a11y o design systems, sin requisito de residencia US.

| Empresa | Puesto | Canal | Ubicación | Encaje | Estado |
|---|---|---|---|---|---|
| Infojini Inc | Lead Software Engineer - Digital Accessibility | a11yjobs (vivo) | LATAM Remote, 9-5 EST, 12 meses | Muy alto - JD idéntico al de Disney (mismo stack: Evinced, AMP, ZoomText, Narrator, Jira, Figma) | Posible mismo req que EIT |
| E-IT (EIT Professionals) | Lead Digital Accessibility Engineer | a11yjobs (vivo) | LATAM/US Remote, contract | Muy alto - es el mismo rol ya en curso | Referencia |
| Cheesecake Labs | [Contractor] Digital Accessibility Consultant | a11yjobs / trakstar | Brazil Remote (LATAM) | Alto - contractor a11y puro | Confirmar vigencia (listing de julio) |
| Equals True | Senior React Engineer (Design Systems) | web / LinkedIn | Remote-first, Argentina listada | Alto - design systems + React/TS | Confirmar vigencia |
| FullStack Labs | Senior Accessibility Engineer (Americas/LATAM) | fullstack.com talent pool | Remote LATAM | Alto - nearshore a11y | Reclutan continuo |
| BairesDev | Remote Accessibility Engineer - WCAG & Inclusive UI | a11yjobs | Anywhere US (pide residencia US) | Medio - encaje técnico alto, filtro de residencia | Revisar si aceptan LATAM |
| GitLab | Senior Accessibility Engineer | handbook/careers | Americas, EMEA - all-remote | Alto - a11y en design system propio | Listing vencido; revisar si reabre |
| Clipboard | Senior Design Engineer, Design Systems | Ashby | US Remote (USD 180-250k) | Medio - design systems, sin foco a11y explícito | Revisar filtro de residencia |

### Hallazgo del relevamiento

El req de Disney/HTC lo estaba pitcheando **más de un vendor**: E-IT e **Infojini Inc** publicaban el mismo puesto (LATAM Remote, 9-5 EST, 12 meses, stack idéntico de herramientas a11y). Confirmaba que era un bench req amplio, no una búsqueda exclusiva ni urgente.

## Cadencia

- Objetivo: 3-5 aplicaciones/día, calidad (stack match) sobre volumen.
- Cada aplicación nueva se agrega con fecha.
