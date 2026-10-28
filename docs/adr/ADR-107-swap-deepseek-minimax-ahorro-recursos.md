# ADR-107: Se intercambian `deepseek-v4.1-flash` y `minimax-m3.1-flash` en el CORE y los defaults (ahorro de recursos medido en uso real)

**Fecha:** 2026-10-28
**Estado:** Aceptado (aplicado al runtime 2026-10-28, verificado)
**Decisores:** Gonzo ("ahora será DeepSeek v4.1 Flash el default... ese 20% más económico en recursos resulta que es bastante... que quede Gemma4 de Helper... Alternativo pondremos MiniMax M3.1 Flash (los estamos intercambiando)") / Kanam
**Origen:** uso real del plan de Ollama Cloud después de la cata 2026-10-20 (`docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`)
**Relacionado:** ADR-090 (asignación de modelos por rol), ADR-102 (minimax como motor del CORE), ADR-077/088/089 (pipeline A/B), ADR-076 (ningún agente hereda modelo local)
**Supersede:** **ADR-102**, secciones "Decisión" y "Riesgos y mitigaciones §3 (cuota)". El resto de ADR-102 (ficha de capacidades, riesgos 1 y 2) sigue vigente como medición del modelo.

---

## Contexto

ADR-102 puso `minimax-m3.1-flash:cloud` como motor del CORE y de `agents.defaults` el 2026-10-20,
apoyado en una cata de 40 celdas donde `main` puntuó 8,9 contra 7,8 de `deepseek-v4.1-flash`.

Su revisión del 2026-10-24 midió la cuota real y concluyó mantener minimax: el delta medido era
**1,25x de cuota por request** (0,066 vs 0,053 px/req), que en la barra semanal era **0,5% de la
cuota**: cambiar el default "compra 0,5% y cuesta la calidad medida del rol main".

Ese cálculo subestimó dos cosas, y el uso real las mostró:

1. **El delta por request no es el delta por sesión.** La cuota de 0,5% se calculó sobre una
   distribución de requests donde minimax tenía 2.201 de ~5.400. En el uso efectivo de octubre el
   CORE concentra la mayoría de los turnos, así que su peso en la barra crece muy por encima de su
   participación en el conteo.
2. **La espiral de thinking de minimax se paga en cuota y en latencia, no solo en calidad.** El
   thinking de minimax es *always-on* - `think:false` no lo apaga (medido en ADR-102: 3 corridas
   con `think:false` devolvieron 463/134/193 caracteres de razonamiento) - y se factura como output.
   El CORE, que es el rol con más turnos, es el que más lo paga.

Gonzo midió el efecto y lo cifró: **~20% más económico en recursos**, un margen bastante mayor que
el 0,5% estimado en la revisión de ADR-102.

## Decisión

**`deepseek-v4.1-flash:cloud` pasa a ser el primario del CORE (`main`) y de `agents.defaults`;
`minimax-m3.1-flash:cloud` pasa a alternativo/fallback.** Es un intercambio de posiciones, no una
baja: minimax sigue disponible como ruta de respaldo.

| Clave | Antes (ADR-102) | Ahora |
|---|---|---|
| `agents.defaults.model.primary` | `minimax-m3.1-flash:cloud` | **`deepseek-v4.1-flash:cloud`** |
| `agents.defaults.model.fallbacks` | `deepseek-v4.1-flash:cloud` | **`minimax-m3.1-flash:cloud`** |
| `agents.entries.main.model.primary` | `minimax-m3.1-flash:cloud` | **`deepseek-v4.1-flash:cloud`** |
| `agents.entries.main.model.fallbacks` | `deepseek-v4.1-flash:cloud` | **`minimax-m3.1-flash:cloud`** |
| `agents.defaults.utilityModel` | `gemma4:cloud` | `gemma4:cloud` (**sin cambio**, es el Helper) |
| Pipeline A/B - revisor (B) | `deepseek-v4.1-flash:cloud` | `deepseek-v4.1-flash:cloud` (**sin cambio**) |
| Pipeline A/B - ejecutor (A) | `gpt-oss:120b-cloud` | `gpt-oss:120b-cloud` (**sin cambio**) |
| Pipeline A/B - pre-filtro | `gemma4:cloud` | `gemma4:cloud` (**sin cambio**) |
| Roles dev/ops/auditor/critic/planner/mind/studio | - | **sin cambio** |

