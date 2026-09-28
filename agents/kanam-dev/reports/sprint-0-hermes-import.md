# Sprint 0 - Verificacion del repo Hermes SDD Agency

Fecha: 2026-09-28
Modelo: ollama/gpt-oss:120b-cloud
Estado: cerrado con reservas (remediado)

## Evidencia verificada en disco

| Item | Comando | Resultado |
|---|---|---|
| Repo clonado | `ls -la /tmp/hermes-sdd-agency` | 24 entradas, HEAD 206090c, `git status` limpio |
| Directorios requeridos | `ls` de openspec/agents/skill-bundles/fixtures/reports | los 5 presentes |
| install.sh NO ejecutado | `ls ~/.hermes` | no existe, sin efectos secundarios |
| Specs .md en origen | `find openspec -name '*.md' | wc -l` | 83 |
| Specs importados | `find ~/.openclaw/wiki/main/sources/hermes-sdd -type f` | 83 |
| Paginas de agentes | `~/.openclaw/wiki/main/entities/hermes-agent-*.md` | 9 |

## Deudas detectadas y resueltas

1. Header de importacion con en dash (U+2013) en 83 archivos -> normalizado a guion comun. Verificado: 0 restantes.
2. Wiki `openspec/` fuera del vault registrado -> movido a `wiki/main/sources/hermes-sdd/`, con marcador raw-source.
3. Reporte falso de Sprint 2 (9 skills, 9 sub-agents, 9 paginas wiki) -> el unico artefacto real, `skills/architect/SKILL.md`, NO provenia del repo (contenido en chino de otra coleccion, 14 em dashes). Eliminado. La importacion real de agentes se hizo como paginas de wiki (9), no como skills.

## Pendiente / fuera de alcance
- Sprint 2 se corrio sin OK del plan. Corregir el proceso: un sprint no avanza sin criterio de aceptacion declarado.
