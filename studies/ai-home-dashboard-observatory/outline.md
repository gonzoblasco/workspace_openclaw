# Clase: I Built an App for My House With AI — un dashboard de casa que no miente

- Fuente: https://www.youtube.com/watch?v=CgkdaeQ58eE
- Canal: Peter Lindgren (Suecia)
- Expositor / speaker: Peter Lindgren — diseñador de producto y ropa, no programador («I have no experience in designing smartphone apps or smart TV apps or dashboards», 00:10:48). Construye con Codex (agente de coding de OpenAI) y un Homey Pro.
- Publicado: 2026-10-26 · Duración: 13:51 (831 s)
- Idioma: inglés · Captions automáticos de YouTube (`en-orig`), 421 cues, 2.669 palabras
- Transcripción: `transcripcion.md` · Código: `github.com/prmgr-org/prmgr-observatory-starter` (MIT, verificado en la API el 2026-11-11)
- Adopción: `ADOPCION.md` · Gate: `scripts/check-freshness-display.py`

## Qué es este video, sin adornos

No es un curso. Es un **case study de 14 minutos** sobre un no-programador que se construye un centro de control en la TV del living, con dos ideas de ingeniería de datos que sí valen:

1. **Un número medido sin su fecha miente.** Si la lectura es vieja, la pantalla tiene que decirlo o apagarse.
2. **Separar quién captura de quién muestra**, porque la captura tiene que sobrevivir a que el Mac se apague.

El resto es diseño, Homey Pro y demos de dashboard. Se puede aprender, pero no es lo que justifica estudiarlo.

## Resultado esperado

Al terminar la clase sabés, y podés mostrar:

1. **Modelar una lectura como `(valor, timestamp)` obligatorio**, y decidir qué hace la UI cuando el timestamp es viejo (degradar, no inventar).
2. **Separar el colector de la vista**: el proceso que escribe datos corre donde la máquina no duerme; la vista consume.
3. **Verificar la unidad de un dato antes de derivar cualquier métrica de negocio** (kilovatios vs. vatios; el costo se calcula recién cuando la lectura está validada).
4. **Evitar el doble conteo** en una agregación jerárquica: un medidor hijo dentro de un total no se suma otra vez.
5. **Derivar un dato de presentación de la fuente de verdad** (hora de fin de impresión = ahora + tiempo restante), no recalcularlo a mano cada vez.

## Mapa temporal

Sin capítulos oficiales en la descripción. Los bloques salen de los cues.

| Tiempo | Bloque |
|---|---|
| 00:00 - 00:01 | Gancho y origen: una gráfica de bomba de calor |
| 00:01 - 00:02 | La pregunta correcta: ¿qué querés saber, y el equipo te lo puede decir? |
| 00:02 - 00:03 | Regla cero: empezar con un equipo y una pregunta |
| 00:03 - 00:04 | Historial: guardar cada lectura con su hora; el costo espera a la validación |
| 00:04 - 00:05 | Contexto de la casa: solar, batería, red; el garage se resta, no se suma |
| 00:05 - 00:06 | Diseño: referencia visual y el brillo de los paneles atado a la producción real |
| 00:06 - 00:07 | El bucle real de trabajo: pedir, probar, encontrar el hueco, pedir de nuevo |
| 00:07 - 00:09 | Mac apagado: mover la captura al NAS; datos separados de la app |
| 00:09 - 00:10 | La TV: Google TV, modo desarrollador y `adb` |
| 00:10 - 00:13 | Tour del dashboard terminado y qué es lo que lo hace útil |
| 00:13 - 00:13 | Cierre, fuente liberada y llamado a comentar |

## Módulos

### Módulo 1 - El proyecto nace de una pregunta aburrida y concreta (00:00 - 00:02)

