---
name: "task-prep"
metadata:
  category: "Career"
  tags:
    - mercor
    - odin
    - grabacion
    - narracion
    - task-recording
description: "Preparar una tarea de grabacion de pantalla (Mercor Project Odin y similares) ANTES de grabar: criterio de seleccion, investigacion previa, pasos, guion de narracion, entorno limpio y checklist de validez."
user-invocable: true
---

# Workflow: Task Prep (grabaciones narradas para Mercor)

> **Fuente de verdad:** `Project Odin Writer Handbook` (135 paginas) y la transcripcion de
> `Project Odin - First Task Orientation`, ambos en `docs/entrevistas/mercor-project-odin/`.
> Si esta skill y el handbook difieren, **gana el handbook** y se corrige la skill.
>
> **Que hace:** prepara una tarea para grabarla. **No la ejecuta y no ayuda durante la
> grabacion.** La IA puede ayudar a *pensar* antes, nunca a producir mientras se graba.

## 0. Que es el puesto

> *"You will record your computer screen while completing professional tasks across several
> domains, narrating what you are doing, where you are doing it, and why."*

Tres actividades por tarea: **planificar y preparar → grabar y narrar → validar y subir**.
**No hay webcam ni filmacion de la persona.** Solo pantalla.

### Los 18 dominios

| Dominio | Abrev. | | Dominio | Abrev. |
|---|---|---|---|---|
| Architecture | ARCH | | Finance | FIN |
| Audio & Music Production | AUD | | Marketing; Sales & Biz Dev | GTM |
| Consulting & Business Ops; Product Mgmt | BUSI | | Healthcare & Life Sciences | HLS |
| Design (Graphic / UX / UI) | DES | | HR & People Ops | HR |
| **Data Science & Analytics; Software & AI/ML Eng.** | **DSD** | | Photography | IMG |
| Education | EDU | | IT Support | IT |
| Engineering (Non-Software) | ENG | | Legal | LAW |
| Research & Academia | RNA | | Content & Writing | TEXT |
| Animation & VFX | VFX | | Video | VID |

**La primera tarea va en el dominio con evidencia mas fuerte.** El perfil de Gonzo cae en **DSD**
(10+ anos, React/TS, 11 PRs, accesibilidad). IMG, VID y TEXT son secundarios defendibles.

## 0b. La regla de la IA

| Momento | Permitido | Prohibido |
|---|---|---|
| **Antes** | **Gemini unicamente**: preparar input files, brainstorming. Watermark de Gemini permitido | **Generar las ideas de la tarea** con IA. Otros watermarks |
| **Durante** | Nada | Mostrar o interactuar con herramientas de IA; generar o revisar el contenido |
| **Despues** | Debrief | - |

**El motivo no es la deteccion: es contaminar el dato.** Si el modelo ve un LLM resolviendo, aprende
eso. Y el razonamiento grabado tiene que ser del que graba.

## 1. Criterio de seleccion

### El test del amigo (el filtro principal)

> *"Ask yourself: 'Can your friend with no domain expertise complete this task?' If yes, choose a
> task that better uses your domain skills."*

### Los criterios

1. **Dominio real**: usa el conocimiento y el juicio de un experto del dominio elegido.
2. **Objetivo claro** en una frase.
3. **Resultado util y verificable**: un test que pasa, un archivo que existe, un numero que cambio.
4. **Complejidad por decisiones, no por pasos**: *"Complexity comes from the decisions you make,
   not from adding extra steps."*
5. **Duracion**: **15 a 20 minutos** para la primera tarea. *"Shorter tasks are easier to get right
   in one recording take."* Si tiene muchos pasos, **se puede partir en dos tareas**.
6. **Apps**: **3 preferidas cuando aportan**; menos (incluso una) si la tarea es lo bastante
   compleja. *"Opening extra apps does not establish complexity."*
7. **Idea propia**, no generada por IA.

**Para la primera: simple y conocido.** Un bug acotado con test que falla y test que pasa.

## 2. La propuesta: cinco campos

El formulario de Studio pide, literal:

```
Domain / Role:
Goal:
Starting materials:
Steps (with the apps for each):
Deliverable:
```

