# Clase: Harvard CS50's Artificial Intelligence with Python — Full University Course

- Fuente: https://www.youtube.com/watch?v=5NgNicANyqM
- Canal: freeCodeCamp.org
- Expositor: Brian Yu (Harvard University)
- Duración: 11:51:22
- Publicado: 2023-08-10
- Idioma: inglés (subtítulos manuales de YouTube, glosario de ASR en `transcripcion.md`)
- Recursos oficiales del curso: https://cs50.harvard.edu/ai/2020/
- Transcripción: `transcripcion.md` (2.616 bloques, 14.299 cues, 144.344 palabras)
- Capítulos: los 8 oficiales de la descripción, alineados 1:1 con los módulos

## Tesis de la clase

**La IA clásica es la disciplina de convertir un problema en una representación que una computadora pueda manipular.** El curso recorre siete familias de técnicas en ese orden exacto, y cada una existe porque la anterior tiene un techo: la búsqueda funciona cuando el estado es conocido y el objetivo es alcanzable; el conocimiento proposicional funciona cuando el mundo es cierto; la probabilidad entra cuando no lo es; la optimización entra cuando no hay una respuesta correcta sino un óptimo bajo restricciones; el aprendizaje entra cuando no podemos escribir las reglas a mano; las redes neuronales entran cuando la función a aprender no tiene forma analítica; y el lenguaje entra cuando la tarea deja de ser clasificar y pasa a ser generar secuencia.

Es una clase universitaria real, no un tutorial: Brian Yu enseña con el pizarrón y con código, y cada módulo tiene un proyecto (degree, knights, tic-tac-toe, crossword, heredity, traffic, page rank, nim, shopping, crossword AI, six degrees, parser, questions, attention). Los proyectos **no son opcionales para aprovechar la clase**: son el punto donde la teoría se puede verificar.

La clase tiene una fecha clara (2020/2023) y sus ejemplos de lenguaje lo delatan: los n-gram y los modelos de Markov se explican antes de que los transformers fueran la norma. Lo que enseña sigue siendo el sustrato de todo lo que vino después, pero conviene leerlo como **fundamentos**, no como estado del arte de 2026.

## Resultado esperado

Al terminar la clase deberías poder:

1. Formular cualquier tarea como un **problema de búsqueda** (estado inicial, acciones, test de objetivo, costo) y elegir entre BFS, DFS, búsqueda voraz, A\* y búsqueda local según la estructura del espacio.
2. Demostrable: escribir un agente que resuelva un problema de camino en un grafo con A\* y una heurística admisible, y explicar por qué la heurística no rompe la optimalidad.
3. Representar conocimiento en **lógica proposicional** y en lógica de primer orden, y usar **inferencia** (model checking, resolución) o encadenamiento hacia adelante/atrás para derivar conclusiones.
4. Usar **inferencia probabilística** con variables aleatorias, independencia condicional, redes bayesianas y muestreo (likelihood weighting, Gibbs), más HMM y filtrado para estado dinámico.
5. Modelar problemas de satisfacción de restricciones y resolverlos con backtracking, forward checking, propagación de arcos y heurísticas MRV/valores mínimos.
6. Optimizar con **hill climbing**, simulated annealing, búsqueda tabú y algoritmos lineales/locales, reconociendo cuándo el dominio es discreto y cuándo continuo.
7. Distinguir **aprendizaje supervisado, no supervisado y por refuerzo**, y evaluar un clasificador (sensibilidad, especificidad, precisión, recall, F1, costo de falsos positivos vs. falsos negativos).
8. Entrenar un **perceptrón y una red multicapa**, explicar el descenso de gradiente y el backpropagation, y por qué una red con activación no lineal puede aproximar funciones que un modelo lineal no.
9. Explicar los **n-gram, la entropía y la perplejidad**, y por qué medir un modelo de lenguaje con perplejidad tiene el sentido que tiene (y sus límites frente a los modelos de 2026).
10. Decidir, frente a un problema nuevo, **cuál de las siete familias** corresponde, y qué evidencia haría cambiar de familia.

## Mapa temporal

