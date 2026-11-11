# Clase: FULL CPACC Study Guide — Derek Mei

**Este es el material de estudio de verdad.** El video anterior (Practice Test Geeks) quedó como
roadmap; este **enseña el contenido** de los tres dominios, en 1:35:11, con captions manuales y
15 capítulos oficiales. Transcript en `transcripcion.md`.

> **Marco de uso (Gonzo, 2026-11-11):** se estudia para aprender, no para rendir. No hay fecha ni
> fee. El plan vive en `docs/cpacc/study-plan.md`; la clase es el contenido que ese plan recorre.

## Ficha del material

- Fuente: https://www.youtube.com/watch?v=a01vcZMTJqU
- Canal: Derek Mei
- Publicado: 2021-11-30 — **tiene 5 años**. Es anterior a WCAG 2.2 y al BoK v4.0 (oct-2023).
- Duración: 1:35:11 (5711 s), 15 capítulos, 2.188 cues, **captions manuales del autor**
- Autor: diseñador; trabajaba en una empresa de **captions, transcripts y audio description**.
  Rindió en abril, **sacó 691/800** (passing 600) y hoy tiene el WAS en el radar.
- **Advertencia de vigencia:** el autor es explícito en que su visión de las leyes es
  *«very Americentric»* (79:18). Y el material es de 2021: los pesos 40/40/20 y los conceptos
  centrales no cambiaron (verificado contra el BoK v4.0), pero **las leyes y los números de
  demanda pueden haber cambiado**. Se estudia el concepto; el dato legal se re-verifica.

## Resultado esperado

Al terminar, podés:

1. Explicar los **siete modelos de discapacidad** y para qué sirve cada lente.
2. Nombrar las **categorías de discapacidad** con sus barreras y AT típicas.
3. Aplicar **etiqueta de discapacidad**: person-first vs identity-first, y cuándo cada una.
4. Argumentar los **nueve beneficios** de la accesibilidad con un caso concreto cada uno.
5. Distinguir **acommodation individual vs diseño universal**, y los siete principios.
6. Explicar **UDL** en sus tres principios y sus subcategorías.
7. Aplicar **POUR** a una interfaz real.
8. Leer el marco legal internacional (UDHR, CRPD, Tratado de Marrakech) y ubicar ADA/508/EAA.
9. Describir los **modelos de madurez organizacional** y qué madura en cada etapa.

## Mapa temporal (capítulos oficiales)

| Tiempo | Capítulo | Qué enseña |
|---|---|---|
| 0:00 | Intro | Contexto: 691/800, el recorrido del examen |
| 1:08 | Why Take the CPACC? | Campo, credibilidad, aprender a fondo |
| 1:53 | CPACC General Information | Nivel, no técnico, la escalera IAAP |
| 4:29 | Important Resources | BoK, Content Outline, Deque, Funka, 100 Days |
| 8:33 | What's in the CPACC Exam? | 40/40/20, formato, qué pesa |
| 11:10 | **Part 1: Models of Disabilities** | Los 7 modelos |
| 18:44 | **Categories of Disabilities** | 8 categorías con barreras y AT |
| 36:05 | Disability Etiquette | Lenguaje y trato |
| 39:07 | Part 2: Accessibility & UD | Entrada al 40% conceptual |
| 42:26 | Benefits of Accessibility | Los 9 beneficios |
| 52:26 | **The Seven Principles of UD** | Los 7 principios con ejemplos |
| 58:07 | **Universal Design for Learning** | Los 3 principios de UDL |
| 68:42 | **Principles of Web Accessibility — POUR** | Perceivable, Operable, Understandable, Robust |
| 78:46 | Part 3: Standards, Laws & Management | El 20% legal |
| 87:42 | Integrating Accessibility into Your Org | Modelos de madurez |
| 93:42 | Conclusion | Cierre |

---

## Parte 1 — Discapacidades, retos y tecnologías de asistencia (40%)

### Módulo 1 — Los siete modelos de discapacidad (11:10 – 18:44)

**Objetivo:** ver la misma realidad por siete lentes distintas y detectar el sesgo de quien habla.

**Regla de entrada:** los modelos **no son mutuamente excluyentes** — «it's important to note that they're not mutually exclusive» (11:10). Y sirven para
detectar el sesgo ajeno: quien te explica algo sobre discapacidad puede estar mirando por una sola.

