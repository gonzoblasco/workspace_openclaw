# Clase: I Built This Interactive 3D Website With AI (Gemini 3.8 Flash)

- Fuente: https://www.youtube.com/watch?v=y1pM7bS6IY8
- Canal: MiladiCode
- Expositor / speaker: MiladiCode (no declara nombre propio en el video)
- Duración: 13:01
- Idioma: inglés (captions automáticos `en-orig`)
- Transcripción: transcripcion.md
- Fecha de publicación: 2026-09-06

## Resultado esperado

Al terminar la clase, poder:

1. Convertir dos imágenes de referencia en un **frame sequence** con transición continua (extremo a extremo), sin depender de una herramienta específica.
2. Montar una **hero section con animación dirigida por scroll** sobre ese frame sequence, con el número de frames y la ruta del asset como parámetros del prompt, no como números mágicos en el código.
3. Construir un **logo carousel infinito de dos filas en direcciones opuestas** sin costuras, y un **bento grid** de cards.
4. **Generar un GLB a partir de una imagen** y integrarlo en una sección con react-three-fiber, verificando que carga en el bundle y no rompe el build.
5. Usar **screenshots como referencia visual** en el prompt a un agente para corregir layout (el bucle del video), separando diseño de lógica.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 00:00 - 00:55 | Promesa: qué se construye y qué se usa |
| 01:06 - 01:33 | Workflow agnóstico de herramienta; la regla "el video no enseña a diseñar, enseña a dirigir" |
| 01:33 - 02:15 | Moodboard: dos imágenes como primer y último frame |
| 02:15 - 03:07 | Preparación de imágenes: calidad, 16:9, mismo estilo |
| 03:07 - 04:34 | Image-to-video con prompts de movimiento; extracción de frames |
| 04:34 - 05:00 | Scaffold de Next.js en el directorio actual (la barra final) |
| 05:00 - 07:37 | Hero section: de referencia a diseño, y corrección por screenshot |
| 07:37 - 09:04 | Carousel infinito + bento grid; correcciones visuales |
| 09:04 - 10:44 | De imagen a GLB (Tripo): best quality vs smart mesh, texturizado, export |
| 10:44 - 12:04 | Sección 3D: referencia, asset en `public/`, reemplazo del placeholder por el modelo |
| 12:04 - 13:01 | Cierre: pulido, footer y la idea de fondo (iterar con instrucciones) |

## Módulos

### Módulo 1 - El workflow, y por qué sirve aunque cambies de herramienta (00:00:00s - 00:01:33s)

- Objetivo: entender qué se está automatizando y qué sigue siendo decisión humana.
- Contenidos:
  - El resultado es una plataforma de generación de imagen y video, no una landing: «we're going to create a fully interactive AI-powered image and video generation platform» (00:00:15).
  - Todo el proceso lo hace un agente, incluidos los assets: «we'll be using AI throughout the entire process, from creating our visual assets and animations to designing the sections and writing the code» (00:00:40).
  - La herramienta es intercambiable; lo que se enseña es la secuencia: «I'm going to be using Antigravity, but you can absolutely follow along using any other AI tool or IDE you prefer» (00:01:06).
- Claim a etiquetar: **anécdota**, no evidencia. El video muestra que *él* llegó a un resultado en minutos por sección; no compara calidad ni mide el tiempo de forma reproducible.
- Ejercicio: escribir en una hoja el pipeline en 6 pasos (moodboard → imágenes → video → frames → código → correcciones) y marcar, por paso, qué decisión es humana (qué se ve bien) y qué es delegable (generarlo, medirlo, escribirlo).

### Módulo 2 - Moodboard: dos imágenes no son inspiración, son los extremos de una animación (00:01:33s - 00:02:15s)

- Objetivo: entender que la primera decisión creativa es elegir el **par** de frames, porque de ahí sale toda la coreografía del scroll.
- Contenidos:
  - «I found this image that I really like, and I want to use it as the first frame of an animation. Then, for the final frame, I'm going to use this second image» (00:01:44).
  - El objetivo no es un video bonito: es material para el scroll: «use that animation to build the scroll-based experience for our hero section» (00:01:58).
  - Plataformas de referencia citadas: Dribbble y Pinterest.
- Ejercicio: elegir dos imágenes que puedan ser 0 % y 100 % de un mismo movimiento (mismo encuadre, distinta cámara/posición) y justificar en una frase por qué el salto entre ellas se puede interpolar.

