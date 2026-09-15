# STATUS - kanam-fixer

**Actualizado:** 2026-09-15
**Ciclo:** 0.0.1
**Slice actual:** S4 completado con **resultado negativo**. S5 (cierre del ciclo) pendiente.

## Donde estamos

| Slice | Estado | Evidencia |
|---|---|---|
| S1 - Esqueleto y decisiones | **Completado** | Commit `6044856`. Terna en verde, hook activo. |
| S2 - La asercion, solo virtual | **Completado** | Commit `fb931ea`. 7 tests. Criterio de salida verificado. |
| S3 - VoiceOver real en local | **Codigo listo, criterio NO verificado** | Commit `b98bf1b`. Blocker: permisos de macOS. Diferido por decision de Gonzo. |
| S4 - El caso testigo (#4109) | **Completado - NO reproduce** | Commit `5090278`. 8 tests. Hallazgo abajo. |
| S5 - Cierre del ciclo | Pendiente | Requiere decision de Gonzo (ver al final). |

**Repo publico:** https://github.com/gonzoblasco/kanam-fixer (`5090278`). Verificado que `.knowledge/` no se filtra.
**Terna:** 17 passed, 4 skipped (los 4 son el plano real, con su causa impresa).

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

## S3: el plano del lector real - BLOQUEADO (diferido)

Diferido por decision de Gonzo (2026-09-15): se avanza S4 primero, S3 queda esperando una accion humana.

### Que quedo construido

- **`ReaderDriver`**: contrato propio (ADR-0001). `virtualDriver` (CI) y `realDriver` (VoiceOver) lo implementan, asi que **la misma asercion corre en los dos planos**.
- **`expectAnnouncement(container, expected, { driver })`**: el driver es opcional; el default sigue siendo el virtual.
- **`realReaderAvailability()`**: arranca y para el lector una vez, para que el llamador pueda **saltear con la razon real** en vez de reportar un falso verde.

### El blocker (necesita a Gonzo, no a un agente)

`screenReader.detect()` y `.default()` devuelven **true**, pero `start()` falla con `VoiceOver cannot be started`. Faltan dos pasos manuales de macOS:

1. **VoiceOver Utility -> General -> tildar "Allow VoiceOver to be controlled with AppleScript".** Verificado: `/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled` **no existe** en esta maquina.
2. **System Settings -> Privacy & Security -> Accessibility**: agregar y tildar el proceso que corre los tests.

### Lo que NO se hizo, y por que

`npx @guidepup/setup setup` automatiza esto, **pero escribe directo en la base de permisos de privacidad de macOS** (`/Library/Application Support/com.apple.TCC/TCC.db` via `sqlite3`, mas el archivo de VoiceOver) y su lista de clientes incluye cosas ajenas a este proyecto (`sshd`, `bash`, `zsh`, `osascript`, Terminal, System Events, navegadores). **Decidido: no ejecutarlo.** Es un cambio de seguridad de la maquina, no del proyecto. La via manual es mas acotada y es la preferida. **Nunca desactivar SIP** (verificado: sigue `enabled`).

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

**S5 (cierre del ciclo), y requiere una decision de Gonzo.** El ROADMAP dice que si la apuesta no se sostiene, se descarta antes de invertir mas.

Los datos dicen algo mas matizado que "se sostiene" o "no se sostiene":

- **Se sostiene** para bugs de **atributos y composicion**: S2 lo demostro con evidencia.
- **No se sostiene** para bugs de **timing y derivacion del viewport**: S4 lo demostro con evidencia, y ademas encontro que el plano virtual puede dar **falsos verdes** ahi.

**Mi lectura:** la apuesta original ("misma asercion, dos planos") sigue en pie, pero **invertida**: el valor no esta en el plano virtual como sustituto, sino en el **plano real como unico juez** de esa clase, con el virtual como red barata para lo demas. Eso cambia el peso de S3: pasa de "cobertura extra" a **nucleo del producto**.

**Ademas, `DISTRIBUTION.md`** estaba congelado esperando la evidencia de S4: si reproducia, se destrababa; si no, se descartaba. **No reprodujo.** Queda sin destrabar, a la espera de la decision de S5.

## Pendientes de decision (de Gonzo)

1. ~~Crear el repo y hacerlo publico~~ **HECHO:** `gonzoblasco/kanam-fixer`, publico.
2. ~~Archivar `a11y-fixer`~~ **HECHO:** `isArchived=true` (2026-09-15 12:46 UTC).
3. ~~Paquete npm `@gonzoblasco/a11y-fixer@0.6.0`~~ **DECIDIDO (2026-09-15):** queda **publicado a proposito, sin deprecar**. Razon textual de Gonzo: "puede servir de entrada a alguien quien llegue a el por error". Verificado: sigue publicado (`0.6.0`), sin flag de deprecacion, 28 descargas en el ultimo mes. `kanam-fixer` sigue libre en npm.
4. ~~`a11y-playground`~~ **DECIDIDO (2026-09-15):** **archivado**. Verificado: `isArchived=true`, y era un scaffold vacio (1 commit, `size=0KB`, sin descripcion).
5. **S5:** decidir el cierre del ciclo a la luz del resultado negativo de S4 (ver arriba).

Seguimiento en la DB de memoria: todo id=54.
