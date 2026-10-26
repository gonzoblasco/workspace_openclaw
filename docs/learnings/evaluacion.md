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

