---
name: "design-direction"
description: "Dirección de arte de una UI antes de implementarla: las 4 preguntas (propósito, tono, restricciones, diferenciación), la decisión de contexto (herramienta funcional vs pieza memorable) y el orden de pensamiento layout → tema → animación → código. Use when starting new UI without an existing aesthetic direction (landing, portfolio, dashboard, product), when choosing typography or visual theme for a project, or when a design is technically correct but has no identity. No cubre implementación ni WCAG: eso es frontend-ui-engineering."
---

# Design Direction

## Overview

Decide la **dirección de arte** de una interfaz **antes** de escribir código de UI: qué se quiere que se sienta, qué decisiones la sostienen y qué se sacrifica para conservarlas. No es una skill de implementación: responde el **por qué** del aspecto visual; el **cómo** de escribirlo vive en [frontend-ui-engineering](../frontend-ui-engineering/) y el ritmo de trabajo en [incremental-implementation](../incremental-implementation/).

```
design-direction (decidir) → incremental-implementation (el cómo, por slices) →
frontend-ui-engineering (la ejecución) → a11y-at-validation (cerrar el loop)
```

## When to Use

- UI nueva sin dirección estética definida: landing, portfolio, página de marca, producto, dashboard nuevo.
- Se va a elegir tipografía o tema visual para un proyecto o superficie nueva.
- El diseño es técnicamente correcto pero no tiene identidad: ninguna decisión visual que se pueda defender en voz alta.

**No usar para:** implementar la UI, estados, WCAG, verificación o anti-patrones de ejecución - todo eso es [frontend-ui-engineering](../frontend-ui-engineering/). Esta skill termina donde empieza el código.

---

## 1. Las 4 preguntas antes de codear

Se responden en orden y por escrito. Un brief sin respuestas escritas es opinión, no dirección.

**1. Propósito.** ¿Qué problema resuelve la interfaz? ¿Quién la usa, en qué momento y con qué apuro? ¿Qué única acción debe permitir? Si la respuesta es un verbo (comparar, cargar, vender), hay diseño posible; si es un adjetivo ("moderno"), todavía hay solo gusto.

**2. Tono.** Se elige UNA dirección conceptual y se responde por ella: minimalismo refinado, maximalista bold, editorial, orgánico, industrial, utilitario, etc. La regla:

> La clave es la **intencionalidad**, no la intensidad.

Un minimalismo refinado y un maximalista bold son igualmente válidos si cada decisión responde a la dirección elegida. Lo indefendible no es ningún extremo: es el promedio sin criterio, "moderno" sin más.

**3. Restricciones.** Framework y stack de estilado (CSS Modules + tokens), budget de performance (peso de assets, fuentes), accesibilidad desde el diseño (contraste como material del tema, `prefers-reduced-motion` previsto desde el plan). Las restricciones no van contra el tono: son el material con el que se talla. La validación con AT cierra el loop después - ver [a11y-at-validation](../a11y-at-validation/).

**4. Diferenciación.** ¿Cuál es la ÚNICA cosa que alguien va a recordar? Si la respuesta serviría para cualquier UI del mundo, no es diferenciación. En una herramienta funcional la respuesta honesta es otra en naturaleza: se recuerda lo que no estorba.

**Salida de esta fase:** el brief de dirección (5-10 líneas, junto al proposal de [openspec-pattern](../openspec-pattern/)): tono elegido, contexto de cada superficie, restricciones duras y la única cosa memorable.

---

## 2. Primero QUÉ es: herramienta funcional vs pieza memorable

La pregunta que resuelve el conflicto eterno de la tipografía. Se responde antes de elegir fuentes, nunca después:

| | Herramienta funcional | Pieza memorable |
|---|---|---|
| Superficies típicas | dashboard, formulario, tabla densa, admin | landing, portfolio, página de marca |
| La neutralidad | **ES la decisión**: el usuario trabaja ahí horas y la fricción visual se paga por sesión | **es pereza**: una página que se parece a todas no se recuerda |
| Tipografía | fuentes de sistema o Inter: legibilidad y densidad mandan | display con carácter + una body neutra: la pareja display/body es la decisión |
| La prueba de oro | "no pienso en la interfaz mientras la uso" | "podría describirla de memoria" |

Regla: **primero preguntar qué es, después elegir tipografía. Nunca al revés.**

Matiz: un mismo producto tiene ambas superficies. La decisión es por superficie, y el puente entre las dos son los tokens compartidos (`--primary`, `--border`): la landing puede gritar mientras el dashboard susurra, con el mismo vocabulario.

---

## 3. El orden del pensamiento: layout → tema → animación → código

