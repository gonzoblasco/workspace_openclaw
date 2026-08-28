# Notas de Captura: Skill "Higiene / Estructura de Portfolio del Workspace"

> Notas acumuladas mientras ejecutamos mejoras del ROADMAP, con el objetivo de materializar un skill práctico y reutilizable al final. Estas notas son el material crudo: procesos, pasos, lecciones y scripts. Cuando esté completo, se formaliza vía `skill_workshop`.

- **Inicio de captura:** 2026-08-28
- **Item del ROADMAP fuente:** 0.2 Higiene del workspace + 2.1 Estrategia de proyectos (ADR-001)
- **Objetivo del skill (borrador):** poder volver a ejecutar el proceso de limpieza/estructuración de portfolio + decisiones de archivo, sin re-descubrir el procedimiento.

---

## 1. Regla de oro (no negociable)

**"Definido en ADR = resuelto, no se vuelve a preguntar."**
- Si un ADR dice que un proyecto queda EXCLUIDO o ARCHIVADO, eso queda definido.
- NO se lista como "candidato a decidir" en auditorías de higiene.
- NO se vuelve a abrir su destino salvo pedido explícito.
- El ADR es la autoridad sobre cualquier auditoría posterior.

**Lección que motivó esto:** al auditar `soporteml-v4` (excluido en ADR-001), lo listé como "a decidir" en vez de darlo por resuelto. Fallo de proceso. Registrada en `docs/learnings/metodologia.md`.

**Cómo hacerlo ejecutable en el ADR:** cuando un proyecto se excluye/archiva, agregar cláusula explícita:
> **NO TOCAR**: este proyecto no se modifica, no se decide su destino, y no se lista como candidato en auditorías de higiene. La exclusión es una decisión cerrada; no se vuelve a abrir salvo pedido explícito.

---

## 2. Patrón real de doble git del workspace (descubierto por observación)

**Este es el hallazgo más valioso de la sesión.** El template `init-project.sh` dice una cosa, pero los proyectos activos hacen otra. El patrón REAL es:

### Cómo trackean los proyectos ACTIVOS (create-stack, kanam-mind, a11y-fixer)
- **El workspace trackea el `.knowledge/` del proyecto como blobs sueltos** (modo `100644`), NO como gitlink.
- **El repo git del proyecto (carpeta con `.git`) convive** con ese trackeo: el workspace trackea `.knowledge/` y el proyecto trackea su código.
- **`.knowledge/` NO está ignorado** en el `.gitignore` del proyecto (por eso el workspace y el repo del proyecto ambos lo trackean - doble trackeo).
- **NO hay `.gitmodules`** en el workspace (no usa submodules).
- Verificación: `git ls-files --stage projects/a11y-fixer/` muestra `100644 .../HANDOFF.md` (blob), no `160000` (gitlink).

### Contraste con el template `init-project.sh`
- El template genera un `.gitignore` que **ignora `.knowledge/`** y registra **submodule** (`git submodule add`).
- ESO NO SE USA en la práctica para los proyectos activos. Es un patrón teórico que difiere del real.

### Cómo promover una carpeta a proyecto doble git (pasos verificados)
1. **Inicializar repo del proyecto** en la carpeta: `git init && git branch -m main`.
2. **Crear `.gitignore` del proyecto SIN ignorar `.knowledge/`** (patrón create-stack).
3. **Crear repo privado en GitHub** y pushear: `gh repo create <owner>/<slug> --private --source=. --push`.
4. **El workspace trackea el `.knowledge/` como blob** (NO como submodule, NO `git submodule add`).
5. **Orden crítico:** el `.knowledge/` debe trackearse en el workspace. Si se inicia el `.git` interno PRIMERO y el `.knowledge/` no está trackeado, el workspace lo ve como repo embebido y NO lo trackea (ni con `-f`). Una vez trackeado, el `.git` interno no interfiere.

### Advertencias del proceso
- **No usar `git submodule add`** para proyectos del workspace (rompe el patrón: crea `.gitmodules`, que el resto no tiene).
- Si cometés el error de crear submodule: deshacer con `git rm --cached -f <path>` + `git config --remove-section submodule.<name>` + borrar `.gitmodules`. Y limpiar del stage.
- **`gh repo archive <owner>/<repo>`** archiva en GitHub → el repo queda read-only (no acepta push). Los repos archivados no se pueden pushear; un commit local quedará sin subir (esperable).

---

## 3. Comandos útiles verificados

