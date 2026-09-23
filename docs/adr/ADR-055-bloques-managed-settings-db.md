# ADR-055: Bloques managed - settings de la DB propagados a documentos de identidad

**Fecha:** 2026-09-22
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** fase 3 de kanam-os; pedido de Gonzo - "hacer cambios globales sin tener que estar reconfigurando cada aplicacion y cada sesion"
**Relacionado:** ADR-038 (learnings con mirror en DB), ADR-050 (memoria en SQLite), ADR-053 (modelos), ADR-054 (kanam-os como app local)

---

## Contexto

ADR-038 cerro una regla: **los documentos narrativos puros** (`MEMORY.md`, `AGENTS.md`, `SOUL.md`, `USER.md`) **no se migran a la DB**. La DB es para datos estructurados con narrativa (todos, inbox, learnings, contributions).

Pero quedo un problema sin resolver, y Gonzo lo nombro con precision: **un valor global repetido en varios archivos se desincroniza solo**. Caso testigo encontrado mientras se construia esta fase:

- `AGENTS.md` decia: primario `deepseek-v4.1-flash:cloud`, thinking `high` (ADR-053).
- `docs/SETUP.md` decia: default `deepseek-v4-flash:cloud`, Kanam en thinking **`max`**, `thinkingDefault = "max"`.

Las dos afirmaciones no pueden ser ciertas. El config real (`~/.openclaw/openclaw.json`: `thinkingDefault: "high"`, default `deepseek-v4.1-flash:cloud`) confirma que **`SETUP.md` estaba stale**, contradiciendo a ADR-053 desde que se escribio. Nadie lo noto porque nadie compara archivos a mano.

Ese es el problema: **no es que falte una DB, es que falta un mecanismo que haga imposible el drift.**

---

## Decision

**Los valores globales viven una sola vez: en la tabla `settings` de `memory.db`. Se propagan a bloques delimitados por marcadores dentro de los archivos.**

```
memory.db (tabla settings)  ->  scripts/managed-blocks.py  ->  bloques en archivos
```

```markdown
<!-- BEGIN MANAGED:model-triple -->
- **Modelo primario:** `deepseek-v4.1-flash:cloud`. **Auxiliar:** `gemma4:cloud`. ...
<!-- END MANAGED:model-triple -->
```

### Reglas del mecanismo (duras)

1. **Solo se reescribe lo que esta ENTRE marcadores.** Todo el texto de afuera queda intacto, byte a byte. Esto es lo que lo hace compatible con ADR-038: el documento sigue siendo narrativo y curado a mano; solo un bloque adentro es generado.
2. **Si faltan los marcadores, no se inserta nada.** El script reporta y muestra el snippet exacto para pegar. **Nunca adivina donde va.** Los documentos de identidad no se tocan sin intervencion explicita.
3. **Idempotente.** Aplicar dos veces no cambia nada la segunda vez.
4. **Dos pasos, siempre.** Cambiar un valor (`set`) solo toca la tabla `settings`. Aplicar a los archivos (`apply`) es una operacion separada, que soporta `--dry-run` y muestra el diff.
5. **El registro de bloques es una lista explicita** (`REGISTRY` en el script): archivo + clave + plantilla. Agregar un bloque nuevo es agregar una entrada, no tocar logica.

### Frontera con ADR-038 (la parte delicada)

ADR-038 sigue vigente: estos documentos **no se migran a la DB**. Lo que cambia es que ahora **pueden contener un bloque generado**. La distincion es concreta:

| | Narrativa pura (ADR-038) | Bloque managed (este ADR) |
|---|---|---|
| Contenido | prosa, criterio, historia | valor unico y verificable |
| Se edita | a mano | nunca (lo mantiene el script) |
| Si se desincroniza | es interpretacion, no error | es un bug |

Un valor que aparece en 3 archivos y se contradice es un dato mal modelado; la prosa alrededor no.

---

## Consecuencias

### Positivas
- **Un solo lugar para cada valor global.** Cambiar el modelo o el thinking es `set` + `apply`, no una caceria por archivos.
- **El drift se vuelve detectable:** `managed-blocks.py check` reporta el desvio sin escribir nada.
- **Ya pago:** al construir esto aparecio la contradiccion `SETUP.md` vs ADR-053. Se resolvio sin editar a mano: se inserto el bloque y la linea vieja se preservo marcada como historica.
- **Sirve a lo que Gonzo pidio:** el cambio se propaga a `AGENTS.md`, `docs/SETUP.md` y (cuando se registren) los `.knowledge/` de cada proyecto, sin reconfigurar cada sesion.

### Negativas
- **Introduce marcadores HTML en archivos markdown.** Son invisibles al render, pero son ruido en el fuente. Aceptado: sin marcadores no hay forma segura de saber que parte es generada.
- **Un script mas que puede escribir documentos de identidad.** Mitigado por las reglas 1, 2 y 4, y por 9 tests que cubren idempotencia, no-tocar-el-resto y no-adivinar.
- **El registro es manual.** Un archivo nuevo con bloque necesita su entrada en `REGISTRY`. Es deliberado: prefiero eso a un descubrimiento automatico que escriba donde no debe.

---

## Alternativas consideradas

1. **Editar los archivos a mano cuando cambia un valor.** Es lo que se hacia, y produjo el drift de `SETUP.md`. Rechazado: el problema es el proceso, no la herramienta.
2. **Generar los archivos completos desde la DB.** Rompe ADR-038 (la narrativa no se genera) y borraria criterio escrito a mano. Rechazado.
3. **Un solo archivo fuente sin marcadores.** Requiere un parser de markdown que sepa que linea es que valor: fragil y peor que un marcador explicito. Rechazado.
4. **Insertar los marcadores automaticamente si faltan.** Un script adivinando donde va un bloque en `AGENTS.md` es exactamente el tipo de automatizacion que no quiero. Rechazado por diseno.

---

## Implementacion

| Pieza | Path |
|---|---|
| Mecanismo | `scripts/managed-blocks.py` (`list`, `seed`, `set`, `check`, `apply [--dry-run]`) |
| Tabla | `settings` en `memory/memory.db` (key, value, description, updated_at) |
| UI | `projects/kanam-os/app/settings` (cambiar valor + ver diff + propagar) |
| Tests | `tests/python/test_managed_blocks.py` (9 tests) |
| Primer bloque | `model-triple` en `AGENTS.md` y `docs/SETUP.md` |

## Referencias

- ADR-038: la regla que este ADR respeta y calibra
- ADR-054: kanam-os, donde vive la UI del mecanismo
- Leccion de la clase de bug: un valor repetido en dos archivos sin sincronizar no falla solo, miente hasta que alguien lo compara