Este orden es el punto de entrada del pensamiento de diseño. No es una preferencia: mover un bloque en un wireframe cuesta un borrador, y descubrirlo después de animar cuesta reescribir estilos y transiciones.

1. **Layout** - estructura, jerarquía de lectura y ubicación del CTA. El artefacto es el wireframe ASCII que [frontend-ui-engineering](../frontend-ui-engineering/) define: no se escribe código de layout sin wireframe.
2. **Tema** - color y tipografía bajados a tokens semánticos propios (`--primary`, `--muted`, `--border`); acá se aplica la decisión de contexto (herramienta vs pieza memorable); iconografía con **Lucide**, nunca emojis como iconos.
3. **Animación** - solo el movimiento que comunica. La micro-sintaxis y las duraciones canónicas viven en [frontend-ui-engineering](../frontend-ui-engineering/); acá se decide si el movimiento existe y qué cuenta.
4. **Código** - recién acá se implementa: la ejecución es [frontend-ui-engineering](../frontend-ui-engineering/) y el ritmo de slices verificables es [incremental-implementation](../incremental-implementation/), que trata cada fase como un paso verificable antes del siguiente.

---

## 4. La regla de intencionalidad

> La ausencia de look malo no es un look bueno.

Evitar el look IA (púrpura, gradientes, cards de stock, hero genérico: anti-patrones ya tabulados en [frontend-ui-engineering](../frontend-ui-engineering/)) apenas evita un defecto. Quitar el púrpura no deja identidad: deja una UI anodina y correcta. Un look bueno es **afirmativo**: declara una dirección y responde por cada decisión.

Test de compromiso: para cada decisión visual importante preguntar "¿por qué?". Si la respuesta es "para no parecer el look malo" o "para parecerse a X", no es una decisión propia: es otra neutralidad con disfraz.

Una dirección excluye alternativas. Si todo es posible, nada está elegido.

---

## Descubrimiento y registro

### Elegir la dirección con previews: show, don't tell

Para elegir una dirección, en vez de describir los estilos en texto, generar 2-3 micro-previews visuales (una card, un header o una title-slide en cada estilo) y mostrarlos para que el humano elija: la conversación abstracta sobre "qué tono queremos" se reemplaza por una reacción a lo que se ve.

Regla complementaria: usar preview visual cuando el contenido ES visual (layout, wireframe, paleta); usar texto cuando es conceptual (propósito, trade-offs, opciones A/B/C/D).

Test: "¿el humano entendería mejor viéndolo que leyéndolo?"

Los previews solo eligen la dirección: no reemplazan el wireframe ASCII de la fase de layout, que vive en [frontend-ui-engineering](../frontend-ui-engineering/).

### Contraste extremo de peso y tamaño (pieza memorable)

Para una pieza memorable, el contraste tipográfico puede ser extremo, no incremental:

- Peso: 100 vs 900, no solo 400 vs 700. El salto máximo de peso define el registro.
- Tamaño: salto mínimo de 3x (body 14-16px vs hero 48px+).

Complementa, no reemplaza, la regla "un canal por paso de nivel" (sección Output Gates): ahí el foco es el salto por PASO de jerarquía entre dos niveles adyacentes; acá es el registro general de la pieza. Contexto: solo pieza memorable; en herramienta funcional rige la neutralidad (la pregunta de contexto, sección 2).

### Paletas derivadas de temas de editor

Un origen de paleta válido y no obvio: los temas de IDE (Dracula, Nord, Tokyo Night, Monokai). Son paletas ya balanceadas por uso intensivo y con reglas propias de contraste. Da mejor resultado que elegir de una lista plana de paletas: da un ORIGEN con criterio en vez de una opción entre muchas. La paleta elegida se baja igual a tokens semánticos según "Anclaje al stack".

### La tabla 80/20 de calidad percibida

Dónde se va el esfuerzo, por impacto percibido:

| Canal | Peso en la calidad percibida |
|---|---|
| Tipografía | ~40% |
| Spacing | ~25% |
| Color | ~20% |
| Lo demás (sombras, bordes, motion) | ~15% |

Tipografía + spacing suman ~65% de la calidad percibida: ahí se invierte primero. La tabla también explica por qué las secciones de tipografía y spacing son las más extensas: es proporción de impacto, no verbosidad.

---

## Anclaje al stack

- **Tokens semánticos como contrato.** La dirección se baja a tokens (`--primary`, `--muted`, `--border`); ninguna decisión de color o tipografía viaja como número suelto al CSS. La dirección expresa relaciones, no valores de moda:

