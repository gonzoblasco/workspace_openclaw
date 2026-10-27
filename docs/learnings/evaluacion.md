# Learnings - evaluacion

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## PR-Agent: el review automatico no alcanza el nivel de la revision humana (medido con verdad de base y juez)

PR-Agent (The-PR-Agent/pr-agent) en modo review automatico NO alcanza el nivel de la
revision humana. Medido el 2026-10-20 contra PRs publicos con revisiones humans
reales como verdad de base, con juez independiente.

Caso encode/httpx#3769 (2 revisores humans apuntan al mismo bug central: dentro
del bloque finally, el for sobre self._mounts no tiene try/finally por transporte,
asi que si un mount lanza al cerrar los siguientes quedan ABIERTOS):
- review (--pr_url, gpt-oss): 0 hallazgos
- review (plain-diff, gpt-oss): 1 hallazgo ("Exception Masking") = adyacente, NO
  el bug real
- ask (plain-diff): 5 falsos positivos, veredicto 0/10
- server A2A en Docker: "No major issues detected", veredicto 0/10
- otros 2 modelos cloud (kimi-k2.6, deepseek-v4-pro): 0 hallazgos
- modelo local gemma4:12b-mlx: se cuelga (ctx 262k deja la RAM al 14%, swap 7.8GB)

Caso pydantic/pydantic#13953: 0 hallazgos, los 3 revisores humans lo encontraron.

Veredictos de los jueces (deepseek-v4-pro / kimi-k2.6): 1/10, 0/10, 0/10.

Conclusion: sirve como generador de borradores (describe, improve, primer pase de
ask) y como reviewer de segunda opinion, NO como detector de bugs. La causa no es
la integracion: es la calidad del modelo sobre este tipo de codigo, y el prompt de
pr_reviewer produce salida estructurada pero sin el acierto.

Metodologia que sirvio: usar PRs publicos que YA tienen revisiones humans como
verdad de base, y un juez con modelo DISTINTO al que genero el output. Cuidado
metodologico: el juez hay que darle la verdad de base SOLO del PR evaluado (si se
le mezclan dos PRs, penaliza hallazgos que no correspondian).

---

## PR-Agent no sirve para redactar PRs: contra Claude Code con el mismo modelo pierde en contenido y rompe el formato

PR-Agent NO sirve para redactar descripciones de PR: medido contra Claude Code con el
mismo modelo (Ollama) y el mismo diff, el 2026-10-20.

Test: diff real de scripts/onyx-tool.py (425 lineas) del propio workspace. Mismo
modelo (minimax-m3.1-flash:cloud via Ollama) para las dos herramientas.

PR-Agent describe (4752 chars): 4 bullets genericos ("CLI to start, stop, restart...",
"Detects project location dynamically"). NO menciona ninguno de los 5 hechos clave
del cambio real: la ruta duplicada (deployment/docker_compose/deployment/docker_compose),
el filtro de containers que no leia los cuatro campos de docker ps, el limite de 8 GB
de Docker Desktop, ni por que el CI fallaba por rutas absolutas. Claude Code (2499
chars) menciona los 5.

Defectos estructurales del output de PR-Agent (visibles en el cuerpo del PR):
- title sale literally "None" (generate_ai_title=false por default, y en plain-diff
  no hay PR al que sacarle el titulo).
- File Walkthrough con 14 links href="" (vacio) y 14 conteos "+-1/--1" (placeholder).
- Declara "10 files" cuando el diff tiene 14.
- en modo --pr_url NO imprime: solo publica, o queda en settings.data; push_outputs
  solo dispara si publish_output es true. O sea: para usarlo en un flujo hay que
  habilitar publicacion real.

Causa de fondo: PR-Agent comprime el diff a un prompt; Claude Code explora el repo
con un loop agéntico (grep, leer archivos, tests) y de ahi sale el contenido real.

Dato de contexto: la descripcion humana del PR pydantic#13884 (4151 chars) que use
como verdad de base termina con "Generated with Claude Code" - o sea, en la practica
la barra de calidad de una descripcion de PR la pone Claude Code, no una persona.

---

## Cuando el motivo de un cierre no está registrado, no lo completes

**26/10/2026 (TEAM/tempo + recontacto a recruiters).** Al registrar la respuesta de Samarth
(Ritz-Carlton) escribí en el tracker que ese proceso "NO cayó por el idioma" y que "el silencio
fue de la empresa", y además repetí el detalle de "Samarth 'let me check with the manager' x7" y
"feedback 24-48h incumplido" que ya estaba en el tracker desde el 22/09. **Gonzo lo Pushback:
"no dijo que fuera por el idioma pero no explicó por qué, así que supongo fue el idioma".**

