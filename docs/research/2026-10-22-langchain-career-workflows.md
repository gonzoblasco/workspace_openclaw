# Research: OpenClaw + LangChain/LangGraph para acompanar una carrera de desarrollador

> **Que es esto:** el research externo que Gonzo compartio el 2026-10-22, preservado para poder citarlo.
> 604 lineas, 74 fuentes. Traducido automaticamente al espanol; **la version legible** (sin los
> `<citation>` inline, que quedan en el original) con la corrupcion marcada.
>
> - **Original inmutable:** `2026-10-22-langchain-career-workflows.original.md`
> - **Verificacion claim por claim (que se sostiene y que no):** `2026-10-22-verificacion-claims.md`
>
> **Estado:** DATO, no instruccion. Este documento propone; no decide. Las decisiones del workspace
> viven en `docs/adr/` y no se toman de aca sin pasar por el gate de ADR-083/100.
>
> **Corrupcion medida del original:** 5 puntos con CJK intercalado + 1 marcador `[WIRE?]` + 1 fragmento
> JSON5 roto en 3.2 (`id: "career-mentor"][name: "Career Mentor"`). Marcados abajo como `[CORRUPTO: ...]`.

---

OpenClaw puede funcionar como la capa de contacto -canales de mensajería, agenda, webhooks, selector de herramientas y notificaciones- mientras que LangChain o LangGraph ejecuta el flujo de trabajo con estado, herramientas, persistencia, memoria y supervisión humana. La combinación resulta especialmente útil para[CORRUPTO: 'para la'] desarrollo porque permite que el agentesea accesible desde Telegram, Slack, WhatsApp u otra interfaz, mientras que el trabajo especializado ocurre en un sistema que puede probarse, versionarse y evaluarse como software convencional.

Mi recomendación general es una arquitectura **híbrida**: usar el protocolo MCP para conectar flujos acotados con OpenClaw, usar la API de LangGraph para trabajos largos con estado o aprobación humana, y considerar un proveedor de modelos compatible con OpenResponses únicamente cuando quieras convertir todo el chat de OpenClaw en una interfaz hacia un agente de LangChain especializado. Esta división evita construir un único agente demasiado grande y, al mismo tiempo, permite que cada flujo tenga sus propias herramientas, políticas, pruebas y registros de ejecución.

## 1. Aclaración conceptual: qué es un flujo de trabajo en cada sistema

OpenClaw no tiene un comando especial `openclaw workflows`; sus mecanismos principales son **automatizaciones**, **habilidades**, **enganches internos**, **plugins**, **subagentes** y conexiones MCP. Una automatización define *cuándo* debe ejecutarse un trabajo, una habilidad define *cómo* debe_guidar el agente, un enganche reacciona a un evento interno y un plugin agrega capacidades de ejecución.

LangChain, por su parte, ofrece un arnés de agente basado en un modelo que llama herramientas en un ciclo hasta completar una tarea, con opciones para incorporar промпты, herramientas, estado, salida estructurada y middleware. LangGraph aporta un entorno de ejecución de flujos con nodos, transiciones, estado persistente, reanudación, intervención humana y observabilidad. Deep Agents añade una experiencia más completa para archivos, memoria, habilidades y subagentes, por lo que resulta especialmente conveniente para un mentor de aprendizaje.

Una regla mental útil es la siguiente:

- **Automatización** significa cuándo ejecutar.
- **Habilidad** significa qué procedimiento reutilizable debe seguir el agente.
- **Standing order** significa qué autoridad, límites y escalamiento aplica.
- **Plugin o MCP** significa qué herramientas puede utilizar.
- **LangGraph** significa cómo se coordina el trabajo, se guarda el estado y se retoma una ejecución.
- **LangSmith** significa cómo se observan y evalúan las ejecuciones.

## 2. Arquitectura general recomendada

La siguiente composición separa las responsabilidades y evita que OpenClaw y LangGraph duplicen accidentalmente la misma programmedación.

```text
WhatsApp / Slack / Telegram / Discord / CLI
                    │
                    ▼
              OpenClaw Gateway
                    │
         ┌──────────┼───────────┐
         ▼          ▼           ▼
      Habilidad   Automatización  Webhook
         │          │           │
         └──────────┼───────────┘
                    ▼
             Router de flujos
                    │
      ┌─────────────┼────────────────┐
      ▼             ▼                ▼
 MCP corto      API LangGraph     OpenResponses
workflow        largo/estado      conversacional
      │             │                │
      └─────────────┴────────────────┘
                    ▼
             LangGraph / Deep Agents
                    │
          Modelos, RAG, memoria,
        herramientas, checkpoints
                    │
                    ▼
                LangSmith
```

