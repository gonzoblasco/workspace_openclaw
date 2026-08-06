# Vibe Code Cleanup

Limpieza de código generado por IA.

## ¿Para qué sirve?

Para **tomar código generado por IA (vibe coding) y llevarlo a estado producible**: sin deuda técnica, con tipos, tests y estructura sólida. Filosofía: "surgery, not demolition" — remover solo lo que está comprobadamente muerto, preservar todo lo demás.

## ¿Cuándo usarlo?

- Cuando generaste código con IA y querés llevarlo a producción
- Cuando querés diagnosticar deuda técnica en una codebase generada
- Cuando necesitás refactorizar componentes grandes, tipar `any`, consolidar duplicación
- Cuando querés endurecer un proyecto generado con tests, types y build verde

## ¿Cómo se usa?

### Workflow completo

1. **Diagnóstico** — escanear y detectar patrones de deuda técnica
2. **Reconocimiento** — mapear la codebase antes de tocar nada
3. **Limpieza** — imports muertos, archivos huérfanos, console.logs, código comentado
4. **Refactor** — extraer lógica repetida, dividir componentes > 150 líneas, tipar `any`
5. **Endurecimiento** — TypeScript estricto, tests, dependencias actualizadas
6. **Verificación** — build + typecheck + tests + lint

### Scripts útiles

```bash
# Diagnosticar codebase
./scripts/diagnose-codebase.sh --dir src

# Verificar que la limpieza no rompió nada
./scripts/verify-cleanup.sh
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/diagnostic-patterns.md` | Red flags con severidad, quick scan, orden de refactorización |
| `references/cleanup-checklist.md` | Checklist por fase: safety, structure, types, consistency, polish |

## Skills relacionadas

- [Review & Quality](../review-quality) — Para revisar el código limpio antes de mergear
- [Debug Investigation](../debug-investigation) — Para diagnosticar bugs en código generado por IA
