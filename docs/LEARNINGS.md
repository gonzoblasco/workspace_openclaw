# LEARNINGS.md — Aprendizajes Metodológicos

Aprendizajes de sesiones que vale la pena recordar. No son ADRs (decisiones), no son CHANGELOG (cambios). Son **lecciones aprendidas** para no repetir errores y mejorar el workflow.

---

## 2026-07-20 — Modelos, truncamiento y workflow de reasoning

### 1. El truncamiento no es del modelo, es de la configuración
Pasé 3 modelos diferentes pensando que el problema era el modelo, cuando era `maxTokens` sin configurar en el gateway (`openclaw.json`).  
**Lección:** antes de cambiar de modelo por truncamiento, revisar la configuración del gateway primero.

### 2. Los benchmarks no predicen la experiencia real
Nemotron-3-Super tenía benchmarks sólidos, pero truncaba en la práctica. DeepSeek-V4-Flash sin `maxTokens` configurado también truncaba.  
**Lección:** el benchmark no te dice si la respuesta se corta antes de terminar. Probar siempre con una tarea real.

### 3. Reasoning off vs maximum: no es "más texto", es un salto cualitativo
Maximum no escribió más, escribió *mejor*: encontró problemas que el otro no vio (5 issues en un ADR que el modo off consideró correcto).  
**Lección:** maximum no es para generar más, es para tener un code reviewer además de un generador. Usarlo cuando el costo de error es alto.

### 4. El consumo de GPU no se puede medir sin probar
La teoría decía que Nemotron era tier 2 y barato, pero en la práctica truncaba. DeepSeek-V4-Flash es tier 2 también, pero con 1M de contexto y thinking modes.  
**Lección:** la única forma de saber si un modelo gasta mucha GPU es usarlo un día entero en tareas reales.

### 5. El workflow de reasoning como filtro de Kanam es un patrón nuevo
No es una configuración técnica, es un acuerdo de cómo trabajamos juntos: Kanam evalúa cada tarea y recomienda subir/bajar reasoning, Gonzo decide si acepta o dice "ignorar recomendación".  
**Lección:** algunos workflows no se configuran en el gateway, se acuerdan en la conversación y se registran. Son igual de importantes que la config técnica.

### 6. MEMORY.md no es para aprendizajes metodológicos
MEMORY.md debe quedar para preferencias personales, datos de Gonzo, y decisiones de configuración. Los aprendizajes de sesión van acá, en LEARNINGS.md.  
**Lección:** separar "quién soy" (MEMORY.md) de "qué aprendí" (LEARNINGS.md).

---

## 2026-07-20 — Inventario de repos públicos y diagnóstico de proyectos

### 12. El inventario de repos como diagnóstico periódico
No sabía el estado real de todos mis repos hasta que los revisé uno por uno. Algunos estaban en estado "zombie" (con README pero sin actividad real, o sin README directamente).

**Lección:** hacer un inventario completo cada N meses evita acumular ruido. Los repos sin README ni descripción (0001, prueba_minecraft_claude_code) son basura digital — archivar o eliminar.

### 13. No todos los proyectos necesitan reset — algunos necesitan evolución
El instinto de "resetear todo lo que no está terminado" es incorrecto. create-stack-next y workflow-kit están bien encaminados: tienen identidad clara, diferenciación real, y están publicados. Lo que necesitan es evolución, no reinicio.

**Lección:** distinguir entre "proyecto que necesita redefinición" (reset) y "proyecto que necesita iteración" (evolución). El workflow de product discovery es para lo primero; el desarrollo incremental para lo segundo.

### 14. Los forks también son parte del portfolio
Aunque no son proyectos propios, los forks de repos Tier 0 (shadcn/ui, TanStack/router, vercel/ai) son señal de contribución OSS activa. No ignorarlos en el inventario. Son parte de la narrativa de "portfolio vivo".

