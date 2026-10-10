# Spec Draft: JobHuntingPipelineV1.md

## 1. Objetivo
Crear un flujo semi-autónomo para la gestión de búsqueda de empleo, donde la transición entre pasos (Descubrimiento $\rightarrow$ Estrategia $\rightarrow$ Redacción $\rightarrow$ Revisión) se decide por un mecanismo de auto-scoring interno, reduciendo la necesidad de intervención humana por defecto.

## 2. Componentes de Misión
1.  **Researcher:** Entrada $\rightarrow$ Keywords/Requisitos.
2.  **Strategist:** Keywords $\rightarrow$ Plan de ataque (personalización del mensaje).
3.  **Writer:** Plan + CV $\rightarrow$ Borrador de Material.
4.  **Critic (Validator):** Borrador + CV $\rightarrow$ Score de Confianza (0-100).

## 3. Mecanismo de Auto-Scoring (Gate)
El `Critic` es el árbitro. Su salida no es binaria (OK/FAIL) sino un objeto JSON:
```json
{
  "score": 78, // Valor entre 0 y 100
  "confidence_level": "HIGH" | "MEDIUM" | "LOW",
  "feedback": "Mensaje específico para el paso anterior."
}
```
**Regla de Avance (Decision Rule):**
*   **IF Score >= 80:** Avance automático al siguiente paso.
*   **IF Score >= 65 AND Confidence == "HIGH":** Avance automático, pero marca el registro como "Auto-aprobado/Bajo Riesgo".
*   **ELSE (Score < 65 o Confidence == "LOW"):** Detener y requerir intervención humana/Generar **Intervención de Gonzo**.

## 4. Flujo de Ejecución (Diagrama Mental)
(Se implementará con un script de orquestación `job-hunting-pipeline.sh`)

1.  [INPUT] $\rightarrow$ 2. Researcher $\rightarrow$ 3. Strategist $\rightarrow$ 4. Writer $\rightarrow$ 5. Critic $\rightarrow$ [Decision Engine] $\rightarrow$ (Loop/End)

## 5. Próximos Pasos
*   [ ] Implementar `scripts/job-hunting-pipeline.sh` (Orquestador).
*   [ ] Definir la plantilla de `job-hunting-pipeline.md` en el `.knowledge/`.
*   [ ] Testear el `ComplexityScorer` en un caso de uso simulado.

---
# metadata
version: 0.1
status: DRAFT
owner: Kanam
date: 2026-10-09
source_agent: main
<!-- project: github.com/gonzoblasco/workspace_openclaw -->
