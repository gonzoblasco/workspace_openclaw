<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# TEAM International × tempo.io - Senior Frontend Developer (Growth)

**Proceso abierto desde el 21/10/2026.** Contacto: David Sanin Valencia (TEAM International) por LinkedIn.

Carpeta de trabajo del proceso. Índice:

| Archivo | Qué es | Estado |
|---|---|---|
| `analisis-fiscal-neto.md` | Cuánto valen realmente USD 5.000/mes brutos en Argentina como contractor (monotributo, Factura E, costos no cubiertos) | Hecho y verificado contra fuentes oficiales (21/10/2026) |
| `revision-adversarial.md` | Encaje JD↔corpus, hallazgos por severidad, veredicto accionable y texto para la call | Hecho (con correcciones del CORE) |
| `producto-y-rol-growth.md` | Qué es Tempo hoy, qué hace un Frontend Dev (Growth), stack probable, preguntas esperadas y para qué hacer | Hecho (investigación con fuentes, 21/10/2026) |
| `prep-tecnica-growth.md` | Prep técnica: 13 preguntas con respuesta en inglés, historia de A/B testing, argumento transferible, 30/60/90, checklist | Hecho (revisado por el CORE) |
| `cv-senior-frontend-growth-gonzalo-blasco.md` (+ `.pdf`) | CV en inglés, una página, orientado al JD | **ENVIADO 21/10.** Markdown + PDF + `cv-style.css` reusable |
| `guion-call-21-10.md` | Texto listo para enviar a David y las 4 preguntas de la call | Hecho - **aún no enviado** (el CV fue primero, por decisión de Gonzo) |

---

## Estado: entrevista agendada

- **21/10, 13:3x** - Gonzo envió el **CV de una página tal cual** (decisión propia: "ya veremos qué respuesta tiene").
- **21/10, 14:14** - **Entrevista agendada: lunes 26/10/2026, 10:00 ART** (= 09:00 EST, en horario de US). David se había desconectado tras el envío; el CV fue lo que reabrió el proceso.
- **Sin confirmar qué paso del proceso es** (call informativa con David / entrevista con el Frontend professional de TEAM / test / entrevista con cliente).

### Tres hallazgos de la investigación que cambian la preparación

1. **El aviso público del puesto NO menciona A/B testing, feature flags ni analytics.** Dice: *"develop some of our flagship products - Tempo Timesheets, Capacity Planner and Financial Manager for Jira Cloud"*, con requisitos genéricos de TS+React. O el JD que te pasó TEAM es una versión ampliada, o es otro req con el mismo título (Tempo postea el mismo rol en varias geos). **Llevá tu JD impreso y preguntá cuál es la versión vigente.**
2. **El CSP de Forge bloquea los SDKs de analytics en el frontend.** Las apps corren en iframe y la CSP por defecto no permite scripts de orígenes externos (Google Analytics, Sentry): los eventos tienen que salir por `invoke()` al backend, con egress permissions declaradas. **Instrumentar no es copy-paste: es diseñar el pipeline de eventos.** Confirmado en docs de Atlassian. Es la pregunta de poder: muy pocos candidatos pueden hacerla.
3. **El growth de Tempo es "seat utilization" dentro de la instancia de Jira del cliente**, no adquisición de usuarios: la licencia se ata al tamaño de la licencia de Jira. La métrica que mueve el negocio es cuántos asientos usan y cuántos módulos se adjuntan.

### Si David pide la call informativa

El guion de `guion-call-21-10.md` tiene las 4 preguntas (idioma por la operación, alcance del contrato, PTO, educational allowance). La del idioma va apoyada en el "B2+ in the JD" y **no** pregunta "¿exige C1?" - preguntar eso es el auto-sabotaje del caso Staffy.

### Cosas que NO quedaron confirmadas

- **El inicio del curso del CUI:** depende de la prueba de nivel del 21/10. Hay ciclos que arrancan el 26/10 (inscripción 7-22/10) y otros en noviembre (inscripción 5-19/11). El guion a David dice "this month", sin fecha.
- **Qué herramientas de analytics y feature flags usan en Tempo:** cero evidencia pública. Preguntalo, no lo supongas.


---

## Ficha de la oferta

