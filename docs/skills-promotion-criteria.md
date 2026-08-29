# Criterio de Promoción de Skills

**Fecha:** 2026-08-28
**Estado:** Aceptado

---

## El Problema

El workspace tiene un set amplio de skills (96+). El riesgo es que muchas se crearon por entusiasmo o por un caso puntual, y no se usan. Una skill que no se usa es deuda: ocupa espacio, agrega ruido al índice y diluye la señal de las que sí aportan.

## El Criterio de Promoción

Una skill se promueve a **"estándar del workspace"** (referenciada en AGENTS.md, TOOLS.md o SKILLS-INDEX.md como recomendada) solo cuando demuestra **valor repetido**:

### Regla del 3x
- **Umbral**: La skill se usó en **3+ sesiones distintas** (evidencia en dailies o en el historial de uso).
- **No por entusiasmo**: Una skill creada para un caso puntual (aunque haya sido brillante) NO se promueve hasta que reaparezca en otro contexto.
- **Evidencia**: El uso debe ser verificable (mención en daily, invocación del script, referencia en un HANDOFF).

### Regla de la Poda
- **Candidata a archivo**: Una skill sin uso en **30 días** se marca como candidata a archivo.
- **Archivo**: Se mueve a `skills/_archived/` (o se elimina si no tiene valor de referencia).
- **Excepción**: Skills de vida/creatividad/infraestructura que son parte del ecosistema personal (adhd, apple-photos, etc.) se conservan aunque no se usen a diario.

## El Mecanismo

1. **Detección**: En la consolidación de memoria (Item 0.3), revisar los dailies y detectar qué skills se mencionaron.
2. **Conteo**: Mantener un registro simple de uso por skill (puede ser un archivo `skills/USAGE.md` o una columna en la DB).
3. **Promoción**: Cuando una skill alcanza el umbral 3x, se promueve a estándar (se agrega a AGENTS.md/TOOLS.md).
4. **Poda**: En la revisión mensual, marcar y archivar skills sin uso.

## Criterio de Éxito

- Cada skill estándar tiene evidencia de uso en 3+ sesiones.
- El índice de skills no crece sin control.
- Las skills que se promueven son las que realmente se usan, no las que "suenan bien".
