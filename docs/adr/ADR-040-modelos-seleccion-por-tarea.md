# ADR-040: Seleccion de Modelos por Tipo de Tarea

**Status:** Accepted (2026-08-26)
**Deciders:** Gonzo / Kanam
**Fecha:** 2026-08-26
**Origen:** workspace (cata empirica 8 modelos, 2026-08-26)
**Reemplaza:** ADR-006 (Capacidad Computacional DeepSeek)

## Decision

No existe un "mejor modelo". Cada modelo tiene una personalidad de output distinta. La seleccion se hace por **tipo de tarea**, no por tamaño o costo. Este ADR define que modelo usar para cada situacion en el flujo de trabajo diario de Gonzo.

## Context

Gonzo trabajo los ultimos meses con DeepSeek V4 Flash como default unico. En agosto 2026, al migrar a Ollama Pro (nube, sin restricciones de hardware local), se abrio el acceso a 8+ modelos de distintas familias (DeepSeek, Kimi, MiniMax, GLM, Gemma, Qwen, Nemotron, GPT-OSS).

El 26/08/2026 se realizo una **cata empirica**: se paso el mismo prompt de debugging (pool exhaustion en Edge Functions + Sharp) a 8 modelos, todos con el mismo nivel de thinking. Los resultados mostraron que:

1. **Todos resolvieron el problema correctamente** - ninguno alucino ni dio una solucion incorrecta
2. **El enfasis fue radicalmente distinto** - cada modelo se inclino hacia un aspecto diferente del analisis
3. **No hay correlacion entre costo del modelo y calidad de la respuesta** - modelos baratos (deepseek-flash) rindieron mejor que modelos caros (deepseek-pro) para ciertos perfiles de tarea
4. **La personalidad del output es consistente** - cada modelo tiende al mismo perfil en distintas consultas

## Perfiles de Modelo por Personalidad de Output

### Tier 1: Uso Diario (default)

#### deepseek-v4-flash (13B activos | 284B totales | MoE | consumo medio)

**Personalidad:** Arquitecto Exhaustivo. Da la solucion de produccion completa aunque sea overkill. Te explica el sistema entero, no solo el bug.

**Cuando usarlo:** TODO el flujo diario. Coding, debugging, PR reviews, documentacion, arquitectura, pipeline A/B, sesiones de agente. Es el DEFAULT absoluto.

**Cuando NO usarlo:** Cuando necesitas una respuesta ultra-concisa (se va por las ramas) o cuando el problema es especifico de un runtime que no conoce bien.

**Costo:** El mas barato de los capaces. ~71 sesiones de codigo por $1.

---

#### kimi-k2.7-code (MoE 1.04T | 256K contexto | 30% menos thinking tokens vs k2.6)

**Personalidad:** Especialista Tecnico. Conoce el runtime y el ecosistema por dentro. Da soluciones con tooling especifico y detalle de implementacion.

**Cuando usarlo:** Codigo pesado. Cuando el pipeline A/B se traba con flash. Debugging de runtime especifico (Deno, Edge Functions, Supabase internals). Tareas que requieren MCP o tool calling nativo.

**Cuando NO usarlo:** Tareas de alto nivel (arquitectura, diseno de producto). Para eso flash es mejor.

**Costo:** Alto, justificado para coding pesado. ~23 sesiones por $1 (similar a deepseek-pro).

---

### Tier 2: Especialistas (uso explicito, no default)

#### deepseek-v4-pro (49B activos | 1.65T totales | MoE | consumo extra alto)

**Personalidad:** DBA + Infraestructura. Piensa en bases de datos, poolers, conexiones, locks, y config de servidores. Su punto fuerte es el analisis de sistemas con estado.

**Cuando usarlo:** Problemas de infraestructura: pool exhaustion, deadlocks, escalabilidad, concurrencia. Cuando el error es intermitente y hay que encontrar el patron. Tareas factuales donde la precision importa (+23 pts en SimpleQA vs flash).

