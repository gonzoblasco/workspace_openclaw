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