| Tiempo | Bloque |
|---|---|
| 0:00:00 - 0:02:44 | Introducción al curso y recorrido de los ocho módulos |
| 0:02:44 - 1:51:52 | Módulo 1 — Search |
| 1:51:55 - 3:39:31 | Módulo 2 — Knowledge |
| 3:39:39 - 5:34:05 | Módulo 3 — Uncertainty |
| 5:34:08 - 7:18:38 | Módulo 4 — Optimization |
| 7:18:52 - 9:04:28 | Módulo 5 — Learning |
| 9:04:41 - 10:45:42 | Módulo 6 — Neural Networks |
| 10:46:00 - 11:51:15 | Módulo 7 — Language |

> Los cortes de 1:51:55, 3:39:39, 5:34:08, 7:18:52 y 10:46:00 son el inicio del cue del saludo de vuelta del profesor (el capítulo oficial de la descripción cae unos segundos antes, sobre música de transición). El último cue del transcript cierra en 11:51:15, unos segundos antes de los 11:51:22 del reproductor.

---

## Módulos

### Módulo 1 - Search (0:02:44 - 1:51:52)

- **Objetivo:** formular una tarea como un problema de búsqueda -estado inicial, acciones, modelo de transición, test de objetivo y costo-, y elegir el algoritmo correcto según la forma del espacio.

- **Contenidos:**
  - **Qué es un problema de búsqueda.** Un agente que debe llegar de un estado inicial a un objetivo por una secuencia de acciones: "This is an example of what you might call a search problem." (0:06:04)
  - **Estado.** Una configuración del agente en su entorno; el estado inicial y las acciones disponibles definen el espacio: "A state is just some configuration of the agent in its environment." (0:07:49)
  - **Modelo de transición.** Da el estado que resulta de aplicar una acción; el conjunto de estados y transiciones dibuja el grafo del problema: "And in order to do that, we'll introduce to our AI a transition model, which" (0:09:56)
  - **Test de objetivo.** La condición que dice si un estado es meta; sin él no hay nada que buscar: "is a goal test, some way to determine whether a given state is a goal state." (0:13:30)
  - **Costo de camino.** No toda solución vale lo mismo: el algoritmo busca la de menor costo: "we'd really like to find one that minimizes this path cost." (0:14:51)
  - **Frontier.** La estructura que guarda lo que todavía se puede explorar; el tipo de cola (pila o fila) decide el algoritmo: "to be stored inside of a single data structure that we'll call the frontier." (0:19:12)
  - **DFS.** Usa una pila y explora lo más profundo; ahorra memoria, no garantiza optimalidad: "that we call this version of the algorithm depth first search." (0:30:36)
  - **BFS.** Usa una cola y explora por niveles; garantiza el camino más corto en costo unitario, a costa de memoria: "It turns out that there's another algorithm called breadth first search," (0:30:52)
  - **Greedy best-first.** Ordena por una heurística y elige el nodo que parece más cerca: "Greedy best-first search, often abbreviated G-BFS," (0:57:05)
  - **Manhattan distance.** La heurística del laberinto: distancia horizontal más vertical, ignorando las paredes: "And it's something called the Manhattan distance," (0:58:57)
  - **A\*.** Suma el costo ya recorrido y la heurística estimada; con la heurística correcta, es óptimo: "A star search is going to solve this problem" (1:07:45)
  - **Admisibilidad.** La heurística nunca puede sobreestimar el costo real: "So the conditions are H of n, my heuristic, needs to be admissible." (1:11:55)
  - **Lo que significa admisible.** El criterio exacto que sostiene la optimalidad de A\*: "Well, a heuristic is admissible if it never overestimates the true cost." (1:11:55)
  - **Minimax.** Búsqueda adversaria: un jugador maximiza la utilidad y el otro la minimiza: "is an algorithm called Minimax, which works very well" (1:16:36)
  - **Alpha-beta pruning.** Poda las ramas que no pueden cambiar la decisión, sin perder el resultado: "is called alpha, beta pruning." (1:45:51)
  - **Depth-limited + evaluación.** Cuando el árbol es intratable (ajedrez), se corta a cierta profundidad y se estima con una función de evaluación: "to depth-limited Minimax called an evaluation function, which" (1:48:51)

- **Claims y evidencia:** *motivación y datos de escala*. El profesor da cifras del espacio de estados del ajedrez y contrasta con demos medidas en clase (maze2: casi 400 estados expandidos por DFS contra 77 por BFS). Los conteos salen de demos reproducibles con el código del curso; las cifras del ajedrez son ilustrativas.