- **Objetivo:** empezar un proyecto de datos por la pregunta y por la fuente, no por la pantalla.
- **Contenidos:**
  - El disparador fue una gráfica imposible de leer: la app del fabricante muestra datos, pero «the app that comes with it is incredibly unintuitive in my opinion» (00:01:17).
  - El ponente quería dos vistas del mismo dato: en vivo y hacia atrás, «looking at what the heat pump does right now is not going to tell me what it did 3 hours ago» (00:00:54), y eso obliga a **grabar**: «we need to gather and record the data it provides» (00:01:00).
  - El equipo habla **Modbus**: «Think of it as a shared language. Our app asks for the water temperature and the heat pump sends back a number» (00:01:58). El proyecto **solo lee mediciones**, no escribe en el equipo.
- **Evidencia vs. anécdota:** el uso de Modbus es un hecho técnico del equipo del ponente (una bomba de calor con interfaz Modbus es estándar en climatización, no una rareza). Que *su* bomba lo tenga es anécdota; que muchas lo tengan, no.
- **Ejercicio:** listá tres preguntas que querés responder de un dispositivo tuyo, y para cada una anotá (a) si el dato es en vivo o histórico, (b) por qué interfaz lo expone el equipo (API, Modbus, MQTT, scraping) y (c) si es lectura o escritura. **Entregable:** tabla de 3 filas. La pregunta (c) es la que evita el proyecto peligroso.

### Módulo 2 - Empezar chico es una regla de ingeniería, no un consejo (00:02 - 00:03)

- **Objetivo:** dimensionar el primer corte de un proyecto de datos para que sea verificable.
- **Contenidos:**
  - «the first thing that I recommend» (00:02:12) … «start small» (00:02:15) … «like start with one unit, ask one question» (00:02:17).
  - La razón que da no es de gestión, es de control: «Don't try to create this behemoths that you don't have control of to begin with because you can elaborate that later» (00:02:19).
  - Antes de construir la app, el paso previo que recomienda es **inspeccionar el equipo** y comprobar que la conexión con Codex va a funcionar (00:02:31). Es la verificación de viabilidad antes del desarrollo.
- **Ejercicio:** para tu primera pregunta del módulo 1, escribí el **camino mínimo** hasta una lectura real: cómo se lee, con qué herramienta, y qué valor concreto esperás ver. **Entregable:** un comando o llamada que devuelva un número, con la salida pegada. Si no lo podés pegar, todavía no hay proyecto.

### Módulo 3 - Toda lectura se guarda con su hora, y el costo espera (00:03 - 00:04)

- **Objetivo:** que la serie histórica sea reconstruible y que ninguna métrica derivada salga de un dato no validado.
- **Contenidos:**
  - Cómo se arma el día en un gráfico: «We save each reading with the time it was taken. That's how we can put the day back together on a graph» (00:03:10). El timestamp es parte de la lectura, no un campo opcional.
  - El costo tienta y se rechaza con una razón concreta: «We're getting a number. We still need to check exactly what it measures and whether we're reading the units correctly. Until then, using it to work out a cost could give you the wrong answer» (00:03:23). Tener un número **no** es tener una medición validada.
  - El ponente lo eleva a regla para cualquiera que replique el proyecto: «you got to make sure that the readings are correct so that all the info that you're getting from the app that you're building is true to the stuff that you actually have in your heat pump» (00:03:43).
- **Evidencia vs. anécdota:** el riesgo de unidad equivocada es real y frecuente (kW vs W, m³ vs litros). No hay estadística en el video; el argumento es de diseño, y es correcto por sí solo.
- **El starter implementa la regla, y la documenta:** en `docs/DATA-FORMAT.md` del repo, `null` se muestra como *unavailable* y corta la línea del gráfico, con la regla escrita al lado: **«Never use zero to mean unavailable»** (verificado el 2026-11-11). El `0` es una medición; la ausencia no lo es.
- **Ejercicio:** tomá una lectura de tu primer corte y **contrastala contra la pantalla del propio equipo** (no contra otra app). **Entregable:** dos valores, el de tu app y el del equipo, con la unidad escrita al lado del número. Diferencia documentada si existe.
- → **Esto es lo que el gate de `ADOPCION.md` hace verificable para las pantallas:** un valor en pantalla sin la fecha de su lectura es del mismo tipo que un costo sin unidad: un número que parece un dato.