**Lección:** cuando hagas inventario, incluir forks. No como proyectos, pero sí como indicadores de actividad.

### 15. antigravity-developer-stack: contenido valioso, estructura wrong
AGDS tiene 30+ patrones y playbooks con contenido real, pero es un monolito con nombre de sci-fi. El contenido merece mejor formato (skill de OpenClaw, docs site, o varios skills separados).

**Lección:** a veces el problema no es la idea sino el vehículo. AGDS no necesita más contenido, necesita reempaquetado.

### 16. ai-engineering-bootcamp no es código por rehacer, es contenido por escribir
La estructura del bootcamp está completa (10 niveles, 23 proyectos), pero todo está en "Pending". No hay código que refactorizar ni arquitectura que rediseñar — hay 23 proyectos de contenido por crear.

**Lección:** no todo lo que parece "incompleto" es un proyecto de software. A veces es un proyecto de contenido, y el approach es diferente: escribir, no programar.

---

## 2026-07-20 — Patrones de fix y humanización en OSS

### 7. Fix de una línea + defensa en profundidad en la capa contigua
Cuando un bug tiene un fix directo (un guard, un cambio de condición), siempre buscar si hay una segunda capa que también debería protegerse. En el PR #7861 de TanStack/router, el fix principal fue no tirar `undefined` cuando el `loadPromise` ya fue limpiado, pero además reforzamos `CatchBoundaryImpl` para que no dependa de la truthiness del error.

**Lección:** el fix directo resuelve el síntoma; la defensa en profundidad evita que la misma clase de error vuelva a ocurrir aunque cambie el código alrededor. Preguntarse siempre "¿qué otra cosa podría romperse de la misma manera?"

### 8. Guarda basada en ID en vez de timestamp para ordenar eventos concurrentes
Cuando necesitás determinar qué versión de un recurso es "la anterior" bajo writes concurrentes, los timestamps tienen colisiones (mismo segundo). Los IDs auto-incrementales son estrictamente monotónicos y no fallan bajo concurrencia. En el PR #17413 de payloadcms/payload, reemplazamos `updatedAt <` por `id < result.id`.

**Lección:** para ordenar eventos concurrentes, preferir un identificador monotónico (ID autoincremental, secuencia, LSN) sobre un timestamp. Los timestamps mienten bajo carga.

### 9. Cuando un bug requiere fix upstream, el valor está en el análisis, no en el workaround
Si el root cause está en otra herramienta (Vite, React, etc.), intentar un workaround desde el proyecto anfitrión suele ser frágil y difícil de mantener. En cambio, dejar un análisis técnico que explique por qué el fix anterior no cubre este caso, y señalar dónde habría que tocar, te posiciona como alguien que entiende el sistema completo.

**Lección:** no todo bug necesita un PR. A veces el mejor aporte es un comment que ahorre horas de investigación al próximo que lo agarre. El análisis vale tanto como el código.

### 10. Para bugs de concurrencia, forzar la condición, no el timing exacto
Los race conditions son difíciles de reproducir porque dependen de timing. En vez de intentar recrear el orden exacto de eventos, identificar la condición que lo causa (mismo timestamp, pending UI que se renderiza antes de que se limpie un promise, etc.) y forzarla directamente en el test.

**Lección:** no perseguir el timing — perseguir la invariante que se rompe. Una vez que sabés qué condición causa el bug, podés reproducirla deterministicamente.

### 11. Humanizar el tono en PRs y comments de OSS, especialmente si ya te confundieron con un bot
En repos donde ya te etiquetaron como bot (TanStack/router), el contenido técnico puede ser el mismo pero el tono tiene que sonar a humano. PR descriptions con formato están bien, pero los comments y respuestas deben sonar a conversación, no a informe generado.

**Lección:** en OSS de alto perfil, la percepción importa. Un PR técnicamente perfecto pero que suena a bot puede ser ignorado o rechazado. Un comment que suena a persona que realmente entendió el código genera más confianza.
