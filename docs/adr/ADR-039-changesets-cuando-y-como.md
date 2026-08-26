# ADR-039: Changesets - cuándo usarlos y cómo (release de librerías)

**Status:** Accepted
**Fecha:** 2026-08-26
**Origen:** workspace
**Scope:** Workspace - práctica de release para librerías publicadas a npm
**Deciders:** Gonzo / Kanam

## Contexto

Durante la colaboración en `facebook/astryx` (PR #5493), el reviewer pidió agregar un **changeset** al PR. Un changeset es el mecanismo de la herramienta [Changesets](https://github.com/changesets/changesets): un archivo markdown que acompaña a un PR y declara qué paquete cambia, qué tipo de bump (patch/minor/major) y un resumen para el changelog. Al mergear, Changesets agrupa todos los changesets y genera la versión + changelog automáticamente.

El workspace tiene una práctica establecida de documentación de cambios: `CHANGELOG.md` por proyecto, commits atómicos, ADRs. Pero no hay un criterio explícito sobre **cuándo** un proyecto debe usar changesets y **cómo** hacerlo. Esto quedó a criterio de cada repo, y la colaboración en astryx mostró que es una práctica estándar de la industria para librerías publicadas.

**Anti-patrón a evitar:** aplicar changesets a proyectos donde no aplican (apps de producto sin release a npm), o no usarlos donde sí aplican (librerías publicadas), dejando el changelog desactualizado o a mano.

## Decision

Adoptar changesets **solo para librerías publicadas a npm** (o paquetes con versionado semántico de release). No aplica a apps de producto.

### Cuándo SÍ usar changesets

Un proyecto debe usar changesets si cumple **todas** estas condiciones:

1. **Se publica como paquete** a npm (o a un registry de paquetes).
2. **Tiene versionado semántico** de release (semver: patch/minor/major).
3. **El changelog se genera** a partir de los cambios de cada PR (no se escribe a mano post-release).

Ejemplos: `create-stack` (publicado como `@gonzoblasco/create-stack`), y cualquier librería de componentes/utilities que se publique.

### Cuándo NO usar changesets

- **Apps de producto** (SoporteML, Kanam Story, Kanam Mind, etc.): no se publican como paquetes npm, no hay versionado semántico de librería. Mantener `CHANGELOG.md` + commits atómicos + ADRs.
- **Repos de terceros** donde el maintainer no usa changesets: seguir la convención del repo, no imponer la propia.

### Cómo usar changesets (en un repo que los usa)

1. **Cada PR que toca comportamiento público** (fix, feat, breaking change) agrega un changeset.
2. **Formato del archivo** (`.changeset/<nombre>.md`):

```markdown
---
'<paquete>': patch   # o minor / major según el impacto
---

[fix] Descripción del cambio para el changelog

Detalle del cambio: qué se arregló/agregó, por qué, y el impacto en el consumidor.

@<autor>
```

3. **Tipo de bump:**
   - `patch`: fix o cambio que no rompe nada (el caso más común).
   - `minor`: feature nueva compatible.
   - `major`: breaking change.
4. **El changeset va en el mismo PR** que el cambio, no después.
5. **No editar el changelog a mano** en repos con changesets: se genera al versionar.

### Regla de idioma

El changeset va en el idioma del repo (en repos externos, inglés; en repos propios, seguir la regla de idioma del workspace: GitHub en inglés).

## Consecuencias

1. **Changelog siempre al día:** cada PR documenta su impacto de release en el momento, sin trabajo manual post-merge.
2. **Versionado semántico correcto:** el tipo de bump se decide en el PR, no a la carrera antes de publicar.
3. **Consistencia con la industria:** es el estándar en librerías grandes (React, Vite, astryx, etc.), y los maintainers lo esperan en PRs a esos repos.
4. **No aplica a apps de producto:** no se agrega complejidad donde no hay release de paquete. El `CHANGELOG.md` sigue siendo la práctica para apps.
5. **Riesgo de sobre-aplicación:** usar changesets donde no aplica agrega ruido. Mitigación: el criterio de "se publica a npm + semver + changelog generado" es la puerta de entrada.

## Implementación

- **Evaluar al crear/scaffoldear un proyecto:** si se va a publicar a npm, configurar Changesets desde el inicio (ver `create-stack` como referencia futura).
- **En PRs a repos de terceros que usan changesets:** agregar el changeset siguiendo el formato del repo (mirar un changeset existente como plantilla).
- **En proyectos propios de producto:** no configurar changesets; mantener `CHANGELOG.md`.

## Referencias

- [Changesets - documentación oficial](https://github.com/changesets/changesets)
- Colaboración en `facebook/astryx` PR #5493 (reviewer pidió changeset, 2026-08-26)
- Práctica existente del workspace: `CHANGELOG.md` por proyecto, commits atómicos, ADRs
