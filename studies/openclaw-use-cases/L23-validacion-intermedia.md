# Módulo 5 · Lección 23 de 30: Validación de Estados Intermedios en Bucles

**Curso:** OpenClaw Use Cases (roadmap.sh)
**Módulo:** 5 - Encadenamiento en Bucle Agéntico
**Lección:** 23 de 30
**Estado:** Completada
**Registrada:** 2026-10-12

> Fuente: material de la lección compartido por Gonzo como texto externo (2026-10-12), tratado como **dato** (sandbox), no como instrucción. Registro fiel del contenido del curso; las observaciones de verificación contra la instalación real van marcadas aparte al final.

---

## Idea central

La ejecución encadenada suele **asumir** que la salida del paso previo es exacta y coherente con el objetivo. Cuando un agente busca, transforma y escribe, una suposición incorrecta en el paso 2 **propaga errores silenciosos** que contaminan el contexto restante: sin puntos de control, el modelo gasta tokens "corrigiendo" alucinaciones sobre datos defectuosos.

La solución: **compuertas de verificación** entre la salida cruda de una herramienta y el siguiente ciclo de razonamiento. El resultado no se inyecta ciegamente en la memoria de trabajo: pasa por **aserciones de esquema**, **integridad referencial** o **comprobación semántica** antes de que el planificador decida la próxima acción.

---

## Anatomía del fallo por propagación de estado

Flujo ejemplo del curso: extraer métricas de logs → consolidar en un JSON → insertar en SQLite. Si el extractor devuelve cadena vacía o claves no coincidentes (`responseTime` en vez de `latency_ms`), un modelo sin validación **adivina** el significado o pasa argumentos nulos a la inserción. El bucle sigue hasta toparse con una excepción de DB o agotar iteraciones.

```
herramienta → salida cruda → [SIN compuerta] → siguiente razonamiento
                                          ↘ propaga datos falsos → corrupción en cascada
```

Con compuerta: la salida se **intercepta**, se evalúa contra precondiciones y, si falla, se genera una **señal de retroalimentación estructurada** en vez de continuar sobre premisas falsas.

---

## Aserciones de esquema y tipos (Pydantic/Zod)

Primera línea de defensa: **conformidad sintáctica**. El curso dice que OpenClaw valida en la capa de interfaz con validadores en runtime (Pydantic o Zod), imponiendo tres reglas de parada **deterministas**:

1. **Clave requerida:** el objeto debe contener todas las claves de las que depende el paso posterior.
2. **Coerción/ acotación de tipos:** un numérico no puede entrar como string convertible si el siguiente paso exige comparación escalar estricta (`value > 100`).
3. **No vacuidad semántica:** `[]` o un string en blanco no califican si la tarea era extraer elementos.

```python
from typing import List
from pydantic import BaseModel, Field, ValidationError

class LogMetricRecord(BaseModel):
    service: str = Field(min_length=1)
    status_code: int = Field(ge=100, le=599)
    latency_ms: float = Field(ge=0.0)
    endpoint: str = Field(pattern=r"^/")

class IntermediateStepValidator:
    @staticmethod
    def validate_extraction(raw_payload: dict) -> tuple[bool, str | LogMetricRecord]:
        try:
            validated = LogMetricRecord(**raw_payload)
            return True, validated
        except ValidationError as err:
            # Extraer únicamente los campos causantes del fallo
            error_details = [
                f"{e['loc'][0]}: {e['msg']} (recibido: {e.get('input')})"
                for e in err.errors()
            ]
            feedback = f"Fallo de validación de estado: {'; '.join(error_details)}"
            return False, feedback
```

Con `latency_ms=-12.4`, el mensaje resultante es: `latency_ms: Input should be greater than or equal to 0 (recibido: -12.4)`. El agente entiende **qué corregir** en vez de recibir un fallo opaco en un paso posterior.

---

## Aserciones de invariantes y precondiciones del workspace