### Módulo 4 - Agregar bien: el garage se resta, y el cargador ya está adentro (00:04 - 00:05)

- **Objetivo:** descomponer un consumo total sin contar dos veces la misma electricidad.
- **Contenidos:**
  - El garage tiene medidor propio, así que no se suma: «we take what the whole property is using, subtract the garage, and what's left is the house» (00:04:11). Es una **diferencia**, no una suma.
  - La condición: «We only show that split when both readings are reliable» (00:04:17). La agregación condicionada a la frescura y validez de sus fuentes, otra vez.
  - Medir el edificio por la compra de la red es un error de modelo: «the house can also be running on solar or battery power. The grid connection only shows what passes between you and the grid» (00:04:24). Mucho consumo con poca compra.
  - El cargador del auto **ya está** en el total: «It's consumption is» (00:04:39) … «already inside the total» (00:04:41), y sumarlo de nuevo sería «an electricity bill with a fictional subplot» (00:04:46).
- **Evidencia vs. anécdota:** es topología de medidores, verificable con los medidores de la casa del ponente. El principio general — un submedidor dentro de un total no se suma — aplica a cualquier agregación jerárquica (tokens por agente dentro de un total, líneas por archivo dentro de un repo).
- **Ejercicio:** dibujá tu árbol de medidores y marcá para cada nodo si es **suma** o **diferencia**. **Entregable:** el árbol en texto, con una frase por nodo explicando de dónde sale. El doble conteo aparece siempre en el nodo que nadie escribió.

### Módulo 5 - Que la pantalla refleje el mundo, y que se apague cuando el mundo no habla (00:05 - 00:06)

- **Objetivo:** atar un efecto visual a un dato real, con una regla explícita para el dato viejo o ausente.
- **Contenidos:**
  - El brillo de los paneles solares no es decoración: «The more electricity the panels are making, the stronger the glow. If they're making nothing, or we haven't had a fresh reading, the pulse stops» (00:05:36). Tres estados, no dos: **produciendo**, **produciendo cero** y **no sé** — y el último se ve distinto del segundo.
  - La interacción también es un mapa de datos: click en los paneles lleva a la información del sistema solar (00:05:19).
  - Cómo se pide el diseño: con una **foto de referencia** de la propia casa (00:05:00), no con adjetivos.
- **Evidencia vs. anécdota:** el criterio «no fresh reading → the pulse stops» es una decisión de producto explícita, y es la idea más transferible del video. No necesita estadística: es una regla que se puede implementar o no.
- **El umbral, que el video no da, sí está en el starter:** un gráfico corta la línea cuando dos muestras consecutivas están a más de **10 minutos**, y se espera un muestreo de 30 s a 5 min; si el muestreo es más lento y no se ajusta, «sparse data will appear as isolated points rather than fabricated lines» (`docs/DATA-FORMAT.md`, verificado el 2026-11-11). Es la respuesta concreta al «¿cuándo está viejo?» que el video deja abierto.
- **Ejercicio:** elegí un indicador de tu app/proyecto que hoy se muestre como «en vivo». **Entregable:** tres estados definidos en texto (vivo / cero / sin dato fresco) y el criterio numérico de «fresco» (p. ej. «más viejo que 2× el intervalo de muestreo»).

### Módulo 6 - El bucle real: pedir, probar, encontrar el hueco, pedir de nuevo (00:06 - 00:07)