**El pipeline no se toca.** Fue explícito en el pedido: "menos en el pipeline, sigue deepseek siendo
el reviewer". La asimetría de ADR-077 (ejecutor liviano, revisor grande) queda tal cual; que B sea
deepseek es ahora *además* la misma familia que corre el CORE, sin efecto mecánico: el revisor se
elige por la asimetría, no por el default.

## Justificación

- **La unidad de decisión es la cuota de GPU, no el precio por token** (corrección ya establecida en
  ADR-102 §3). Con esa unidad, un 20% medido en uso real es un orden de magnitud mayor que el 0,5%
  que estimó la revisión del 24.
- **Off-peak iguala los precios.** Fuera de 12:00-18:00 UTC en días hábiles (y todo el fin de semana)
  `minimax-m3.1-flash` y `deepseek-v4.1-flash` tienen el mismo precio de output ($0.60/1M). El
  ahorro viene del **consumo**, no del precio: minimax gasta ~25% más de output por thinking
  always-on.
- **El costo de calidad es acotado y reversible.** La diferencia medida era 8,9 vs 7,8 en el rol
  `main`, sobre una cata de 40 celdas - no sobre el uso real. El fallback es la ruta de vuelta en un
  turno, y revertir el swap es cambiar dos claves.
- **Deepseek ya era el fallback del CORE**, así que su comportamiento en este entorno está probado
  por las corridas que cayeron en fallback.

## Riesgos y mitigaciones

1. **Degradación de calidad en el CORE sin señal fuerte.** El rol que orquesta (delega, verifica,
   sintetiza) tolera algo menos de punta que un rol de generación, pero no errores de verificación.
   *Mitigación:* vigilar los cierres de sesión que dependan de verificación del repo y de gates.
   Síntoma esperado si falla: verificación superficial, no espirales. Si aparece, volver es cambiar
   el `primary` de `main` a minimax (el bloque managed y este ADR registran el estado anterior).

2. **`minimax` como fallback hereda su espiral de thinking en el peor momento.** El fallback se usa
   justo cuando deepseek falla, y minimax es el modelo con celdas irrecuperables (ADR-102 §1: 1 de 40
   en 3 intentos).
   *Mitigación:* aceptada. Un fallback imperfecto es mejor que ninguno, y el rol `main` no tiene SLA
   de entrega. Si el fallback se vuelve frecuente, el problema es deepseek, no minimax.

3. **La cuota de Ollama es semanal con reset; el ahorro se confirma al cierre de la ventana.**
   *Vigilancia:* comparar la barra de uso del panel al final de la semana contra la de la semana
   previa con volumen de requests comparable. Anotar el resultado acá o en el daily.

## Verificación (2026-10-28, runtime vivo)

- `openclaw config patch --file` → `Applied 5 config update(s)`, `Config valid`.
- `openclaw config get agents.defaults.model` → `deepseek-v4.1-flash:cloud` + fallback
  `minimax-m3.1-flash:cloud`. `agents.entries.main.model` idéntico. `utilityModel` =
  `gemma4:cloud` (sin cambio).
- Diff contra el backup (`/tmp/openclaw.json.bak-20261028-185246`): **un solo agente cambió**
  (`main`); los otros siete, byte a byte iguales. Cero rutas de config perdidas.
- `openclaw doctor`: único aviso de modelo = `minimax-m3.1-flash:cloud` "not in the local model
  catalog" - esperado, es un modelo cloud que el catálogo local no lista; resuelve por `ollama show`.
- `scripts/gateway-config-drift.sh --accept` → `no config drift`.
- `managed-blocks`: `model_primary`, `model_triple`, `model_by_agent` y `model_alternative`
  actualizados; `apply` idempotente (segunda corrida = "al día"); `AGENTS.md` 16.277/20.000 y
  `USER.md`/`MEMORY.md` bajo cap.