| Capa | Responsabilidad recomendada | Fundamento |
|---|---|---|
| OpenClaw | Captar intenciones, recibir eventos, programar trabajos,-selected herramientas y entregar resultados | Es la capa más cerca de la persona usuaria |
| Habilidad de OpenClaw | Describir cuándo usar cada flujo y qué datos entregarle | Las habilidades son instrucciones operativas reutilizables |
| MCP | Exponer flujos de LangGraph como herramientas descubribles | Agent Server publica agentes como herramientas MCP |
| LangGraph | Coordinar nodos, herramientas, memoria, persistencia, interrupciones y reanudaciones | Proporciona control fino sobre el flujo |
| Deep Agents | Aportar memoria, habilidades y subagentes con una configuración relativamente sencilla | Es una opción con más abstrações[CORRUPTO: marcador ilegible del original] |
| LangSmith | Registrar ejecuciones, costos, pasos, herramientas, latencias y evaluaciones | Despliegues y ejecuciones quedan conectados a trazas |

## 3. Cuatro formas de disparar workflows de LangChain o LangGraph desde OpenClaw

### 3.1. MCP: la opción más natural para flujos acotados

LangGraph Agent Server expone su endpoint `/mcp` mediante transporte HTTP en streaming, y cada agente desplegado aparece como una herramienta MCP cuyo nombre corresponde al nombre del agente y cuyo esquema de entrada deriva del agente. La implementación actual es sin sesión, por lo que cada solicitud MCP es independiente y no sustituye automáticamente a los hilos persistentes de LangGraph.

OpenClaw funciona como cliente MCP nativo: puede registrar servidores guardados bajo `mcp.servers`, aplicar filtros de herramientas, iniciar sesión con OAuth, verificar conexiones y limitar qué servidores o herramientas puede utilizar cada agente. Por esta razón, esta integración resulta especialmente útil para flujos como un plan de aprendizaje, una explicación de código o una revisión de un cambio.

La forma documentada de registro es la siguiente.

```bash
openclaw mcp add career-workflows \
  --url "https://agents.example.com/mcp" \
  --transport streamable-http \
  --include "career_mentor,repo_tutor,pr_reviewer"
```

Los nombres incluidos deben corresponder a herramientas reales publicadas por el servidor MCP, y en LangGraph el nombre de la herramienta coincide con el nombre del agente. Si el servidor utiliza OAuth y la autorización aún no existe, la fase de prueba del registro puede omitirse hasta completar el inicio de sesión.

Después debe verificarse que el servidor no solo esté guardado, sino que realmente responda y publique las herramientas esperadas.

```bash
openclaw mcp doctor career-workflows --probe
openclaw mcp probe career-workflows --json
```

Las mutaciones del registro y algunas operaciones de autenticación requieren que el Gateway local esté detenido, mientras que la inspección básica puede ejecutarse con el Gateway activo. Una vez conectado, OpenClaw aplica los mismos filtros de perfil, listas permitidas, denegaciones por agente, políticas de proveedor y reglas del entorno aislado que usa con sus demás herramientas.

**Cuándo elegir MCP:**

- Cuando cada solicitud deba producir un resultado relativamente autocontenido.
- Cuando quieras que OpenClaw pueda discoverar y aplicar una colección de flujos.
- Cuando el flujo completo deba quedar encapsulado detrás de una interfaz de herramienta.
- Cuando no quieras que OpenClaw administer directamente el estado interno de una ejecución larga.

**Cuándo no elegir MCP como único mecanismo:**

- Cuando el flujo deba pausarse durante horas o días esperando una aprobación.
- Cuando necesite conservar un hilo largo con múltiples interacciones.
- Cuando necesite reanudación después de una caída en medio de una tarea.
- Cuando un mismo trabajo deba continuar después de que OpenClaw cierre la conversación.

### 3.2. Adaptador OpenResponses: OpenClaw como interfaz conversacional completa

Si quieres que **toda** la conversación de OpenClaw se procese dentro de un agente de LangChain, puedes exponer ese agente mediante una API compatible con `POST /v1/responses` y registrarla como un proveedor de modelos de OpenClaw. El adaptador recibe el mensaje normalizado de OpenClaw, lo entrega al agente de LangChain y devuelve una respuesta compatible con OpenResponses, tanto en formato normal como mediante Server-Sent Events.

La configuración mínima tendría esta forma.

```json5
{
  models: {
    mode: "merge",
    providers: {
      "career-backend": {
        baseUrl: "https://agents.example.com/v1",
        api: "openai-responses",
        apiKey: "${CAREER_BACKEND_API_KEY}",
        models: [{
            id: "career-mentor"][name: "Career Mentor"
          }]
      }
    }
  }
}
```

El `baseUrl` debe incluir `/v1` porque OpenClaw añade la ruta `/responses`, y el adaptador `openai-responses` debe ser utilizado únicamente cuando el servicio remoto implemente realmente ese contrato. El contrato no trivial debe producir un arreglo `output` con un mensaje del asistente y métricas de uso, mientras que el modo de flujo debe emitir los eventos `response.created`, `output_item.added`, `content_part.added`, `output_text.delta`, `output_text.done`, `output_item.done`, `response.completed` y `[DONE]`.

Este camino es útil cuando la conversación completa debe tener memoria, herramientas propias y respuestas en tiempo real. En cambio, tiene una disadvantage arquitectónica: si toda la conversación se delega al servicio externo, OpenClaw deja de controlar directamente qué herramientas nativas se presentan al modelo en cada turno.

