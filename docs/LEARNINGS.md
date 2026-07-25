# LEARNINGS.md — Aprendizajes Metodológicos

Aprendizajes de sesiones que vale la pena recordar. No son ADRs (decisiones), no son CHANGELOG (cambios). Son **lecciones aprendidas** para no repetir errores y mejorar el workflow.

**Clasificación:**
- 🔧 **OpenClaw** — la herramienta, el runtime, el gateway. Aplica a cualquiera que use OpenClaw.
- 🧠 **AI Engineering OS** — nuestra mecánica, rutinas, patrones, skills. El sistema que construimos sobre OpenClaw.
- **Proyecto** — un proyecto de producto concreto en `projects/<slug>/`.

---

## 2026-07-20 — Modelos, truncamiento y workflow de reasoning

### 1. El truncamiento no es del modelo, es de la configuración 🔧 **OpenClaw**
Pasé 3 modelos diferentes pensando que el problema era el modelo, cuando era `maxTokens` sin configurar en el gateway (`openclaw.json`).  
**Lección:** antes de cambiar de modelo por truncamiento, revisar la configuración del gateway primero.

### 2. Los benchmarks no predicen la experiencia real 🔧 **OpenClaw**
Nemotron-3-Super tenía benchmarks sólidos, pero truncaba en la práctica. DeepSeek-V4-Flash sin `maxTokens` configurado también truncaba.  
**Lección:** el benchmark no te dice si la respuesta se corta antes de terminar. Probar siempre con una tarea real.

### 3. Reasoning off vs maximum: no es "más texto", es un salto cualitativo 🔧 **OpenClaw**
Maximum no escribió más, escribió *mejor*: encontró problemas que el otro no vio (5 issues en un ADR que el modo off consideró correcto).  
**Lección:** maximum no es para generar más, es para tener un code reviewer además de un generador. Usarlo cuando el costo de error es alto.

### 4. El consumo de GPU no se puede medir sin probar 🔧 **OpenClaw**
La teoría decía que Nemotron era tier 2 y barato, pero en la práctica truncaba. DeepSeek-V4-Flash es tier 2 también, pero con 1M de contexto y thinking modes.  
**Lección:** la única forma de saber si un modelo gasta mucha GPU es usarlo un día entero en tareas reales.

### 5. El workflow de reasoning como filtro de Kanam es un patrón nuevo 🧠 **AI Engineering OS**
No es una configuración técnica, es un acuerdo de cómo trabajamos juntos: Kanam evalúa cada tarea y recomienda subir/bajar reasoning, Gonzo decide si acepta o dice "ignorar recomendación".  
**Lección:** algunos workflows no se configuran en el gateway, se acuerdan en la conversación y se registran. Son igual de importantes que la config técnica.

### 6. MEMORY.md no es para aprendizajes metodológicos 🧠 **AI Engineering OS**
MEMORY.md debe quedar para preferencias personales, datos de Gonzo, y decisiones de configuración. Los aprendizajes de sesión van acá, en LEARNINGS.md.  
**Lección:** separar "quién soy" (MEMORY.md) de "qué aprendí" (LEARNINGS.md).

---

## 2026-07-20 — Inventario de repos públicos y diagnóstico de proyectos

### 12. El inventario de repos como diagnóstico periódico 🔧 **OpenClaw**
No sabía el estado real de todos mis repos hasta que los revisé uno por uno. Algunos estaban en estado "zombie" (con README pero sin actividad real, o sin README directamente).  
**Lección:** hacer un inventario completo cada N meses evita acumular ruido. Los repos sin README ni descripción son basura digital — archivar o eliminar.

### 13. No todos los proyectos necesitan reset — algunos necesitan evolución 🔧 **OpenClaw**
El instinto de "resetear todo lo que no está terminado" es incorrecto. create-stack-next y workflow-kit están bien encaminados. Lo que necesitan es evolución, no reinicio.  
**Lección:** distinguir entre "proyecto que necesita redefinición" (reset) y "proyecto que necesita iteración" (evolución).

### 14. Los forks también son parte del portfolio 🔧 **OpenClaw**
Aunque no son proyectos propios, los forks de repos Tier 0 son señal de contribución OSS activa. No ignorarlos en el inventario.  
**Lección:** cuando hagas inventario, incluir forks. No como proyectos, pero sí como indicadores de actividad.

