# ADR-070: todo estado recuperable expone su via de recuperacion

**Fecha:** 2026-09-25
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** el usuario reporto no poder ver lo generado ni recuperar nada
**Relacionado:** ADR-069 (datos de prueba), ADR-065 (DB-first vs doc-only)

---

## Contexto

Dos funcionalidades del mismo producto tenian **solo la pierna de ida**:

| Mecanismo | Ida implementada | Vuelta |
|---|---|---|
| Borrado en dos fases (`deleted_at`) | Si, desde v0.1.0 | **No existia endpoint** |
| Historial de generaciones (`generation_job.resultado`) | Si, los candidatos se guardan | **La UI nunca listaba** |

En ambos casos la spec declaraba el estado como recuperable ("ventana de recuperacion
de 30 dias"; "las propuestas quedan guardadas") y en ambos casos **el dato estaba en
disco pero era inalcanzable por la interfaz**. Gonzo lo vivio como perdida de datos: al
recargar la pagina las propuestas desaparecian, y una ficha borrada no volvia.

El sintoma se reporto dos veces con palabras distintas ("no veo modo de recuperar lo
generado", "solo veo el primer tab") y eran la misma clase de falla.

## Decision

**Un mecanismo que produce estado recuperable se entrega junto con su via de
recuperacion, en el mismo cambio.** No es una mejora posterior.

Concretamente, el Definition of Done de un mecanismo con estado recuperable incluye:

1. La operacion de vuelta expuesta por la API (listar lo recuperable + recuperar).
2. Una via en la UI para alcanzarla, no solo curl.
3. Un test que ejercite **el ciclo completo**: crear, borrar, listar lo borrado,
   restaurar, y comprobar que quedo igual que antes.
4. La operacion de vuelta registrada en el audit log (quien restauro y cuando).

La regla aplica a: borrado logico, historiales, papelones, versiones anteriores,
sesiones archivadas, snapshots, cualquier `deleted_at`, `archived_at` o `status`.

## Evidencia

- `GET /projects/{id}/entities/deleted` + `POST /projects/{id}/entities/{eid}/restore`
  + seccion Papelera. Restaurar sube version, reindexa y audita.
- `GET /projects/{id}/generations` consumido por la UI + tabla de historial con boton
  para reabrir propuestas de cualquier generacion anterior.
- El ciclo se verifico contra la API viva: 3 fichas borradas, listadas, restauradas, y
  el retrieval las volvio a encontrar.
- Contraejemplo medido: la migracion 002 marco como aplicados candidatos que nunca
  entraron, y **no habia forma de deshacerlo**. Fue el mismo error a nivel de datos:
  un estado (aplicado) sin operacion inversa (desaplicar). Se resolvio derivando el
  estado de la fuente de verdad en la migracion 003, en vez de agregar "desaplicar".

## Consecuencias

- Al disenar un mecanismo de dos fases, **la fase de vuelta se estima en el mismo
  presupuesto**, no se difiere.
- Un estado derivable es preferible a un estado almacenado: si el estado se puede
  recalcular desde la fuente de verdad (que fichas existen), no hay que mantenerlo ni
  inventar su inverso. La migracion 004 futura que agregue un flag nuevo deberia
  preguntarse primero si es derivable.
- Corolario de verificacion: "el endpoint responde 200" no prueba que la recuperacion
  funcione. Se prueba el ciclo.

## Alternativas descartadas

- **Agregar "desaplicar candidato":** descartado. El estado `aplicado` era un cache
  derivable de `card.generacion_id`; mantenerlo sincronizado exigia dos operaciones
  nuevas en vez de una. Se deriva.
- **Dejar el historial solo en la API:** descartado. La regla 2 pide via en la UI; sin
  eso el dato es alcanzable por curl y no por el usuario.
