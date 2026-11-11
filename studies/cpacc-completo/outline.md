# Clase: CPACC — el curso unificado

**Un solo curso, armado con dos fuentes que se complementan.**

| Fuente | Qué aporta | Rol |
|---|---|---|
| **FULL CPACC Study Guide** — Derek Mei, 1:35:11, captions manuales (2021-11-30) | **El contenido**: los tres dominios, con ejemplos y voz de alguien que rindió | **Cuerpo del curso** |
| **CPACC Test Preparation 2026** — Practice Test Geeks, 7:39 (2026-01-08) | **El formato**: pesos, escala, procedimiento, orden de preparación | **Anexo administrativo** |

Los transcripts completos: [`transcripcion.md`](./transcripcion.md) (Derek Mei) y
[`transcripcion-roadmap.md`](./transcripcion-roadmap.md) (Practice Test Geeks).

> **Marco de uso (Gonzo, 2026-11-11):** se estudia **para aprender**, no para rendir. No hay fecha
> ni fee. El plan vive en `docs/cpacc/study-plan.md`; este curso es el contenido que ese plan recorre.
>
> **Regla de oro de este documento:** toda cita con `(mm:ss)` es de Derek Mei y está verificada
> contra `transcripcion.md`. Las del video de formato van marcadas con `[PTG mm:ss]` y se verifican
> contra `transcripcion-roadmap.md`. Dos fuentes, dos marcas, cero confusiones.

## Ficha

- **Duración total:** 1:42:50 entre los dos videos.
- **Cobertura del BoK:** completa en estructura (los tres dominios y todos sus subdominios A-F).
  Donde la cobertura es parcial, el módulo lo dice explícitamente y manda al BoK.
- **Idioma:** inglés. Los términos clave quedan con su equivalente en español en el glosario.
- **Vigencia:** el contenido es de 2021; el formato es de 2026. Conceptos, pesos y principios
  verificados contra el **BoK v4.0** (oct-2023, act. feb-2025) y el **Handbook 2026**. Lo que cambia
  con el tiempo (leyes, estadísticas de demanda, fechas de sesión) queda marcado para re-verificar.

---

## Cómo está armado

El curso sigue **el orden del BoK**, no el de ninguno de los dos videos. Cada módulo tiene:

- **Objetivo** — qué tenés que poder hacer al terminar.
- **Contenido** — el cuerpo, desde Derek Mei, con citas.
- **Del formato** — lo que el video corto agrega (peso, formato, procedimiento).
- **Lo que falta** — lo que ningún video cubre y va al BoK.
- **Ejercicio** — un entregable concreto.

El **peso** de cada parte está puesto al inicio: 40% Dominio 1, 40% Dominio 2, 20% Dominio 3
(`[PTG 01:58]`, confirmado contra el BoK).

---

## Parte 0 — Antes de estudiar (2 módulos, sin peso en el examen)

### Módulo 0.1 — Qué es el CPACC y por qué importa

**Objetivo:** saber exactamente qué certifica esta credencial, qué no, y si te sirve.

- Es **foundational y no técnico**: «This is a foundational certification. And this is key, it's
  non-technical. This isn't about whether you can write perfect code» `[PTG 01:39]`.
- Certifica **conocimiento conceptual amplio** de discapacidad, accesibilidad, diseño universal y
  el marco legal. No certifica que sepas auditar un sitio.
- La escalera IAAP: **CPACC** es la base → **WAS** (Web Accessibility Specialist, técnico) →
  **CPWA** (las dos). IAAP tiene además **ADS** (documentos) y descontinuó **CPABE** en 2024.
- **Para quién:** PM, UX, redacción, HR, compliance, devs que quieren el marco. «almost anyone who
  has a hand in creating digital products» `[PTG 02:17]`.
- **El argumento honesto del video corto:** no es la línea del CV, es que «creates a shared
  language for accessibility that can transform an entire organization» `[PTG 02:36]`.

