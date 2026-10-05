# Spec: Output Gates y jerarquia en `design-direction` 🌿

**Creado:** 2026-10-05
**Origen:** skill #11 analizada - `Design` (ivangdavila / Clawic). Es la unica de las 11
skills de la tanda con GATES REALES de verificacion visual. Responde directo al hueco
marcado desde la #1: ninguna skill externa tenia verificacion.
**Rol dueño:** kanam-dev
**Estado:** PROPUESTO - pendiente de delegacion

---

## 1. Motivacion

`design-direction` (creada hoy) cubre DECIDIR la direccion estetica. Lo que le falta es el
cierre: como VERIFICAR que la direccion se cumplio. `Design` (Clawic) trae la unica pieza
de la tanda que resuelve esto: los **Output Gates**, mas un marco de jerarquia como ranking
que es criterio de diseño puro (no CSS).

Van a `design-direction` (no a `frontend-ui-engineering`, que es de ejecucion CSS y ya
recibio 3 cambios hoy). Razon: son criterio de direccion + verificacion de diseño, y cierran
el ciclo "decidir direccion -> verificar que se cumplio".

---

## 2. Alcance: que SI

Agregar a `agents/kanam-dev/skills/design-direction/SKILL.md` una seccion nueva:
**"Output Gates: verificacion de diseño"**, mas un bloque de jerarquia.

### 2.1 Jerarquia como ranking (Core Rule)
- La jerarquia es un RANKING, no una pasada de estilos.
- Inventariar cada elemento, rankear 1-3 por importancia para el usuario:
  1 = debe verse, 2 = de apoyo, 3 = metadata.
- **Exactamente un rank-1 por vista.**
- Check: una captura en escala de grises debe revelar el ranking en 3 segundos.
- **Un canal por paso de nivel:** niveles adyacentes difieren en UN canal (tamaño x1.25,
  peso +300, o un salto de luminosidad). Tres tweaks chicos leen como ruido.
  Ejemplo: 18px/600 al lado de 16px/400 son dos medio-pasos y rankean mal; usar 20px/400
  o 16px/700.

### 2.2 Los 6 Output Gates (verificacion antes de entregar)
1. **Grayscale test:** desaturado, el ranking 1-3 sigue obvio en 3 segundos?
2. **Squint test:** desenfocado, saltan exactamente el titulo y la accion primaria?
3. **Alignment count:** <= 3 lineas de alineacion vertical, y cada elemento sobre una.
4. **Spacing audit:** cada gap es multiplo de la base; entre-grupos >= 2x intra-grupos.
5. **Contrast check:** cada par texto/fondo cumple su piso (4.5:1 body, 3:1 large/UI).
6. **Single rank-1:** exactamente una accion primaria o foco por vista.

### 2.3 "Design in grayscale first"
- Layout, jerarquia y spacing deben funcionar sin color.
- El color entra ULTIMO, para codificar significado (estado, accion, marca).
- Razon: el color usado para rescatar jerarquia falla para ~8% de hombres con CVD y
  falla el grayscale gate.

### 2.4 "Space belongs to what it labels"
- Un heading esta mas cerca del texto de abajo (8px) que de la seccion de arriba (32px).
- Gaps iguales destruyen el agrupamiento.

### 2.5 "Optical beats mathematical"
- Iconos, triangulos y botones de play necesitan un shift de 1-3px hacia su peso visual
  para verse centrados.
- Default: grid para layout, correcciones opticas permitidas a nivel componente. Nunca
  al reves.

### 2.6 "One radius scale per artifact"
- Una sola escala de radios por artefacto (ej. 4/8/16).
- Radii mezclados en elementos hermanos es el tell mas rapido de UI generada sin revisar.

### 2.7 Tabla de Traps (adaptada)
Errores comunes con por que fallan y que hacer. Al menos: centrar texto largo; enfasis con
bold + grande + color a la vez; color como unica señal de estado; grises puros al lado de
un accent saturado; rellenar cada espacio vacio; restyling antes de rankear; diseñar solo
el happy state.

---

## 3. Fuera de alcance: que NO

- **NO** importar ni instalar la skill `Design` (Clawic) ni sus skills relacionadas.
- **NO** crear la estructura `~/Clawic/data/design/` ni mover datos ahi. Nuestra memoria es
  `memory.db`; no se replica infraestructura externa.
- **NO** incluir contenido promocional ("star it", "get more skills at clawic.com").
- **NO** copiar el archivo de config `.yaml` ni el sistema de overrides por pagina.
- **NO** duplicar lo ya existente en `design-direction`: las 4 preguntas, la distincion
  herramienta/memorable, el orden layout->tema->animacion->codigo, la regla de
  intencionalidad. Solo agregar lo nuevo.
- **NO** duplicar reglas que ya viven en `frontend-ui-engineering` (easing, duraciones,
  neutros con tinte, dark mode, 65ch/1280px). Si hace falta, referenciar.
- **NO** mencionar la fuente externa (Clawic, ivangdavila) en el cuerpo de la skill.
- **NO** editar ningun otro archivo fuera del listado.

---

## 4. Criterios de aceptacion (verificacion real)

1. Seccion "Output Gates: verificacion de diseño" (y el bloque de jerarquia) en
   `design-direction/SKILL.md`.
2. Contiene los 6 gates + jerarquia como ranking + los puntos 2.3 a 2.7.
3. Sin duplicacion: las 4 preguntas / herramienta-vs-memorable / orden de fases siguen
   apareciendo una sola vez (no se repiten en la seccion nueva).
4. `grep -in "clawic\|ivangdavila\|star it\|clawic.com"` = 0 lineas.
5. `python3 scripts/check-agent-skill-boundary.py` pasa.
6. Frontmatter intacto. Diff minimo.
7. `check_em_dash.py` = sin guiones largos (ADR-082).

---

## 5. Evidencia esperada (Core verifica, ADR-078)

- `git diff` de la skill (solo el hunk nuevo).
- Greps de los criterios 3 y 4.
- `git status` mostrando solo el archivo esperado.
- Salida de boundary + em dash.

---

## 6. Delegacion

- **Rol:** `kanam-dev` (dueño de las skills de diseño). Core gobierna, DEV implementa (ADR-083).
- **Modelo:** `glm-5.3-flash:cloud`.
- **Contexto:** isolated; taskName y write-scope explicitos.
