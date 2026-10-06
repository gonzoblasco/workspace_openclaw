# Skill Evals System (Kanam OS) 🌿

> **Estado: EXPERIMENTO NO ADOPTADO (2026-10-06).** La implementación existe (`scripts/eval-engine.py`) pero **nada la invoca** (ni pre-commit ni cierre de sesión). Se conserva como spec del experimento de la Etapa 2; no se borra. Si se retoma el frente "ciclo de vida de skills", este es el punto de partida.

Este sistema define cómo se verifica el comportamiento de una skill. Una skill no se considera "estable" solo porque el código corre, sino cuando pasa sus **Assertions**.

## 📄 Formato de Assertions (`.eval.yaml`)

Cada skill debe tener un archivo adjunto llamado `nombre-de-la-skill.eval.yaml`. Este archivo define los casos de prueba obligatorios.

### Estructura del YAML
```yaml
skill: "nombre-de-la-skill"
version: "1.0.0"
assertions:
  - id: "test-01"
    description: "Verifica que el sistema maneje entradas vacías"
    input: ""
    expected: "Error: Entrada vacía"
    forbidden: ["None", "Null", "Crash"]
    critical: true # Si falla, la skill se marca como FAIL inmediata

  - id: "test-02"
    description: "Prueba de flujo nominal"
    input: "Hola Kanam"
    expected: "Hola Gonzalo"
    critical: false
```

## 🚦 Estados de Evaluación

Al correr el motor de `evals`, cada test puede resultar en:

| Estado | Significado | Acción |
| :--- | :--- | :--- |
| **PASS** | El output contiene lo esperado y NO contiene lo prohibido. | ✅ Ninguna. |
| **FAIL_CRITICAL** | Falló un test marcado como `critical: true`. | ❌ Bloqueo de integración. |
| **FAIL_SOFT** | Falló un test no crítico. | ⚠️ Registro de deuda técnica. |
| **CHRONIC** | El test falla consistentemente en las últimas 5 ejecuciones. | 🛠️ Trigger automático de `skill-repair`. |

## 🔄 El Ciclo de Estabilización

1. **Draft:** La skill se escribe y se crea su `.eval.yaml`.
2. **Testing:** Se corre el `eval-engine`.
3. **Iteration:** El autor corrige la skill basándose en los fallos del eval.
4. **Stabilization:** La skill pasa el 100% de sus tests críticos. Solo entonces se marca como **READY** para uso en producción.

---

*Actualizado el 2026-10-01. Parte del Sprint 2.1 - Ciclo de Vida de la Skill.*