Verificado con `git log -S` y grep sobre todo el workspace: **las dos frases del "x7" y del
"24-48h" no tenían fuente en ningún archivo.** El transcript real de Ritz-Carlton
(`docs/entrevistas/ritz-carlton/ritz-carlton-retest-seguimiento.md`) muestra: test 69% -> retest
OK -> primera ronda con la empresa el 02/09 -> **silencio**, y el documento dejó el proceso
**ABIERTO** el 11/09 ("pese a no haber tenido una respuesta directa, aun no la demos por cerrada").
Cerró por la regla de los 10 días, **no por un rechazo**, y el motivo del silencio **nunca quedó
registrado**. Se corrigió la fila: dos hipótesis (idioma / priorities del cliente), ninguna
verificada.

**La regla que sale:**
1. **Un detalle sin fuente no entra al tracker.** Si no se puede señalar el archivo y la línea de
   donde salió, no se escribe. "Repetido x7" y "24-48h incumplido" son el tipo de frase que se
   invente por inercia al resumir un proceso y después viaja como dato duro durante meses.
2. **"No fue por X" es tan fuerte como "fue por X".** Afirmar una causa negativa sin evidencia
   requiere el mismo respaldo que la positiva. Lo seguro es: "cerró por la regla de los 10 días,
   no hubo rechazo, y el motivo del silencio no está registrado".
3. **Cuando el dato falta, la hipótesis va explícita** ("hay dos hipótesis y ninguna verificada"),
   no resuelta por deducción. Gonzo suponiendo "fue el idioma" es una hipótesis legítima y
   declarada; yo escribiéndolo como hecho es un error de registro.
4. **Verificación cruzada antes de amplificar:** cuando un resumen viejo ya trae un detalle
   dudoso, no hay que propagarlo. `git log -S "<frase>"` muestra cuándo entró; `grep` sobre las
   fuentes reales muestra si existe.

**Contexto:** en un proceso donde el idioma es el filtro, la credibilidad de Gonzo es lo único que
no se negocia, y la del workspace también: un tracker con un motivo inventado termina
justificando decisiones que no corresponden.

---

## Una herramienta en el CV que no está en la ficha: hay que sacarla, no matizarla

**26/10/2026 (Figma).** Gonzo revisó un documento de prep y marcó: *"te dije ya, no usaba Figma
sino React Storybook"*. Verificado con grep sobre todo el workspace: **Figma no estaba en
`memory/career-facts.md`.** Estaba en **9 CVs** (Infjini, MercadoPago, Team/Tempo, Mural, Sol,
frontend-code-evaluator, MercadoLibre, RYZ, EIT/HTC), en **2 mensajes de outreach** (RYZ y
MercadoPago), y en los **PDF y DOCX generados** de todos ellos. En el seguimiento de EIT/HTC
estaba marcado **"CUMPLE (confirmado por Gonzo 15:56)"** - una atribución **falsa** que yo mismo
escribí.

**La cadena de cómo entró:** el corpus §2.2 decía "revisaba componentes de Storybook y **diseños**
antes de implementar" (correcto, y es Storybook). Al traducirlo a skills, alguien -yo- leí
"diseños" como "diseños en Figma" y agregué **Figma (revisión de diseño)** a la lista de
herramientas. Después, los CVs se generaron desde esa línea y el claim heredó a todas partes.
**El corpus no era el problema: la traducción de "diseños" a "Figma" sí.**

**La regla que sale:**
1. **El corpus es la fuente, y "diseños" no es "Figma".** Traducir una línea del corpus a un
   claim de herramienta es un paso que **agrega información**: si la herramienta no está
   nombrada en la ficha, no puede aparecer en el CV. La revisión de diseño de Gonzo es sobre
   **componentes en Storybook (React)**, y eso es exactamente lo que la ficha dice.
2. **Una herramienta que aparece en un CV tiene que estar en el corpus, con la misma
   granularidad.** "Diseño" ≠ "Figma". "Testing" ≠ "Playwright". La lista de herramientas del
   corpus es una lista de hechos, no de sinónimos.
3. **La falsa atribución es el peor de los casos.** "Confirmado por Gonzo 15:56" sobre algo que
   Gonzo no dijo es peor que un claim inventado: le da al dato una autoridad que no tiene, y
   desarma cualquier revisión posterior. Cuando se reescribe una tabla de fit, la atribución se
   reescribe con ella o se borra.