Si el servicio remoto solo ofrece Chat Completions, también puede construirse un adaptador FastAPI, pero LangServe no debería ser la base de una solución nueva porque fue marcado como obsoleto y sus propios documentos recomiendan LangGraph Platform para aplicaciones nuevas.

### 3.3. API y SDK de LangGraph: opción para procesos largos y con estado

Para un flujo largo conviene crear un hilo, asociarlo con un asistente, iniciar una ejecución y conservar el `thread_id` para consultas o reanudaciones posteriores. El SDK de Python permite trabajar con clientes síncronos y asíncronos, administrar asistentes, hilos y ejecuciones, y establecer la URL del servidor.

Un patrón de invocación de alto nivel es el siguiente.

```python
from langgraph_sdk import get_client

client = get_client(url="https://agents.example.com")

thread = await client.threads.create()
stream = client.runs.stream(
    thread["thread_id"],
    "career-mentor",
    input={
        "messages": [{
                "role": "user"]["content": "Diseña una sesión de práctica sobre closures en JavaScript."
            }]
    },
)

async for chunk in stream:
    print(chunk)
```

El SDK también permite esperar una ejecución mediante `POST /threads/{thread_id}/runs/wait`, enviando el identificador del asistente, la entrada, el contexto, la configuración, el modo de flujo, la estrategia para tareas concurrentes y opciones de durabilidad. Las ejecuciones pueden pausarse con `interrupt()` y reanudarse con `Command(resume=...)` utilizando el mismo `thread_id`.

OpenClaw puede activar este recorrido desde una automatización programada mediante un comando o un script. Sin embargo, la ejecución de comandos de host puede desactivarse arrancando el Gateway con `OPENCLAW_DISABLE_CRON_HOST_EXECUTION=1`; en ese modo se rechazan comandos, condiciones y cargas útiles de scripts, aunque se conservan los turnos de agente programados.

Por ello, la recomendación operativa es:

- Usar MCP para los flujos breves y conversacionales.
- Usar la API de LangGraph para los procesos largos, approvals y trabajo por lotes.
- Usar una automatización de OpenClaw para iniciar la llamada, y el SDK de LangGraph para manejar la sesión, el estado y la reanudación.

### 3.4. Flujo inverso: LangGraph notifica o invoca OpenClaw

En algunos casos, el flujo de LangGraph debe devolver el resultado a una conversación de OpenClaw o iniciar una acción autorizada en el Gateway. La superficie `POST /tools/invoke` permite invocar una herramienta directamente mediante autenticación del Gateway y políticas de herramientas.

Sin embargo, esa superficie tiene una lista de prohibición predeterminada que incluye `exec`, `spawn`, `shell`, operaciones de escritura y movimiento de archivos, `apply_patch`, creación y envío de sesiones, `cron`, `gateway` y `nodes`. Por ello, no debe utilizarse como atajo para permitir que un flujo de LangGraph ejecute acciones arbitrarias en el host.

El uso razonable consiste en que LangGraph devuelva un resultado estructurado a un servicio de notificación, o que invoque únicamente herramientas de entrega previamente habilitadas y autorizadas. En operaciones de publicación, compras, eliminación, cambios en producción o envíos externos debe existir una aprobación humana explícita.

## 4. Catálogo de workflows útiles para una carrera de desarrollo

### 4.1. Mentor diario de aprendizaje

Este flujo puede convertir una meta profesional en un plan pequeño, ejecutable y verificable. La entrada podría incluir el puesto objetivo, horas semanales, tecnologías actuales, límites de tiempo y nivel de dificultad deseado.

Un diseño razonable tendría estos pasos:

1. Identificar el puesto, las competencias y el nivel actual.
2. Detectar brechas y clasificarlas por impacto, urgencia y dificultad.
3. Crear una sesión diaria de entre veinte y sesenta minutos.
4. Alternar teoría, ejercicio, lectura de código y práctica deliberada.
5. Generar una pregunta de recuperación y un ejercicio verificable.
6. Evaluar la respuesta y ajustar el siguiente paso.
7. Guardar preferencias, conceptos dominados y errores recurrentes con alcance por usuario.
8. Programar repasos y actualizar el mapa de competencias.

Deep Agents es una buena elección para este flujo porque combina memoria en archivos, habilidades, carga progresiva de instrucciones y subagentes especializados. LangGraph resulta mejor si cada sesión debe seguir una máquina de estados estricta, guardar un punto de control por etapa y.Sortear la aprobación humana antes de cambiar el plan.

**Resultado esperado:** un resumen diario pequeño, un ejercicio concreto, una pregunta de comprobación y una evidencia de avance, en lugar de una lista interminable de cursos.

### 4.2. Tutor del repositorio con recuperación semántica

Este workflow puede responder preguntas sobre un repositorio sin enviar todo el código al modelo. El proceso de indexación puede utilizar Tree-sitter para extraer clases, funciones y métodos, conservar el archivo, la ubicación y el código fuente, generar inserciones y guardarlas con sus metadatos.

El grafo de ejecución podría seguir esta secuencia:

