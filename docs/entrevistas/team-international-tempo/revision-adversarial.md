# Revisión Adversarial - Oferta Senior Frontend Developer (Growth) - Tempo.io

## 1️⃣ Tabla de encaje JD vs Corpus

| Requisito del JD | Veredicto | Evidencia / Comentario |
|------------------|-----------|------------------------|
| 5+ años de experiencia front‑end comercial | CUMPLE | “10+ años de desarrollo total (feb 2016‑hoy)” (memory/career-facts.md) |
| ≥1 año con TypeScript y React | CUMPLE | “Freelance (05/2025‑presente): React/Vite/TS…” y “EY: Senior Frontend Engineer, React” (memory/career-facts.md) |
| Título universitario en CS, Ingeniería o afín | NO CUMPLE | “no hay título universitario registrado”; formación: Digital House - React (2018) y Universidad de Palermo - Ing. en Informática (2001‑2002, incompleta) (memory/career-facts.md) |
| Conocimientos de fundamentos de CS (Big‑O, estructuras, algoritmos) | DATO NO VERIFICADO | No hay mención explícita en el corpus. |
| Dominio de TypeScript/JS/CSS3/HTML5 | CUMPLE | React/TS (Freelance) y React enterprise (EY) implican uso de JS/HTML/CSS (memory/career-facts.md) |
| Experiencia en UI compleja | CUMPLE | EY Motif: librería React con +50 componentes WCAG 2.2 AA (memory/career-facts.md) |
| Performance (optimización, métricas) | DATO NO VERIFICADO | No se menciona en el corpus. |
| Experiencia práctica con A/B testing o frameworks de experimentación | **DATO NO VERIFICADO** | El corpus no lo tiene. **No es "no cumple": es un hecho que no está registrado.** Existen 2 bullets de A/B testing en 4 CVs (§2, hallazgo crítico) que el corpus no contiene. Hay que resolver el origen con Gonzo antes de afirmarlo. |
| Instrumentación de analytics y análisis de funnel | **NO CUMPLE / DATO NO VERIFICADO** | Cero mención en el corpus (ni "analytics", ni "funnel", ni "instrumentación"). **Verdadero gap del corpus:** no hay nada que pueda afirmarse. Esto no se resuelve con una pregunta, se resuelve Contestando la pregunta en la entrevista. |
| Conocimiento profundo de onboarding, métricas de engagement y optimización de conversión | **NO CUMPLE / DATO NO VERIFICADO** | Cero mención en el corpus. Mismo caso que el anterior. |
| Inglés B2+ (upper‑intermediate) oral y escrito | CUMPLE | “Inglés: B2 (dato duro, NUNCA C1…)” (memory/career-facts.md) |
| Capacidad de explicar decisiones técnicas con claridad | DATO NO VERIFICADO | No está documentado. |
| Soft‑skills para comunicación multicultural | DATO NO VERIFICADO | No está documentado. |
| Autonomía y capacidad de trabajar sin especificación completa | DATO NO VERIFICADO | No está documentado. |
| Colaboración en la elaboración de especificaciones técnicas | DATO NO VERIFICADO | No está documentado. |

## 2️⃣ Hallazgos (severidad → detalle)

