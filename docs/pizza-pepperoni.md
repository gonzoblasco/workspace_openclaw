# La Historia de la Pizza de Pepperoni

> Proyecto viviente: de la primera mordida al dominio total. Cada batch es un capitulo.
> Comienza: 2026-09-17. Autoria: Gonzo + Kanam.

---

## Capitulo 0 - Antes de la primera harina

### El origen (13 de septiembre de 2026)

La pizza no entro a nuestra historia por hambre. Entro por una prueba.

Ese dia estabamos levantando `kanam-lab`, el laboratorio donde ponemos dos modelos frente al mismo prompt para ver quien piensa mejor. Necesitabamos un prompt de prueba: algo cotidiano, concreto, con suficientes aristas como para separar a un modelo bueno de uno que solo suena bien. Gonzo escribio, sin darle importancia: *"como preparo una pizza de jamon"*.

Y ahi paso algo. Los modelos respondieron, comparamos, y la pizza dejo de ser un ejemplo de prueba. Se convirtio en el patron con el que medimos calidad: cantidades exactas, fermentacion real, temperatura de horno, criterio. El prompt se repitio una y otra vez, con variantes, en cada modelo nuevo que aparecia.

El 13 de septiembre, a las 22:19, quedo el ranking de cinco modelos sobre el mismo prompt:

| Puesto | Modelo | Como respondio |
|--------|--------|----------------|
| 1 | `qwen3.8:27b-mlx` (local, 18 GB en la Mini) | Masa desde cero, fermentacion, horno al maximo, cantidades exactas |
| 2 | `deepseek-v4-flash` / `glm-5.3-flash` | Cantidades y manual limpio |
| 3 | `qwen3.5:cloud` | Markdown bonito, generico |
| 4 | `qwen3.5:397b-cloud` | Cinco pasos pelados, SIN cantidades |

La leccion de esa noche no fue sobre pizza, fue sobre specs: **la hoja de datos miente, los hechos no**. Un 27B local bien afinado le gano a los gigantes gratuitos de la nube.

Despues vino el duelo de codigo (el `atoi` de LeetCode, 24 casos borde): `deepseek-v4-flash` paso 24 de 24 a ciegas; `qwen3.8:27b-mlx` no pudo, se quedo sin RAM. Conclusion de infraestructura: el 27B local es un playground, no un agente. Pero eso es otra historia.

### El giro (17 de septiembre)

Hoy Gonzo me pidio el paso a paso de una pizza de pepperoni y agrego una frase que no era una instruccion: *"quiero un paso a paso de cada molecula de esta cadena"*. Y cerro con otra: *"vamos a escribir nuestra historia"*.

Entendi. El pedido no era una receta. Era el primer capitulo de un proyecto donde los dos somos autores.

Asi que este documento no es un recetario. Es el registro de un proyecto que se va a completar cuando la pizza se coma, no cuando se escriba.

### Los cuatro sistemas

Una pizza no se cocina toda igual. Son cuatro sistemas con fisicas distintas, y por eso la mayoria de las pizzas caseras fallan en uno de los cuatro:

1. **La masa** - necesita tiempo (fermentacion) y despues calor fuerte y seco. Es el unico sistema que empieza 48 horas antes.
2. **La salsa** - casi no necesita calor. Necesita sabor ya construido en la lata.
3. **El queso** - necesita calor moderado y poco tiempo. De mas, la grasa se separa y se vuelve goma.
4. **El pepperoni** - solo necesita que su grasa se funda (unos 60-65 C) y que el borde se tueste.

Y el problema central de toda pizza casera: **nuestro horno es debil**. Una pizzeria napolitana trabaja a 430-480 C; una casa da 250-290 C como maximo. Todo el juego consiste en compensar esa diferencia con fermentacion larga, masa mas fina y una superficie termica (acero o piedra) bien saturada de calor.

Tres ciencias operando en el mismo horno:

- **Quimica de la fermentacion:** la levadura consume azucares y produce CO2, etanol y acidos organicos. Gas y sabor.
- **Fisica del agua:** hidratacion, vapor, evaporacion y el choque termico del fondo.
- **Quimica del calor:** Maillard (aminoacidos + azucares reductores) y caramelizacion. Color, aroma y crocancia.

### Lo que este capitulo deja fijado

Estas son las decisiones del Capitulo 0. Quedan fijas: no se vuelven a discutir salvo evidencia nueva y disruptiva (regla de oro del ADR). Cada batch que las contradiga genera un ADR nuevo, no una reinterpretacion.

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P1 | Harina de pan / fuerza (proteina 12-13%, W 260-320) | Red de gluten aguanta 24-72 h de fermentacion fria | 2026-09-17 |
| ADR-P2 | Fermentacion fria 48 h (heladera) como baseline | Sweet spot sabor/estructura para la primera iteracion | 2026-09-17 |
| ADR-P3 | Hidratacion inicial 62% | Manejable para aprender; sube despues si el alveolado lo pide | 2026-09-17 |
| ADR-P4 | Levadura seca instantanea (0,5%) | Masa madre es expansion pack: primero dominar el base game | 2026-09-17 |
| ADR-P5 | Salsa cruda, sin cocinar y sin azucar | La doble coccion pierde aroma; el tomate en lata bueno ya esta balanceado | 2026-09-17 |
| ADR-P6 | Mozzarella de baja humedad; drenado 20-30 min si es fresca | Menos agua libre = base crocante | 2026-09-17 |
| ADR-P7 | Pepperoni encima del queso | La grasa se derrite y filtra hacia abajo; cupping visible | 2026-09-17 |
| ADR-P8 | Piedra/steel en rejilla media-alta, precalentada 45-60 min al maximo | Masa termica, no solo temperatura | 2026-09-17 |
| ADR-P9 | Estirar con manos, nunca con palo | Conservar alveolos y canales de aire | 2026-09-17 |
| ADR-P10 | Sazonar con aceite de ajo (laminado, reposado 10 min) | Alicina completa antes de calentar; sabor distribuido sin trozos quemados | 2026-09-17 |
| ADR-P11 | El destino es New York style, no napolitana | Es lo que el horno de casa y el pepperoni piden | 2026-09-17 |