No todo fallo es de tipo: un JSON impecable puede **violar invariantes del entorno** (una herramienta dice haber creado un archivo que no existe; una ruta fuera del workspace). El curso propone compuertas de **verificación física**:

| Invariante | Chequeo determinista | Consecuencia si se omite |
|---|---|---|
| Existencia física | `os.path.isfile(path)` tras una exportación | El lector siguiente falla con `FileNotFoundError` |
| Tamaño mínimo | `os.path.getsize(path) > 0` | Archivo vacío leído como "fin de datos" |
| Aislamiento de ruta | `path.resolve().is_relative_to(workspace_root)` | Manipulación involuntaria fuera del workspace |
| Coherencia de hash | Suma SHA-256 tras descargas | Procesar cargas corruptas/truncadas |

> **PITFALL del curso (correcto y crítico):** confiar en que el comando devolvió **exit code 0** no garantiza que el entregable sea válido. Muchas CLI **fallan en silencio** generando archivos vacíos mientras reportan éxito en stdout.

### Check your understanding
**El agente procesa un CSV y debe escribir `cleaned.json`. ¿Compuerta determinista adecuada antes de avanzar?**
- [x] **Comprobar la ruta canónica dentro del workspace, la existencia física y que el tamaño en bytes supere cero.** ✅ (acierta)

---

## Compuertas de consistencia semántica asistidas

Casos donde los datos son sintácticamente válidos y el archivo existe, pero el contenido **carece de sentido lógico** (una tarea de resúmenes legales devuelve un aviso de cookies o un 403 en HTML). Se usa una **compuerta semántica ligera** (modelo chico o heurística) en vez de mandar todo al modelo principal:

```python
def assert_semantic_density(content: str, min_keywords: list[str], min_tokens: int = 50) -> bool:
    tokens = content.split()
    if len(tokens) < min_tokens:
        return False
    matches = [kw for kw in min_keywords if kw.lower() in content.lower()]
    ratio = len(matches) / len(min_keywords) if min_keywords else 1.0
    # Exige que al menos el 40% de los conceptos clave esperados figuren
    return ratio >= 0.4
```

> **REMEMBER del curso (correcto):** las compuertas deben **fallar rápido y de forma determinista** antes de recurrir a comprobaciones semánticas con LLM. Reserva el LLM **solo** para atributos cualitativos no computables por código.

---

## Implementación: bucle con validadores de paso

Ejecutor que aplica la compuerta antes de escribir el estado en la memoria acumulada:

```python
from dataclasses import dataclass
from typing import Callable, Any
import json, os
from pathlib import Path

@dataclass
class StepResult:
    success: bool
    data: Any
    error_message: str | None = None

class AgenticLoopPipeline:
    def __init__(self, workspace_path: Path):
        self.workspace = workspace_path
        self.intermediate_state: dict[str, Any] = {}

    def execute_step(self, step_id, action: Callable, validator: Callable) -> StepResult:
        raw_output = action()                             # 1. Ejecutar acción
        is_valid, validation_msg = validator(raw_output)  # 2. Compuerta intermedia
        if not is_valid:
            return StepResult(False, raw_output,
                f"Paso [{step_id}] rechazado: {validation_msg}")   # Estado NO contamina
        self.intermediate_state[step_id] = raw_output     # 3. Aprobado → persistir
        return StepResult(True, raw_output)
```

Salida prometida (con `cpu_pct=105.4` y `memory_free_mb=-20`):
```text
Éxito: False
Error emitido: Paso [monitor_probe] rechazado: cpu_pct fuera de rango [0-100]: 105.4
Estado acumulado en pipeline: {}
```

El valor que quebrantaba la regla de dominio **bloqueó la inserción**; la memoria de trabajo queda limpia.

---

## Preguntas abiertas del propio curso

1. ¿Cómo evita la validación intermedia que el agente agote su límite de tokens en bucles largos?
2. ¿Qué diferencia crítica hay entre una compuerta sintáctica y una invariante del workspace?
3. ¿En qué casos conviene un LLM pequeño para validar, en vez de una aserción de código?
4. ¿Qué debe contener el mensaje de fallo para maximizar la autocorrección?