```bash
# Estado de un submodulo/gitlink
git diff --submodule=log projects/<slug>

# Ver si una carpeta es gitlink (160000) o blob suelto (100644) en el workspace
git ls-files --stage projects/<slug>/

# Archivar un repo en GitHub (read-only después)
gh repo archive <owner>/<repo> --yes

# Ver estado de archivo de un repo
gh repo view <owner>/<repo> --json isArchived

# Quitar un submodule mal creado
git rm --cached -f projects/<slug>
git config --remove-section submodule.projects/<slug>
rm -f .gitmodules
```

---

## 4. Pasos del proceso de higiene (flujo general del skill)

1. **Solo lectura primero** - `git status`, `git ls-files --stage projects/*`, ver gitlinks vs blobs.
2. **Clasificar cada proyecto:** ¿gitlink? ¿blob suelto? ¿untracked? ¿candidato a archivar/reset según ADR?
3. **Respetar el ADR** - si un proyecto está excluido/archivado, NO tocarlo, NO preguntar de nuevo.
4. **Archivar repos en GitHub** que lo requieran (`gh repo archive`).
5. **Limpiar basura** (ej. `.DS_Store` trackeado): `git rm --cached` + `trash` del disco, commit y push (salvo repo archivado).
6. **Promover carpetas** a doble git siguiendo el patrón real (sección 2).
7. **Commit atómico + push** del workspace (con `git pull --rebase` antes).
8. **Verificar estado final limpio** - `git status --short` solo con cambios intencionales.

---

## 5. Auditoría completa de projects/* (2026-08-28 - resultado REAL)

Estado de los 16 projects/:

**BLOB(.knowledge) - patrón correcto (10):** a11y-fixer, create-stack, kanam-forge, kanam-mind, kanam-solitaires, kanam-story, portfolio-strategy, quedamos, soporteml-v3, soporteml, ultimo-turno

**GITLINK - sin .knowledge como blob (4):** accessible-ui (archivado), ai-developer-stack, create-with-ai (archivado), soporteml-v4 (tiene .knowledge en disco pero NO trackeado por workspace)

**REPO-PROPIO/otros:** kanam-skills (repo de skills vivo en GitHub, sin .knowledge/ - su contenido son skills, correcto así), kanam-forge (README.md modificado = trabajo en curso de Gonzo, no tocar), kanam-mind (components/SettingsModal.tsx modificado = trabajo en curso, no tocar)

### Observación clave
Coexisten DOS patrones: el dominante (blob `.knowledge/` trackeado por workspace) y el gitlink (solo puntero al repo, sin `.knowledge/` como blob). Los gitlinks parecen ser proyectos más nuevos o que no migraron. LOS ARCHIVADOS (accessible-ui, create-with-ai) y SOPORTEML (v3/v4, decisión cerrada) NO se tocan.

### Hallazgo: ai-developer-stack (proyecto vivo, NO tocar sin pedido)
- Es un gitlink. Su `.knowledge` es un **symlink roto**: apunta a `../ai-developer-stack-knowledge`, directorio que NO existe ni en disco ni en GitHub (modo 120000 en git).
- El contenido real (ai-agents, backend-infra, etc.) vive en carpetas del repo, no en un `.knowledge/` real.
- ES PROYECTO VIVO de skills de agentes IA. No es basura. Reparar su estructura requiere decisión explícita de Gonzo.
- Registrado como hallazgo, no como acción de higiene.

### Decisión pendiente
¿Migrar los gitlinks activos (ai-developer-stack, soporteml-v4) al patrón blob (trackear `.knowledge/` en workspace) para garantizar respaldo? O dejarlos como gitlink si el repo GitHub es la fuente confiable.

---

## 6. Pendiente para completar el skill

- [ ] Decidir si reparar el symlink roto de .knowledge en ai-developer-stack (requiere pedido explícito de Gonzo - es proyecto vivo).
- [ ] Auditar los `projects/*` restantes en detalle (kanam-skills, soporteml, quedamos - por qué blob vs gitlink).
- [ ] Decidir el destino local de `accessible-ui` (archivado en GitHub, pero ¿se deja la carpeta local o se limpia?).
- [ ] Verificar si todos los proyectos activos siguen el patrón `.knowledge/` en el repo GitHub (validar que "GitHub es la fuente" se cumple).
- [ ] Testear la reproducibilidad: ¿puedo volver a ejecutar un scaffold doble git sin romper el patrón?
- [ ] (Post) Migrar gitlinks activos a blob si se decide.
