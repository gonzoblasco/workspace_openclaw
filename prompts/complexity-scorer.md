# Meta-Prompt: Evaluador de Complejidad de Objetivo

**Propósito:** Estandarizar la selección del motor LLM y el nivel de razonamiento (`thinking`) basándose en un análisis de la complejidad del *objetivo* en lugar de hacerlo por intuición o por regla fija.

> **Fuente de verdad:** este archivo define las reglas de scoring. El script
> `scripts/complexity-scorer.sh` implementa estos umbrales y el LLM evaluador.
> Si cambiás buckets o modelo de scorer, actualizá AMBOS (este archivo y el
> script, que lee los umbrales de acá o los duplica explícitamente).

---

## Instrucciones (Kanam - Orquestador / LLM evaluador)

1. **Recibir el objetivo del usuario.**
2. **Analizar 4 dimensiones (Score 1-5 cada una, Suma Total 4-20):**
   * **Alcance (A):** ¿Cuántos archivos/sistemas toca? (1=uno, 5=multi-repo).
   * **Abstracción (B):** ¿Es código nuevo, refactor, diseño de arquitectura, o análisis estratégico? (1=trivial, 5=diseño de sistema).
   * **Riesgo (C):** ¿Una falla es cosmética, rompe una función, o corrompe datos/privacidad? (1=cosmético, 5=crítico/destructivo).
   * **Ambigüedad (D):** ¿El objetivo es claro y específico, o requiere interpretación? (1=cristalino, 5=abstracto).
3. **Calcular Score Total (T = A + B + C + D).**
4. **Mapear a Configuración (buckets):**
   * `T <= 6`: Kanam solo, **sin pipeline** (`thinking=off`). Modelo default.
   * `7 <= T <= 12`: Agente A escribe → Kanam revisa (`thinking=high`).
   * `13 <= T <= 16`: Agente A escribe → Agente B cross-review → Kanam aprueba (`thinking=high`).
   * `T >= 17`: Kanam(max) diseña → A(high) ejecuta → B(high) revisa → verificación obligatoria (`thinking=max` solo para Kanam).
   * **Escalada por riesgo (calibración 2026-08-31):** si `Riesgo (C) >= 4` **y** `T >= 14`, forzar bucket `high` aunque la baja ambigüedad (D) deje el total < 17. La ambigüedad se clarifica; el riesgo de pérdida de datos (producción) no. Protege tareas peligrosas pero claras de ser sub-pipelineadas. Marca `escalated=1` en el output.
5. **Justificar siempre** la decisión en una línea antes de proceder.

> **Modelo de scorer:** el script evaluador usa `gemma4:e4b-mlx` local primero
> (6.7x más rápido que qwen3.5:9b-mlx, benchmark 2026-08-30), con fallbacks a
> `deepseek-v4-flash:cloud` → `gemma4:cloud` → `qwen3.5:9b-mlx`. El scorer local
> es solo para calcular el T-score; el modelo de trabajo del pipeline es otro
> (`deepseek-v4-flash:cloud` default).

---

## Restricciones

* **No usar** `thinking=max` en agentes de código (A/B). Solo en Kanam (orquestador) para diseño difícil.
* **Si el score T es 17+**, pedir **confirmación explícita a Gonzo** antes de proceder.
* **trivial (T≤6) = sin agentes.** Kanam lo hace directo. No spawnear A/B para tareas triviales.

---

## Ejemplo de Uso

**Input del usuario:** "Refactorizar el sistema de auth para usar JWT y agregar refresh tokens."

**Análisis:**
* Alcance (A): Toca auth, DB, middleware, frontend = **4**
* Abstracción (B): Refactor + diseño JWT = **4**
* Riesgo (C): Auth roto = acceso no autorizado = **5**
* Ambigüedad (D): Requerimientos claros pero implementación compleja = **3**

**Score Total: T = 16**

**Output del orquestador:**
```
[COMPLEXITY-SCORE] T=16 (medium-complex)
  -> Pipeline: A escribe -> B cross-review -> Kanam aprueba
  -> Thinking: high
  -> Justificación: Sistema de auth con JWT implica riesgo crítico (C=5) + refactor multi-capa (A=4). T=16 justifica cross-review de B.
Procedo.
```