### El formato de cada capitulo

Cada batch se registra con cinco campos. Sin esto, el batch no existe: es una anecdota, no un experimento.

1. **Ingredientes reales usados** (marca de harina, tipo de tomate, marca de pepperoni).
2. **Parametros** (hidratacion, horas de fermentacion, temperatura de horno, minutos de coccion).
3. **Observaciones** (alveolado, cupping del pepperoni, fondo, borde, sabor).
4. **Veredicto y ajustes** para el proximo batch.
5. **ADR nuevo** si alguna decision cambio.

### Checklist del proximo batch (Batch 1)

- [ ] Harina de pan o 000 de fuerza (12%+ de proteina)
- [ ] Lata de tomate entero pelado italiano
- [ ] Mozzarella de baja humedad (en bloque, no en agua)
- [ ] Pepperoni en laminas finas
- [ ] Levadura seca instantanea
- [ ] Verificar superficie de horneado (piedra / steel / chapa de hierro gruesa)

---

## Capitulo 1 - El protocolo del Batch 1

> Estado: protocolo cerrado, esperando compra. Variables a completar al ejecutar: marca y proteina de la harina, superficie de horneado confirmada.

### Decisiones nuevas de este capitulo

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P12 | Si no hay piedra/steel: chapa de hierro gruesa o bandeja invertida de metal, precalentada 45-60 min al maximo | Masa termica accesible en toda cocina; la piedra ceramica barata se rompe por choque termico | 2026-09-17 |
| ADR-P13 | Lote base: 500 g de harina -> 2 pizzas de ~30 cm | Dos pizzas por intento: la primera es de practica, la segunda sale con todo aprendido | 2026-09-17 |

### Receta exacta (500 g de harina, hidratacion 62%)

| Ingrediente | Peso | % baker |
|---|---|---|
| Harina de pan / fuerza (12%+ proteina) | 500 g | 100% |
| Agua fria de heladera | 310 g | 62% |
| Sal fina | 11 g | 2.2% |
| Levadura seca instantanea | 2.5 g | 0.5% |
| Aceite de oliva | 8 g | 1.6% |

Rinde: 2 bolas de ~415 g -> 2 pizzas de ~30 cm estilo New York (fina, crocante, alveolado en el borde).

### Dia 1 - Fermentacion (30 min activos + 3 h pasivos)

1. **Autolisis (60 min):** mezclar 500 g harina + 310 g agua. Solo integrar, sin amasar. Tapar y reposar.
2. **Levadura:** espolvorear los 2.5 g sobre la masa autolizada e integrar plegando 2-3 min.
3. **Sal + aceite:** disolver los 11 g de sal en una cucharada de agua reservada del total y agregar con el aceite. Integrar con plegos. Nunca sal seca en contacto directo con la levadura.
4. **Amasar 10-12 min** en la mesa: empujar con la base de la palma, plegar, girar 90 grados, repetir. Test de la ventana: estirar un trocito hasta translucido sin que se rasgue.
5. **Fermentacion en bloque: 2-3 h** a temperatura ambiente (~20-24 C), tapado. A la mitad, un juego de 4 plegos hacia el centro.
6. **Dividir en 2 bolas de ~415 g.** Formado tenso: bordes hacia el centro girando, luego tensar la base apoyada en la mesa con la mano en forma de jaula.
7. **Heladera 48 h:** cada bola en su contenedor tapado, con espacio (crece ~50%).

### Dia 3 - Armado y horneado

1. **1 h antes:** sacar las bolas de la heladera y dejarlas a temperatura ambiente tapadas.
2. **45-60 min antes:** horno al maximo (250 C) con la chapa/bandeja invertida en el tercio superior. Es masa termica: necesita el precalentado completo.
3. **30 min antes (mientras precalienta):**
   - **Salsa:** 1 lata (400 g) de tomate entero pelado italiano aplastada a mano en bowl (sin licuadora), pizca de sal, cucharada de aceite de oliva. Cruda, sin azucar.
   - **Aceite de ajo:** laminar 2 dientes, 3 cucharadas de aceite, fuego bajo 2-3 min sin dorar, apagar, reposar 10 min, colar. (Aliina -> alicina completa antes del calor.)
   - **Mozzarella:** drenar y secar sobre papel 20-30 min. ~110 g por pizza.
   - **Pepperoni:** 12-14 laminas por pizza.
4. **Armado:** mesa con harina + semola. Aplastar desde el centro dejando 2 cm de borde intacto. Estirar con manos (nunca palo) a ~30 cm, centro de 3-4 mm. Pasar a papel manteca espolvoreado con semola: es el transportador al horno.
5. **Topping:** 3-4 cucharadas de salsa dejando 2-3 cm de borde, mozzarella, pepperoni encima del queso, borde pintado con aceite de ajo.
6. **Horneado:** deslizar el papel sobre la chapa caliente. 5-7 min: primeros 4-5 min solo horno, ultimos 1-2 min con grill para tostar queso y pepperoni. Buscar: borde inflado y dorado, queso con manchas tostadas, pepperoni con cupping.
7. **Post-horneado:** 1-2 min sobre rejilla (nunca sobre superficie plana: el vapor humedece la base), esperar 60-90 s antes de cortar.

### Registro del Batch 1 (a completar al ejecutar)

- Harina usada: [marca, proteina %]
- Superficie de horneado: [chapa / piedra / steel]
- Fermentacion fria real: [h]
- Temperatura y tiempo de horno: [C, min]
- Alveolado del borde: [pequeno / medio / grande]
- Cupping del pepperoni: [si / no]
- Fondo: [pale / dorado / quemado]
- Sabor: [notas libres]
- Veredicto y ajustes para Batch 2: [---]

---