4. **Los artefactos derivados heredan el error.** El claim entró al corpus, y de ahí a 9 CVs, 2
   mensajes, 9 PDFs y varios DOCX. Un error en el corpus es un error multiplicado por el
   pipeline. Por eso la corrección va **desde el corpus**, y los derivados se regeneran
   (`scripts/cv-md-to-html.py` + `scripts/build-cv-docs.sh`; el PDF de Tempo usa
   `md-to-pdf` con `cv-style.css`).

**Verificación hecha (26/10/2026):** 0 ocurrencias de "Figma" en los 9 PDFs y en los 5 DOCX
regenerados; Figma quedó **solo** donde corresponde: (a) como **requisito del puesto** en el JD
de RYZ, (b) en el tracker como parte del stack del req de Disney, (c) en la nota de corrección
del corpus y del seguimiento de EIT/HTC.

**El patrón de fondo, que ya es el cuarto de hoy:** un dato entra al corpus por una traducción
que parece inocua ("diseños" → "Figma", "el cliente no respondió" → "no fue por idioma",
"cerró por la regla de los 10 días" → "el silencio fue de la empresa"). Cada vez, la traducción
agregó una afirmación que el original no tenía. **El original no se toca; lo que se agrega tiene
que estar verificado.**

---

## No te quedes con el no: recontactá con hechos, no con excusas (26-27/10/2026)

**El caso de prueba.** Cinco procesos cerrados en cuatro días por el mismo motivo: **filtro de
inglés conversacional (C1)**.

| Proceso | Cierre | Qué dijo el recruiter al cierre |
|---|---|---|
| Staffy / Pfizer (20/10) | cerrado | *"I think it would be best not to move forward at this stage."* |
| Sol Bisio (21/10) | cerrado | *"El cliente necesita sí o sí un C1 conversacional"* |
| EIT / HTC / Disney (24/09) | cerrado | *"We will update if they want to schedule call"* |
| Ritz-Carlton (22/09) | cerrado por la regla de los 10 días | la empresa nunca respondió |
| TEAM / tempo.io (26/10) | posición cerrada | *"The position is on hold"* (el gate lo puso el cliente, en Europa) |

**El 26/10, Gonzo recontactó a los cinco con un mensaje corto** que decía tres cosas: que
arrancaba clases de inglés **ese mismo día**, que preguntaba si en **uno o dos meses** podían
**reevaluar**, y que el objetivo era revalidar B2 y después el C1. A Sol, en español (con ella se
había hablado todo en español).

**Resultado: 5 de 5 respondieron y ninguno cerró la puerta. Solo UNO tiene fecha concreta
(Siraj/Disney, 1ra o 2da semana de noviembre); los otros cuatro aceptaron "volvemos a hablar en uno
o dos meses" o "te avisamos" - que es puerta abierta sin fecha.**

| Contacto | Respuesta | Qué abre |
|---|---|---|
| Samarth | "Sure thing, Gonzalo and All the Best" | reencuentro (el puesto de ~USD 82k nunca dio feedback) |
| Julieta Costa | "Of course :) Best!" | reencuentro (el gate lo ponía Pfizer, el cliente) |
| Siraj Shaik | "estudiá inglés para cuando me presente a Disney" | **entrevista en la 1ra o 2da semana de noviembre** |
| Parthasarathy | "We will update you if we have response. Position is on hold it seems" | la **posición** del req está en pausa en el canal de EIT (el mismo req vive en Infojini) |
| Sol Bisio | "Qué bueno que hayas arrancado las clases... Podemos volver a hablar en uno o dos meses y ver... qué oportunidades hay disponibles" | reencuentro. **No reabre el req de Full Stack**: es un "vemos en el momento", sin fecha |

**Por qué funcionó - la mecánica, no la suerte:**

1. **El mensaje NO pidió reconsideration.** No decía "reconsideren mi candidatura" ni "denme una
   oportunidad". Decía **"estoy resolviendo el bloqueante y les aviso"**. Eso cambia la naturaleza
   de la conversación: deja de ser un individuo rogando y pasa a ser alguien que **está haciendo
   algo concreto sobre la causa del no**. La respuesta natural a eso no es otro no.
2. **Aportó una fecha, no un pedido.** "En uno o dos meses" + un curso que empieza HOY es
   verificable. Un pedido sin fecha no se puede cumplir.
3. **Fue corto y no se excusó.** ~100 palabras, sin explicar de más, sin disculparse, sin
   mencionar el nivel declarable. Cero riesgo de humiliation.
