# ADR-112: `beam:cloud` descartado como primario del CORE y el fallback redefinido: red ante falla, nunca ante lentitud

**Fecha:** 2026-11-09 (revisado 2026-11-12)
**Estado:** Aceptado (revisado y re-aplicado al runtime 2026-11-12, verificado en `openclaw.json`)
**Decisores:** Gonzo ("No usemos beam, ya no es más gratuito. Volvemos a nuestro andando DeepSeek"; 2026-11-12: "Dejar fallback como red, solo cuando el modelo falla en lugar de cuando tarda. Son dos cosas completamente distintas. Extendido a todos los agentes") / Kanam
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

> **Correccion del 2026-11-12 — el fundamento de arriba era incompleto.**
>
> Gonzo midio el sintoma real: el sistema no cambiaba de modelo solo por falta de credito,
> **sino tambien por timeout en respuestas largas**, y en un problema complejo eso terminaba
> en una respuesta de peor calidad. La conclusion: *"si cambiaba a una respuesta menor al
> menos sea buena"*.
>
> El error del razonamiento original fue tratar **lentitud** y **falla** como lo mismo. Son
> dos casos distintos y piden respuestas opuestas:
>
> | Caso | Que corresponde |
> |---|---|
> | El modelo tarda (bufferea razonamiento, respuesta larga) | **No** cambiar de modelo: extender el techo de timeout |
> | El modelo falla (proveedor caido, error, cuota) | Cambiar de modelo: ahi entra el fallback |
>
> Y el fallback por falla **no necesita ser local**: si lo que se cayo es el modelo y no la red,
> otro modelo de la misma nube es un respaldo valido. El local sigue siendo la ultima salida
> cuando la nube entera no responde, pero no es el unico respaldo posible.
>
> ### Decision revisada (2026-11-12)
>
> 1. **El fallback cubre fallas, no lentitud.** La lentitud se resuelve con techo de timeout.
> 2. **Techo de timeout elevado a 900s** en los tres providers (`ollama`, `ollama-cloud`,
>    `ollama-local`), contra el implicito de ~120s de idle/stream que truncaba respuestas.
>    Con 15 minutos de margen, un modelo lento ya tiene margen para terminar antes de que
>    el watchdog dispare.
> 3. **El fallback vuelve a ser `gemma4:12b-mlx` (local) en los nueve agentes.** Con el
>    timeout resuelto, la unica razon que queda para cambiar de modelo es que el primario
>    falle de verdad — y ante una falla, la salida honesta es local, no otro modelo de la
>    misma nube. El fallback cloud que se probo a las 08:20 del 2026-11-12 quedo revertido
>    en la misma manana: resolvia un sintoma que el timeout ya resuelve.
> 4. Sigue vigente: **`beam:cloud` no es primario de ningun agente.**
>
> **Historial de esta revision, para que no se repita el ida y vuelta:** primero se probo
> `gpt-oss` como secundario cloud (08:20), y a los 20 minutos se volvio a Gemma local (08:41)
> al extender el timeout a 900s. La regla que queda es la de arriba; el paso intermedio no
> es una alternativa vigente.

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

Criterio de aceptación: ningún `primary` es `ollama/beam:cloud`; todo agente tiene fallback; y el fallback es `gemma4:12b-mlx` en los nueve agentes.

Aplicado y verificado el 2026-11-09. Revisado y re-aplicado el 2026-11-12 (fallback redefinido como red ante falla; techo de timeout a 900s en los tres providers; fallback vuelve a Gemma local en los nueve agentes).
