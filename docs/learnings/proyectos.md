# Learnings - proyectos

> Generado desde memory/memory.db (tabla learnings). Fuente de verdad: la DB.

## 2026-08-06 - Skill consolidation: google/addy skills patterns + prune

**Context:** Adopted `addyosmani/agent-skills` (24 skills) as the engineering baseline, consolidating the workspace from 96 to 60 active skills. The old `google-skills-adoption-plan.md` and `kanam-product-pipeline.md` (referencing ~33 now-deleted skills) were removed.

**Lesson - what Addy/Google skills got right (now our baseline):**
- **Frontmatter YAML estandarizado** with `name` + `description` in the "Use when..." trigger form. Consistent triggers make skill discovery reliable.
- **Anti-rationalization tables**: each skill lists common excuses agents use to skip steps ("I'll add tests later") with documented rebuttals. This is the strongest guard against agents cutting corners.
- **Verification is non-negotiable**: every skill ends with evidence requirements (tests passing, build output, runtime data). "Seems right" is never sufficient.
- **Progressive disclosure**: `SKILL.md` is the entry point; supporting `references/*.md` load only when needed, keeping token usage minimal.
- **Process, not prose**: skills are workflows agents follow (steps + checkpoints + exit criteria), not reference docs they read.

**Lesson - pruning discipline:**
- Having 96 overlapping skills (4 UI, 3 review, 3 debug, etc.) fragments context and burns tokens. Consolidate to orthogonal skills where each covers a full capability.
- Keep infrastructure/life skills that are unique (adhd, apple-photos, supabase-assistant, sql-insight) even when pruning dev skills - they're not duplicates of an engineering baseline.
- Archived/pruned content is recoverable from git history - deleting is safe as long as the consolidation mapping is documented in the commit message and SKILLS-INDEX.
- When removing a process doc, fold its durable lessons into LEARNINGS.md first so the knowledge outlives the file.

**Tags:** Skill consolidation: google/addy skills patterns + prune

---

## 2026-08-06 (cierre) - Consolidación no-dev + fusión de skills + eliminación de proyecto

**Context:** Segunda ola de consolidación. Tras reducir 96→60 skills (ingeniería), se evaluaron las 29 skills no-dev (vida/creatividad/infraestructura) y se decidió qué hacer.

**Lesson - las skills no-dev NO se solapan como las de ingeniería:**
- Las 24 skills de ingeniería de Addy tenían duplicación real (5 fusiones absorbieron 20+ skills). Las no-dev son **ortogonales** - ninguna referencia a otra, ninguna es referenciada por otra.
- Por eso la consolidación no-dev NO es por duplicación, sino por **decisión de uso**. La regla "una skill pública = una decisión de workflow distinta" no aplica igual a un catálogo heterogéneo de herramientas de vida.
- Conclusión: no fusionar por número. La única fusión obvia fue `adhd-daily-planner` (que ya se autodeclaraba "extensión de adhd-assistant"). El resto de las 4 candidatas (content-serializer, curriculum-builder, brand-name-forge, checkmate) Gonzo decidió mantenerlas como están.

**Lesson - fusionar una skill = actualizar en TODAS las ubicaciones:**
- Una skill vive en 3 lugares: `skills/`, `.github/skills/` (mirror) y `projects/kanam-skills/skills/` (repo público). Al fusionar hay que propagar a los 3 + README + `web/generate.js` del repo + regenerar la web.
- El generador de web estático **no limpia HTML huérfanos** (solo escribe, no borra). Al eliminar una skill hay que borrar `web/public/skills/<name>.html` a mano además de regenerar.
- La web se regenera en CI desde `skills/`, así que `web/public/` está en `.gitignore` - los cambios locales ahí no se commitean.

**Lesson - eliminar un proyecto con repo remoto:**
- `gh repo delete` requiere el scope `delete_repo` en el token. Si no lo tenés, Gonzo lo borra a mano (opción B) - es más simple que pedir permiso de scope.
- Al eliminar un proyecto, preservar el `.knowledge/` (BRIEF + ROADMAP) moviéndolo a `projects/_archived/<slug>/` con un `ARCHIVED.md`. Git lo detecta como rename si movés los archivos, conservando el historial.
- Usar `trash` en vez de `rm -rf` para la carpeta local - recuperable beats gone forever.

**Self-reflection:**
- CONTEXT: consolidación de skills + fusión + eliminación de proyecto (multi-step, cambios estructurales)
- REFLECTION: el criterio correcto para consolidar no es el número sino la existencia de duplicación real o decisión de uso. En ingeniería había duplicación; en no-dev no.
- LESSON: distinguir "muchas skills" (problema de descubribilidad, resuelve con capas/entradas) de "skills duplicadas" (problema de competencia, resuelve con fusión). No son lo mismo.
- BIASES DETECTED: ninguno flagrante; evité el sesgo de "menos = mejor" sin evidencia de duplicación.