- **Ejercicio:** implementar A\* sobre un laberinto en texto con la Manhattan de la clase. Entregable: `search/astar.py` que imprima la ruta y la cantidad de estados expandidos; correrlo sobre dos mapas y comparar contra BFS. La prueba es que A\* expanda menos en ambos y devuelva el mismo costo.

- **Candidatos de adopción para un workspace de agentes:** (1) cuando un agente elige qué herramienta usar, decidir por costo ya pagado más estimación del resto, y no solo por lo que parece más cerca (el error del greedy); (2) contar los pasos expandidos de un bucle de agente, como se cuentan los estados del laberinto.

### Módulo 2 - Knowledge (1:51:55 - 3:39:31)

- **Objetivo:** representar hechos en lógica proposicional y de primer orden, y derivar conclusiones con un motor de inferencia en vez de código ad hoc.

- **Contenidos:**
  - **Knowledge base.** Un conjunto de oraciones que la IA sabe verdaderas; es lo que se le puede preguntar: "Inside of a knowledge base, so to speak, information that we know." (1:54:14)
  - **Entailment.** La consecuencia lógica: si todo modelo que hace verdadera la base hace verdadera la consulta, la base la implica: "And that is the notion of entailment." (2:08:47)
  - **Model checking.** El algoritmo más simple: enumerar todos los modelos y verificar la implicación: "And one of the simplest, perhaps, is known as model checking." (2:14:26)
  - **Modus ponens.** Si se sabe `P implica Q` y se sabe `P`, se concluye `Q`; la primera regla de inferencia: "This inference rule is known as modus ponens," (2:57:16)
  - **Resolution.** El método completo: probar la negación de la consulta por contradicción: "of the most common, which is known as resolution." (3:09:42)
  - **Lógica de primer orden.** Reemplaza la explosión de símbolos por predicados, constantes y cuantificadores: "known as first order logic, which is a little bit more powerful than" (3:30:28)
  - **Cuantificador universal.** "Para todo x" permite escribir una regla una vez en lugar de N oraciones: "the first of which is universal quantification." (3:34:58)
  - **Ingeniería del conocimiento.** El trabajo real: traducir un problema (Clue, Hogwarts) a símbolos y reglas: "is known as knowledge engineering." (2:32:03)

- **Claims y evidencia:** sin claims cuantitativos fuera del costo de model checking (2^n modelos), que el profesor usa como argumento. Es demostración en vivo, no medición.

- **Ejercicio:** codificar el puzzle de Hogwarts (personas, casas, "solo una casa por persona") con `logic.py` y consultar una consecuencia que no está escrita. Entregable: `knowledge/houses.py` que imprima la consulta; la prueba es que la conclusión no aparezca literalmente en ningún axioma.

- **Candidatos de adopción para un workspace de agentes:** (1) una regla repetida en N archivos es candidata a axioma (una sola fuente), no a `grep` preventivo; (2) distinguir en un gate entre *encontrar* la regla (model checking, enumerar todo) y *derivar* de ella (resolution), que es la diferencia entre un checklist y un script.

### Módulo 3 - Uncertainty (3:39:39 - 5:34:05)

- **Objetivo:** razonar con incertidumbre: probabilidad condicional, redes bayesianas, muestreo y modelos de estado dinámico.

- **Contenidos:**
  - **Rango de la probabilidad.** Un valor entre 0 y 1; no hay probabilidades negativas ni mayores que uno: "must range between 0 and 1 inclusive." (3:43:16)
  - **Probabilidad condicional.** El grado de creencia en una proposición dado un dato que ya se reveló: "So conditional probability is the degree of belief in a proposition" (3:49:37)
  - **Independencia.** Dos eventos son independientes cuando conocer uno no cambia la creencia sobre el otro: "And independence refers to the idea that the knowledge of one event" (4:01:27)
  - **Regla de Bayes.** El mecanismo para invertir una condicional: pasar de `P(e|h)` a `P(h|e)`: "in probability theory, which is known as Bayes rule." (4:06:02)
  - **Red bayesiana.** Una red de variables aleatorias donde las flechas codifican dependencia, y la estructura ahorra el cálculo: "And a Bayesian network is just going to be some network of random variables," (4:29:22)
  - **Inferencia por enumeración.** La respuesta exacta: sumar sobre las variables ocultas. Cara, pero correcta: "So the formula for how you do this in a process known as inference by enumeration" (4:48:57)
  - **Sampling.** Cuando enumerar es intratable, se estima con muestras: "In the process of sampling, I'm going to take" (5:00:37)
  - **Likelihood weighting.** La variante que fija la evidencia y pondera las muestras por su probabilidad: "One such sampling method is called likelihood weighting." (5:09:05)
  - **Cadena de Markov.** La secuencia de variables donde solo importa el estado anterior: la simplificación que hace tratable el futuro: "where a Markov chain is just some sequence of random variables" (5:14:36)
  - **Hidden Markov model.** El estado real está oculto y solo se observan emisiones; es el modelo del filtrado: "before, we're going to use what we call a hidden Markov model." (5:23:57)

