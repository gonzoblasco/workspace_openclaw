# Learnings - metodologia

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 2026-08-01 - Documentation at milestone end is expensive

**Context:** Created README, ROADMAP, DEFINITION, STATUS, CHANGELOG, HANDOFF, and `docs/` only after v1.0.0 was feature-complete.

**Lesson:** Start documentation in parallel with development. Each significant decision or feature should incrementally update the relevant doc file.

**Tags:** Documentation at milestone end is expensive

---

## Godot: aprender juntos, no automatizar (2026-08-02)

Gonzo quiere aprender Godot paso a paso. No construir juegos de un prompt. El skill `godot-mcp` se reescribió de "build-everything" a "learn-together". Registro del viaje en `projects/godot-journey/.knowledge/BRIEF.md`.

**Tags:** Godot: aprender juntos, no automatizar (2026-08-02)

---

## Skill Workshop stale cuando SKILL.md ya existe (2026-08-02)

Si se crea el archivo físico antes de aprobar el workshop, la propuesta queda stale y no se puede aplicar. Workaround: editar el SKILL.md directamente y commitear. El workshop es para skills nuevas que aún no existen en disco.

**Tags:** Skill Workshop stale cuando SKILL.md ya existe (2026-08-02)

---

## MCP server `editor_instantiate_scene` rompe .tscn (2026-08-02)

La tool `editor_instantiate_scene` del Godot MCP corrompe el formato de main.tscn (ids con triple comilla, nodos perdidos). Preferir edición manual de .tscn o usar `add_node` + `attach_script` por separado.

**Tags:** MCP server `editor_instantiate_scene` rompe .tscn (2026-08-02)

---

## Export templates de Godot 4.7.1 (2026-08-02)

El mirror tuxfamily.org falló por timeout. Probar GitHub releases o mirror alternativo cuando se retome el export.

**Tags:** Export templates de Godot 4.7.1 (2026-08-02)

---

## Sport Cars: validación visual obligatoria para sitios de marca (2026-08-02)

El build pasando no garantiza que el sitio se vea profesional. Para proyectos con identidad visual, la validación con screenshots + evaluación crítica debe ser parte del cierre de cada iteración. Issues como contraste bajo, colores inconsistentes o títulos engañosos no los detecta Biome.

**Tags:** Sport Cars: validación visual obligatoria para sitios de marca (2026-08-02)

---

## Feature flags portable: no hardcodear en UI (2026-08-02)

El primer flag (`showPrices`) se implementó con provider client-side + localStorage + componente `PriceDisplay`. El panel de flags solo se renderiza en desarrollo. El siguiente paso es extraerlo a `@workflow-kit/feature-flags` para reuso.

**Tags:** Feature flags portable: no hardcodear en UI (2026-08-02)

---

## No commitear mockups intermedios (2026-08-02)

Los mockups y screenshots de iteración (v2, v3, etc.) son ruido en el repo del proyecto. Solo conservar la evidencia final (home/catálogo) en el commit de release; los intermedios van al daily note o a un artifact.

**Tags:** No commitear mockups intermedios (2026-08-02)

---

## npm 404 en publish scoped no es problema de scope (2026-08-04)

El 404 `PUT .../@scope%2fpackage` al publicar NO significa que el scope esté mal. Primero verificar `npm whoami` - si da 401, el fix es `npm login`, no tocar el scope. El scope `@usuario/` se resuelve solo cuando coincide con el username logueado. (Pasó con `@gonzoblasco/create-stack`.)

**Tags:** npm 404 en publish scoped no es problema de scope (2026-08-04)

---

## npm login usa browser OTP flow (2026-08-04)

El login de npm ahora abre browser (OTP), no acepta token en consola. Los tokens que saltan 2FA se están restringiendo - para CI a futuro usar tokens con `mfa=publish` o `automation`.

**Tags:** npm login usa browser OTP flow (2026-08-04)

---

## AI Engineering Bootcamp - COMPLETO (2026-08-03)

- 10/10 niveles completados. N1-N4 fundamentos, N5-N6 calidad/seguridad, N7-N8 arquitectura/producción, N9 estándares/dashboard, N10 sistema completo (capstone).
- N8-N10 son convergentes: reusan el sistema del N7 (vive dentro de `projects/level-07-microservices/`).
- El N10 junta todo: auth + users + orders + notifications + gateway + CI/CD + dashboard + cloud. Probado: gateway enruta, health agregado ok, register/login/orders funcionan, 401 en credenciales malas.
- **El nivel 7 es el núcleo físico de los niveles 7-10**: N8, N9 y N10 extienden el mismo folder (ADR-001). El nombre del folder confunde - el README lo documenta como "Niveles 7-10" con tabla de acumulación y diagrama de arquitectura.

**Tags:** COMPLETO (2026-08-03)

---

## Patrón por inercia vs contexto cambiado (2026-08-03)

Cuando un patrón se repite muchas veces (7+ niveles de bootcamp con carpeta nueva), el riesgo no es equivocarse en el patrón - es aplicarlo por inercia cuando el contexto ya cambió. La señal de alerta no es "¿lo sé hacer?" sino "¿es este caso realmente igual a los que ya resolví?". Pasó en el Nivel 8 del bootcamp (convergente, no lineal - transformaba el N7, no creaba carpeta nueva). ADR: `projects/ai-engineering-bootcamp/.knowledge/ADR-001-niveles-convergentes.md`.

**Tags:** Patrón por inercia vs contexto cambiado (2026-08-03)

---

## Reflexión del curso (meta-aprendizaje, 2026-08-03)

- El patrón "detectores locales + validación cruzada / IA contextual" apareció 5 veces (N3, N5, N6, N8, N9) → formalizado como skill `pipeline-detector`.
- Formato nivel de bootcamp (teoría + práctica + LinkedIn + self-review) es un template de skill reusable.
- Los proyectos resueltos son el "contrato" del curso - demuestran que el nivel es posible, no son la respuesta.
- Falta un mecanismo de verificación automática al final de cada nivel (tests contra el proyecto del alumno).

**Tags:** Reflexión del curso (meta-aprendizaje, 2026-08-03)

---

## Seleccion de libros tecnicos para preparar un puesto

Para comprar libros tecnicos para preparar una entrevista o puesto, buscar editoriales serias (Packt, O'Reilly) y filtrar el ruido de autoayuda que domina Amazon ('make money with AI', autores fantasma, series de ingreso pasivo). El valor esta en arquitectura e ingenieria de produccion, no en guias de principiante. Caso real: de 50 resultados 'openclaw' en Amazon solo 1 era tecnico serio (OpenClaw AI in Production de Ken Huang, Packt). Nota: 3 de 4 titulos 'openclaw' en PacktPub eran videos, no libros.

**Tags:** libros,amazon,packt,entrevista,aiaa

---