| Modelo | Qué sostiene | Cita |
|---|---|---|
| **Médico** | La discapacidad es un problema biológico de la persona: medicar, curar, aliviar | «looking at disability strictly through the lens of the medical field» (11:40) |
| **Social** | Lo discapacitante es cómo la sociedad ve y trata a la persona: estigma, actitudes | «how others will view you» (12:42) |
| **Biopsychosocial** | Intersección de lo biológico, lo psicológico y lo social; el más completo pero no perfecto | «intersection between the medical model, the social model» (13:12) |
| **Económico** | Costo puro: cuánto cuesta soportar, cómo consiguen trabajo | «looking at it from a purely monetary perspective» (14:15) |
| **Soluciones funcionales** | Resolver el problema con producto/tech; enfoque emprendedor | «of an entrepreneurial perspective» (15:47) |
| **Identidad social / afiliación cultural** | Pertenencia a una comunidad (ej. la comunidad Sorda) | «in order to become culturally affiliated or socially» (16:20) |
| **Caridad** | Dar por lástima, desde una posición de superioridad | «people who are not self-sufficient» (17:24) |

**Las dos ideas fuerza del módulo:**
- El **social** no es «la persona no puede», es «el mundo no deja». Es la que más pesa en el examen
  porque cambia la pregunta: no «qué le pasa a esta persona» sino «qué le pasa a esta interfaz».
- Sobre caridad: «if they're asking for help, that's when you» (17:57). El consentimiento ordena el trato.

**Ejercicio:** tomá un bug de accesibilidad que hayas arreglado y escribilo desde cada modelo.
El mismo `<div>` clickeable sin teclado, en siete versiones. Entregable: siete líneas.

### Módulo 2 — Categorías de discapacidad, barreras y AT (18:44 – 36:05)

**Objetivo:** mapear cada categoría a su barrera típica y a la tecnología que la resuelve.

**Las 8 categorías que cubre el video:**

1. **Visual.** Ceguera, baja visión, daltonismo. Causas varias (glaucoma, degeneración macular,
   diabetes, congénita) y espectro completo. AT: lentes para daltonismo, lectores de pantalla.
   Detalle que el examen pregunta: las variantes de daltonismo son **protanopía** y **tritanopía**,
   y no es lo mismo que baja visión.
2. **Auditiva.** Sordera, hipoacusia, y **CAPD (Central Auditory Processing Disorder)** — que se
   confunde con ADHD o problemas de aprendizaje pero es otra cosa: no hay pérdida medible, el
   problema es procesar el habla (22:27). AT: subtítulos, transcripciones, alternativas a lo
   time-based.
3. **Sordoceguera.** Combinación de ambas. AT: **Braille**, displays Braille refrescables que
   reciben la salida del lector de pantalla (24:34).
4. **Del habla.** Tartamudeo, apraxia, disartria, mutismo. AT: comunicación aumentativa y
   alternativa (AAC), síntesis de voz, sistemas por deducción de movimiento.
5. **Movilidad, flexibilidad y estructura corporal.** ~3-4% de la población de EE.UU. (27:44).
   AT: punteros de cabeza, teclados de una mano, switches.
6. **Cognitiva.** Comprensión, atención, memoria, procesamiento; TDAH. El video es claro:
   «there's no one size fits all» — hay que **testear con personas con discapacidad cognitiva**
   (30:56).
7. **Convulsiones / epilepsia fotosensible.** Regla concreta: **no más de tres destellos por
   segundo** (32:33). El caso histórico que cita: Pikachu y el episodio que causó convulsiones.
8. **Psicológica / psiquiátrica.** Depresión, ansiedad, TCA, esquizofrenia, bipolar. La AT varía
   caso por caso y el patrón es **impredecible en el tiempo** (33:39).
9. **Múltiple / compleja.** Combinación de las anteriores; se acomoda **caso por caso**, siempre.

**El marco que introduce acá y vale para todo el resto:** el modelo de Microsoft de
**permanente / temporal / situacional** (29:21). Una discapacidad situacional —llevar un bebé en
un brazo— se beneficia de las mismas soluciones que una permanente. Ese es el argumento del
diseño universal, y es el que convence a un PM.

**Ejercicio:** por cada una de las 8 categorías, una tabla de tres columnas: barrera en la web,
barrera en el mundo físico, AT. Entregable: 8 filas × 3.

### Módulo 3 — Etiqueta de discapacidad (36:05 – 39:07)

**Objetivo:** hablar de personas sin ofender ni presumir.

- **Regla base:** tratar a la persona como a cualquier otra (36:06).
- **Person-first por defecto:** «person with a disability», no «disabled person» (37:07).
- **Pero la preferencia individual manda:** la comunidad Sorda elige identity-first — «you're going to refer to them as a person who is deaf» (37:07), y la comunidad Sorda prefiere lo contrario. El video es explícito en que
  esto **pisa** la regla general. Preguntar antes de asumir.