### Módulo 3 - Preparación de imágenes: lo aburrido decide si la animación sale limpia (00:02:15s - 00:03:07s)

- Objetivo: dejar las dos imágenes con la misma proporción y el mismo estilo antes de gastar generaciones.
- Contenidos:
  - La primera imagen: mejorar calidad y 16:9: «enhance the image quality and convert it to a 16:9 aspect ratio» (00:02:32).
  - La segunda: alinear estilo y color con la primera, y la misma proporción: «adjust the colors so that it matches the first frame more closely» (00:02:49), «convert the image to 16:9 so both images have exactly the same dimensions» (00:02:53).
  - Regla implícita y reutilizable: **la consistencia se prepara antes de generar, no se pide después**.
- Ejercicio: tomar dos imágenes cualquiera y producir el par final con la misma resolución exacta; verificarlo con `sips -g pixelWidth -g pixelHeight` (macOS) y anotar la diferencia si la hay.

### Módulo 4 - Image-to-video y el frame sequence: 24 a 60 imágenes haciendo de animación (00:03:07s - 00:04:34s)

- Objetivo: producir los frames del scroll y entender por qué se usa un video en vez de CSS.
- Contenidos:
  - Renombrar los archivos antes de subirlos: «I'm going to rename the files so it's immediately clear which image is the first frame and which one is the last frame» (00:03:19). Dato menor, pero evita el error más común (invertir el par).
  - El prompt de video es una **especificación de movimiento**: «describe the movement, camera motion, transitions, lighting, atmosphere, and other visual details I want the AI to preserve» (00:03:42).
  - Se puede cambiar de modelo sin cambiar de flujo: «if you're not satisfied with the results of your video, you can simply change the model and try again» (00:04:04). Seedance 2.5 fue el que le funcionó (00:04:10).
  - Extracción de frames con el agente o con un sitio aparte: «You can also use websites like EasyGIF, where you can upload the video and extract the individual frames» (00:04:21).
- Lo que el video **no** enseña y hay que decidir: cuántos frames, a qué resolución y con qué peso. En un hero a pantalla completa, 60 frames de 1920×1080 sin comprimir son ~370 MB de PNG; es el punto donde la técnica se cae en producción. Ver `ADOPCION.md`.
- Ejercicio: extraer 60 frames de un video de 2 s con `ffmpeg -i in.mp4 -vf fps=30 frames/%04d.webp` y medir el tamaño total del directorio. Repetir en WebP con calidad 80 y comparar.

### Módulo 5 - Scaffold de Next.js en el directorio actual (00:04:34s - 00:05:00s)

- Objetivo: arrancar sin carpetas anidadas de más.
- Contenidos:
  - Instalación desde nextjs.org y **la barra final** del comando: «don't forget to add the slash to the end of the command, so it installs the Next.js project in the current directory» (00:04:51).
  - Es el único momento donde el video da un comando concreto. El resto lo hace el agente.
- Ejercicio: correr `create-next-app` dos veces, una con `.` y otra con `/`, y describir en una línea la diferencia de estructura resultante.

### Módulo 6 - Hero section: referencia → diseño → corrección (00:05:00s - 00:07:37s)

- Objetivo: reproducir el bucle real de trabajo con un agente visual, que no es "un prompt y listo", sino tres pasadas.
- Contenidos:
  - **Pasada 1, la referencia**: «recreate this exact design, but optimize it so it matches our own brand and project details» (00:05:16). El screenshot de Pinterest es la entrada del prompt.
  - **Pasada 2, quitar lo que estorba la animación**: «remove this image from the center, and I also want to remove any background effects so we can apply the scroll animation in the next step» (00:05:39). Es preparación, no estética.
  - **Pasada 3, corregir contraste**, y el hallazgo del video: «because of the color of the background, our text is not fully visible» (00:06:57) → headline más bold + sombra. La sombra es un parche: el problema es elegir texto y fondo sin verificar contraste (ver `ADOPCION.md`).
  - El tercer prompt lleva **una segunda referencia visual** refinada fuera del agente (ChatGPT): «I'm going to attach this image to the prompt as a reference as well» (00:07:18).
- Ejercicio: escribir el prompt del hero en tres partes separadas (estructura, limpieza para la animación, contraste) en vez de uno solo, y anotar qué parte el agente cumple a la primera y qué parte necesita ver un screenshot.

### Módulo 7 - Scroll-driven animation: los tres parámetros que hay que reemplazar a mano (00:05:55s - 00:06:48s)

