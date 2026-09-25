# ADR 0001: Verificacion en dos capas (determinista primero, modelo para lo que requiere juicio)

- **Fecha:** 2026-09-24
- **Contexto:**
  La app genera una especificacion tecnica en 14 secciones a partir de un brief. El problema es que "brief entra, texto sale" ya lo hace cualquier chat con un LLM: sin nada mas, la app es un envoltorio. La funcion `buildReviewMessages` (revision cruzada del documento con el modelo) se escribio en el primer commit, con tests, y **nunca se cableo a la UI**: la capacidad que justifica la herramienta estaba dormida.

  Al decidir como cerrar ese hueco aparecieron dos familias de problemas muy distintas:
  - **Objetivos y comprobables:** una seccion quedo en el esqueleto, un requisito no tiene criterio de verificacion, hay un `TBD` o una celda vacia. Esto se detecta mirando el texto, sin interpretarlo.
  - **De juicio:** dos secciones se contradicen, una decision no se sostiene, un requisito contradice un supuesto de otra seccion. Esto requiere entender el documento completo.

  Tratarlas igual tenia un costo concreto: si todo depende del modelo, saber que falta una seccion exige esperar una llamada a Ollama, y el resultado deja de ser confiable (un modelo puede no reportar una seccion vacia, que es un hecho verificable).

- **Decision:**
  **Dos capas separadas, con origenes distintos y visibles en la UI.**

  1. **Linter determinista (`src/lib/lint.ts`), sin modelo.** Funcion pura que detecta secciones sin contenido, requisitos sin criterio de verificacion y plantillas sin completar (TBD/TODO/FIXME, corchetes de ejemplo, celdas vacias). Devuelve hallazgos con severidad (alta, media, baja). Es instantaneo, gratis y no falla.
  2. **Revision con modelo, cableada a la UI.** Reusa `buildReviewMessages` y `streamChat` (con `onThinking`, porque el modelo razona antes de escribir). Detecta lo que requiere leer el documento en cruz: contradicciones, huecos, cambios de mayor impacto.
  3. **El linter es valor derivado, no estado guardado.** Se recalcula en cada render con `useMemo`. Guardarlo obligaria a invalidarlo; siendo puro, no puede quedar desincronizado del documento.
  4. **El resultado del modelo si se persiste**, con marca de vigencia: el documento guarda `review.docUpdatedAt` y la vigencia se resuelve comparando contra `updatedAt`. Guardar la revision no debe tocar `updatedAt`, o la revision se marcaria desactualizada a si misma.
  5. **El estado de verificacion entra al export** como seccion final. La spec circula como archivo: si los problemas quedan solo en la UI, quien recibe el `.md` no los ve. Exportar no se bloquea.

- **Alternativas descartadas:**
  - **Una sola capa con LLM que haga todo.** Descartada: degrada el determinismo, encarece y hace lento hasta lo trivial. Un hecho comprobable no deberia depender de un modelo.
  - **Guardar tambien los hallazgos del linter.** Descartada: es estado derivado, y persistirlo crea el problema de invalidarlo sin ninguna ganancia (`lintDoc` es puro y rapido).
  - **Parsear el texto del modelo a hallazgos estructurados.** Descartada por fragil: el modelo devuelve markdown libre. Los hallazgos estructurados son los del linter; el texto del modelo se muestra tal cual, en su propio grupo.
  - **Bloquear el export si hay hallazgos altos.** Descartada: la spec se puede entregar con problemas conocidos. Informar y bloquear no son lo mismo, y bloquear rompe el uso real (una spec a medio escribir que queres compartir para pedir opinion).
  - **Auto-corregir las secciones flojas con el modelo.** Descartada: la app reporta, no reescribe. Decidir que cambiar es del autor.

- **Consecuencias:**
  - La app deja de ser un generador de texto y pasa a cerrar un ciclo: brief, generacion por seccion, deteccion de problemas, revision cruzada, export verificable.
  - El panel muestra los hallazgos por origen (linter / modelo), lo que hace evidente que capa encontro cada cosa. El mismo problema puede aparecer en las dos; se acepta, con origen etiquetado. Deduplicar queda como pregunta abierta.
  - La revision puede quedar desactualizada al editar. Es visible y se avisa, en vez de mostrar como vigente algo viejo.
  - Los documentos guardados antes de este cambio no se rompen: `normalizeDoc()` los normaliza como "sin revision".
  - El limite real del enfoque: si el linter no lo ve y el modelo no lo reporta, el problema pasa. La verificacion es una ayuda, no una garantia.
  - Sin dependencias nuevas. La spec formal vive en `openspec/changes/add-spec-review/` (proposal, specs, design, tasks).

- **Referencias:**
  - OpenSpec change: `openspec/changes/add-spec-review/` (capacidades `spec-lint` y `spec-review`)
  - `src/lib/lint.ts`, `src/lib/review.ts`, `src/components/ReviewPanel.tsx`
  - Regla del workspace: ADR-067 (los ADRs del workspace no pertenecen a un proyecto; los del proyecto viven en el repo del proyecto)

- **Estado:** Aceptado
