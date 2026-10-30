<!-- project: github.com/gonzoblasco/workspace_openclaw -->

# Glosario de narración en inglés (para grabaciones de Mercor)

> Criterio de Maven (29/10/2026): *"Your narration is judged on how it sounds, not on a
> certificate."* No hay mínimo CEFR. Lo que se evalúa:
> - claro, con sentido, profesional;
> - **se entiende a la primera**, sin repetir ni adivinar;
> - dice **qué estás haciendo y dónde en pantalla**;
> - **en inglés de punta a punta**.

---

## 1. La regla que ordena todo

**Cada acción se narra con tres partes en una sola frase: WHAT / WHERE / WHY.**

Fuente: cheat sheet oficial del proyecto.

> *"I am opening the filter... in the Status column header... to show overdue invoices."*

| Parte | Pregunta | Ejemplo |
|---|---|---|
| **WHAT** | ¿Qué hago? | "I am opening the filter..." |
| **WHERE** | ¿Dónde en pantalla? | "...in the Status column header..." |
| **WHY** | ¿Para qué? | "...to show overdue invoices." |

**El WHY es la parte que demuestra razonamiento. Sin WHY, es un tutorial de clics.**

Al cambiar de paso, numerá: *"Step 2: I'll now..."*

---

## 1b. Los límites exactos (fuente: manual oficial del proyecto)

| Regla | Número / criterio |
|---|---|
| **Arranque (START)** | **menos de 20 segundos** |
| **Silencio máximo** | **45 segundos**. Un gap mayor invalida esa parte de la toma |
| **Pausa ideal** | **menos de 30 segundos** |
| **Ventanas superpuestas** | **no más del 25 %, no más de 6 segundos** |
| **Epílogo** | objetivo **3 min**, máximo **4** |
| **Narración** | durante toda la toma, como un walkthrough paso a paso |
| **Narración y cursor sincronizados** | el cursor tiene que estar **sobre el ítem que nombra la narración** |
| **Atajos de teclado** | **anunciarlos antes o mientras los usás**: "I'm pressing Command + Shift + 4 to..." |
| **Rambling / filler** | prohibido. Ni "um", ni saltarse pasos con huecos |
| **Ruido de fondo** | tiene que no tapar la voz |

---

## 2. Frases de ubicación

Estas son las que más puntúan, porque el rubric las pide explícitamente.

### Dónde estoy mirando
- "On the **left sidebar**, I can see the project files."
- "In the **editor** on the right, the file is open."
- "At the **bottom**, in the terminal, the last command finished."
- "In the **tab bar at the top**, two files are open."
- "On the **top right**, the extensions panel."
- "In the **status bar at the bottom**, it shows the current branch."

### Dónde hago clic
- "I'm clicking the **file name** in the sidebar."
- "I'm opening the **Command Palette** with Command-Shift-P."
- "I'm switching to the **terminal tab**."
- "I'm scrolling **down** to the function definition."
- "I'm hovering over the **warning icon** on line 8."

### Movimiento
- "I'm going **back** to the sidebar."
- "I'm opening a **new tab**."
- "I'm splitting the view so I can see **both files at once**."
- "I'm closing this panel to get **more room** for the code."

---

## 3. Frases de acción (por fase)

### Al empezar
- "I'm going to reproduce the problem first, before changing anything."
- "Let me run the test to see the current failure."
- "I'll start by reading the error message."

### Al investigar
- "I'm opening the docs to confirm the method signature."
- "I'm searching the codebase for where this function is called."
- "I'm checking git blame to see when this line changed."
- "I'll look at the test file to understand what's expected."

### Al diagnosticar
- "The error says the property is undefined, so the object isn't being built before it's used."
- "This line returns `null` when the array is empty. That's the cause."
- "I found it. The loop starts at index 1 instead of 0."

### Al decidir
- "I have two options here: fix it in the caller, or in the function itself. I'll fix it in the function, because every caller has the same problem."
- "I'm choosing the smaller change, because it's easier to verify."
- "I'll avoid touching the other file, since it's out of scope for this task."

### Al corregir
- "I'm changing this condition from `>` to `>=`."
- "I'm adding a guard clause at the top of the function."
- "I'm moving this line above the lookup, so the value exists first."