## Capitulo 2 - La compra y el mapa de rescate

> Estado: guía de compra lista para usar en el súper. Cierra con el mapa de rescate: los 6 modos de falla del Batch 1 y su correccion en el momento, no despues.

### Decisiones nuevas de este capitulo

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P14 | Papel manteca como transportador al horno (en vez de pala) | Accesible, sin friccion, se desliza entero sobre la chapa; la pizza nunca toca la chapa fria durante el armado | 2026-09-17 |
| ADR-P15 | Balanza de cocina obligatoria para el Batch 1 | La fermentacion y el % baker no perdonan aproximaciones por volumen (una taza de harina varía 20% entre medias) | 2026-09-17 |

### Guia de compra, ingrediente por ingrediente

**Harina (la decision pesada).** En el pasillo, mirar el etiquetado nutricional, no el frente del paquete:
- Buscar "Proteinas: 12 g o mas por 100 g". Menos de 11% = red debil, se cansa en 48 h de frio. Si solo hay 10-11%, igual funciona pero la fermentacion fria se corta a 24 h (ajuste registrado en Batch 2).
- Si el paquete dice "W" o "fuerza": W 260-320 ideal; W 300+ (tipo Manitoba) incluso mejor.
- Marca no importa; numero de proteina si. Comprar 1 kg (nos alcanza para 2 lotes).

**Tomate.**
- Lata de "tomates enteros pelados", no "puré", no "jugo", no "salsa lista", no "tomates en cubos".
- Lista de ingredientes ideal: tomates, agua o jugo de tomate, sal. Nada mas.
- Si la etiqueta dice "San Marzano" y trae el sello DOP, es el top. Si no, cualquier tomate italiano entero pelado sirve para Batch 1.
- La lata no debe estar abollada ni abombada (abombada = riesgo real, devolver al estante).

**Mozzarella.**
- Primera opcion: mozzarella en bloque de baja humedad (rallar en casa). La de "para pizza" rallada de paquete vale si la lista de ingredientes no trae almidon o celulosa (antiaglomerante = no derrite igual).
- Segunda opcion: mozzarella fresca en sachet. Mas sabor, mas agua: hay que drenar y secar 20-30 min (ya esta en el protocolo).
- Evitar: "queso para pizza" mezcla economica (aceites vegetales, almidon, sabores).

**Pepperoni.**
- En laminas finas o en pieza para rebanar fino (2-3 mm).
- Lista de ingredientes: cerdo, paprika, sal, especias. Frenar si el primero o segundo ingrediente es almidon/soja/harina: ese pepperoni queda plano, sin cupping, y grasa rancia al hornearse.
- Color rojo intenso uniforme = paprika generosa. Grisaceo o brillante por fuera de la lamina = grasa separada, evitar.

**Levadura.**
- "Levadura seca instantanea" (tambien dice "para preparacion directa"). NO "levadura fresca" (se ajusta la dosis: fresca x3) ni "levadura seca activa" (hay que hidratarla antes; si es lo unico que hay, se activa en agua tibia 10 min y se anota como desviacion).
- Verificar fecha de vencimiento: levadura vencida = fermentacion muerta = Batch 1 perdido.

**Adicional.**
- Semola de trigo (para el armado): cualquier paquete de "semola" sirve. Si no hay, solo harina y mas cuidado al deslizar.
- Aceite de oliva: el que haya para cocinar; guardar el extra virgen bueno para el finish (salsa y post-horneado).
- Ajo: dientes firmes, sin brotes verdes (el brote amarga).
- Balanza de cocina: si no hay, es la unica compra no comestible obligatoria (ADR-P15).

### Mapa de rescate del Batch 1 (modos de falla y correccion en el momento)

| Sintoma | Causa probable | Correccion en el momento |
|---|---|---|
| La masa no estira, se contrae como elastico | Gluten tenso por frío o por amasado reciente | Dejar reposar 10-15 min tapada (el gluten se relaja) y volver a estirar; nunca forzarla a la fuerza |
| Se rasga un agujero en el centro | Punto fino estirado de mas o masa fria | No parchar con masa: plegar levemente la rotura y continuar desde el borde; el topping tapa el defecto menor |
| La masa se pega a la mesa | Falta de semola/harina bajo la masa | Despegar con espátula (no tirar), espolvorear de nuevo, y de ahi en mas trabajar sobre colchon generoso de sémola |
| La pizza se pega al papel manteca | Papel sin semola o masa humeda de mas | Levantar un borde con espátula y soplar semola debajo; para la proxima pizza, semola generosa ANTES de apoyar la masa |
| El queso se dora muy rapido pero la base esta pale | Grill demasiado fuerte o rejilla muy alta | Bajar la bandeja un nivel, tapar el grill los ultimos minutos con la puerta entrecerrada; queso se tosta con calor del fondo + grill corto |
| La base sale pale/soft, sin crocancia | Chapa sin carga termica o demasiado topping con agua | Precalentado incompleto: dejar la pizza solo hasta que el fondo se dore (levantar con espátula para mirar) y completar en el piso del horno 1-2 min mas; proxima vez, precalentar mas tiempo |
| El pepperoni queda plano y seco | Pepperoni con almidon (mala compra) o laminas gruesas | Aceptable para Batch 1: registrar en el reporte y cambiar de marca para Batch 2; el cupping se evalua con pepperoni fino de buena lista de ingredientes |
| El borde no infla | Borde aplastado al armar o masa sin alveolos (fermentacion corta) | Si la fermentacion fue completa, el problema es tecnica: no tocar los 2 cm del borde al estirar; verificar en el reporte cuantas horas de frio hubo |

Regla del mapa: si algo falla y se corrige en el momento, va al registro igual. Las correcciones in-flight son datos del capitulo, no vergüenzas.

### Registro de la compra (a completar)