- **Claims y evidencia:** *evidencia teórica* (la fórmula de Bayes, la suma a 1) con ejemplos de juguete (dados, clima). No hay benchmark: el sustento está en la matemática, que se demuestra en clase.

- **Ejercicio:** red bayesiana de tres variables (clima → tráfico → demora); calcular una query a mano con enumeración y después con 10.000 muestras de likelihood weighting. Entregable: `uncertainty/bayes.py` con ambos resultados impresos; la prueba es que la estimación converja al valor exacto al crecer el número de muestras.

- **Candidatos de adopción para un workspace de agentes:** (1) una regla de memoria aprendida de un caso único es un estimador con n=1: guardar la frecuencia junto con la regla; (2) tratar los checks de un gate como evidencia condicional y no como probabilidad incondicional.

### Módulo 4 - Optimization (5:34:08 - 7:18:38)

- **Objetivo:** resolver problemas donde importa el resultado y no el camino, con búsqueda local, programación lineal o satisfacción de restricciones.

- **Contenidos:**
  - **Búsqueda local.** No le importa cómo llegar, solo cuál es la mejor configuración: "is known as a local search." (5:35:17)
  - **Hill climbing.** Sube al vecino con mejor valor y se queda cuando ninguno mejora: "On the other hand, in local search, this is going" (5:35:51)
  - **Simulated annealing.** Se inspira en el recocido físico: aceptar movimientos peores al principio y cada vez menos: "as simulated annealing, simulated because it's modeling" (6:03:50)
  - **Temperatura.** La idea general: ruido decreciente para escapar de los óptimos locales: "And that's going to be the general idea of simulated annealing." (6:04:06)
  - **Programación lineal.** Otra familia de problemas de optimización, sobre variables reales: "are known as these categories of linear programming types of problems." (6:14:55)
  - **Minimizar sujeto a restricciones.** Formular el problema como una función de costo con límites: "the goal of linear programming is to minimize a cost function." (6:15:13)
  - **CSP.** Un problema de satisfacción de restricciones: variables, dominios y restricciones entre ellas: "Well, a constraint satisfaction problem is just some set of variables, x1" (6:28:30)
  - **Arc consistency.** Cada valor del dominio de una variable debe tener un valor compatible en la vecina: "And arc consistency refers to when all of the values in a variable's domain" (6:37:17)
  - **AC-3.** El algoritmo que propaga la arc consistency hasta que no cambia nada: "But this now is AC3, this algorithm for enforcing arc consistency" (6:47:02)
  - **Backtracking.** Asignar, y si no se puede avanzar, retroceder: "is something known as backtracking search." (6:51:04)
  - **La idea del backtracking.** Probar una asignación y volver atrás cuando el siguiente no se puede satisfacer: "And the big idea of backtracking search is we'll" (6:51:04)
  - **Mantener la arc consistency durante el backtracking.** El paso de inferencia que poda antes de equivocarse: "And by maintaining arc consistency in the backtracking search process," (7:07:26)

- **Claims y evidencia:** *motivación* en los ejemplos (hospitales, vendedor viajante) y *evidencia de código* al correr `scipy.optimize.linprog` en vivo, que devuelve el óptimo del problema de fábrica. No hay comparación de tiempos.

- **Ejercicio:** resolver el mismo CSP de dos formas -backtracking puro y backtracking con forward checking y arc consistency- contando nodos explorados. Entregable: `optimization/csp.py` con ambos conteos; la prueba es que la versión con inferencia explore estrictamente menos y devuelva la misma asignación válida.

