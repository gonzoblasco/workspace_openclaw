# Log de decisiones editoriales

> Registro de **qué elegí, por qué, y qué cambió Gonzo** en cada pieza entregada.
> Sirve para una cosa: no repetir una corrección que ya me hiciste.

**Diferencia con otros archivos:**

| Archivo | Qué guarda |
|---|---|
| `docs/voz-gonzo.md` | Cómo escribe Gonzo. Reglas durables, sin proyecto |
| `memory/editorial-guidelines.md` | Qué cambia por proyecto y superficie |
| **`memory/editorial-log.md`** (este) | Qué pasó en cada pieza concreta: elección, motivo, corrección |

---

## Formato de entrada

```
### YYYY-MM-DD - <proyecto> - <pieza>

**Pedido:** qué se pidió, en una línea.
**Entrega:** ruta del artefacto.
**Elecciones discutibles:** qué elegí y por qué (las que no eran obvias).
**Corrección de Gonzo:** qué cambió. Si no hubo, "aprobado sin cambios".
**Patrón:** qué regla emerge. Vacío si es caso único.
**Destino del patrón:** si se consolidó en voz-gonzo o editorial-guidelines, decirlo acá.
```

**Regla:** si el patrón se repite dos veces, deja de ser caso y se consolida
en `docs/voz-gonzo.md`. Este log no debe crecer con reglas duplicadas.

---

## Entradas

### 2026-11-09 - Kanam STUDIO - Auditoría de la sesión 2026-11-06

**Pedido:** revisar que la sesión del viernes no haya introducido errores.
**Entrega:** este registro + 3 correcciones en `editorial-guidelines.md` y `ROADMAP.md`.
**Verificado contra el disco:** 7 archivos commiteados presentes, pasos 1-6 de
AGENTS.md sin huecos, 3 referencias a `voz-gonzo` en skills, 11 artículos,
22 repos / 16 PRs de OSS-TRACKER, `preflight/README.md` 8974 bytes,
`kanam-onwheels` inexistente.
**Hallazgo 1 (no mío):** `docs/voz-gonzo.md` tiene la numeración de reglas con
la 8 faltante (pasa de 7 a 9). Precedía a mi commit: ya estaba en `5dbec551ae~1`.
**Resuelto el 2026-11-09:** la regla 8 era "Guion común (-) siempre", retirada
por ADR-082 (`c22fc400a5`) sin renumerar. No se reescribe: se deja la línea
tachada con el motivo, para que el hueco sea legible y no parezca una pérdida.
Yo leí el archivo el viernes y no lo vi. Ahora que es canónico, pesa.
**Hallazgo 2 (mío, razonamiento):** el viernes "restauré" 3 reviews de
`kanam-critic` asumiendo que staging ajeno = archivos válidos. Eran copias
anidadas por un bug de cwd relativo, borradas correctamente en `c9db4a14f7`.
Reviví basura que se iba a borrar igual. Daño nulo, criterio equivocado.
**Hallazgo 3 (mío, documental):** `editorial-guidelines.md` decía "Acción
pendiente" sobre algo ya ejecutado (1.4). Contradecía la realidad dentro del
mismo archivo. Corregido.
**Hallazgo 4 (mío, conteo):** dije "13 reglas consolidadas" y hay 12.
Corregido en ambos archivos.
**Patrón:** un archivo que declara un estado puede quedar obsoleto por un
cambio hecho en la misma sesión. La regla del disco aplica también a mis
propios documentos, no solo a los de terceros.

### 2026-11-06 - Kanam STUDIO - Post de kanam-fixer (Pipeline A, primer uso real)

**Pedido:** usar `kanam-fixer` como caso de uso para empezar a promocionar.
**Entrega:** borrador de post (LinkedIn + X), descartado el 2026-11-06 a pedido
  de Gonzo: el foco de la sesión era optimizar el agente, no publicar. Se borró.
  El README y la trampa #7 sí quedaron corregidos y son el valor real del caso.
**Elecciones discutibles:**
- La tesis del post no es la feature sino **la parcialidad de la medición**: el
  plano virtual detecta atributos y falla en timing/viewport. Un post de
  "construí esto y funciona" no se distingue; uno que mide y declara el límite, sí.
- Saqué todas las métricas de vanidad (0 stars) y los conteos de tests: no son
  la tesis y abaratan.
- CTA: "probarlo", sin pedir stars ni cerrar con pregunta.
- Verifiqué los números contra el código (4 opciones, posinset 9, setsize 99).
  No puse el costo del ciclo porque no lo sé y no lo invento.
**Corrección de Gonzo:** "adelante" sin cambios de redacción.
**Hallazgo colateral:** el README decía "Not published" y el registry dice 0.0.2
(17/09/2026). Corregido el README y marcada la trampa #7 como resuelta.
**Patrón:** un post con el límite medido vale más que uno con la promesa. Es la
misma lógica del artículo de modelos, aplicada a un proyecto propio.
**Destino del patrón:** candidato a `editorial-guidelines.md` (superficie 4) si
se confirma en un segundo post.

### 2026-11-06 - Kanam STUDIO - Unificación de voz (Fase 1)

**Pedido:** validar el guideline y resolver la decisión de posts públicos.
**Entrega:** `docs/voz-gonzo.md`, `content-serializer/SKILL.md`,
`copy-editing/SKILL.md`.
**Elecciones discutibles:**
- Gonzo dijo "no sé" ante la decisión de branding. En vez de dejarla abierta,
  la resolví con evidencia: el contenido de branding sale de artículos,
  READMEs y PRs, que ya están escritos en `voz-gonzo`. Un registro aparte
  sería la cuarta definición del mismo problema.
- Elegí **modular**, no duplicar: `voz-gonzo` gana la tabla de tipos de pieza
  y `content-serializer` pasa a referenciarla.
**Corrección de Gonzo:** "bien" (1), "no sé" (2), "no" (3 y 4). Ninguna
corrección de redacción.
**Patrón:** ante un "no sé" con datos disponibles, resolver con evidencia
citada en vez de devolver la pregunta. Marcar la decisión como tomada y su
fundamento, para que se pueda revertir con criterio.
**Destino del patrón:** candidato a `AGENTS.md` si se repite.

### 2026-11-06 - Kanam STUDIO - ROADMAP v0.2.1

**Pedido:** planificar cómo convertir a STUDIO en un agente con demanda real.
**Entrega:** `ROADMAP.md`.
**Elecciones discutibles:**
- Propuse 3 skills nuevas. Gonzo corrigió: "definamos workflows y pipelines
  mejores en lugar de seguir agregando cosas".
- Al revisar, encontré que `voice-calibrator` ya existía como `docs/voz-gonzo.md`.
  Error mío: propuse crear lo que no había leído.
- Reescrito a "0 skills nuevas": las candidatas pasan a ser etapas de pipeline.
**Corrección de Gonzo:** reemplazar acumulación por consolidación. Explícita y
en una línea.
**Patrón:** **leer lo que ya existe antes de proponer algo nuevo.** Antes de
crear una skill, buscar si un archivo, skill o pipeline ya lo cubre.
**Destino del patrón:** consolidado en el principio rector del ROADMAP.
Candidato a `AGENTS.md` cuando se confirme en una segunda pieza.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
