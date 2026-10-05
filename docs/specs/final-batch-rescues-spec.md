# Spec: lote final de rescates de la tanda de 19 skills 🌿

**Creado:** 2026-10-05
**Origen:** rescates menores acumulados de las skills #14, #16, #17 y #18 de la tanda de 19.
**Rol dueño:** kanam-dev
**Estado:** PROPUESTO - pendiente de delegacion

---

## Lote A: `design-direction` (rescates #14, #16, #17)

Agregar a `agents/kanam-dev/skills/design-direction/SKILL.md` los siguientes aportes.

### A.1 Descubrimiento visual: "show, don't tell" (de #14, Frontend Slides)
- Para elegir una direccion, en vez de DESCRIBIR estilos en texto, **generar 2-3
  micro-previews visuales** (una card, un header o una title-slide en cada estilo) y
  mostrar las opciones para que el humano elija.
- El humano reacciona mejor a lo que VE que a lo que lee: bajar a 3 previews concretos
  evita la conversacion abstracta sobre "que tono queremos".
- Regla complementaria (de #18): usar preview visual cuando el contenido ES visual
  (layout, wireframe, paleta); usar texto cuando es conceptual (proposito, trade-offs,
  opciones A/B/C/D).
- Test: "el humano entenderia mejor viendolo que leyendolo?".

### A.2 Salto extremo de peso y tamaño (de #16, Elite Frontend Design)
- Para una pieza memorable, el contraste tipografico puede ser EXTREMO, no incremental:
  - Peso: 100 vs 900 (no solo 400 vs 700). El salto maximo de peso define el registro.
  - Tamaño: salto minimo de 3x (ej. body 14-16px vs hero 48px+).
- Complementa (no reemplaza) la regla ya existente "un canal por paso de nivel" que vive
  en `frontend-ui-engineering`: ahi el foco es el salto por PASO de jerarquia; aca es el
  registro general de la pieza.
- Contexto: esto es para pieza memorable. En herramienta funcional rige la neutralidad.

### A.3 Paletas derivadas de temas de editor (de #16)
- Una fuente de inspiracion de paleta valida y no obvia: **temas de IDE** (Dracula, Nord,
  Tokyo Night, Monokai). Son paletas ya balanceadas por uso intensivo y tienen reglas
  propias de contraste.
- Es una alternativa mejor que "elegi de una lista de paletas": da un ORIGEN con criterio.

### A.4 La tabla 80/20 de calidad percibida (de #17, UI Design)
- Donde se va el esfuerzo, por impacto percibido:
  - Tipografia: ~40%
  - Spacing: ~25%
  - Color: ~20%
  - Todo lo demas (sombras, bordes, motion): ~15%
- Tipografia + spacing = ~65% de la calidad percibida: invertir ahi primero.
- Esta tabla EXPLICA por que las secciones de tipografia y spacing son las mas extensas.

---

## Lote B: proceso de spec (rescate #18, Superpowers Brainstorming)

Agregar a `agents/kanam-dev/skills/spec-driven-development/SKILL.md` (o
`openspec-pattern` si encaja mejor; decidir y justificar) una seccion corta:

### B.1 El hard gate de aprobacion
- **Antes de invocar cualquier skill de implementacion, escribir codigo o arrancar un
  proyecto: presentar el diseño y obtener aprobacion.** Sin importar la complejidad
  percibida.
- "'Simple' es justo donde los supuestos no examinados causan mas desperdicio. El diseño
  puede ser corto (pocas frases para un proyecto simple), pero debe ser presentado y
  aprobado."
- El flujo TERMINA en el plan de implementacion, no salta a construir.

### B.2 Evaluar el alcance antes de preguntar
- Si el pedido describe multiples subsistemas independientes (ej. chat + storage + billing
  + analytics), marcarlo de inmediato. No refinar detalles de algo que primero hay que
  descomponer.

### B.3 Spec self-review (4 chequeos)
Tras escribir el spec, revisarlo con ojos frescos:
- Placeholder scan: hay "TBD"/"TODO"/partes incompletas?
- Consistencia interna: se contradicen las secciones?
- Scope check: es suficientemente enfocado para un solo plan?
- Ambiguity check: algun requisito admite dos interpretaciones? Elegir una y explicitarla.
- Arreglar inline, sin re-revisar.

---

## Fuera de alcance

- **NO** importar ninguna de las skills externas.
- **NO** crear estructuras externas (docs/superpowers/, ~/Clawic/, etc.).
- **NO** adoptar GSAP/Lenis/Three/Framer Motion/Pillow ni dependencias externas.
- **NO** duplicar reglas ya existentes.
- **NO** mencionar fuentes externas (Clawic, Superpowers, awwwards, etc.).
- **NO** editar archivos fuera de los dos listados.

---

## Criterios de aceptacion

1. `design-direction/SKILL.md` con los 4 aportes del Lote A.
2. La skill de proceso con los 3 puntos del Lote B (justificar eleccion de destino).
3. Sin menciones a fuentes externas ni dependencias no adoptadas.
4. Checks: `check-agent-skill-boundary.py`, `check_em_dash.py` (ADR-082), frontmatter valido.
5. Diff minimo y atomico por archivo.

---

## Evidencia esperada (Core verifica, ADR-078)

- `git diff` de ambas skills.
- `git status` con solo los 2 archivos esperados.
- Greps de prohibidas.
- Salida de los checks.