- **Candidatos de adopción para un workspace de agentes:** (1) distinguir si importa el camino (search) o solo el resultado (local search): un plan y un informe no se mejoran con el mismo algoritmo; (2) el agente que mejora un draft con la última sugerencia es hill climbing: no escapa del óptimo local, y por eso necesita un criterio externo en vez de más vueltas del mismo modelo.

### Módulo 5 - Learning (7:18:52 - 9:04:28)

- **Objetivo:** aprender una función desde datos: clasificación, regresión, evaluación honesta y aprendizaje por refuerzo.

- **Contenidos:**
  - **Aprendizaje supervisado.** Se le da al sistema pares entrada-salida etiquetados por una persona y aprende la función: "And one of the most popular is the idea of supervised machine learning," (7:20:00)
  - **Clasificación.** La tarea de asignar una categoría a una entrada: "And classification is the problem where, if I give you a whole bunch of inputs," (7:20:49)
  - **Regresión lineal.** Buscar la recta que separa o ajusta los datos: "Now what we're doing is trying to use a technique known as linear regression" (7:32:31)
  - **Regresión logística.** Un umbral suave en lugar de un corte duro: la salida es una probabilidad: "as logistic regression is instead of using this hard threshold" (7:50:25)
  - **Perceptrón.** La regla de aprendizaje más simple: ajustar los pesos cuando se equivoca: "One of the most common is known as the perceptron learning rule." (7:42:09)
  - **Support vector machine.** Busca el separador de margen máximo, y funciona mejor en dimensiones altas: "The support vector machine will try and find this maximum margin separator," (7:55:20)
  - **Regresión (salida continua).** El problema hermano de la clasificación: predecir un número, no una etiqueta: "where we try and learn a function mapping inputs to outputs same as before." (7:58:35)
  - **Overfitting.** El modelo se ajusta demasiado a los datos de entrenamiento y deja de generalizar: "with anything that we're trying to do, is a problem known as overfitting." (8:08:29)
  - **Regularización.** Sumar a la función de costo un término que penaliza la complejidad del modelo: "So oftentimes, you'll see us add some regularizing term" (8:15:04)
  - **Train/test split.** Evaluar sobre datos que el modelo no vio; es la única forma de detectar que no generaliza: "But the key idea is separating the training data from the testing data," (8:18:07)
  - **Aprendizaje por refuerzo.** No hay dataset: el agente aprende de la experiencia y de la recompensa: "reinforcement learning is all about learning from experience." (8:28:50)
  - **Markov decision process.** Estados, acciones y recompensas: el modelo formal del problema de decisión: "as what's known as a Markov decision process, similar in spirit" (8:31:56)
  - **Q-learning.** Aprender el valor de tomar cada acción en cada estado, sin conocer el modelo: "And the one that we're going to look at is a method known as Q-learning." (8:38:43)
  - **Exploración vs. explotación.** Elegir siempre lo mejor conocido deja sin descubrir rutas mejores: "and it's never going to explore and go along that route instead." (8:48:25)

- **Claims y evidencia:** *evidencia* en la demo de billetes falsos (entrenamiento, test y regularización con resultados visibles) y *motivación* en el robot que camina. No se usan métricas formales de precisión y recall en este módulo.

- **Ejercicio:** entrenar un clasificador sobre un dataset chico propio, separar train/test y medir la caída. Entregable: `learning/eval.py` que imprima precisión en train, en test, y con y sin regularización; la prueba es que el regularizado no baje en test aunque suba la pérdida en train.

- **Candidatos de adopción para un workspace de agentes:** (1) separar casos de prueba de ejemplos de desarrollo: medir un gate sobre las mismas tareas con las que se corrigió es overfitting; (2) todo lo aprendido en el workspace -modelos de agentes y prompts- se valida en held-out, igual que un clasificador.

### Módulo 6 - Neural Networks (9:04:41 - 10:45:42)

- **Objetivo:** construir y entrenar una red neuronal: unidades, activaciones, descenso de gradiente, backpropagation y capas ocultas.