- **Objetivo:** reconocer en qué consiste trabajar con un agente de coding, sin romance.
- **Contenidos:**
  - La descripción del proceso, en primera persona: «I told the Codex what I wanted to have, and then Codex made it for me, and then I tried everything out, and then I found the loopholes, and found the things that I wanted to adjust, and then I told the Codex again» (00:05:48).
  - Un cambio de presentación que elimina trabajo mental: la hora de fin de la impresión 3D, en vez del tiempo restante. «I'm doing the maths every time. If we add that, then I can just see which timestamp the print is going to be finished» (00:06:17).
  - El agente propone **derivar** en vez de agregar un campo: «We can calculate a finish time from the printer's estimate» (00:06:25).
- **Evidencia vs. anécdota:** el bucle describe la práctica del ponente; no hay medición de cuántas iteraciones hizo (una cifra que faltaría para evaluar el método). Se registra como descripción, no como dato.
- **Ejercicio:** tomá una tarea que hoy hacés calculando a mano sobre datos que ya tenés, y reemplazala por un valor **derivado** en la superficie donde lo mirás. **Entregable:** el campo derivado escrito, y el input del que sale.

### Módulo 7 - Homey Pro como capa de integración (00:06 - 00:08)

- **Objetivo:** entender cuándo un hub comercial es la decisión correcta y cuándo no.
- **Contenidos:**
  - El argumento a favor de Homey es de inventario, no de features: «all my smart devices» (00:06:39) — ya está todo conectado, y desde ahí se expone una API.
  - El argumento en contra de Home Assistant no es técnico: Home Assistant «would probably work» (00:06:59), pero Homey es lo que el ponente ya tiene, con «a nice UI. It's very simple» (00:07:07) y flows que se generan con ayuda de un LLM.
  - El ponente es explícito sobre el criterio: «the reason that I kind of went for Homey is because everything is connected to it» (00:07:01).
- **Evidencia vs. anécdota:** esto es una decisión **contextual**, no una recomendación. Para alguien que arranca de cero, Home Assistant es la opción por defecto (OSS, sin hardware propietario); Homey se justifica si ya está y funciona. Registrar la condición, no la conclusión.
- **Ejercicio:** si tenés un hub, listá qué porcentaje de tus dispositivos expone una API utilizable. **Entregable:** lista con sí/no por dispositivo. Si la respuesta es «casi todos vía la app del hub», el hub *es* la capa de integración.

### Módulo 8 - Separar captura de presentación, antes de que duela (00:07 - 00:09)

- **Objetivo:** diseñar para que el colector viva donde no duerme la máquina.
- **Contenidos:**
  - El agujero se detecta preguntando, no leyendo código: «What is going to happen if I turn my Mac off? Because everything is stored locally, right?» (00:07:25) → «Shut down the Mac and we stop building that history» (00:07:32).
  - La solución es un NAS Synology: «a storage computer on your home network. Yours can also run this app. It already stays on» (00:07:45).
  - Qué se mueve, exactamente: «We move the bit that collects the readings, the history we've already saved, and the saved connections it needs» (00:07:58). No se mueve la app entera; se mueve **el colector y su base**.
  - Se corre con **Container Manager** (Docker) del NAS (00:08:31).
  - Y la separación que salva los datos: «The app and the saved history live separately. That means we can replace the app when we update it without replacing all the readings you've collected» (00:08:38). El comentario seco del ponente: «It tends to become very important immediately after someone forgets» (00:08:49).
- **Evidencia vs. anécdota:** la separación app/datos es estándar y obligatoria en cualquier sistema con historial (volumen de Docker fuera de la imagen). La anécdota del Mac dormido es el disparador, no la prueba.
- **Ejercicio:** identificá en tu proyecto qué proceso **escribe** y qué proceso **leen**. **Entregable:** dos líneas, con la respuesta a «¿qué pasa con la captura si esta máquina se apaga una hora?». Si la respuesta es «se pierde», ahí está la deuda.

### Módulo 9 - La TV como superficie: Google TV y modo desarrollador (00:09 - 00:10)