1. Recibir una pregunta sobre autenticación, arquitectura, una clase o un flujo de datos.
2. Determinar si la pregunta necesita explicación, navegación, modificación o diagnóstico.
3. Recuperar fragmentos sintácticamente relevantes y sus referencias.
4. Explicar la respuesta citando archivos, funciones y líneas.
5. Generar un ejercicio basado en el código real.
6. Proponer una prueba que el estudiante pueda ejecutar.
7. Conservar el historial temático y las preguntas todavía abiertas.

Un ejemplo de pregunta sería “¿Dónde se valida el permiso antes de modificar un recurso?” o “¿Qué archivos participate en la rotación de tokens?”. La respuesta debe distinguir hechos recuperados del código, inferencias y recomendaciones.

### 4.3. Revisor de código y pull requests

OpenClaw incluye un lector de GitHub para repositorios públicos que puede mostrar problemas, solicitudes de cambio, confirmaciones, archivos, diferencias, comentarios y estados de verificación, pero no puede publicar comentarios, editar, mezclar ni aprobar cambios. Por eso, su función natural es reunir evidencia y optionally activar un flujo de revisión, no reemplazar por sí solo la autorización de escritura en GitHub.

LangGraph permite un revisor avanzado basado en cuatro estrategias:

- **WRITE:** guardar diferencias y notas intermedias en un scratchpad y puntos de control.
- **SELECT:** recuperar solo normas internas y patrones de revisión relevantes.
- **COMPRESS:** agrupar hallazgos en problemas críticos, mejoras y sugerencias menores.
- **ISOLATE:** ejecutar revisiones separadas de seguridad, rendimiento y estilo.

El flujo podría ser:

1. Recibir la referencia de la solicitud de cambio mediante una habilidad, un webhook o un comando.
2. Obtener diferencias, contexto y estado de verificación.
3. Recuperar normas del proyecto y patrones históricos.
4. Ejecutar agentes aislados para seguridad, rendimiento, estilo y pruebas.
5. Comprimir los hallazgos sin perder acciones ejecutables.
6. Presentar cada hallazgo con evidencia y nivel de severidad.
7. Pedir aprobación antes de comentar, etiquetar o modificar código.
8. Conservar únicamente patrones validados, no el historial completo sin procesar.

El disparador más directo para unaPull Request es un webhook externo autenticado, como un evento del repositorio, pero OpenClaw debe mantener un token dedicado, aceptar solamente `POST`, aplicar idempotencia y devolver una confirmación de admisión antes de que el trabajo termine.

### 4.4. Agente de proyectos y portafolio

Este workflow puede convertir una idea en una especificación, una arquitectura, tareas, implementación, pruebas, revisión y documentación. Open SWE ofrece un buen patrón de referencia con un gerente que inicializa y enruta el trabajo, un planificador que investiga, un programador que implementa y un revisor que valida antes de abrir una Pull Request.

Una versión para tu carrera podría ser:

1. Recibir la meta, por ejemplo “construir un gestor de órdenes con FastAPI y React”.
2. Generar criterios de aceptación y una arquitectura Justificada.
3. Dividir el trabajo en un grafo de tareas.
4. Implementar cada tarea en un entorno aislado.
5. Ejecutar pruebas, formateadores y análisis de seguridad.
6. Pedir una revisión especializada.
7. Corregir los hallazgos y repetir el ciclo.
8. Preparar una Pull Request y una explicación para la portafolio.
9. Archivar decisiones, métricas y，[CORRUPTO: 'archivar']?lecciones aprendidas para reutilizarlas.

El resultado final debe ser un proyecto verificable, no únicamente una respuesta larguísima, porque la evidencia técnica es la que puede.shieldsar tu portafolio.

### 4.5. Simulador de entrevistas técnicas

El flujo puede alternar rol de entrevistador, evaluador y coach, con el entrevistador，[CORRUPTO: 'intercambio'] conversational y el evaluador trabajando en un contexto aislado.

El diseño recomendado es:

- El entrevistador formula una pregunta según el puesto y el nivel.
- El entrevistado responde en un canal normal de OpenClaw.
- El evaluador compara la respuesta con una rúbrica de diseño, implementación, pruebas y comunicación.
- El coach explica los vacíos y propone ejercicios.
- El planificador decide la siguiente pregunta.
- El supervisor decide si cambiar de especialidad o continuar con la misma.

Un supervisor es más conveniente que un enjambre libre cuando hay dependencias entre preguntas, evaluación acumulativa y necesidad de mantener coherencia. Un enjambre es más útil para evaluaciones paralelas e independientes, como diez simulaciones de entrevistas con personas técnicas diferentes.

### 4.6. Analizador de ajuste con ofertas de empleo

Este flujo puede comparar ofertas, currículum, repositorios y resultados de evaluaciones para producir una matriz de brechas. Las ofertas pueden fournirsele manualmente, mantenerse en una carpeta local o leerse mediante el navegador en páginas autorizadas.

El flujo puede producir:

