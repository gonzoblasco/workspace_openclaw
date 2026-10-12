# Módulo 5 · Lección 21 de 30: Desglose Estratégico de Tareas Complejas

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 5 - Encadenamiento en Bucle Agéntico
**Lección:** 21 de 30 · **abre el Módulo 5**
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

El bucle agéntico se distingue de un pipeline de scripts porque el modelo **evalúa el resultado de cada acción** antes de decidir la siguiente. Pero ante un objetivo complejo y abierto (auditar una base de código heredada, generar un informe consolidando fuentes, refactorizar un módulo con tests rotos), un agente sin marco de descomposición comete un error característico: **intenta resolver todo de golpe**, satura la ventana de contexto con herramientas dispares y **pierde de vista la meta original**.

El desglose estratégico es la fase de planificación donde el agente traduce una directiva abstracta en un **grafo acíclico dirigido (DAG) de subtareas** bien delimitadas. No es un resumen enumerado: define **criterios estrictos de entrada y salida** para cada eslabón, aísla el contexto relevante y reduce la probabilidad de alucinaciones en cadenas largas.

---

## Anatomía de una descomposición jerárquica

Un objetivo amplio **no** debe abordarse como lista plana secuencial (si un paso falla o devuelve algo ambiguo, colapsa). Tres capas funcionales:

- **Meta / Objetivo Primario:** la condición de satisfacción global (p. ej. *"actualizar la especificación OpenAPI de los endpoints de facturación y verificar que no existan discrepancias con el código"*).
- **Hitos / Fases aisladas:** bloques independientes con límites de contexto claros (Fase 1: reconocimiento; Fase 2: análisis diferencial; Fase 3: generación del esquema).
- **Subtareas atómicas:** unidades mínimas ejecutables con **una sola herramienta** o un par lectura/escritura (p. ej. `read_file` sobre `routes/billing.ts`, o `ast_grep` para extraer decoradores `@Post`).

Al forzar el desglose estructurado **antes** de activar herramientas, la memoria operativa se descarga: el agente solo sostiene el **contrato de la subtarea activa**, no la visión completa del entregable en cada llamada.

---

## El manifiesto del plan (`task_manifest.json`)

Para que el bucle no dependa de interpretaciones vagas, OpenClaw formaliza la descomposición en un **artefacto persistente**. El primer paso no es invocar un comando arbitrario, sino materializar este esquema en el espacio temporal de trabajo. Desacopla **razonamiento** de **ejecución**: cada subtarea declara dependencias explícitas, herramientas permitidas y criterios de aceptación.

```json
{
  "task_id": "audit-billing-endpoints-2025",
  "objective": "Auditar endpoints de facturación contra la especificación OpenAPI 3.1",
  "phases": [
    {
      "id": "phase_1_discovery", "name": "Descubrimiento de rutas", "status": "completed", "dependencies": [],
      "steps": [
        { "step_id": "1.1", "action": "ast_grep", "params": { "pattern": "@Post('/billing/$$$')" },
          "expected_output": "Rutas activas extraídas del router", "status": "done" }
      ]
    },
    {
      "id": "phase_2_validation", "name": "Comprobación cruzada de esquemas", "status": "in_progress",
      "dependencies": ["phase_1_discovery"],
      "steps": [
        { "step_id": "2.1", "action": "schema_validator",
          "params": { "spec_file": "docs/openapi.json", "target_routes": "phase_1_discovery.output" },
          "expected_output": "Lista de diferencias y tipos inconsistentes", "status": "pending" }
      ]
    }
  ]
}
```

Disciplina que impone:

- **Restricción de radio de impacto:** la fase de descubrimiento **solo** invoca herramientas de inspección (`ast_grep`, `read_file`), nunca de mutación (`write_file`, `git_commit`).
- **Contratos de datos:** la fase 2 consume **explícitamente** el resultado de la fase 1. Si la fase 1 no produjo una estructura legible, el bucle detecta la incompatibilidad de dependencias y **no avanza a ciegas**.

---

## Estrategias de partición según tipología

Tres patrones:

1. **Por capas de abstracción (Top-Down)** - arquitecturas y migraciones. Se definen interfaces/contratos antes de bajar a implementaciones. Ejemplo: pasarela de pagos → interfaz abstracta `PaymentGateway` → adaptadores (`StripeAdapter`, `PayPalAdapter`) → tests. Programar el cliente HTTP primero acoplaría métodos y rompería el contrato general.
2. **Por frontera de dominio (Domain Partitioning)** - análisis de repos extensos o auditorías. Fases paralelas en diseño, **serializadas en ejecución** para no desbordar contexto; cada dominio produce un resumen en disco antes de abordar el siguiente.

   | Dominio | Foco | Herramientas | Criterio de corte |
   |---|---|---|---|
   | Controladores/API | Payloads y decoradores | `ast_grep`, `read_file` | Todas las rutas registradas |
   | Servicios/Lógica | Transacciones/reglas | `symbol_search`, `read_file` | Flujos débito/crédito mapeados |
   | Persistencia/Modelos | Prisma/TypeORM y migraciones | `diff_check`, `read_file` | Índices y restricciones chequeados |

3. **Por embudo iterativo (Search-Narrow-Execute)** - depuración forense en producción. Búsqueda amplia → filtrar sospechosos → intervenir solo el archivo exacto.

> **PITFALL del curso (correcto):** permitir que el agente **modifique** durante la fase de búsqueda, antes de aislar la causa raíz, provoca regresiones graves: parches aleatorios que alteran código funcional y **oscurecen el error original**.

---

## Granularidad de subtareas y ventana de contexto

**Regla de invarianza de estado:**

```
Atomicidad ⟺ Entrada fija ⟶ Acción idempotente ⟶ Salida verificable
```

Una subtarea es atómica si cumple tres condiciones:
1. **Entrada autocontenida:** no requiere adivinar variables globales no documentadas.
2. **Propósito único:** **o** recopila info sin modificar (lectura), **o** aplica un cambio respaldado por comprobación inmediata (mutación).
3. **Criterio de salida booleano:** existe condición determinista de éxito (`exit_code == 0`, archivo generado en ruta, o regex en stdout).

Demasiado fina (`cd`, `ls`, `cat` como subtareas separadas) dispara latencia y tokens de meta-orquestación; demasiado gruesa ("analizar y corregir el fallo") mezcla lectura y mutación sin introspección intermedia.

> **REMEMBER del curso (correcto):** nunca permitas que una subtarea combine **exploración sin límites** con **edición de configuración**. Detección y edición van en **fases distintas**.

### Check your understanding
**¿Principio óptimo para el manifiesto al corregir un fallo en producción?**
- [x] **Las operaciones de exploración y diagnóstico deben aislarse de las fases de edición mediante contratos claros de entrada y salida.** ✅ (el curso acierta)

---

## Implementación de un planificador

El curso delega la generación del manifiesto a un paso de **meta-planificación** antes de ceder el control al motor de ejecución.

```typescript
import { AgentRuntime, PlanManifest, TaskPhase } from '@openclaw/core';

export async function generateStrategicPlan(runtime: AgentRuntime, directive: DirectiveInput): Promise<PlanManifest> {
  const systemPrompt = `Eres el módulo PLANNER de OpenClaw. Tu único propósito es descomponer el objetivo en fases acíclicas.
Reglas: 1. Máximo 4 fases. 2. La primera DEBE ser de sólo lectura. 3. Cada subtarea con criterios de salida unívocos. 4. Devuelve sólo JSON conforme a PlanManifest.`;
  const planResponse = await runtime.completeStructured({ system: systemPrompt, prompt: userPrompt, schema: PlanManifestSchema });
  validateAcyclicGraph(planResponse.phases);                     // sin ciclos
  await runtime.workspace.write('.openclaw/current_task_manifest.json', JSON.stringify(planResponse, null, 2));
  return planResponse;
}

function validateAcyclicGraph(phases: TaskPhase[]): void { /* DFS con recursionStack */ }
```

`validateAcyclicGraph` impide dependencias mutuas: si la fase de mutación dependiera de una fase que requiere que los cambios ya estén aplicados, el bucle quedaría **bloqueado indefinidamente**.

---

## Resumen