### 15. antigravity-developer-stack: contenido valioso, estructura wrong 🧠 **AI Engineering OS**
AGDS tiene 30+ patrones y playbooks con contenido real, pero es un monolito con nombre de sci-fi. El contenido merece mejor formato.  
**Lección:** a veces el problema no es la idea sino el vehículo. AGDS no necesita más contenido, necesita reempaquetado.

### 16. ai-engineering-bootcamp no es código por rehacer, es contenido por escribir 🧠 **AI Engineering OS**
La estructura del bootcamp está completa (10 niveles, 23 proyectos), pero todo está en "Pending". No hay código que refactorizar — hay 23 proyectos de contenido por crear.  
**Lección:** no todo lo que parece "incompleto" es un proyecto de software. A veces es un proyecto de contenido, y el approach es diferente: escribir, no programar.

---

## 2026-07-20 — P09 Evaluation Lab: LLM-as-a-Judge y evaluación de prompts

### 21. El patrón LLM-as-a-Judge con 3 dimensiones es más robusto que un score único 🔧 **OpenClaw**
P09 implementa un juez que evalúa respuestas en 3 dimensiones separadas. El score final se recalcula server-side como promedio, no se confía en el score que devuelve el modelo.  
**Lección:** cuando un LLM evalúa a otro LLM, pedir criterios separados y recalcular el agregado server-side.

### 22. Forzar JSON puro en el system prompt del juez, con validación estricta post-parse 🔧 **OpenClaw**
Nunca confiar en que el modelo va a devolver JSON limpio. Siempre try/catch + raw response en el error.  
**Lección:** el patrón `validateAndNormalize()` con clamp + type checking es obligatorio.

### 23. Batch evaluation con Promise.allSettled + after() para tolerancia a fallos 🔧 **OpenClaw**
En evaluación batch, la tolerancia a fallos es crítica. Un test case mal formado no debe impedir que el resto se evalúe.  
**Lección:** `allSettled` + estado agregado (failed si todos fallaron, completed si alguno funcionó) es el patrón correcto.

### 24. Interpolación de variables en system prompts con validación de existencia 🔧 **OpenClaw**
La interpolación de prompts debe validar que las fuentes de datos existen antes de armar el prompt. Fallar temprano con 400 es mejor que fallar en la llamada a la API con 502.

### 25. Skills de evaluación como documentación del patrón, no como código ejecutable 🔧 **OpenClaw**
Documentar patrones de IA como skills markdown (no como código) los hace portables entre proyectos. El skill describe el qué y el por qué; la implementación concreta se adapta a cada stack.

---

## 2026-07-20 — Biome: el lint que rompe CI por culpa de nuestro propio stack

### 17. Biome formatea su propio JSON de configuración 🧠 **AI Engineering OS**
`biome.json` no es un archivo de configuración pasivo. Biome lo lee y lo lintea con sus propias reglas.  
**Lección:** el último paso del scaffold debe ser `npx biome check --write .` para que Biome deje todo consistente.

### 18. Los componentes de shadcn/ui generan falsos positivos de a11y en Biome 🧠 **AI Engineering OS**
`noLabelWithoutControl` se dispara en `label.tsx` de shadcn/ui porque el componente `Label` es un wrapper genérico.  
**Lección:** ignorar `src/components/ui/*` en `biome.json` > `files.ignore` desde el día 1.

### 19. Biome + shadcn/ui: el combo que siempre da problemas si no se configura desde el día 1 🧠 **AI Engineering OS**
Cada vez que se crea un proyecto con shadcn/ui + Biome, hay que ignorar los componentes y autoformatear.  
**Lección:** esto debería ser parte del workflow de scaffold, no un fix post-hoc.

### 20. `biome check --unsafe` puede romper typecheck 🔧 **OpenClaw**
El unsafe fix de Biome puede cambiar `!.` a `?.` y romper typecheck.  
**Lección:** después de `biome check --unsafe`, siempre correr `tsc --noEmit` para verificar.

---

## 2026-07-22 — Self-Improving Agent: Pattern-Keys, Recurrence-Count y umbral de promoción

### 26. Pattern-Keys como mecanismo de deduplicación de aprendizajes 🧠 **AI Engineering OS**
Formato `area.symptom` como identificador estable para entradas de aprendizaje.  
**Decisión:** adoptado como campo opcional en LEARNINGS.md.

### 27. Recurrence-Count + umbral de promoción para detectar patrones sistémicos 🧠 **AI Engineering OS**
Cuando un aprendizaje se repite 3+ veces en 30 días en >= 2 tareas distintas → promover a AGENTS.md/MEMORY.md.  
**Lección:** las recurrencias no son accidentes — son patrones que el sistema debería absorber.