- **Lenguaje neutro:** evitar eufemismos y, peor, términos ofensivos. Los dos que nombra: «retarded»
  y «special needs» (38:44). «That person has a disability» no se centra en la discapacidad.

**Ejercicio:** auditá el copy de un proyecto propio y listá cada caso de disability-first, eufemismo
o término ofensivo. Entregable: diff propuesto.

---

## Parte 2 — Accesibilidad y diseño universal (40%)

### Módulo 4 — Beneficios de la accesibilidad (42:26 – 52:26)

**Objetivo:** tener nueve argumentos con sustento, no una lista de buenas intenciones.

1. **Mejora la vida de las personas**: acceso a educación, empleo, servicios, sin depender de otros.
2. **Mejora la percepción pública de la organización** y la diferencia de competidores que «just
   talk the talk» (44:00).
3. **Aumenta la compatibilidad** entre sistemas, entorno y personas; accesibilidad y usabilidad
   están pegadas.
4. **Mejora el SEO**: lo accesible se rastrea mejor y los buscadores lo rankean más alto (45:03).
5. **Alcanza a más audiencia**: diseño universal = base de clientes más grande.
6. **Ayuda a conseguir financiamiento**: contratos públicos que exigen cumplimiento.
7. **Reduce el riesgo de juicio**: cita **más de 10.000 demandas ADA Title III en 2020**, según
   Seyfarth Shaw (47:06). **Dato de 2021 con fecha explícita**: verificar antes de usarlo en 2026.
8. **Alivia la carga de cuidadores** (familia, amigos): la independencia de uno descarga a varios.
9. **Conecta con personas**: entender discapacidades ocultas cambia la forma de vincularse.

**Ejercicio:** elegí los tres que más le importan a tu interlocutor (PM, legal, marketing) y
escribí el pitch de una frase para cada uno. Entregable: tres frases.

### Módulo 5 — Accommodation vs diseño universal + los 7 principios (52:26 – 58:07)

**Objetivo:** distinguir la solución puntual de la solución estructural, y aplicar los siete.

- **Acomodación individual:** resolver caso por caso, para una persona concreta (49:39).
- **Diseño universal:** diseñar para que sirva a todos sin adaptación posterior (50:10).
- **El ejemplo canónico del video:** los **curb cuts** (rampas en las esquinas). Nacieron para
  sillas de ruedas y los usan carritos, bicicletas y valijas con ruedas (50:42).

**Los siete principios, con el ejemplo que da el video:**

| # | Principio | Ejemplo |
|---|---|---|
| 1 | **Uso equitativo** | El curb cut: sirve igual a todos |
| 2 | **Flexibilidad en el uso** | Subtítulos configurables: tamaño, color, fuente (53:30) |
| 3 | **Uso simple e intuitivo** | Sirve igual a un chico y a un adulto mayor, sin manual |
| 4 | **Información perceptible** | Si no se oye, subtítulo; si no se ve, descripción; redundancia de canales (55:06) |
| 5 | **Tolerancia al error** | Poder deshacer; que un error no borre todo (55:37) |
| 6 | **Bajo esfuerzo físico** | El pelapapas rediseñado para quien no tiene fuerza en las manos (56:40) |
| 7 | **Tamaño y espacio para aproximarse y usar** | Espacio suficiente para llegar y maniobrar (57:12) |

**Ejercicio:** pasá una pantalla tuya por los siete y anotá, por principio, un defecto real.
Entregable: tabla de 7 filas con defecto y fix.

### Módulo 6 — Universal Design for Learning (58:07 – 68:42)

**Objetivo:** entender UDL — la parte que el autor confiesa que le resultó más ajena.

**Tres principios (58:38):**

1. **Múltiples medios de representación** — *el qué* del aprendizaje.
   - Opciones para la **percepción** (visual, auditivo, táctil).
   - Opciones para **lenguaje, expresiones matemáticas y símbolos** (descomponer antes de avanzar).
   - Opciones para la **comprensión** (conectar con modelos mentales previos, retener).
2. **Múltiples medios de acción y expresión** — *el cómo*.
   - Opciones para la **acción física** (escribir, hablar, presentar, proyecto).
   - Opciones para la **expresión y comunicación** (elegir el canal).
   - Opciones para las **funciones ejecutivas** (metas, planificación, seguimiento del progreso).
3. **Múltiples medios de implicación** — *el porqué*.
   - **Reclutar interés**; sin interés no hay aprendizaje.
   - **Sostener el esfuerzo y la persistencia**; acá entra el **flow** de Csikszentmihalyi: si es
     muy fácil, aburre; si es muy difícil, angustia (65:53).
   - **Autorregulación**: metas realistas, reflexión periódica sobre el propio proceso.

