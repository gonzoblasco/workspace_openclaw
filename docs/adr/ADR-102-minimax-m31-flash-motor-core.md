# ADR-102: `minimax-m3.1-flash:cloud` como motor del CORE (main)

**Fecha:** 2026-10-20
**Estado:** Aceptado (aplicado al runtime 2026-10-20, verificado)
**Decisores:** Gonzo / Kanam
**Origen:** cata de 8 roles x 5 clases de estres (`docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`)
**Relacionado:** ADR-090 (asignacion de modelos por rol), ADR-077/088/089 (pipeline A/B), ADR-076 (ningun agente hereda modelo local)
**Modifica:** ADR-090, seccion 1 (tabla de asignacion por rol) - el rol `main` pasa a `minimax-m3.1-flash:cloud`.

---

## Contexto

Ollama sumo `minimax-m3.1-flash` a su catalogo cloud (428B, 1M de contexto, `tools` +
`thinking` + `vision`). Gonzo lo propuso como candidato para el pipeline y decidio
que se lo evaluara **solo a el**: "queremos solo hacerle la cata a este modelo
minimax-m3.1-flash".

La pregunta no era "que puntaje saca" sino "**puede el CORE dejar de correr con
deepseek-v4.1-flash**". Un puntaje absoluto no se lee sin vara: se mide contra los
modelos que hoy ocupan los roles.

## Decision

**El CORE (`main`) y los defaults de agente pasan a `minimax-m3.1-flash:cloud`,
con `deepseek-v4.1-flash:cloud` como unico fallback.** Los demas roles no cambian.

Justificacion por rol (content corregido, escala 0-10):

| Rol | gpt-oss | deepseek | gemma4 | **minimax** | Veredicto |
|---|---|---|---|---|---|
| **main (CORE)** | 7.5 | 7.8 | 6.5 | **8.9** | **cambia** |
| dev | 6.4 | 7.0 | 7.4 | 6.7 | no |
| ops | 7.7 | 8.2 | 6.2 | 6.7 | no |
| mind | 5.0 | 8.7 | 6.0 | 8.6 | no (empate con coste) |
| studio | 7.9 | 9.4 | 6.7 | 9.0 | no |
| critic | 6.2 | 9.1 | 8.2 | 7.2 | no |
| auditor | 6.6 | 8.4 | 7.5 | 7.0 | no |
| planner | 5.9 | 7.5 | 5.1 | 7.1 | no |

El rol que cambia es **precisamente el que mejor le sale**: `main` 8.9 contra 7.8 del
motor vigente, con mejor desempenho en las tres clases que discriminan (restriccion
dura 7.4, la mejor de los cuatro; frontera humana 8.4; canonico 8.1) y 17 wins
absolutos sobre 40 celdas, mas que cualquier otro candidato.

**El resto de los roles no se tocan** porque alli minimax no supera al titular por
margen que justifique su costo operativo, y porque su modo de fallo (espiral de
thinking) es exactamente el que castiga a los roles de presion.

## Por que el CORE y no otro rol

El CORE **orquesta**: delega, verifica, sintetiza. Su costo por latencia no esta en
una ruta critica con otro agente esperando - quien espera es la persona. Los roles de
generacion (dev, critic, studio) si tienen ruta critica: el pipeline A/B espera al
agente que escribe, y 77s de mediana contra 3-14s de los titulares se paga en cada
iteracion.

## Ficha de capacidades (VERIFICADA 2026-10-20)

Fuente: `ollama show minimax-m3.1-flash:cloud` (API local 11434) y la pagina oficial
`https://ollama.com/library/minimax-m3.1-flash`.

| Atributo | Valor | Fuente |
|---|---|---|
| Arquitectura | `minimax-m3` (MoE, 428B) | `api/show` |
| Contexto | **1.000.000** tokens | `api/show` (`minimax-m3.context_length`) |
| Capacidades | `completion`, `tools`, `thinking`, `vision` | `api/show` |
| Tool calling | verificado: devuelve argumentos JSON validos | prueba directa 2026-10-20 |
| Parametro de thinking | `low` / `medium` / `high` / `max` (string) o `true`/`false` (bool) | `api/chat` 2026-10-20 |

**Advertencia operativa (medida):** **`think: false` NO apaga el razonamiento.** Tres
corridas con `think:false` devolvieron 463 / 134 / 193 caracteres de thinking. La
razonamiento es always-on por la via `/api/chat`; solo se puede acotar con
`think: "low"`. Consecuencia: el thinking se factura como output y no hay forma de
pagarlo por debajo.