- Porcentaje de coincidencia por competencia.
- Competencias que ya dominas, parciales o ausentes.
- Proyectos concretos para cerrar cada brecha.
- Errores frecuentes en entrevistas.
- Vocabulario y conceptos que debes repasar.
- Una lista de esfuerzo, prioridad y resultado esperado.

El buscador no debería publicar solicitudes, enviar cartas ni tomar decisiones finales; esas acciones deben permanecer bajo revisión humana. El análisis puede[CORRUPTO: 'practicamente'] generarse con RAG, indexando descripciones de puesto y[CORRUPTO: 'los datos'] de carrera con metadatos de fuente y fecha.

### 4.7. Asistente de depuración y incidentes

LangGraph es Particularly suitable for this task because checkpointers preserve the state at each super-step, retain successful writes from failed branches and allow recovery from the last successful step. The workflow could include:

1. Recopilar Symptoms, logs, stack traces and recent changes.
2. Formulate ranked hypotheses.
3. Design a minimal reproduction.
4. Execute controlled diagnostics.
5. Apply a provisional fix in an isolated environment.
6. Run regression and load tests.
7. Compare results against the previous baseline.
8. Prepare a causal explanation and patch for approval.
9. Record the incident and prevention measures.

Any side effect executed before an `interrupt()` must be idempotent, because the node restarts from its beginning when the run resumes. That is particularly important if the workflow sends messages, opens issues or modifies external systems.

### 4.8. Coach de contribuciones de código abierto

OpenClaw’s public GitHub integration can search up to 20 issues or pull requests per call, ordered by most recent activity, and supports pagination and completeness indicators. This allows designing a coach that selects an approachable issue, analyzes the repository, explains the required changes, creates a study plan and prepares a contribution locally.

Because the public integration is read-only, any comment, Pull Request or merge must be a separate explicit phase with human approval. The workflow should evaluate more than technical feasibility: it must also consider maintenance activity, issue clarity, contribution rules, testability and fit with the owner’s roadmap.

## 5. Priorización recomendada

The following complexity rating is my own assessment based on the documented capabilities, not a metric published by either project.

| Flujo | Valor principal estimado | Complejidad estimada | Orden |
|---|---|---:|---:|
| Mentor diario | Crea una rutina sostenible de estudio y evidencia | Baja | 1 |
| Tutor del repositorio | Convierte el código real en material educativo | Media | 2 |
| Revisor de código | Mejora la calidad del trabajo antes de publicarlo | Media-alta | 3 |
| Proyectos de portafolio | Produce resultados demostrables y explicables | Media-alta | 4 |
| Simulador de entrevistas | Entrena razonamiento, comunicación y detección de vacíos | Media | 5 |
| Analizador de ofertas | Alinea el aprendizaje con oportunidades concretas | Media | 6 |
| Depuración e incidentes | Practica diagnóstico, pruebas y prevención | Alta | 7 |
| Coach de código abierto | Entrena contribución, lectura y colaboración | Media | 8 |

Esta priorización intenta comenzar con workflows que produzcan resultados visibles rápidamente, pero que también anderungen la architecture needed for the more advanced flows.

## 6. Diseño técnico del primer MVP

### 6.1. Lado LangGraph

La primera versión puede exponer tres agentes independientes:

- `career_mentor`: diagnóstico, plan, ejercicio y seguimiento.
- `repo_tutor`: recuperación de código, explicación y práctica.
- `pr_reviewer`: auditoría de cambios y recomendaciones.

Los nombres y descripciones de los agentes pueden establecerse en `langgraph.json` y actualizarse después mediante el SDK. El servidor debe desplegarse con autenticación y, si se exposición fuera del equipo, HTTPS y un control de acceso específico.

Para desarrollo, `langgraph dev` puede levantar el Agent Server con almacenamiento en memoria, mientras que producción requiere almacenamiento persistente. El endpoint MCP requiere `langgraph-api>=0.2.3` y `langgraph-sdk>=0.1.61`.

Los grafos de estado deben guardar, como mínimo:

- Identificador de usuario o equipo.
- Objetivo profesional.
- Hilo de conversación.
- Estado del plan.
- Material recuperado y sus referencias.
- Ejercicios realizados.
- Hallazgos y decisiones.
- Aprobaciones pendientes.
- Errores y reintentos.

### 6.2. Conexión desde OpenClaw

El flujo de configuración recomendado es.

```bash
# El Gateway local debe estar detenido durante la mutación.
openclaw mcp add career-workflows \
  --url "https://agents.example.com/mcp" \
  --transport streamable-http \
  --auth oauth

# Si la autorización OAuth quedó pendiente, iniciar sesión.
openclaw mcp login career-workflows

# Comprobar conexión, herramientas y capacidades reales.
openclaw mcp doctor career-workflows --probe
openclaw mcp probe career-workflows --json
```

Después deben revisarse las políticas de herramientas y los permisos del agente que utilizará el servidor. Una lista permitida demasiado restrictiva puede dejar al agente sin ninguna herramienta invocable, por lo que conviene verificar el resultado con `openclaw agents list --bindings` y con una solicitud de prueba.