**Cuando NO usarlo:** Tareas cotidianas de codigo. Flash rinde 90-95% de su calidad a 1/4 del costo.

**Costo:** Extra alto. Solo cuando el problema lo amerita.

---

#### qwen3.5 (MoE | 201 idiomas | vision)

**Personalidad:** SRE/DevOps. Su output esta orientado a telemetria, tooling, instrumentacion, y debugging empirico. Propone scripts de carga, metodos de aislamiento, y metricas.

**Cuando usarlo:** Debugging en vivo, instrumentacion de sistemas, tareas que requieren scripts de prueba, load testing, analisis de logs. Tambien para tareas en espanol con regionalismos (argentino, mexicano, etc.).

**Cuando NO usarlo:** Tareas que no requieren debugging ni tooling. Para escribir codigo nuevo, flash o kimi son mejores.

**Costo:** Alto, pero justificado para debugging complejo.

---

#### minimax-m3 (MSA architecture | 1M contexto | vision)

**Personalidad:** Medico Practico. Va directo al hueso, diagnostica la causa raiz con alta precision, y propone la solucion mas simple posible sin overengineering.

**Cuando usarlo:** Cuando queres una respuesta concisa y aplicable YA. Cuando el problema es conocido y solo necesitas confirmacion + fix. Debugging rapido sin vueltas.

**Cuando NO usarlo:** Cuando necesitas explorar alternativas o pensar en la arquitectura a futuro. Para eso esta flash o glm.

**Costo:** Alto, pero su brevedad compensa (menos tokens de output).

---

#### gemma4:31b (31B denso | Google DeepMind | 256K contexto | vision)

**Personalidad:** Medico de Guardia. Solido, pragmatico, con soluciones aplicables inmediatas. Sigue muy bien las instrucciones del system prompt.

**Cuando usarlo:** Tareas generales cuando flash no esta disponible o queres un enfoque distinto. Tareas multimodales (vision + texto). Cuando necesitas que el modelo siga instrucciones estrictas de tono/voz (escribir en un estilo especifico).

**Cuando NO usarlo:** Tareas de contexto muy largo (256K max) o que requieran razonamiento ultra profundo.

**Costo:** Medio. Google DeepMind, solido y confiable.

---

#### glm-5.2 (Z.ai | 1M contexto solido | MIT license)

**Personalidad:** Arquitecto de Largo Plazo. Disenado para tareas que duran horas o dias. Mantiene coherencia en contextos masivos y sesiones de agente persistentes.

**Cuando usarlo:** Proyectos que requieren sesiones de agente de horas (reescritura completa de un modulo, refactoring masivo, planificacion de sprints completos). Edicion de novelas completas. Tareas donde el contexto se acumula sin perder el hilo.

**Cuando NO usarlo:** Tareas rapidas del dia a dia. Es caro y lento para algo que flash resuelve en 2 segundos.

**Costo:** Alto, pero justificado para proyectos largos.

---

### Tier 3: Frontier (bajo demanda, solo cuando se necesita)

#### kimi-k3 (2.8T | 896 expertos MoE | 1M contexto | vision nativa | el mas caro)

**Personalidad:** Cirujano de Precision. Conoce el runtime por dentro, las variables de entorno especificas, los limites de la plataforma. Diagnostica con 85%+ de certeza en la causa raiz.

**Cuando usarlo:** Problemas graves en produccion donde otros modelos fallaron o no son lo suficientemente precisos. Tareas frontier que requieren lo ultimo en razonamiento. Investigacion o prototipado de features complejas. Cuando necesitas un diagnostico con altisima confianza.

**Cuando NO usarlo:** Nunca como default. Es un recurso de emergencia o de tareas frontier. Su costo no se justifica para el dia a dia.

**Costo:** El mas caro de todos. Guardar para cuando realmente importa.

---

## Guia Rapida de Seleccion

