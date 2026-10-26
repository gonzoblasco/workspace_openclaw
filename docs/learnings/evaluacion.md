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

## El filtro de idioma no se negocia con el CV: se negocia con la pregunta

Staffy/Pfizer (2026-10-20): el screening se cerro en la etapa final por C1 conversacional, un requisito que el JD NO declaraba y que el pitch inicial de la reclutadora tampoco menciono. Preguntar por el nivel de ingles requerido en el PRIMER mensaje de un proceso LATAM con comunicacion diaria en ingles con clientes US: es la variable que mas rapido descarta y la que mas caro cuesta descubrir tarde. La honestidad sobre el nivel oral (B2 hablado, C1 escrito) no alcanza ante un filtro real de C1 conversacional: Writing C1 no compensa, son evaluaciones distintas.

---

