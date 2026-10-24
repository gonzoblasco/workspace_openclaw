# ATS Playbook - cómo se llena un formulario de postulación de verdad

> Fuente: la tanda del 2026-10-22/23 (RYZ Labs / Lever, Mural / Ashby, Mercado Pago / Eightfold).
> Cada punto de acá está verificado contra el repo o contra una respuesta del servidor, con la evidencia.
> **Fecha deRelevancia: 2026-10-23.** Los formularios de terceros cambian: si un adaptador falla, se
> re-verifica contra esta tabla antes de inventar un fix.

---

## 0. La regla que gobierna todas las demás

**React no ve lo que `fill()` escribe.**

`page.fill()` / `locator.fill()` setea el valor del DOM, pero **no dispara el `onChange` que React
escucha**. El formulario se ve completo en la pantalla, y el servidor responde "9 fields missing".
Esto se mide en los tres ATS, y es la causa raíz de la mayoría de los fallos de la primera tanda.

La verificación: el input de React tiene un tracker interno, `_valueTracker`, con el último valor que
React conoce.

```js
const reactValue = (el) => el._valueTracker?.getValue?.() ?? '(sin tracker)';
```

Si `reactValue(el) !== el.value`, **el campo no está lleno** para efectos del envío.

### Cómo escribir de verdad

| Operación | Cómo | Por qué |
|---|---|---|
| Escribir texto | `el.type(valor, { delay: 12 })` | `type()` sí despacha los eventos de teclado que React registra |
| Limpiar el campo | `Meta+A` (macOS) + `Delete`, o `el.select()` + `Delete` | **`Backspace` no limpia**: borra un carácter y deja el resto. El valor queda concatenado |
| Elegir un desplegable | **click de mouse real sobre las coordenadas** de la opción | `element.click()` desde JS no lo registra; `locator.click({force:true})` tampoco, en Ashby |
| Marcar un radio | click sobre la **ETIQUETA**, no sobre el input | el input está oculto (`opacity: 0`) y su click sintético no se registra |
| Subir un archivo | `setInputFiles()` + **esperar al parseo** | el parseo asíncrono pisa el formulario después |

En macOS el select-all es `Meta+A`, **no** `Control+A`.

---

## 1. Lever (RYZ Labs, y otros que usan Lever)

**Particularidad principal:** el auto-lector del CV completa campos solo y **pisa tu nombre con el de la
empresa del CV** (puso "Freelance" en *Full name*). Hay que sobreescribirlo *después* de que el
parser asiente.

| Campo | Cómo se localiza |
|---|---|
| CV | `input[type="file"]` (el único) |
| Nombre, email, teléfono, empresa | `input[name="name" \| "email" \| "phone" \| "org"]` |
| Ubicación | `input[name="location"]` + `input[name="selectedLocation"]` (autocomplete) |
| Salario | `input[name*="[field0]"]` (hay otro hidden con la misma etiqueta) |
| Nivel de inglés | `input[type="radio"][value="Upper Intermediate"]` (el `value` **es** el texto de la opción) |
| Info adicional | `textarea[name*="[field2]"]` |
| Submit | `button.btn-submit` (clase dinámica) |

**La ubicación es el campo tramposo.** El autocomplete de Lever concatena la opción a lo que ya
estaba tipeado ("Buenos Aires" + "Nuñez, Comuna 13, Buenos Aires, ARG" = dos valores pegados) y con
`fill()` el input visible queda **vacío** aunque el hidden quede bien. El único método que deja el
campo visible con texto es el humano: **teclear → `ArrowDown` → `Enter`**.

### El captcha (el muro de Lever)

El hCaptcha de Lever **no lo resuelve ningún navegador automatizado**. Medido el 2026-10-23:

| Contexto | `navigator.webdriver` | "Headless" en el UA | Token |
|---|---|---|---|
| Chrome lanzado por Playwright | **true** | sí | 0 |
| Perfil `imported` de OpenClaw (`--headless=new`) | false | **sí** | 0 |
| Chrome relanzado visible, mismo perfil | false | no | 0 |
| **Safari** | n/a | n/a | **no hizo falta captcha: el envío salió directo** |

El captcha detecta el **contexto**, no los intentos. Antes de pedirle a una persona que lo resuelva
a mano, hay que verificar que el contexto que se le pasa no está marcado. En Safari no hubo
captcha: **los formularios con captcha se resuelven en el navegador real del usuario**, y el envío
también.

**El botón de submit de Lever tiene dos `button[type="submit"]`**: el visible (`btn-submit`) y uno
**oculto** de hCaptcha (`id=hcaptchaSubmitBtn`). Un selector genérico agarra el oculto y falla con
timeout de 30s.

---

## 2. Ashby (Mural, y otros que usan Ashby)

**Particularidad principal:** el panel **"Autofill from resume"** dispara un parseo asíncrono que
**sobrescribe el formulario** con lo que extrajo del CV. Si escribís los textos antes, los pierdes.

**El orden correcto:**
1. Subir el CV al panel de autofill (el input cuyo ancestro dice "Autofill from resume").
2. **Esperar** a que termine (12-15 s).
3. Escribir los textos con `type()`.
4. Marcar radios y checkbox.
5. Adjuntar el CV al campo "Resume" y la cover letter al campo "Cover Letter" (el autofill los resetea).
6. Verificar.
7. Enviar, y leer la **respuesta GraphQL** (`ApiSubmitMultipleFormsAction`), que es el veredicto.

