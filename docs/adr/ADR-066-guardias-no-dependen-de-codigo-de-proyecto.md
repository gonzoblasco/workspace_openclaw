# ADR-066: los guardias del workspace no leen codigo de proyectos

**Fecha:** 2026-09-24
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** workspace (25 runs de CI en rojo el 2026-09-24; el log lo compartio Gonzo)
**Relacionado:** ADR-065 (DB-first vs doc-only), ADR-062 (vectores), regla de triple git en `AGENTS.md`

---

## Contexto

El 2026-09-24 la suite `pytest tests/python/` del workspace quedo en rojo y **estuvo 12 runs seguidos sin que nadie lo mirara**. Los logs que llego Gonzo mostraban 12 fallas, todas de `tests/python/test_contrast.py`, con la misma causa:

```
FileNotFoundError: .../projects/kanam-os/app/globals.css
```

El diagnostico completo, con evidencia:

- **Verde local, rojo en CI.** En la maquina de desarrollo `projects/kanam-os/` esta clonado y el archivo existe. En CI el checkout solo trae lo versionado.
- **El archivo no esta versionado a proposito.** `AGENTS.md` (triple git) y `.gitignore` establecen que el workspace trackea **solo** `projects/<slug>/.knowledge/`. El codigo de cada proyecto vive en su propio repo. Verificado: `git ls-files projects/kanam-os` devuelve unicamente los dos `.knowledge/`. El checkout de CI tiene el directorio vacio.
- **El pre-commit hook no lo puede ver.** `scripts/pre-commit.template` corre `pytest` cuando cambian `scripts/` o `skills/`. Como localmente el archivo existe, el hook pasa siempre. Da **confianza falsa**: es el mismo patron que este workspace ya registro dos veces (una auditoria de contraste que comparaba claves `--` contra claves sin `--` y reportaba "0 fallas"; un check de refs que no veia la direccion inversa).
- **Los commits que lo empujaron no tenian relacion.** Los 12 runs rojos se empujaron como `memory:`, `docs:` y `chore:`. Nadie corrio la suite porque "solo cambie documentacion".

El detonante fue un test agregado el mismo dia (`a6130988`, 12:14): el guardia de contraste de kanam-os nacio leyendo la ruta del CSS real. Es un guard **correcto en su logica** y **estructuralmente incapaz de correr fuera de esta maquina**.

### El mismo dia, segunda falla, misma familia

`docs/LANGCHAIN_STRATEGY.md` citaba los cuatro scripts del starter (ingest, store, query y agent) sin el prefijo `projects/langchain-starter/`. `check-refs.py` los marcaba rotos con razon: esas rutas no existen en el workspace. Se corrigio a la forma calificada en `bc060729`. **Pero la correccion reabre el problema de fondo:** una ruta que apunta a codigo no versionado existe solo en la maquina que tiene el proyecto clonado, asi que un test que exija su existencia es localmente verde y remotamente rojo.

---

## Decision

**Ningun chequeo ni test del workspace lee codigo de proyectos como fuente de verdad.**

### 1. Los tests del workspace prueban la logica, con un fixture versionado

`tests/python/fixtures/kanam-os-themes.css` es el **contrato de temas**: una paleta valida de dos temas, siempre disponible en el checkout. Los 12 tests de `test_contrast.py` corren contra el fixture, sin depender de ningun clon.

Esto no debilita la cobertura: los tests que importan son los que prueban que el guard **PUEDE fallar** (mutation tests), y eso es logica pura sobre un CSS valido. Un mutation test no necesita la paleta vigente; necesita una base que cumpla y una mutacion que no.

### 2. Un test anti-deriva, opt-in por presencia

`test_fixture_no_deriva_del_css_real` importa el CSS real **solo si esta clonado** (`skipif`), y compara **claves, no valores**. En la maquina de desarrollo vigila que el fixture no quede viejo; en CI se saltea y no rompe nada.

Se comparan claves y no valores a proposito: una clave que desaparece rompe la logica del guard (hay que reflejarla), mientras que un valor distinto solo significa que la paleta se retoco, y de esa paleta responde su propio repo.

### 3. El guard de la paleta real vive donde vive la paleta

`scripts/check-contrast.py` **queda en el workspace**: es del ecosistema y sirve para auditar cualquier paleta (incluido el fixture). Lo que no vive aca es el test que afirma "la paleta de kanam-os cumple": ese pertenece al repo `kanam-os`, que es el unico que puede ver su `globals.css`.

**Pendiente registrado:** montar ese check en `projects/kanam-os/` (con su CI o su pre-commit). Mientras tanto, la paleta real no tiene guard automatico en ningun lado, y eso es deuda declarada, no un olvido.

### 4. Regla general

Antes de escribir una ruta o un test, preguntar: **¿esta ruta existe en un checkout limpio del repo?**
- Si apunta a codigo de un proyecto: **calificarla** con `projects/<slug>/` (es trazabilidad, no una promesa de existencia) y **no** exigir su existencia por test.
- Si es un artefacto que el guard necesita como valor: **fixture versionado**.
- Si el guardia es del proyecto: **vive en el repo del proyecto**.

---

## Consecuencias

### Positivas
- La suite deja de depender del estado de la maquina: **verde local y verde en CI significan lo mismo**. Verificado en un checkout limpio de `HEAD` sin `projects/kanam-os/`: 187 tests, 1 skip, 0 fallas.
- El anti-deriva conserva el valor del guard en la maquina que si tiene el proyecto, sin romper CI.
- El patron queda registrado: el workspace ya tiene el precedente de un guard que daba falsa confianza, y este es la misma familia.

### Negativas
- **El fixture puede quedar viejo.** Mitigado por el test anti-deriva, pero ese test se saltea justo donde mas importa (la maquina de desarrollo es la unica que lo corre, y es la que menos lo necesita).
- **La paleta real queda sin guard automatico** hasta que kanam-os monte el suyo. Es el pendiente de la Decision 3.

### Lo que queda fuera del alcance
- **No** se versiona el codigo de los proyectos en el workspace. Es la regla de triple git y este ADR no la toca.
- **No** se generaliza a los `.knowledge/`, que si estan versionados y si pueden citarse como ruta existente.

---

## Alternativas consideradas

1. **Marcar los tests con `skipif` y nada mas.** Rechazada: deja el guard de contraste sin correr en CI **y** sin correr al fixture, o sea sin ningun test de su logica en CI. La suite quedaria verde y vacia.
2. **Copiar `globals.css` al workspace y testear contra la copia.** Rechazada: es una segunda copia de la paleta que deriva en silencio. Es exactamente el error que el guard existe para evitar (colores escritos a mano que esquivan la validacion).
3. **Mover todo `check-contrast.py` + tests al repo kanam-os.** Rechazada **por ahora** como unica medida: perderia la capacidad de auditar cualquier paleta desde el workspace y duplicaria un guard generico en un proyecto. Es complementaria a esta decision, no alternativa (Decision 3).
4. **Detectar el error antes: que el pre-commit corra pytest siempre.** Parcial, y no alcanza: localmente el archivo existe, asi que el hook seguiria verde. La falla es del entorno, no del alcance del hook.
