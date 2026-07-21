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

## 2026-07-20 — P09 Evaluation Lab: LLM-as-a-Judge y evaluación de prompts

### 21. El patrón LLM-as-a-Judge con 3 dimensiones es más robusto que un score único
P09 implementa un juez que evalúa respuestas en 3 dimensiones separadas: **accuracy** (precisión técnica), **completeness** (cobertura de puntos requeridos) y **tone** (adecuación del tono). El score final se recalcula server-side como promedio, no se confía en el score que devuelve el modelo.

**Lección:** cuando un LLM evalúa a otro LLM, pedir criterios separados y recalcular el agregado server-side. El modelo puede ser inconsistente en el score global pero consistente en cada dimensión por separado. Además, el clamp a [0,1] server-side evita valores fuera de rango.

### 22. Forzar JSON puro en el system prompt del juez, con validación estricta post-parse
El system prompt del juez instruye: "Respondé ÚNICAMENTE con JSON válido, sin texto adicional, sin markdown, sin backticks". Pero igual hay que hacer try/catch del parse y si falla, devolver el raw response para debugging. El error tipado `PARSE_ERROR:<detail>\n<raw>` permite debuggear sin perder contexto.

**Lección:** nunca confiar en que el modelo va a devolver JSON limpio. Siempre try/catch + raw response en el error. El patrón `validateAndNormalize()` con clamp + type checking es obligatorio.

### 23. Batch evaluation con Promise.allSettled + after() para tolerancia a fallos
El batch orchestrator corre N variantes × M test cases en paralelo. Usa `Promise.allSettled` (no `all`) para que un par fallido no cancele todo el batch. Si todos fallan → status='failed', si al menos uno funciona → status='completed'. Corre en `after()` de Next.js para responder 200 inmediato.

**Lección:** en evaluación batch, la tolerancia a fallos es crítica. Un test case mal formado no debe impedir que el resto se evalúe. `allSettled` + estado agregado (failed si todos fallaron, completed si alguno funcionó) es el patrón correcto.

### 24. Interpolación de variables en system prompts con validación de existencia
P09 usa `{{buyer_question}}` y `{{seller_context}}` como variables en los system prompts. El evaluador busca los test cases y variantes en paralelo con `Promise.allSettled`, verifica que existan, y recién entonces interpola. Si un ID no existe → 400 inmediato, no 500.

**Lección:** la interpolación de prompts debe validar que las fuentes de datos existen antes de armar el prompt. Fallar temprano con 400 es mejor que fallar en la llamada a la API con 502.

### 25. Skills de evaluación como documentación del patrón, no como código ejecutable
Los 3 skills de P09 (prompt-evaluator, llm-judge, batch-orchestrator) documentan el patrón completo: endpoint, request/response, errores, flujo de implementación, notas. Son reutilizables en cualquier proyecto que necesite evaluar prompts, sin depender del código de P09.

**Lección:** documentar patrones de IA como skills markdown (no como código) los hace portables entre proyectos. El skill describe el qué y el por qué; la implementación concreta se adapta a cada stack.

---

## 2026-07-20 — Biome: el lint que rompe CI por culpa de nuestro propio stack

### 17. Biome formatea su propio JSON de configuración — y si no lo hacés, rompe CI
`biome.json` no es un archivo de configuración pasivo. Biome lo lee **y lo lintea** con sus propias reglas de formato. Si el JSON no está formateado según las reglas de Biome (indentStyle, indentWidth, lineWidth), `biome check .` falla.

**El error concreto:** el scaffold de create-stack-next generó `biome.json` con tabs, pero la config de Biome dice `indentStyle: "space", indentWidth: 2`. Biome detecta la inconsistencia y la reporta como error.

**Fix:** correr `npx biome check --write biome.json` después de crear el proyecto. Biome se autoformatea.

**Lección para el workflow de scaffold:** el último paso del scaffold debe ser `npx biome check --write .` para que Biome deje todo consistente. Si no, el primer CI falla por una pavada.

### 18. Los componentes de shadcn/ui generan falsos positivos de a11y en Biome
`noLabelWithoutControl` se dispara en `label.tsx` de shadcn/ui porque el componente `Label` es un wrapper genérico que no tiene `htmlFor` — el control se asocia en el componente que lo usa. Es un falso positivo.

**Fix:** ignorar `src/components/ui/*` en `biome.json` > `files.ignore`. Esos componentes vienen de shadcn/ui y no deberían pasar por nuestro lint.

**Lección para el workflow de scaffold:** agregar `src/components/ui/*` a los ignores de Biome automáticamente al crear el proyecto.

### 19. Biome + shadcn/ui: el combo que siempre da problemas si no se configura desde el día 1
Cada vez que se crea un proyecto con shadcn/ui + Biome, hay que:
1. Ignorar `src/components/ui/*` en `biome.json`
2. Correr `npx biome check --write .` para que Biome se autoformatee
3. Verificar que `biome check .` pase limpio antes del primer commit

Si no se hace, el primer CI falla y perdés 10 minutos debuggeando algo que sabías que iba a pasar.

**Lección:** esto debería ser parte del workflow de scaffold, no un fix post-hoc. Agregar al checklist de creación de proyecto.

### 20. `biome check --unsafe` puede romper typecheck — revisar siempre después
El unsafe fix de Biome cambió `this.browser!.newPage()` a `this.browser?.newPage()`, lo que hizo que `page` fuera `Page | undefined`. TypeScript lo atrapó en el typecheck, pero si solo corrés `biome check --write --unsafe` sin verificar, el CI pasa lint pero falla en typecheck.

**El patrón correcto:** en vez de optional chaining, usar un guard explícito:
```ts
if (!this.browser) throw new Error('...')
const page = await this.browser.newPage()
```
Esto satisface tanto a Biome (no usa non-null assertion) como a TypeScript (page no es undefined).

**Lección:** después de `biome check --unsafe`, siempre correr `tsc --noEmit` para verificar que no introdujo errores de tipo. El unsafe fix confía en Biome, no en TypeScript.

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