| Campo | Cómo se localiza |
|---|---|
| Nombre, email | `input[name="_systemfield_name" \| "_systemfield_email"]` |
| Teléfono | `input[name="2c6cb798-..."]` (UUID) |
| Ubicación | `input[role="combobox"]` con placeholder "Start typing..." |
| LinkedIn | `input[name="d7ce58e9-..."]` (UUID) |
| Salario | `input[name="6bb011c6-..."]` (UUID) |
| Archivos | por el **texto del ancestro** (`Resume` / `Cover Letter`): los `name` de los inputs de archivo desaparecen al re-renderizar, y los `id` se reordenan entre navegaciones |
| Radios | `input[type="radio"][name*="<uuid>"]` + índice dentro del grupo. **Todos tienen `value="on"`**: no se distinguen por valor, sino por posición |
| Submit | `getByRole("button", { name: "Submit Application" })` (hay 4 `button[type=submit]`, tres son "Upload file") |

### El autocomplete de "Location" no reconoce "Buenos Aires"

Medido: `"Buenos Aires"` → **"No results"**. `"Argentina"` → ok. `"Nunez"` → ok (y "Núñez" con tilde → no).
El valor resuelto queda como `{"name":"Nuñez, Comuna 13, Buenos Aires, ARG", ...}`.

Ese detalle costó un submit fallido con 9 campos "faltantes" en un formulario que se veía perfecto.

### La validación es client-side

El submit **no va al servidor** cuando faltan campos: lo muestra un `div` con la lista
"Missing entry for required field: X". Por eso no hay POST que capturar: el veredicto se lee del DOM
después del click.

**El footer sticky** (Cancelar / Borrar formulario / Enviar solicitud) tapa los últimos campos: el
click normal da timeout. Hay que hacer `scrollIntoView` y usar click forzado.

### El reCAPTCHA de Ashby se resuelve solo

Token de 2.382 chars sin intervención (modo invisible), disparado por el parseo del CV.

---

## 3. Eightfold (Mercado Pago, y otros que usan Eightfold)

**Particularidad principal:** los campos se identifican por **`id`, no por `name`** (`name=null` en
todos). Y **no hay área de texto libre**: la presentación viaja en el CV.

| Campo | Cómo se localiza |
|---|---|
| Email, nombre, apellido | `#Informaci_n_de_contacto_email`, `..._firstname`, `..._lastname` |
| Teléfono | `#Informaci_n_de_contacto_phone` |
| Ciudad | `#Informaci_n_de_contacto_city` |
| LinkedIn | `#Preguntas_sobre_la_solicitud_LinkedIn` |
| Código de país | `#input-7` (combobox, opciones con bandera: "🇦🇷 (+54) Argentina") |
| País | `#input-10` (combobox) |
| Privacidad | `#input-13` (combobox: "Si" / "No") |
| Conflicto de interés | `#input-16` (combobox: "Si" / "No") |
| **Estado** | aparece **solo después** de elegir el país, con id dinámico |

**Los dos últimos campos NO son áreas de texto.** La primera versión del script escribía la nota de
presentación ahí: la mandaba a una caja de desplegable. El riesgo no es que falle, es que **se envíe
algo equivocado**.

**El teléfono no acepta `+` ni espacios** ("Utiliza solo dígitos, guiones o paréntesis"), y con el
código de país en +54 espera el **número nacional** ("1149374656", no "+54 11 4937-4656").

**El modal de "Acuerdo de privacidad de datos"** bloquea el formulario al inicio: hay que aceptar
"Estoy de acuerdo" antes de tocar nada.

**El veredicto del envío es la respuesta del servidor:** `POST /api/application/v2/submit` responde
`201 {"success": true, ...}` y la página queda en `/careers/apply/success`.

---

## 4. Lo que hay que hacer SIEMPRE, en cualquier ATS

1. **Verificar contra el estado de React**, no contra el DOM. Campo por campo, antes de habilitar el envío.
2. **Leer la respuesta del servidor** después del envío, no el exit code ni la ausencia de error.
3. **Capturar evidencia** (screenshot) del formulario lleno y del resultado.
4. **Dejar el envío para la persona**, salvo que Gonzo lo pida explícitamente.
5. **Registrar en el tracker** con el veredicto textual, no con un "ok".

---

## 5. El discovery (encontrar las vacantes)

Endpoints que funcionaron el 2026-10-23, y qué rindieron:

| Fuente | Endpoint | Rendimiento |
|---|---|---|
| **Mercado Pago** | `careers-meli.mercadolibre.com/api/positions?country=AR` | **866 vacantes**, paginables y filtrables. El listado del portal solo muestra 12 |
| **Mural** | `api.ashbyhq.com/posting-api/job-board/<empresa>` | 14 vacantes, JSON limpio, con `applyUrl` |
| **RYZ Labs** | `api.lever.co/v0/postings/<slug>` | 47 vacantes, JSON limpio, con `applyUrl` |
| **LinkedIn** | `linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search` | Funciona **sin login** y trae `datePosted` |
| a11yjobs | HTML | 208 avisos, casi todos US-only |
| vacantesdigitales | `vacantesdigitales.com/api/detail/<id>` | API propia, con `apply_url` y `url` |
| Remotive / Himalayas / RemoteOK / Jobicy | JSON público | Filtrar por LATAM + Remote |

**El filtro que sirve** (medido sobre 10+ boards): el mercado de *accesibilidad* activo es casi
entero US-only. Los avisos que filtran "LATAM" son casi todos el mismo bench de recruiters
(Infojini, E-IT, FullStack: el mismo req de Disney/HTC). Lo que hay es **vacantes de front-end con
accesibilidad en empresas de producto reales**, y ahí el idioma es ruido de fondo en vez de filtro de
elegibilidad.

**Corolario operativo:** apuntar a empresas de producto con su propio equipo, no a nearshore-agencies
que reasignan tu tiempo a clientes US.
