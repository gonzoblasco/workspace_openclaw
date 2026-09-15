# Plan de Seguimiento - EIT / HTC Global / Disney (Lead Software Engineer, Digital Accessibility)

**Fecha:** 2026-09-11
**Estado:** RESPUESTA RECIBIDA (15:34) - rate USD 4.000/mes, contractor independiente para EIT USA (sin visa, ciudadania argentina OK). **DECISION DE GONZO (15:43): ACEPTAR los USD 4.000. No se contraoferta.** Contexto declarado por el: situacion economica urgente ("estoy desesperado"). Pendiente: mandar aceptacion + preguntar estructura.

---

## Contexto

- **Quien escribe:** Parthasarathy Ebenezer (EIT Professionals / E-IT) - mensaje directo, primer contacto.
- **Rol:** Lead Software Engineer (Digital Accessibility).
- **Hire-type:** Contract.
- **Location:** Remote.
- **Client (declarado):** HTC Global.
- **Horario:** 9 AM a 5 PM EST. Con EDT (sep) eso es 10 AM a 6 PM Argentina. Compatible.

## La cadena real (vendedor apilado)

El JD huele a Disney de punta a punta:
- "Hyperion y Vista" design systems (Hyperion = design system de Disney).
- "RA Design Systems", "DXT" (Disney Experiences Technology), "Guest and Employee facing applications".
- "Regulatory Testing of legacy Guest and Employee facing applications".
- "Prior Disney experience is nice to have".

**Cadena:** Disney (cliente final) -> HTC Global (prime / supplier) -> EIT Professionals (sub-vendor) -> Gonzo.

HTC Global Services: IT services, HQ Troy MI (US), ~1650 empleados US, fundada 1990, fuerte en sponsorship H-1B (dato publico: filings LCA en htcinc.com). Body-shop / C2C clasico.
EIT (E-IT Professionals Corp): staffing, Livonia MI, fundada 1999, ~56-179 empleados segun fuente. Sub-vendor que busca candidatos.

**Implicancia:** cada capa come margen. El rate que llega al contractor esta comprimido por 2 intermediarios.

## Fit real contra el JD (corregido 2026-09-11 tras correccion de Gonzo)

| Requisito | Estado |
|---|---|
| Min 6 anos de Digital Accessibility Engineering en **enterprise** | **CUMPLE.** ~8+ anos con a11y continua desde 2016, con **~5 anos donde a11y fue la funcion central**: Super7ui (~1 ano dedicado: 200+ fixes con screen readers) + EY (~3.7 anos enterprise: 50+ componentes a WCAG como referente). |
| **Certificacion** (required en el JD: "Relevant regional certification" - vago) / IAAP (preferred) | **PARCIAL.** No tiene IAAP (CPWA/WAS/CPACC) - esta en Preferred, no Required. **SI tiene Deque University Accessibility Specialist Program (2021)**, que puede entrar como la "regional certification" del required. Verificar. |
| JAWS, VoiceOver, NVDA, Narrator, ZoomText | **MAYORIA CUMPLE.** JAWS (uso real, no esta en el CV - agregar), VoiceOver, NVDA, TalkBack. Narrator/ZoomText: no confirmado. |
| HTML, CSS, JS, WAI-ARIA expert | Fuerte. Es su terreno. |
| Figma + plugins de a11y, anotaciones | **CUMPLE (confirmado por Gonzo 15:56).** |
| Axe, Lighthouse, ACR reporting (Evinced, AMP) | Axe/Axe DevTools si (confirmado). Lighthouse si. Evinced/AMP: no confirmado. |
| 3+ anos matrixed / SDLC en paralelo | **CUMPLE (confirmado).** Equipo cross-regional US/India en EY, agile squads. |
| Jira (defectos + priorizacion) | **CUMPLE (confirmado por Gonzo 15:56).** |
| Certificacion de entrenamiento tecnico (ADS, Design, Agile, QE) | **CUMPLE.** Deque University (5 cursos, 2021). |
| Full stack (React/TS) + a11y como especializacion activa | Su diferencial real. |