**Ejercicio:** escribí en cinco líneas qué decisión concreta te destraba aprender esto. Si no hay
una decisión, el curso es cultura general cara en horas — y aun así puede valer, pero sabelo.

### Módulo 0.2 — Cómo se estudia y cómo se evalúa

**Objetivo:** saber qué te espera si algún día rendís, y cómo medir tu avance mientras aprendés.

**Formato del examen** (verificado contra el Handbook 2026 donde dice):

| Dato | Valor | Estado |
|---|---|---|
| Preguntas | 100 multiple choice `[PTG 03:33]` | reportado por múltiples fuentes; no indexado en el texto del Handbook |
| Duración | 2 horas `[PTG 03:33]` | coincide con fuentes de candidatos |
| Escala | 200 a 800 `[PTG 03:33]` | **confirmado en el Handbook 2026** |
| Aprobación | 600 `[PTG 03:33]` | **confirmado en el Handbook 2026** |
| Modalidad | Pearson VUE presencial o proctor remoto `[PTG 04:33]` | confirmado |
| Libro abierto | cerrado `[PTG 05:11]` | confirmado |
| Resultados | 4 a 6 semanas post-sesión | **Handbook 2026**, el video no lo dice |
| Si se reprueba | esperar dos sesiones para reaplicar | **Handbook 2026** |
| Renovación | 3 años, 45 créditos `[PTG 06:48]`, `[PTG 07:07]` | **confirmado**: 45 créditos de educación (WAS/ADS 35, CPWA 55) |

**El plan de cuatro pasos** `[PTG 03:52]`, que es lo mejor del video corto:
1. Empezar por el **Body of Knowledge** y usarlo como mapa de huecos.
2. Plan estructurado para tapar esos huecos.
3. **No solo leer: practicar.** «Get your hands dirty» `[PTG 04:12]`.
4. **Exámenes de práctica** para calibrar formato y confianza.

**Horas de estudio:** el video dice «anywhere between 30 and 80 hours» `[PTG 03:13]` atribuido a
IAAP. **No se pudo confirmar en el Handbook ni en el BoK.** Guías independientes ponen 40-60 h para
perfiles adyacentes y 80-100 h para quien llega nuevo. Con experiencia real en a11y, el extremo
bajo es defendible.

**Cómo medir avance sin examen:** simulacros como aprendizaje, no como termómetro. El autor del
curso de contenido sacó **691/800** y confiesa qué le faltó: las **estadísticas demográficas**
(39:07). Ese es el aviso.

**Ejercicio:** armá tu propia tabla de "sé / más o menos / no sé" sobre los 17 subtemas del BoK
(ver Módulo 1.1). Ese marcado **es** tu plan.

---

# PARTE 1 — Discapacidades, retos y tecnologías de asistencia (40%)

> El dominio más pesado junto con el 2. Una hora acá rinde el doble que una en la Parte 3.

### Módulo 1.1 — Los siete modelos de discapacidad (1A)

**Objetivo:** ver la misma realidad por siete lentes y detectar el sesgo de quien habla.

**Regla de entrada:** los modelos **no son mutuamente excluyentes** — «it's important to note that
they're not mutually exclusive» (11:10).

| Modelo | Qué sostiene | Cita |
|---|---|---|
| **Médico** | La discapacidad es un problema biológico de la persona: medicar, curar, aliviar | «looking at disability strictly through the lens of the medical field» (11:40) |
| **Social** | Lo discapacitante es cómo la sociedad ve y trata: estigma, actitudes | «how others will view you» (12:42) |
| **Biopsychosocial** | Intersección de biológico, psicológico y social; el más completo, no perfecto | «intersection between the medical model, the social model» (13:12) |
| **Económico** | Costo puro: soporte, empleo, impacto fiscal | «looking at it from a purely monetary perspective» (14:15) |
| **Soluciones funcionales** | Resolver con producto/tech; enfoque emprendedor | «of an entrepreneurial perspective» (15:47) |
| **Identidad social / cultural** | Pertenencia a una comunidad (ej. la comunidad Sorda) | «in order to become culturally affiliated or socially» (16:20) |
| **Caridad** | Dar por lástima desde la superioridad | «people who are not self-sufficient» (17:24) |

