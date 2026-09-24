# ADR-067: los ADRs del workspace no pertenecen a un proyecto - verificar el sujeto antes de borrar

**Fecha:** 2026-09-24
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** pedido de Gonzo de "eliminar los ADRs que hagan referencia a definiciones tecnológicas" y "los que hagan referencia a versiones previas de SoporteML"
**Relacionado:** ADR-001 (product-pipeline-integration), ADR-066 (guardias del workspace), ADR-048 (shadcn/Radix), ADR-037 (Lucide), ADR-036 (Turborepo/pnpm)

---

## Contexto

Al arrancar el greenfield de la nueva generación de SoporteML, Gonzo pidió limpiar los ADRs que "hagan referencia a definiciones tecnológicas" para no arrastrar decisiones viejas, y despues precisó: **aquellos que ya cumplieron su función y referencian versiones previas de SoporteML**.

La orden describe un objeto que, verificado, **casi no existe**. La auditoria previa a ejecutar cualquier borrado dio esto:

| Medición | Valor |
|---|---|
| ADRs en `docs/adr/` | **68** |
| Citados por al menos otro archivo | 30+ (ADR-001 lo citan 36, ADR-040 18, ADR-037 11, ADR-048 10) |
| **Con SoporteML como SUJETO** | **0** |
| Que lo mencionan de pasada | 11 |
| Que citan alguna tecnologia | 47 |

Los 11 que mencionan SoporteML lo hacen como **ejemplo o trazabilidad**, nunca como sujeto de la decision. Y dos de ellos afirman lo contrario de lo que la orden suponia:

- **ADR-048** (shadcn/Radix), textual: *"la familia `soporteml` queda fuera de todo barrido (ADR-001, decision de Gonzo). No se toca."*
- **ADR-037** (Lucide, `Scope: Global - aplica a todos los proyectos`): lo cita como *"ya usado en Soporteml v1/v3"*.

Los ADRs que **si** cumplian el criterio estaban en otro lugar: los repos de v3 y v4 (independencia de vendor, runtime Node+Hono, tokens de Lovable), no en el workspace. Los ADRs de un proyecto viven en el repo del proyecto.

### El blast radius de la orden, tal como estaba formulada

Borrar "los 47 que citan tecnologia" habria eliminado decisiones que hoy sostienen entre 7 y 20 proyectos:

- ADR-048 (shadcn/Radix) -> citado en **20** proyectos
- ADR-037 (Lucide) -> **15**
- ADR-036 (Turborepo/pnpm) -> **7**

Ninguno de esos proyectos es SoporteML. Resetear un producto no justifica romper el ecosistema que lo hospeda.

---

## Decision

**Ningun borrado se ejecuta sin verificar antes el sujeto de la orden y su blast radius.**

### 1. Distinguir "es el sujeto" de "lo cita"

La prueba no es `grep -l "soporteml" docs/adr/*.md` (devuelve citas), sino sobre el **titulo** del ADR. Un ADR cuyo titulo no nombra al proyecto no es del proyecto, aunque lo mencione en el cuerpo.

```bash
for f in docs/adr/*.md; do
  head -1 "$f" | grep -qi "<proyecto>" && echo "SUJETO: $f"
done
```

### 2. Medir el blast radius antes de tocar

Contar cuantos archivos referencian cada ADR candidato, **fuera de su propio archivo**:

```bash
grep -rl "ADR-NNN" docs/ projects/*/.knowledge/ memory/*.md skills/ | grep -v "docs/adr/ADR-NNN-"
```

Un ADR con 15 referencias externas es infraestructura del ecosistema, no deuda.

### 3. Los ADRs de un proyecto viven en el repo del proyecto

Un ADR de alcance de proyecto (stack, runtime, design tokens de esa app) pertenece al repo de esa app. El workspace aloja decisiones de alcance general. Mezclarlos es lo que produjo la confusion que origino este ADR.

### 4. Archivar antes que borrar

Cuando una decision de version cerrada ya cumplio su funcion: `Estado: ARCHIVADO` con el motivo y la fecha. Sale del espacio de decision -que es el objetivo real- sin perder el *por que*. Borrar la evidencia de un error invita a repetirlo; los cuatro ciclos de SoporteML son el caso testigo.

---

## Consecuencias

### Positivas
- Queda registrado que **ningun ADR del workspace es de SoporteML**, con la medicion que lo prueba. Un futuro intento de "limpiar los ADRs de SoporteML" choca con este ADR y su evidencia, en vez de con otra auditoria de 20 minutos.
- El blast radius entra como paso obligatorio: la pregunta "¿quien depende de esto?" se hace antes, no despues.
- Se refuerza el principio de ADR-001 de portfolio (el proyecto no se toca sin pedido explicito de Gonzo) sin contradecirlo: esta vez **lo pidio explicitamente**, asi que la puerta estaba abierta - pero para el proyecto, no para el workspace.

### Negativas
- **Un barrido de "limpieza" requiere auditoria previa**, lo que agrega friccion a una tarea que parece trivial. Es el costo deliberado: la operacion parece obvia y no lo es.
- El precedente de ADR-037 (*"ya usado en Soporteml v1/v3"* como parte del fundamento) **queda pendiente de limpieza**: es precedente fabricado segun la regla de `USER.md`, y la correccion es acotarlo a su fundamento tecnico. No se hizo en este ADR para no mezclar dos cambios.

### Fuera de alcance
- **No** se borra ni archiva ningun ADR del workspace en esta decision. La decision es sobre el *procedimiento*, no sobre un archivo concreto.
- El destino de los ADRs tecnologicos de v3/v4 (archivar vs borrar) es **decision pendiente de Gonzo** y vive en su propio ADR, porque son de otro repo.

---

## Alternativas consideradas

1. **Ejecutar el borrado como se pidio.** Rechazada: habria eliminado decisiones de 15-20 proyectos vivos para resetear uno. La orden describia un objeto que casi no existe (0 de 68 como sujeto).
2. **Marcar `Superseded` los ADRs tecnologicos.** Rechazada: no estan superseded por nada -siguen gobernando a los proyectos que los usan-. Un estado falso es peor que el ruido.
3. **Mover los 11 que mencionan SoporteML a otro directorio.** Rechazada: son decisiones de alcance general que casualmente lo citan. Moverlas rompe las referencias de los proyectos que las usan y no elimina ninguna deuda real.