## Preguntas bloqueantes (resolver ANTES de invertir tiempo)

1. **Rate**: no lo dicen. ~~En contratos C2C Disney via 2 capas suele rondar USD 60-95/hr.~~ **RESPONDIDO (15:34): USD 4.000/mes.**
2. **Work authorization**: ~~los contratos de este tipo suelen exigir US work auth.~~ **RESPONDIDO: contractor independiente para EIT Professionals (empresa US). Sin visa. Ciudadania argentina OK.**

## UPDATE 2026-09-11 15:34 - Respuestas de Parthasarathy

> * Rate: $4000 USD per month
> * Contractor independiente para EIT Professionals (US company). No visa needed. Argentina citizenship is fine.

### Analisis del rate

**USD 4.000/mes = USD 48.000/ano (~USD 23/hr a 40h/semana).**

| Benchmark | Annual |
|---|---|
| **Esta oferta** | **$48k** |
| EY Argentina (historico, senior) | $36k |
| EY Global via LTM (28/hr, rechazado) | $58k |
| Su target para US/global | $85k-$105k |

**Lectura:** es BAJO para el titulo (Lead Software Engineer, cliente Disney enterprise). Pero esta ARRIBA de su piso local (EY Argentina $36k). En el medio: no es la oportunidad que el perfil merece, pero es ingreso real y remoto sin visa.

**Ojo con la cadena:** Disney -> HTC -> EIT -> Gonzo. EIT probablemente factura a HTC $70-90/hr; los $4k/mes dejan mucho margen. Hay lugar probable para contraofertar.

### Riesgos

1. **Certificacion IAAP (required en el JD):** sigue sin resolver. Si es gate real, el proceso se cae mas adelante.
2. **Compromiso full-time (9-5 EST = 10-18 Argentina):** conflictua con los otros procesos abiertos (reconsideracion OpenSistemas, etc.).
3. **Contractor 1099:** sin beneficios, sin estabilidad, facturacion US (W-8BEN).
4. **Dos intermediarios:** el rate llega comprimido por 2 capas.

### Proximo paso

1. **Contraoferta recomendada: USD 5.500/mes** (o $5k como piso aceptable). Justificar con: titulo Lead, 8+ anos, 1 ano dedicado a a11y (Super7ui), 4 anos enterprise (EY), screen readers incluido JAWS, PRs mergeados en design systems OSS.
2. **Preguntas de estructura:** horas (40h fijas o "hasta"), duracion, terminos de pago, si la certificacion IAAP es gate real.

### UPDATE 15:50 - Detalles operativos confirmados por Parthasarathy

> * 40 hours/week, yes; **no work on US holidays**.
> * **Start date: 1 de octubre.**
> * **Pago: biweekly** (quincenal). Contrato, W-8BEN y certificaciones "se discuten con el payroll team en una etapa posterior".

**Estado:** oferta efectivamente en firme. Arranque 01/10. Pendiente: confirmar aceptacion final + papeleo.

### Lectura de los detalles

- **40h/semana + 9-5 EST (10-18 Argentina):** es full-time real. Ocupa la jornada entera. Quedan los US holidays libres (Columbus Day 12/10, Thanksgiving, Navidad, etc.) - unos 10-11 dias en el ano.
- **Arranque 01/10:** ~3 semanas desde hoy.
- **Biweekly - ojo con la aritmetica:** si son 26 pagos por ano, cada uno es **USD 1.846,15** (~$48k/ano). Si son 2 pagos por mes (24/ano), cada uno es **USD 2.000**. Da lo mismo al ano, pero no al flujo mensual. Conviene confirmarlo: es una linea, no una negociacion.
- **"Certificaciones se discuten con payroll mas adelante":** esquiva la pregunta del gate IAAP. No la filtran ahora, pero tampoco la descartan. **Riesgo residual:** puede aparecer tarde, cuando ya haya invertido tiempo. Queda registrado como pendiente a vigilar.