**Idea fuerza:** UDL no es «adaptar el curso para quien no puede»; es diseñar el curso con varios
caminos desde el principio. Aplica igual a documentación técnica y a onboarding.

**Ejercicio:** rediseñá un README o una guía interna con los tres principios. Entregable: la guía
reescrita con al menos un camino alternativo por principio.

### Módulo 7 — POUR: los cuatro principios de accesibilidad web (68:42 – 78:46)

**Objetivo:** poder auditar una interfaz contra POUR sin mirar la checklist.

**POUR = Perceivable, Operable, Understandable, Robust** (69:13).

**P — Perceivable.** Que se pueda percibir por algún canal.
- *Text alternatives*: alt text real. «An orange cat sleeping on a chair» (70:15).
- *Time-based media*: captions y transcripts para video y audio.
- *Adaptability y distinguishability*: el error del video es el borde rojo como **único** indicador
  de error (71:18). Necesita un segundo canal: texto, ícono.

**O — Operable.** Que se pueda operar.
- Teclado: todo lo que se hace con mouse se hace con teclado.
- **Tiempo suficiente**: modales que no desaparecen mientras alguien lee (72:51). El caso del
  usuario de lector de pantalla al que se le cierra el modal y queda en la página de abajo.
- **Navegación**: skip link, navegación consistente, foco visible (73:52).
- **Sin contenido que cause convulsiones**; sin apps interactivas inaccesibles (Flash).

**U — Understandable.** Que se entienda.
- **Predecible**: no cambiar el contexto sin avisar.
- **Errores**: mensaje claro que diga qué pasó y qué hacer, no «oh no, there has been an error» (75:58).
- **Legibilidad**: tipografías legibles, texto alineado a la izquierda, sin justificado en párrafos
  largos (77:00).

**R — Robust.** Que siga funcionando cuando cambia el entorno.
- Responsive, distintos dispositivos, VR, consolas, kioscos físicos (78:04).

**Ejercicio:** tomá una pantalla con formulario validado y auditá P/O/U/R con evidencia (captura o
selector). Entregable: 4 filas, cada una con un hallazgo y su nivel WCAG aproximado.

---

## Parte 3 — Estándares, leyes y gestión (20%)

### Módulo 8 — Instrumentos internacionales (78:46 – 87:42)

**Objetivo:** ubicar la jerarquía y saber qué instrumento hace qué.

**Advertencia del autor:** «I have a very Americentric view of the world» (78:47). El examen es **internacional**.

| Instrumento | Qué es y qué hace |
|---|---|
| **UDHR — Universal Declaration of Human Rights (ONU, 1948)** | Declaración, no convención: menos formalizada, pero base de todo. «Everyone is born free and equal» (81:51) |
| **CRPD — Convention on the Rights of Persons with Disabilities (ONU)** | **La primera convención específica** sobre personas con discapacidad. Es la que más se pregunta. Cubre salud, empleo, educación, y explícitamente **tecnología asistiva, accesibilidad y diseño universal** (84:29) |
| **Tratado de Marrakech (OMPI)** | Acceso a obras publicadas para personas ciegas o con discapacidad para leer: excepciones y limitaciones obligatorias. Habilitó EPUB, Kindle, .mobi accesibles (85:01) |
| **Regionales y nacionales** | Convención Interamericana (OEA), **Equality Act 2010** (UK), **ADA 1990** (EE.UU.), **AODA 2001** (Ontario) (86:39) |
| **Por dominio** | **CVAA** (comunicaciones y video, EE.UU.), **Section 508** (compras federales), **EN 301 549** (Europa) |

**El detalle que casi todos pierden:** declaración ≠ convención. Una declaración no obliga; una
convención sí crea obligaciones para los Estados que la ratifican. El examen lo pregunta.

**Ejercicio:** tabla de 3 columnas —instrumento / alcance (global, regional, nacional) /
obligatorio o no—. Entregable: 8 filas.

### Módulo 9 — Integrar la accesibilidad en la organización (87:42 – 93:42)

**Objetivo:** saber que la accesibilidad no es un proyecto sino un proceso, y leer la madurez.

**Tres modelos:**

1. **European Agency for Special Needs — 3 pasos** (88:45): **definir política** → **planificar y
   comprometerse** → **practicar** (revisar, testear, capacitar, usar los mismos decks internos).