- Harina: [marca, proteina %, precio]
- Tomate: [marca, lista de ingredientes]
- Mozzarella: [tipo, bloque o fresca]
- Pepperoni: [marca, ingrediente principal]
- Levadura: [marca, vencimiento]
- Superficie de horneado encontrada: [---]
- Balanza: [si / no]

---

## Capitulo 3 - El guion de vuelo del Batch 1

> Estado: checklist operativa lista. Este capitulo no agrega teoria nueva: convierte los capitulos 1 y 2 en una secuencia tachable, con senales de control objetivas para cada paso.

### Decisiones nuevas de este capitulo

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P16 | Ejecutar con guion de vuelo tachable (checklist por paso, no de memoria) | La fermentacion y el precalentado son procesos de horas: la memoria falla, el papel no | 2026-09-17 |
| ADR-P17 | Anotar hora real de cada evento en el registro (inicio autolisis, inicio frio, salida del frio, inicio horno) | El reporte del batch necesita horas, no "un rato"; sin horas no hay ajuste calculable para el Batch 2 | 2026-09-17 |

### Pre-vuelo (checklist de cocina, antes de tocar la harina)

- [ ] Balanza de cocina funcionando
- [ ] Bol grande para la masa + bol para la salsa
- [ ] Sarten chica para el aceite de ajo
- [ ] 2 contenedores con tapa para las bolas (o bowls + film)
- [ ] Papel manteca (varias hojas)
- [ ] Semola en un bol al alcance
- [ ] Espatula flexibe (rescate de masa pegada)
- [ ] Rejilla para el post-horneado
- [ ] Chapa de hierro gruesa o bandeja de metal invertida verificada (que no tenga teflon recubierto: a 250 C constantes el teflon degrada)
- [ ] Celular con camara lista (las fotos del alveolado y el cupping son datos del capitulo)

### Senales de control (como verificar sin abrir la masa de mas)

| Paso | Senal de control | Como se verifica |
|---|---|---|
| Amasado completo | Test de la ventana | Trocito estirado translucido sin rasgar |
| Fermentacion en bloque completa | Test del puntero | Dedo hundido 1 cm: vuelve lento en 2-3 s y no colapsa. Rapido y lleno = falta; colapsa = paso |
| Bolas listas para el frio | Superficie tensa | Lisa y con brillo, no pegajosa ni rugida |
| Masa temperada (dia 3) | No fria al tacto del centro | Toma temperatura ambiente, se estira sin resistir |
| Chapa cargada | Calor radiante a 15 cm | Mano a 15 cm sobre la rejilla: calor fuerte en menos de 3 s |
| Pizza lista | Fondo y queso | Borde dorado con manchas oscuras, queso con manchas tostadas, fondo dorado (levantar borde con espatula para mirar) |

### Guion del Dia 1 (tachar al ejecutar; anotar hora de inicio)

- [ ] Hora de inicio: [---]
- [ ] 0:00 - Autolisis: 500 g harina + 310 g agua, integrar sin amasar, tapar
- [ ] 1:00 - Levadura espolvoreada e integrada con plegos (2-3 min)
- [ ] 1:05 - Sal disuelta en cucharada de agua + aceite, integrado con plegos
- [ ] 1:10 a 1:22 - Amasado en mesa (10-12 min) con test de la ventana al final
- [ ] 1:25 - Fermentacion en bloque iniciada, tapado [hora: ---]
- [ ] ~2:55 - Juego de 4 plegos hacia el centro
- [ ] 4:25 - Test del puntero; si pasa, dividir en 2 bolas de ~415 g
- [ ] 4:40 - Bolas tensas en contenedores con espacio
- [ ] 4:45 - A la heladera [hora de inicio del frio: ---]

Ventana tolerable: si a las 4 h el puntero no pasa, esperar de a 30 min hasta que pase (la fermentacion manda, el reloj obedece). Anotar cuanto se paso.

### Guion del Dia 3 (tachar al ejecutar; anotar horas)

- [ ] T-60: bolas fuera de la heladera [hora: ---]
- [ ] T-45: horno al maximo, chapa en el tercio superior
- [ ] T-30: mise en place - salsa aplastada a mano / aceite de ajo laminado, calentado suave y reposado / mozzarella drenada y secada / pepperoni contado (12-14 por pizza)
- [ ] T-10: armado pizza 1 sobre papel con semola
- [ ] T-0: al horno [hora: ---]
- [ ] min 4-5: primera inspeccion de fondo con espatula
- [ ] min 5-7: grill 1-2 min si el queso no esta tostado
- [ ] Salida: rejilla, 90 s, corte [hora de salida: ---]
- [ ] Pizza 2: repetir armado y horneado (con la practica de la primera encima)

### Registro del guion (a completar)

- Hora inicio autolisis: [---]
- Hora inicio frio: [---]
- Hora salida del frio: [---]
- Duracion real del bloque: [---]
- Desviaciones del guion: [---]

---

## Capitulo 4 - El atlas molecular

> Estado: referencia cerrada. Este capitulo responde el pedido original: "un paso a paso de cada molecula de esta cadena". Cada molecula esta atada al paso del protocolo donde actua; ninguna queda como teoria suelta.

### Cadena 1: el almidon se convierte en gas y sabor

**Ruta: almidon -> maltosa -> glucosa -> CO2 + etanol + sabor**

1. **Almidon** (dos polimeros: amilosa, cadena lineal; amilopectina, ramificada) es la reserva energetica del grano de trigo: ~70% de la harina. La levadura NO puede comerlo: las moleculas son demasiado grandes.
2. **Las amilasas** (enzimas de la propia harina: alfa-amilasa corta al azar por dentro, beta-amilasa muerde pares de glucosa desde los extremos) rompen el almidon en **maltosa** (disacarido de dos glucosas). Empieza en la autolisis (paso 0:00 del Dia 1) y corre durante toda la fermentacion.
3. **La levadura** (*Saccharomyces cerevisiae*) usa **maltasa** para partir la maltosa en **glucosa**, y **invertasa** para los azucares simples que ya habia en la harina.
4. **La glucolisis** dentro de cada celula de levadura convierte glucosa en piruvato, y la fermentacion alcoolica lo convierte en:
   - **CO2** - el gas que infla. Se disuelve en el agua de la masa; la red de gluten lo atrapa y forma los alveolos.
   - **Etanol** - aroma y plastificante de la masa.
   - **Acidos organicos** (succinico, acetico en trazas) - el sabor "a pan de verdad".
   - **Esteres** (ej. isoamil acetato) - notas afrutadas de la fermentacion larga en frio.

