# Spec: skill nueva `design-direction` 🌿

**Creado:** 2026-10-05
**Origen:** analisis de 3 skills externas de diseno traidas por Gonzo (ClawHub):
`SuperDesign` (mpociot), `Frontend Design` (michaelmonetized), `UI/UX Design Guide` (itsjustdri).
**Rol dueño:** kanam-dev
**Estado:** PROPUESTO - pendiente de delegacion

---

## 1. Motivacion

Las tres skills externas comparten un hallazgo: **ninguna resuelve el problema que
atacan, pero todas apuntan al mismo hueco real.**

- `SuperDesign`: aporta el ORDEN (layout -> tema -> animacion -> codigo). Vicio: catalogo
  de temas perecedero + dependencias (Flowbite, Tailwind-CDN).
- `Frontend Design`: aporta el MARCO (4 preguntas + intencionalidad estetica). Vicio:
  contradiccion interna ("cohesive" vs "no design should be the same") + cero a11y.
- `UI/UX Design Guide`: aporta NUMEROS concretos (escala tipografica, grid, GPU). Vicio:
  es un manual de Tailwind/Shadcn disfrazado de guia de diseno.

**Ninguna de las tres tiene verificacion real.** Todas dicen que hacer; ninguna da un gate.

**Lo que ya tenemos:** `frontend-ui-engineering` cubre IMPLEMENTACION (WCAG, estados,
tokens, verificacion) y lo hace mejor que las tres. Lo que NO cubre es el paso anterior:
**decidir la direccion de diseno antes de implementar.**

Este es el hueco. Y es el hilo abierto del 2026-09-14 ("entrenarme en el arte del diseno").

---

## 2. Alcance: que SI (crear skill nueva)

Crear `agents/kanam-dev/skills/design-direction/SKILL.md` - skill NUEVA, no una seccion de
`frontend-ui-engineering`. Tiene identidad propia: es direccion de arte, no implementacion.

### Contenido obligatorio

**a) El marco de las 4 preguntas (antes de codear)**
1. **Proposito:** que problema resuelve la interfaz? quien la usa?
2. **Tono:** elegir una direccion conceptual (minimal refinado, maximalista bold, editorial,
   organic, industrial, etc.). Regla: la clave es la INTENCIONALIDAD, no la intensidad.
   Un minimalismo refinado y un maximalismo bold son igualmente validos.
3. **Restricciones:** framework, performance, accesibilidad (enganchar con a11y-at-validation).
4. **Diferenciacion:** cual es la UNICA cosa que alguien va a recordar?

**b) La distincion de contexto (pieza clave que resuelve el conflicto de fuentes)**
- **Herramienta funcional** (dashboard, form, tabla densa, admin): la neutralidad ES la
  decision. Fuentes de sistema/Inter correctas. La legibilidad y la densidad mandan.
- **Pieza memorable** (landing, portfolio, pagina de marca): la neutralidad es pereza.
  Fuentes con caracter, display + body.
- Regla: primero preguntar QUE es, despues elegir tipografia. Nunca al reves.

**c) El orden de las 4 fases de pensamiento**
layout -> tema -> animacion -> codigo. Punto de entrada del pensamiento de diseno.
Enlazar a `incremental-implementation` (el como) y a `frontend-ui-engineering` (la ejecucion).

**d) La regla de intencionalidad**
"La ausencia de look malo no es un look bueno." Evitar el "look IA" (purpura, gradientes,
cards de stock, hero generico) NO alcanza: hay que COMPROMETERSE con una direccion.

### Anclaje al stack real (obligatorio)
- Tokens semanticos propios (`--primary`, `--muted`, `--border`).
- **Lucide** para iconografia (regla del workspace; nunca emojis como iconografia).
- **CSS Modules** como via de estilado (NO Tailwind, NO Shadcn).
- Loop cerrado con `a11y-at-validation`.

---

## 3. Fuera de alcance: que NO

- **NO** importar ni instalar ninguna de las 3 skills externas.
- **NO** adoptar **Shadcn/ui** ni **Radix**: el TODO de Radix/shadcn sigue SIN ADR. Esta
  skill NO decide ese punto; solo lo enlaza. Decidirlo requiere su propio ADR.
