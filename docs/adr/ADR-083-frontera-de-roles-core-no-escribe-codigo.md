# ADR-083: Frontera de roles - el CORE orquesta y no escribe código

**Fecha:** 2026-09-29
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** El CORE escribió el código de producción de `kanam-onwheels` durante una sesión entera. Gonzo preguntó por qué no se usaba `kanam-dev`, y la respuesta fue que la regla existía, estaba escrita, y nada la verificaba.
**Relacionado:** ADR-073 (arquitectura multi-agente), ADR-074 (protocolo de despacho), ADR-056 (guardas de gobernanza), ADR-066 (los guardias no leen código de proyecto)

---

## Contexto

El **2026-09-29**, durante el arranque de `kanam-onwheels`, el CORE escribió directamente:
migraciones SQL, el cliente de datos de Supabase, el panel completo (login, stock, revisión, alta),
la UI de aprobación, un e2e de Playwright, y las correcciones que sus propios tests destaparon.

Nada de eso es su dominio. Es el dominio de `kanam-dev`.

**La regla existía y estaba escrita en tres lugares:**

- `SKILLS-INDEX.md` §2.4: *"El Core **no ejecuta** skills de otro rol: las delega. `scripts/dispatch-validation.sh <skill> <agent>` lo verifica."*
- ADR-073: *"El CORE utiliza el `skill-router` ... y **delega la tarea al agente especialista** mediante `sessions_spawn`."*
- ADR-074: *"El `kanam-core` no ejecuta tareas de ejecución; **despacha** tareas de ejecución."*

Las tres se violaron sin que nada avisara. Ese es el patrón que este ADR cierra.

### La causa mecánica (por qué la regla no se sostuvo)

La regla estaba escrita como **documentación**, no como **contexto**. Los dos archivos que el CORE
lee siempre son `AGENTS.md` (bootstrap) y su propio catálogo de skills. Ninguno de los tres lugares
donde la regla vivía es alguno de esos dos:

| Dónde estaba la regla | ¿El CORE lo lee siempre? |
|---|---|
| `SKILLS-INDEX.md` §2.4 | No: es un inventario que se consulta |
| ADR-073 / ADR-074 | No: son documentación de decisión |
| `AGENTS.md` | **Sí** - no mencionaba la delegación en absoluto |

Y el catálogo jugaba en contra: **las 9 skills del ciclo de desarrollo (`hermes-*`) vivían en
`skills/`, el árbol del CORE.** Entre ellas `hermes-builder`, cuya descripción es, textualmente:
*"implementation. Writes the change's code and nothing else."* El CORE tenía el playbook de
ingeniería a la vista y lo ejecutó. Lo que un agente ve, un agente lo hace.

### El verificador citado no verificaba nada

`scripts/dispatch-validation.sh` existe desde 2026-09-26. Su docstring dice que valida que el Core
no ejecute una skill ajena. Tres problemas:

1. **Es voluntario.** Hay que invocarlo con el nombre de la skill. Si el CORE no lo corre, no pasa nada. **Nadie lo invoca:** sus únicas referencias eran sus propios docs.
2. **Es reactivo, no estructural.** Responde "¿esta skill existe en otro agente?", no "¿el CORE ejecutó trabajo de otro rol?".
3. **No tiene test.** Un check sin suite es indistinguible de un check ausente.

El ADR-074 lo había dejado como pendiente sin marcar: *"Implementar validación de despacho: si el Core intenta ejecutar una tarea de `kanam-dev` directamente, el sistema debe alertar que la tarea debe ser delegada."* Este ADR la implementa.

---

## Decisión

**El CORE orquesta; no ejecuta el trabajo de un rol.**

### 1. El alcance del CORE sobre un proyecto

Sus **artefactos de gobierno**: discovery, specs, ADRs, `.knowledge/`. Ahí escribe y responde.

**El código de producción de un proyecto no es suyo.** Tampoco el deploy, el research ni el
contenido: son de DEV, OPS, MIND y STUDIO respectivamente.

El criterio operativo: antes de escribir, *¿esto es gobernar el proyecto o implementarlo?* Si es
implementar, se delega.

### 2. La separación de árboles ES el enforcement

Una skill de un rol vive en `agents/<rol>/skills/`, **nunca** en `skills/`.

Esto no es cosmético ni organización de carpetas: **lo que el CORE ve, el CORE lo ejecuta.** Un
prompt es una instrucción que se puede ignorar; un catálogo es una capacidad que se ejerce. Por eso
la corrección estructural es mover el ciclo SDD fuera del árbol del CORE, no pedirle al CORE que se
porte bien.

Consecuencia: las 9 skills `hermes-*` se mueven de `skills/` a `agents/kanam-dev/skills/`.
El CORE conserva `sdd-agent-loop`, que es el **orquestador** del ciclo - sabe qué etapa sigue y a
quién delegarla, sin saber cómo se implementa.