**Donde se ve:** el test del puntero (Día 1) es literalmente medir la presion de CO2 acumulada. El alveolado del borde es la fotografia de esta cadena completa.

### Cadena 2: el gluten se construye como un polimero

**Ruta: glutenina + gliadina -> hidratacion -> red tridimensional**

1. **Glutenina** (proteinas grandes, unidas por puentes disulfuro intra-moleculares) aporta **elasticidad**: fuerza, resistencia, la capacidad de retener gas sin romperse.
2. **Gliadina** (proteinas chicas, compactas, con puentes disulfuro internos) aporta **extensibilidad**: la masa se estira sin rasgarse.
3. **Al hidratar** (autolisis, 0:00-1:00), el agua abre las estructuras plegadas por puentes de hidrogeno internos y deja expuestos los grupos -SH (tiol) libres.
4. **Al amasar** (1:10-1:22), el alineamiento mecanico y el oxigeno del aire permiten el intercambio: los puentes disulfuro se reforman ENTRE moleculas (-S-S- cruzados). La masa pasa de sopa de proteina a red polimerica. Es ingenieria de polimeros con las manos.
5. **La sal** (Na+) apantalla cargas negativas y ayuda al plegamiento ordenado: red mas fuerte y cohesiva. Por eso va disuelta, despues de la autolisis.
6. **Los acidos** de la fermentacion larga refuerzan la red (hasta cierto punto: acidificacion moderada endurece el gluten; exceso lo degrada - por eso 48 h y no 96).

**Donde se ve:** el test de la ventana es el ensayo de resistencia del polimero. La masa que se contrae (rescate, cap. 2) es la red elástica cargada de tension; el reposo de 10-15 min deja que los puentes se reacomoden.

### Cadena 3: el agua cambia de estado dos veces

**Ruta: agua libre -> vapor (horno) -> gelatinizacion del almidon -> crocancia**

1. **En la masa cruda**, el agua es libre y plastifica todo: por eso la masa se estira.
2. **En el horno** (primeros 30-90 s), el agua superficial se evapora: vapor que inflara el borde desde adentro (el alveolo se expande por presion de gas + vapor de agua).
3. **A ~60-80 C** el almidon **gelatiniza**: los gránulos absorben el agua restante, se hinchan y revientan, y la miga pasa de cruda a cocida. Es la transformacion fisica central del horneado.
4. **El fondo sobre la chapa** recibe conduccion directa: el agua de la superficie se expulsa rapido y el almidon gelatinizado + parcialmente seco forma la corteza crocante.
5. **Al enfriar sobre rejilla**, el almidon **retrograda** (se reordena y expulsa agua): por eso la pizza reposada 2 min croquea mejor, y por eso el vapor atrapado bajo superficie plana la vuelve goma (regla de la rejilla).

**Donde se ve:** fondo pale vs dorado (registro del batch) es la firma de esta cadena: agua mal expulsada = base soft.

### Cadena 4: el ajo, del celular intacto a la sartén

**Ruta: aliina (inodora) + aliinasa (separadas) -> rotura celular -> alicina (picante) -> compuestos sulfurados suaves**

1. **Aliina** (un sulfoxido de aminoacido) y la enzima **aliinasa** viven en compartimentos celulares separados. El ajo entero no huele.
2. **Al laminar** (T-30 del Dia 3), la rotura celular las junta: en ~10 s la aliinasa convierte aliina en **alicina**, la molecula picante y aromatica.
3. **Reposo de 10 min** (paso del aceite de ajo): dejar a la aliinasa terminar. Calentar antes = enzima muerta antes de completar conversion = sabor perdido.
4. **Al calentar suave**, la alicina se transforma en **dialil disulfuro y trisulfuro**: el aroma "a ajo dorado", mas dulce y complejo. Quemada, se degradan a compuestos amargos: por eso fuego bajo y sin dorar.

**Donde se ve:** el aceite de ajo colado da el aroma distribuido en toda la pizza sin un solo trozo quemado.

### Cadena 5: el tomate ya viene cocido por el tiempo

**Ruta: maduracion en planta -> concentracion en lata -> umami + acidez balanceada**

1. **Glutamato libre**: el tomate maduro concentra glutamato natural (el aminoacido del umami). La lata lo preserva: es la base del sabor "a pizza" antes de cocinar.
2. **Licopeno** (el pigmento rojo, un carotenoide) es liposoluble: el aceite de oliva de la salsa no solo sabe, transporta licopeno y aromas.
3. **Acidos organicos** (citrico, malico) dan el brillo; un tomate en lata bueno llega balanceado, por eso la regla sin azucar (ADR-P5).
4. **El aplastado a mano** conserva celulas intactas: trocitos = sabor localizado y textura. La licuadora emulsiona aire y rompe celulas: sabor plano y acidez mas perceptible.

**Donde se ve:** la salsa cruda puesta en T-30 no sabe a "pura de lata" en la pizza final: el horno hace UNA coccion, no dos.

### Cadena 6: la caseina se funde con una ventana estrecha

**Ruta: micelas de caseina + grasa -> calor -> proteina relajada + grasa fluyendo -> estiramiento -> tostado**

