# Regression Control Gate (Kanam OS) 🌿

> **Estado: EXPERIMENTO NO ADOPTADO (2026-10-06).** La implementación existe (`scripts/regression_gate.py`, reparada el 2026-10-06: no compilaba) pero **nada la invoca**. Se conserva como spec; no se borra.

Este sistema implementa el "Freno de Mano de Calidad". Su objetivo es garantizar que ninguna actualización del workspace degrade la calidad sistémica medida a través de la rúbrica SHARP.

## 📉 El Concepto de Degradación

Un cambio se considera **Degradado** si el resultado final reduce la puntuación de calidad en uno o más ejes de SHARP, sin que exista una justificación técnica superior (trade-off documentado).

### Matriz de Alerta

| Caída de Puntaje | Estado | Acción Obligatoria |
| :--- | :--- | :--- |
| **0 - 2 pts** | 🟢 Estable | Integración permitida. |
| **3 - 5 pts** | 🟡 Alerta | Registro de deuda técnica en el Daily. |
| **> 5 pts** | 🔴 Bloqueo | El commit se marca como "Regression". Requiere revisión manual de Gonzo. |

## 🛠️ Flujo de Trabajo del Gate

1. **Pre-Commit Scan:** El sistema identifica los archivos modificados.
2. **SHARP Baseline:** Se recupera el puntaje de la última versión estable (desde `.knowledge/quality_baseline.json`).
3. **Evaluation:** Se corre la evaluación del nuevo estado.
4. **Comparison:** Se calcula la delta $\Delta = \text{Baseline} - \text{Actual}$.
5. **Verdict:** Si $\Delta > \text{Umbral}$, se dispara el bloqueo o la alerta.

---

*Actualizado el 2026-10-01. Parte del Sprint 2.2 - Regression Control.*
