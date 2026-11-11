# Clase: forzar a la IA a escribir un sistema operativo (AuroraOS)

- Fuente: https://www.youtube.com/watch?v=s6FNslOI5ac
- Canal: The Render Guy · **Publicado:** 2026-10-07 · **Duración:** 7:32 (452 s)
- Idioma: inglés · **Formato:** video-experimento corto (no es un curso: es un challenge con veredicto)
- Transcript: [transcripcion.md](transcripcion.md) — 150 cues, 865 palabras, subtítulos automáticos
- Capítulos oficiales: 7 (de la descripción), alineados 1:1 con los módulos de acá
- Herramientas que muestra: Claude Opus 5.5 · QEMU · VirtualBox · C y assembly

> **Advertencia de género.** Esto no es un tutorial: nadie explica cómo escribir un kernel.
> Es un video de **proceso y veredicto**: qué se le pidió a un agente, cuánto tardó, qué
> salió, qué se rompió, y qué nota le puso el autor. La clase se lee como **caso de estudio
> de delegación**, no como material de sistemas operativos.

## Resultado esperado

Al terminar la clase se puede:

1. **Descomponer una tarea "imposible" en fases verificables** antes de delegarla, y hacer que el agente bootee el artefacto después de cada fase en vez de al final (Módulo 2).
2. **Escribir el prompt con criterios de hecho, no con adjetivos**: qué arquitectura, qué emulador, qué formato de salida, qué estilo visual (Módulo 1).
3. **Distinguir una advertencia del agente de un bloqueo**: cuando el agente avisa que algo no va a correr y se lo ignora, el costo aparece en el primer intento de ejecución (Módulo 4).
4. **Leer un "no se puede" del agente como una propuesta de alcance**, no como una negativa: "no hay browser completo" → "hay browser de texto con un helper de TLS fuera del OS" (Módulo 6).
5. **Evaluar el resultado por lo que el artefacto hace**, no por lo que el autor cuenta que hace: el mismo video se pone 6.5/10 y lista dos defectos concretos (Módulo 7).
6. **Dimensionar el costo real de una delegación**: 50 minutos + 18 minutos de agente, por ~6.000 líneas y un ISO (Módulo 3 y 6).

## Mapa temporal

| Tiempo | Capítulo oficial | Módulo |
|---|---|---|
| 0:00 | The Impossible AI Challenge | 1 |
| 1:18 | What goes into building a real OS? | 2 |
| 2:43 | Claude writes 6,000+ lines of code | 3 |
| 3:06 | The VirtualBox Crash & Fix (QEMU) | 4 |
| 3:30 | Booting AuroraOS for the first time | 5 |
| 5:18 | Pushing it further: Adding a Web Browser | 6 |
| 7:18 | Final Verdict: Can Claude replace developers? | 7 |

---

## Módulo 1 — El challenge y cómo se armó el prompt (0:00 – 1:16)

**Objetivo:** reconocer las decisiones que un prompt de delegación tiene que cerrar antes de
mandarse, y quién las cerró acá.

El truco del video: **no escribe el prompt él, se lo pide a Claude**. El prompt que sale de ahí
declara cinco cosas cerradas:

- lenguaje: C y assembly, «like real operating systems» (00:12)
- entorno de ejecución: VirtualBox, con interfaz estilo macOS (00:18)
- entregable: un `.ISO` (00:26)
- arquitectura: x86, GRUB, boot por BIOS (00:38)
- nombre: AuroraOS (00:41)

Y el plan que devuelve son **siete fases**: boot, kernel, input, graphics, window manager,
apps y polish (00:48).

**Idea fuerza:** el prompt no pide "un sistema operativo". Pide **siete fases con nombre** y un
artefacto por fase. Esa es la diferencia entre un pedido y un contrato.

Cita: «I'm letting Claude write the prompt for Claude code.» (00:06)

**Ejercicio.** Tomá una tarea grande que hoy se pide en una sola frase y reescribila con las
cinco decisiones del video (lenguaje, entorno, entregable, arquitectura, nombre). Si alguna
no la podés cerrar vos, marcá cuál y por qué: eso es lo que se delega al agente, no lo que se
deja abierto.

---

## Módulo 2 — Qué hay adentro de un OS de verdad (1:18 – 2:42)

**Objetivo:** entender por qué la tarea es difícil, para poder juzgar el resultado después.

La explicación ocupa menos de un minuto y es la única parte técnica del video. La cadena es:

1. **Boot loader** — al apretar power despierta y carga el kernel; acá es GRUB (00:59).
2. **Kernel** — «the boss»: habla con CPU, memoria, teclado y mouse (01:04).
3. **Drivers + gráficos** — para que las dos cosas anteriores tengan superficie donde verse (01:08).
4. **Window manager** (01:10).
5. **Apps** (01:12).