### 28. IDs de entrada (LRN-YYYYMMDD-XXX) para referenciar aprendizajes 🧠 **AI Engineering OS**
Útil cuando una entrada es referenciada desde otra o desde MEMORY.md. Opcional.

### 29. No instalar skills que pisanean lo que ya tenemos — robar ideas, no skills 🔧 **OpenClaw**
Si una skill externa pisa 80%+ de nuestra estructura, no la instalamos — le robamos las ideas que nos faltan.  
**Lección:** el 90% de las skills externas no vale la pena instalarlas, pero casi todas tienen 1-2 ideas que podemos robar.

---

## 2026-07-20 — Patrones de fix y humanización en OSS

### 7. Fix de una línea + defensa en profundidad en la capa contigua 🔧 **OpenClaw**
Cuando un bug tiene un fix directo, siempre buscar si hay una segunda capa que también debería protegerse.  
**Lección:** el fix directo resuelve el síntoma; la defensa en profundidad evita que la misma clase de error vuelva a ocurrir.

### 8. Guarda basada en ID en vez de timestamp para ordenar eventos concurrentes 🔧 **OpenClaw**
Los timestamps tienen colisiones bajo writes concurrentes. Los IDs auto-incrementales son estrictamente monotónicos.  
**Lección:** para ordenar eventos concurrentes, preferir un identificador monotónico sobre un timestamp.

### 9. Cuando un bug requiere fix upstream, el valor está en el análisis, no en el workaround 🔧 **OpenClaw**
Si el root cause está en otra herramienta, intentar un workaround suele ser frágil. Un análisis técnico detallado vale tanto como el código.  
**Lección:** no todo bug necesita un PR. A veces el mejor aporte es un comment que ahorre horas de investigación.

### 10. Para bugs de concurrencia, forzar la condición, no el timing exacto 🔧 **OpenClaw**
No perseguir el timing — perseguir la invariante que se rompe. Una vez que sabés qué condición causa el bug, podés reproducirla deterministicamente.

### 11. Humanizar el tono en PRs y comments de OSS 🔧 **OpenClaw**
En repos de alto perfil, la percepción importa. Un PR técnicamente perfecto pero que suena a bot puede ser ignorado.  
**Lección:** en OSS de alto perfil, el tono humano genera más confianza que la perfección técnica.

---

## 2026-07-22 — Self-Improving Agent (ivangdavila): Learning Signals, Self-Reflection y Conflict Resolution

### 30. Learning Signals: frases gatillo para logging automático 🧠 **AI Engineering OS**
Tener señales explícitas reduce la dependencia de que el agente "sepa" cuándo loggear.  
**Adoptado:** incorporado a AGENTS.md.

### 31. Self-Reflection post-tarea como hábito 🧠 **AI Engineering OS**
Después de tareas significativas, hacer una pausa de evaluación con formato CONTEXT / REFLECTION / LESSON.  
**Adoptado:** incorporado a AGENTS.md.

### 32. Conflict Resolution: qué hacer cuando dos lecciones se contradicen 🧠 **AI Engineering OS**
Más específico gana → más reciente gana → preguntar a Gonzo.  
**Adoptado:** incorporado a AGENTS.md.

### 33. Common Traps: errores típicos al aprender 🧠 **AI Engineering OS**
Aprender del silencio, promover muy rápido, leer todo siempre, compactar borrando.  
**Adoptado:** incorporado a AGENTS.md.

---

## 2026-07-22 — Proactive Agent (halthelobster): WAL Protocol, Working Buffer, Resourcefulness

### 34. WAL Protocol: escribir antes de responder 🔧 **OpenClaw**
Cuando el input contiene correcciones, preferencias o decisiones, PRIMERO se escribe al archivo, DESPUÉS se responde.  
**Adoptado:** incorporado a AGENTS.md.

### 35. Working Buffer: loggear exchanges en zona de peligro 🧠 **AI Engineering OS**
Cuando el contexto de sesión llega al ~60%, capturar cada exchange en un archivo que sobrevive a la compactación.  
**Adoptado:** incorporado a AGENTS.md.

### 36. Compaction Recovery: protocolo de recuperación post-compactación 🧠 **AI Engineering OS**
Leer working buffer → leer daily notes → memory_search → extraer → presentar resumen.  
**Adoptado:** incorporado a AGENTS.md.