## Riesgos y mitigaciones

1. **Espiral de thinking / fallo de entrega.** En la primera pasada, 7 de 40 celdas
   de minimax devolvieron 0 caracteres de entrega con 44k-56k caracteres de
   razonamiento. Con `num_predict` x2 se recuperaron 6; **1 quedo irrecuperable en 3
   intentos consecutivos** (`ops-D1`: 100k de thinking, sin entrega).
   *Mitigacion:* el CORE no es un rol de produccion con SLA de entrega, y su fallback
   (`deepseek-v4.1-flash:cloud`) cubre el caso. *Vigilancia:* si aparecen vacios en
   el CORE, el sintoma es thinking quemado, no logica.

2. **Latencia.** Mediana 77s por celda contra 3-14s de los titulares; 35x el mas
   rapido en el computo agregado de la cata.
   *Mitigacion:* aceptada por rol (el CORE espera a la persona, no a un pipeline).

3. **Costo.** No se midio: `ollama.com/pricing` no expone tabla en HTML estatico.
   Gonzo: "hasta el 22 a las 23.59 M3.1 Flash sera gratis, no preocuparse por el
   precio; igual nunca usamos el precio". Con el costo en cero, la objecion no aplica
   en esta ventana. *Pendiente:* reevaluar si la gratuidad termina y el rol se
   mantiene.

## Regla de mantenimiento (misma que ADR-090)

Al cambiar un modelo por rol, las **cuatro** fuentes deben coincidir:

1. `~/.openclaw/openclaw.json` (`agents.entries.main.model`, `agents.defaults.model`)
2. `settings` de `memory.db` (`model_primary`, `model_by_agent`) via
   `scripts/managed-blocks.py set ...`
3. Bloques gestionados (`AGENTS.md` `model-operativo`, `docs/SETUP.md` `model-triple`)
   via `scripts/managed-blocks.py apply`
4. Este ADR y ADR-090

Verificacion: `python3 scripts/managed-blocks.py check` (sin drift) y
`python3 scripts/check-single-source.py` (un dato, un dueno).

**Estado al 2026-10-20:** las cuatro fuentes coinciden, verificado.

## Evidencia

- Informe de cata: `docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`.
- Bateria congelada (los 40 prompts): `docs/ecosystem/cata-minimax-m31-flash-2026-10-20-battery.py`.
- Artefactos crudos (160 registros con `prompt` + `content` + `thinking` separados, y los
  40 veredictos de juez): `playground/model-cata-2026-10-20/` (1.7 MB, fuera de git por
  politica de `playground/`; se regeneran con `run-battery.py` + `judge-battery.py`).

## Lektion de la cata (metodologia, reutilizable)

**Los 2 jueces ciegos fallaron la clase "premisa falsa".** En `main-C1`, gpt-oss
obedecio la regla falsa declarada en el prompt y el juez le dio 6.0 (el mejor
puntaje); minimax detecto la contradiccion y freno (que es lo correcto) y recibio
5.0. Se detecto leyendo los artefactos, no confiando en el score.

*Resolucion:* las clases "premisa falsa" y "fuera de rol" se re-puntuaron **a mano,
celda por celda, leyendo cada artefacto**; los jueces ciegos quedaron para las clases
canonica, ambigua y de restriccion.

*Conclusion:* la evaluacion de comportamiento (obedecer o frenar ante una premisa
falsa) **no es una tarea de prosa**: un juez LLM puede fallarla igual que el modelo.
El judge's score es evidencia, no veredicto.

## Pendientes con fecha

- **Re-cata con K3 como juez:** cancelada por Gonzo (2026-10-20) - costo de recursos
  desmedido para el beneficio. Los 160 registros quedan disponibles si se decide
  revertir.
- **Validacion en uso real:** 2 semanas de uso del CORE con minimax antes de dar el
  rol por cerrado. Fecha de corte: 2026-11-03.
- **Costo real:** reevaluar si la gratuidad hasta el 2026-10-22 23:59 cambia el
  balance. Fecha: 2026-10-23.

## Artefactos

- Config runtime: `~/.openclaw/openclaw.json` (backup previo:
  `~/.openclaw/openclaw.json.bak-20261020-1526-m31-core`).
- Bloques gestionados: `scripts/managed-blocks.py` -> `AGENTS.md`, `docs/SETUP.md`.
- Informe de cata: `docs/ecosystem/cata-minimax-m31-flash-2026-10-20.md`.
- ADR-090: seccion 1 actualizada el 2026-10-20 con esta asignacion.