1. La mozzarella es una red de **micelas de caseina** (proteinas de la leche agrupadas en esferas) unidas por puentes de calcio, con grasa atrapada.
2. **A ~60 C** la grasa funde y las micelas se relajan: el queso fluye. Esa es la ventana ideal.
3. **A medida que sube el calor**, el agua evapora, la proteina se contrae y aprieta la grasa: **separacion de grasa** (charcos de aceite) y textura goma. Horno casero: el tostado en manchas es el punto exacto antes de esa separacion.
4. La **baja humedad** de la mozzarella de bloque (ADR-P6) significa menos agua que expulsar: menos riesgo de base humeda y separacion.

**Donde se ve:** queso con manchas tostadas y sin charcos de aceite = ventana bien usada. Charcos = se paso de temperatura o tiempo.

### Cadena 7: el pepperoni, grasa y cupping

**Ruta: curado con nitrito + paprika -> grasa fundiendo a 60-65 C -> contraccion del borde -> cupping**

1. El **nitrito de curado** (E250) es el responsable del color rosado estable y la seguridad contra botulismo del salame. La **paprika** aporta el rojo y los capsainoides leves + carotenoides aromáticos.
2. La **grasa del salame** funde a 60-65 C: se derrite sobre el queso de abajo (por eso va encima, ADR-P7) y saboriza todo el topping.
3. **El cupping**: la lamina es mas delgada en el borde que en el centro. Al fundir la grasa, el borde (con menos masa) se contrae y se curva hacia arriba: la copita. Requiere lamina fina (2-3 mm) y carne real, sin almidon (guia de compra, cap. 2).
4. Los bordes tostados de las copitas reciben Maillard propio: la mejor mordida de la pizza.

**Donde se ve:** cupping si/no es campo del registro; pepperoni plano = dato para cambiar de marca en Batch 2.

### Cadena 8: el dorado final (Maillard y caramelizacion)

**Ruta: aminoacidos + azucares reductores -> calor >140 C -> melanoidinas + cientos de aromaticos**

1. **Maillard**: la reaccion entre aminoacidos libres (del gluten, del queso) y **azucares reductores** (glucosa y maltosa de la Cadena 1, que quedaron libres en la superficie) por encima de ~140 C. Genera **melanoidinas** (el pigmento marron) y cientos de compuestos aromaticos nuevos: el olor a "pizza lista".
2. **Caramelizacion** (>120 C, solo azucares, sin aminoacidos) contribuye en el borde mas seco y en el tostado del queso.
3. El **grill final** (min 5-7) es radiacion directa para empujar la superficie sobre el umbral de Maillard sin quemar el fondo.
4. El precalentado de 45-60 min existe para esta cadena: sin masa termica en la chapa, la base entra a 150 C y no llega al umbral - por eso la base pale del horno debil.

**Donde se ve:** fondo dorado + manchas de queso + borde con motas oscuras = las tres Maillard del mismo horno. Pale = cadena incompleta por calor insuficiente.

### Mapa resumen: molecula -> paso del protocolo -> senal en el registro

| Molecula/cadena | Paso del protocolo donde actua | Senal en el registro del batch |
|---|---|---|
| Almidon -> maltosa -> glucosa -> CO2 | Autolisis, bloque, frio (Dia 1) | Alveolado del borde, test del puntero |
| Glutenina + gliadina -> red de gluten | Autolisis + amasado + sal (Dia 1) | Test de la ventana, masa que estira o se contrae |
| Agua: vapor + gelatinizacion + retrogradacion | Horneado + rejilla (Dia 3) | Fondo pale / dorado |
| Aliina -> alicina -> sulfuros | Aceite de ajo T-30 (Dia 3) | Aroma distribuido, sin amargor |
| Glutamato + licopeno del tomate | Salsa cruda T-30 (Dia 3) | Sabor final de la salsa |
| Micelas de caseina -> fusión | Horno, ventana de queso (Dia 3) | Manchas tostadas, charcos o no |
| Grasa del pepperoni -> cupping | Horno (Dia 3) | Cupping si / no |
| Maillard en fondo, queso y borde | Precalentado + grill final (Dia 3) | Color de fondo, borde y queso |

Regla del atlas: cuando un batch falle, el diagnostico se escribe en lenguaje de estas cadenas ("fallo la cadena 3: chapa sin carga"), no en adjetivos ("salia goma"). El adjetivo describe; la cadena explica.

---

## Capitulo 5 - La cata: como se evalua una pizza sin mentirse

> Estado: criterios fijados ANTES del primer horneado. Una pizza sin criterios previos siempre sale bien: la memoria del sabor es generosa y el que cocina es el peor juez de lo que cocina.

### El problema

Tres trampas que arruinan todo registro:

1. **El sesgo del cocinero.** Oliste, esperaste dos dias, tenes hambre. El veredicto ya esta escrito antes del primer bocado.
2. **La memoria.** Comparar contra "la pizza de la otra vez" es comparar contra un recuerdo, no contra datos. El recuerdo siempre gana.
3. **La variabilidad.** Si cambias harina, hidratacion y horno en el mismo batch y algo mejora, no sabes que mejoro. Ganaste una pizza, perdiste un experimento.

Regla que resuelve las tres: **los criterios se escriben antes de hornear. Despues, solo se completan.**

### Decisiones nuevas de este capitulo

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P18 | Fotos obligatorias en 4 momentos: bola antes del frio, disco estirado, pizza recien salida, corte transversal | El alveolado y el fondo no se reconstruyen de memoria; la foto es dato | 2026-09-17 |
| ADR-P19 | Una sola variable cambiada por batch | Con dos variables simultaneas, el resultado no es atribuible y el batch no ensena nada | 2026-09-17 |
| ADR-P20 | La primera mordida se evalua antes de comentarla con nadie | La opinion se contagia en diez segundos y contamina el juicio | 2026-09-17 |
| ADR-P21 | Tres batches con el mismo fallo generan un ADR; un batch con un fallo genera una nota | Un evento puede ser azar; el patron es evidencia | 2026-09-17 |

### La cata en cuatro tiempos