| Dato | Valor | Fuente |
|---|---|---|
| Empresa | TEAM International (IT consulting, HQ Lake Mary FL, fundada 2020, 1000+ empleados; oficinas en Colombia, Poland, Ukraine) | teaminternational.com |
| Cliente | tempo.io - "Portfolio Management Software for the AI Enterprise", gestión de portfolios para Jira, sede US, SOC 2 Type II, ISO/IEC 27001, GDPR, +20 años en el mercado | tempo.io (verificado 21/10/2026) |
| Puesto | Senior Frontend Developer (Growth) | JD |
| Ubicación | "Colombia;Argentina" | JD |
| Salario | **USD 5.000/mes brutos** (≈ USD 31,25/h a 160 h) | Mensaje de David |
| Modalidad | Full-time contractor indefinite, L-V, remoto | Mensaje de David |
| Beneficios | Health insurance USD 89/mes (desde mes 3, reembolsable contra factura, eligiendo aseguradora), hobbies USD 22/mes, comunicaciones USD 15/mes desde el mes 1, educational allowance USD 400/año (desde mes 3, con aprobación de HR y cláusula de permanencia de 12 meses si supera el 65%), PTO 20 días el primer año (prorrateado) / 21 / 22 / 23, medio día en el cumpleaños, licencia por enfermedad grave (2 semanas), 5 días por fallecimiento de familiar, licencia por maternidad (2 meses) / paternidad (2 semanas) / adopción | Benefits Policy 2026 (5 págs) |
| Proceso | (1) call informativa 10-15 min con David · (2) entrevista con el profesional Frontend de TEAM · (3) test del cliente desde casa · (4) dos entrevistas con el cliente | Mensaje de David |

## Estado

- **21/10, 12:16** - David escribe por LinkedIn. Pitch: *"Sr Frontend Developer, English Advance. Payment in USD / Great Benefits."*
- **21/10, 12:21** - Gonzo responde: declara inglés upper-intermediate (B2), dice que se anota en un centro de idiomas para C1 + TOEFL, y que no quiere perder la oportunidad por eso. **Corrección 27/10: el nivel es B2+ (el CUI se lo corrigió el 27/10, tras un error de inscripción en B1+).**
- **21/10, 12:30** - David responde con el JD, la Benefits Policy, el salario, la modalidad y el proceso de 4 pasos. **No responde el nivel de inglés requerido.**
- **21/10, 12:33** - Gonzo: *"dale gracias. dame un rato que leo todo bien en detalle y te digo cómo seguiríamos? con respecto al nivel de inglés, es válido lo que te dije?"*. **Sin respuesta aún.**

---

## Lo que YA sabemos y cambia el análisis

1. **El JD pide `B2+`, no `C1`.** Esto lo distingue de Staffy (20/10) y Sol (21/10), que cerraron por exigencia de C1 conversacional. El filtro de idioma sigue siendo el riesgo #1, pero acá está *declarado* y es más bajo.
2. **El pitch de David decía "English Advance", que contradice el "B2+" del JD.** Alguien escribió "Advance" sin que el JD lo pida. Eso es exactamente el patrón que en Staffy y Sol se filtró tarde.
3. **Es el tercer proceso en 4 días con riesgo de idioma.** El costo de un tercer cierre por la misma causa ya se pagan solo.
4. **El neto real es ~USD 4.140-4.270/mes (≈ USD 25,9-26,7/h)**, no USD 5.000. Contra Infjini (USD 22/h all-inclusive) es una mejora clara; contra Staffy (USD 30-35/h) es un empate técnico, no una mejora.
5. **El riesgo no es la tarifa: son las horas.** Es fijo por mes, no por hora. A 45-50 h/semana el valor/hora cae a USD 21-22 netos, por debajo de Infjini.
6. **El núcleo del puesto es "Growth"** (experimentación, analytics, funnel, feature flags) y es donde el encaje es más débil: el corpus no tiene evidencia de analytics, instrumentación, feature flags ni análisis de funnel.

## Preguntas abiertas para Gonzo

- **~~A/B testing~~ - RESUELTO 21/10/2026.** Gonzo confirma que en 2019, en Minutentag, **trabajó
  con Adobe Target** corriendo experimentos sobre features y diseños en producción, en squads
  ágiles con diseño y producto. El hecho ya está en el corpus (`memory/career-facts.md` §2.4) y
  los 5 CVs que lo declaraban quedan respaldados. **Lo que NO está confirmado es el claim de
  haber construido la infraestructura de experimentación**: ese bullet ("Implemented A/B testing
  infrastructure powering data-driven product decisions") se sacó del markdown del CV de
  Infjini. No estaba en los DOCX/PDF que se mandaron, así que no salió a la calle.
  **Pendiente RESUELTO (27/10/2026):** los bullets "Architected and built micro frontend
  architecture serving 2M+ monthly active users" y "Developed shared component library used across
  5 product teams" no tienen respaldo. Gonzo aclaró que **la librería de componentes fue EY Motif,
  nunca Minutentag**. Salieron de todos los CVs y de los PDF/DOCX regenerados.
  (markdown del CV de Infjini, tampoco en los DOCX). El corpus dice *participó de la migración a
  React* y *mejoró un sitio con 2M+ usuarios mensuales*, sin atribuirle la arquitectura. Si no
  los confirma, salen del markdown.
- **Educación:** el JD exige *"Degree in Computer Science, Software Engineering, or related studies"*. El corpus dice que no hay título registrado; los CVs llevan Digital House + UADE Diseño Gráfico; el 14/10 Gonzo.validó "Universidad de Palermo - Ing. en Informática (2001-2002, dropped)". ¿Qué se declara acá?