Cierre: «No Linux, no libraries, nothing.» (01:16)

**Idea fuerza:** lo difícil no es una línea de código, es **la cadena completa de dependencias**.
Un solo eslabón sin escribir y no hay boot. Por eso el plan en siete fases del Módulo 1 no es
adorno: es la única forma de tener algo que arranque en cada paso.

**Ejercicio.** Para el proyecto en el que estés trabajando, escribí la cadena de cinco capas
equivalente (de lo más bajo a lo más alto) y marcá cuál de ellas hoy **no existe** y no se nota
porque no se llega ahí. En `reinos-de-la-frontera` esa capa es la simulación headless: si
falta, el juego "anda" pero no hay partida real.

---

## Módulo 3 — La delegación y el costo (2:43 – 3:05)

**Objetivo:** medir qué significa "50 minutos de agente" y qué evidencia produjo.

El flujo que muestra:

- antes de escribir, **chequea herramientas**: VirtualBox, Homebrew, compiladores (01:37)
- **planea** antes de escribir una línea (01:39), y por cada fase bootea en QEMU para verificar (01:47)
- usa las capturas de macOS como inspiración, con instrucción explícita de que sea **original** (01:53)
- hace **dos preguntas** antes de arrancar: dónde poner el proyecto, y avisa que VirtualBox no va a correr x86 sobre ARM (01:58)

Resultado declarado: «About 50 minutes» (02:26), «Almost 6,000 lines of C» (02:34)

**Idea fuerza:** el agente **avisó** del problema de arquitectura antes de empezar, y el autor
eligió ignorarlo (02:09). Eso convierte al módulo 4 en una consecuencia anunciada, no en un
accidente.

**Claim a tomar con pinza:** 6.000 líneas y 88 archivos son lo que dice el video. No hay repo
público enlazado ni forma de verificar el conteo; se citan como **declaración del autor**.

**Ejercicio.** Revisá el último trabajo que delegaste: ¿el agente te hizo una pregunta que
contestaste sin leer, o te avisó de un riesgo que ignoraste? Escribí qué costó después.

---

## Módulo 4 — El crash que estaba anunciado y cómo se resolvió (3:06 – 3:29)

**Objetivo:** extraer la lección de proceso: una advertencia ignorada tiene fecha de vencimiento.

Secuencia textual:

- «Claude says VirtualBox can't run it on my Mac.» (02:41)
- «Remember that warning I ignored? Yeah, it was right.» (02:46)
- motivo real: Mac ARM contra OS compilado para x86, «basically, a different language» (02:52)
- solución: **QEMU**, un emulador que se hace pasar por una PC x86 (02:57)

**Idea fuerza:** el agente no falló. El humano tenía el dato y lo descartó por costo percibido.
El costo de resolver después fue cambiar emulador, no reescribir el OS: **la arquitectura del
plan (ISO x86) era la correcta, el entorno de prueba no**.

Distinción que vale para el workspace: *VirtualBox* era el entorno pedido en el prompt, *QEMU*
el que efectivamente ejecuta. Pedir "que corra en X" cuando X no puede correr la salida es un
requisito mal escrito, no un bug del agente.

**Ejercicio.** Encontrá en tu setup un requisito que pide "correr en X" cuando la arquitectura
real hace que X no aplique. Escribilo como par: entorno pedido / entorno que ejecuta.

---

## Módulo 5 — El artefacto arranca: qué se puede evaluar (3:30 – 5:17)

**Objetivo:** aprender a separar lo que el artefacto **hace** de la estética que lo rodea.

Lo que el video muestra funcionando, en orden:

| Evidencia | t= |
|---|---|
| Pantalla de arranque y desktop | 03:05, 03:08 |
| «About this computer»: versión 0.1, **lee CPU y memoria** del host | 03:14, 03:20 |
| Ventanas arrastrables | 03:22 |
| Dock con magnificación al hover | 03:22, 03:27 |
| App reloj: analógico, digital, calendario | 03:27, 03:32 |
| File viewer con changelog y readme | 03:43, 03:49 |
| Menú de sistema: about, settings, restart, shut down | 03:49, 03:55 |
| Terminal: `echo`, `ls`, `cat`, `memory`, `uptime`, `processes`, benchmark de primos | 03:59, 04:08 |
| `echo "Hello from OS"` ejecutado | 04:13, 04:28 |
| Apagado real: «It actually powered itself off» | 04:41, 04:44 |
| Fallo honesto: `power off` no existe como comando | 04:30, 04:33 |

**Idea fuerza:** la línea más valiosa del módulo no es lo que funciona, es **lo que no**:
`power off` → `command not found`, y el autor lo dice en vez de cortarlo. Un demo sin un fallo
declarado no es un demo, es un comercial.

