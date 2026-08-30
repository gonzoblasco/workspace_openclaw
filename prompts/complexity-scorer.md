# Meta-Prompt: Evaluador de Complejidad de Objetivo

**Propósito:** Estandarizar la selección del motor LLM y el nivel de razonamiento (`thinking`) basándose en un análisis de la complejidad del *objetivo* en lugar de hacerlo por intuición o por regla fija.

---

## Instrucciones (Kanam - Orquestador)

1. **Recibir el objetivo del usuario.**
2. **Analizar 4 dimensiones (Score 1-5 cada una, Suma Total 4-20):**
   * **Alcance (A):** ¿Cuántos archivos/sistemas toca? (1=uno, 5=multi-repo).
   * **Abstracción (B):** ¿Es código nuevo, refactor, diseño de arquitectura, o análisis estratégico? (1=trivial, 5=diseño de sistema).
   * **Riesgo (C):** ¿Una falla es cosmética, rompe una función, o corrompe datos/privacidad? (1=cosmético, 5=crítico/destructivo).
   * **Ambigüedad (D):** ¿El objetivo es claro y específico, o requiere interpretación? (1=cristalino, 5=abstracto).
3. **Calcular Score Total (T = A + B + C + D).**
4. **Mapear a Configuración:**
   * `T <= 6`: Modelo `gemma4:cloud` (rápido/económico), `thinking=low`.
   * `7 <= T <= 12`: Modelo `deepseek-v4-flash:cloud` (default), `thinking=high`.
   * `13 <= T <= 16`: Modelo `glm-5.3:cloud` (escalado), `thinking=high`.
   * `T >= 17`: Modelo `deepseek-v4-flash:cloud` o `glm-5.3:cloud` (caso por caso), `thinking=max` (solo para Kanam).
5. **Justificar siempre** la decisión en una línea antes de proceder.

---

## Restricciones

* **No usar** `thinking=max` en agentes de código (A/B). Solo en Kanam (orquestador) para diseño difícil.
* **Si el score T es 17+**, pedir **confirmación explícita a Gonzo** antes de proceder.

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
[COMPLEJITY-SCORE] T=16 (High-Complex)
  -> Modelo: glm-5.3:cloud (escalado)
  -> Thinking: high
  -> Justificación: Sistema de auth con JWT implica riesgo crítico (C=5) + refactor multi-capa (A=4). T=16 justifica escalada de modelo.
Procedo.
```
