---
name: "job-application"
metadata:
  category: "Career"
  tags:
    - job
    - postulacion
    - application
    - cv
    - ats
    - busqueda-laboral
description: "Flujo completo de busqueda y postulacion: descubre vacantes, arma el CV contra el JD, llena el formulario del ATS y verifica el envio. Deja el submit para Gonzo."
user-invocable: true
---

# Workflow: Job Application

> **El comando que Gonzo quiere:** "busca puestos y aplica".
> Lo que hace: descubre vacantes que encajen, prepara el CV y el mensaje, deja el formulario del ATS listo y verificado, y **se detiene antes de enviar**.
> Lo que **no** hace: enviar sin su OK. Ese límite no es una limitación, es el diseño (ADR-104).

## Cuándo usarlo

- "busca puestos", "buscá trabajo", "mirá qué hay"
- "postulá a X", "aplicá a esta vacante", "armá el CV para este puesto"
- "seguí con el proceso de Y"
- "postulaciones" como tarea recurrente

## La regla que gobierna todo

**Nada sale sin el sí explícito de Gonzo.**

El flujo **prepara**: arma el CV, llena el formulario, lo verifica, captura evidencia, y se detiene.
El envío es un paso aparte que requiere su OK explícito, en cada caso.

Esto no es conservadorismo: es que una postulación es un documento contractual firmado con su
nombre, su teléfono, su expectativa salarial y su nivel de inglés. Un error ahí no se
deshace con un mensaje.

## Las tres fases

### Fase 1 - Descubrir

```bash
node skills/job-application/scripts/find-jobs.mjs --query "frontend" --country AR --remote --json
```

**Qué se filtra y por qué** (medido sobre 10+ boards el 2026-10-23):

- El mercado de *accesibilidad* activo es **casi entero US-only**. Los avisos que filtran "LATAM"
  son casi todos el mismo bench de recruiters (Infojini, E-IT, FullStack), que es el req que ya
  cerró con Disney/HTC.
- Lo que hay, y funciona, son vacantes de **front-end con accesibilidad en empresas de producto
  reales**: RYZ Labs, Mural, Mercado Pago, Bluelight, Makai Labs, Nortal.
- **Regla operativa:** apuntar a empresas de producto con su propio equipo, no a nearshore-agencies
  que reasignan tu tiempo a clientes US. En las agencies el idioma es filtro de elegibilidad; en
  producto es ruido de fondo.

**El filtro de idioma va en la fase 1, no en la fase 3.** Los dos cierres recientes (Staffy 20/10,
Sol 21/10) llegaron tarde: el CV ya estaba armado, el screening hecho, y el filtro apareció al
final. Por eso la **primera** pregunta de screening es siempre el nivel de inglés conversacional, y
va en el primer mensaje.

### Fase 2 - Armar (CV + mensaje)

El CV lo redacta **STUDIO** con `cv-tailor` (ADR-083: el CORE orquesta, el contenido lo hace el rol
que corresponde). El CORE pasa el JD, el perfil y las restricciones.

Restricciones que no se negocian, y que verifica `scripts/check-cv-facts.py`:

| Regla | Por qué |
|---|---|
| Un solo headline de años: 10+ | ADR-101, dueño único de los hechos |
| **Ningún número de años de accesibilidad** | La aritmética da 4,42 de función central: cualquier redondo obliga a elegir entre quedar corto o inflar |
| Inglés **B2**, nunca "fluent"/"Advanced"/"C1" | La regla dura del corpus. Declarar más es comprar una conversación que se cae sola |
| Sin título universitario, sin "IAAP certified" | No existen. Deque es un **programa** (2021), no una credencial |
| Roles y fechas canónicas | Freelancer 05/2025-, EY 09/2021-05/2025, Super7UI 08/2020-05/2021, Minutentag 02/2016-11/2019 |
| El perfil es un **filtro**, nunca una verdad nueva | Un perfil cambia el relato, no los hechos |

El **perfil activo** por defecto es "AI-native frontend" (corpus §10): React/TS + design systems +
accesibilidad + IA en el flujo. Es el que dio resultado en las tres postulaciones de octubre.
El perfil a11y puro existe y es válido para los avisos de accesibilidad de empresa.

El **mensaje de primer contacto** va en `references/outreach.md`: 130-200 palabras, hook específico
del JD, un hecho real, el diferenciador, y las preguntas de screening con la del idioma al final.