4. **Fue por el intermediario, no al cliente.** El que puede matchearte contra otro req es el
   recruiter, y en los 5 casos la barra la puso el cliente final (Pfizer, Disney, Tempo, el
   cliente de Samarth). **Recontactar al intermediario es lo correcto**: es el único que puede
   reabrir la puerta cuando el filtro caiga.
5. **El idioma se atacó con un hecho, no con una promesa.** "Empiezo el curso hoy" es un hecho
   verificable; "voy a mejorar mi inglés" es una promesa. Los recruiters respondieron al hecho.

**Lo que hay que corregir del mensaje usado (registrado aparte):** decía *"I'm retaking the course"*
y *"re-validate my B2 level"*, que presuponen un curso previo y un certificado de B2 que **el
corpus no tiene** (§4 solo tiene Deque). En un proceso donde el idioma es el filtro, la
credibilidad es lo único que no se negocia, y un recruiter repregunta fechas. **La forma
verificable, igual de fuerte:** *"I started a B2 intensive course at the CUI (UBA) today - two
months - and I plan to take the C1 certification exam next year."*

**La regla general, que aplica más allá del inglés:**

> **Un cierre por un bloqueo objetivo (idioma, certificación, disponibilidad) no es un no al
> perfil: es un no a una condición. Si la condición es resoluble y estás resolviéndola, el
> circuito correcto es avisar, con fecha y con hecho - una sola vez, y volver al trabajo.**

La segunda parte importa: **una vez y volver al trabajo.** Insistir sobre un no consume el capital
de la relación. El tracker lo tiene como regla ("energía de follow-up solo si ellos escriben,
máximo un reclamo por proceso") y este caso la confirma: después del mensaje no se volvió a
insistir con nadie, y ninguno de los cinco cerró la puerta.

---

## El filtro de idioma no se negocia con el CV: se negocia con la pregunta

**La regla (origen Staffy/Pfizer 2026-10-20, ampliada 2026-10-26 con 4 casos):** preguntar por el nivel de ingles requerido en el PRIMER mensaje de un proceso LATAM con comunicacion diaria en ingles. Es la variable que mas rapido descarta y la que mas caro cuesta descubrir tarde. La honestidad sobre el nivel oral (B2 hablado, C1 escrito) no alcanza ante un filtro real de C1 conversacional: Writing C1 no compensa, son evaluaciones distintas.

**Ampliacion del 26/10: el filtro no es "clientes US", es clientes NO ANGLOPARLANTES.** Los cuatro casos, con quien ponia la barra:

| Caso | Quien pone la barra | Idioma |
|---|---|---|
| Staffy / Pfizer (20/10) | el cliente (Pfizer) | C1 conversacional, comunicacion diaria con US y Canada |
| Sol Bisio (21/10) | el cliente sin nombre | C1 conversacional "si o si" |
| Infjini / Disney (26/10) | el cliente (Disney) | el idioma bloquea la presentacion, no el proceso |
| **TEAM / tempo.io (26/10)** | **el cliente (Tempo), y el equipo esta en EUROPA** | "bastante exigentes con la fluidez en ingles, **especialmente al momento de discutir y explicar temas tecnicos**" |

**Las dos correcciones que traen los casos 3 y 4:**
1. **El filtro es el cliente, nunca el intermediario.** En los cuatro, el recruiter/intermediario (Julieta, Sol, Siraj, David) no es quien pone la barra: la pone el cliente final. Consecuencia: **recontactar al intermediario es lo correcto**, porque es el que puede matchearte contra otro req. Y el "gate" se levanta solo con el ingles en curso.
2. **El equipo del cliente puede estar en Europa**, y ahi la exigencia no es el acento sino la **fluidez para discutir y explicar temas tecnicos** (texto literal de David, 26/10). Eso es un recorte distinto al de "clientes US": no es un موضوع de horario ni de acento, es **de poder sostener una conversacion tecnica en vivo y explicar decisiones**. Por eso la regla no dice "clientes US" sino **"comunicacion diaria en ingles con clientes o equipos no angloparlantes"**.

**El dato que mas ayuda a preparar:** el cliente de TEMPO exijo fluidez **"al discutir y explicar temas tecnicos"**, que es exactamente lo que Gonzo ya hace en su trabajo real (en EY escribia los requisitos tecnicos de accesibilidad con ejemplos de codigo y revenia disenos antes de implementar). El gap de idioma es oral, pero **la habilidad pedida - explicar decisiones tecnicas - es su fuerte, no su gap**.

---