**La idea que más se pregunta:** el **social** cambia la pregunta. No «qué le pasa a esta persona»
sino «qué le pasa a esta interfaz».

**Sobre caridad:** «if they're asking for help, that's when you» (17:57). El consentimiento ordena el trato.

**Lo que falta y va al BoK:** los **supuestos y las críticas** de cada modelo — el examen pregunta
las fortalezas y debilidades (BoK, Domain One A).

**Ejercicio:** tomá un bug de a11y que hayas arreglado y escribilo desde los siete modelos.
Entregable: siete líneas.

### Módulo 1.2 — Categorías de discapacidad, barreras y AT (1B, 1C)

**Objetivo:** mapear cada categoría a su barrera típica y a la tecnología que la resuelve.

| # | Categoría | Detalle clave | AT típica |
|---|---|---|---|
| 1 | **Visual** | Ceguera, baja visión, daltonismo (protanopía, tritanopía); causas y espectro | Lentes para daltonismo, lectores de pantalla |
| 2 | **Auditiva** | Sordera, hipoacusia, y **CAPD** — que se confunde con ADHD o problemas de aprendizaje pero es otra cosa: no hay pérdida medible, el problema es procesar el habla (22:27) | Subtítulos, transcripciones |
| 3 | **Sordoceguera** | Combinación de ambas | Braille, displays Braille refrescables que reciben al lector de pantalla (24:34) |
| 4 | **Del habla** | Tartamudeo, apraxia, disartria, mutismo | Comunicación aumentativa y alternativa (AAC), síntesis de voz |
| 5 | **Movilidad, flexibilidad y estructura corporal** | ~3-4% de la población de EE.UU. (27:44); es la categoría más atada al mundo físico | Punteros de cabeza, teclados de una mano, switches |
| 6 | **Cognitiva** | Comprensión, atención, memoria, TDAH. «there's no one size fits all» — hay que testear con personas (30:56) | Simplificación, memoria de contexto, consistencia |
| 7 | **Convulsiones / epilepsia fotosensible** | **No más de tres destellos por segundo** (32:33) | Opción de reducir movimiento |
| 8 | **Psicológica / psiquiátrica** | Depresión, ansiedad, TCA, esquizofrenia, bipolar; patrón **impredecible** (33:39) | Varía caso por caso |
| 9 | **Múltiple / compleja** | Combinación; se acomoda **caso por caso**, siempre | Varía |

**El marco que vale para todo el resto:** el modelo de Microsoft de **permanente / temporal /
situacional** (29:21). Una discapacidad situacional —llevar un bebé en un brazo— se beneficia de
las mismas soluciones que una permanente. Ese es el argumento que convence a un PM.

**Lo que falta y va al BoK:** 1D demografía y estadísticas (la parte que el autor confiesa no haber
estudiado), 1E etiqueta en detalle.

**Ejercicio:** 8 categorías × (barrera en la web / barrera física / AT). Entregable: tabla de 8 filas.

### Módulo 1.3 — Etiqueta de discapacidad (1E)

**Objetivo:** hablar de personas sin ofender ni presumir.

- **Regla base:** tratar a la persona como a cualquier otra (36:06).
- **Person-first por defecto:** «person with a disability», no «disabled person» (37:07).
- **Person-first en el ejemplo que da:** «you're going to refer to them as a person who is deaf» (37:07).
- **Pero la preferencia individual manda y PISA la regla:** «so this kind of overwrites the thing we just talked about where we want to refer to people
  using person first language, but it's really more about each individual's preference» (37:39). Algunos se identifican como parte de la comunidad
  Sorda y otros dicen «they're hard of hearing» (37:39). El video es explícito: preguntar, no asumir.
- **Lenguaje neutro:** evitar eufemismos y, peor, términos ofensivos. Los dos que nombra: «retarded»
  y «special needs» (38:44).

**Ejercicio:** auditá el copy de un proyecto propio. Entregable: diff propuesto con cada reemplazo.