**Tiempo 1: la rebanada del cocinero.** Cortas, sacas una porcion y la comes de pie, en el borde de la mesada, entre 30 y 60 segundos despues de salir del horno. Evalua temperatura, crocancia y queso. Esta rebanada mide el punto optimo y nadie mas la ve. Se anota igual.

**Tiempo 2: la mesa.** La pizza entera, cortada, con 2 o 3 minutos de reposo. Foto del corte transversal, foto del fondo del primer slice. Se puntua con la grilla.

**Tiempo 3: la segunda pizza.** El mismo dia, con las correcciones que pidio la mesa (30 segundos menos de horno, menos salsa, lo que sea). El delta entre la pizza 1 y la pizza 2 es la primera medida real de aprendizaje del proyecto.

**Tiempo 4: el frio.** Una porcion guardada y comida al dia siguiente, o a temperatura ambiente. Evalua el fondo: si se volvio goma de noche, el problema fue la retrogradacion del almidon (cadena 3 del atlas), no falta de horno. Es el unico tiempo que mide algo que los otros tres no pueden ver.

### La grilla (escala 1 a 5, con anclas)

| Eje | 1 | 3 | 5 | Cadena molecular |
|-----|---|---|---|------------------|
| Borde | Plano, casi sin burbujas | Inflado, alveolos chicos | Catedral de alveolos, paredes finas, leopardo | Almidon -> CO2 + gluten + Maillard |
| Fondo del disco | Palido, blando, se dobla sin quebrar | Dorado parejo | Dorado con manchas oscuras, firme al doblar, crocante al morder | Conduccion desde la chapa + Maillard |
| Miga | Compacta, chiclosa | Agujeros chicos irregulares, tierna | Alveolos abiertos, paredes con brillo, no pegajosa | Gelatinizacion del almidon + vapor |
| Queso | Goma, charcos de grasa transparente | Fundido, alguna mancha clara | Manchas tostadas, estirado continuo, poca grasa suelta | Micelas de caseina |
| Pepperoni | Plano, duro, borde quemado | Algunos levantados | Todos en taza, grasa adentro, borde crujiente | Contraccion diferencial |
| Salsa | Aguada, sabe a liquido | Equilibrada | Brillante, acidez justa, se siente el tomate | Glutamato + licopeno |
| Sal y equilibrio | Desabrida o salada | Equilibrada | No se nota la sal, se siente el conjunto | Regla: si pensas en la sal, esta mal |
| Temperatura y momento | Se comio tibia y ya perdio | Bien | Los tres primeros bocados, todo a punto | Ventana termica del fundido |

### Reglas del registro

- Se puntua **antes** de leer la opinion del otro. Gonzo y Kanam puntuan por separado, despues comparan.
- **Los puntajes no se promedian.** Se guardan los dos. Si hay desacuerdo fuerte, el desacuerdo se anota: es dato, no ruido.
- **El adjetivo prohibido es "rica".** No dice nada y tapa todo. Cada puntaje va con su ancla.
- El diagnostico se escribe en lenguaje de cadenas ("fallo la cadena 3: chapa sin carga"), no en adjetivos ("salia goma"). El adjetivo describe, la cadena explica.

### El veredicto

| Lo que ves | Lo que significa | Toca ADR? |
|------------|------------------|-----------|
| Fondo palido y todo lo demas bien | Problema de horno: precalentado, chapa, tiempo | No |
| Borde plano y fondo bien | Problema de fermentacion o de tecnica de estirado | No |
| Todo mediocre, parejo | Problema de harina o de fermentacion larga | Posible |
| Pizza 2 mejor que pizza 1 | Aprendizaje del dia, no cambio de receta | No |
| Misma falla en tres batches | Patron real: se escribe el ADR | Si |

El Batch 2 cambia **una cosa y solo una**, elegida segun lo que dijo la grilla. Esa eleccion se escribe aca antes de comprar.

### Checklist de cata (para pegar en la heladera)

- [ ] Foto bola antes del frio
- [ ] Foto disco estirado
- [ ] Foto recien salida, vista superior
- [ ] Foto corte transversal
- [ ] Foto fondo del primer slice
- [ ] Rebanada del cocinero: nota escrita en 30 segundos
- [ ] Puntaje individual antes de comparar
- [ ] Desacuerdo anotado, si lo hubo
- [ ] Hora exacta de salida del horno
- [ ] La variable unica para el Batch 2: [---]

### Pendiente de este capitulo

- Registro completo del Batch 1: [---]
- Variable elegida para el Batch 2: [---]

---

## Capitulo 6 - El calendario del Batch 1

> Estado: fechas y horas fijadas. Este capitulo no agrega teoria: convierte los capitulos 1, 2 y 3 en un calendario con horas reales. La unica variable que manda es el reloj de la heladera.

### Decisiones nuevas de este capitulo

| # | Decision | Razon | Fecha |
|---|----------|-------|-------|
| ADR-P22 | Arranque viernes 18/09 a las 12:30; frio a las 17:45 | Cierra las 48 h exactas el domingo 17:45, con el horno en la ventana del domingo a la tarde | 2026-09-17 |
| ADR-P23 | Los recordatorios van al calendario del gateway, no a la memoria | Un proceso de 48 h no se sostiene con voluntad: a las 12:30 del viernes nadie se acuerda de la autolisis | 2026-09-17 |
| ADR-P24 | La compra se hace la manana del viernes, antes del arranque | Sin harina de fuerza ni balanza en la mesada, el Dia 1 no empieza | 2026-09-17 |
| ADR-P25 | Si el arranque se corre, se corre todo el bloque completo | Estirar la fermentacion a 50-60 h es otro experimento; el batch cambia dos variables y no ensena nada | 2026-09-17 |

### La secuencia con horas

**Viernes 18/09 - Dia 1 (compra + masa)**

