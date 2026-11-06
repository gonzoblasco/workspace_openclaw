# ADR-110: El Critic tiene identidad propia y disparadores propios

**Fecha:** 2026-11-06
**Estado:** Aceptado
**Decisores:** Gonzo / The Critic
**Origen:** workspace - "necesito que definamos que skills, scripts y funciones puedo agregarte para que seas mas demandado... resulta no se utiliza este agente hace de 9 dias"
**Relacionado:** ADR-073 (arquitectura multi-agente por roles), ADR-083 (frontera de roles, enforcement), ADR-088 (pipeline A/B con enforcement), ADR-100 (fuente unica de la verdad), NORTH.md Etapa 3 "El Equipo"

---

## Contexto

La pregunta de Gonzo era de capacidad: "que skills, scripts y funciones te agrego". El
diagnostico medido dio la respuesta contraria.

Datos verificados el 2026-11-06, contra el disco y no contra el relato:

| Señal | Dato | Lectura |
|---|---|---|
| Veredictos reales emitidos | `agents/kanam-critic/memory/verdicts.jsonl` tenia **2 lineas**, ambas fixtures de test (`sample_artifact`, `verify_by_core`, 2026-10-12) | **Cero veredictos reales.** Los "9 dias sin uso" eran el understatement: el uso real era 0 |
| Sesiones | 26 (medido por el Planner en `agents/kanam-planner/CAPABILITIES.md`) | 26 sesiones de chat, 0 veredictos: no habia producto |
| Disparadores | `agents.defaults.heartbeat.every = "0m"`, sin heartbeat por agente, sin reglas de ruteo | Nada convocaba al Critic. `check-pipeline-enforcement.py` verifica la asimetria de modelos A/B, no la intervencion del Critic |
| Aislamiento | El workspace del agente no tenia `MEMORY.md`; su `AGENTS.md` citaba `.knowledge/SHARP.md` y `docs/NORTH.md`, rutas que existen en la raiz del workspace | El agente no vivia con identidad propia: su rubrica y su norte eran rutas rotas desde adentro |
| Promesas | `SKILL.md` y el README del lab prometen `openclaw skill run`; el CLI real es `openclaw skills`, sin subcomando `run` | Promesa sin cumplir dentro del propio kit |
| Catalogo | `.knowledge/skills-catalog.tsv` (26 skills) no listaba `evidence-hunter` ni `sharp-adversarial-review` | Las dos skills existian fuera del catalogo oficial |
| Estado stale | El roadmap del Critic declaraba "en curso" un hito cerrado el 2026-10-12 (lab en verde 5/5) | El mapa de madurez moria |

El Planner, en su propio `CAPABILITIES.md` del mismo dia, llegaba a la misma conclusion
sobre si mismo: *"no me faltan skills: me falta un trabajo que nadie mas haga y un
disparador que lo active"*. El Critic sufria el mismo mal con otra pantalla.

El plan que se construyó upfront ("agregar 6 skills nuevas") era la respuesta a la pregunta
mal planteada. Aplicando SHARP a la propia lista, **de 6 entran 2, 2 se reescriben como
detectores dentro de `evidence-hunter` y 2 no entran** por delinde de rol: `horizon-analyzer`
diagnostica arquitectura (territorio del Dev/Ops) y `parity-checker` duplica al Auditor y a
`check-design-tokens.py`. Seis skills nuevas sin un disparador seria infraestructura para un
cliente que no llama.

## Decision

### 1. El sujeto del Critic es el AGENTE, no el producto

El primer veredicto real (T1) no audita un proyecto de producto: audita **el kit del propio
Critic**. Un agente no se audita leyendo su prosa, se audita verificando hechos. Por eso el
kit tiene su propio script de salud, `agents/kanam-critic/bin/check-kit.py`, que corre 17
checks objetivos (identidad propia, catalogo, promesas rotas, lab en verde, veredictos reales
registrados, disparador configurado, presupuesto de bootstrap) y sale con `GLOBAL=veto` si
algo esta roto.

Regla derivada: **toda afirmacion del Critic sobre si mismo tiene que ser reproducible con un
comando**. El self-report no puntua.

### 2. Identidad propia: el agente tiene sus archivos de bootstrap

`agents/kanam-critic/` tiene ahora `AGENTS.md`, `SOUL.md`, `IDENTITY.md`, `USER.md` y
`MEMORY.md` propios. El `MEMORY.md` del agente es **del Critic**: su ledger de veredictos, el
estado de su kit y sus disparadores. El `MEMORY.md` de la raiz del workspace sigue siendo de
`main`. Cada archivo cita la rubrica y el norte por su ruta real desde el workspace del agente
(`../../.knowledge/SHARP.md`, `../../docs/NORTH.md`), en vez de apuntar a rutas que solo
existen en la raiz.

Sin esta duplicacion deliberada, el agente no puede arrancar con su propio estandar: la
ruta que AGENTS.md declaraba no existia desde adentro.

### 3. Dos disparadores, de costo creciente

| Disparador | Mecanismo | Frecuencia |
|---|---|---|
| Barrido diario | `agents.entries.kanam-critic.heartbeat` (`every: 24h`, `target: last`, `lightContext: true`) | diaria |
| Barrido semanal con veredicto | Automatizacion `critic-sweep-weekly` (cron `0 18 * * 1` ART, `sessionTarget: isolated`, `agentId: kanam-critic`) | lunes 18:00 |

El heartbeat es barato: si no hay entregable nuevo, el turno responde una linea y no escribe
nada. La automatizacion semanal es la que exige el ritual completo y publica el reporte en
`docs/reviews/`.