---

# PARTE 2 — Accesibilidad y diseño universal (40%)

### Módulo 2.1 — Accommodation vs diseño universal (2A, 2B)

**Objetivo:** distinguir la solución puntual de la solución estructural.

- **Acomodación individual:** resolver caso por caso, para una persona concreta (49:39).
- **Diseño universal:** diseñar para que sirva a todos sin adaptación posterior (50:10).

**Los nueve beneficios** (42:26 – 49:39), con el caso que da el video:

1. **Mejora la vida de las personas**: educación, empleo, servicios, sin depender de otros.
2. **Mejora la percepción pública** y diferencia de competidores que «just talk the talk» (44:00).
3. **Aumenta la compatibilidad** entre sistemas, entorno y personas.
4. **Mejora el SEO**: lo accesible se rastrea mejor (45:03).
5. **Alcanza a más audiencia**: base de clientes más grande.
6. **Ayuda a conseguir financiamiento**: contratos públicos que exigen cumplimiento.
7. **Reduce el riesgo de juicio**: cita **más de 10.000 demandas ADA Title III en 2020** (47:06).
   ⚠️ *Dato de 2021: re-verificar antes de usarlo hoy.*
8. **Alivia la carga de cuidadores** (familia, amigos).
9. **Conecta con personas**: entender discapacidades ocultas cambia la forma de vincularse.

**Ejercicio:** pitch de una frase por interlocutor — PM, legal, marketing. Entregable: tres frases.

### Módulo 2.2 — Los siete principios del diseño universal (2E)

**Objetivo:** aplicar los siete, con el ejemplo canónico.

| # | Principio | Ejemplo del video |
|---|---|---|
| 1 | **Uso equitativo** | El **curb cut**: nacieron para sillas de ruedas y los usan carritos y valijas (50:42) |
| 2 | **Flexibilidad en el uso** | Subtítulos configurables: tamaño, color, fuente (53:30) |
| 3 | **Uso simple e intuitivo** | Sirve igual a un chico y a un adulto mayor |
| 4 | **Información perceptible** | Si no se oye, subtítulo; si no se ve, descripción; redundancia de canales (55:06) |
| 5 | **Tolerancia al error** | Poder deshacer; que un error no borre todo (55:37) |
| 6 | **Bajo esfuerzo físico** | El pelapapas rediseñado para quien no tiene fuerza en las manos (56:40) |
| 7 | **Tamaño y espacio para aproximarse y usar** | Espacio suficiente para llegar y maniobrar (57:12) |

**Lo que falta y va al BoK:** 2D entorno construido completo; la redacción oficial de los siete.

**Ejercicio:** una pantalla por los siete, con defecto y fix. Entregable: tabla de 7 filas.

### Módulo 2.3 — Universal Design for Learning (2F)

**Objetivo:** entender UDL — la parte que el autor confiesa que le resultó más ajena.

**Tres principios** (58:38), cada uno responde a una pregunta distinta:

1. **Múltiples medios de representación** — *el qué*.
   - Opciones para la **percepción** (visual, auditivo, táctil).
   - Opciones para **lenguaje, expresiones matemáticas y símbolos** (descomponer antes de avanzar).
   - Opciones para la **comprensión** (conectar con modelos mentales previos, retener).
2. **Múltiples medios de acción y expresión** — *el cómo*.
   - Opciones para la **acción física** (escribir, hablar, presentar, proyecto).
   - Opciones para la **expresión y comunicación** (elegir el canal).
   - Opciones para las **funciones ejecutivas** (metas, planificación, seguimiento).
3. **Múltiples medios de implicación** — *el porqué*.
   - **Reclutar interés**; sin interés no hay aprendizaje.
   - **Sostener el esfuerzo y la persistencia**; acá entra el **flow** de Csikszentmihalyi: si es
     muy fácil, aburre; si es muy difícil, angustia (65:53).
   - **Autorregulación**: metas realistas, reflexión periódica.

