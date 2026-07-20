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