```css
/* Ejemplo del vocabulario decidido para una dirección "editorial calmada" */
:root {
  --primary: /* un solo color con presencia - todo lo demás es neutro */;
  --muted:   /* el gris de ESTA paleta, no el gris por defecto de nadie */;
  --border:  /* línea discreta: la jerarquía se construye con tipografía y espacio, no con cajas */;
}
```

- **Lucide** para toda la iconografía (regla del workspace: nunca emojis como iconos). El tono también se juega en los iconos: un solo set, con trazo y peso consistentes con la dirección.
- **CSS Modules** como vía de estilado, con clases semánticas que nombran por rol y no por apariencia.
- **Fuera de alcance de stack:** Tailwind y sus utilidades como filosofía de estilado, y Shadcn/ui o Radix, que siguen sin ADR de adopción - el TODO abierto vive en `frontend-ui-engineering`; esta skill no decide stack, solo dirección.
- **`a11y-at-validation` cierra el loop:** las restricciones de la pregunta 3 ya incluyen contraste, `prefers-reduced-motion` y AT. Toda UI que cambie lo que anuncia un lector de pantalla se valida manualmente según esa skill antes de darse por terminada.

---

## Errores comunes de dirección

| Error | Por qué es trampa | Corrección |
|---|---|---|
| Elegir la tipografía antes de definir el contexto | Una display con carácter en una tabla densa es ruido; una neutra en una landing es pereza | La pregunta de contexto primero: ¿qué es esta superficie? |
| Neutralidad que nadie decidió | "No arriesgar" parece prudencia y es abandono | Si la superficie es una herramienta, anotarlo como decisión; si no, elegir dirección y responder por ella |
| Copiar el tema de un producto exitoso | El tema del otro responde al propósito del otro; no sobrevive a tus restricciones | Partir del propósito propio y dejar que el tema salga de ahí |
| Tono elegido sin pasar por restricciones | Un maximalista bold sin budget de performance se implementa mal o no se implementa | Las restricciones recortan el tono antes de llegar al código |
| Confundir "diferente" con "diferenciado" | El gimmick sin propósito también es una no-dirección, solo que más ruidosa | La diferenciación responde al propósito; el gimmick lo ignora |

---

## Output Gates: verificación de diseño

La dirección decide; los gates verifican que se cumplió. Antes de dar por terminado un artefacto de diseño (wireframe, composición de una vista, tokens aplicados a una superficie) se corre la batería completa: es la diferencia entre "la dirección está escrita" y "la dirección se respetó". Son gates de diseño visual, previos a la implementación. No reemplazan la validación completa (WCAG, AT, `prefers-reduced-motion`), que sigue viviendo en [a11y-at-validation](../a11y-at-validation/).

### Jerarquía como ranking

La jerarquía no es una consecuencia de los estilos: es un **ranking** decidido antes. Se inventaría cada elemento de la vista y se le asigna un nivel 1 a 3 según su importancia para el usuario:

- **1 - debe verse:** el foco o la acción primaria. **Exactamente uno por vista.**
- **2 - de apoyo:** sostiene al 1 sin competir con él.
- **3 - metadata:** está disponible, pero no compite por la mirada.

Check: una captura en escala de grises debe revelar el ranking en 3 segundos. Si a los 3 segundos no se sabe dónde mirar, no hay jerarquía: hay una lista de estilos.

**Un canal por paso de nivel.** Dos niveles adyacentes deben diferir en un canal: tamaño (x1.25), peso (+300) o un salto de luminosidad. Tres tweaks chicos apilados leen como ruido, no como niveles. Ejemplo: 18px/600 al lado de 16px/400 son dos medio-pasos y rankean mal; usar 20px/400 o 16px/700.

### Los 6 gates

Se corren los seis, en orden, antes de entregar. Un gate que falla no se documenta: se corrige y se vuelve a correr la batería.

1. **Grayscale test:** en desaturado, ¿el ranking 1-3 sigue siendo obvio en 3 segundos?
2. **Squint test:** desenfocada la vista, ¿saltan exactamente el título y la acción primaria?
3. **Alignment count:** ¿hay 3 líneas de alineación vertical o menos, y cada elemento está sobre una?
4. **Spacing audit:** ¿cada gap es múltiplo de la base espacial, y el gap entre grupos es >= 2x el gap intra-grupo?
5. **Contrast check:** ¿cada par texto/fondo cumple su piso? 4.5:1 body, 3:1 texto large y componentes de UI.
6. **Single rank-1:** ¿hay exactamente una acción primaria o un foco por vista? Con dos primarias, ninguna lo es.

### Design in grayscale first