El desglose estratégico convierte requerimientos amplios en **unidades gobernadas y predecibles**: fases jerárquicas vía `task_manifest.json`, lectura aislada de mutación, y herramientas restringidas por etapa → evita perder el rumbo en la ventana de contexto.

**UP NEXT · Lección 22 de 30:** *Ejecución Consecutiva de Herramientas y Habilidades*. Faltan **4 lecciones** para cerrar el Módulo 5.

---

## Preguntas abiertas del propio curso ("Can you answer these?")

1. ¿Cómo evita OpenClaw bucles infinitos al descomponer una tarea compleja?
2. ¿Por qué es crítico separar inspección de mutación en fases distintas?
3. ¿Qué métrica determina si una subtarea es demasiado amplia?
4. ¿Cómo se propaga la información de una fase preliminar a las subsecuentes?

(Anotadas. La #1 la responde el `validateAcyclicGraph`; la #2 y #4, los contratos del manifiesto.)

---

## Notas de verificación (Kanam)

**El núcleo conceptual es correcto y muy valioso - y coincide con cómo trabajamos:**

- ✅ **DAG de fases + dependencias explícitas** en vez de lista plana: correcto y central.
- ✅ **Aislar lectura de mutación** en fases distintas: correcto y crítico (el PITFALL de "parchear durante la búsqueda" es real).
- ✅ **Contrato por subtarea** (entrada autocontenida / propósito único / salida booleana): excelente criterio de diseño.
- ✅ **REMEMBER** (no combinar exploración con edición): correcto.
- ✅ **`validateAcyclicGraph` funciona**: lo corrí en Node → acíclico pasa sin excepción; con ciclo `A↔B` **lanza** "Dependencia cíclica detectada en la fase: A". El algoritmo es correcto.
- ✅ **Acierta el quiz** (aislar exploración de edición).
- ✅ **Mapea a nuestra práctica real:** el pipeline A/B, `session_plan.py`, y sobre todo el patrón "plan → A escribe → B revisa → verificar repo" del AGENTS.md son, literalmente, este desglose. Y `NORTH.md`/HANDOFF cumplen el rol de "manifiesto persistente".

**Lo que NO existe en la instalación real:**
- ❌ **`@openclaw/core` no existe como paquete** (tercer caso: L05/L11/L21). El import con `AgentRuntime`, `PlanManifest`, `runtime.completeStructured`, `runtime.workspace.write` es **inventado**. Los paquetes reales: `ai`, `fs-safe`, `proxyline`.
- ❌ **Las "herramientas" del curso no existen:** `ast_grep`, `symbol_search`, `schema_validator`, `diff_check` **no aparecen** en docs ni como tools de OpenClaw. (Son plausibles como herramientas que uno instalaría, pero no son nativas.)
- ❌ **`.openclaw/current_task_manifest.json`** y el "motor de manifiesto de tareas" no son del producto. (En este workspace, el equivalente real es `scripts/session_plan.py` + `.knowledge/archive/session_plan_*.json` - que **también corrimos**, ver daily 10-08.)
- ❌ **`task_manifest.json` con `action`/`params`/`expected_output`**: esquema del curso, no de OpenClaw.

**Verificación ejecutable:**
- ✅ Node disponible; `validateAcyclicGraph` **corre y es correcto** (sin dependencias externas, más allá del import ficticio que el fragmento completo requeriría).
- ⚠️ El código de `generateStrategicPlan` **no corre** tal cual: depende de `@openclaw/core` y `PlanManifestSchema`, inexistentes.

**Patrón (vigésimo primer caso, consistente):** **excelente ingeniería** (DAG, contratos, separación lectura/mutación, validación de ciclos) montada sobre una **API inventada** (`@openclaw/core`, herramientas mágicas, manifiesto nativo). **El qué es de lo mejor del curso y ya lo hacemos** - el valor extra es que **pone nombre y estructura formal** a lo que en el workspace es praxis implícita. Traducible: `session_plan.py`/ADR/task graphs, no `@openclaw/core`.

**Nota de contexto (Módulo 5):** tras esta L21 el propio curso indica *"4 lessons left in Encadenamiento en Bucle Agéntico"* → Módulo 5 = 5 lecciones (L21-L25). Lección 22: *Ejecución Consecutiva de Herramientas y Habilidades*.