### 37. Relentless Resourcefulness: probar 5-10 approaches antes de rendirse 🔧 **OpenClaw**
Antes de decir "no puedo", probar múltiples approaches: CLI, browser, web search, subagentes.  
**Adoptado:** incorporado a AGENTS.md.

### 38. Verify Implementation: cambios de texto ≠ cambios de comportamiento 🔧 **OpenClaw**
Cuando se cambia cómo funciona algo, verificar el mecanismo real, no solo el texto.  
**Adoptado:** incorporado a AGENTS.md.

---

## 2026-07-22 — Neo Soul Decision Agent: Confidence Tagging y Retrospective enriquecido

### 39. Confidence Tagging en recomendaciones 🔧 **OpenClaw**
Cuando se da una recomendación con datos incompletos, etiquetar el nivel de confianza: 🟢/🟡/🔴.  
**Adoptado:** incorporado a AGENTS.md.

### 40. Self-Reflection enriquecido con BIASES DETECTED 🔧 **OpenClaw**
Identificar sesgos cognitivos en retrospectiva ayuda a no repetir patrones de pensamiento erróneos.  
**Adoptado:** actualizado el formato en AGENTS.md.

---

## 2026-07-22 — SkillCompass: evaluación multidimensional, gate dimension y auto-rollback

### 41. Framework de evaluación multidimensional 🔧 **OpenClaw**
Evaluar en múltiples dimensiones con pesos explícitos es más robusto que un score único.

### 42. Gate dimension: una dimensión que puede vetar todo 🔧 **OpenClaw**
Si una lección, workflow o cambio tiene un error crítico, no se promociona aunque cumpla con todos los otros criterios.

### 43. Tiered verification (L0-L3) post-cambio 🔧 **OpenClaw**
El nivel de verificación debe escalar con el alcance del cambio. Un cambio de typo no necesita full eval; un cambio arquitectónico sí.

### 44. Auto-rollback on regression 🔧 **OpenClaw**
Si después de una mejora el sistema empeora, revertir automáticamente. No todas las mejoras lo son realmente.

---

## 2026-07-22 — AI Persona OS: DREAMS.md, Structured Escalation y Growth Loops

### 45. DREAMS.md: consolidación programada de memoria 🧠 **AI Engineering OS**
Cada ~7 días, consolidar daily logs recientes a MEMORY.md y archivar viejos.  
**Adoptado:** incorporado a AGENTS.md.

### 46. Structured Escalation: handoff cuando el agent está stuck 🔧 **OpenClaw**
BLOQUEO / CAUSA / INTENTOS / NECESITO / ALTERNATIVA. Nunca "no sé" sin contexto.  
**Adoptado:** incorporado a AGENTS.md.

### 47. Growth Loops: cuatro ciclos de mejora continua 🧠 **AI Engineering OS**
Curiosidad, Reconocimiento de Patrones, Expansión de Capacidades, Seguimiento de Resultados.  
**Adoptado:** incorporado a AGENTS.md.

---

## 2026-07-22 — Agent Team Orchestration: Handoff estructurado entre subagentes

### 48. Handoff estructurado entre subagentes 🔧 **OpenClaw**
Qué se hizo, dónde están los artifacts, cómo verificar, issues conocidos, qué sigue.  
**Adoptado:** incorporado a AGENTS.md.

---

## 2026-07-22 — Productividad & ADHD

### 49. Sistema de productividad adaptado a ADHD 🧠 **AI Engineering OS**
Una cosa a la vez, inbox capture, overload triage, rutinas de inicio/cierre, sin culpa.  
**Adoptado:** incorporado a AGENTS.md.

---

## 2026-07-22 — Meta-aprendizaje: evaluar skills externas

### 50. El patrón de evaluar skills de ClawHub con integración selectiva 🧠 **AI Engineering OS**
Leer → identificar qué pisa → qué aporta → decidir (instalar/robar/pasar).  
**Resultado:** 0 skills instaladas, ~25 patrones adoptados como convención propia.  
**Patrón formalizado:** agregado a AGENTS.md.

---

## 2026-07-23 — Skills Overhaul

### 51. El pipeline de producto funcionó exactamente como fue diseñado 🧠 **AI Engineering OS**
Seguimos el flujo completo sin pensarlo. El pipeline no es teoría, es cómo trabajamos.  
**Lección:** cuando el sistema está bien diseñado, los workflows se activan solos por contexto.

### 52. El patrón "evaluar → decidir → crear" es un mega-patrón reusable 🔧 **OpenClaw**
Lo aplicamos 3 veces en la misma jornada con distintos tipos de input.  
**Mega-patrón:** cualquier proceso de evaluación sigue este ciclo. Aplica a skills, herramientas, dependencias, frameworks, candidatos.