Layout, jerarquía y spacing tienen que funcionar sin color. El color entra último y para una sola cosa: codificar significado (estado, acción, marca). Nunca rescatar con color una jerarquía que no se sostiene sola: esa decisión falla el grayscale gate y falla para cerca del 8% de los hombres con daltonismo (CVD). Tamaño, peso y espacio construyen la jerarquía; el color la confirma.

### Space belongs to what it labels

El espacio pertenece a lo que etiqueta: un heading está más cerca del texto que encabeza (8px) que de la sección anterior (32px). Gaps iguales destruyen el agrupamiento: si la distancia no distingue, la vista se lee como una pila plana de bloques.

### Optical beats mathematical

A nivel componente, la ótica gana a la matemática: iconos, triángulos y botones de play necesitan un shift de 1 a 3px hacia su peso visual para verse centrados. Default: la grilla es matemática (layout); la corrección ótica se permite por componente. Nunca al revés: una grilla corregida a ojo rompe las alineaciones que el alignment count mide.

### One radius scale per artifact

Una sola escala de radios por artefacto (ej. 4/8/16), y ningún radio fuera de escala. Radios mezclados en elementos hermanos (un card con 8px al lado de otro con 11px) es el tell más rápido de una UI generada sin revisar.

### Traps que los gates atrapan

| Trap | Por qué falla | Qué hacer |
|---|---|---|
| Centrar texto largo | Cada línea arranca en un punto distinto y el ojo pierde el anclaje de lectura | Texto corrido alineado a la izquierda; el centrado queda para titulares y piezas cortas |
| Dar énfasis con bold + grande + color a la vez | Tres canales a la vez leen como ruido, no como énfasis | Un canal por paso de nivel: elegir uno |
| Color como única señal de estado | Falla el grayscale gate y falla para ~8% con CVD | Codificar el estado también con texto, icono o peso |
| Grises puros al lado de un accent saturado | El accent vibra, los neutros se apagan y el ranking se miente | Neutros que pertenezcan a la paleta - la regla vive en [frontend-ui-engineering](../frontend-ui-engineering/) |
| Rellenar cada espacio vacío | El espacio es la señal de agrupamiento; rellenarlo lo borra | El gap entre grupos es un dato: >= 2x intra-grupo |
| Restyling antes de rankear | Estilar sin ranking previo produce jerarquía aleatoria | Inventariar y rankear 1-3 antes de tocar un estilo |
| Diseñar solo el happy state | La vista real pasa más tiempo en vacío, carga o error | Rankear y verificar los estados de borde con la misma batería |

---

## Cuando NO aplicar una direccion bold

Una direccion fuerte no siempre es la respuesta. Antes de comprometerse con una pieza memorable, chequear el contexto: hay superficies donde el criterio correcto es la sobriedad, no el caracter.

| Contexto | Por que la direccion bold estorba | Que hacer |
|---|---|---|
| Conversion (e-commerce, checkout, alta) | La friccion visual cuesta ventas: cada distraccion es un abandono | Simplicidad: claridad sobre creatividad |
| Informacion densa (dashboard, admin, tablas) | La densidad ya es ruido; encima, ruido estetico | Es una herramienta funcional: neutralidad decidida |
| Accessibility-first | El motion pesado y los efectos custom pueden excluir | WCAG primero; efectos solo si no bloquean |
| Presupuesto o tiempo acotado | Una direccion bold mal ejecutada es peor que una sobria bien hecha | Ejecutar poco, pero impecable |

La pregunta que ordena todo sigue siendo la misma: **que es esta superficie**. Un sitio que convierte y un portfolio que se recuerda piden decisiones opuestas, y ambas pueden estar bien tomadas. El error no es elegir un extremo: es no elegir, o elegir el equivocado para el contexto.

---

## Salida esperada

Tres artefactos, todos antes del primer commit de UI:

1. **Brief de dirección:** las 4 preguntas respondidas (tono elegido, contexto por superficie, restricciones, la única cosa memorable). Vive junto al proposal/contrato.
2. **Tokens decididos:** `--primary`, `--muted`, `--border` (y el par display/body si la superficie lo pide), con la decisión anotada.
3. **Wireframe ASCII por superficie:** el artefacto de la fase de layout, definido en [frontend-ui-engineering](../frontend-ui-engineering/).

Con eso la ejecución arranca en [incremental-implementation](../incremental-implementation/) y en [frontend-ui-engineering](../frontend-ui-engineering/), y se cierra con [a11y-at-validation](../a11y-at-validation/).

_Relacionadas: `frontend-ui-engineering` (ejecución) · `incremental-implementation` (ritmo) · `a11y-at-validation` (validación) · `openspec-pattern` (contrato previo). Origen: `docs/specs/design-direction-spec.md`._