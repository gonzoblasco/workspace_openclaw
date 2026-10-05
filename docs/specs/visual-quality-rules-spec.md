# Spec: reglas de calidad visual en `frontend-ui-engineering` 🌿

**Creado:** 2026-10-05
**Origen:** quinta skill analizada - `Frontend Design Pro` (antonia-sz, ClawHub, inspirada
en `pbakaus/impeccable`). Sintesis de la tanda completa de 5 skills de diseño.
**Rol dueño:** kanam-dev
**Estado:** PROPUESTO - pendiente de delegacion

---

## 1. Motivacion

De las 5 skills externas analizadas hoy, `Frontend Design Pro` es la que aporta los
detalles de calidad MAS concretos. Son reglas verificables que ninguna de nuestras skills
tiene todavia - ni las otras cuatro skills externas.

Lo que se busca: no importar la skill (esta en chino, depende de una CLI propia, y prohibe
Inter a secas - lo que contradice nuestra regla de contexto recien creada). Se toman SOLO
los detalles de calidad, anclados a nuestro stack.

**Lo que NO entra aca:** los 11 comandos (`/audit`, `/distill`, `/polish`, etc.). Son un
vocabulario de operaciones y merecen decision aparte (probablemente `skill-router` o un ADR
propio). Ver seccion 5.

---

## 2. Alcance: que SI

Agregar a `agents/kanam-dev/skills/frontend-ui-engineering/SKILL.md` una seccion nueva
corta: **"Reglas de calidad visual"**, con estos puntos:

### 2.1 Neutros siempre con tinte
- Nunca gris puro (`#888`, `hsl(0 0% 50%)`). Los neutros llevan una pizca de tinte:
  warm gray o cool gray.
- Razon: el gris puro es el tell #1 de UI generada. Un neutro con tinte se siente
  intencional sin costo de legibilidad.

### 2.2 Dark mode: fondo con tinte, no negro puro
- Fondo oscuro `#0f0f0f` (o equivalente oklch), nunca `#000000`.
- Razon: el negro puro aplasta, no deja profundidad ni jerarquia por elevacion.

### 2.3 Easing y duraciones canonicas
- Easing recomendado: `cubic-bezier(0.16, 1, 0.3, 1)` (fast-in-slow-out).
- Micro-interacciones: 100-200ms. Transiciones de pagina: 300-500ms.
- Nada por encima de 600ms.
- Prohibido bounce/elastic easing.
- Complementa (no reemplaza) la micro-sintaxis ya existente en la seccion
  "Design Thinking Before Code". Sigue vigente la regla dura de `prefers-reduced-motion`.

### 2.4 Medidas de lectura
- Ancho de texto de lectura: 65ch.
- Ancho de contenedor amplio: 1280px.

### 2.5 Priorizar codigo, no conceptos
- El consejo de diseño tiene que aterrizar en CSS/codigo concreto, no quedarse en concepto.
- (Refuerza el espiritu de la skill, que ya es de implementacion.)

### 2.6 Regla de fuentes POR CONTEXTO (no absoluta)
- **NO prohibir Inter a secas.** La regla dura es la de `design-direction`: depende del
  contexto.
  - Herramienta funcional (dashboard, form, tabla): fuentes de sistema o Inter son una
    decision valida (legibilidad, densidad, carga instantanea).
  - Pieza memorable (landing, portfolio, marca): fuentes con caracter.
- Esta seccion debe CITAR a `design-direction` y NO contradecirla.

---

## 3. Fuera de alcance: que NO

- **NO** importar ni instalar `Frontend Design Pro` ni el repo `impeccable`.
- **NO** incluir los 11 comandos (`/audit`, `/critique`, `/polish`, `/distill`, `/colorize`,
  `/animate`, `/bolder`, `/quieter`, `/delight`, `/normalize`, `/harden`). Van a decision
  aparte.
- **NO** prohibir Inter/system-ui de forma absoluta (contradice `design-direction`).
- **NO** copiar el catalogo de fuentes concretas (Geist, Instrument Serif, Sora) como
  obligatorio: es tendencia, no criterio. Si se mencionan, que sea como ejemplos.
- **NO** traducir/pegar la skill en chino.
- **NO** duplicar WCAG, empty/error states, skeletons ni el checklist de verificacion ya
  existentes.
- **NO** editar ningun otro archivo fuera del listado.

---

## 4. Criterios de aceptacion (verificacion real)

1. La seccion "Reglas de calidad visual" existe en `frontend-ui-engineering/SKILL.md`.
2. Contiene los 6 puntos de la seccion 2.
3. `grep -in "inter"` en la skill NO muestra una prohibicion absoluta de Inter; debe citar
   la regla de contexto de `design-direction`.
4. No hay menciones a `/audit`, `/polish`, `/distill` ni a los otros comandos.
5. `grep -in "impeccable\|antonia"` = 0 lineas (no se filtro la fuente externa en el cuerpo).
6. `python3 scripts/check-agent-skill-boundary.py` pasa.
7. Diff minimo: una seccion nueva, sin reescribir el resto.
8. Frontmatter intacto.

---

## 5. Follow-up registrado (NO se resuelve aca)

**Los 11 comandos como vocabulario de diseno.** Son la pieza mas valiosa de las 5 skills
externas: operaciones atomicas sobre un componente (`/bolder`, `/quieter`, `/distill`,
`/polish`, `/delight`...). Merecen decision propia porque no son "una regla mas": son
**triggers**. Candidatos:
- Mapearlos como triggers en `skill-router` (rutear el verbo -> skill con contexto).
- O una skill nueva de "design operations".

Requiere su propio analisis. Registrar en el daily y dejar citado en el CHANGELOG.

---

## 6. Evidencia esperada (Core verifica, ADR-078)

- `git diff` de la skill.
- Greps de los criterios 3, 4 y 5.
- `git status` mostrando solo los archivos esperados.
- Salida del check de frontera.

---

## 7. Delegacion

- **Rol:** `kanam-dev` (dueño de la skill). Core gobierna, DEV implementa (ADR-083).
- **Modelo:** `glm-5.3-flash:cloud`.
- **Contexto:** isolated; taskName y write-scope explicitos.