### 53. El validation gate entre fases es un patrón real 🔧 **OpenClaw**
Duplicación directa → descartar. Solapamiento parcial → evaluar profundidad. Sin duplicación → adoptar.  
**Lección:** cualquier decisión con alternativas puede usar este filtro de 3 vías.

### 54. Las skills transversales se activaron solas por contexto 🧠 **AI Engineering OS**
engineering-governance, knowledge-management, session-lifecycle, oss-contribution surgieron del contexto, no fueron invocadas explícitamente.  
**Lección:** si un workflow necesita ser "invocado" explícitamente todo el tiempo, quizás no está bien integrado.

### 55. La reflexión post-sesión debe ser parte del cierre 🔧 **OpenClaw**
Analizar "¿qué aprendimos? ¿qué patrones identificamos? ¿es global o de proyecto?" al final de cada sesión significativa.  
**Formalizado:** agregado a session-lifecycle como fase de reflexión.

### 56. Clasificar aprendizajes como global vs proyecto 🔧 **OpenClaw**
🌍 Global → aplica a cualquier proyecto. 🏗️ Proyecto → específico del AI Engineering OS. 📦 Contexto → específico de un proyecto de producto.  
**Lección:** esta clasificación misma es un mega-patrón.

### 57. Patrón de postulación: no saltar pasos 🔧 **OpenClaw**
🌍 Global
**Señal:** Gonzo pasa link de puesto laboral → pide CV optimizado.
**Patrón correcto:**
1. Fit analysis contra CV actual
2. **Preguntar por gaps** antes de escribir (no asumir experiencia que no está en el CV)
3. Esperar respuesta
4. Recién ahí crear CV optimizado
**Error:** dos veces seguidas salté del paso 1 al 4 sin preguntar. No corregí después del primer error.
**Lección:** cuando un patrón se repite en la misma sesión, corregir en el momento — no esperar a la próxima. Si ya lo vi fallar una vez, la segunda tengo que detectarlo antes de repetirlo.

---

## 2026-07-24 — Tailscale + OpenClaw webchat remoto

### 58. El gateway no usa el puerto del config si el LaunchAgent pasa `--port` 🔧 **OpenClaw**
🌍 Global
El `openclaw.json` tenía `port: 3000`, pero el LaunchAgent arrancó el gateway en 18789. El service file (`~/Library/LaunchAgents/ai.openclaw.gateway.plist`) le pasa `--port 18789` por encima del config.
**Lección:** cuando el gateway arranca vía LaunchAgent, el puerto real puede diferir del config. Verificar con `openclaw gateway status`.

### 59. Tailscale Serve funciona como proxy inverso contra loopback 🔧 **OpenClaw**
🌍 Global
No hace falta cambiar `bind` a `0.0.0.0` ni abrir puertos. `tailscale serve --https=443 127.0.0.1:<port>` expone el webchat en la tailnet sin modificar la config del gateway.
**Lección:** Tailscale Serve es la forma correcta de exponer OpenClaw. Simple, seguro, sin tocar config.

### 60. Device pairing es necesario incluso con token configurado 🔧 **OpenClaw**
🌍 Global
El token autentica la sesión HTTP, pero el device pairing autoriza el navegador como dispositivo. La primera vez desde un navegador externo (iPhone, otra máquina) requiere `openclaw devices approve <id>`.
**Lección:** esperar device pairing la primera vez. No es un error, es el flujo normal.

### 61. No hay app nativa iOS para OpenClaw 🔧 **OpenClaw**
🌍 Global
OpenClaw no tiene app para iOS. La alternativa es agregar el webchat a la pantalla de inicio como PWA desde Safari.
**Lección:** no buscar app en la App Store. Usar "Agregar a pantalla de inicio".

### 62. Node.js v22.18.0 del installer oficial compite con Homebrew 🔧 **OpenClaw**
🌍 Global
El installer de nodejs.org deja el binario en `/usr/local/bin/node`. Homebrew instala en `/opt/homebrew/bin/node`. Si `/usr/local/bin` está antes en el PATH, gana el viejo.
**Solución:** `sudo mv /usr/local/bin/node /usr/local/bin/node-v22.bak` para que Homebrew tome el control.
**Lección:** antes de diagnosticar problemas raros de OpenClaw, verificar `node --version`. Si no es ≥22.22.3 o ≥24, ese es el problema.