| Severidad | Hallazgo | Por qué importa | Evidencia | Acción concreta |
|-----------|----------|-----------------|-----------|-----------------|
| **CRÍTICO** | **Filtro de inglés** - El JD exige B2+, mientras el pitch de David menciona “English Advance” (implícito C1). En procesos previos (Staffy, Sol) el filtro oculto de C1 provocó cierre. Aquí el recruiter no cuestionó el nivel y no dio señal, aunque la entrevista inicial es corta (10‑15 min). Detectar este filtro temprano evita pérdida de tiempo y riesgo de cierre. | Si el cliente realmente requiere C1 y Gonzo sólo tiene B2, el proceso fallará en etapas posteriores. | JD: “Upper‑intermediate spoken and written English (B2+)”. Pitch: “English Advance”. Historial: cierres por C1 en Staffy y Sol. | Preguntar explícitamente el nivel de inglés requerido **antes** de la call de 10 min. |
| **CRÍTICO** | **Integridad del A/B testing** - Los bullets de A/B testing aparecen en 4 CVs y son **requisito nuclear de este JD** (el puesto es "Growth": A/B, multivariate, instrumentación de analytics, feature flags, funnel). El corpus `memory/career-facts.md` no los contiene, y el CV de agosto 2026 que originó el de Infjini tampoco los tenía. Agregados después de agosto 2026 por un camino que no pasó por el corpus. `check-cv-facts.py` no valida educación ni A/B: corre verde con 5 CVs y no ve nada. | Si el bullet no resiste una pregunta de fondo ("¿cómo definiste la métrica, cómo cortaste el test, qué resultado tuvo?"), se rompe en la entrevista - y el paso 3 es un test del cliente sobre justo esto. | Corpus sin "A/B", "Adobe Target", "analytics", "experiment", "funnel". Bullets presentes en Infjini, MercadoLibre, Sol y EIT/HTC. Ausentes en `memory/archive/sessions/2026-08-19-0951.md` (origen del CV de Infjini). | Preguntarle a Gonzo el origen (ver `guion-call-21-10.md` §A/B testing). Si es real: al corpus primero, al CV después. Si no: sale de los 4 CVs. **No mandes un CV con esos bullets sin resolverlo** - ni borrándolos a ciegas, ni declarándolos sin verificar. |
| **ALTO** | **Educación requerida** - El JD pide “Degree in Computer Science …”. El corpus indica ausencia de título universitario y solo estudios no pertenecientes a CS (Digital House, Diseño Gráfico) o incompletos (Universidad de Palermo). | El cliente podría descartar por falta de título. Pero ojo: “dropped” no es un degree, y este es el **primer** JD que pide título - en los anteriores Gonzo lo quitó porque "no aporta literalmente nada". | `memory/career-facts.md` §3/§11; CVs con EDUCACION: Digital House (2018) + UADE Diseño Gráfico (2003-2004); `memory/2026-10-14.md`: "Universidad de Palermo - Ing. en Informática (2001-2002, dropped); carrera validada por él". | **No decidirlo solo**: es una decisión de Gonzo y el corpus tiene datos que se contradicen. Preguntáselo (texto en `guion-call-21-10.md` §Educación). No preguntar en la call "¿aceptan bootcamp en vez de degree?" - eso te clasifica en la primera pantalla. |
| **ALTO** | **Falta de evidencia en Growth (A/B, analytics, feature‑flags, funnel)** - El núcleo del puesto (activation, retention, conversion; A/B y multivariate; instrumentación de analytics; feature flags) **no tiene respaldo en el corpus**. Lo único que podría afirmarse es el A/B de Minutentag con Adobe Target, y encima está en duda. | Si el test del cliente (paso 3) evalúa esas habilidades, Gonzo no tiene con qué responder. Esto no se arregla con un bullet: se arregla o aceptando el gap en la entrevista, o no postulando. | Cero menciones de "analytics", "feature flag", "funnel", "conversion", "retención", "activación" en `memory/career-facts.md` (verificado por grep). | Decidir **antes** de mandar el CV: ¿el gap es tolerable para este puesto? Si sí, llevarlo con una historia de cómo se aprende (la de "usar IA para trabajar mejor" ya funciona en entrevistas). Si no, el proceso no es para este puesto y conviene decirlo temprano. |
| **MEDIO** | **Desalineamiento entre pitch y JD (inglés)** - Pitch menciona “English Advance” (implicando C1) mientras JD acepta B2+. Puede crear confusión en el recruiter y generar una expectativa de nivel superior. | Confusión puede llevar a preguntar después y revelar que Gonzo sólo tiene B2, generando desconfianza. | Pitch de David vs JD. | Aclarar en la primera call que el nivel B2+ es suficiente según JD y preguntar confirmación. |
| **MEDIO** | **Riesgo contractual con TEAM vs Tempo** - La oferta es a través de TEAM International; beneficios y políticas de salud pueden cambiar según el contrato con Tempo. Si Tempo termina, el contractor pierde estabilidad. | Dependencia de terceros puede afectar continuidad laboral y beneficios. | Docs/entrevistas/team-international-tempo/analisis-fiscal-neto.md indica que salario neto es menor al bruto y depende de contrato. | Preguntar en la entrevista final quién será el punto de contacto para temas contractuales y garantías de continuidad. |
| **BAJO** | **Precedente de cierre por idioma en procesos recientes** - Dos procesos en los últimos días (Staffy, Sol) cerraron por requerimiento C1 aunque no estaba en el JD. | Indica patrón de filtro oculto que podría repetirse. | Historias de Staffy (30‑10) y Sol (21‑10). | Mantener la pregunta de nivel de inglés en la primera interacción para mitigar. |
| **BAJO** | **Salario neto vs expectativa** - El bruto de USD 5 000/mes equivale a neto ~USD 4 140‑4 270 como contractor en Argentina, lo que podría ser menos atractivo. | Impacta la decisión del candidato y la negociación salarial. | docs/entrevistas/team-international-tempo/analisis-fiscal-neto.md. | Presentar expectativa salarial neta en la negociación o considerar ajuste de tarifa. |

## 3️⃣ Veredicto Accionable

### (i) Qué hacer **antes** de la call de 10 min (texto en inglés listo para copiar/pegar)