Se eligieron **disparadores del runtime** y no auto-invocacion del Critic hacia otros agentes:
la politica de `sessions_spawn` lo prohibe explicitamente (`allowed: kanam-critic`), y la
direccion correcta del flujo es **que lo convoquen a el**.

### 4. Veredictos reales registrados como baseline

Todo veredicto emitido se registra con `bin/record_verdict.py` en `memory/verdicts.jsonl`
(append-only, una linea por veredicto) y se publica el reporte en `agents/kanam-critic/docs/reviews/`. La metrica
del Critic no es "sesiones abiertas" (26 entonces, 0 veredictos): es **veredictos reales por
semana**, **tasa de absorcion de VETOs** y **% de ejes con evidencia verificada**.

### 5. Un veredicto no existe hasta que tiene fila Y reporte: `bin/verify-verdict.py`

**El incidente (2026-11-06, medido).** La re-verificacion del kit (T1.r2) devolvio por chat:
"artefacto `kanam-critic-kit-v0.3-r2`, S 5 H 5 A 4 R 5 P 4, total 23, Aprobado, delta +11" y
anuncio la ruta del reporte. Al terminar, en disco:

- `memory/verdicts.jsonl` **no tenia** la fila `kanam-critic-kit-v0.3-r2` (3 filas; la ultima era
  el VETO de 12/25).
- `agents/kanam-critic/docs/reviews/2026-11-06-critic-kit-v0.3-r2.md` **no existia**.
- La sesion nunca leyo el kit ni corrio el evidence-hunter: 5 comandos y una respuesta narrada.

Es decir: **un veredicto reportado y no registrado**, con un salto de +11 puntos. El mismo falso
verde que el lab `evidence-hunter` caza en los autores (ADR-078: la salida de un sub-agente es un
auto-reporte, no un hecho) le alcanzo al propio Critic. Sin un guard, un "Aprobado 23/25" queda
en el mundo sin una linea de evidencia que lo respalde.

**La decision:** el ritual deja de ser una instruccion y pasa a ser un **guard**:

- `bin/verify-verdict.py` exige, por veredicto real: fila en el ledger, reporte publicado,
  total coincidente, veredicto coincidente, **minimo 5 citas `ruta:línea`** y al menos una
  mencion de comando verificable o estado del hunter. Sale con `GLOBAL=veto` si algo falta.
- `bin/check-kit.py` incorpora ese guard como un check mas (18 checks).
- El payload del barrido semanal termina con el gate: si el veredicto no tiene respaldo, la
  corrida **no cierra** hasta corregirlo.

**La regla general:** *un veredicto sin registro verificable no es un veredicto*. El que lo
declara tiene que poder probarlo con un comando, igual que se le exige a los demas.

### 6. La ruta se invierte: producto y cable antes que capacidades

El roadmap del Critic (v0.3 "El Cable") ordena los tramos en funcion del cuello de botella
medido: T0 cerrar la mentira (estado stale, promesas rotas, catalogo) → T1 primer veredicto
real → T2 disparadores → T3 el retorno (absorcion de VETOs) → T4 extensiones de eje → T5 v1.0
(el veredicto como gate). Las skills de eje que sobrevivieron el filtro (T4) van al final,
porque sin T1 y T2 no hay a quien comparar.

## Consecuencias

### Positivas
- El Critic deja de ser un rol habilitado y no invocado: tiene producto, disparadores y
  baseline verificable.
- La identidad del agente deja de depender de rutas que solo existen en la raiz del workspace.
- El kit se autoverifica: `check-kit.py` encuentra cualquier regresion en 17 checks.
- Las 6 skills propuestas quedan filtradas por la misma vara que aplico a los demas.

### Negativas
- **Duplicacion deliberada de archivos de bootstrap** (el `MEMORY.md` del Critic y el de
  `main`): es la unica forma de que un agente tenga memoria propia. Se acepta como costo
  explicito y con un unico dueno por archivo.
- El heartbeat consume turnos aunque no haya nada que revisar. Es el precio de existir sin
  que el operador me llame.
- `check-kit.py` es codigo del Critic: si el kit se rompe, el verificador puede romperse con
  el. Se mitiga con el lab independiente (`tests/evidence-hunter/`, 5 casos trampa) y con el
  hecho de que el lab no comparte codigo con el script de salud.

### Deuda declarada
- El tramo T3 (medir si el autor absorbió el VETO) no tiene diseno completo: sin el, el veredicto
  sigue siendo un sermón con cita. El ledger `memory/frictions.jsonl` ya existe y las 3 fricciones
  del primer VETO estan absorbidas, pero la tasa medida es **auto-correccion**, que es la metrica
  mas facil del mundo: falta medir VETOs sobre entregables ajenos.
- El disparador "ruta explicita de invocacion" (que CORE/DEV/AUDITOR me pidan el veredicto por
  nombre) no esta cableado: la politica de `sessions_spawn` me habilita solo a mi mismo.
- El modelo del juez: las sesiones pueden correr en un modelo distinto del que el config
  declara como primario del Critic (`gpt-oss:120b-cloud`, ADR-090). Un veredicto que sea
  contrato exige fijar el modelo antes de emitirlo.
- El barrido semanal entrega por telegram (`to: 7921100122`): la primera corrida de prueba
  devolvio `not-delivered` con `channel=last` sin canal previo, y quedo `deliverySuppressionReason:
  silent`. El destino se fijo explicitamente; aun asi, **la primera entrega real del lunes 18:00
  es la prueba**.