Si el catálogo MCP tiene muchas herramientas, puede habilitarse la búsqueda estructurada de herramientas para no enviar todos los esquemas al modelo desde el primer turno. Esa capacidad permite descubrir una herramienta, describirla completamente y despacharla, pero las herramientas MCP de origen no confiables deben describirse antes de invocarlas.

### 6.3. Habilidad de OpenClaw

La habilidad no debe contener toda la lógica del workflow, sino que debe actuar como router, indicar cuándo usar cada herramienta y establecer el formato de salida.

Un ejemplo de `SKILL.md` sería.

```markdown
---
name: career-dev
description: Planifica aprendizaje, explica repositorios y revisa cambios de código.
user-invocable: true
---

Cuando el usuario solicite una ruta de aprendizaje:
1. Identificar puesto objetivo, tiempo disponible y nivel actual.
2. Usar la herramienta de mentor de carrera.
3. Presentar una meta, una actividad, una evidencia y el siguiente paso.

Cuando el usuario pregunte sobre el repositorio:
1. Usar la herramienta de tutor del repositorio.
2. Incluir referencias a archivos y funciones.
3. Separar hechos, inferencias y recomendaciones.

Cuando el usuario solicite una revisión:
1. Usar la herramienta de revisor de código.
2. Mostrar severidad, evidencia y acción sugerida.
3. No publicar comentarios ni modificar código sin aprobación.
```

La habilidad puede invocarse explícitamente con `$career-dev` o `/career-dev`, y también puede ser detectada por el modelo cuando la solicitud coincida con su descripción. Las habilidades son instrucciones; las operaciones reales de indexación, ejecución de pruebas, recuperación semántica o revisión deben vivir en LangGraph, MCP o un plugin.

### 6.4. Automatización diaria

Una automatización puede solicitar el resumen diario y anunciarlo en el canal configurado.

```bash
openclaw automations create "0 8 * * 1-5" \
  "Ejecuta el mentor diario usando el plan vigente. \
  Devuelve una meta concreta, un ejercicio, una pregunta de comprobación \
  y la evidencia que debe conservar el usuario." \
  --name "plan-diario-carrera" \
  --tz "America/Bogota" \
  --session isolated \
  --announce
```

La zona horaria debe reemplazarse por la zona IANA correspondiente al usuario. La automatización puede invocar una herramienta MCP o una habilidad dentro de OpenClaw, mientras que las reglas permanentes -rol, límites,Material permitido y reglas de escalamiento- deben residir en `AGENTS.md` como standing order.

Esta separación evita duplicar instrucciones y permite modificar la cadencia sin reescribir la autoridad del agente.

### 6.5. Webhooks para eventos externos

Un repositorio, una prueba de código o un sistema de seguimiento puede iniciar un trabajo mediante `POST /hooks/agent`. Un token dedicado, una clave de idempotencia y un límite de espera hacen que la integración sea más segura.

La forma conceptual es.

```bash
curl --include http://127.0.0.1:18789/hooks/agent \
  -H 'Authorization: Bearer <token-de-hook>' \
  -H 'Content-Type: application/json' \
  -H 'Idempotency-Key: revision-2026-001' \
  --data '{
    "message": "Revisa la pull request 184 y genera hallazgos priorizados.",
    "agentId": "main",
    "deliver": false
  }'
```

Una respuesta `200` con `runId` confirma la admisión del trabajo, no que el modelo haya terminado ni que el resultado haya sido entregado. Si se requiere una respuesta sincrónica, puede activarse `waitForCompletion`, aunque la propia documentación advierte que la respuesta no expone el texto generado.

## 7. Evaluación: cómo demostrar que los workflows realmente ayudan

La usefulness de a career assistant should not be measured only by the number of responses, but by evidence of learning and work quality. LangSmith can record model calls, tool calls, intermediate steps, costs, latency, errors and feedback, while a custom evaluation dataset can test the consistency of the final responses.

For the mentor flow, useful metrics include.

- Percentage of sessions with a completed exercise.
- Retention in the next session’s recall.
- Error rate in technical questions.
- Time spent searching for resources.
- Number of concepts applied to a real repository.
- Changes in the skill-gap map over time.

For the repository tutor and reviewer, useful metrics include.

- Accuracy of file and function references.
- Recall of relevant code.
- Precision of reported vulnerabilities.
- False-positive rate.
- Percentage of findings accompanied by reproducible evidence.
- Test pass rate after applying a proposed change.
- Reduction in tokens and execution time compared with a single-agent baseline.

For the project builder, the most valuable evidence is usually a functional project, a passing test suite, an architecture explanation, a Pull Request and a retrospective. The workflow should not claim that it has learned a technology merely because the user read a generated summary.

## 8. Seguridad, permisos y privacidad

### Autenticación y red

OpenClaw enlaza el Gateway al bucle local por defecto y expone la superficie HTTP en el mismo puerto multiplexado que WebSocket y las APIs. El endpoint `/tools/invoke` exige autenticación y política de herramientas, y no debe exponerse directamente a Internet. El endpoint MCP de Agent Server utiliza la autenticación del servidor de agentes, de modo que conviene utilizar OAuth o un mecanismo equivalente antes de exponerlo.

### Privilegios mínimos

