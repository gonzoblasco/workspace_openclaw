# Clase: Crea tu Propia Miniserie con IA 100% GRATIS (Paso a Paso)

- **Fuente:** https://www.youtube.com/watch?v=imAI27aV-gU
- **Canal:** Edwin Arenas
- **Expositor:** Edwin Arenas (@edwin_arenas_ia)
- **Duración:** 25:37
- **Idioma:** español
- **Transcripción:** `transcripcion.md`
- **Plataforma:** [Google Flow](https://flow.google.com/) (plantilla *Storyboard Studio* + generación de vídeo)

## Resultado esperado

Al terminar la clase podés:

1. Convertir una idea en un **storyboard de 6 escenas** con guión, personajes, locaciones y objetos consistentes entre escenas.
2. Generar **clips de 10 s en 9:16, 720p** con Omni Flash, fijando personajes y props por `@mención` para que la IA no invente.
3. Continuar la producción cuando se acaban los créditos de una cuenta, sin perder el hilo de la historia.
4. Unir los clips en un capítulo de ~1 minuto (editor interno de Flow o editor externo).
5. Pedir a la herramienta una **continuación** que conserve personajes y agregue escenas nuevas.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 00:00 | Cold open: el capítulo terminado (hospital, Dr. Vega) |
| 00:59 | Promesa y presentación de Google Flow; el modelo de créditos diarios |
| 01:28 | Nuevo proyecto → Tools → plantilla *Storyboard Studio* |
| 01:58 | Escribir la idea (el prompt lo escribe ChatGPT) |
| 02:44 | Generar personajes, locaciones y objetos |
| 03:43 | Generar las imágenes de las escenas (4 por escena) |
| 04:14 | **Guardar la historia** (JSON) — el seguro contra perder el trabajo |
| 05:00 | Ajustes de generación: vídeo, 9:16, Omni Flash, 1 clip, 10 s, 720p |
| 06:14 | Escena 1: prompt + `@personaje` + `@objeto` + frame inicial/final |
| 09:13 | Revisar y descargar el clip 1 |
| 09:59 | Escena 2: consistencia de personajes |
| 12:42 | Pausa promocional (redes) |
| 12:57 | El límite: 3 vídeos por cuenta |
| 13:27 | Escena 3 y el límite alcanzado |
| 15:08 | **Rotación de cuentas**: cerrar sesión, abrir la historia guardada |
| 16:35 | *Auto-crear imágenes* para repoblar personajes/locaciones |
| 17:37 | Escena 4 con la cuenta nueva |
| 18:51 | Unir clips: editor interno vs. editor externo |
| 19:36 | Cuentas necesarias para un capítulo; 10 cuentas = 5 min/día |
| 20:22 | Unir los 6 clips en el editor de Flow |
| 22:08 | Capítulo completo terminado |
| 23:10 | Continuación: pedir 6 escenas más con los mismos personajes |
| 24:38 | Aritmética del sistema gratuito y cierre |

## Módulos

### Módulo 1 — La promesa y el modelo de créditos (00:59 – 01:28)

- Objetivo: entender qué produce la clase y cuál es el costo real.
- Contenidos:
  - El claim central: «Esta miniserie la hice totalmente gratis con una plataforma que nos regala créditos de manera diaria» (00:59).
  - Google Flow permite «capítulos de uno, de dos o hasta tres minutos diarios totalmente gratis» (01:14).
  - Los créditos se renuevan diariamente (01:28).
- Claims: es una **afirmación del ponente sobre su propia cuenta**, no una política pública de Google. Verificar el plan vigente de Flow antes de planificar un capítulo.
- Ejercicio: anotar cuántos créditos da una cuenta nueva hoy y a cuánto sale un clip de 10 s. Entregable: tabla `créditos disponibles / clips posibles`.

### Módulo 2 — Del prompt al storyboard (01:28 – 04:14)

- Objetivo: producir guión, personajes y escenas sin escribir nada a mano.
- Contenidos:
  - Nuevo proyecto → **Tools** → plantilla **Storyboard Studio** (01:28).
  - Storyboard Studio «actúa como un director de cine, nos hace el storyboard, nos crea los personajes, las escenas» (01:44).
  - El prompt de la idea lo redacta ChatGPT fuera de la herramienta: «Yo utilizo ChatGPT para crear la idea» (01:58).
  - Tres botones clave: **generar caracteres**, **generar locaciones**, **generar objetos** (03:13).
  - La herramienta genera **cuatro imágenes por escena** (04:30), pero para animar solo se usan dos.
- Claims: la calidad del storyboard depende del prompt de entrada, no de la herramienta. Es opinión sostenida por el flujo mostrado, no medición.
- Ejercicio: escribir un prompt de 1 minuto / 6 escenas con protagonista, secundario, antagonista implícito, locación y objeto característico. Entregable: el prompt en texto plano + el storyboard generado.

### Módulo 3 — Guardar la historia: el seguro (04:14 – 04:45)

- Objetivo: no perder el proyecto por un error de la página.
- Contenidos:
  - Menú de tres puntos → **guardar la historia** (04:14).
  - Motivo explícito: «puede que se presente algún error en la página, se borra todo y pues vamos a perder trabajo» (04:14).
  - Se descarga en formato **JSON** (ASR: «formato Jameson»).
  - Es también el mecanismo para **migrar el proyecto entre cuentas** (Módulo 6).
- Ejercicio: guardar, borrar el proyecto de prueba y reimportarlo. Entregable: archivo `.json` versionado (v1, v2) con nota de qué cambió.

### Módulo 4 — Configurar la generación de vídeo (05:00 – 06:14)

- Objetivo: fijar los parámetros correctos antes de gastar créditos.
- Contenidos (lo que el ponente configura, en orden):
  - Modo **vídeo** (no imagen).
  - Aspect ratio **9:16** (explícitamente para TikTok).
  - Modelo **Omni Flash**.
  - Cantidad de clips: **1** («muy importante que esté en uno»).
  - Duración **10 segundos**.
  - Calidad **720p**: «Calidad, yo sugiero que sea 720, 360 es un» (05:46).
- Claims: 720p es el mínimo razonable para publicar. Es recomendación, no medición.
- Ejercicio: generar el mismo prompt en 360 y en 720 y comparar lado a lado. Entregable: dos clips + conclusión escrita.

### Módulo 5 — Prompt con anclas `@` (06:14 – 09:13)

- Objetivo: que la IA no invente personajes ni objetos.
- Contenidos:
  - Pegar el prompt de la escena en el campo de texto (06:14).
  - Reemplazar cada aparición de un personaje por `@` + su ficha: Damián, Valeria (06:43).
  - Hacer lo mismo con los objetos: linterna táctica, mochila desgastada (06:58).
  - Justificación explícita: «IA va a empezar a inventar cosas» (07:13).
  - Elegir **fotografía inicial** y **fotografía final** entre las 4 imágenes generadas (07:43) — el *frame* condiciona el movimiento.
- Ejercicio: tomar una escena y reescribirla reemplazando **todos** los nombres y objetos por `@`. Entregable: la escena v1 (sin anclas) y v2 (con anclas), con veredicto de consistencia.

### Módulo 6 — El muro de los 3 vídeos y la rotación de cuentas (12:57 – 17:37)

- Objetivo: seguir produciendo cuando la cuenta se queda sin créditos.
- Contenidos:
  - «esta cuenta gratis me permite crear tres videos solamente» (12:57).
  - Al tercer vídeo: «ya me dice que no puedo crear más vídeos con esta cuenta» (14:52).
  - Los créditos: 5 restantes contra 15 por vídeo (15:08).
  - Procedimiento de rotación (15:21):
    1. Cerrar sesión.
    2. Iniciar sesión con **otra cuenta de Gmail**.
    3. Nuevo proyecto → Tools → plantilla Storyboard Studio.
    4. Tres puntos → **abrir historia** → cargar el JSON guardado.
    5. En personajes y locaciones: **auto-crear imágenes** para repoblar lo que la cuenta nueva no tiene (16:35).
    6. Regenerar solo las escenas que faltan; no tocar las ya hechas (17:06).
- Claims:
  - «Gmail permite hasta 15 cuentas con el mismo número de celular y es totalmente permitido» (15:21). **Verificar contra la política vigente de Google antes de replicarlo**: la afirmación es del ponente y no cita fuente. Rotar cuentas para esquivar límites de un servicio puede violar sus términos aunque el registro de cuentas sea legítimo. Etiqueta: anécdota/afirmación sin fuente.
  - Las imágenes de personajes y locaciones **no viajan** con el JSON de la historia; hay que regenerarlas por cuenta.
- Ejercicio: documentar paso a paso cuántas piezas del proyecto sobreviven a un cambio de cuenta y cuántas hay que regenerar. Entregable: checklist de migración.

### Módulo 7 — Unir los clips en un capítulo (18:51 – 22:08)

- Objetivo: entregar un capítulo continuo.
- Contenidos:
  - Flow tiene editor interno: subir los seis clips de una vez y pegarlos en orden (20:38).
  - El ponente **prefiere un editor externo**: «me gusta hacer la edición en un software, colocarlos, hacer los recortes, transiciones» (18:51); los editores internos «no son tan perfectos muchas veces».
  - Descargar un clip **no consume créditos**: «No les va a quitar créditos por» (20:06).
  - Recurso sugerido: pack de +1000 efectos de sonido sin copyright, enlazado en la descripción (21:37).
- Claims: re-descargar el mismo clip no cobra. Coherente con el modelo de créditos por generación, no por descarga.
- Ejercicio: montar los 6 clips en orden, agregar al menos 3 efectos de sonido y exportar. Entregable: capítulo de ~1 minuto.

### Módulo 8 — Continuación y aritmética del sistema gratuito (23:10 – 25:24)

- Objetivo: escalar de un capítulo a una temporada.
- Contenidos:
  - Para continuar: ir al script y pedir **«crea otras seis escenas de 8 segundos para darle continuación a la historia, mismos personajes»** (23:38).
  - La herramienta **agrega** escenas 7–10 sin borrar las anteriores y conserva los personajes (23:52).
  - Guardar la historia de nuevo al terminar la continuación (24:22).
  - Aritmética declarada: 1 minuto ≈ 2 cuentas; 10 cuentas ≈ 5 minutos/día ≈ 5 capítulos diarios (19:51, 24:38).
  - Cierre: «no importa lo difícil que sea el camino, si tienes una meta definida, siempre vas a encontrar la manera» (25:24).
- Claims: la aritmética es del ponente y depende de que los 3 vídeos por cuenta y la renovación diaria se mantengan. Etiqueta: estimación, no garantía.
- Ejercicio: escribir el prompt de continuación de un capítulo propio y verificar que las escenas nuevas no rompan la continuidad de vestuario ni de locación. Entregable: capítulo 2 con las mismas anclas `@`.

## Ejercicios por bloque

- [ ] **Bloque A (Módulos 1–2):** idea → prompt → storyboard de 6 escenas generado.
- [ ] **Bloque B (Módulos 3–5):** historia guardada en JSON; clip 1 generado con anclas `@` y frames inicial/final.
- [ ] **Bloque C (Módulo 6):** migración completa a una segunda cuenta documentada, con checklist de qué se regeneró.
- [ ] **Bloque D (Módulo 7):** capítulo de 1 minuto montado y exportado con efectos de sonido.
- [ ] **Bloque E (Módulo 8):** capítulo 2 generado como continuación, con continuidad verificada.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué el ponente reemplaza los nombres por `@` en el prompt? ¿Qué pasaría si no lo hace?
2. ¿Qué dos fotografías se eligen por escena y por qué esas dos y no las otras?
3. ¿Qué se pierde exactamente al cambiar de cuenta y qué hay que regenerar? ¿Por qué el JSON no alcanza solo?
4. ¿Cuál es el límite real de vídeos por cuenta y cómo se relaciona con la duración del clip?
5. ¿Dónde entra la edición externa que el ponente prefiere y por qué la considera mejor que el editor interno?
6. ¿Qué cambia al pedir una continuación en lugar de empezar un proyecto nuevo?
7. ¿Qué parte del método es replicable sin riesgo y qué parte exige leer los términos de servicio de Google antes de tocarla?
8. Si tuvieras que hacer un capítulo de 2 minutos en una sola cuenta, ¿qué parámetros cambiarías y qué perderías?

## Notas editoriales

- **No hay capítulos oficiales en la descripción.** El mapa temporal se derivó del transcript, no de un índice publicado.
- **Rotación de cuentas (Módulo 6):** se enseña como está en el video, pero queda marcado como afirmación sin fuente. Antes de aplicarlo hay que leer los términos de Google Flow sobre cuentas múltiples; el registro de varias cuentas de Gmail es legítimo, el uso para esquivar límites no necesariamente lo es.
- **Claims sin evidencia:** los límites de créditos (3 vídeos/cuenta, 15 créditos por vídeo, renovación diaria) cambian con el plan. Verificar antes de planificar.
- **Errores del ASR** consolidados en el glosario de `transcripcion.md`; el más dañino es «formato Jameson» por **JSON**.
- **Acciones externas:** publicar en TikTok/Instagram no forma parte de la clase; requiere OK de Gonzo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