2. **Carnegie Mellon — madurez de procesos** de accesibilidad en IT digital (89:49): desde
   *Initial* hasta **optimizing**, pasando por etapas con checkpoints y gobernanza.
3. **Accessibility Maturity Model** (90:53): niveles 1 a 5, de informal sin documentación a
   mejores prácticas e innovación.

**Idea fuerza:** sin proceso, la accesibilidad se degrada. «The second that you start forgetting
about it, accessibility is going to fall by the wayside» (88:14). Es la misma ley de entropía que
golpea a todo lo que no tiene dueño.

**Ejercicio:** ubicá tu organización o tu práctica propia en el modelo de 5 niveles, con una
evidencia por nivel (qué hay y qué falta). Entregable: nivel + 3 evidencias.

---

## Ejercicios por módulo

- [ ] **M1** — Un bug propio escrito desde los siete modelos (7 líneas).
- [ ] **M2** — Tabla de 8 categorías × (barrera web / barrera física / AT).
- [ ] **M3** — Auditoría de copy: disability-first y eufemismos, con diff.
- [ ] **M4** — Pitch de una frase para PM, legal y marketing.
- [ ] **M5** — Una pantalla pasada por los 7 principios, con defecto y fix.
- [ ] **M6** — Un README rediseñado con los 3 principios de UDL.
- [ ] **M7** — Auditoría POUR de un formulario, con evidencia.
- [ ] **M8** — Tabla de 8 instrumentos legales por alcance y obligatoriedad.
- [ ] **M9** — Nivel de madurez propio + 3 evidencias.

## Banco de preguntas

1. ¿Por qué los siete modelos de discapacidad **no** son mutuamente excluyentes, y qué te permite
   eso al leer a otra persona?
2. ¿Qué distingue al modelo **social** del **médico**, y cómo cambia la pregunta que te hacés
   frente a una interfaz inaccesible?
3. ¿Qué es el CAPD y con qué se confunde habitualmente?
4. ¿Cuál es la regla de destellos por segundo y de dónde sale ese número?
5. ¿Cuándo el identity-first language **pisa** la regla de person-first? ¿Quién decide?
6. Nombrá los siete principios del diseño universal y el ejemplo del curb cut: ¿qué prueba?
7. ¿Cuáles son los tres principios de UDL y qué responde cada uno (*qué*, *cómo*, *porqué*)?
8. En POUR, ¿qué falla cuando el error de un formulario se indica **solo** con borde rojo?
9. Diferencia entre declaración y convención, y por qué la CRPD importa más que la UDHR para a11y.
10. ¿Qué le pasa a la accesibilidad de una organización que no tiene proceso, según el video?

## Notas editoriales

- **Es el material de estudio, no un roadmap.** A diferencia del video de Practice Test Geeks,
  este recorre el contenido: los siete modelos con la voz del autor, las ocho categorías con
  barreras y AT, POUR con ejemplos de DOM, y los tres modelos de madurez. Sirve para aprender.
- **Captions manuales.** No hay ASR: los acrónimos y nombres propios están bien. No hace falta
  glosario de errores de reconocimiento.
- **Vigencia (2021).** Los conceptos, pesos y principios no cambiaron (verificado contra el BoK
  v4.0, oct-2023). Lo que **sí** puede haber cambiado: el conteo de demandas ADA de 2020 mencionado
  en 47:06, y el marco legal (WCAG 2.2 ya existe; ver si las leyes citadas se actualizaron).
  Regla: se estudia el concepto acá y se re-verifica el dato legal en la fuente.
- **Sesgo declarado.** El autor lo dice: «very Americentric» (78:47). El examen es internacional.
  Lo que falta y el BoK cubre: EN 301 549 / EAA en Europa, Ley 26.653 en Argentina, y el detalle
  de la Convención Interamericana.
- **El video se autocorrige.** En la descripción, el autor aclara que la UDHR es de **1948**, no
  1946. En el audio dice «late 1940s», así que el cue quedó bien; la corrección es suya y no se
  toca el transcript.
- **Dato de calibración útil:** el autor sacó **691/800** y confiesa qué le faltó estudiar (las
  estadísticas demográficas por país, 39:07). Es un aviso: la parte de datos del Dominio 1 es la
  que más se descuida.
- **Cruce con la otra clase:** el video de Practice Test Geeks da el formato y los pesos; este da
  el contenido. Son dos piezas distintas y se complementan sin solaparse.
- **Pendiente sugerido:** este curso cubre el **contenido**, pero dos piezas del examen quedan
  flojas —estadísticas demográficas (1D) y el detalle de leyes no estadounidenses (3B-3D)—. Ahí
  conviene ir directo al BoK.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