- **Contenidos:**
  - **ANN.** Un modelo matemático de neuronas que mapea entradas a salidas y aprende sus pesos: "in effect designing an artificial neural network, or an ANN," (9:06:25)
  - **Función de activación.** La no linealidad que decide cuándo una unidad se enciende: "will come to call an activation function, a function that" (9:10:46)
  - **Sigmoid.** La curva en S que da una probabilidad intermedia en lugar de un booleano: "was the logistic sigmoid function that has sort of an s-shaped curve," (9:11:04)
  - **Multicapa.** Agregar capas ocultas: la red puede representar funciones que un modelo lineal no: "Well, what was proposed was the idea of a multilayer neural network," (9:34:43)
  - **Capa oculta.** Las unidades intermedias cuyo valor correcto los datos no dicen: "It has an output layer, but also has one or more hidden layers in between." (9:35:00)
  - **Backpropagation.** Propagar el error del output hacia atrás para estimar el error de cada capa oculta: "but the idea of this algorithm is known as back propagation." (9:38:10)
  - **Descenso de gradiente.** El algoritmo que mueve los pesos en la dirección que reduce la pérdida: "And what gradient descent is, it is an algorithm" (9:20:45)
  - **SGD.** Un punto a la vez en lugar de todos: converge más rápido por paso: "We can employ a method like stochastic gradient descent," (9:24:15)
  - **Mini-batch.** El compromiso: un grupo chico de puntos, más estable que uno y más barato que todos: "is a technique called mini-batch gradient descent, where the idea there" (9:25:21)

- **Claims y evidencia:** *demostración en vivo* con TensorFlow (clasificación de puntos, dígitos de MNIST, caption bot) y *motivación* histórica (perceptrón de los 50 y la crítica de Minsky). Los resultados se ven en pantalla, no se comparan por métricas.

- **Ejercicio:** implementar backpropagation a mano para una red de una capa oculta y comparar con la librería. Entregable: `nn/backprop.py` entrenando sobre un dataset sintético por ambos caminos; la prueba es que la pérdida final difiera menos que un epsilon fijo y que el gradiente analítico coincida con el numérico.

- **Candidatos de adopción para un workspace de agentes:** (1) cuando un agente "itera" un texto, la señal llega desde el output: sin ver el criterio final, el plan y el outline no tienen cómo corregirse; (2) el batch importa: corregir sobre un caso a la vez da gradiente ruidoso, y es la razón para tener un set de casos y no una iteración suelta.

### Módulo 7 - Language (10:46:00 - 11:51:15)

- **Objetivo:** procesar lenguaje natural: tokenización, n-gram, clasificación de texto, RNN y atención.

- **Contenidos:**
  - **NLP.** La disciplina de hacer que las computadoras trabajen con lenguaje humano: "Well, they all fall under this general heading of natural language processing," (10:47:10)
  - **Tokenización.** Separar el texto en unidades: la primera decisión de todo pipeline de lenguaje: "And we were able to do this essentially via a process known as tokenization." (11:02:27)
  - **n-gram.** Secuencias contiguas de n ítems: la base del modelo estadístico de texto: "An n-gram is just some contiguous sequence of n items from a sample of text." (10:59:45)
  - **Cadena de Markov para texto.** Predecir la próxima palabra a partir de las n-gramas, y generar texto que sigue el patrón: "So the one thing that we might try is we could build a Markov chain," (11:02:44)
  - **Bag of words.** Representar el texto como una bolsa sin orden, suficiente para clasificar: "We're going to use a model known as the bag of words model, which" (11:07:00)
  - **Naive Bayes.** Clasificar texto combinando bag of words con la regla de Bayes: "to build something known as a naive Bayes classifier." (11:07:32)
  - **Red neuronal recurrente.** Procesar la secuencia palabra por palabra, guardando un estado oculto: "Well, one tool that we can use is the recurrent neural network, which" (11:29:00)
  - **Atención.** Decidir a qué palabras del contexto prestar atención al generar la siguiente: "Attention is all about letting us decide which values" (11:34:30)
  - **Self-attention.** Cada palabra mira a las demás del propio input; es lo que permite paralelizar: "is going to be a self-attention step." (11:43:40)
  - **Transformer.** La arquitectura que reemplaza la recurrencia por atención: "And that's known as the transformer architecture." (11:40:08)

- **Claims y evidencia:** *demostración en vivo* de generación con Shakespeare y clasificación de reviews, más una *afirmación sin benchmark* sobre la calidad del transformer frente al RNN. El curso es de 2020: el módulo se detiene en la arquitectura del transformer y no cubre los modelos de lenguaje de escala de 2026.

