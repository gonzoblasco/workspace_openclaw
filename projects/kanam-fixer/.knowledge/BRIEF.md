# BRIEF - kanam-fixer

**Estado:** S1 completado (2026-09-15). Esqueleto y tooling en pie, sin logica de a11y todavia. Repo publico: https://github.com/gonzoblasco/kanam-fixer (commit `6044856`).
**Primer ciclo:** 0.0.1
**Pilar:** Accesibilidad como diferenciador (ADR-001, seccion 6: candidato a ancla, alcance en definicion)
**Sucede a:** `a11y-fixer` (archivado 2026-09-14). **No hereda su codigo ni su alcance.**

> **Direccion propuesta, pendiente de confirmacion de Gonzo.** El alcance se definio a partir de evidencia (ver "Por que"), pero la decision de direccion es de Gonzo. Si cambia la direccion, cambia el roadmap.

---

## Que es, en una linea

**De los atributos a lo que se escucha:** assertar el **anuncio** del lector de pantalla - en local con el lector real, y en CI con uno virtual, con la misma API.

## Por que este proyecto y no un a11y-fixer v2

`a11y-fixer` no murio por falta de codigo: murio por **falta de uso**. Llego feature-complete (40/40 tareas), publicado en npm, con 102 tests verdes - y 0 estrellas, 0 usuarios externos. El espacio de "correr axe-core sobre un PR y comentar" esta **saturado y commoditizado**: en el propio Marketplace de GitHub conviven `a11y-check`, `a11yguard`, `accessibility-scanner` y varios mas.

Rehacer eso seria no haber aprendido nada. **La leccion de 0.0.1 es que el camino empieza por el usuario, no por la feature.**

## El hueco que ataca

Todo el toolchain mainstream de a11y **testea atributos y estructura**. Ninguno testea **lo que el lector de pantalla dice**.

Ese limite esta documentado en nuestra propia practica. La skill `a11y-at-validation` define la frontera asi:

| Verificable por test unitario | Solo verificable a mano |
|---|---|
| Atributos ARIA en el DOM | **Lo que el lector de pantalla anuncia (la frase)** |
| Roles, `aria-labelledby`, `aria-selected` | **El timing del anuncio** (cuando se dice, si se dice) |
| Estructura del arbol de accesibilidad | Interaccion real (roving focus, `aria-activedescendant`) |