### Analisis del rate (final, con decision de Gonzo)

**USD 4.000/mes = USD 48.000/ano (~USD 23/hr a 40h/semana).**

| Benchmark | Annual |
|---|---|
| **Esta oferta (Aceptada)** | **$48k** |
| EY Argentina (historico, senior) | $36k |
| EY Global via LTM (28/hr, rechazado) | $58k |
| Su target para US/global | $85k-$105k |

**Decision de Gonzo (15:43): ACEPTAR. No contraofertar** (necesidad economica inmediata). La contraoferta a $5.500 queda descartada por decision suya - no insistir.

**Principio activo:** velocidad sobre optimizacion de rate.

### Riesgos abiertos

1. **Certificacion IAAP:** esquiva, no resuelta. Vigilar cuando llegue el payroll team.
2. **Full-time desde 01/10:** conflictua con la reconsideracion de OpenSistemas y cualquier otro proceso. Es exclusividad de facto.
3. **Contractor 1099:** sin beneficios, sin estabilidad, sin vacaciones pagas.
4. **Facturacion internacional:** W-8BEN, canal de cobro (Wise/Deel/wire) y su costo, e impuestos en Argentina (ingreso real a declarar).
5. **Dos intermediarios:** Disney -> HTC -> EIT -> Gonzo. El rate llega comprimido.

---

## Borrador final - Aceptacion + confirmacion de arranque

> Confirmed - October 1 works for me, and 40 hours a week is expected on my side.
>
> Two details to close before then:
> * Biweekly payment: is it $1,846 x 26 payments, or $2,000 twice a month?
> * What do you need from me now to get the contract moving - passport, bank details, W-8BEN?
>
> Happy to get the paperwork done ahead of time so day one is clean.
>
> Best,
> Gonzalo

**Por que asi:** confirma en una linea, pregunta solo lo que falta, y ofrece adelantar papeleo (= disponibilidad, no ansiedad). Sin preguntar por la certificacion todavia: eso lo pone el payroll team cuando toque, y preguntarlo ahora suena a que le falta algo.

---

### UPDATE 15:54 - Segunda difusion del MISMO puesto (otro reclutador de E-IT)

Llego el mismo JD por **Naveen Raj** (Talent Acquisition, E-IT Professionals Corp). Comparacion contra el original de Parthasarathy:

| Item | Parthasarathy (15:18) | Naveen (15:54) |
|---|---|---|
| Titulo | Lead Software Engineer (Digital Accessibility) | **identico** |
| Hire-type | Contract | **identico** |
| Location | Remote | **Remote (LATAM)** - ahora explicito |
| Horario | 9 AM - 5 PM EST | **identico** |
| Required Quals | lista completa | **identica palabra por palabra**, incluido "Relevant regional certification" y "Prior Disney experience is nice to have" |
| Preferred Quals | IAAP, Deque/Level Access, Flutter SDUI, ITIL | **identicos** |
| Narrativa interna | "About The Role & Team" con DXT, RA Design Systems (Hyperion y Vista), Guest and Employee facing apps | **no aparece** |
| Educacion | Required + Preferred | **no aparece** |

**Conclusion: es el MISMO puesto.** Mismo titulo, mismas required quals palabra por palabra, misma senal de cliente (Disney), mismo vendor (E-IT). La version de Naveen es la version "outbound": pelada de la narrativa interna (DXT/Hyperion/Vista son detalles que no se publican) y con LATAM explicito.

**Correccion:** el requerimiento dice **"Relevant regional certification"** (vago), no "IAAP". IAAP (CPWA/WAS/CPACC) esta en **Preferred**. El gate puede ser mas blando de lo que asumi.

