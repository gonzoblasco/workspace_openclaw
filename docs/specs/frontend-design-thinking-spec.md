# Spec: Design Thinking Before Code (ampliación de `frontend-ui-engineering`) 🌿

**Creado:** 2026-10-05
**Origen:** análisis de la skill externa `SuperDesign` (mpociot, ClawHub) traída por Gonzo.
**Rol dueño:** kanam-dev
**Estado:** PROPuesto - pendiente de delegación

---

## 1. Contexto y motivación

`frontend-ui-engineering` (kanam-dev) es una skill de **implementación**: asume que el
diseño ya existe y enseña a construirlo accesible, responsive y con tokens. Lo que **no**
cubre es el paso anterior: *cómo se piensa un diseño bueno antes de que exista el código.*

Ese es el hueco que la skill externa `SuperDesign` toca (con contenido flojo: catálogo de
temas efímero, dependencias prescindibles como Flowbite/Tailwind-CDN). Rescatamos **solo
los patrones portables**, no la skill ni sus dependencias.

**Hilo de fondo:** 2026-09-14, Gonzo pausó kanam-lab para abrir el frente de "entrenarme
en el arte del diseño UI/UX" (que UI/UX/estética importen SIEMPRE). Sigue abierto.

---

## 2. Alcance (qué SÍ)

Agregar a `agents/kanam-dev/skills/frontend-ui-engineering/SKILL.md` una sección nueva:
**"Design Thinking Before Code"** con tres artefactos de planificación:

### 2.1 Wireframe ASCII como primer artefacto obligatorio
- Para toda UI **nueva** (no para cambios menores), el primer entregable es un boceto
  ASCII del layout: estructura de bloques, jerarquía, ubicación de CTA.
- Regla: no se escribe código de layout sin el wireframe. Es el análogo de "spec antes
  de código" aplicado al diseño.
- Debe integrarse con `openspec-pattern` (contrato de intención) y el ciclo de discovery.

### 2.2 Micro-sintaxis de animación (planificar el movimiento antes de codearlo)
- Notación compacta para *pensar* las transiciones antes de implementarlas. Ejemplo:
  - `hover: 200ms [Y0→-2, shadow↗]`
  - `fadeIn: 400ms ease-out [Y+20→0, α0→1]`
- Duraciones canónicas: entry 300-500ms ease-out · hover 150-200ms · press 100-150ms.
- **Regla dura nuestra (no de SuperDesign):** todo motion respeta `prefers-reduced-motion`.
  La micro-sintaxis es para *planificar*; nunca reemplaza la verificación de accesibilidad.

### 2.3 El orden layout → tema → animación → código
- El diseño se piensa en cuatro fases antes de implementar. Encuadra con
  `incremental-implementation` (slices verticales), pero en el eje de diseño.

---

## 3. Fuera de alcance (qué NO)

- **No** importar la skill `SuperDesign` ni instalarla como unidad adoptable.
- **No** adoptar **Flowbite** ni ninguna component library nueva. Si hace falta evaluar
  una, va por ADR de stack (regla 2026-09-14: el precedente no es un motivo).
- **No** adoptar **Tailwind por CDN** (`cdn.tailwindcss.com`) ni unpkg fuera de prototipos.
- **No** copiar el catálogo de temas (Vercel/Linear, Neo-Brutalism, Glassmorphism): es
  tendencia perecedera y no es criterio.
- **No** duplicar lo que la skill ya tiene (WCAG 2.1 AA, empty/error states, skeletons,
  anti-patrones "look IA", checklist de verificación): ya está cubierto y mejor.

---

## 4. Anclaje al stack real (obligatorio)

Toda la sección debe referenciar nuestro stack, no el de la skill externa:
- Tokens semánticos propios (`--primary`, `--muted`, `--border`), no Flowbite.
- **Lucide** como iconografía (ya es regla del workspace); nunca emojis como iconografía.
- Cerrar el loop con `a11y-at-validation` y con el TODO abierto de **Radix/shadcn**
  (que sigue sin ADR de adopción - no resolverlo acá, solo enlazarlo).

---

## 5. Criterios de aceptación (verificación real, no auto-reporte)

1. La sección nueva existe en `frontend-ui-engineering/SKILL.md` y no rompe el frontmatter
   (`name`/`description`).
2. Los tres artefactos (wireframe, micro-sintaxis, orden de fases) están presentes y
   anclados a nuestro stack; cero menciones a Flowbite/CDN/unpkg.
3. Consistencia: no contradice `a11y-at-validation`, `incremental-implementation` ni
   `openspec-pattern`. Verificar con `grep` cruzado.
4. Si el repo tiene check de skills (`scripts/check-agent-skill-boundary.py`), pasa:
   la skill sigue en el árbol de kanam-dev, no del Core.
5. Diff mínimo y atómico: una sección, sin reescritura del resto del archivo.

---

## 6. Evidencia esperada (para que el Core verifique)

- `git diff` de la skill.
- `grep -i "flowbite\|cdn.tailwindcss\|unpkg"` sobre la skill = 0 líneas.
- Salida del check de frontera de skills (si aplica).

> **Nota (ADR-078):** la salida del sub-agente es un auto-reporte, no un hecho. El Core
> verifica en el repositorio real antes de dar el trabajo por cerrado.

---

## 7. Delegación

- **Rol:** `kanam-dev` (dueño de `frontend-ui-engineering`). Frontera de roles: el Core
  gobierna (este spec), DEV implementa (ADR-083).
- **Modelo:** `glm-5.3-flash:cloud` (default del rol).
- **Contexto:** isolated; el taskName y el write-scope van explícitos en el spawn.