**Caso testigo (radix-ui #4109/#4110):** el `aria-posinset` estaba correcto en el DOM y los 51 tests pasaban en verde - pero con VoiceOver el first option **no anunciaba nada**, por una carrera de timing entre el mount y el anuncio. Ningun test unitario podia atraparlo.

Hoy eso se resuelve **a mano**: abrir el storybook, prender VoiceOver, escuchar. Es conocimiento de especialista, no se automatiza. **Ahi esta el producto.** Y es exactamente el trabajo que hacemos en cada PR de accesibilidad en repos ajenos.

## El usuario

**Especialistas de a11y y maintainers de design systems** que tienen que defender el comportamiento de un componente en review y no pueden correr un lector de pantalla en cada PR.

Es el usuario que Gonzo conoce desde adentro: 8+ anos en el tema, ~5 con a11y como funcion central, 200+ fixes probados con lectores de pantalla, y hoy Lead Software Engineer de Digital Accessibility. No es un usuario imaginado.

**Criterio de exito (definido por NORTH.md, Horizonte 1):** que lo use alguien que no sea Gonzo, con issues y PRs de terceros.

## La apuesta

Que el trabajo que hoy es **manual y de especialista** se vuelva **una asercion repetible** - sin perder la verdad del lector real.

La pieza que lo hace posible ya existe y esta viva: **Guidepup** (MIT, 561 stars, ultimo push 2026-09-13, ~27.500 descargas semanales). Automatiza lectores de pantalla **reales**: VoiceOver en macOS, NVDA en Windows. Y su driver virtual (`@guidepup/virtual-screen-reader`, ~33.000 descargas semanales) corre sin AT real.

**El diferenciador no es automatizar un lector - es la misma asercion en dos planos:**

| Plano | Driver | Donde corre | Para que |
|---|---|---|---|
| Rapido | virtual | CI, cualquier SO | No romper el anuncio en cada PR |
| Verdad | VoiceOver / NVDA | local, macOS / Windows | Confirmar antes de publicar |

Eso es un workflow que hoy nadie empaqueta, y que nosotros ya ejecutamos a mano.

## Que NO es

- **No es un scanner.** No compite con axe-core ni lo reemplaza. Si el problema es un `alt` vacio, axe-core ya lo resuelve mejor.
- **No es un dashboard de reportes.** Nadie cambia de herramienta por graficos.
- **No es SaaS.** Sin lock-in, corre en la maquina de quien lo usa.
- **No hereda el engine de a11y-fixer.** Si algo de ese codigo sirve, se porta con decision explicita, no por inercia.
- **No es un framework de testing.** Es una asercion puntual sobre el anuncio, no un runner.

## Stack propuesto (a validar en 0.0.1)

- **TypeScript** + Node (el ecosistema de Guidepup es JS/TS).
- **Guidepup** para el driver real; su driver virtual para CI.
- **Playwright** para llevar el navegador al estado previo al anuncio.
- Biome, Vitest, pre-commit hooks (regla del workspace: lint -> test -> build).

## Riesgos y restricciones (honestos)

1. **El lector real no corre en CI.** VoiceOver necesita macOS y permisos de accesibilidad; NVDA, Windows. **Por eso existe el driver virtual** - no es un extra, es la respuesta a esta restriccion.
2. **Automatizar lectores de pantalla es intrinsecamente flaky** (timing, foco, audio). Exige la misma disciplina que ya nos costo caro con SSE en kanam-pulse: waits generosos y tests que no dependan del reloj.
3. **Dependencia de terceros.** Guidepup es MIT y esta activo, pero es una dependencia central. Verificado el 2026-09-14: `stars=561`, `pushed=2026-09-13`, `archived=false`, `license=MIT`. No hay alternativa real para automatizar lectores de pantalla reales; el riesgo se mitiga con una capa propia fina sobre su API.
4. **La frase anunciada varia por lector, version y SO.** No se puede prometer "el anuncio" universal: hay que declarar la matriz (lector x version x SO) igual que hacemos en los PRs.

### Documentos del proyecto

- **`ROADMAP.md`** - el ciclo `0.0.1` y sus slices.
- **`DISTRIBUTION.md`** - material de lanzamiento **guardado, sin ejecutar**. Investiga los canales de descubrimiento (awesome lists, GitHub Marketplace) y conserva los textos redactados el 2026-09-14 para `a11y-fixer`, con la advertencia de que no se reciclan tal cual. **Congelado hasta que exista evidencia (S4).** Publicar esta fuera de alcance de `0.0.1`.

## Requisitos de S3 (permisos de macOS)

El plano del lector real **no corre sin dos pasos que solo se hacen a mano** en macOS. Verificado el 2026-09-15 en esta maquina: `screenReader.detect()` y `.default()` devuelven `true`, pero `start()` falla con `VoiceOver cannot be started`.

1. **VoiceOver Utility -> General -> "Allow VoiceOver to be controlled with AppleScript".** El archivo que lo habilita, `/private/var/db/Accessibility/.VoiceOverAppleScriptEnabled`, **no existe** hoy.
2. **System Settings -> Privacy & Security -> Accessibility:** agregar y tildar el proceso que corre los tests (la terminal o el host del agente).

Hasta que esos dos permisos existan, el plano real **se saltea con su causa a la vista** (`REAL_READER_UNAVAILABLE: VoiceOver cannot be started`), nunca pasa en falso.

### Advertencia: `@guidepup/setup setup`

Ese comando automatiza los permisos, pero **escribe directo en la base de privacidad del sistema** (`/Library/Application Support/com.apple.TCC/TCC.db`, via `sqlite3`) y en el archivo de VoiceOver. Su lista de clientes es amplia e incluye cosas ajenas a este proyecto (`sshd`, `bash`, `zsh`, `osascript`, Terminal, System Events, navegadores, runners de CI).

**Decision (2026-09-15):** no ejecutarlo sin pedido explicito de Gonzo. Es un cambio de seguridad de la maquina, no del proyecto. Existe ademas una via manual, mas acotada, documentada en https://www.guidepup.dev/docs/guides/manual-voiceover-setup - **preferible**, porque otorga el permiso solo al proceso que lo necesita.

**Nunca desactivar SIP** para esto: la propia documentacion de Guidepup lo advierte por sus implicancias de seguridad.

## Pendientes de decision (de Gonzo)

1. ~~Confirmar la direccion~~ **HECHO (2026-09-15):** direccion confirmada ("si, dale").
2. ~~Nombre / repo~~ **HECHO (2026-09-15):** `gonzoblasco/kanam-fixer` creado y **publico** (https://github.com/gonzoblasco/kanam-fixer). Codigo de S1 pusheado (commit `6044856`). Verificado que `.knowledge/` NO se filtro al repo publico. `kanam-fixer` sigue libre en npm (404) - publicar el paquete es una decision aparte, no tomada.
3. **`a11y-fixer`:** repo de GitHub **archivado** (verificado: `isArchived=true`, 2026-09-15 12:46 UTC). **Falta decidir** el paquete npm `@gonzoblasco/a11y-fixer@0.6.0` (publicado 2026-07-29, con descargas): dejarlo, deprecarlo o despublicar.
4. **`a11y-playground`:** declara depender de `a11y-fixer` como base. Migra, se archiva o se sostiene sola. **Sin decision.**

Seguimiento en la DB de memoria: todo **id=54**.