- **Ejercicio:** entrenar un bigram sobre un corpus propio y medir perplejidad en held-out variando el tamaño del corpus. Entregable: `language/ngram.py` con tres valores de perplejidad para tres recortes; la prueba es que el valor empeore cuando el held-out queda fuera del estilo del corpus, lo que muestra que la métrica mide ajuste y no utilidad.

- **Candidatos de adopción para un workspace de agentes:** (1) tokenizar y normalizar antes de comparar: dos documentos que parecen distintos por formato pueden ser el mismo contenido, y esto evita duplicados en la memoria; (2) la atención es filtro, no memoria: un agente que atiende a todo el contexto pierde señal, y recortar por relevancia es una decisión de diseño.

---

## Ejercicios por bloque

El curso está pensado con un proyecto por módulo, publicados en https://cs50.harvard.edu/ai/2020/. La columna de la derecha es el entregable que verifica el módulo.

- [ ] **Search** — escribir el agente y medir: ¿cuántos estados expande A\* frente a BFS en el mismo grafo? El número de expansiones es el objetivo del ejercicio, no el resultado.
- [ ] **Knowledge** — codificar un conjunto de creencias en lógica proposicional y pedirle al motor de inferencia que pruebe una consecuencia que a mano cuesta ver.
- [ ] **Uncertainty** — implementar likelihood weighting sobre una red bayesiana chica y comparar con el resultado exacto.
- [ ] **Optimization** — resolver el mismo problema con hill climbing y con simulated annealing; medir cuántas veces cada uno queda en un óptimo local.
- [ ] **Learning** — entrenar un clasificador de dos clases, armar la matriz de confusión y justificar el umbral elegido con un costo real.
- [ ] **Neural Networks** — implementar backpropagation a mano sobre una red de una capa oculta y comparar contra una librería.
- [ ] **Language** — entrenar un bigram sobre un corpus propio, medir perplejidad en held-out y explicar por qué el número se mueve cuando cambia el corpus.

## Banco de preguntas para estudiar con el usuario

1. ¿Por qué A\* es óptimo solo si la heurística es admisible, y qué pasa con una heurística consistente que es peor que otra admisible?
2. Si el mundo es cierto, ¿para qué sirve la lógica probabilística? ¿Qué gana un sistema cuando admite incertidumbre y qué pierde?
3. La independencia condicional es la suposición que hace barata una red bayesiana. ¿Cuándo esa suposición es mentira y cómo se nota en la práctica?
4. El módulo de optimization distingue problemas cuyos pasos importan de problemas cuyo costo total importa. ¿Qué clase de problema del workspace de agentes cae de cada lado?
5. Si un modelo lineal y una red neuronal tienen el mismo número de parámetros, ¿por qué la red puede aprender una función que el lineal no?
6. ¿Por qué el descenso de gradiente necesita una tasa de aprendizaje y qué pasa conceptualmente si se elige mal, en los dos sentidos?
7. La perplejidad mide qué tan sorprendido queda un modelo. ¿Por qué un modelo con menor perplejidad no es automáticamente mejor generando texto?
8. De las siete familias, ¿cuál usarías para decidir qué herramienta llamar en un agente, y cuál para decidir si dos textos hablan de lo mismo? Justificá con la estructura del problema, no con la moda.

## Notas editoriales

- **Fecha del curso.** Publicado 2023-08-10, material de CS50 AI de 2020. Los ejemplos de NLP terminan en n-gram y Markov; no cubren transformers, embeddings ni atención. Se enseña como fundamento, y el outline marca dónde el estado del arte de 2026 va más lejos.
- **Duración.** 11:51:22 según el reproductor; el transcript cierra en 11:51:15.
- **Proyectos del curso.** La descripción enlaza https://cs50.harvard.edu/ai/2020/, no un repo. Los ejercicios del outline derivan de la estructura de los módulos, no copian enunciados que no fueron transcriptos.
- **ASR.** Los captions son manuales (no auto-generados) y la calidad es alta; los errores se limitan a términos técnicos. Glosario en `transcripcion.md`.
- **Adopción.** Ver `ADOPCION.md`: qué de la clase cambia algo en el workspace y qué queda descartado.

<!-- project: github.com/gonzoblasco/workspace_openclaw -->