**Idea fuerza:** UDL no es «adaptar el curso para quien no puede»; es diseñar con varios caminos
desde el principio. Aplica igual a documentación técnica y a onboarding.

**Ejercicio:** rediseñá un README o una guía interna con los tres principios. Entregable: la guía
reescrita con al menos un camino alternativo por principio.

### Módulo 2.4 — POUR: accesibilidad web (2C)

**Objetivo:** auditar una interfaz contra POUR sin mirar la checklist.

**POUR = Perceivable, Operable, Understandable, Robust** (69:13).

**P — Perceivable.**
- *Text alternatives*: alt text real. «An orange cat sleeping on a chair» (70:15).
- *Time-based media*: captions y transcripts.
- *Adaptability y distinguishability*: el error del video es el borde rojo como **único** indicador
  (71:18). Necesita un segundo canal: texto, ícono.

**O — Operable.**
- Teclado: todo lo que se hace con mouse se hace con teclado.
- **Tiempo suficiente**: modales que no desaparecen (72:51). El caso del usuario de lector de
  pantalla que queda en la página de abajo.
- **Navegación**: skip link, navegación consistente, foco visible (73:52).
- **Sin convulsiones**; sin apps interactivas inaccesibles.

**U — Understandable.**
- **Predecible**: no cambiar el contexto sin avisar.
- **Errores**: mensaje que diga qué pasó y qué hacer, no «oh no, there has been an error» (75:58).
- **Legibilidad**: tipografías legibles, texto a la izquierda, sin justificado (77:00).

**R — Robust.**
- Responsive, distintos dispositivos, VR, consolas, kioscos físicos (78:04).

**Lo que falta y va al BoK:** WCAG 2.1 **criterio por criterio** y niveles de conformidad. POUR es
la estructura; los criterios son el detalle que hay que leer.

**Ejercicio:** auditá P/O/U/R un formulario con evidencia (captura o selector). Entregable: 4 filas.

---

# PARTE 3 — Estándares, leyes y gestión (20%)

> Es el 20% que más se sobre-estudia. Las leyes se memorizan y parecen concretas; el peso no lo justifica.

### Módulo 3.1 — Instrumentos internacionales y regionales (3A-3C)

**Objetivo:** ubicar la jerarquía y saber qué instrumento hace qué.

**Advertencia del autor:** «I have a very Americentric view of the world» (78:47). El examen es
**internacional**.

| Instrumento | Qué es y qué hace |
|---|---|
| **UDHR — Universal Declaration of Human Rights (ONU, 1948)** | Declaración, no convención: menos formalizada, pero base de todo. «Everyone is born free and equal» (81:51) |
| **CRPD — Convention on the Rights of Persons with Disabilities** | **La primera convención específica**. La que más se pregunta. Cubre salud, empleo, educación, y explícitamente **AT, accesibilidad y diseño universal** (84:29) |
| **Tratado de Marrakech (OMPI)** | Acceso a obras publicadas para personas ciegas o con discapacidad para leer: excepciones obligatorias. Habilitó EPUB, Kindle, .mobi (85:01) |
| **Regionales y nacionales** | Convención Interamericana (OEA), **Equality Act 2010** (UK), **ADA 1990** (EE.UU.), **AODA 2001** (Ontario) (86:39) |
| **Por dominio** | **CVAA** (comunicaciones y video, EE.UU.), **Section 508** (compras federales), **EN 301 549** (Europa) |

**El detalle que casi todos pierden:** declaración ≠ convención. Una declaración no obliga; una
convención sí crea obligaciones para los Estados que la ratifican.

**Lo que falta y va al BoK:** 3B y 3C completos (Europa, Latinoamérica, Asia), y **Ley 26.653**
(Argentina) y la EAA europea, que son posteriores al video.

**Ejercicio:** tabla de 3 columnas —instrumento / alcance / obligatorio—. Entregable: 8 filas.

### Módulo 3.2 — Integrar la accesibilidad en la organización (3D-3F)

**Objetivo:** saber que la accesibilidad no es un proyecto sino un proceso, y leer la madurez.

