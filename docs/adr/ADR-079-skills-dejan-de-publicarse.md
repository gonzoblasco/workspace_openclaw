# ADR-079: La coleccion de skills deja de publicarse (kanam-skills archivado)

**Fecha:** 2026-09-28
**Estado:** Aceptado
**Decisores:** Gonzo (definicion explicita)
**Origen:** sesion 2026-09-28 - Gonzo: *"quedamos que kanam-skills ya NO SE ACTUALIZARIA... ya no compartiremos nuestros skills"*
**Relacionado:** ADR-038 (learnings mirror DB)
**Supersede:** la practica de publicar skills al repo publico

---

## Contexto

El workspace mantenia una coleccion publica de skills en `gonzoblasco/kanam-skills`, alimentada por un proceso de publicacion con sanitizacion (`scripts/publish-skills.sh`, `scripts/sanitize-skills.py`) y por un **mirror interno** (`rsync` de `skills/` a `.github/skills/`).

Dos problemas acumulados:

1. **El mirror interno es una fuente de errores.** El 2026-09-28, `rsync --delete skills/ .github/skills/` **borro 111 archivos del mirror** (el mirror tiene skills que `skills/` ya no tiene; `--delete` los tomo como residuo). Detectado en el mismo comando y revertido con `git restore`, rehecho aditivo. Ademas, un `git add skills/*/SKILL.md` sin comillas expandio el glob y stageo skills borradas.

2. **La publicacion ya no aporta.** Gonzo define que no se comparten mas las skills.

## Decision

**1. `kanam-skills` deja de actualizarse y queda archivado en GitHub.**

Verificado: `gh repo view gonzoblasco/kanam-skills --json isArchived` -> `{"isArchived":true,"visibility":"PUBLIC"}`. Reversible con `gh repo unarchive`.

**2. La skill `publish-skills` queda archivada** (`status: archived`, `user-invocable: false`), conservada como registro de como se publicaba, no como procedimiento activo.

**3. El mirror `.github/skills/` es deuda a eliminar.** Registrado como TODO #62: "no nos hacen falta y cometemos errores como estos al intentar tenerlos sincronizados".

## Reglas que quedan del periodo de publicacion

Aunque ya no se publique, estas reglas siguen vigentes **para el mirror interno mientras exista**:

- **El mirror se sincroniza ADITIVO, nunca con `--delete`.** El mirror contiene skills que `skills/` ya no tiene; `--delete` las borra.
- **`git add` con pathspec de skills va con `--literal-pathspecs`.** Hay un path trackeado con `*` literal en el nombre (`skills/*/SKILL.md`, placeholder) y git lo trata como glob, stageando las skills borradas.
- **Sanitizacion si alguna vez se retoma:** lo personal (`Gonzo`/`gonzoblasco`) y los proyectos internos salen; la marca `Kanam` se queda (es el nombre del producto, no una identidad personal).

## Consecuencias

- **Menos superficie de error:** dos de los errores propios de la sesion del 2026-09-28 vinieron del manejo del mirror.
- El historial de como se publicaba queda en la skill archivada y en este ADR, para no reinventarlo si se retoma.
- El TODO de eliminar el mirror queda abierto hasta que el owner decida.
