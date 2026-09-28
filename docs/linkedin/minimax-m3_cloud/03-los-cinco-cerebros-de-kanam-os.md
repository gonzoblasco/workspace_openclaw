# Art. 3 - Los 5 Cerebros de Kanam OS

> **Fuente:** ADR-073 (Arquitectura Multi-Agente)
> **Audiencia:** LinkedIn semanal - público técnico general
> **Formato:** post listo para pegar (≈ 2.400 caracteres)

---

## Versión LinkedIn (cuerpo del post)

Pongamos caras al sistema. Estos son los cinco agentes que conviven en Kanam OS:

**Kanam CORE - el estratega**
Orquesta, gobierna, decide. Tiene la visión global del workspace, mantiene la memoria compartida y la coherencia del mapa de orquestación. No escribe código: decide qué código hay que escribir. Convive con la raíz del repo.

**Kanam DEV - el ingeniero**
Software, specs y tests. Usa OpenSpec como formato primario de documentación, Vitest como framework y TypeScript en todos los tests. Cuando hay que tocar código, refactorizar, implementar una skill o validar una spec, el CORE le pasa la pelota.

**Kanam OPS - el de infra**
Gateway, CI/CD, secrets, deploys. Administra LaunchAgents, servidores y configuración del entorno. Si toca subir, asegurar o provisionar algo, este es el responsable. Tiene el radar de costos y riesgos operativos encendido todo el tiempo.

**Kanam MIND - el investigador**
Investigación, corpus y aprendizaje. Su trabajo es buscar, leer, resumir y cruzar fuentes externas - web, papers, documentación oficial - antes de que DEV u OPS actúen sobre una afirmación que no se verificó. Es el encargado del principio "el precedente no es un motivo": cada decisión se justifica hoy, no por existir desde ayer.

**Kanam STUDIO - el comunicador**
Narrativa, redacción y marca. Pasa cuando hay que escribir algo que va a salir al mundo: una spec que se publica, un post en LinkedIn, la documentación de una API. Maneja la voz de Kanam hacia afuera y la consistencia visual de los entregables.

Cada uno tiene su propio directorio bajo `agents/` y su propio set de skills cargado. Ninguno carga las skills de otro. Si DEV necesita información de MIND, MIND corre primero y devuelve un handover - no se meten en la misma sesión.

Esa es la clave: la separación no es solo organizativa. Es técnica. Cada sesión arranca con menos ruido en el prompt porque solo ve lo que necesita para su rol.

La consecuencia inesperada fue una caída sostenida en alucinaciones. No porque el modelo mejoró, sino porque dejamos de pedirle que sepa todo al mismo tiempo.

---

## Notas técnicas (no publicar)

- **Mapeo de rutas (extraído del ADR-073):**
  - `Kanam CORE` → `/workspace/` (raíz)
  - `Kanam DEV` → `/workspace/agents/kanam-dev/`
  - `Kanam OPS` → `/workspace/agents/kanam-ops/`
  - `Kanam MIND` → `/workspace/agents/kanam-mind/`
  - `Kanam STUDIO` → `/workspace/agents/kanam-studio/`
- **No publicar pistas internas** (precios de modelos, scores de benchmarks, nombres de archivos del repo, nombres de proyectos privados). Solo los roles y el "qué hace cada uno" están blindados para público.
- **Por qué agrupar así:** las cinco especialidades coinciden con los cinco buckets originales del workspace consolidado. La división sigue el uso real.
- **Pendiente honesto:** DEV/MIND comparten un subconjunto de tooling (web fetch, embeddings). Está documentado pero no necesariamente explicado en este post - ese es tema del artículo 4.

---

## Hashtags sugeridos

```
#MultiAgente #AgentesIA #LLM #IngenieríaDeSoftware #ArquitecturaDeSoftware #IA
```

---

## Por qué este post va tercero

Después de instalar el problema (art. 1) y la solución mecánica (art. 2), el lector ya se pregunta "¿y eso cómo se ve?". Este post responde a eso con el "quién es quién". El artículo 4 baja al último nivel: cómo comparten lo que saben.
