# ADR-104: La búsqueda laboral como proceso factorizado, no como odisea por puesto

**Fecha:** 2026-10-23
**Estado:** Aceptado
**Decisores:** Gonzo / Kanam
**Origen:** Gonzo, tras la tanda del 2026-10-22/23: "podemos hacer que este proceso de las postulaciones sea algo que podamos hacer nuevamente con muchas otras postulaciones? factorizarlo... hacer skill, script o lo que sea que haga falta para que yo te diga: busca puestos y aplica.. o algo asi"
**Relacionado:** ADR-101 (hechos de carrera con dueño único), ADR-083 (frontera de roles), ADR-077/089 (pipeline A/B)

---

## Contexto

El 2026-10-22/23 se postuló a tres vacantes (RYZ Labs, Mural, Mercado Pago) y las tres quedaron confirmadas por el servidor. El resultado visible fueron tres postulaciones. El costo real fue otro: **casi ocho horas de trabajo con dos personas, y una jornada entera dedicada a descubrir, a mano, cómo funciona cada formulario.**

Lo que se aprendió ese día, medido:

| Hallazgo | Costo de descubrirlo | ¿Se puede volver a aprender? |
|---|---|---|
| `fill()` de Playwright no actualiza el estado de React (`_valueTracker`): el servidor ve "9 fields missing" con los campos visiblemente llenos | 3 intentos de submit fallidos en Ashby | Sí, pero solo por hallazgo |
| Los desplegables de Ashby no toman el valor con click sintético: hay que clickear con mouse real sobre coordenadas | Varios intentos | Sí, pero caro |
| `Backspace` no limpia un input controlado: hay que `Meta+A` + borrar (en macOS, no `Control+A`) | Campos con valores concatenados | Sí, pero raro de adivinar |
| El autocomplete de "Location" de Ashby **no reconoce "Buenos Aires"**: solo "Argentina" y "Nunez" | Un submit fallido con 9 campos "faltantes" | No: es arbitrario |
| El panel de "Autofill from resume" de Ashby pisa el formulario con su parseo asíncrono | Un submit fallido | Sí, pero hay que saber el orden |
| En Eightfold, los campos se identifican por `id`, no por `name`; y los dos últimos campos **no** son áreas de texto sino Si/No (privacidad, conflicto de interés) | Casi un envío de la nota de presentación a una caja de desplegable equivocada | Sí, pero con riesgo de mandar algo equivocado |
| El teléfono de Eightfold no acepta `+` ni espacios, y con el código de país en +54 espera el número nacional | Un submit fallido | Sí |
| El hCaptcha de Lever **no lo resuelve ningún navegador automatizado**; en Safari el envío salió directo sin captcha | Toda una tarde | No: es un detector de contexto |

El último es el más caro, porque el primer intento fue pedirle a Gonzo que resolviera el captcha a mano en una ventana que **yo había marcado como automatizada**. El "fallo" de la persona era el fallo del instrumento.

El patrón que estos once hallazgos comparten: **son conocimiento de interfaces de terceros, costoso de descubrir y barato de reusar.** Volver a pagarlos en cada puesto es exactamente lo que ADR-101 establece la razón: "si un dato aparece en dos archivos, uno de los dos es un bug". El mismo razonamiento aplica a los workarounds: si cada postulación re-descubre que `fill()` no funciona, hay dos verdades sobre cómo se llena un formulario.

## Decisión

**Se construye un skill de flujo (`skills/job-application/`) más scripts reutilizables, con el conocimiento de los tres ATS capturado una sola vez.**

Estructura:

```
skills/job-application/
├── SKILL.md                  el flujo: descubrir -> tailored -> aplicar -> verificar -> trackear
├── scripts/
│   ├── find-jobs.mjs         descubrimiento multi-board
│   ├── apply.mjs             orquestador: llena, verifica, envia con el OK de Gonzo
│   ├── ats/{lever,ashby,eightfold}.mjs   adaptadores por ATS
│   └── lib/{react-form,real-browser,captcha}.mjs   los workarounds, uno por archivo
├── references/
│   ├── ats-playbook.md       las particularidades de cada ATS, con la evidencia
│   └── outreach.md           plantillas de mensaje y las preguntas de screening
└── commands/
    └── find-and-apply.mjs    el comando "busca puestos y aplica"
```