- **Objetivo:** conocer el costo real de llevar una app a una pantalla que no es el navegador.
- **Contenidos:**
  - La pregunta es de producto: «I want to be able to open it with my remote» (00:09:06).
  - El paso previo correcto antes de escribir una línea: «Find the exact» (00:09:26) … «model, the operating system» (00:09:28) … «how you can unlock the developer mode» (00:09:31).
  - El procedimiento real: siete taps en «Build» del menú de ajustes para ser desarrollador, y después **activar la depuración** (00:09:49), que es lo que permite instalar desde la Mac con aprobación en la TV (00:10:00).
- **Evidencia vs. anécdota:** el procedimiento de Android TV es estándar y verificable en la documentación de Google; el ASR deforma el nombre del menú pero la secuencia es la conocida.
- **Ojo con el alcance:** la descripción del video aclara que **la app de TV no está incluida** en el starter. El módulo 9 es lo que el ponente hizo, no lo que se descarga.
- **Ejercicio:** si te interesa una TV, escribí los tres pasos de *setup* del dispositivo en tu equipo, con el modelo exacto. **Entregable:** modelo + versión de OS + método de depuración. Sin eso, el proyecto de TV no empieza.

### Módulo 10 - El dashboard que vale: todo a la vista, en una pantalla (00:10 - 00:13)

- **Objetivo:** decidir qué merece estar en la vista principal de un dashboard personal.
- **Contenidos:**
  - La razón de construir el dashboard, en palabras del ponente: ver todo «right in front of your eyes without» (00:12:48) … «having to click in multiple different programs» (00:12:49). El valor es la **reducción de saltos**, no tener más gráficos.
  - Cada elemento de la casa es un punto de entrada a su detalle: casa, paneles solares, garage (00:11:39).
  - El dashboard no mira solo la casa: cámaras, Instagram, YouTube, y responder comentarios **desde ahí** porque usa las APIs de Meta (00:12:22).
  - Un detalle de fidelidad al mundo: las luces del jardín se encienden en la imagen cuando se encienden en la casa (00:13:05).
  - Cuándo se para: «I could probably keep tweaking» (00:11:21) … «this forever» (00:11:22) … «but there's no» (00:11:22) … «need to keep working on something that I» (00:11:25) … «think is good» (00:11:27).
- **Evidencia vs. anécdota:** todo el módulo es el resultado de un caso personal. Lo verificable es la fuente liberada (MIT, `prmgr-org/prmgr-observatory-starter`) y que el demo usa **datos de muestra etiquetados**.
- **Ejercicio:** escribí las cinco cosas que mirarías de tu casa en una pantalla, y para cada una la fuente del dato. **Entregable:** cinco filas; las que no tienen fuente, se borran o se marcan como «no disponible», no se rellenan con números inventados.

### Módulo 11 - Cierre: lo que el video no dice (00:13 - 00:13)

- **Objetivo:** separar el entusiasmo del contenido transferible.
- **Contenidos:**
  - La descripción del video aclara tres límites: el starter es «the starter foundation, rather than my complete personal setup», usa datos de muestra etiquetados, y «an installed TV app is not included». El README del repo (verificado el 2026-11-11) lista además lo que **no** trae: descubrimiento automático de dispositivos, login de Homey, integraciones hechas de NIBE/GoodWe/Shelly, facturación eléctrica, controles, cámaras y el APK de Android TV.
  - El código está en GitHub, MIT, verificado el 2026-11-11 (108 stars, creado el 2026-10-26, `pushed_at` del mismo día). Es un repo **de un solo día de vida**: sirve como base, no como dependencia a largo plazo.
  - Tampoco trae dependencias ni build: «No account, subscription, external scripts, analytics, npm dependencies, or build step» (README). El demo abre `public/index.html` directo en el navegador.
  - Lo que no hay en el video ni en el starter: pruebas del colector, manejo de errores de la lectura, retención de historial, ni qué pasa cuando el NAS falla.
