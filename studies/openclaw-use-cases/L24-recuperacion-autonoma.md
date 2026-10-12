# Módulo 5 · Lección 24 de 30: Recuperación Autónoma Frente a Respuestas Fallidas

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 5 - Encadenamiento en Bucle Agéntico
**Lección:** 24 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

En un bucle iterativo de herramientas, **los fallos son la norma, no la excepción**: un `bash` devuelve un código inesperado, una HTTP da timeout, un parser de JSON falla porque el paso anterior truncó las llaves. La diferencia entre un script frágil y un agente operativo está en la capacidad del bucle de **interceptar el colapso, diagnosticarlo y formular una corrección sin abortar la ejecución global**.

La recuperación autónoma **no** delega al humano ante el primer tropiezo: transforma el error de la herramienta en **una nueva observación diagnóstica**. El motor analiza el mensaje junto al objetivo, ajusta parámetros o elige otra herramienta, y reanuda el ciclo **manteniendo el estado local íntegro**.

---

## Anatomía de un fallo en el ciclo de ejecución

Bajo la secuencia **ReAct (Reasoning + Acting)**, el comportamiento ingenuo es dejar que la excepción rompa la pila. Un ejecutor robusto la captura y emite un **objeto estructurado de fallo** dentro del historial: el agente no percibe una rotura, sino un resultado adverso a evaluar.

Tres categorías operativas:

1. **Errores de sintaxis / invocación de argumentos:** nombres incorrectos, formatos no serializables, tipos incompatibles con el esquema de la herramienta.
2. **Errores transitorios de entorno:** HTTP 429, 503, bloqueos temporales de lectura.
3. **Errores semánticos de ejecución:** la herramienta corre sin excepción, pero el resultado **no cumple las precondiciones** (buscar un usuario y obtener `[]` cuando se esperaba un único registro).

```json
{
  "step": 4, "tool": "execute_shell", "status": "error",
  "payload": {
    "command": "sed -i 's/foo/bar/g' /var/log/app.conf",
    "exit_code": 1,
    "stderr": "sed: can't read /var/log/app.conf: No such file or directory"
  },
  "recovery_attempt": 1, "max_retries": 3
}
```

El `stderr` pasa a ser el **prompt de observación** del siguiente paso de razonamiento. Clave: **no ocultar el error ni maquillar la pila**. Un `Command failed` genérico no da señal; un volcado preciso (ruta fallida + código exacto) permite contrastar la causa física contra las expectativas.

---

## Estrategias de auto-corrección adaptativa

Auto-corregir **no** es reintentar la misma llamada con idénticos argumentos a ciegas. Tres patrones concretos:

1. **Inyección de feedback correctivo:** cuando la salida rompe el esquema esperado, se inyecta un mensaje de sistema que detalla el fallo del parser:
   ```text
   [SYSTEM OBSERVER]
   Error al parsear la salida de 'fetch_metrics':
   Se esperaba un objeto JSON válido con las claves 'cpu_usage' y 'memory_usage'.
   Texto recibido: "CPU: 42%, MEM: 80% (status ok)"
   Acción requerida: Reformula la llamada o utiliza una herramienta de parseo auxiliar.
   ```
2. **Sustitución de herramientas:** si una falla irrecuperablemente (p. ej. TLS en red corporativa), el agente pivota a una alternativa (p. ej. `execute_shell` con `curl --insecure`, **tras evaluar riesgos permitidos**).
3. **Ajuste paramétrico progresivo:** ante desbordes (leer un log de 50 MB con `read_file`), se contraen los argumentos (`tail -n 100`, `grep`).

> **Regla fundamental:** el agente debe **mantener la memoria del intento fallido**. Si el contexto limpia los errores para ahorrar espacio, el modelo entra en **bucle infinito** reintentando la misma llamada.

---

## Límites de reintento y políticas de escalada

Resiliencia sin límites = bucle fuera de control. Tres variables de control:

- **`max_step_retries`** (presupuesto por paso): correcciones consecutivas sobre una misma herramienta antes de abortar el subobjetivo (típico 2-3).
- **`max_total_retries`** (presupuesto acumulado): correcciones toleradas en todo el ciclo.
- **Detector de idempotencia/estancamiento:** verifica si dos llamadas consecutivas tienen **los mismos parámetros y el mismo código de error**.

> **PITFALL del curso (correcto):** si payload y exit code son idénticos dos ciclos seguidos, el agente entró en **ciclo ciego**. Reintentar una tercera vez es inútil: **pausar o escalar** de inmediato.

Agotado el presupuesto, la **rutina de preservación de estado** (no un simple `ProcessAbortedException`):
1. **Empaquetado del contexto de fallo:** objetivo original + pasos exitosos + errores + última hipótesis.
2. **Ticket/notificación:** alerta al operador con el diagnóstico consolidado.
3. **Punto de restauración:** el workspace guarda el estado intermedio para reanudar sin repetir fases validadas.

### Check your understanding
**Ante un `No such file or directory` de bash, ¿respuesta operativa correcta?**
- [x] **Inyectar el código de error y el volcado de stderr en el historial de observaciones para que el agente razone una alternativa.** ✅ (acierta)

---

## Implementación: bucle resiliente

`ResilientAgentLoop` intercepta la salida antes de devolver el control a inferencia y administra el contador:

```python
import subprocess
from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class ToolExecutionResult:
    success: bool
    output: str
    error: str = ""
    exit_code: int = 0

@dataclass
class ExecutionContext:
    task: str
    history: List[Dict[str, str]] = field(default_factory=list)
    step_retries: int = 0
    max_step_retries: int = 3

class ResilientAgentLoop:
    def __init__(self, context: ExecutionContext):
        self.context = context
    def execute_tool(self, tool_name: str, **kwargs) -> ToolExecutionResult:
        if tool_name == "run_shell":
            cmd = kwargs.get("command", "")
            process = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            if process.returncode == 0:
                return ToolExecutionResult(True, process.stdout.strip(), exit_code=0)
            return ToolExecutionResult(False, process.stdout.strip(),
                error=process.stderr.strip() or "Error en comando sin salida stderr",
                exit_code=process.returncode)
        return ToolExecutionResult(False, "", error="Herramienta no reconocida", exit_code=-1)
    def step(self, proposed_action: Dict[str, Any]) -> bool:
        tool = proposed_action.get("tool"); params = proposed_action.get("params", {})
        result = self.execute_tool(tool, **params)
        if result.success:
            self.context.history.append({"role": "tool_observation", "content": result.output, "status": "success"})
            self.context.step_retries = 0
            return True
        self.context.step_retries += 1
        if self.context.step_retries >= self.context.max_step_retries:
            self.context.history.append({"role": "system_escalation",
                "content": f"Límite de {self.context.max_step_retries} reintentos superado en {tool}. Solicitando derivación."})
            return False
        self.context.history.append({"role": "tool_error",
            "content": f"Fallo al ejecutar '{tool}'. Código: {result.exit_code}. Error: {result.error}",
            "directive": "Evalúa el motivo del fallo y prueba una acción alternativa o ajusta los parámetros."})
        return True
```

`step` **no silencia** la excepción: la documenta como `tool_error`. El LLM recibe la orden original **y** la traza exacta del fallo → diagnostica y elige otra vía en vez de atascarse.

---

## Ejercicio (verificado)

`evaluate_db_failure(error_msg, attempt, max_attempts=2)`: error de **credenciales** → escalar ya; límite alcanzado → escalar; si no → `retry` con el error exacto. Salida real de mi corrida (idéntica a la del curso):
```text
Paso 1: retry -> Error SQL detectado: Syntax error near 'WHERE AND id=10'. Ajusta la consulta y reintenta.
Paso 2: escalate -> Credenciales inválidas. Requiere intervención de credenciales.
```

---

## Resumen

Convertir anomalías en **observaciones procesables**: errores descriptivos (stderr + traza + código), reformulación y límites claros → operatividad sin supervisión en cada fallo transitorio.

