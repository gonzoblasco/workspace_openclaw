# Debug Investigation

Investigación sistemática de bugs.

## ¿Para qué sirve?

Para **encontrar la causa raíz** de un bug de forma metódica. No implementa fixes, no refactoriza, no optimiza. Su única misión es responder "¿qué está pasando?" y "¿por qué ocurre?".

**Filosofía:** Diagnose before you prescribe. La primera hipótesis suele ser incorrecta. Los síntomas no son la causa.

## ¿Cuándo usarlo?

- Bugs que no entendés
- Errores intermitentes
- Regresiones después de un cambio
- Comportamiento inconsistente
- Degradación de performance

## ¿Cómo se usa?

### Workflow completo

1. **Intake** — registrar problema, entorno, frecuencia, evidencia
2. **Reproduction** — lograr reproducir el bug
3. **Scope Analysis** — ¿siempre ocurre? ¿solo prod? ¿solo ciertos usuarios?
4. **Evidence Collection** — logs, stack traces, network, DB, screenshots
5. **Hypothesis Generation** — múltiples hipótesis, ordenadas por probabilidad
6. **Experiment Design** — un experimento por pregunta
7. **Root Cause Analysis** — causa inmediata + sistémica + factores contribuyentes
8. **Handoff** — documentación para el workflow de implementación

### Scripts útiles

```bash
# Git bisect automatizado
./scripts/bisect.sh <good-commit> "npm run test"

# Colectar logs del sistema
./scripts/log-collector.sh --server /var/log/app

# Analizar archivos de log
python3 scripts/analyze_logs.py /var/log/app.log --top 10

# Verificar pasos de reproducción
./scripts/reproduce-check.sh DEBUG_REPORT.md
```

## Referencias

| Archivo | Qué contiene |
|---|---|
| `references/experiments.md` | Diseño de experimentos: una variable a la vez |
| `references/techniques.md` | Técnicas: binary search, git bisect, rubber duck, five whys |
| `references/git-bisect-guide.md` | Guía práctica de git bisect |
| `references/browser-devtools.md` | Debugging en Chrome DevTools |
| `references/node-debugging.md` | Debugging en Node.js: inspector, heap, CPU profiles |

## Skills relacionadas

- [Performance Optimization](../performance-optimization) — Para investigar degradaciones
- [Incident Response](../incident-response) — Para bugs en producción con impacto