- **Ejercicio:** listá los tres puntos de arriba que tu proyecto no cubre. **Entregable:** tres líneas. Es la lista de deuda del proyecto, no del video.

## Ejercicios por bloque

- [ ] M1 — Tres preguntas con fuente, en vivo/histórico y lectura/escritura (tabla de 3 filas).
- [ ] M2 — Camino mínimo a una lectura real, con la salida pegada.
- [ ] M3 — Lectura contrastada contra la pantalla del equipo, con la unidad escrita.
- [ ] M4 — Árbol de medidores con suma o diferencia por nodo.
- [ ] M5 — Tres estados (vivo/cero/sin dato fresco) y el criterio numérico de frescura.
- [ ] M6 — Un campo derivado reemplazando una cuenta a mano.
- [ ] M7 — Inventario de dispositivos con API utilizable (o la admisión de que el hub es la capa).
- [ ] M8 — Escritor vs. lector, y qué pasa con la captura si la máquina duerme una hora.
- [ ] M9 — Setup de TV escrito con modelo + OS + método de depuración (o descartado con motivo).
- [ ] M10 — Cinco métricas de la pantalla principal, cada una con su fuente.
- [ ] M11 — Tres cosas que el video no cubre y tu proyecto tampoco.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué el ponente se niega a convertir la lectura eléctrica en «cost» antes de validarla? ¿Qué clase de error evita esa negativa, y qué cuesta esperar?
2. El garage se **resta** del total y el cargador del auto **no se suma**. ¿Cuál es la regla única detrás de las dos decisiones? ¿Dónde la aplicarías en un proyecto que no sea de domótica?
3. «Si no hay una lectura fresca, el pulso se detiene»: ¿cuántos estados tiene un indicador honesto, y por qué dos no alcanzan?
4. ¿Por qué el `timestamp` de la lectura tiene que ser parte del registro y no un campo agregado por la vista?
5. El ponente elige Homey sobre Home Assistant. ¿Qué parte de ese razonamiento es una decisión y qué parte es su inventario de dispositivos? ¿Cuándo se invierte?
6. Separar la app del historial suena obvio hasta que alguien actualiza. ¿Qué diseño concreto hace que actualizar no borre datos, y cómo se prueba antes de necesitarlo?
7. ¿Qué se gana y qué se pierde al empezar con «un equipo, una pregunta» en vez de con la arquitectura completa?
8. De las once ideas del video, ¿cuál es la única que hoy podés convertir en un chequeo automático de tu trabajo? (La respuesta del curso está en `ADOPCION.md`.)

## Notas editoriales

- **Sin capítulos oficiales:** el video no trae `chapters`; el mapa temporal se derivó de los cues y se verificó con el barrido de timestamps (BAD: 0).
- **Duración:** 831 s según `lengthSeconds` del reproductor y `duration` de yt-dlp; el último cue cae en 00:13:45, seis segundos antes del cierre.
- **Repo verificado:** `prmgr-org/prmgr-observatory-starter`, MIT, 108 stars, creado 2026-10-26, último push el mismo día (API de GitHub, 2026-11-11).
- **Alcance del starter:** la descripción declara que no incluye la app de TV y que el demo abre con datos de muestra etiquetados. El README y `docs/DATA-FORMAT.md` del repo se leyeron el 2026-11-11 para los módulos 3, 5 y 11: el umbral de 10 minutos, la regla `null ≠ 0` y la lista de lo que no trae salen de ahí, no del ASR.
- **Afiliados:** la descripción incluye links de afiliado (Homey Pro, gear). No condicionan el contenido técnico, pero la recomendación de Homey viene de alguien que vende Homey por afiliado: se registra como sesgo posible, no como descalificación.
- **Lo que falta:** no hay medición de cuántas iteraciones llevó el proyecto, ni pruebas del colector, ni política de retención. Se nombra como hueco, no se estima.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