Cada agente debe tener una lista explícita de herramientas MCP permitidas y una denegación de herramientas peligrosas. Las listas pueden utilizar nombres con prefijo del servidor y comodines para excluir familias completas. OpenClaw también permite separar permisos por agente, proveedor, sesión y subagente, y cada capa solo puede endurecer la política anterior.

### Ejecución aislada

Las tareas de compilación, pruebas, análisis y generación de parches deben ejecutarse dentro de un entorno aislado cuando sea posible. El agente no necesita acceso de escritura al repositorio principal para producir un plan, y no debería obtener permiso de publicación para merely analizar un cambio.

### Aprobaciones humanas

Las acciones irreversibles o externas deben quedar bloqueadas detrás de una confirmación: publicar, enviar, comprar, eliminar, mezclar, cambiar producción o compartir información sensible. En los flujos de código, una pausa antes de guardar patrones en memoria también evita convertir falsos positivos en reglas permanentes.

### Memoria y datos personales

La memoria de Deep Agents puede organizarse por usuario, agente u organización, y los permisos de escritura pueden ser diferentes según el tipo de archivo. Los datos profesionales, preferencias y resultados de entrevistas no deberían mezclarse silenciosamente entre usuarios. Los datos de múltiples sesiones pueden guardarse en una base vectorial o en un wiki del proyecto, pero la selección debe conservar la fuente y la fecha.

### Ejecuciones concurrentes

Si dos ejecuciones se reanudan simultáneamente sobre el mismo `thread_id`, pueden Saltarse un punto de convergencia y dejar una rama interrumpida. En Agent Server puede utilizarse `multitask_strategy=enqueue` para serializar las ejecuciones de un hilo.

### Secretos

Las claves de modelos, OAuth y servicios externos deben guardarse mediante variables de entorno o referencias de secreto, y nunca deben aparecer en el código de una habilidad, una definición de plugin o un ejemplo público. El registro MCP también recomienda evitar encabezados estáticos con literales sensibles y utilizar mecanismos de credenciales compatibles.

## 9. Hoja de ruta de implementación

### Fase 1: mentor mínimo viable

Construir solamente el flujo `career_mentor` con intake, mapa de brechas, sesión diaria, ejercicio, evaluación y memoria por usuario. Conectarlo mediante MCP, crear la habilidad `$career-dev` y programar una automatización diaria. Medir la finalización de actividades y la retención antes de añadir otros flujos.

### Fase 2: tutor del repositorio

Incorporar indexación con Tree-sitter, inserciones, metadatos y recuperación semántica. Añadir un segundo agente MCP, `repo_tutor`, y permitiría que el mentor invoque o recomiende el tutor según la tarea. Validar que las respuestas incluyan referencias verificables al código y no solo explicaciones genéricas.

### Fase 3: revisión y aprobación

Incorporar `pr_reviewer` con estrategias de escritura, selección, compresión y aislamiento. Probar primero con repositorios públicos y lectura únicamente. Añadir escritura en GitHub únicamente después de implementar aprobación explícita, idempotencia y trazabilidad.

### Fase 4: proyecto de portafolio

Integrar el mentor, el tutor y el revisor en un flujo de proyecto completo basado en el patrón de Open SWE. El resultado debe incluir especificación, decisiones, código, pruebas, revisión y retrospectiva. Publicar o abrir la Pull Request debe seguir siendo una acción explícitamente aprobada.

### Fase 5: Arguendo y mercado

Agregar simulador de entrevistas, análisis de ofertas y preparación de contribuciones. En esta etapa conviene medir precisión y utilidad, no solamente el tiempo de ejecución.

## Conclusión

La mejor combinación para acompañar una carrera de desarrollador no es elegir entre OpenClaw y LangChain, sino asignar a cada sistema la responsabilidad que mejor controla: OpenClaw para interacted, horarios, webhooks y entrega; MCP para conectar herramientas; LangGraph para workflows con estado, aprobación y reanudación; Deep Agents para memoria y aprendizaje contextual; y LangSmith para observabilidad y evaluación.

El primer producto que produciría el mayor valor es un sistema de tres piezas: un mentor diario para organizar el aprendizaje, un tutor del repositorio para convertir el código real en ejercicios y un revisor que obligue a verificar calidad, seguridad y pruebas antes de publicar. Una implementación MVP puede utilizar exclusivamente MCP y una automatización diaria, dejando la API de hilos e interrupciones de LangGraph para los flujos que necesiten varias sesiones o aprobación humana.

Para convertir esta arquitectura en un plan personalizado, faltaría definir el puesto objetivo, las tecnologías actuales, las horas semanales disponibles, los repositorios que quieres usar como material de aprendizaje, el canal principal de interacción y si prefieres ejecutar todo localmente, en un servidor privado o en la nube administrada.