- **Starting materials**: de cero o con material existente. Si hay inputs, se preparan **antes** y
  cumplen privacidad, licencia y disclosure.
- **Steps**: cada paso con la app donde ocurre.
- **Deliverable**: el resultado concreto que queda.

**Esperar la aprobacion antes de grabar.** Si el plan cambia de forma material, pedir el cambio y
esperar otra aprobacion.

## 3. Los TRES lugares del Goal

Una vez aprobada la idea, Studio **llena solo** el idea completo y cambia el estado a
**In progress**. De ahi se copia **solo la seccion Goal, palabra por palabra**, a **tres** lugares:

| # | Donde |
|---|---|
| 1 | `TaskRecorder` |
| 2 | El documento de apertura (opening document) |
| 3 | Seccion **Request** de `metadata.rtf` |

**No se reescribe: se copia.** El cuarto lugar (la propuesta) ya lo completo Studio.

### metadata.rtf: apps en orden de uso

> *"List each app in the order you use it, **listing an app again each time you return to it**."*

Si vas VS Code → Terminal → VS Code, la lista es: VS Code, Terminal, VS Code. No se agrupa.

## 4. Narrar: WHAT / WHERE / WHY

**Cada accion, en una frase:**

> *"I'll click the blue export button in the top right corner to save the report."*

| Parte | Pregunta |
|---|---|
| **WHAT** | que hago |
| **WHERE** | donde en pantalla |
| **WHY** | para que |

- Al cambiar de paso: *"Step 2: I'll now..."*
- **Nombrar los controles** que se usan.
- Explicar la decision detras de cada paso significativo.
- **Cursor para señalar**, movimiento deliberado.
- *"As though teaching a colleague."* Ese es el tono.

El glosario completo de frases: `docs/glosarios/glosario-narracion-mercor.md`.

## 5. La grabacion, paso a paso

### Antes de grabar

1. **Preparar archivos y entorno.**
2. **Lanzar las apps, terminar el sign-in y la carga, abrir los archivos requeridos**, y
   **minimizar las apps**. Nada de logins en camara.
3. **Ocultar informacion privada**: pestañas personales, emails, notificaciones.
4. **Dejar solo el documento del Goal visible**, detras de TaskRecorder.
5. **Ocultar el approval ID.**

### Arranque (menos de 20 segundos)

1. Empezar a grabar.
2. **Minimizar TaskRecorder.**
3. Decir: *"I will be beginning my task soon. Here is the workflow I have in mind."*
4. **Minimizar o cerrar el documento del Goal**, traer las apps, empezar.

### Durante

- **Una sola toma** ("record the complete task in one take").
- Narracion durante todo el recorrido.
- **Nunca mas de 45 s** de: tipeo continuo, inactividad del mouse o silencio de audio.
  Si una entrada de texto es larga, cortarla en secciones y despues revisar, señalar, explicar.
- **Menu bar, clock y dock visibles.** Sin full-screen. Sin ventanas apiladas.
- Ventanas: una clara activa, o lado a lado. Los dialogos temporales de la misma app pueden
  superponerse mientras se usan, y se cierran al terminar.

## 6. Apps: las cuatro categorias

| Categoria | Regla |
|---|---|
| **Banned** | No se puede usar para trabajo nuevo. No abrir, ni mostrar, ni usar |
| **Limited use** | **Regla del 20 %**: no mas del 20 % del tiempo, y condiciones mas estrictas (ej. solo en background) |
| **Alternatives preferred** | Permitidas, pero hay preferida |
| **Unrestricted** | Sin aprobacion ni entrada en catalogo |

- **Firefox es preferido** para navegar. Chrome y Safari estan permitidos.
- Si una app no aparece en Studio: elegir **Other** y escribir el nombre exacto. La idea igual
  necesita aprobacion.
- **Excel de escritorio rompe TaskRecorder**: usar Google Sheets, o Excel en el navegador.
- **Windows en VM (Parallels, VMware, CrossOver) esta prohibido.**
- **VPN, proxy e iCloud Private Relay prohibidos.** La VPN puede terminar el contrato sin aviso.
- **No crear Apple ID ni iCloud** para una tarea: pide telefono, expone datos.

## 7. Lo que invalida una toma