**Tags:** Consolidación no-dev + fusión de skills + eliminación de proyecto

---

## 2026-08-10 (cierre 2) - Narrativa del pipeline + sanitización de skills públicas

**Context:** Tras reconstruir oss-contribution y sanitizar kanam-skills, Gonzo corrigió la narrativa del pipeline del workspace: no era "24 skills de Addy Osmani" sino su propio set organizado en ese esquema, combinado con skills pre-existentes y skills 100% propias (accesibilidad).

**Lesson - la atribución incorrecta hiere más que el código:**
- El pipeline decía "Skills del pipeline: 24 de Addy Osmani + core OpenClaw + oss-contribution". Eso era falso en dos sentidos: (1) el set no es de Addy, es de Gonzo organizado con ese esquema; (2) ignoraba las skills 100% propias (accesibilidad, infraestructura OpenClaw, vida).
- Cuando se describe el origen de un sistema, la precisión de la narrativa importa tanto como la funcionalidad. "Inspirado en / organizado como X" ≠ "es X". Corregir la atribución cuando sea incorrecta, sin esperar a que el dueño la reclame.

**Lesson - skills públicas vs workspace (regla establecida en AGENTS.md):**
- El workspace (privado) mantiene las referencias personales (setup de Gonzo). kanam-skills (público) se sanitiza (sin referencias personales).
- Dos versiones de cada skill: una con contexto (workspace), una limpia (público). Al copiar, sanitizar en el camino.
- Excepción legítima: identidad de instalación del repo (gonzoblasco/kanam-skills en README/docs/web) y LICENSE.

**Self-reflection:**
- CONTEXT: corrección de narrativa del pipeline + regla de sanitización
- REFLECTION: cometí el error de describir el set como "de Addy Osmani" cuando es propio organizado con ese esquema, y de no considerar las skills 100% propias. Gonzo lo notó ("solo hiere mi orgullo").
- LESSON: la atribución y la narrativa del origen son parte del deliverable. Verificar que la descripción del origen sea precisa antes de commitearla.
- BIASES DETECTED: anchoring (me anclé en la narrativa previa de "24 de Addy" de la consolidación sin cuestionarla).

**Tags:** Narrativa del pipeline + sanitización de skills públicas

---

## 2026-08-10 (cierre 3) - Tormenta de ideas: convertir una idea en negocio

**Context:** Sesión de brainstorming sobre "IA como Servicio" para terceros no-técnicos. Evolucionó de "vender un workspace" a "SaaS con Cloud + Local + soporte como embudo de conversión". Se identificaron las primeras cuentas reales: los hermanos de Gonzo (hermana = concesionario Jeep/RAM, hermano = motos).

**Lesson - la entrevista de descubrimiento antecede al producto:**
- No crear artifacts de proyectos hasta tener el insumo real (la charla con el cliente/contacto). Los artifacts de la idea madre y PIBÄ se crearon porque tenían decisiones tomadas. Los proyectos Cloud NO se crearon aún porque falta la entrevista con la hermana que defina el dolor real y el workflow bandera.
- Escribir sobre humo (suposiciones sin validar) genera artifacts que después se reescriben.

**Lesson - acceso en caliente > nicho teórico:**
- El primer cliente casi nunca sale de un mercado genérico, sale de la red. Los hermanos de Gonzo son acceso en caliente (confianza familiar) = laboratorio gratuito + piloto + red de referidos.
- Estrategia: hermana (contacto cercano) = laboratorio/prototipo; hermano (menos cercano pero con red de locales) = regalo → referidos → clientes pagos. Un acceso cubre "aprender", el otro "escalar".

**Lesson - vender el Cloud, no el sistema a medida:**
- PIBÄ: el dolor del stock (sistema de pedidos) queda corto - es ERP a medida, no escalable, posiciona mal. Se reencuadró a "IA que maneja el negocio completo". No vender un sistema a medida, vender un servicio que resuelve dolores.

**Self-reflection:**
- CONTEXT: sesión de brainstorming multi-hilo (modelo de negocio, 2 candidatos reales, estrategia de acceso)
- REFLECTION: la sesión fue productiva y el enfoque de "hablar antes de escribir" (que pidió Gonzo) funcionó - se destiló el modelo conversando sin escribir prematuremente. Bien registrar cada decisión periódicamente, no al final.
- LESSON: en brainstorming de negocio, separar "definición de decisiones" (se documenta) de "exploración sin validar" (no se documenta como artifact). El acceso en caliente (familia) es el mayor activo para el primer cliente.
- BIASES DETECTED: none (el flujo conversacional guiado evitó confirmación prematura; Gonzo frenó la creación de artifacts hasta tener insumo real).