Citations:
[1] https://docs.openclaw.ai/tools
[2] https://docs.openclaw.ai/automation
[3] https://www.digitalocean.com/resources/articles/what-is-openclaw
[4] https://docs.openclaw.ai/help/faq/skills-and-automation
[5] https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph
[6] https://www.langchain.com/blog/mcp-in-langchain-stateless-protocol-elicitation-and-more
[7] https://docs.langchain.com/oss/python/langchain/mcp
[8] https://docs.langchain.com/oss/python/langgraph/checkpointers
[9] https://docs.openclaw.ai/es/gateway
[10] https://docs.openclaw.ai/es/cli/acp
[11] https://docs.openclaw.ai/plugins/tool-plugins
[12] https://docs.openclaw.ai/cli/mcp
[13] https://docs.openclaw.ai/tools/tool-search
[14] https://docs.openclaw.ai/gateway/tools-invoke-http-api
[15] https://www.langchain.com/blog/managed-deep-agents-schedules-per-run-configuration-slack
[16] https://www.langchain.com/blog/runtime-behind-production-deep-agents
[17] https://docs.langchain.com/oss/python/langchain/tools
[18] https://docs.openclaw.ai/automation/cron-jobs/managing-jobs
[19] https://docs.openclaw.ai/tools/creating-skills
[20] https://docs.openclaw.ai/automation/cron-jobs/webhooks
[21] https://docs.langchain.com/oss/python/langgraph/local-server
[22] https://reference.langchain.com/python/langsmith/deployment-sdk
[23] https://docs.langchain.com/langsmith/streaming
[24] https://docs.openclaw.ai/cli/attach
[25] https://docs.openclaw.ai/tools/code-mode/tool-surface
[26] https://docs.openclaw.ai/cli/mcp/registry
[27] https://reference.langchain.com/python/langgraph-sdk
[28] https://docs.langchain.com/langsmith/server-mcp
[29] https://github.com/xiaotonng/lc2mcp
[30] https://docs.openclaw.ai/automation/standing-orders
[31] https://docs.openclaw.ai/tools/multi-agent-sandbox-tools
[32] https://docs.openclaw.ai/concepts/multi-agent
[33] https://docs.openclaw.ai/plugins/github
[34] https://pub.towardsai.net/building-an-ai-pr-review-agent-with-openclaw-9787759e9e46
[35] https://www.langchain.com/blog/introducing-open-swe-an-open-source-asynchronous-coding-agent
[36] https://www.langchain.com/blog/building-multi-agent-applications-with-deep-agents
[37] https://docs.openclaw.ai/plugins/hooks
[38] https://docs.langchain.com/oss/python/langgraph/interrupts
[39] https://acpx.sh/
[40] https://forum.langchain.com/t/how-to-partially-stop-the-langgraph-workflow/4239
[41] https://www.meta-intelligence.tech/en/insight-openclaw-commands
[42] https://docs.langchain.com/langsmith/agent-server-overview
[43] https://docs.langchain.com/langsmith/agent-server-api/thread-runs/create-run-wait-for-output
[44] https://docs.langchain.com/langsmith/cron-jobs
[45] https://docs.openclaw.ai/clawhub
[46] https://docs.openclaw.ai/tools/agent-send
[47] https://docs.openclaw.ai/cli/agent
[48] https://github.com/langchain-ai/langsmith-cookbook/blob/main/testing-examples/agent_steps/evaluating_agents.ipynb
[49] https://www.lancedb.com/blog/building-rag-on-codebases-part-1
[50] https://www.analyticsvidhya.com/blog/2025/10/building-study-planner-agent-ai-agent-tutorial/
[51] https://huggingface.co/blog/darielnoel/an-agentic-backend-openclaw-integration
[52] https://www.augmentcode.com/guides/swarm-vs-supervisor
[53] https://docs.openclaw.ai/tools/exec
[54] https://docs.openclaw.ai/gateway/config-tools/custom-providers
[55] https://docs.openclaw.ai/concepts/model-providers/custom-providers
[56] https://clawhub.ai/manojrammurthy/skills/openclaw-skill-langchain-local
[57] https://dev.to/gateofai/build-a-langgraph-api-with-fastapi-47j
[58] https://github.com/samuelint/langchain-openai-api-bridge
[59] https://github.com/langchain-ai/langserve
[60] https://docs.openclaw.ai/cli
[61] https://docs.openclaw.ai/tools/skills
[62] https://www.codecademy.com/learn/paths/learn-langchain
[63] https://github.com/MAS-Infra-Layer/Agent-Git
[64] https://ssahuupgrad-93226.medium.com/building-an-enterprise-grade-ai-code-review-agent-with-langgraph-a-deep-dive-into-contextual-514756b803da
[65] https://docs.openclaw.ai/tools/mcp
[66] https://www.langchain.com/blog/introducing-ambient-agents
[67] https://docs.openclaw.ai/tools/swarm
[68] https://docs.openclaw.ai/tools/browser
[69] https://docs.langchain.com/oss/python/deepagents/memory
[70] https://docs.openclaw.ai/plugins/memory-wiki
[71] https://docs.langchain.com/langsmith/agent-server-api/threads/create-thread
[72] https://docs.openclaw.ai/automation/hooks
[73] https://docs.langchain.com/oss/python/langchain/agents
[74] https://docs.langchain.com/langsmith/agent-server-api/thread-runs/create-run