**Ejercicio.** Hacé la tabla equivalente de tu último entregable: una fila por cosa que **viste
funcionar** con su evidencia, y una fila con **lo que falló**. Si la segunda fila está vacía,
no lo probaste.

---

## Módulo 6 — El segundo pedido: alcance negociado (5:18 – 7:17)

**Objetivo:** leer la contrapropuesta del agente como una decisión de ingeniería, no como un "no".

Pedido: «Quickly add a web browser so I can search.» (04:54)

Respuesta del agente: un browser completo no entra — todo buscador necesita HTTPS, y eso son
**decenas de miles de líneas** — pero puede hacer un **browser de texto** (05:10).

Lo que efectivamente construyó (05:27):

1. driver de la placa de red virtual
2. ethernet → IP → DNS → TCP → HTTP, en ese orden
3. para HTTPS: **un helper chico en la Mac** que hace el cifrado, fuera del OS

Resultado declarado: «about 18 minutes» (05:48).

Lo que se vio funcionando: icono nuevo en el dock y start page (05:59), resultados de
DuckDuckGo reales (06:09), Wikipedia sin estilos pero cargando (06:14), Google
en HTML plano (06:22), y settings con light/dark mode (06:40).

**Idea fuerza:** el recorte de alcance es explícito y **con el motivo técnico al lado**: no
"no puedo", sino "HTTPS requiere X, y X es más grande que todo lo anterior". Eso permite
decidir informado en vez de discutir con el agente.

Segunda idea: **delegar el borde de afuera**. El cifrado TLS no vive en el OS, vive en un
helper del host. Es la decisión de arquitectura más honesta del video: el sistema operativo
no se convierte en un navegador para poder decir que tiene navegador.

**Ejercicio.** Tomá un pedido que hoy rechazás entero y partilo en tres: lo que entra, lo que
entra degradado, y lo que queda afuera con el motivo técnico. Después decidí con esa tabla,
no con la primera impresión.

---

## Módulo 7 — El veredicto: 6.5/10 y por qué (7:18 – 7:31)

**Objetivo:** evaluar con criterio explícito, incluyendo lo que el autor se niega a inflar.

El autor resume lo construido: kernel propio, desktop estilo macOS, apps, terminal, browser
(06:53). Después lista los defectos **antes** de la nota:

- no corre en VirtualBox en su Mac (07:06)
- los sitios web no tienen ningún estilo (07:09)

Nota: «I'm giving it 6.5 out of 10.» (07:11)

Y la pregunta que abre el título: «Can Claude replace developers?» queda respondida de forma
ambigua a propósito: «Claude can actually build an operating system» (07:15).

**Idea fuerza:** la nota no mide el esfuerzo del agente (50 minutos, 6.000 líneas), mide el
**artefacto**: arranca, hace cosas, no cumple dos requisitos. Un veredicto con los defectos
listados al lado vale más que un 10/10 sin lista.

**Ejercicio.** Ponele nota a tu último entregable con el mismo formato: tres cosas que hace,
dos que no cumple, y un número. Si el número no se puede defender con esa lista, está inflado.

---

## Banco de preguntas

1. ¿Qué cinco decisiones cerraba el prompt del video y cuál de ellas fue la que falló después?
2. ¿Por qué el plan en siete fases es lo que hace verificable la tarea? Relacionelo con "bootear después de cada fase".
3. El agente avisó antes de empezar que VirtualBox no correría x86 sobre ARM. ¿Qué convierte esa advertencia en un problema y qué la habría evitado?
4. ¿Qué diferencia hay entre pedir "un browser" y aceptar "un browser de texto con helper TLS en el host"? ¿Cuál es la parte que no vive en el OS y por qué es una buena decisión?
5. El video declara 6.000 líneas y 88 archivos. ¿Por qué eso no es evidencia de que el artefacto funcione?
6. ¿Qué dice el `power off` → `command not found` sobre cómo se presenta un demo?
7. El autor se pone 6.5/10. Enumerá la lista que sostiene esa nota y decí si el número es consistente con ella.
8. ¿Qué se puede adoptar de este video para un proyecto de simulación por ticks como `reinos-de-la-frontera`, y qué no?

## Lo que este video no cubre

- **No enseña a escribir un kernel ni un bootloader.** No hay una línea de código explicada.
- **No enlaza el repo.** Los conteos (líneas, archivos, minutos) son declaraciones del autor, sin forma de verificar.
- **No muestra el prompt completo**, solo fragmentos y la respuesta del plan.
- **No explica el helper TLS** del host, que es justamente la pieza que permite el browser de texto.
- **La versión "Opus 5.5"** es la que anuncia el video; no se verificó contra el catálogo de modelos de Anthropic.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