- Objetivo: entender por qué el prompt del scroll no se puede pegar tal cual.
- Contenidos:
  - El número del último frame tiene que coincidir con el zip: «For the last frame number, you need to make sure that it matches the exact same number in your zip file» (00:06:04).
  - El patrón del nombre del archivo tiene que coincidir con los nombres reales, **en dos lugares**: «make sure that the frame image name matches the actual image names inside your zip file. And make sure to update that in the scroll logic section as well» (00:06:15).
  - La ubicación del zip/ruta del asset también va en el prompt: «you need to mention the location of the zip file here» (00:06:25).
  - Resultado: scroll suave (00:06:53) con un efecto que el video describe como perfecto.
- Lección transferible, y es la más fuerte del video: **lo que cambia entre corridas va en el prompt como variable, no incrustado en el código**. Si el count de frames está escrito en dos lugares, el tercer lugar (el zip) va a desincronizarse.
- Ejercicio: escribir un prompt parametrizado (`FRAME_COUNT`, `FRAME_PATTERN`, `ASSET_PATH`) y verificar que la generación no deja ninguno de esos valores hardcodeado con `grep -rn "00[0-9][0-9]" app components`.

### Módulo 8 - Carousel infinito y bento grid (00:07:37s - 00:09:04s)

- Objetivo: dos patrones de layout que se repiten en cualquier landing.
- Contenidos:
  - **Carousel de dos filas en direcciones opuestas**: «The first row will continuously move from right to left, while the second row will move in the opposite direction» (00:07:46).
  - **Bento grid debajo**, con referencia de Pinterest propia (00:07:59).
  - Corrección por screenshot, otra vez: «we have some design problems with these three cards that need to be fixed. So, I'll go ahead and take a screenshot of them» (00:08:30).
  - Correcciones de detalle no delegables a un texto: quitar el contenedor de cada logo y pasarlos a blanco y negro (00:08:38 - 00:08:43).
- Claim: «fix everything for us in about a minute» (00:08:55) es **anécdota de sesión**, no un benchmark.
- Ejercicio: implementar el carousel con dos `@keyframes` de dirección opuesta y `animation: ... infinite linear`, duplicando la lista de logos; verificar que no hay salto visible en el punto de unión (grabación de pantalla de 10 s).

### Módulo 9 - De imagen a GLB: best quality vs smart mesh (00:09:04s - 00:10:44s)

- Objetivo: obtener un modelo 3D usable en web desde una sola imagen, sabiendo el costo de cada modo.
- Contenidos:
  - **La preparación de la imagen manda**: quitar fondo, piso y texto antes de generar: «I need to prepare the image by removing the background, the land, and the text from it» (00:09:19). Lo hace con ChatGPT (00:09:26), y prueba sacar y volver a poner la escalera (00:09:30 - 00:09:36): iteración sobre la referencia, no sobre el modelo.
  - Herramienta: Tripo (dicho «Trepo»), AI 3D model builder (00:09:45).
  - Dos modos: **best quality** y **clean topology** (00:09:54). Elige best quality (00:09:57).
  - Segunda pasada con **smart mesh + generate multi-views**, y después **texture** (00:10:06 - 00:10:28). El resultado texturizado «actually looks better than the previous result» (00:10:31).
  - Export en **GLB**, con la razón explícita: «make sure to export it in GLB format, since that's the format we're going to use later to integrate our 3D model into the website» (00:10:36).
- Lo que no se dice y hay que saber: clean topology es la opción correcta para un modelo que va a animarse o deformarse, no para un hero estático; y el peso del GLB (típicamente 3-20 MB) es el número que decide si la sección es usable.
- Ejercicio: generar el mismo modelo en los dos modos y comparar peso de archivo y número de triángulos (abrir el GLB en un visor que muestre stats). Escribir una regla de cuál usar según el destino.

### Módulo 10 - Integrar el GLB: asset primero, sección después (00:10:44s - 00:12:04s)

- Objetivo: poner el modelo dentro de una sección sin que el agente adivine rutas.
- Contenidos:
  - Nueva sección con referencia visual propia (00:10:50), generada mientras mueve el asset: «create a new folder inside the public folder and name it 3D model, and then I'll drag and drop the 3D model right inside this folder» (00:11:11).
  - **Reemplazo explícito del contenedor**, con la ruta del GLB al final del prompt: «ask the agent to remove this section and replace it with my 3D model. And at the end of the prompt, I also need to provide the path to my 3D model GLB file» (00:11:35).
  - El screenshot del contenedor como ancla espacial: «take a screenshot of this large container» (00:11:32).
  - Resultado: los elementos funcionales, no mockups: «not just simple mock-up designs. Everything is working just like a real 3D platform» (00:11:58).
