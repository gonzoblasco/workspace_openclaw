# Rúbrica de Calidad SHARP (Kanam OS) 🌿

Este documento es el estándar de medición de calidad para todo entregable de Kanam (código, diseño, documentación, decisiones). El objetivo es eliminar la subjetividad y reemplazarla por una **presión adversarial basada en evidencia**.

## 📐 Los 5 Ejes de Evaluación

Cada entregable se evalúa en una escala de **1 a 5** por cada eje.

### 1. Sharpness (Nitidez)
*Mide la precisión y la ausencia de ruido.*
- **1:** Difuso, redundante, lleno de "muletillas" de IA o dudas.
- **3:** Claro, pero con algunas secciones innecesarias.
- **5:** Cirúrgico. Cada palabra y cada línea de código tiene una razón de existir.

### 2. Horizon (Horizonte)
*Mide la capacidad de anticipación y sostenibilidad.*
- **1:** Solución "parche" que crea deuda técnica inmediata.
- **3:** Soluciona el problema actual sin romper nada, pero no escala.
- **5:** Visión sistémica. Resuelve el problema y prepara el terreno para la siguiente etapa.

### 3. Asymmetry (Asimetría)
*Mide la relación Esfuerzo $\rightarrow$ Valor.*
- **1:** Sobre-ingeniería masiva para un problema trivial.
- **3:** Esfuerzo equilibrado con el resultado.
- **5:** "Palanca de Arquitectura". Un cambio mínimo que genera un impacto masivo en la eficiencia.

### 4. Resistance (Resistencia)
*Mide la robustez y el manejo de casos borde.*
- **1:** Frágil. Funciona solo en condiciones perfectas.
- **3:** Robusto en el camino feliz, maneja errores básicos.
- **5:** Indestructible. Anticipa fallos, tiene logs claros y es a prueba de errores humanos.

### 5. Parsimony (Parsimonia)
*Mide la simplicidad elegante.*
- **1:** Complejidad innecesaria, dependencias superfluas.
- **3:** Solución estándar, sin excesos pero sin optimización.
- **5:** Elegancia minimalista. La solución más simple posible que resuelve el problema al 100%.

---

## 📊 Matriz de Calificación

| Puntaje Total | Clasificación | Acción Obligatoria |
| :--- | :--- | :--- |
| **0 - 12** | 🔴 **Mediocre** | Rechazo inmediato. Re-diseño total. |
| **13 - 18** | 🟡 **Funcional** | Aceptado, pero se registra la deuda técnica. |
| **19 - 23** | 🟢 **Alta Calidad** | Aprobado. Se convierte en referencia. |
| **24 - 25** | ✨ **Excepcional** | Oro. Se documenta como "Best Practice" del sistema. |

## 🛠️ Proceso de Auditoría (El Ritual)
Para evaluar un entregable, no se usa una intuición. Se sigue este proceso:
1. **Presentación:** El autor presenta el resultado.
2. **Ataque Adversarial:** El Auditor (o el Critic) busca activamente dónde el resultado falla en uno de los 5 ejes.
3. **Puntuación:** Se asigna el valor por eje basándose en evidencia (ej: *"esto es un 2 en Parsimonia porque agregaste 3 dependencias para una función de 10 líneas"*).
4. **Veredicto:** Se suma el total y se decide la acción.

---

*Actualizado el 2026-10-01. Basado en el estándar SHARP del Academic Multi-Agent System.*
