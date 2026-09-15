# STATUS - kanam-fixer

**Actualizado:** 2026-09-15
**Ciclo:** 0.0.1 **CERRADO**. Decision: no abrir `0.0.2` todavia (depende de S3, que depende de upstream).

## Donde estamos

| Slice | Estado | Evidencia |
|---|---|---|
| S1 - Esqueleto y decisiones | **Completado** | Commit `6044856`. Terna en verde, hook activo. |
| S2 - La asercion, solo virtual | **Completado** | Commit `fb931ea`. 7 tests. Criterio de salida verificado. |
| S3 - VoiceOver real en local | **Bloqueado por upstream** | Commits `b98bf1b` + `a080a27`. Reportado en guidepup/guidepup#149. |
| S4 - El caso testigo (#4109) | **Completado - NO reproduce** | Commit `5090278`. 8 tests. Hallazgo abajo. |
| S5 - Cierre del ciclo | **Completado** | Commit `88ca9ff`. README con la evidencia + `HANDOFF.md`. |

**Repo publico:** https://github.com/gonzoblasco/kanam-fixer (`88ca9ff`). Verificado que `.knowledge/` no se filtra.
**Terna:** 17 passed, 4 skipped (los 4 son el plano real, con su causa impresa).

## S5: el cierre del ciclo

- **README reescrito para abrir por lo que el ciclo ENCONTRO**, no por la promesa. Tabla de que clases de bug captura el plano virtual (atributos: si, con las frases observadas) y cuales no (timing y viewport). El caso testigo quedo etiquetado como **hueco del ecosistema**, no como demostracion de que esta herramienta lo cubra.
- **Corregido un ejemplo enganoso:** el README mostraba `import from 'kanam-fixer'` como si fuera instalable, cuando el paquete es `private: true` y no esta en npm (verificado: 404).
- **ADR-0002 actualizado:** las filas de la matriz ya no dicen "Previsto en S3". La version del plano real **la determina el asset que Guidepup publique** para la plataforma del host: dependencia dura, ahora hecho medido.
- **`HANDOFF.md` nuevo:** donde vive cada cosa, el blocker y como se cierra, la trampa de debugging, las decisiones tomadas y lo que no hay que hacer.

### La decision sobre 0.0.2

**No se abre todavia.** Y la razon es concreta, no una postergacion: el siguiente paso del proyecto depende de **S3**, y S3 depende de que Guidepup publique un asset para Darwin 27. Abrir `0.0.2` hoy seria invertir sobre la parte que resulto **mas fragil** sin resolverla primero.

---

## S4: el caso testigo - RESULTADO NEGATIVO

**El plano virtual NO reproduce el caso #4109/#4110.** Eso es el resultado, no un fracaso del slice: el ROADMAP dice que `0.0.1` prueba la apuesta y que si no se sostiene se descarta antes de invertir mas.

### El caso real (leido de los issues, no de memoria)

- **#4109** agrego `aria-posinset`/`aria-setsize` calculados a `Select.Item`. Los atributos quedan correctos y los tests unitarios pasan.
- **#4110** (abierto) reporta que, sin valor preseleccionado, la **primera opcion no anuncia nada** con VoiceOver + Chrome: carrera de timing, mas un total que el browser deriva de las opciones **visibles en el viewport**.

### Lo que verifique, con sondas discriminantes

No lo asumi: lo medi. Tres experimentos, cada uno con una prediccion distinta:

| Experimento | Resultado observado | Que significa |
|---|---|---|
| Atributos **ausentes** | Anuncia igual `position 1, set size 4` | **Deriva la posicion de la estructura.** No detecta la regresion que #4109 arreglo. |
| Atributos **deliberadamente erroneos** (`9` de `99`, en una lista de 4) | Repite `position 9, set size 99` | Refleja **la declaracion**, no la verdad. |
| Atributo aplicado **tarde** vs **nunca** | Salida **identica** | **No hay momento de anuncio** contra el cual correr una carrera. |

Las dos causas reales viven en el lector real y en el browser: un total derivado del viewport, y una carrera en el momento del anuncio. Un driver que camina el arbol de accesibilidad **una vez** no tiene ninguna de las dos.

### El hallazgo mas importante (y el mas incomodo)

El tercer experimento dice algo que va mas alla de S4: **el plano virtual puede dar un falso verde** en esta clase de bug. Un test virtual puede pasar mientras el lector real anuncia mal.

Eso no invalida S2: la asercion **si** ve los bugs de **atributos y composicion** (lo demostro con `aria-pressed`, `aria-label` y el nivel de heading). Lo que no ve son los de **timing y derivacion del viewport**.

**Corolario:** el plano real (S3) no es un lujo ni un extra de cobertura. Es la unica forma de cubrir esa clase. Es decir: **S4 refuerza la necesidad de S3**, en vez de restar valor al proyecto.

### Por que los tests quedaron, si el resultado es negativo

El suite de S4 es un **test de caracterizacion**: fija el comportamiento observado del driver para que la razon no se pierda ni se vuelva a adivinar. Si alguien retoma el proyecto en tres meses, encuentra escrito por que el caso testigo no se reproduce aca, con los numeros.

---

## S3: el plano del lector real - BLOQUEADO POR UPSTREAM (no por permisos)

> **Correccion de diagnostico (2026-09-15).** El registro anterior atribuia este blocker a **permisos de macOS faltantes**. **Era incorrecto.** Se deja escrito el error y su correccion, no solo el resultado final.

### La causa real

`screenReader.start()` falla con `VoiceOver cannot be started`, pero ese mensaje **oculta un cause anidado**:

```
VoiceOver cannot be started
  cause: Error: macOS version not supported
```

Guidepup busca la version mayor de Darwin (`os.release()`) en su `manifest.json` y lanza si no hay asset para esa plataforma.

| Este equipo | Guidepup 0.34.0 (latest) |
|---|---|
| macOS 27.0, **Darwin 27** | `platformVersions`: **21, 22, 23, 24, 25** |

Confirmado por el CLI: `npx @guidepup/setup install voiceover` -> `The requested screen reader asset is not available for this platform: VoiceOver on darwin 27`. Verificado tambien contra `main` upstream: tampoco tiene 26 ni 27.

### Los permisos NO eran el problema (verificado)

- El paso de **VoiceOver Utility** esta **hecho**: `/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled` existe con `a` (creado hoy 10:39).
- El **control por AppleScript funciona**: `osascript -e 'tell application "VoiceOver" to activate'` arranco VoiceOver. El binario arranca y se controla.
- `detect()`/`.default()` dan `true` porque VoiceOver **esta instalado**; eso nunca probo que Guidepup pudiera manejarlo.

### Lo que quedo construido (y sigue valido)

- **`ReaderDriver`**: contrato propio (ADR-0001). `virtualDriver` (CI) y `realDriver` (VoiceOver) lo implementan, asi que **la misma asercion corre en los dos planos**.
- **`expectAnnouncement(container, expected, { driver })`**: el driver es opcional; el default sigue siendo el virtual.
- **`realReaderAvailability()`**: arranca y para el lector una vez, para que el llamador pueda **saltear con la razon real** en vez de reportar un falso verde.

**El codigo esta listo; lo que falta es cobertura de un tercero.** Cuando Guidepup publique el asset de Darwin 27, S3 se cierra corriendo el test, sin cambiar nada de lo escrito.

### Consecuencia para el proyecto

S3 **no depende de Gonzo, depende de upstream.** Y materializa el riesgo que **ADR-0001** anticipo como el mas duro: *"el plano real es el lado mas dificil de reemplazar"*. Ya no es advertencia teorica: el driver virtual corre en cualquier SO; el real exige un asset para la version exacta del sistema.

### Opciones (estado: 1 tomada, 2 descartada, 3 abierta)

1. **Reportar el hueco upstream** **HECHO (2026-09-15):** issue https://github.com/guidepup/guidepup/issues/149, abierto.
2. **Correr el plano real en otra maquina** con macOS soportado (Darwin 21-25). **DESCARTADA (2026-09-15):** todas las maquinas de Gonzo corren macOS 27. No hay segunda maquina aprovechable.
3. **Declarar la limitacion** en la matriz de ADR-0002 y dejar S3 documentado como bloqueado por upstream. Sigue siendo la opcion de respaldo.

### Advertencia que sigue en pie: `@guidepup/setup setup`

Escribe directo en la base de privacidad del sistema (`TCC.db` via `sqlite3`), con lista de clientes ajena al proyecto (`sshd`, `bash`, `zsh`, `osascript`, Terminal, System Events, navegadores). **No ejecutarlo.** En este caso ademas no habria servido: el bloqueo es un asset faltante, no un permiso.

**Nunca desactivar SIP** (verificado: sigue `enabled`). El maintainer de setup reporto (`guidepup/setup#66`) que en macOS 26 el marcador solo se escribe con SIP desactivado, y que escribirlo como root falla igual.

---

## S1: esqueleto y decisiones

- **Stack:** TypeScript (`nodenext` ESM), Biome 2.5, Vitest 5, build con `tsc`, pre-commit hook (`simple-git-hooks`).
- **Dependencias:** `@guidepup/virtual-screen-reader` (driver virtual), `jsdom` para el DOM en tests, `@guidepup/guidepup` y `@guidepup/playwright` para el plano real.
- **ADR-0001:** capa propia fina sobre Guidepup; su API nunca es el contrato publico. Incluye que pasa si Guidepup desaparece.
- **ADR-0002:** la matriz de lectores (lector x version x SO) se declara desde el dia uno.
- **README:** abre por el problema, no por la feature.

## S2: la asercion sobre el anuncio (driver virtual)

- **`expectAnnouncement(container, expected)`** - recorre el contenedor con el lector y compara la secuencia de frases habladas, en orden.
- **`readAnnouncements(container)`** - la observacion cruda, para que un fallo pueda mostrar que se anuncio de verdad.
- **La matriz viaja con el resultado** (ADR-0002), y su version se lee del paquete instalado en vez de escribirse a mano.
- **7 tests**, incluidos 3 de mutacion mas uno que verifica que TODAS las mutaciones fallan.

### Criterio de salida de S2: verificado

| Variante | Correcto anuncia | Roto anuncia |
|---|---|---|
| Sin `aria-label` en el grupo | `group, Channels` | `group` (sin nombre) |
| Sin `aria-pressed` | `button, Email, pressed` | `button, Email` |
| Heading reemplazado por contenedor con label | `heading, Notification settings, level 1` | `Notification settings` (sin nivel) |

Los tests de mutacion matchean contra **lo que el lector anuncia**, no contra la lista esperada que el mensaje de error repite (esa version debil habria pasado por cualquier mismatch).

**Dato que vale registrar:** la segunda fila es la clase de bug del PR #9879 en ibm-products (`aria-pressed` hace que VoiceOver anuncie un toggle). El driver virtual **si** lo detecta.

## El hook hizo su trabajo en todos los slices

- **S1:** bloqueo el primer commit. Biome encontro 2 errores en `dist/`.
- **S2:** `tsc` fallaba por tipos faltantes (`Node` del DOM, `node:module`) y Biome por un import sin usar.
- **S4:** Biome por un import sin usar y el orden de imports.

En los tres casos freno un commit que no estaba limpio.

---

## Proximo paso

**El ciclo 0.0.1 esta cerrado. No se abre `0.0.2` todavia.** La razon es concreta: el siguiente paso del proyecto depende de **S3**, y S3 depende de que Guidepup publique un asset de VoiceOver para Darwin 27. Invertir sobre la parte que resulto mas fragil, sin resolverla primero, es exactamente lo que el ciclo `0.0.1` existia para evitar.

### Cuando se destraba

| Evento | Que pasa |
|---|---|
| Guidepup publica el asset de Darwin 27 | Correr `npm test`. Los 4 skips se vuelven tests reales. **Sin cambiar codigo.** Ese es el cierre de S3. |
| ~~Correr el plano real en una maquina con Darwin 21-25~~ | ~~Igual: `npm test` y los skips se activan.~~ **Descartado (2026-09-15):** todas las maquinas de Gonzo tienen macOS 27. |
| Gonzo decide no esperar a upstream | Abrir `0.0.2` declarando la limitacion en la matriz (ADR-0002) y apoyarse en el plano virtual **solo** para bugs de atributos. |

### Lo que el ciclo dejo claro

- **Se sostiene** para bugs de **atributos y composicion** (S2, con las frases observadas).
- **No se sostiene** para **timing y derivacion del viewport** (S4), y ahi el plano virtual puede dar **falsos verdes**.
- **La apuesta sigue en pie, invertida:** el valor no esta en el virtual como sustituto, sino en el **real como unico juez** de esa clase, con el virtual como red barata para lo demas. S3 pasa de "cobertura extra" a **nucleo del producto**, y a la vez resulto ser la parte fragil.

### `DISTRIBUTION.md`

Estaba congelado esperando la evidencia de S4: si reproducia, se destrababa; si no, se descartaba. **No reprodujo.** Queda **sin destrabar**, y esa es la decision, no un pendiente olvidado.

## Pendientes de decision (de Gonzo)

1. ~~Crear el repo y hacerlo publico~~ **HECHO:** `gonzoblasco/kanam-fixer`, publico.
2. ~~Archivar `a11y-fixer`~~ **HECHO:** `isArchived=true` (2026-09-15 12:46 UTC).
3. ~~Paquete npm `@gonzoblasco/a11y-fixer@0.6.0`~~ **DECIDIDO (2026-09-15):** queda **publicado a proposito, sin deprecar**. Razon textual de Gonzo: "puede servir de entrada a alguien quien llegue a el por error". Verificado: sigue publicado (`0.6.0`), sin flag de deprecacion, 28 descargas en el ultimo mes. `kanam-fixer` sigue libre en npm y **no se publica** (el paquete es `private: true`).
4. ~~`a11y-playground`~~ **DECIDIDO (2026-09-15):** **archivado**. Verificado: `isArchived=true`, y era un scaffold vacio (1 commit, `size=0KB`, sin descripcion).
5. ~~S5 - cierre del ciclo~~ **HECHO (2026-09-15):** ciclo cerrado con evidencia. Decision: **no abrir `0.0.2`** hasta que S3 se pueda cerrar. Ver "Proximo paso".

**Abierto, y es una espera, no una tarea:** Guidepup publique el asset de Darwin 27 ([issue #149](https://github.com/guidepup/guidepup/issues/149), ya reportado).

Seguimiento en la DB de memoria: todo id=54.
