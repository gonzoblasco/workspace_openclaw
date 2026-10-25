# Rework: A corrige con el reporte de B

Pregunta que responde este bench: cuando hay que corregir algo, ¿**A** (el autor)
corrige con el reporte de **B**, o corrige **B** directamente?

## Diseño

- Artefacto: `reports.py` con 4 bugs sembrados (mismo ground truth que el head-to-head).
- A (`gpt-oss:120b-cloud`) recibe el **reporte de findings de B** y corrige.
- Se mide: recall final, cobertura de los findings de B, iteraciones y lineas cambiadas.

## Resultado medido (2026-10-25)

| Metrica | Rework (A corrige) | B corrige directo (deepseek) |
|---|---|---|
| Recall final | 4/4 | 4/4 |
| Findings de B cubiertos | 7/8 | 9/9 (todos) |
| Iteraciones | 2 | 1 |
| Lineas cambiadas | 35 | 46 |
| Agentes involucrados | 3 (A, B, A) | 2 (A, B) |
| Requests de pipeline | +50% | base |

**El unico finding que A no cubrio** (de los 9 que reporto B): `filter_by_date`
descarta fechas que son objetos `datetime` reales o strings ISO con componente
horario (`date.fromisoformat` falla con `"2023-01-05T10:00:00"` y el `except`
los ignora en silencio). A no lo vio porque no estaba en el reporte que recibio.

**Conclusion**: el rework funciona (mismo recall que corregir directo) pero
cuesta un 50% mas de requests y pierde los hallazgos que el autor no puede
verificar por si mismo. El argumento a favor del rework es la propiedad
"el autor conoce la intencion"; el argumento en contra es el costo y el
findings que se escapan.