### Fase 3 - Aplicar

```bash
# 1) dejar el formulario listo y verificado (NO envia)
node skills/job-application/scripts/apply.mjs --url "<posting>" --ats auto \
  --cv docs/entrevistas/<proceso>/<cv>.pdf --answers <respuestas.json> --out <dir>

# 2) con el OK de Gonzo, enviar
node skills/job-application/scripts/apply.mjs --url "<posting>" --cv <cv.pdf> \
  --answers <respuestas.json> --submit
```

**El ATS se detecta solo** por la URL (Lever / Ashby / Eightfold). Los workarounds de cada uno están
en `references/ats-playbook.md` y en `scripts/ats/*.mjs`.

## Lo que el flujo NO puede hacer

**Un captcha no lo resuelve la automatización.** No es un obstáculo: es un **detector de contexto**.
Un browser con `navigator.webdriver === true` o con `--headless=new` en el User-Agent es rechazado
aunque una persona clickee el checkbox (medido el 2026-10-23: token 0 en Playwright, token 0 en el
perfil headless, **envío directo en Safari**).

Por eso, cuando el ATS tiene captcha:
1. `real-browser.mjs` se conecta al **Chrome real del usuario** por CDP (no lanza uno nuevo).
2. El flujo llena y verifica todo.
3. **Se detiene** y le dice a Gonzo: "resolvé el captcha y apretá Submit".

Y antes de pedirle eso, verificar que el contexto que se le pasa **no está marcado**. El "fallo" de
la persona suele ser el fallo del instrumento.

## Verificación: contra el servidor, no contra la pantalla

En formularios de React, `fill()` deja el valor en el DOM pero **no actualiza el estado interno**
(`_valueTracker`): el formulario se ve completo y el servidor responde "9 fields missing". Por eso
cada adaptador **relee el DOM y compara contra el estado de React** antes de habilitar el envío, y
después del envío **lee la respuesta del servidor** (no el exit code, ni la ausencia de error).

Los veredictos reales de referencia:
- Ashby: `"Your application was successfully submitted. We'll contact you if there are next steps."`
- Eightfold: `201 {"success": true}` + `"¡Gracias por su solicitud, Gonzalo!"`
- Lever: página de confirmación tras el submit.

## Después de aplicar

1. **Tracker** (`docs/entrevistas/_general/job-search-tracker.md`): una fila por proceso, con el
   veredicto textual, la fecha, el canal y el riesgo #1. Es la fuente única de los procesos.
2. **Carpeta por proceso** (`docs/entrevistas/<empresa>-<puesto>/`): CV en markdown (la verdad),
   HTML, DOCX, PDF, la evidencia (capturas) y los scripts usados.
3. **El `.md` del CV es la verdad**; el DOCX y el PDF son derivados y se regeneran con
   `scripts/build-cv-docs.sh`.

## Errores que ya se pagaron (no repetirlos)

| Error | Regla |
|---|---|
| `fill()` no llena para React | `type()`, y verificar con `_valueTracker` |
| `Backspace` no limpia | `Meta+A` + `Delete` (macOS, no `Control+A`) |
| El desplegable no toma el valor | click **real de mouse** sobre las coordenadas |
| El radio no se marca | click sobre la **etiqueta** |
| El autofill de Ashby pisa el formulario | CV primero → esperar → escribir → adjuntar |
| El captcha no resuelve | cambiar de navegador, no insistir |
| Faltan 9 campos y el form se ve lleno | el servidor ve el estado, no la pantalla |

El detalle de cada uno, con su evidencia, está en `references/ats-playbook.md`.

## Archivos

```
skills/job-application/
├── SKILL.md
├── references/
│   ├── ats-playbook.md    particularidades de cada ATS (con fecha y evidencia)
│   └── outreach.md        plantillas de mensaje y preguntas de screening
└── scripts/
    ├── find-jobs.mjs      discovery multi-board
    ├── apply.mjs          orquestador
    ├── lib/               workarounds de React, browser real, registro de adaptadores
    └── ats/               un adaptador por ATS
```

## Relacionado

- `agents/kanam-studio/skills/cv-tailor/` - redacción del CV (STUDIO)
- `scripts/check-cv-facts.py` - el gate de los hechos de carrera
- `docs/entrevistas/_general/job-search-tracker.md` - fuente única de los procesos
- `docs/adr/ADR-104-busqueda-laboral-proceso-factorizado.md` - por qué existe esta skill
