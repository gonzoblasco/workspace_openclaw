---
name: "blog-publishing"
metadata:
  category: "Content"
  tags:
    - blog
    - writing
    - publishing
    - accessibility
    - devto
  status: "active"
description: "Manejar el blog personal de Gonzalo de punta a punta: convertir una fuente (PR, post de LinkedIn, caso de trabajo) en un artículo con la voz del ensayo 'The Quieter Announcement', verificarlo contra la fuente, generar el sitio estático y sindicarlo a dev.to con canonical al sitio. Usar cuando Gonzo diga 'escribamos un artículo', 'actualizá el blog', 'publicá esta nota', 'regenerá los artículos', 'sindicá a dev.to' o cuando haya que convertir un PR mergeado en una pieza pública."
user-invocable: false
---

# Blog Publishing

Una pieza publicada no es un resumen de un PR. Es la historia de lo que el usuario
escucha, por qué el código parecía correcto y qué decisión cambió el resultado. El
estándar es `content/writing/the-quieter-announcement.md`: 1.000 palabras, primera
persona, escena concreta, cero relleno.

## Fuente de verdad

| Dato | Dónde |
|---|---|
| Artículo publicado | `projects/a11y-portfolio/content/writing/<slug>.md` |
| Sitio y build | `projects/a11y-portfolio/` (`bun scripts/build.ts`) |
| Posts originales de LinkedIn | `docs/linkedin/*.md` (workspace) |
| Hechos de carrera | `memory/career-facts.md` |
| PRs y reviews | GitHub vía `gh pr view <n> --repo <repo> --json ...` |
| Mapa editorial | `projects/a11y-portfolio/.knowledge/CONTENT-MAP.md` |
| Decisiones de diseño | `projects/a11y-portfolio/.knowledge/DESIGN-BRIEF.md` |

El markdown es la fuente. El HTML es generado y no se edita a mano.

## Categorías

El blog no es solo de accesibilidad. Accesibilidad es la prioridad y el diferenciador, pero
la práctica cubre otros frentes. La categoría se elige por el tema del artículo, no por
default.

| Slug | Etiqueta | Qué entra |
|---|---|---|
| `accessibility` | Accessibility | Lo que anuncia la tecnología asistiva y los fixes de ARIA, foco y anuncios. Es la mayoría. |
| `testing` | Testing | Dónde corre un test, qué puede ver y qué bug se le escapa. |
| `engineering` | Engineering | Arquitectura, refactors, tooling y decisiones de implementación. |
| `field-notes` | Field notes | Ejercicios, challenges, proceso y lo que se aprende fuera del código. |

Regla: si el artículo no trata de accesibilidad, **no se fuerza** a esa categoría. Un
balance de un ejercicio de dev.to va a `field-notes`; un refactor orquestado va a
`engineering`; un bug que solo aparecía en browser va a `testing`.

## Anatomía del artículo

Usar este orden. No todos los artículos necesitan las siete partes, pero las primeras
cuatro son obligatorias.

1. **Apertura fría (1-3 frases).** Una afirmación contraintuitiva o una escena. Sin
   contexto previo, sin "en este artículo voy a".
2. **La escena y lo que el usuario escucha.** Componente, acción concreta, salida del
   screen reader. Si no podés describir qué oye una persona, todavía no entendés el bug.
3. **Por qué nada lo detectó.** TypeScript, axe, el test, la review: qué preguntó cada
   uno y qué no. La brecha entre "válido" y "usable".
4. **El fix y la decisión.** Una decisión de ingeniería, no una lista de pasos. Código
   solo si aclara el contrato.
5. **La review (opcional pero valiosa).** Qué objetó el maintainer, qué cambiaste, qué
   borraste. El conflicto es la parte más creíble.
6. **Tu propio error (opcional).** Un test que probaba la cosa equivocada, una
   precedencia invertida. Sin autocompasión y sin moraleja.
7. **La regla que queda.** Una frase transferible, no un resumen.

Largo: **800-1.200 palabras**. Párrafos de 1-4 frases. Un solo `h1` (el título); `h2`
para las secciones, sin numerar.

## Voz

- Primera persona, pasado concreto. "Abrí el PR en agosto", no "se abordó la problemática".
- Nombres propios y números reales: repos, PRs, roles, líneas, tests. Si un número no
  está en la fuente, no va.
- Frases cortas para los golpes. La frase de una línea después de un párrafo largo.
- Nada de hashtags, emojis de LinkedIn, "estoy feliz de compartir", "aprendí muchísimo".
- Nada de em dashes ni en dashes. Coma, dos puntos o punto.
- No explicar lo que el lector ya sabe. No definir ARIA en el párrafo 3.
- El humor, si aparece, es seco y en una sola frase. Nunca un chiste explicado.