- Ejercicio: integrar un GLB en una sección con `@react-three/fiber` y `useGLTF`, con `Suspense` y un fallback visible; verificar con `npm run build` que el loader no rompe el server component y que el primer render no bloquea el LCP más de 200 ms.

### Módulo 11 - Cierre: pulir es seguir dirigiéndonos, no escribir (00:12:04s - 00:13:01s)

- Objetivo: entender el límite del método.
- Contenidos:
  - Cambios finales en un solo mensaje: colores y fondo de la sección (00:12:08), imágenes de las bento cards (00:12:15), footer (00:12:20).
  - La tesis: «you can add, remove, edit, and customize almost anything in your project simply by giving your AI agent the right instructions» (00:12:22).
  - La palabra clave es **right instructions**. Todo el video es, en realidad, una demostración de que la calidad del resultado depende de la calidad de la instrucción y de la referencia visual: cinco de las once secciones del video son prompts con screenshot.
  - Los prompts completos están en la descripción (Notion), no en el video: sin ese link, los ejercicios son reconstrucción.
- Ejercicio: reescribir el cierre del proyecto como una lista de instrucciones con su ancla (screenshot, ruta, número); la que no tenga ancla, se marca como pendiente de referencia.

## Ejercicios por bloque

- [ ] M1: pipeline en 6 pasos con la columna "humano / delegable".
- [ ] M2: par de imágenes 0 % / 100 % con justificación de interpolación.
- [ ] M3: dos imágenes con la misma resolución exacta, verificadas con `sips`.
- [ ] M4: 60 frames extraídos en WebP y peso total medido; comparación contra PNG.
- [ ] M5: diferencia estructural entre `.` y `/` en `create-next-app`.
- [ ] M6: prompt del hero en tres pasadas separadas.
- [ ] M7: prompt parametrizado + `grep` que confirma cero valores hardcodeados.
- [ ] M8: carousel de dos filas sin salto visible en el loop.
- [ ] M9: mismo modelo en los dos modos, con peso y triángulos comparados.
- [ ] M10: GLB integrado con `Suspense` y build verde.
- [ ] M11: instrucciones finales con ancla, o marcadas como pendientes.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué el video prepara las dos imágenes en el mismo 16:9 antes de generar el video, en vez de recortar después?
2. El scroll animation usa frames en vez de un `<video>` en loop: ¿en qué casos esa elección gana y en cuáles es un error de rendimiento?
3. ¿Qué se rompe si el `FRAME_COUNT` del prompt no coincide con el zip, y por qué el author insiste en actualizarlo en dos lugares?
4. ¿Cuándo conviene **clean topology** y cuándo **best quality** en un modelo que va a la web?
5. El video arregla el contraste del headline con una sombra. ¿Cuál es la corrección de fondo, y cómo se verifica sin mirar?
6. ¿Qué cinco momentos del video usan un screenshot como referencia, y qué tienen en común?
7. El cierre dice "with the right instructions". ¿Qué hace que una instrucción sea "right" en este flujo: la longitud, la referencia visual o la parametrización?
8. ¿Qué parte de este pipeline no se puede delegar a un agente, y por qué?

## Notas editoriales

- **Discrepancia de modelo:** el título y la descripción dicen Gemini 3.8 Flash; el cue de 00:05:29 dice «3.6». Se registra sin corregir el transcript.
- **Nombres deformados por el ASR:** Runable/Runnable, Tripo/Trepo, EasyGIF/ezgif, Bento. Glosario en `transcripcion.md`.
- **RunDiffusion (00:02:20):** el ponente lo dice, pero el flujo descrito (imagen + video + frames en un agente, y luego «Runnable has completed the task») corresponde a Runable. No se edita el cue; queda como desliz registrado.
- **Prompts:** están en un link de Notion, fuera del video. Esta clase enseña el método, no reproduce los prompts.
- **Claims sin fuente:** tiempos por sección («a few minutes», «about a minute») y calidad comparativa entre modos de Tripo. Son anécdotas de sesión.
- **Acción externa:** los links de Runable y Tripo llevan UTMs de afiliado. No se abren ni se registran cuentas sin el OK de Gonzo.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