**Riesgo:** doble sumision. Dos reclutadores del mismo vendor (E-IT) trabajando el mismo req. Si se postula por los dos, puede quedar duplicado en el sistema del vendor.

**Accion recomendada:** no responder como prospecto nuevo. Decirle a Naveen que ya esta en proceso con Parthasarathy por este mismo rol, y pedir que se coordinen. Una sola conversacion, limpia.

---


### UPDATE 16:05 - CV a11y enviado + respuesta a Naveen

- **CV a11y enviado a Parthasarathy** (PDF: `docs/entrevistas/Gonzalo_Blasco_Lead_Digital_Accessibility_Resume.pdf`). Merge de sus 3 CVs, adaptado al JD. Cobertura de keywords 41% -> 94,1%.
- **Naveen Raj respondido (16:06):** avisado de que ya esta en proceso con Parthasarathy. **Respuesta de Naveen (16:09):** "okay thank you / he is my team lead only, You can continue with him." -> **sin conflicto.** Parthasarathy es el team lead de Naveen; se sigue con el. No hay doble sumision.
- **Hallazgo importante:** Gonzo tiene **Deque University Accessibility Specialist Program (2021)** (5 cursos). El JD pide "relevant regional certification" en Required; IAAP esta en Preferred. Puede cubrir el requisito sin IAAP - mencionado en el CV.
- **Estado:** esperando novedades de Parthasarathy. Arranque acordado 01/10.

---


## Borrador 1 DESCARTADO - Contraoferta a USD 5.500

No se envia (decision de Gonzo: no pelear). Se conserva solo como referencia historica.

## Borrador 2 DESCARTADO

> Hi Parthasarathy,
>
> Thanks for the quick answers - both work for me.
>
> On the rate: $4,000/month comes out to roughly $23/hour for a role that asks for a Lead Software Engineer with 6+ years of digital accessibility engineering. I am 8+ years in, with a full year dedicated to accessibility at Super7ui (200+ fixes tested with screen readers, including JAWS) and 4 years at EY as the accessibility reference for the team (50+ enterprise components remediated to WCAG), plus accessibility PRs merged in large open source design systems.
>
> I can move forward at $5,500/month. If the budget is fixed, tell me and we can look at how the contract is structured.
>
> A few things I need to plan properly:
>
> 1. Is this a fixed 40 hours/week, and what is the expected contract duration?
> 2. Is a specific accessibility certification required for this placement, or is demonstrated enterprise experience accepted?
> 3. Payment terms (monthly invoicing, W-8BEN).
>
> Once I have those, I can confirm quickly.
>
> Best,
> Gonzalo

## Borrador 2 - Aceptar el rate y solo preguntar estructura

Mismo cuerpo, sin el parrafo de contraoferta: arrancar con "Thanks - that works for me." y pasar directo a las 3 preguntas.

**Pendiente:** decision de Gonzo. Escanear guiones con `scripts/check_em_dash.py` antes de enviar.

## Proximo paso

Responder con interes + las 2 preguntas bloqueantes. Liderar con la fuerza real: 8+ anos de desarrollo con a11y continua desde 2016, incluyendo 1 ano dedicado a accesibilidad en Super7ui y 4 anos enterprise en EY, JAWS + screen readers. No mencionar la falta de certificado en el primer mensaje (aunque sea required en el JD) - primero cerrar rate y work auth.

---

## Borrador de respuesta (English - el proceso es en ingles)

> Hi Parthasarathy,
>
> Thanks for reaching out - this one caught my attention. Digital accessibility is exactly where I focus, and the CoE scope (shift-left, WCAG 2.2 A/AA, design review, in-sprint developer support) is the kind of work I want to be doing.
>
> Two things I need before we go deeper:
>
> 1. What is the rate range for this contract?
> 2. Can EIT engage a contractor based in Argentina, or does HTC require US work authorization? I work 100% remote and can align with EST core hours.
>
> On fit: I am a full stack engineer (React/TypeScript) with 8+ years of experience and accessibility as a continuous thread since 2016. I spent a full year dedicated to accessibility at Super7ui (200+ fixes tested with screen readers, including JAWS), and 4 years at EY as the accessibility reference for the team, where I audited and remediated 50+ components of an enterprise library to WCAG. I also have accessibility PRs merged in large open source design systems, with the reviewer iteration and browser tests to back them.
>
> Send me the details and I will get you what you need.
>
> Best,
> Gonzalo