**Tags:** Tormenta de ideas: convertir una idea en negocio

---

## 2026-08-11 - Estructura de estudio gamificada: nivel → subnivel → topic (3 capas de artifacts)

**Context:** Gonzo quiere estudiar system design (para entrevista de Greenhouse) de forma teórico/práctica, con gamificación tipo bootcamp. Al diseñar el plan, pidió explícitamente dividir cada nivel en subniveles y topics, y documentar el aprendizaje en artifacts.

**Patrón validado (el que vale):**
- **Nivel → Subnivel → Topic** - cada nivel se divide en subniveles (bloques grandes) y cada subnivel en topics (piezas chicas). Cada topic es una unidad completa y verificable sola.
- **Documentar en 3 capas de artifacts, no un documento gigante:** plan maestro (estático, se actualiza poco) + artifact por nivel (crece con el aprendizaje) + registro de progreso (se actualiza después de cada topic, cambio chiquito). Escalabilidad de edición + repaso dirigido.
- **Gamificar:** XP por topic, badges por nivel, streak, jefe final (evaluación completa).

**Self-reflection:** el patrón ya existía implícito (bootcamp de AI engineering), pero la estructura de 3 capas de artifacts fue un refinamiento explícito de Gonzo que lo hizo reusable. Se formalizó como skill `learning-tracker` para que cualquier estudio futuro (no solo este curso) use la misma documentación.

**Lección pedagógica (corrección de Gonzo):** no pedir respuestas de conceptos que todavía no se enseñaron - primero explicar la teoría, después verificar. Verificar sin haber enseñado genera frustración ("clueless").

**Tags:** Estructura de estudio gamificada: nivel → subnivel → topic (3 capas de artifacts)

---

## 2026-08-11 - SoporteML v3: estructura de doble git (leer skills antes de tocar organización)

**Context:** Sesión de construcción de SoporteML v3. Al crear el repo del proyecto, me enredé con submodules y moví el `.knowledge/` al repo del proyecto, cuando Gonzo me había dicho que los ADRs van en `docs/adr/` del proyecto y que el sistema es de doble git. Gonzo me corrigió: "estuviste revisando eso pero no leíste mis skills para identificar cómo ordeno las cosas".

**Lesson - leer las skills de estructura ANTES de tocar la organización de proyectos:**
- El sistema de doble git de Gonzo (AGENTS.md §211 + práctica real):
  - **Workspace git:** capta workspace + `.knowledge/` del proyecto + README.
  - **Repo del proyecto:** capta todo el contenido (código + docs/adr) + README. Independiente, NO submodule.
  - `.knowledge/` va en el workspace, NO en el repo del proyecto.
- Me enredé con submodules (quedamos, kanam-solitaires son submodules) sin darme cuenta de que soporteml-v3 es un proyecto NO-submodule (como daily-ink, ensulugar) donde el workspace trackea `.knowledge/` directamente.
- LESSON: antes de reorganizar la estructura de un proyecto, leer AGENTS.md §211 + la skill de git-workflow + verificar cómo lo hacen 2-3 proyectos existentes. No asumir el patrón por un solo ejemplo.

**Lesson - el `.gitignore` del proyecto con `.knowledge/` pisa la negación del raíz:**
- El `.gitignore` del proyecto tiene `.knowledge/` (para que el repo del proyecto no lo trackee). Pero las reglas de `.gitignore` de subdirectorios ganan sobre las del raíz, así que la negación `!/projects/<slug>/.knowledge/**` del raíz no funciona.
- Solución: trackear `.knowledge/` en el workspace con `git add -f` (force). Una vez trackeados, el `.gitignore` del proyecto ya no los afecta.

**Lesson - repo anidado bloquea el trackeo del workspace:**
- Si el proyecto tiene `.git` propio (repo anidado), git lo trata como gitlink y no trackea su contenido en el workspace, ni siquiera con `git add -f`.
- Solución: mover temporalmente el `.git` del proyecto, `git add -f` del `.knowledge/` en el workspace, y restaurar el `.git`.

**Self-reflection:**
- CONTEXT: creación de repo + estructura de doble git
- REFLECTION: me fui por las ramas con submodules sin verificar el sistema real de Gonzo. La corrección fue oportuna pero costó varias iteraciones de git.
- LESSON: la organización de proyectos es una decisión estructural - verificar el sistema documentado (AGENTS.md, skills) y la práctica real de proyectos existentes ANTES de tocar nada.
- BIASES DETECTED: anchoring (me anclé en el patrón de submodules de quedamos/kanam-solitaires sin verificar que soporteml-v3 es NO-submodule).

**Tags:** SoporteML v3: estructura de doble git (leer skills antes de tocar organización)

---