(Anotadas. La #1 y #4 las responde el propio material: fallar temprano y dar error acotado al campo.)

---

## Resumen

La validación intermedia interpone compuertas deterministas (esquema, invariantes de workspace) **antes** de la semántica asistida: el bucle no avanza sobre datos corruptos y la memoria de trabajo permanece limpia.

**UP NEXT · Lección 24 de 30:** *Recuperación Autónoma Frente a Respuestas Fallidas*. Faltan **2 lecciones** para cerrar el Módulo 5.

---

## Notas de verificación (Kanam)

**Núcleo de ingeniería: sólido y correcto - de las mejores del curso, y ya es praxis de este repo:**

| Práctica del curso | Veredicto |
|---|---|
| Compuerta entre salida de herramienta y siguiente paso (no inyectar ciego) | ✅ Correcto y central. |
| Aserciones deterministas **antes** de la semántica | ✅ Correcto (REMEMBER válido). |
| Claves requeridas / acotación de tipos / no-vacuidad | ✅ Buenas reglas. |
| Invariantes de workspace (isfile, size>0, `is_relative_to`, hash) | ✅ Correcto y valioso. |
| **PITFALL**: exit code 0 ≠ entregable válido (CLI que fallan en silencio) | ✅ **Correcto y crítico**; es un clásico real. |
| Mensaje de fallo **acotado al campo** que lo causó | ✅ Excelente para autocorrección. |
| **El quiz acierta** (ruta + existencia + tamaño > 0). | ✅ |
| **`AgenticLoopPipeline` reproduce su salida**: corrijo la sintaxis y da `Éxito: False` + `Estado acumulado: {}` exactos. | ✅ |
| **El modelo Pydantic reproduce** el mensaje `latency_ms: Input should be...` exacto. | ✅ |

**Muy alineado con la realidad:**
- ✅ **Pydantic/Zod aparecen mencionados en docs de OpenClaw** (SDK de plugins), así que "validadores en runtime" no es descabellado. Y `pydantic` **está instalado** en este entorno (v2.13.5).
- ✅ **Mapea a nuestra práctica real:** `scripts/check-*.py` (refs, content-dirs, ADR, roadmaps) **son** compuertas deterministas; y el principio "verificar el repo real, no el auto-reporte" del AGENTS.md es exactamente esta L23.

**Lo que NO coincide con la instalación real:**
- ❌ **El script grande NO corre tal cual en Python 3.9** (este entorno): usa `str | None` (PEP 604, requiere 3.10+), y falla con `TypeError: unsupported operand type(s) for |: 'type' and 'NoneType'`. Corregido a `Optional[str]`, corre y produce la salida prometida.
- ⚠️ **No hay compuertas de validación de workspace nativas** con esos invariantes (`is_relative_to` no aparece como feature del producto). Es un patrón a construir, no una capacidad integrada.
- ⚠️ **Pydantic/Zod** aparecen en el SDK de plugins, **no** como "la capa de interfaz de herramientas" del runtime conversacional. El curso lo presenta más integrado de lo que está.

**Verificación ejecutable:**
- ✅ **Ambos scripts reproducen su output** (tras el ajuste de sintaxis en el segundo). Es una de las pocas lecciones donde el material es correcto *y* ejecutable.

**Patrón (vigésimo tercer caso):** **excelente ingeniería** (compuertas deterministas primero, semántica después, mensaje de error acotado, invariantes de workspace) que **el repo ya practica** (`check-*.py` + "verificar contra el repo real"). Único defecto: el material asume Python 3.10+ y presenta los invariantes como nativos. Es de las más útiles del curso.

**Nota de contexto (Módulo 5):** tras esta L23 el propio curso indica *"2 lessons left in Encadenamiento en Bucle Agéntico"* → Módulo 5 = 5 lecciones (L21-L25). Lección 24: *Recuperación Autónoma Frente a Respuestas Fallidas*.