**Pendiente:** validar con Gonzo antes de enviar. Escanear guiones con `scripts/check_em_dash.py`.

---

## UPDATE 2026-09-14 11:29-11:56 - Retailoring del CV para el JD (pedido de reclutadores)

**Pedido de Gonzo:** los reclutadores de Disney pidieron agregar skills al CV para matchear el JD.

**Base:** el CV que se envio el 11/09 para este mismo proceso (`Gonzalo_Blasco_Lead_Digital_Accessibility_Resume.pdf` + `eit-cv-gonzalo-blasco-a11y.md`), no un CV generico.

**Entregable:** `docs/entrevistas/Gonzalo_Blasco_Lead_Software_Engineer_Digital_Accessibility.docx` (13 KB, formato original del DOCX intacto - misma tipografia/colores, single-column, sin tablas, sin header/footer, sin em/en dash). Gonzo pidio explicitamente Word (no PDF).

### Cobertura de keywords

| Metrica | Antes | Ahora |
|---|---|---|
| Cobertura total | - | **95%** (19/20) |
| Hard skills | - | 92% (11/12) |
| Soft skills | - | 100% (5/5) |
| Domain/Industry | - | 100% (3/3) |

Unico gap: **Flutter/SDUI** (Preferred, no Required). No se agrego por falta de evidencia real.

### Cambios aplicados (todos verificados con Gonzo antes de escribir)

| Cambio | Motivo |
|---|---|
| `roughly 5 years` -> `6+ years in enterprise digital accessibility engineering` | El JD pide minimo 6 anos. Defendible con las fechas propias (a11y continua desde 2016, foco enterprise desde Super7UI). Confirmado por Gonzo. |
| `CORE COMPETENCIES` -> `SKILLS` | Heading estandar que buscan los ATS + el JD usa "skills". |
| Sumo **Narrator** y **ZoomText** a AT | Estaban en el JD. Confirmado por Gonzo que los uso. |
| **Axe DevTools** explicito + **ACR** escrito entero + axe-core/Lighthouse | El JD busca los nombres exactos de las tools y el acronimo. Confirmado por Gonzo. |
| Sumo **EAA y ACA** a estandares | Requisito blando del JD, ya presentes de forma implicita. |
| Nueva linea **Delivery and stakeholder management** | El JD lista colaboracion, comunicacion con stakeholders y multiples SDLC en paralelo. |
| EY: suma `Axe DevTools, Lighthouse, JAWS y NVDA` | Conecta la experiencia concreta con las tools del JD. |

### Decisiones y correcciones de Gonzo en esta sesion

1. **Sin PDF:** "no pdf, necesito un word". Solo DOCX.
2. **Sin seccion EDUCACION:** "quite educacion... no aporta literalmente nada". Se agrego en la primera version y Gonzo la hizo sacar. El CV final NO tiene seccion EDUCATION (ni Digital House ni UADE).
3. **No se toco:** Flutter/SDUI (sin evidencia), Evinced (no confirmado), AMP (no confirmado), IAAP (no la tiene - Deque University cubre la "relevant regional certification" del Required).

### Riesgo residual (sin cambios)

La certificacion **IAAP** sigue en Preferred, no Required. Si el payroll team la pone como gate mas adelante, el proceso puede complicarse. Deque University Accessibility Specialist (2021) es el argumento actual. **Vigilar.**

### Secciones finales del CV