## Proceso

### 1. Source pack (antes de escribir)

Reunir y guardar en `/tmp/<slug>-source.md`:

```bash
gh pr view <n> --repo <repo> --json title,body,comments,reviews,additions,deletions,changedFiles,mergedAt
gh issue view <issue> --repo <repo> --json title,body
```

Para un post de LinkedIn, leer el archivo completo y separar el cuerpo del post de la
metadata interna y las notas de estilo.

Para un caso sin repo público (ej. Moderno), la única fuente es el post. Se puede
escribir sobre el proceso, pero **no se inventan métricas, fechas ni resultados**.

### 2. Ficha de hechos

Antes del draft, una tabla de 5-10 líneas:

| Afirmación | Fuente | Verificada |
|---|---|---|
| `aria-label` no llegaba al `<ul role="tree">` | PR #5493 body | sí |
| 78 tests en TreeList | PR body | sí |

Toda afirmación del artículo tiene que estar en esa tabla o ser una opinión explícita.
Si una sección no tiene fuente, se recorta; no se rellena.

### 3. Draft

Escribir el markdown completo en `content/writing/<slug>.md`. Frontmatter obligatorio:

```yaml
---
title: "..."
slug: "..."
date: "YYYY-MM-DD"
lang: "en"
kind: "note" | "essay"
category: "accessibility" | "testing" | "engineering" | "field-notes"
summary: "25-45 palabras, con el bug y la consecuencia."
tags: ["accessibility", "..."]
repo: "org/repo"     # opcional
pr: 1234             # opcional
source: "linkedin"   # opcional
source_url: "..."    # opcional
---
```

### 4. Verificación

- Releer contra la ficha de hechos. Cada número, fecha y número de PR.
- `scripts/check_em_dash.py` si existe.
- Buscar hashtags, "LinkedIn", "Status:", metadata interna.
- Verificar que el summary no prometa lo que el cuerpo no entrega.

### 5. Build y gates

```bash
cd projects/a11y-portfolio
bun scripts/build.ts
```

Gates:

- build exit 0 e idempotente;
- axe-core 0 violaciones en la página del artículo;
- 1 `h1`, links internos resueltos, sin overflow a 390/1280;
- contraste AA;
- `pre` scrolleable por teclado.

### 6. Preview y publicación

- Mostrar el artículo en el portal local y pedir OK.
- Commit local atómico. Push solo con OK explícito de Gonzo.
- Después del push, esperar el rebuild de GitHub Pages y verificar la URL live.

### 7. dev.to (sindicación)

El sitio es la copia canónica. dev.to es sindicación.

- `canonical_url`: la URL del artículo en el sitio.
- Tags: máximo 4, en inglés, sin hashtags en el cuerpo.
- Estado: bloqueado hasta tener API key. El markdown de dev.to se deriva del mismo
  archivo, sin encabezado de frontmatter propio.
- Nunca publicar el mismo texto en dev.to sin canonical: duplica contenido y canibaliza
  el SEO.

## Anti-patrones

- **Resumen de PR:** "Este PR agrega X, cambia Y y actualiza tests". Eso es un changelog.
- **Listicle disfrazado:** "3 lecciones de accesibilidad". La historia va primero.
- **Métrica decorativa:** "mejoró un 40%" sin fuente. No va.
- **Entrada genérica:** "La accesibilidad es importante". Ya lo sabe el lector.
- **Repetir el mismo arquetipo:** si todas las piezas son "bug raro → review → regla",
  variar el ángulo: una puede ser un caso de producto, otra una comparación de tooling.
- **Convertir todo en accesibilidad:** si el tema es un challenge, un refactor o una
  decisión de proceso, va a su categoría. La prioridad no es la única voz.
- **Publicar por cadencia:** un PR flojo no se convierte en post.

## Checklist de cierre

- [ ] Source pack guardado y ficha de hechos completa.
- [ ] Categoría elegida por tema, no por default.
- [ ] 800-1.200 palabras, primera persona, sin hashtags ni em dashes.
- [ ] Cada número verificado contra PR/post.
- [ ] Frontmatter completo, summary de 25-45 palabras.
- [ ] Build exit 0; axe 0; links y overflow OK.
- [ ] Preview mostrado; commit local; push con OK.
- [ ] URL live verificada después del rebuild.
- [ ] Si va a dev.to: canonical correcto y API key disponible.