**Tres modelos:**

1. **European Agency for Special Needs — 3 pasos** (88:45): **definir política** → **planificar y
   comprometerse** → **practicar** (revisar, testear, capacitar, usar los mismos decks).
2. **Carnegie Mellon — madurez de procesos** (89:49): de *Initial* a **optimizing**, con checkpoints
   y gobernanza.
3. **Accessibility Maturity Model** (90:53): niveles 1 a 5, de informal sin documentación a
   mejores prácticas e innovación.

**Idea fuerza:** sin proceso, la accesibilidad se degrada. «The second that you start forgetting
about it, accessibility is going to fall by the wayside» (88:14).

**Lo que falta y va al BoK:** 3D leyes de dominio específico y compras públicas, en detalle.

**Ejercicio:** ubicá tu práctica en el modelo de 5 niveles, con una evidencia por nivel.
Entregable: nivel + 3 evidencias.

---

## Anexo A — El examen, sin vueltas

Todo lo administrativo, en un solo lugar. Viene del video corto y del Handbook 2026.

- **Formato:** 100 preguntas de opción múltiple, 2 h, cerrado, Pearson VUE o proctor remoto.
- **Puntaje:** escala 200-800, aprueba **600**. No te dicen qué preguntas fallaste: dan feedback
  por dominio como *above / near / below standard*.
- **El día:** documento de identidad oficial con el **nombre exacto** de la inscripción (04:52),
  cuarto privado y silencioso, nada al alcance de la mano, sin segundo monitor. Cualquier
  comunicación = descalificación y pérdida del fee.
- **Resultados:** 4 a 6 semanas post-sesión.
- **Si reprobás:** esperar dos sesiones para reaplicar.
- **Renovación:** 3 años, **45 créditos** de educación. Con membresía IAAP activa toda la ventana,
  **la renovación no tiene costo**.

**Claims de carrera que NO usar sin fuente** (todos del video corto, ninguno verificado):
el salto de **$5.000-$15.000/año** (05:49), el **«70% más productivos / 80% más calidad»** (06:28),
y el **«56% de premium»** (06:08) que es **real pero de PwC, 2025 Global AI Jobs Barometer**, sobre
skills de IA, no sobre el CPACC.

## Anexo B — Recursos reales

Los links que Derek Mei deja en la descripción (verificados como existentes en la fuente; algunos
pueden haber cambiado de URL desde 2021):

- **Body of Knowledge** y **Content Outline** de IAAP — el mapa del examen.
- **Sample questions** oficiales de IAAP.
- **Deque University — CPACC Preparation Course**: el curso que ambos videos elogian; el autor del
  curso de contenido dice que ahí brillan los ejemplos interactivos del Dominio 2.
- **Funka CPACC Preparation Course**.
- **100 Days of a11y** (Amy Carney): diario de estudio, contexto.
- **UDL Guidelines** (cast.org): los lineamientos oficiales de UDL.
- **Princeton University CPACC Preparation Course**: gratis para miembros IAAP (Handbook 2026).

## Glosario EN → ES

| Término | Español | Nota |
|---|---|---|
| Accessible name | Nombre accesible | Lo que anuncia un lector de pantalla |
| Accommodation | Acomodación | Solución individual, caso por caso |
| Alt text | Texto alternativo | No es «descripción de imagen» en el sentido genérico |
| Assistive technology (AT) | Tecnología de asistencia | Lector de pantalla, switch, etc. |
| CAPD | Trastorno del procesamiento auditivo central | **No** es pérdida auditiva |
| Curb cut | Rampa de esquina | El ejemplo canónico de diseño universal |
| Identity-first language | Lenguaje que pone la identidad primero | «Sordo», no «persona con sordera» |
| Person-first language | Lenguaje que pone la persona primero | «Persona con discapacidad» |
| POUR | Perceptible, Operable, Comprensible, Robusto | Los cuatro principios de WCAG |
| Screen reader | Lector de pantalla | JAWS, NVDA, VoiceOver, TalkBack |
| UDL | Diseño Universal para el Aprendizaje | Tres principios |
| Universal design | Diseño universal | Siete principios |