### 3. La regla vive en el bootstrap

La regla va a `AGENTS.md`, que es el único archivo que el CORE lee siempre. Vivir en un índice o en
un ADR no alcanza: **una regla que solo está en la documentación depende de que alguien la lea.**

### 4. El check reemplaza al verificador voluntario

`scripts/check-agent-skill-boundary.py` (con suite) verifica la frontera de forma **automática y
estructural**, y corre en el pre-commit:

1. Una skill del ciclo SDD en el árbol del CORE.
2. Una skill en dos árboles (un duplicado anula la separación).
3. El ciclo SDD incompleto en su rol (un movimiento a medias pierde etapas en silencio).

`dispatch-validation.sh` queda como herramienta de consulta manual; su semántica no cubría el caso
(el CORE nunca lo invocaba).

### 5. Verificar la delegación, no creerle al reporte

Cuando un rol devuelve trabajo, el CORE lo verifica en el repositorio real - `git status`, el diff,
y volver a correr el resultado. Un auto-reporte de subagente es un reporte, no un hecho
(`sdd-agent-loop`: medido 2026-09-28, dos tandas reportaron tablas de éxito sobre 43 y 9 artefactos;
el disco mostró 83 y 0).

### 6. El ruteo por etapa no es solo DEV

El CORE enruta cada etapa al rol que corresponde, y **el dueño natural de una etapa no siempre es
DEV**:

| Etapa | Rol | Por qué |
|---|---|---|
| Discovery / reconocimiento | **MIND** (con DEV) | El reconocimiento del ecosistema, el prior art y el estado de la memoria son su dominio (`knowledge-management`, `search-fusion`) |
| Investigación, research | **MIND** | Es su especialidad |
| Specs / ADRs / gobernanza | **CORE** | Gobierno del proyecto |
| Design / plan / build / review / qa / release | **DEV** | Es su ciclo |
| Infra, deploy, gateway | **OPS** | Su dominio |
| Contenido, marca, OSS | **STUDIO** | Su dominio |

El caso que originó esta nota: el discovery de `kanam-onwheels` lo hizo el CORE solo. **MIND debía
haber sido convocado** - el reconocimiento es su trabajo, y el CORE lo hizo sin ayuda.

---

## Consecuencias

### Positivas

- La regla pasa de declarada a **verificada**: un check automático con suite, en el pre-commit.
- El CORE pierde las herramientas del trabajo que no debe hacer. No es una restricción de conducta:
  es una capacidad que no tiene.
- El costo del bootstrap baja (9 skills menos en el árbol del CORE).
- La causa raíz fue mecánica y quedó cerrada mecánicamente, no con una instrucción más.

### Negativas / pendientes

- **El ciclo SDD queda solo en el árbol de DEV.** Si DEV no está disponible, el CORE no puede
  implementar: es exactamente el efecto buscado, pero hay que poder delegar para que funcione.
- **`hermes-*` ya no está en el catálogo del CORE**, así que el CORE no puede leer el detalle de una
  etapa. Conserva `sdd-agent-loop` como contrato de orquestación; si necesita el detalle, lo delega.
- **La identidad git no distingue agentes.** Todos commitean como `gonzoblasco`, así que un commit
  del CORE y uno de DEV son indistinguibles *a posteriori*. El enforcement es previo (qué ve cada
  agente), no forense. OpenClaw soporta `agents.entries.*.tools.github.gitAuthor`; queda como deuda
  declarada por si se quiere atribución en el historial.
- **El gate cubre el ciclo SDD, no toda skill de rol.** Mover otra skill al árbol del CORE se caza
  por la regla de duplicados si existe en su rol, pero una skill nueva nacida directamente en
  `skills/` no se detecta hasta que alguien la declare del ciclo. Se acepta: la lista explícita
  sigue valiendo aunque alguien borre las skills de su rol.

---

## Notas

- La asimetría que hace útil el check: **18 violaciones** al momento de escribirlo (9 skills en el
  árbol del CORE + 9 etapas faltantes en el de DEV). Antes: 0 checks. Después: 0 violaciones.
- El check se probó **en negativo** antes de confiar en él: se sembró `skills/hermes-builder/SKILL.md`,
  el hook abortó con exit 1, y se limpió. Un guard que nunca falla es indistinguible de un guard
  ausente.
- El propio check tuvo el fallo que persigue: su primera conexión usaba el disparador de
  `skills/|scripts/`, que **no matchea** `agents/<rol>/skills/` - justo donde se viola la frontera.
  Se detectó sembrando la violación y viendo que el hook salía 0. Es la lección de
  `rule-enforcement-audit` aplicada a un check nuevo: la conexión es parte del enforcement.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