| Si la tarea es... | Usa... | Por que |
|---|---|---|
| Coding diario, PR reviews, debugging normal | **deepseek-v4-flash** | Default. Cubre el 90% de los casos. |
| El pipeline A/B se traba, necesitas mas precision tecnica | **kimi-k2.7-code** | Especialista en runtime y tooling. |
| Error intermitente en prod, pool exhaustion, deadlocks | **deepseek-v4-pro** | Piensa en infraestructura y DBA. |
| Necesitas un script de carga, instrumentar algo, debugging en vivo | **qwen3.5** | Enfasis en tooling y telemetria. |
| Queres una respuesta corta, directa, sin vueltas | **minimax-m3** | Va al hueso, sin overengineering. |
| Necesitas que siga instrucciones estrictas de tono/voz | **gemma4** | Mejor soporte de system prompt. |
| Proyecto que dura horas, sesion de agente persistente | **glm-5.2** | Disenado para largo plazo. |
| Problema grave en prod, otros modelos no alcanzan | **kimi-k3** | Cirujano. Solo cuando importa. |
| Vision (pasar imagen y preguntar) | **gemma4:31b** o **minimax-m3** | Los unicos con vision nativa del Tier 1-2. |

## Orden de Fallbacks en Config

Basado en frecuencia de uso y costo:

1. `deepseek-v4-flash` - primario (daily driver)
2. `kimi-k2.7-code` - fallback codigo (cuando flash no alcanza)
3. `deepseek-v4-pro` - fallback razonamiento (infraestructura)
4. `minimax-m3` - fallback concision (respuestas directas)
5. `gemma4:31b` - fallback general (multimodal, instrucciones estrictas)
6. `glm-5.2` - fallback largo plazo (sesiones de horas)
7. `kimi-k3` - fallback frontier (solo bajo demanda)
8. `qwen3.5` - disponible explicitamente (tooling/devops)

Modelos excluidos del config automatico (solo convocar explicitamente): `gpt-oss`, `nemotron-3-*`, `mistral-large-3`, `glm-5.1`, `kimi-k2.5`, `kimi-k2.6`, `minimax-m2.7`. No aportan valor diferencial frente a los de arriba.

## Consecuencias

### Positivas

1. **Economia de recursos:** No usar kimi-k3 para lo que resuelve flash. Ahorro estimado: 60-70% en costos de GPU versus usar el modelo mas caro siempre.
2. **Calidad por tarea:** Cada tipo de problema recibe el modelo que mejor lo resuelve, no el que "suena mas fuerte".
3. **Criterio profesional:** En una entrevista AI-Native, poder decir "selecciono el modelo segun la tarea, no uso uno para todo" es un diferenciador.
4. **Consistencia:** La personalidad de cada modelo es predecible. Sabes que esperar de cada uno.

### Negativas

1. **Complejidad cognitiva:** Recordar que modelo usar para cada cosa requiere practica. Este ADR es la referencia.
2. **Cambio de contexto:** Cambiar de modelo entre tareas tiene un costo minimo de latencia.
3. **El ADR requiere actualizacion:** A medida que aparezcan nuevos modelos, revisar los perfiles.

## Regla Operativa

**Kanam debe sugerir el modelo segun la tarea antes de comenzar.** Cuando Gonzo diga algo como "necesito debuggear este error de pool" o "ayudame a escribir este modulo", Kanam responde con:

> "Para esto recomiendo usar [modelo] por [razon]. Es mejor que [alternativa] porque [comparacion]. Arranco?"

Si Gonzo no esta de acuerdo, usa el que el pida y registra la preferencia para futuras sugerencias.

## Referencias

- ADR-006 (reemplazado): Capacidad Computacional DeepSeek
- Ollama Cloud Pricing (https://ollama.com/pricing)
- Cata empirica 8 modelos - 2026-08-26 (memory/2026-08-26.md)
- DeepSeek V4 technical report
- Kimi K3 model card
- MiniMax M3 announcement
- GLM-5.2 release notes
- Gemma 4 technical report