**UP NEXT · Lección 25 de 30:** *Generación de Entregables Finales Multi-Etapa*. **Queda 1 lección** para cerrar el Módulo 5.

---

## Preguntas abiertas del propio curso

1. ¿Cómo evita OpenClaw el bucle infinito repitiendo la misma herramienta fallida?
2. ¿Diferencia entre error transitorio de entorno y error sintáctico de parámetros?
3. ¿Por qué es perjudicial limpiar los mensajes de error del contexto durante un reintento?
4. ¿Qué datos debe incluir un paquete de escalada?

(Anotadas. #1 → detector de estancamiento; #3 → la regla de memoria del intento; #4 → empaquetado de contexto.)

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto.** Es de las mejores del curso y **muy alineada con este repo:**

- ✅ **El error como observación, no como aborto:** patrón correcto (ReAct).
- ✅ **No ocultar el error / no `Command failed` genérico:** correcto y clave.
- ✅ **Memoria del intento fallido (no limpiar el error al reintentar):** **correcto y crítico** - es el hueco clásico.
- ✅ **PITFALL del ciclo ciego** (payload + exit code idénticos dos veces → pausar/escalar): correcto.
- ✅ **Presupuestos por paso + acumulado + detector de estancamiento:** buen diseño.
- ✅ **Preservación de estado al escalar** (empaquetado + ticket + punto de restauración): correcto y valioso.
- ✅ **Acierta el quiz.**
- ✅ **El ejercicio `evaluate_db_failure` corre tal cual** → reproducí `retry` / `escalate` exactos.
- ✅ **Mapea a este repo:** el PITFALL del ciclo ciego == nuestro "verificar el repo real, no el auto-reporte"; y la preservación de estado al escalar == nuestro HANDOFF + `.knowledge/`.

**Lo que SÍ existe (con otro nombre):**
- ✅ **OpenClaw tiene retry/backoff reales:** `agent-loop.md` menciona *"bounded session retry budget"*, *"retry grace"* (ventana de 15 s para fallback), y backoff en el scheduler. El *concepto* de presupuesto de reintentos es real.
- ⚠️ **Pero NO con la superficie del curso:** `max_step_retries`, `max_total_retries`, `ProcessAbortedException`, `ResilientAgentLoop` **no existen** en docs. Es un **modelo a construir** encima, no una API del producto.
- ⚠️ El **presupuesto real** de ejecución es el de tiempo (`agents.defaults.timeoutSeconds`) + grace windows, no un contador de reintentos por herramienta con esos nombres.

**Lo que NO existe:**
- ❌ **`execute_sql`, `run_shell`, `read_file`, `fetch_metrics`, `execute_shell`** no son tools nativas con esos nombres (verificado). `read_file`/`write`/`exec` existen con otros nombres y semántica; el resto es inventado.
- ❌ Los **roles del historial** `tool_error`, `tool_observation`, `system_escalation` son del ejemplo (el runtime real usa rol `tool` + `tool_call_id`, ver L22).

**Verificación ejecutable:**
- ✅ El único script con lógica pura (`evaluate_db_failure`) **corre y reproduce su salida exacta**.
- ❌ `ResilientAgentLoop` es ilustrativo (depende de "OpenClaw" que en realidad es solo `subprocess` de Python); no hay primitivas de OpenClaw en juego.

**Patrón (vigésimo cuarto caso, consistente):** **excelente ingeniería** (error-como-observación, no perder el intento, límites, detección de estancamiento, preservación al escalar) montada sobre una **API de bucle inventada** (`ResilientAgentLoop`, `max_step_retries`). El *qué* es correcto y ya lo practicamos; el *cómo* real es el retry budget + grace windows nativos + herramientas propias.

**Nota de contexto (Módulo 5):** tras esta L24 el propio curso indica *"1 lesson left in Encadenamiento en Bucle Agéntico"* → Módulo 5 = 5 lecciones (L21-L25). Lección 25: *Generación de Entregables Finales Multi-Etapa*.
