# Spec: patrones CSS de produccion en `frontend-ui-engineering` 🌿

**Creado:** 2026-10-05
**Origen:** skill #9 analizada - `Web Design` (wpank, ClawHub). Es CSS puro (no Tailwind),
aplicable a nuestro stack de CSS Modules. La mejor de la tanda desde la #5.
**Rol dueño:** kanam-dev
**Estado:** PROPUESTO - pendiente de delegacion

---

## 1. Motivacion

`Web Design` (wpank) trae patrones CSS de produccion que NO tenemos y que son aplicables
directo a CSS Modules (a diferencia de todas las skills de Tailwind de la tanda). Declara
su propio alcance ("esto es codigo, no teoria de diseño") y es la unica que estructura sus
citas de WCAG por criterio numerado.

Se toman SOLO los patrones tecnicos, anclados a nuestro stack. NO se importa la skill.

---

## 2. Alcance: que SI

Agregar a `agents/kanam-dev/skills/frontend-ui-engineering/SKILL.md` una seccion nueva:
**"Patrones CSS de produccion"**, con estos puntos:

### 2.1 Grid vs Flexbox: tabla de decision por contexto
Cada caso con su por que:
- Estructura de pagina -> CSS Grid con `grid-template-areas` (regiones nombradas).
- Barras de navegacion -> Flexbox (eje unico, `gap`).
- Card grids -> Grid `auto-fill`/`auto-fit` (responsive sin media queries).
- Centrado -> `place-items: center`.
- Sidebar + contenido -> `grid-template-columns: 250px 1fr`.
- **Overlaps -> Grid stacking (`grid-area: 1/1`) en vez de `position: absolute`.**

### 2.2 Grid stacking para superposicion
- Superponer elementos con `grid-area: 1/1` en vez de `position: absolute`.
- Razon: mas predecible, no saca el elemento del flujo, evita problemas de stacking context.

### 2.3 Tipografia y spacing fluidos con `clamp()`
- Tipografia fluida: `font-size: clamp(2rem, 1.5rem + 2.5vw, 3.5rem)`.
- Spacing fluido: `padding-block: clamp(2rem, 1rem + 4vw, 6rem)`.
- Grid intrinseco: `repeat(auto-fit, minmax(min(100%, 20rem), 1fr))`.

### 2.4 Container queries
- `@container` para responsividad a nivel componente (responde a su contenedor, no al viewport).

### 2.5 Surface layering en vez de sombras
- Profundidad por capas de luminosidad, no por drop shadows:
```css
--surface-0: hsl(220 15% 8%);  /* page */
--surface-1: hsl(220 15% 12%); /* card */
--surface-2: hsl(220 15% 16%); /* raised */
--surface-3: hsl(220 15% 20%); /* modal */
```
- Conectar con la regla de dark mode ya existente (`#0f0f0f`, nunca negro puro) y con
  "layered lightness, not inverted colors".

### 2.6 Motion por proposito (con diferencias por direccion)
- Tabla de duraciones por interaccion: hover 150ms ease-out; modal open 250ms ease-out;
  **modal close 200ms ease-in (mas rapido y con easing distinto)**; page transition 300ms
  ease-in-out; micro-feedback 100ms ease-out.
- **Stagger reveal:** `animation-delay` incremental (50-80ms por item).
- Conectar con la tabla ya existente en "Reglas de calidad visual"; NO duplicar easing ni
  duraciones canonicas, solo agregar lo que falta (el cierre asimetrico y el stagger).

### 2.7 `gap` en containers, no margenes en hijos
- Usar `gap` en Grid/Flexbox en vez de `margin` en los hijos.
- Razon: elimina bugs de margin-collapse y simplifica el responsive.

### 2.8 Arquitectura de tokens en 3 capas
- `primitive` (valores crudos) -> `semantic` (proposito) -> `component` (especifico).
- Permite theme switching remapeando la capa 2 sin tocar componentes.
- Anclar a los tokens propios (`--primary`, `--muted`, `--border`).

### 2.9 Citas de WCAG por criterio
- Cuando se documente una regla de a11y, citar el criterio numerico (ej. 2.4.7 focus
  visible, 2.5.8 touch target, 2.3.3 motion). Esto eleva el rigor - ya lo hacemos en
  parte, formalizarlo.

---

## 3. Fuera de alcance: que NO

- **NO** importar ni instalar la skill `Web Design` (ni `npx clawhub install`).
- **NO** copiar el catalogo de pares tipograficos concretos (Playfair+Source Sans, Syne+
  Outfit, etc.): es tendencia, no criterio. Si se citan, son ejemplos.
- **NO** duplicar lo ya existente: WCAG general, empty/error states, skeletons, anti-patrones
  "look IA", escala tipografica 8px, easing/duraciones canonicas, neutros con tinte, dark
  mode `#0f0f0f`, 65ch/1280px. Todo eso ya esta.
- **NO** adoptar Tailwind ni nada de la skill hermana (tailwind-design-system, #7).
- **NO** mencionar la fuente externa (`wpank`, `web-design`) en el cuerpo de la skill.
- **NO** editar ningun otro archivo fuera del listado.

---

## 4. Criterios de aceptacion (verificacion real)

1. Seccion "Patrones CSS de produccion" en `frontend-ui-engineering/SKILL.md`.
2. Contiene los 9 puntos de la seccion 2.
3. Sin duplicacion: `grep` de las reglas ya existentes (easing canonico, 65ch, #0f0f0f,
   neutros con tinte) debe mostrar que la seccion nueva NO las repite - solo las referencia.
4. `grep -in "wpank\|clawhub\|npx"` = 0 lineas.
5. `python3 scripts/check-agent-skill-boundary.py` pasa.
6. Frontmatter intacto. Diff minimo (una seccion nueva).
7. `check_em_dash.py` sobre la skill = sin guiones largos (ADR-082).

---

## 5. Evidencia esperada (Core verifica, ADR-078)

- `git diff` de la skill (solo el hunk nuevo).
- Greps de los criterios 3 y 4.
- `git status` mostrando solo los archivos esperados.
- Salida del check de frontera + em dash.

---

## 6. Delegacion

- **Rol:** `kanam-dev` (dueño de la skill). Core gobierna, DEV implementa (ADR-083).
- **Modelo:** `glm-5.3-flash:cloud`.
- **Contexto:** isolated; taskName y write-scope explicitos.