PROFESSIONAL SUMMARY | SKILLS | PROFESSIONAL EXPERIENCE | CERTIFICATIONS | SELECTED PROJECTS | OSS PARTICIPATIONS (Merged PRs + Contributions)

## 2026-09-15 (12:22-13:33) - IAAP certification: respuesta al cliente + plan de estudio

**Disparador:** el cliente pregunto por (1) certificaciones y CEUs mas recientes, (2) si hay plan de rendir IAAP, (3) para cuando la completa. Envia Parthasarathy, responde Gonzo.

### Hechos verificados contra el handbook oficial de IAAP (Candidate and Certificant Handbook, enero 2026)
- Examenes en **6 ventanas por ano**, rendicion online proctored o test center.
- Credenciales validas **3 anos**; renovacion **sin costo con membresia IAAP activa** (renovacion con fee si no hay membresia continua).
- CEUs por ciclo trienal: CPACC 45, WAS 35, CPWA 55, ADS 35.
- Fee del examen: USD 385-545 segun credencial/membresia (fuente de terceros, confirmar en portal).

### Entregable: `iaap-certification-email-draft.md`
Email en ingles (subject "IAAP Certification - Status and Plan"), verificado sin em/en dash con `scripts/check_em_dash.py`. Estrategia:
1. **Punto 1 (certificaciones):** Deque University Accessibility Specialist (2021) descrito con precision - son certificados de cursos, no una credencial IAAP vencida. Mata el "lapsed" con exactitud; el curso "IAAP Certification Quick Guide (04/2021)" queda como evidencia de prep previa hacia IAAP. Ademas: educacion continua aplicada (referente a11y en EY hasta 05/2025, contribuciones OSS mergeadas en 2026, estudio estructurado WCAG 2.2 / APG / lectores).
2. **Punto 2 (plan IAAP):** si, CPACC primero + WAS segundo (credencial natural de profundidad tecnica).
3. **Punto 3 (timeline):** registro el 01/10 al arrancar; completar ~1 mes desde el arranque (fin de octubre), rendiendo la ventana IAAP mas temprana disponible; fecha exacta se confirma al registrar. Fee: "if the client or HTC is able to sponsor or reimburse it, I will register immediately" - positivo, sin mencionar dinero en tono negativo (cumple lo que pidio Parthasarathy).
4. Cierra ofreciendo compartir los certificados Deque y documentacion.

### Plan de estudio (pedido de Gonzo, 13:33)
- **Recomendado:** Deque University IAAP CPACC prep (video + practica, self-paced; curriculum completo USD 400/ano, incluye contenido de prep para WAS). Ya conoce la plataforma (5 cursos Deque en 2021).
- **Alternativa economica:** Level Access Academy IAAP Bundle, USD 249/ano, 12 meses, incluye 18.25 creditos CEU (mitad de un ciclo de renovacion).
- **Obligatorio gratis:** CPACC Body of Knowledge (oct 2023, v4.0) - fuente del examen. Princeton CPACC prep course gratis para miembros IAAP (beneficio extra si el cliente sponsoriza membresia).
- **Focos de estudio de Gonzo (perfil dev):** (1) leyes y regulaciones (ADA, Section 508, AODA, EN 301 549); (2) datos de discapacidad (OMS) y modelos de discapacidad (medico vs social), 7 principios de universal design; (3) estructura y terminologia WCAG (niveles A/AA/AAA, documento: principles -> guidelines -> SC -> techniques).
- Con la base de Gonzo (5 anos a11y central), 4 semanas de preparacion es holgado; el riesgo es solo calendario de ventanas.

### Estado
- Email entregado, **pendiente de revision/aprobacion de Gonzo** antes de enviar.
- Si el cliente sponsoriza: pedir examen + membresia IAAP + curso en un mismo paquete (renovable gratis de por vida = argumento facil de vender).
- **Riesgo IAAP (Preferred) ahora mitigado activamente** con el plan; seguir vigilando si payroll lo pone como gate.
