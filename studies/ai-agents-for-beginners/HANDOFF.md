# HANDOFF - Curso ai-agents-for-beginners

**Fecha:** 2026-11-12 01:18 GMT-3
**Proyecto:** ai-agents-for-beginners
**Branch:** main
**Repo:** https://github.com/gonzoblasco/workspace_openclaw
**Autor:** Kanam (CORE)

> HANDOFF generado en el cierre de sesion (2026-11-12). Es el punto de entrada para continuar este proyecto. El informe detallado de la sesion vive en `memory/2026-11-12.md`.

---

## Que se hizo en esta sesion

Estudio guiado del curso AI Agents For Beginners - OpenClaw Case Study, modulos 1 y 2. M1: clase explicada con mecanismo (ChatGPT vs GPT, transformer/atencion, pre-training, generacion, alucinacion, LLM a agente) y verificada contra papers (Attention Is All You Need arXiv:1706.03762; GPT-3 arXiv:2005.14165; Chinchilla arXiv:2203.15556; GPT-4 Technical Report arXiv:2303.08774). Se corrigieron dos fronteras del outline (una cita de M1 que era de M2; un claim de contexto de M4 en M2) y se creo el worksheet m1-llm-en-10-lineas.md con version modelo de 10 lineas, criterios de correccion y espacio para la version de Gonzo. M2: Gonzo ejecuto el prompt de investigacion en Vane y entrego un informe de 6 modelos; se guardo verbatim en m2-informe-modelos-2026-11-12.md con auditoria. La auditoria verifico contra fuentes oficiales: GPT-5.1 esta deprecated y SI soporta function calling (el informe decia 'no publicado'); Claude Sonnet 4.5 esta fuera de la linea actual (la vigente es Sonnet 5.5, 1M, $2/$10, corte jun-2026); DeepSeek-V4-Pro coincide con la pagina oficial (1M/384K, tool calls, $0.66/$1.98 off-peak); Gemini 2.5 Pro no se pudo verificar por redirect loop; Llama 4 Scout quedo parcial; Mistral Large 2407 esta deprecado y el modelo actual es Mistral Large 4. Conclusion: el informe es buen primer barrido pero no es la tabla final porque eligio modelos deprecados y tiene un falso negativo de tool calling. Pendiente: Gonzo escriba sus 10 lineas del M1; segunda pasada del M2 con 4 modelos vigentes y URLs oficiales; despues M3. Commits locales: 0ee1c4899e1 (worksheet M1), 922a7ddd37 (informe M2 + auditoria), y el commit de cierre. Sin push.

## Estado actual

- Modulo actual: Modulo 1 ensenado; Modulo 2 iniciado con el informe de Vane.
- Ejercicios hechos: M1 worksheet con version modelo; falta la version de Gonzo. M2 informe recibido y auditado; falta la tabla final.
- Preguntas abiertas: cual es el flagship actual de OpenAI; verificar Gemini 3.8 Flash y Llama 4 Scout; elegir 4 modelos vigentes.
- Proximo bloque: M1 (10 lineas de Gonzo) + segunda pasada M2; despues M3 (diagrama app -> API -> modelo).

## Proximos pasos

1) Gonzo escribe sus 10 lineas del M1 y las revisamos. 2) Segunda pasada del M2 con 4 modelos vigentes y URLs oficiales (Sonnet 5.5, DeepSeek-V4-Pro, Llama 4 Scout, Mistral Large 4, Gemini 3.8 Flash; identificar el flagship actual de OpenAI). 3) Recien despues M3: diagrama app -> API -> modelo.

## Decisiones y contexto que no debe perderse

- Se respeto el mapa oficial de 22 capitulos 1:1 aunque el contenido real derive en algunos bloques (el lab de ReAct cae dentro de memoria; el cap. 19 contiene PI packages y dos labs; el cap. 22 contiene todo prompt engineering). Los claims sin link quedan como afirmaciones del expositor, no como bibliografia verificada. El curso describe un OpenClaw generico: cualquier dato de archivos o tools se verifica contra el repo/instalacion local antes de usarse.
- El informe de Vane se conserva como borrador, no como tabla final. La auditoria es parte del ejercicio: un informe internamente coherente puede estar respondiendo otra pregunta si elige modelos deprecados.
- 'No publicado' no equivale a 'no existe': GPT-5.1 si soporta function calling segun la ficha oficial.
- Las fuentes terciarias (OpenRouter, UserRightAI) sirven para cross-check, no como fuente primaria.

## Como continuar

1. Leer este HANDOFF (estado actual + proximos pasos).
2. Leer `memory/2026-11-12.md` para el informe completo de la sesion.
3. Verificar el estado real antes de actuar (git, tests, la DB).

---

*Generado por `scripts/session-handoff.py` (session-lifecycle). Se regenera en cada cierre de sesion.*