### Al verificar
- "Now I'm running the test again."
- "The test passes. That confirms the fix."
- "I'm running the full suite to make sure nothing else broke."
- "The terminal shows zero failures."

### Al cerrar
- "The task is done: the bug is fixed and the test passes."
- "I'm saving the file and stopping the recording."

---

## 4. Cuando te trabás (y no querés silencio)

El silencio largo es lo que invalida una toma. Estas frases llenan sin mentir:

- "Let me think about this for a second."
- "I'm checking one thing before I continue."
- "I don't remember the exact name, so I'm going to look it up."
- "That's not what I expected. Let me re-read the error."
- "I'm going to try a different approach."
- "I was wrong about that. The value is actually here."

**La última es la más valiosa**: admitir un error en voz alta demuestra razonamiento real. El rubric premia eso, no la perfección.

---

## 5. Trampas de inglés (B2+)

| Trampa | Qué hacer |
|---|---|
| **Muletillas**: "um", "eh", "you know" | Pausá en silencio una fracción de segundo. Se nota menos |
| **Frases largas** | Cortá: "Two things. First, the test fails. Second, the value is null." |
| **Traducir nombres técnicos** | `array`, `string`, `commit`, `branch`: se dicen en inglés, siempre |
| **Pronunciar mal los nombres de archivo** | Si el archivo se llama `parser.ts`, decí "parser dot tee ess" |
| **Silencio mientras leés** | Leé en voz alta lo que estás leyendo: "The error says..." |
| **Empezar con "So..."** | Es muletilla. Arrancá con el hecho: "The test fails on line 12." |

---

## 6. La estructura completa de la grabación

Fuente: cheat sheet oficial. Tres fases con reglas propias.

### Antes de apretar Record

- [ ] **Accessibility Inspector corriendo**, con la ventana cerrada, y el **Dock dot visible**
- [ ] **TaskRecorder**: description y apps correctos
- [ ] **Ventanas no usadas cerradas**

### 1. START (menos de 20 segundos)

1. **Mostrás el Goal aprobado.**
2. **Minimizás TaskRecorder.**
3. Decís **solo**: *"I will be beginning my task soon. Here is the workflow I have in mind."*
4. **Ocultás el Goal.** No lo leas, no lo expliques.

### 2. DURING

- Al cambiar de paso: *"Step 2: I'll now..."*
- Cada acción, con **WHAT / WHERE / WHY**.
- **El cursor sobre el control** que nombrás.
- **Anunciá los atajos** antes o mientras los usás.
- Las screenshots nativas de macOS están permitidas para el trabajo.

### 3. FINISH

- **A)** Mostrás el archivo guardado, explicás los chequeos, confirmás el resultado.
- **B)** **Epílogo: 3 minutos objetivo, máximo 4.** Estructura: **resultado · decisiones · desafíos · mejoras**.
- **C)** Anunciás que terminaste y **parás la grabación**.

---

## 6b. Estructura mínima de una narración de 3 minutos

| Tiempo | Qué decís |
|---|---|
| 0:00-0:30 | **Qué vas a hacer**: "I'm going to fix a failing test in this small project." |
| 0:30-1:30 | **Reproducir y diagnosticar**: "The test fails here. The error says... Let me find where this is called." |
| 1:30-2:30 | **Corregir**: "The problem is this line. I'm changing it because..." |
| 2:30-3:00 | **Verificar**: "Now the test passes. The task is complete." |

**Ensayo gratis (lo dice Maven):** practicá 3 minutos en voz alta **sin grabar**. Es la mejor preparación que existe, y no cuesta nada.

---

## 7. El ensayo de ubicación (ejercicio de 5 minutos)

Antes de grabar la primera tarea, hacé esto:

1. Abrí cualquier proyecto.
2. Hablá 3 minutos en voz alta, narrando **solo ubicación**: dónde mirás, dónde hacés clic, qué ves.
3. Sin explicar conceptos. Solo posición y acción.
4. Grabate con el celular y escuchá: ¿se entiende a la primera?

Si te escuchás y no sabés dónde estabas mirando, el oyente tampoco.

---

## 7b. Preparar la tarea ANTES, nunca dictarla durante