### PII: datos privados
Emails personales, telefonos, direcciones, IDs, biometricos, MAC addresses, nombre completo, info
de cuenta.

### PII: info del proyecto
**Mercor, Project Odin, Studio, el handbook, las guidelines**, cualquier material del proyecto. El
propio handbook esta marcado "PII EXPOSED": **no tenerlo abierto mientras se graba.**

**Donde se filtra sin darse cuenta:** nombre de usuario del SO en la barra de menu, avatar,
nombre del perfil del navegador, barra de titulo de Finder o VS Code.

### Escritorio
- **Modo oscuro**, **Dock a la izquierda o derecha** (nunca abajo), fondo no-default,
  **cursor default**.
- Ventanas grandes y legibles. Sin full-screen. Sin menu bar/dock ocultos.
- **Overlap del 25 % o mas por mas de 6 segundos**: invalida.

### Audio
Silencio maximo **45 s**. Pausa ideal menos de 30 s. Sin ruido de fondo que tape la voz.

### Contenido con licencia
Solo **CC0 o Public Domain** verificados para uso comercial y ML. **Royalty-free no alcanza.**
Sin marcas de agua (excepto Gemini en inputs), sin ©, sin ownership notice.

## 8. Al terminar: los cuatro archivos y AutoQC

| Archivo | Nota |
|---|---|
| `video.mp4` | La grabacion, una sola toma |
| **zip original de TaskRecorder** | **Intacto**, sin re-zipear |
| `deliverables.zip` | Los archivos producidos |
| `metadata.rtf` | En su **propio campo**, separado |

- **Correr los dos checks de AutoQC.**
- **Arreglar o disputar cada major flag** antes de enviar. Los minor son consejo y no bloquean;
  arreglarlos cuando sea practico.
- **Inspeccionar la seccion marcada** antes de decidir que corregir. Un problema de archivo puede
  necesitar una subida corregida.

## 9. Entorno de trabajo

- **`~/odin-work/`** fuera del workspace, en el perfil limpio. Nunca dentro del repo: es material
  del proyecto y no se mezcla con el codebase propio (CIIAA §2(c)).
- **Perfil de usuario limpio** en la Mac, con el idioma en **ingles**.
- **Navegador dedicado a Mercor**: Firefox (preferido por el manual), con Okta cuando haga falta.

## 10. Antes de grabar: checklist

- [ ] Pasa el **test del amigo**.
- [ ] Dominio declarado correctamente.
- [ ] Duracion estimada: 15-20 min.
- [ ] Apps en la categoria correcta (ninguna banned).
- [ ] Investigacion hecha y los puntos de decision definidos.
- [ ] `~/odin-work/` sin nada del workspace propio.
- [ ] Apps lanzadas, sign-in terminado, archivos abiertos, apps minimizadas.
- [ ] Approval ID oculto.
- [ ] Solo el documento del Goal visible, detras de TaskRecorder.
- [ ] Escritorio: modo oscuro, Dock a un costado, fondo propio, cursor default.
- [ ] Sin VPN, sin Private Relay, sin Excel de escritorio.
- [ ] UI en ingles.
- [ ] Ensayo de 3 minutos en voz alta **sin grabar**.
- [ ] Goal identico en los **tres** lugares.

## 11. Pendiente (no inventar)

1. **Los numeros de tier y bonus** en el handbook: leidos el 30/10. Confirmar contra el Odin
   Dashboard cuando se habilite (el owner no tiene "My Pay" todavia).
2. **Reviewer feedback**: que rechazan con mas frecuencia (la seccion 08 del handbook).
3. **Limites de tareas abiertas por fase**: Onboarding, Trial (12 h, +3 h por aprobacion),
   Production (Writer 60 h/sem, 5 abiertas).
4. **La regla exacta del 20 %** para apps de limited use.

## Archivos

- `docs/entrevistas/mercor-project-odin/Project Odin Writer Handbook.pdf` (+ `handbook.txt`)
- `docs/entrevistas/mercor-project-odin/orientacion-transcripcion.md`
- `docs/entrevistas/mercor-project-odin/evidencia/manual/` (9 slides + cheat sheet)
- `docs/glosarios/glosario-narracion-mercor.md` (frases y criterios de narracion)