Las tres reglas que gobiernan el diseño:

### 1. El captcha define la arquitectura, no es un obstáculo más

**Regla dura:** ante un formulario con captcha, el relleno se hace en el navegador real del usuario, y el envío se hace ahí también. Nunca se intenta resolver el captcha con automatización, porque el captcha detecta el **contexto**, no los intentos: un browser con `navigator.webdriver === true` o con `--headless=new` en el User-Agent es rechazado aunque una persona clickee el checkbox.

Esto es lo que convierte el trabajo de "probar 8 contextos" en "usar el contexto correcto una vez".

### 2. Verificar antes de enviar, y contra el servidor

Cada adaptador **relee el DOM y compara contra el estado interno de React** antes de habilitar el envío, y después del envío **lee la respuesta del servidor**, no el exit code. La razón es medida: un formulario puede verse completo y el servidor rechazar 9 campos; y un envío puede "no fallar" y no haberse registrado.

### 3. Nada sale sin el sí explícito de Gonzo

El flujo **prepara y deja listo**: rellena el formulario, verifica, captura evidencia, y se detiene. El envío requiere el OK de Gonzo. Es la regla que ya existe en `AGENTS.md` ("Nada sale sin un sí explícito de Gonzo. Push, comentarios, respuestas inline...") aplicada al caso de las postulaciones. Una skill que postula sola es una skill que puede invalidar una postulación con un número de teléfono mal o un gap omitido.

El límite con el captcha es la excepción, y no contradice la regla: el captcha **no se resuelve** con automatización; se resuelve con un humano en un contexto no marcado. La skill deja el formulario listo y dice exactamente qué falta.

## Consecuencias

**A favor:**
- "Busca puestos y aplica" pasa de ser una odisea de horas a un comando con revisión.
- Los gaps de cada ATS quedan documentados una vez, con la evidencia del día que se descubrió.
- El conocimiento de formularios de terceros se vuelve activo: aparece el caso nuevo (un ATS distinto) y se le agrega un adaptador, sin tocar lo que funciona.
- El gate de hechos (`scripts/check-cv-facts.py`) deja de ser un paso opcional: el flujo no genera un CV que no lo pase.

**En contra (y son reales):**
- Un skill más que mantener. La regla de la capa es que el conocimiento de interfaz de terceros **envejece**: un ATS cambia su formulario y el adaptador queda viejo. Por eso el playbook lleva la fecha y la evidencia de cada workaround, para que se sepa qué volver a verificar.
- El discovery multi-board depende de APIs de terceros que pueden cambiar o caerse. Por eso el radar es una ayuda para encontrar, no la fuente de verdad: la verificación del puesto es manual y explícita.
- Automatizar el envío sin OK es exactamente el riesgo que la regla 3 evita. Por eso la skill **prepara** y no **envía**.

## Alternativas descartadas

- **Un solo script grande con un flag por ATS.** Descartado: los tres ATS divergen en el mapeo de campos y en el flujo de submit; un script con flags por ATS es peor que tres adaptadores con una interfaz común.
- **Solo documentar el know-how en un doc, sin código.** Descartado: los workarounds son de *interacción* (qué evento dispara React, qué coordenadas clickear, cuándo esperar el parseo asíncrono). Un doc los describe; solo el código los aplica.
- **La skill en `agents/kanam-studio/skills/`.** Descartado por ADR-083: el CORE orquesta el flujo; STUDIO redacta el contenido del CV. La skill del flujo es del CORE, y llama a `cv-tailor` (STUDIO) para la redacción.
- **Automatizar el captcha con un solver.** Descartado: además de ser unreliable, es un bypass de un control anti-bot deliberado. No se hace.

## Estado

Aceptado 2026-10-23. Implementación en curso.