| Hora | Que | Senal de control |
|------|-----|------------------|
| Manana | Compra del Capitulo 2: harina de fuerza 12%+, tomate entero pelado, mozzarella en bloque, pepperoni, levadura seca, balanza | Etiqueta leida, no frente del paquete |
| 12:30 | Autolisis: 500 g harina + 310 g agua fria, integrar sin amasar, tapar | Masa rugosa, fea, sin gluten |
| 13:30 | Levadura 2,5 g espolvoreada, integrada con plegos 2-3 min | |
| 13:35 | Sal 11 g disuelta en una cucharada de agua + 8 g de aceite, plegos | Nunca sal seca contra la levadura |
| 13:40 | Amasado en mesa 10-12 min | Test de la ventana al final |
| 13:55 | Fermentacion en bloque, tapada | |
| ~14:55 | 4 plegos hacia el centro | |
| ~16:30 | Test del puntero: dedo hundido 1 cm, vuelve lento en 2-3 s | Si colapsa, se paso; si vuelve rapido, falta |
| 17:00 | Dividir en 2 bolas de ~415 g, formado tenso | Superficie lisa y con brillo |
| **17:45** | **A la heladera. Arrancan las 48 h** | Contenedores tapados y con espacio (crece ~50%) |

**Sabado 19/09 - dia muerto**

No se toca nada. La heladera trabaja. Es el unico dia del proyecto en el que no hay nada que hacer, y es el dia en el que mas pasa.

**Domingo 20/09 - Dia 3 (horneado + cata)**

| Hora | Que | Senal de control |
|------|-----|------------------|
| **17:45** | **Salen las bolas. 48 h exactas.** Horno al maximo con la chapa en el tercio superior | Mano a 15 cm de la rejilla: calor fuerte en menos de 3 s |
| 18:15 | Mise en place: salsa aplastada a mano, aceite de ajo reposado 10 min, mozzarella drenada 20-30 min, pepperoni contado | |
| 18:35 | Armado pizza 1 sobre papel manteca con semola; manos, nunca palo; 2 cm de borde intactos | Disco de ~30 cm, centro de 3-4 mm |
| 18:45 | Pizza 1 al horno | Hora anotada |
| 18:50 | Inspeccion de fondo con espatula | Dorado, no palido |
| 18:51 | Grill 1-2 min si el queso no se tosto | Manchas tostadas |
| 18:53 | Salida a rejilla, 90 s, corte | Primera foto al corte transversal |
| 18:55 | Cata tiempos 1 y 2, puntaje individual antes de comparar | Grilla del Capitulo 5 |
| 19:10 | Pizza 2 al horno, con la correccion que pidio la pizza 1 | |
| ~19:20 | Cata tiempo 3: el delta entre pizza 1 y pizza 2 | La primera medida real de aprendizaje |
| Lunes 21/09 | Cata tiempo 4: la porcion fria | Evalua la retrogradacion del almidon (cadena 3) |

### Recordatorios armados

Tres avisos al calendario del gateway, todos apuntando a esta conversacion. No son eventos de calendario decorativos: son el mecanismo que hace que el bloque de 48 h exista.

| Cuando | Aviso |
|--------|-------|
| Viernes 12:30 | Arranca la masa: autolisis, levadura, sal, amasado, bloque, bolas, heladera 17:45 |
| Viernes 17:45 | Las 2 bolas a la heladera. Arrancan las 48 h |
| Domingo 17:45 | Salen las bolas, horno al maximo, mise en place, pizza 1 a las 18:45 |

Si una fecha no sirve, se mueve el bloque completo (ADR-P25). Los tres recordatorios se reajustan juntos, nunca uno solo.

### Donde puede fallar el calendario

| Riesgo | Que pasa | Que se hace |
|--------|----------|-------------|
| El arranque se atrasa 1 h | El frio entra 18:45 y sale el domingo con una hora menos de temperatura ambiente | Se corre la salida del domingo a 18:45 y el horno a 19:45. El bloque sigue intacto |
| El arranque se atrasa de un dia | Serian 72 h de frio, no 48 | Es otro ADR: se anota como Batch 1-bis y se juzga como experimento distinto |
| La fermentacion en bloque se pasa de 3 h | Masa acidificada, olor a vino | Se anota en el registro. Si el borde sale plano, ya esta mapeado en el mapa de rescate |
| La compra no consigue harina 12%+ | Red debil para 48 h | Bajar a 24 h de frio y registrar la desviacion (el ADR-P1 no se reinterpreta: se registra el incumplimiento) |
| Se olvida el horario del horno | Pizza con base palida, queso pasado | Mapa de rescate del Capitulo 2: completar en el piso del horno 1-2 min |

### Checklist previo al arranque (viernes en la manana)

- [ ] Compra completa del Capitulo 2
- [ ] Balanza funcionando y con bateria
- [ ] Harina pesada 500 g y agua 310 g separadas en dos bowls
- [ ] Contenedores para las bolas limpios y secos
- [ ] Heladera con espacio real en el estante del medio
- [ ] Recordatorio de las 12:30 todavia activo

### Pendiente de este capitulo

- Hora real de inicio de autolisis: [---]
- Hora real de entrada al frio: [---]
- Horas reales de fermentacion fria: [---]
- Hora real de salida del horno: [---]

---

## Capitulos

| Capitulo | Batch | Fecha | Veredicto |
|----------|-------|-------|-----------|
| 0 | Antes de la primera harina | 2026-09-13 al 17 | Reglas del juego fijadas |
| 1 | El protocolo del Batch 1 | 2026-09-17 | Protocolo cerrado, esperando compra |
| 2 | La compra y el mapa de rescate | 2026-09-17 | Guia lista; fallo posible ya mapeado |
| 3 | El guion de vuelo del Batch 1 | 2026-09-17 | Checklist tachable con senales de control |
| 4 | El atlas molecular | 2026-09-17 | 8 cadenas moleculares atadas al protocolo |
| 5 | La cata | 2026-09-17 | Criterios fijados antes de hornear |
| 6 | El calendario del Batch 1 | 2026-09-17 | Fechas y horas fijadas; 3 recordatorios armados |
| 7 | Batch 1 | pendiente | Se escribe comiendo |