- **NO** adoptar **Tailwind** ni utilidades de Tailwind como filosofia de estilado.
- **NO** Tailwind por CDN (`cdn.tailwindcss.com`), **NO** unpkg, **NO** Flowbite.
- **NO** copiar catalogos de temas/paletas hardcodeadas (Vercel/Linear, Neo-Brutalism,
  Glassmorphism): tendencia perecedera, no criterio.
- **NO** duplicar lo que ya hace `frontend-ui-engineering` (WCAG detallado, empty/error
  states, skeletons, checklist de verificacion, anti-patrones "look IA"). Aca solo se
  hace la DIRECCION; la IMPLEMENTACION vive en la otra skill.
- **NO** mencionar a Claude ni a ningun modelo como destinatario de la skill.

---

## 4. Ajuste complementario (menor) en `frontend-ui-engineering`

Agregar UNA linea de contexto al inicio de la seccion "Design Thinking Before Code":
> "Esta seccion asume que ya existe una direccion estetica. Para UI nueva sin direccion
> definida, ver la skill `design-direction`."

Es un ajuste de una linea. NO reescribir la skill.

---

## 5. Registro obligatorio (no olvidar)

1. **`SKILLS-INDEX.md`:** agregar `design-direction` a la seccion 3.2 (kanam-dev, 34 -> 35),
   en el grupo "Build" o "Define" (a criterio de kanam-dev, justificar en el commit).
2. **Contador:** actualizar el conteo de kanam-dev en la linea 24.
3. **`CHANGELOG.md` del workspace:** registrar la skill nueva (cambio estructural).
4. **NO** crear `.eval.yaml` todavia salvo que kanam-dev lo considere necesario.

---

## 6. Criterios de aceptacion (verificacion real, no auto-reporte)

1. `agents/kanam-dev/skills/design-direction/SKILL.md` existe con frontmatter valido
   (`name: design-direction`, `description` con trigger claro).
2. Contiene los 4 bloques obligatorios (a-d) y el anclaje al stack.
3. `grep -in "flowbite\|cdn.tailwindcss\|unpkg\|shadcn\|tailwind"` sobre la skill nueva =
   0 lineas (probar que no se filtro el stack de las skills externas).

   > Excepcion: si la skill necesita MENCIONAR Shadcn/Tailwind para decir "no los usamos",
   > que sea en una linea explicita de rechazo. Probar que no hay instrucciones de uso.
4. `grep -in "shadcn\|tailwind"` NO aparece como recomendacion de adopcion en ningun lado.
5. `python3 scripts/check-agent-skill-boundary.py` pasa (la skill vive en kanam-dev, no en
   el Core).
6. `python3 scripts/check-skill-index-integrity.py` (o el check que valide SKILLS-INDEX)
   pasa: el indice lista la skill nueva y no hay refs rotas.
7. El ajuste de una linea en `frontend-ui-engineering` esta presente y no rompe nada.
8. Diff atomico: skill nueva + 1 linea en la existente + indice + CHANGELOG. Nada mas.

---

## 7. Evidencia esperada (para que el Core verifique)

- `git status` mostrando solo los archivos esperados.
- `ls agents/kanam-dev/skills/design-direction/` con el SKILL.md.
- Las salidas de grep del criterio 3 y 4.
- Salida del check de frontera + check de indice.
- Diff del ajuste de una linea en `frontend-ui-engineering`.

---

## 8. Delegacion

- **Rol:** `kanam-dev` (dueño de las skills de ingenieria). El Core gobierna (este spec),
  DEV implementa (ADR-083).
- **Modelo:** `glm-5.3-flash:cloud` (default del rol).
- **Contexto:** isolated; taskName y write-scope explicitos.

## 9. Follow-ups que NO se resuelven aca (dejar registrados)

- **Radix/shadcn sin ADR de adopcion:** las 3 skills lo empujaron al centro de la mesa.
  Requiere su propio ADR, no este spec.
- **WCAG 2.1 vs 2.2:** `UI/UX Design Guide` menciona 2.2 (agrega foco no oscurecido,
  tamanos de target, arrastre alternativo). Evaluar si vale subir de version. Va aparte.
- **`transform`/`opacity` only para animaciones:** regla tecnica portable (performance/GPU).
  Considerar agregarla a `frontend-ui-engineering` o a `performance-optimization`.
