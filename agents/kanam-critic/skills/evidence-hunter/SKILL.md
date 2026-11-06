---
name: "evidence-hunter"
description: "Caza evidencia verificable en el repositorio para sustentar los ejes de la rúbrica SHARP. Convierte afirmaciones del autor en pruebas automáticas (git diff, pruebas unitarias, búsquedas de código) y genera una tabla de evidencia citada.")
metadata:
  category: "Critic"
  tags:
    - critic
    - sharp
    - evidence
    - verification
    - git
    - auto-test
---

# evidence‑hunter

**Propósito**: Automatizar la recolección de evidencia concreta que respalde o refute cada afirmación de un entregable antes de aplicar la rúbrica SHARP. El objetivo es eliminar la dependencia de *auto‑reportes* y elevar los ejes **Resistance** y **Sharpness** del Critic.

## Cuándo usarla

Se invoca automáticamente por `sharp‑adversarial‑review` cuando el entregable incluye una sección de *“Afirmaciones del autor”* (por ejemplo, `README.md` con ✅ ✔️ o en comentarios de PR). También puede llamarse manualmente para validar cualquier conjunto de afirmaciones externas.

## Entrada

```yaml
assertions:
  - description: "La función foo() está cubierta por pruebas unitarias"
    source: "src/foo.py:12"
  - description: "El componente Header está implementado con React y usa el token `color-primary`"
    source: "src/components/Header.jsx:3"
```

* `assertions` - lista de objetos con `description` (texto libre) y `source` (ruta opcional para ayudar al motor a localizar rápidamente). Las descripciones pueden incluir palabras clave que el motor reconoce (`prueba`, `test`, `cobertura`, `token`, `dependency`, `build`).

## Proceso (Procedimiento)

1. **Parseo de afirmaciones** - se extraen palabras‑clave y se genera una serie de *detectors* (git‑diff, grep, test‑runner, dependency‑checker).
2. **Ejecución de detectores** - en orden de costo (git → test → grep → dependency). Cada detector produce un resultado:
   - `verificado` - evidencia encontrada en el repo o en la salida de pruebas.
   - `parcial` - evidencia parcial (por ejemplo, solo el archivo existe pero la prueba falla).
   - `auto‑reportado` - no se encontró evidencia; la afirmación depende solo de la palabra del autor.
   - `bloqueado` - no se pudo ejecutar (falta herramienta, error de sintaxis, etc.).
3. **Normalización** - se asigna a cada afirmación una *cita* del tipo `ruta:línea` o `comando‑output`.
4. **Construcción de tabla** - se genera una tabla Markdown con columnas:

   | Afirmación | Estado | Evidencia (cita) |
   |------------|--------|-------------------|
   | … | verificado | `src/foo_test.py:45` |
   | … | auto‑reportado | - |

5. **Salida estructurada** - además de la tabla, se devuelve JSON con la lista de objetos `assertionId`, `status`, `evidence` para que la skill `sharp‑adversarial‑review` lo inserte directamente en su reporte.

## Salida

```json
{
  "evidenceTable": "| Afirmación | Estado | Evidencia |
|---|---|---|
| La función foo() está cubierta por pruebas unitarias | verificado | src/tests/test_foo.py:23 |
| … | auto‑reportado | - |
",
  "details": [
    {"id":0,"status":"verificado","evidence":"src/tests/test_foo.py:23"},
    {"id":1,"status":"auto‑reportado","evidence":null}
  ]
}
```

## Integración con `sharp‑adversarial‑review`

La skill `sharp‑adversarial‑review` debe:
1. Llamar a `evidence‑hunter` pasando las afirmaciones extraídas del entregable.
2. Incluir la tabla Markdown generada en la sección **Evidencia** de cada eje SHARP.
3. Usar los campos `status` para decidir si el eje puede puntuarse (solo `verificado` o `parcial` permiten puntuar; `auto‑reportado` obliga a **VETO** o a **puntos de fricción**).

## Ejemplo de uso en pipeline

La skill es una **procedimiento de agente**, no un subcomando del CLI. El CLI de OpenClaw
(`openclaw skills`) sirve para **descubrirla y verificarla**, no para ejecutarla:

```bash
# Verificar que la skill esta visible y lista para este agente
openclaw skills list --agent kanam-critic | grep evidence-hunter
openclaw skills check --agent kanam-critic

# Ejecutar el runner (si el detector es el que produce la evidencia)
python3 agents/kanam-critic/bin/evidence-hunter.py assertions.yaml > evidence.json

# Validar la salida contra los casos canonicos del lab
python3 agents/kanam-critic/tests/evidence-hunter/validate.py evidence.json
```

**Nota (2026-11-06):** hasta esta version la skill prometia `openclaw skill run evidence-hunter`;
ese comando no existe (el CLI real es `openclaw skills`, sin subcomando `run`). Promesa rota
promesa incumplida. Corregido contra `openclaw skills --help`.

## Dependencias

- `git` (para `git diff --name-status`)
- Entorno Python con `pytest` (para detectar pruebas unitarias)
- Herramienta de búsqueda `rg` (ripgrep) para expresiones regulares en código.

Todas están ya presentes en el workspace del OS Kanam.

## Red Lines (líneas rojas)

- **No asumir que una afirmación es cierta sin evidencia verificable.** Si el detector no encuentra nada, el estado queda `auto‑reportado` y el Critic debe volver a VETO.
- **No ejecutar código arbitrario del autor.** Sólo se permiten comandos seguros (`git`, `pytest`, `rg`).
- **No manipular la tabla final** fuera del formato Markdown especificado.

## Referencias

- `.knowledge/SHARP.md` - definición oficial de la rúbrica.
- `.knowledge/SKILLS-ARCHITECTURE.md` - política de entrada pública de skills.
- `agents/kanam-critic/skills/sharp-adversarial-review/SKILL.md` - skill que coordina el flujo.

---

*Esta skill está diseñada para ser pública y reutilizable dentro del ecosistema Kanam.*

<!-- project: github.com/gonzoblasco/workspace_openclaw -->

