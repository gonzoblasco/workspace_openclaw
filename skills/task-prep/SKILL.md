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

> **Fuente de verdad: `Project Odin Writer Handbook`** (135 paginas), archivado en
> `docs/entrevistas/mercor-project-odin/`. El handbook es la biblia: si esta skill y el handbook
> difieren, **gana el handbook** y se corrige la skill. El texto extraido vive en
> `handbook.txt` al lado del PDF.
>
> **Que hace esta skill:** prepara una tarea para grabarla. **No la ejecuta y no ayuda durante la
> grabacion.** La linea es contractual y de proyecto: la IA puede ayudar a *pensar* antes, nunca a
> producir mientras se graba.

## 0b. Que es el puesto (no deducirlo del titulo)

**Odin Writer no es "escribir textos" y no es "programar".** El handbook lo define asi:

> *"You will record your computer screen while completing professional tasks across several
> domains, narrating what you are doing, where you are doing it, and why."*

**18 dominios**, y se elige uno segun la expertise real:

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
(10+ anos, React/TS, 11 PRs, accesibilidad). TEXT, DES y BUSI son alternativas validas si una idea
de otro dominio es mejor, pero no como primera.

**No hay webcam ni filmacion de la persona.** Solo pantalla.

## Cuando usarlo

- "preparame la tarea de Odin"
- "voy a grabar, arma el plan"
- "que tarea propongo"

## 0. La regla que ordena todo

**Antes sí, durante no.**

| Momento | Que se puede | Que no |
|---|---|---|
| Antes de grabar | **Gemini unicamente**, para input files y brainstorming. Investigacion, docs, notas | Generar las ideas de la tarea con IA (*"Task ideas must be entirely your own"*) |
| Durante la grabacion | Nada. Vos, la pantalla y el microfono | Cualquier IA en pantalla: ni prompt, ni conversar, ni generar, ni resumir |
| Despues | Debrief: que funciono, que quedo flojo | - |

**El riesgo real no es la sancion: es contaminar el dato.** El modelo aprende de lo que ve. Si te ve
usando un LLM, aprende eso.

## 1. Criterio de seleccion de la tarea

Una tarea sirve si cumple **los siete**:

1. **Objetivo claro** en una frase.
2. **Inicio y fin definidos** (sabés cuando terminó, sin dudar).
3. **Secuencia con sentido**: pasos que se encadenan, no acciones sueltas.
4. **Resultado verificable**: un test que pasa, un archivo que existe, un numero que cambio.
5. **2 o 3 apps como maximo**, todas aprobadas en la propuesta.
6. **Cero datos privados** ni del proyecto (ver §6).
7. **Idea propia**, no generada por IA.

**Para la primera tarea: simple y conocido.** Un bug acotado con test que falla y test que pasa.
No un refactor grande: en 25 minutos de narracion no se puede contar bien y el rubric castiga la
complejidad, no la premia.

## 2. Investigacion previa (la parte que evita el silencio)

Antes de grabar, con la investigacion hecha, respondé:

- **Que API / funcion / sintaxis** voy a usar, y **en que doc** esta (URL exacta).
- **Que comando** voy a correr y **que salida** espero.
- **Cuales son los 2 o 3 puntos de decision** de la tarea, y que opcion elijo en cada uno con el
  WHY: por que esa y no la otra.
- **Que NO voy a tocar**, para no salirme del scope durante la toma.

**La investigacion se hace ANTES y en otra maquina si hace falta.** Durante la grabacion no hay
consultas: hay ejecucion narrrada.

## 3. El guion de narracion

Usar el glosario: `docs/glosarios/glosario-narracion-mercor.md`. Lo esencial:

**Cada accion, en una frase con tres partes:**

> *"I am opening the filter... in the Status column header... to show overdue invoices."*

| | |
|---|---|
| **WHAT** | que hago |
| **WHERE** | donde en pantalla |
| **WHY** | para que (esta es la que demuestra razonamiento) |

- Al cambiar de paso: **"Step 2: I'll now..."**
- Cursor **sobre** el control que nombro.
- Atajos: **anunciarlos** antes o mientras ("I'm pressing Command + Shift + 4 to take a screenshot").

## 4. Los cuatro lugares del Goal (regla de oro)

**El mismo texto exacto, copiado y pegado. No reescrito.**

| # | Donde |
|---|---|
| 1 | Idea inicial (Slack / Studio) |
| 2 | `Metadata.rff` → campo Request |
| 3 | Documento de intro → Task Description |
| 4 | `TaskRecorder` → Task Description |

Si lo reescribis en cada lugar, aunque diga lo mismo, se lee como inconsistencia.

## 5. La estructura de la grabacion