> **Corrección del revisor (CORE):** la versión que propone el Critic - *"could you please confirm the
> required English proficiency… does the client require a conversational C1?"* - es exactamente el
> auto-sabotaje que este proceso tiene que evitar. Preguntar por C1 con esas palabras te clasifica
> como el candidato que se autoexcluye, y destruye la opción sin información a cambio. La pregunta
> tiene que ir por la **operación** (cuánto inglés hablado a diario) y apoyarse en el **JD**, que
> es el documento de ellos. Texto completo, justificación y alternativas: `guion-call-21-10.md` §1.

**Texto recomendado (voz de Gonzo - directa, sin rodeos):**

```
Thanks David, I read everything in detail - the role, the benefits and the process all look
solid, and the B2+ in the JD matches where I am right now.

A couple of things I want to nail down before we set up the call:

* For this role, is the spoken English requirement the B2+ mentioned in the JD, or is there a
  higher bar for the client interviews? I want to be upfront about my level rather than find
  out later.
* The role mentions working with Tempo's US team - how much of the day-to-day is spoken English
  with the client, versus async written work?

On my side: my written English is strong (documentation, code review, async work is where I am
most comfortable) and my spoken is solid B2 - upper intermediate. I am enrolling for C1 and
TOEFL this month.
```

**Justificación:**
- **No auto-sabotear**: ancla la pregunta en el "B2+ in the JD" - el documento de ellos - en vez de
  en tu declaración. Si el filtro real fuera C1, ellos se contradicen y tienen que decirlo.
- **Detectar filtro temprano**: la segunda viñeta (cuánto inglés hablado a diario con Tempo) es la
  que da el dato real. El riesgo no está en la call de 10 min: está en la comunicación diaria.
- **Voz de Gonzo**: "I want to be upfront about my level rather than find out later" invierte el
  marco - no es una disculpa, es alguien que no quiere hacer perder tiempo a nadie. Viñetas en
  chat, sin relleno, cierra con un hecho (el C1 en camino) no con una urgencia.

**Versión alternativa (más corta, para un chat de LinkedIn):**

```
Thanks David, read everything in detail - the role and the benefits look solid.

Before we set up the call, one thing I want to be clear about: my written English is strong
(documentation, code review, async work is where I am strongest) and my spoken is solid B2,
which matches the B2+ in the JD. I am enrolling for C1 and TOEFL this month.

Is B2+ the level you work with for this role, and how much of the daily work with Tempo is
spoken English?
```

**Lo que NO se manda (y por qué):** ninguna versión que pregunte *"¿el cliente exige C1
conversacional?"*. Con esas palabras, el caso Staffy se repite por auto-sabotaje: te quedás sin
proceso y sin información.

**Las otras 3 preguntas de la call (horas, PTO, educational allowance) están en
`guion-call-21-10.md`.** El PTO es la que más cambia el número: si los 20 días no se pagan, el
neto cae de ≈ USD 4.140 a ≈ USD 3.810.

### (ii) Qué cambiar según la respuesta de David

| Respuesta de David | Acción subsecuente |
|--------------------|--------------------|
| **“B2+ es lo que pedimos”** y el día a día con Tempo es mayormente async/documentación | **Avanzá.** Mandá el CV de frontend/code-evaluator (no declara A/B testing, así que no depende de resolver ese punto todavía). Pedí la call. |
| **“B2+ alcanza, es mayormente async”** pero en las entrevistas hay calls con el cliente US | **Avanzá igual**, diciendo que el C1 viene en camino y que el inglés hablado es tu punto a trabajar. No lo escondas: un C1 de papel que no se sostiene en una call es peor que un B2 honesto. |
| **“El cliente requiere C1 conversacional”** (o equivalente) | **No gastes más en el proceso.** Salí con dignidad: *"Thanks for being clear - that's a gap I need to close first. Let's keep in touch."* Sol y Staffy confianza en vos; esa confianza se reutiliza. Preguntale si hay otro req Frontend sin ese filtro. |
| **Respuesta vaga / no menciona el día a día** ("B2+ is fine" y cambia de tema) | **Es el patrón Staffy/Sol en incubación.** Tratá el idioma como filtro hasta que se demuestre lo contrario. Eso no es desconfiar de David: es no mandar el CV todavía. Insistí **una** vez con la pregunta operativa: *"Just to make sure I get it right - how much of the daily work with Tempo is spoken English?"* Una insistencia, no más. |
| **El PTO se paga** (o hay flexibilidad) | Subí la prioridad del proceso: el neto real pasa de ≈ USD 4.140 a la parte alta del rango, y la oferta deja de ser solo un empate con Staffy. |

---

**Conclusión:** Verificar el nivel de inglés antes de la entrevista y resolver la falta de evidencia en A/B testing y educación son los pasos críticos para mitigar riesgos y evitar un cierre inesperado.