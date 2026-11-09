# ADR-112: `beam:cloud` descartado como primario del CORE y Gemma local como único fallback

**Fecha:** 2026-11-09
**Estado:** Aceptado (aplicado al runtime 2026-11-09, verificado en `openclaw.json`)
**Decisores:** Gonzo ("No usemos beam, ya no es más gratuito. Volvemos a nuestro andando DeepSeek"; "Usemos Gemma como único fallback") / Kanam
**Origen:** sesión 2026-11-09 — `beam:cloud` apareció asignado como primario de `agents.defaults.model`, dejó de estar en el plan gratuito de Ollama y produjo errores en dos sesiones de cursos de YouTube que tuvieron que re-evaluarse con DeepSeek.
**Relacionado:** ADR-090 (asignación de modelos por rol), ADR-107 (`deepseek-v4.1-flash` primario del CORE), ADR-105 (`beam` 3/4 en el bench del slot B), ADR-076 (ningún agente hereda modelo local), ADR-100 (fuente única).

---

## Contexto

`beam:cloud` entró al workspace como candidato por ser un modelo nuevo de Ollama Cloud, y salió del bench del slot B con el peor resultado de los tres evaluados: 3 de 4 bugs encontrados, se auto-aprobó con el defecto vivo y respondió en inglés contra el formato pedido (ADR-105 §6: *"no entra al pipeline"*). Esa decisión solo lo excluyó del revisor B.

El 2026-11-09 apareció asignado como **primario** de `agents.defaults.model`, un cambio que no pasó por ADR ni por revisión. En paralelo dejó de estar incluido en el plan gratuito de Ollama Cloud, y falló en dos sesiones reales de cursos de YouTube que hubo que re-evaluar con DeepSeek.

Mientras tanto la política de fallbacks había crecido sin criterio: cada agente encadenaba uno o dos modelos cloud como respaldo (`minimax`, `deepseek`, `nemotron`, `gemma4:cloud`). Un fallback que vive en la misma nube que el primario no es un fallback: es la misma dependencia con otro nombre de archivo.

## Decisión

1. **`beam:cloud` no se asigna como primario de ningún agente**, ni del CORE ni de rol. Queda únicamente en el catálogo de modelos habilitados, sin asignación.
2. **El único fallback de todos los agentes es `gemma4:12b-mlx`** (local, MLX). No se encadenan modelos cloud como respaldo.
3. La cadena queda, para cada agente: **primario en la nube según su rol (ADR-090) → `gemma4:12b-mlx`**. Sin escalones intermedios.
4. Aclaración necesaria: **`gemma4:cloud` no es local** aunque el nombre lo sugiera. El local es `gemma4:12b-mlx`.

## Fundamento

- **Costo:** `beam` dejó de ser gratuito. Un primario que se paga sin haber ganado su lugar no se sostiene.
- **Calidad ya medida:** 3/4 bugs y auto-aprobación con el defecto vivo. Un modelo que no ve el error que tiene delante no es un ahorro, es deuda.
- **Arquitectura:** el fallback existe para el caso "la nube no responde". Si el respaldo también está en la nube, no cubre ese caso. La única salida real es local.

## Consecuencias

**A favor:** el sistema sigue operando sin red y sin cuota. Una caída del proveedor deja de ser una caída del workspace. La política queda con una sola regla, comprobable de un vistazo.

**En contra:** cuando se caiga la nube, el trabajo baja a un 12B local — más lento y con menos capacidad que cualquier primario cloud. Es una degradación aceptada a cambio de no quedar sin servicio.

**Descartado:** mantener `minimax`/`nemotron`/`gemma4:cloud` como escalones intermedios. Agregaban latencia de fallo sin cubrir el escenario que importa.

## Verificación

Comando de control sobre el config vivo:

```bash
python3 -c "
import json
d=json.load(open('$HOME/.openclaw/openclaw.json'))
a=d['agents']
print('defaults', a['defaults']['model']['primary'], a['defaults']['model']['fallbacks'])
for k,v in a['entries'].items():
    m=v.get('model')
    if m: print(k, m['primary'], m.get('fallbacks'))
"
```

Criterio de aceptación: ningún `primary` es `ollama/beam:cloud`, y todo `fallbacks` es exactamente `["ollama/gemma4:12b-mlx"]`.

Aplicado y verificado el 2026-11-09.