| Fase | Regla |
|---|---|
| **Antes** | Accessibility Inspector corriendo con ventana cerrada y Dock dot visible; TaskRecorder con description y apps correctos; ventanas no usadas cerradas |
| **START** | **menos de 20 segundos**. Mostrar el Goal, minimizar TaskRecorder, decir exactamente *"I will be beginning my task soon. Here is the workflow I have in mind."*, ocultar el Goal. **No leerlo ni explicarlo** |
| **DURING** | WHAT / WHERE / WHY en cada accion. Cursor sobre el control. Atajos anunciados |
| **FINISH** | Mostrar el archivo guardado, explicar los chequeos, confirmar el resultado. **Epilogo: 3 min objetivo, maximo 4** (resultado, decisiones, desafios, mejoras). Anunciar que termino y parar |

## 6. Entorno: lo que invalida una toma

### PII: datos privados
Emails personales, telefonos, direcciones, IDs, biometricos, **MAC addresses**, **nombre
completo**, info de cuenta.

### PII: info del proyecto
**Mercor, Project Odin, la pagina de Studio, las Writer Guidelines**, o cualquier material del
proyecto. El propio handbook esta marcado "PII EXPOSED": **no tenerlo abierto mientras se graba**.

**Donde se filtra sin darse cuenta:** nombre de usuario de la Mac en la barra de menu, avatar de la
esquina, nombre del perfil del navegador, barra de titulo de Finder o VS Code.

### UI Diversity: el escritorio no puede parecer una Mac nueva
| NO | SI |
|---|---|
| Fondo default (Tahoe Day) | Fondo no-default |
| Modo claro | **Modo oscuro** |
| **Dock abajo** | **Dock a la izquierda o derecha** |
| Tema automatico, highlight azul | Tema propio (ej. Purple + highlight amarillo) |
| Cursor cambiado | **Cursor default, siempre** |

### Ventanas
| GOOD | BAD |
|---|---|
| Una ventana activa, limpia | Menu bar, clock o dock ocultos |
| Ventanas grandes y legibles | Full-screen mode |
| Minimizar lo no usado | Ventanas flotantes chicas |
| Side-by-side si hace falta | **Overlap del 25 % o mas por mas de 6 segundos** |

### Silencio y ruido
- Silencio maximo: **45 s**. Pausa ideal: **menos de 30 s**.
- Ruido de fondo que tape la voz: invalida.
- Rambling y filler: prohibidos.

### Contenido con licencia (input files)
- Solo **CC0 o Public Domain**, verificados para uso comercial y ML.
- **Royalty-free no alcanza.**
- Evitar: marcas de agua, ©, ownership notice, licencias poco claras, material pago.

## 7. Entorno de trabajo

- **`~/odin-work/`** - fuera del workspace, en el perfil limpio. Nunca dentro del repo: es material
  del proyecto y no se mezcla con el workspace personal.
- **Perfil de usuario limpio** en la Mac, con el idioma en **ingles**.
- **Chrome dedicado a Mercor con el Okta Browser Plugin** (el manual lo pide como extension de
  Chrome; no Firefox).
- Nada de repos propios ni herramientas propias en la grabacion: activa la licencia perpetua de
  §2(c) del CIIAA.

## 8. Antes de grabar: checklist

- [ ] La tarea cumple los 7 criterios de §1.
- [ ] La investigacion esta hecha y los 3 puntos de decision definidos.
- [ ] El Goal es **identico** en los cuatro lugares.
- [ ] El proyecto vive en `~/odin-work/`, sin nada del workspace.
- [ ] Escritorio: modo oscuro, Dock a un costado, fondo propio, cursor default.
- [ ] Ventanas cerradas, ninguna superpuesta mas de 6 s.
- [ ] Chrome con Okta, sin cuenta personal, sin el handbook abierto.
- [ ] UI en ingles.
- [ ] Ensayo de 3 minutos en voz alta **sin grabar**.
- [ ] TaskRecorder con description y apps correctos.

## 9. Pendiente (no inventar)

Lo que falta verificar antes de completar la skill:

1. **TaskRecorder**: captura ventana o pantalla completa? como maneja el audio?
2. **`Metadata.rff`**: formato exacto y campos obligatorios.
3. **Los numeros de tier y bonus** en el handbook (hoy solo esta lo del mail de bienvenida).
4. **Reviewer feedback**: que rechazan con mas frecuencia.
5. **Duracion objetivo de la tarea** (el ejemplo de ExpertWoka dice 25 min + 3 de epilogo, pero es
   de terceros, no del manual).
6. **Certn vs Zinc**: si algun proyecto acepta Certn, el check es de 5-7 dias habiles.

## Archivos

- `docs/glosarios/glosario-narracion-mercor.md` - frases y criterios de narracion (fuente de §3).
- `docs/entrevistas/mercor-project-odin/` - el proceso: contratos, pack, brief, CV.
- `docs/entrevistas/mercor-project-odin/evidencia/manual/` - el manual oficial del proyecto
  (9 slides + `odin-writer-cheat-sheet.pdf`). **Es la fuente primaria de esta skill.**