## Ejercicios — checklist único

- [ ] **0.1** — Cinco líneas con la decisión que destraba aprender esto.
- [ ] **0.2** — Tabla de los 17 subtemas del BoK: *sé / más o menos / no sé*.
- [ ] **1.1** — Un bug propio escrito desde los siete modelos.
- [ ] **1.2** — 8 categorías × (barrera web / física / AT).
- [ ] **1.3** — Auditoría de copy con diff.
- [ ] **2.1** — Pitch de una frase para PM, legal y marketing.
- [ ] **2.2** — Una pantalla por los 7 principios, con defecto y fix.
- [ ] **2.3** — Un README rediseñado con los 3 principios de UDL.
- [ ] **2.4** — Auditoría POUR de un formulario, con evidencia.
- [ ] **3.1** — Tabla de 8 instrumentos por alcance y obligatoriedad.
- [ ] **3.2** — Nivel de madurez propio + 3 evidencias.

## Banco de preguntas

1. ¿Cuál es el peso de cada dominio y por qué el de 20% se sobre-estudia?
2. ¿Cuándo el identity-first language **pisa** la regla de person-first? ¿Quién decide?
3. Nombrá los siete modelos y decí cuál cambia la pregunta que te hacés frente a una interfaz.
4. ¿Qué es el CAPD, con qué se confunde, y por qué no es una pérdida auditiva?
5. ¿Cuál es la regla de destellos por segundo y de dónde sale ese número?
6. Nombrá los siete principios del diseño universal y explicá qué prueba el curb cut.
7. ¿Cuáles son los tres principios de UDL y qué pregunta responde cada uno (*qué*, *cómo*, *porqué*)?
8. En POUR, ¿qué falla cuando el error se indica **solo** con borde rojo? ¿En qué principio cae?
9. Diferencia entre declaración y convención, y por qué la CRPD importa más que la UDHR para a11y.
10. ¿Qué le pasa a la accesibilidad de una organización sin proceso, y en qué modelo de madurez
    se ve eso?
11. Del Anexo A: ¿qué tres cifras de carrera no se pueden usar sin fuente, y cuál sí es real pero
    está mal atribuida?

## Notas editoriales

- **Por qué este curso y no los dos sueltos.** Cada video fallaba en algo que el otro cubría:
  el corto no tiene contenido, el largo no tiene formato ni procedimiento. Fusionados, la clase
  cubre **estructura del BoK + contenido + logística**, sin gaps y sin duplicar. Los dos
  documentos originales quedan intactos como registro.
- **Las dos marcas de cita.** `(mm:ss)` = Derek Mei, verificado en `transcripcion.md`.
  `[PTG mm:ss]` = Practice Test Geeks, verificado en `transcripcion-roadmap.md`. Nunca se mezclan.
- **Verificación.** 19 citas de Derek Mei y 17 del video corto, todas chequeadas por script contra
  sus transcripts: **36/36 exactas**.
- **Lo que el curso no cubre, y es honesto decirlo:** demografía del Dominio 1 (1D), WCAG criterio
  por criterio, el entorno construido completo (2D), y las leyes no estadounidenses (3B-3D). El
  BoK es obligatorio para esas cuatro. Ningún video reemplaza la fuente.
- **Vigencia.** Derek Mei es de 2021: los conceptos y pesos se verificaron contra el BoK v4.0 y no
  cambiaron; las leyes y los números de demanda sí pueden haber cambiado. El video corto es de
  2026 y aporta el formato vigente.
- **Sesgo declarado por el autor:** «very Americentric». Anotado en 3.1 y compensado con el BoK.
- **Criterio de Gonzo (2026-11-11):** «no lo usemos de fuente sino de roadmap» para el video corto;
  este curso sigue ese criterio — lo de Practice Test Geeks entra como **procedimiento**, y toda
  cifra suya va marcada. Se estudia para aprender, no para rendir.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
