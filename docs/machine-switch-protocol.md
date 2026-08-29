# Protocolo de Cambio de Máquina

**Fecha:** 2026-08-28
**Estado:** Aceptado

---

## El Problema

Gonzo trabaja entre dos máquinas (Mac Mini y MacBook Air), con el workspace sincronizado por git. El riesgo es la fricción al cambiar de máquina: conflictos de merge, daily notes pisados, submódulos huérfanos.

## El Protocolo

### Al Llegar a una Máquina (Pull)
1. **Siempre `git pull --rebase`** antes de trabajar. Esto evita pisar cambios de la otra máquina.
2. **Si hay conflictos en daily notes**: NO descartar automáticamente. Comparar el contenido local vs el del repo. Las notas locales pueden tener sesiones que la otra máquina nunca pusheó. Backup primero (`cp` a /tmp), comparar con `diff`, quedarse con la versión más completa.
3. **Si hay conflictos en general**: hacer **merge, nunca reset**. El soft reset descarta commits de la otra máquina.

### Al Terminar en una Máquina (Push)
1. **Commit atómico** de los cambios del workspace.
2. **`git pull --rebase`** antes del push (para traer cualquier cambio de la otra máquina).
3. **`git push`**.

### Submódulos y Repos Embebidos
- **Verificar `.gitmodules`**: Un gitlink sin entrada en `.gitmodules` es un "submódulo huérfano" que se muestra como dirty (`m` flag) para siempre.
- **Repos muertos**: Un submódulo que apunta a un repo que no existe en GitHub no bloquea, pero ensucia el estado. Inspeccionar y limpiar.
- **Worktrees**: Los proyectos que son worktrees (`.git` es un archivo) requieren que los hooks y configs se apliquen en el `.git` del worktree, no en el principal.

### Datos Locales (NO viajan por git)
- `.env`, `*.db`, tokens, uploads: **NO se respaldan con git**. Son IRRECUPERABLES.
- **Regla**: Antes de mover, limpiar o re-clonar un proyecto, respaldar SIEMPRE `.env` y `*.db` a una carpeta de backups fuera del repo (ej. `backups/<proyecto>/`).

## Criterio de Éxito

- Cambio de máquina sin fricción (pull --rebase, merge, no reset).
- 0 conflictos de merge no resueltos en un mes.
- Ningún dato local perdido por limpieza o sync.