La investigación y el plan se hacen **antes** de grabar; durante la grabación se ejecuta solo lo que
**ya se sabe**. Dictar pasos en vivo convierte al que graba en ejecutor de un guion, y el evaluador
lee a alguien leyendo, no a alguien razonando.

Lo que se prepara antes y se entrega **escrito**:

1. **Criterio de selección**: objetivo claro, inicio y fin definidos, secuencia con sentido,
   resultado verificable, solo apps aprobadas, cero datos privados, idea propia.
2. **Las URLs exactas** y **qué buscar en cada una**, no solo el tema.
3. **Los pasos** con el punto de decisión de cada uno.
4. **El proyecto ficticio ya armado** en un directorio neutro, con el defecto o estado inicial listo.
5. **Las trampas de esa tarea**: qué ventana no abrir, qué app no tocar, dónde no mirar.

**La primera tarea va del dominio donde hay evidencia real y resultado verificable** (un test que
falla y pasa), no una que impresione: el rubric castiga la complejidad.

---

## 7c. La línea de la IA: prepara antes, el razonamiento grabado es tuyo

**El motivo no es que puedan detectarlo.** La detección existe (*"submissions evidently produced by
AI will be flagged"*), pero el argumento real es otro: si la IA escribe la narración, el evaluador
está viendo el razonamiento de un modelo, no el tuyo. Y el dato de entrenamiento aprende a usar el
modelo.

| Práctica | Estado |
|---|---|
| Autocompletado del editor (IntelliSense) | Permitido: no es IA de terceros |
| Asistente de IA integrado en el IDE | Zona gris: preguntar por escrito |
| Pedir a un modelo que escriba lo que se graba | Prohibido |
| IA en trabajo propio **no grabado** | Fuera del alcance |
| **Gemini antes de grabar** (inputs, brainstorming) | Permitido por el manual del proyecto |
| Idea de la tarea generada por IA | **Prohibido, siempre** |

Lo que se puede pedir antes es **el plan y el qué hacer**. Lo que no se delega es **el qué decir**.

---

## 7d. El directorio de trabajo va fuera del repo

El proyecto que se graba vive en el **home del perfil dedicado** (`~/odin-work/` o equivalente), no
dentro del workspace: dentro del repo se commitea o ensucia el `git status`, y además es material del
cliente que no se mezcla con el código propio. Si hay que dejar constancia, se documenta la **ruta y
el porqué** en la carpeta del proceso, no se aloja ahí.

---

## 7e. Un pipeline es una skill, no un agente

Un pipeline fijo (investigar, planificar, entregar pasos y guion) es una **skill**, no un rol. Un
agente nuevo consume modelo, contexto y memoria propia, exige sus archivos de identidad y su gate de
frontera, sin agregar criterio que la skill no tenga. **Y el nombre dice qué produce, no qué persona
sería**: "preparación de tarea", no "profesor" ni "maestro".

---

## 7f. Separar tres cosas que se confunden al pedir "un perfil limpio"

| Concepto | Qué es | Cómo se resuelve |
|---|---|---|
| **Perfil de usuario del SO** | La cuenta de macOS/Windows | Usuario nuevo, home propio |
| **Identidad del sistema visible** | `user@host` en terminal y títulos | El usuario nuevo lo resuelve |
| **Cuentas personales en pantalla** | Mail, navegador, avatares | Cerrar o silenciar, **no renunciar** |

**No hace falta renunciar a las cuentas.** El requisito es que nada personal aparezca **en la
grabación**. Distinguí "perfil sin iCloud" (pierde acceso) de "perfil con iCloud y notificaciones
apagadas" (no pierde nada). La segunda como default; la primera solo si se pidió máximo aislamiento.

**Cuando el trabajo es recurrente, el perfil nuevo deja de ser opcional**: el nombre de usuario del
SO aparece en cada terminal, en cada barra de título y en cada prompt de shell. Es el punto que
decide si el trabajo a largo plazo es sostenible.

---

## 7g. Precedencia de la fuente

Cuando el proyecto publica un manual, cheat sheet o guías internas, **esas guías priman sobre la
interpretación del contrato y sobre cualquier consejo previo**. Si contradicen algo ya dicho, se
corrige la instrucción, no se sostiene la versión anterior.

| Orden | Fuente |
|---|---|
| 1 | **Guías y manual del proyecto** (Slack, docs compartidos, cheat sheet) |
| 2 | **Contrato firmable** (Offer Letter, Worker Agreement, CIIAA) |
| 3 | Documentación pública del proveedor |
| 4 | Consejo previo, incluido el de esta skill |

Los links de documentos compartidos suelen requerir login: **pedir la exportación a PDF** en vez de
asumir que no hay contenido. Después de leer, archivar las capturas o el PDF como evidencia y citar
de ahí.

---

## 8. Lo que NO decir

- **"As you can see..."** - el oyente no ve nada, está escuchando.
- **"Basically..."** - muletilla, y sugiere que lo anterior no fue claro.
- **"This is simple..."** - descalifica y no aporta.
- **"I'm just..."** - minimiza. "I'm changing this line", no "I'm just changing".
- **Cualquier cosa en español**, incluso un "bueno" o "dale". El rubric pide inglés de punta a punta.
- **El Goal completo recitado**: mostrar el Goal es correcto (START, menos de 20 s); **leerlo o explicarlo** es el error. Decí las dos frases y ocultalo.
- **Cualquier mención a Mercor, Project Odin, Studio, Writer Guidelines o materiales del proyecto.** La info del proyecto es PII: el propio handbook está marcado "PII EXPOSED". Tampoco tengo que tener esas guías abiertas en pantalla.

---

## 8b. El cursor es parte del rubric (Mouse Movement Requirements)

Esto no es obvio para un developer, y es donde más se falla.

| MUST DO | MUST NOT |
|---|---|
| Movimiento **intencional**, que avanza la tarea | **Aimless activity**: círculos o jitter sin intención |
| **Teaching pointer**: el cursor sobre el ítem que nombra la narración | **Keyboard overuse**: atajos de teclado cuando se podría usar el mouse |
| Inactividad **menor a 45 s**, pausas de **menos de 30 s** | **Inactivity & pauses**: cursor quieto más de 45 s |

**Para un dev, `Keyboard overuse` es el riesgo #1.** El hábito es `⌘⇧P`, `⌘T`, todo por teclado. En Odin eso **puntúa mal**: quieren ver el mouse moviéndose al elemento. Si podés hacerlo con mouse, hacelo con mouse.

**Pero los atajos puntuales SÍ están permitidos si los anunciás**: *"I'm pressing Command + Shift + 4 to take a screenshot of the filtered table."* El problema no es usar el atajo: es usarlo **en lugar** de señalar con el mouse, sin decirlo.

---

## 8c. El escritorio tiene que NO parecer una Mac nueva (UI Diversity)

Esto es requisito, no preferencia. La Mac con settings default descalifica.

| DO NOT (Mac default) | DO THIS INSTEAD |
|---|---|
| Fondo Tahoe Day (playa) | Fondo no-default |
| Modo claro | **Modo oscuro** |
| **Dock abajo** | **Dock a la izquierda o derecha, nunca abajo** |
| Tema automático, highlight azul | Tema Purple, highlight amarillo |
| Iconos default del publisher | Iconos de app oscuros |
| Cursor de tamaño/color cambiado | **Cursor default, siempre** |

Además: se pueden variar fondo, resolución, modo, color de tema, tamaño del Dock, layout.

---

## 8d. Window Management

| GOOD | BAD |
|---|---|
| Una ventana activa, limpia | Hide menu bar, clock o dock |
| Ventanas grandes y legibles | Full-screen mode / full-screen split |
| Minimizar las apps no usadas | Ventanas flotantes chicas |
| Side-by-side cuando hace falta | Stack, overlap, push windows |
| Popups de la misma app pueden superponerse | **Overlap del 25 % o más por más de 6 segundos** |

---

## 9. Antes de grabar: el checklist de idioma

- [ ] La UI está **en inglés** (macOS, VS Code, terminal).
- [ ] Los nombres de archivos y carpetas están **en inglés**.
- [ ] Practicaste 3 minutos en voz alta.
- [ ] Tenés a mano las frases de ubicación de §2.
- [ ] Sabés dónde NO mirar (nada de apps personales).
