<style>
body { font-family: -apple-system, "Helvetica Neue", Georgia, serif; max-width: 680px; margin: 0 auto; padding: 40px 24px; line-height: 1.65; color: #1d1f1e; font-size: 16px; }
h1 { font-size: 2.1em; line-height: 1.15; letter-spacing: -0.02em; margin-bottom: 0.2em; }
h2 { font-size: 1.35em; margin-top: 2em; border-bottom: 1px solid #e2e5e2; padding-bottom: 0.3em; }
h3 { font-size: 1.1em; margin-top: 1.5em; }
blockquote { border-left: 3px solid #2f6f4f; margin-left: 0; padding-left: 1em; color: #4a4f4c; font-style: italic; }
table { border-collapse: collapse; width: 100%; margin: 1.4em 0; font-size: 0.92em; }
th, td { border: 1px solid #d8dcd8; padding: 0.5em 0.7em; text-align: left; }
th { background: #f4f6f4; font-weight: 600; }
code { background: #f4f6f4; padding: 0.12em 0.35em; border-radius: 3px; font-size: 0.9em; }
pre { background: #f7f8f7; border: 1px solid #e2e5e2; border-radius: 4px; padding: 1em; overflow-x: auto; font-size: 0.85em; line-height: 1.45; }
pre code { background: none; padding: 0; }
hr { border: none; border-top: 1px solid #e2e5e2; margin: 2.5em 0; }
</style>

# gemma4:12b-mlx

## Escribe código como un senior y lee logs como un pasante

Hay modelos que se caen en la trampa y otros que te explican por qué la trampa no existe. Este hace lo segundo, prolijo, en Python, con inyección de dependencias y Kahn sin recursión. Y después, frente a un `ECONNREFUSED 127.0.0.1:5432`, te ofrece tres formulitas de call center.

## I. Lo que es, antes de lo que promete

| Dato | Valor medido |
| :--- | :--- |
| Modelo evaluado | gemma4:12b-mlx |
| Contexto declarado por el modelo | 262.144 tokens |
| Contexto de la corrida | 262.144 tokens |
| Formato | MLX |
| Carga inicial (p1) | 3,83 s |
| Tiempos de respuesta | 5,51 s a 43,27 s según tarea |
| Tokens de salida | 94 a 926 tokens |
| Think / reasoning | false, 0 caracteres de thinking |

El dato que el fabricante no dice: no hay. El modelo declara 262.144 tokens y la corrida corrió con 262.144 tokens. Coincidencia exacta entre lo prometido y lo habilitado, algo que no siempre pasa y que acá sí.

## II. La trampa que no mordió

Si hay un lugar donde los modelos se entregan solos es en las preguntas con carnada. Le tirás un consenso distribuido, tres nodos, y esperás que diga que Raft no sirve para número impar o que Paxos es obsoleto. Gemma4:12b-mlx no solo no pisa el palito: lo levanta, lo mira y te explica por qué lo pusiste ahí.

La pregunta buscaba que afirmara que Raft no funciona con tres servidores. La respuesta fue la contraria: "Raft es perfectamente capaz de funcionar con 3 servidores y tolerar la caída de 1." Y por si quedaba duda, remata: "Es un error conceptual pensar que no puedes usar Raft con 3 servidores."

No es chamuyo. Desarrolla margen de error, latencia y costo con criterio, sin inventar teoremas. Dice que con tres nodos tolerás una falla, que si cae el segundo te quedás sin quórum, y que esa es la configuración mínima estándar para alta disponibilidad. Todo correcto según el evaluador, veredicto CORRECTO sin atenuantes.

Esa solidez no es un accidente. Viene de la misma matriz que le permite resolver el ejercicio complejo de dependencias en 43,27 s y 926 tokens de salida: "utilizaremos el **Algoritmo de Kahn** para el ordenamiento topológico." No hay recursión, hay `deque`, hay `in_degree`, hay detección de ciclos con `if len(order) != len(in_degree): return None`. Es código que podría ir a producción sin que nadie levante una ceja. Complejidad O(n + m) declarada y cumplida, grafo inverso bien construido, casos de prueba con y sin ciclo incluidos.

Cuando un modelo hace eso, uno espera que el resto acompañe. Y acompaña, hasta que le mostrás un log.

## III. El programador que tenés a mano

Antes del tropiezo, lo bueno cotidiano. Porque este modelo no es un demo de algoritmo exótico: es un compañero de editor que responde en rioplatense sin que se lo ruegues y sin caer en el lunfardo de cotillón.

Le pedís una función para saber si un número es par y te devuelve "return n % 2 == 0" con docstring, ejemplos para 4, 7, 0 y -2, y explicación en tres puntos. Tiempo: 13,05 s. Nada del otro mundo, pero correcto y sin vueltas. Veredicto CORRECTO.

Le pedís qué es un context manager y te dice: "Lo usás para manejar archivos, conexiones a bases de datos o bloqueos de hilos sin dejar basura tirada." En 5,51 s y 94 tokens te acomoda `with`, limpieza automática y manejo de errores. No te recita la PEP, te dice para qué sirve. Veredicto CORRECTO.

Le tirás un `KeyError` por diccionario sin `'cantidad'` y te lo arregla con `.get()`: "Para solucionarlo, debes usar el método `.get()`, que permite asignar un valor por defecto (en este caso `0`) si la llave no existe." Código corregido, `precio = i.get('precio', 0)`, test con lista vacía y diccionario incompleto. 12,92 s. Veredicto CORRECTO.

Y cuando le pedís refactorizar una función que depende del reloj y de SMTP, aplica inyección de dependencias como si fuera obvio: "def enviar_recordatorio(email, ahora=None, smtp_client=None):". Mantiene compatibilidad hacia atrás, agrega `MagicMock`, escribe dos tests, uno para las 19:00 y otro para las 10:00, con `assert` y `assert_not_called`. 31,57 s y 707 tokens que valen cada segundo. Veredicto CORRECTO.

Hasta acá, seis de siete pruebas en verde. Un modelo que escribe, corrige y refactoriza Python con criterio, que entiende determinismo y aislamiento de efectos, que no se pierde en el marketing de "código limpio" y te muestra el código limpio. Si tu laburo es codear, este pibe rinde.

## IV. Donde funciona

Funciona donde importa para un dev: en la zona de escritura.

No es solo que no se equivoca. Es que elige bien. Elige `% 2 == 0` en vez de `& 1` para legibilidad. Elige `.get('cantidad', 0)` en vez de `try/except` para un default simple. Elige parámetros opcionales `ahora=None` y `smtp_client=None` para no romper la API existente. Elige Kahn iterativo con cola para evitar `RecursionError` en grafos grandes. Son decisiones de alguien que leyó código ajeno y sufrió código ajeno.

También funciona en el tono. Mantiene el "vos" sin forzar. Dice "Lo usás", "verificá", "Revisá". No se le escapa un "tú" ni un neutro de manual. Para una revista que escribe en rioplatense, eso no es detalle menor: es que podés copiar el snippet y pegarlo en documentación interna sin traducir.

Y funciona bajo presión conceptual. La trampa de Raft era para ver si repetía el mito de que los consensos necesitan pares o impares mágicos. No lo repitió. Corrigió. Eso vale más que cualquier benchmark de contexto grande, porque muestra que no alucina por asociación.

En síntesis: si lo usás como pair programmer para Python, como explicador de conceptos y como revisor de refactors, te devuelve trabajo usable en tiempos razonables, entre 5,51 s y 43,27 s según complejidad, con salidas de 94 a 926 tokens que no se van por las ramas.

## V. Donde falla

Y acá se pincha.

La prueba p7 era simple y cruel: un log con `ECONNREFUSED 127.0.0.1:5432`. Cualquier dev que haya levantado Postgres local sabe qué significa: 127.0.0.1 es tu propia máquina, loopback, no es "la base de datos en algún lado". 5432 es el puerto por defecto de Postgres. ECONNREFUSED es "nadie está escuchando ahí". Traducción: no levantaste el servicio, o lo levantaste en otro puerto, o en otro host. No es un problema de firewall remoto ni de "disponibilidad del puerto" en abstracto. Es local y concreto.

El modelo respondió con tres opciones de atención al cliente:

"El error indica que el sistema no puede conectarse a la base de datos. Por favor, verificá si el servicio de la base de datos está encendido y funcionando correctamente."

Y la tercera, peor: "Revisá si el servicio está iniciado y si el puerto está disponible."

El evaluador lo marcó FALSO con severidad alta, y con razón. No explica que 127.0.0.1 es la misma máquina. No explica que ECONNREFUSED significa que nadie escucha en el puerto. La acción que propone es vaga, "verificá si está encendido", y la mención a "si el puerto está disponible" roza el diagnóstico de red/firewall que la fuente declara FALSO.

Este es el párrafo central de todo el artículo porque es donde suena seguro y está equivocado. No es un error de sintaxis que el intérprete te escupe. Es un error de diagnóstico que te hace perder media tarde. Te manda a revisar si el servicio "está encendido" como si fuera una heladera, cuando el log ya te dijo dónde y por qué: en tu loopback, en el 5432, sin nadie del otro lado.

¿Por qué duele más acá? Porque el mismo modelo que te explicó Kahn con grafo inverso y grados de entrada no pudo traducir una IP de cuatro números. Sabe arquitectura distribuida y falla en local. Sabe inyectar un mock de SMTP y no sabe decir "es tu máquina". Es la asimetría clásica de los LLM entrenados con mucho Stack Overflow y poco troubleshooting de trinchera.

No es que no sepa nada de redes. Es que no conecta el dato concreto del log con la explicación. Generaliza. Y generalizar un `127.0.0.1:5432` es perder la única pista que tenías.

## VI. Empaquetado, límites y configuración

MLX, 12B, contexto de 262.144 tokens declarados y habilitados. Carga en 3,83 s en la primera inferencia, luego 0,00 s a 0,08 s. No hay thinking intermedio, todo es salida directa. Eso explica la velocidad en tareas simples y la demora lógica en la compleja: 43,27 s para Kahn no es lentitud, es que generó 926 tokens de código comentado y testeado.

Límites vistos: no inventa contexto, no alucina APIs, no rompe compatibilidad en el refactor. Pero no confíes en él para leer logs crudos. Si le das un traceback, pedile explícitamente que traduzca IP, puerto y código de error, uno por uno. No asumas que lo va a hacer solo.

Configuración recomendada: usalo con `ctx` alto si vas a pasarle grafos grandes o archivos largos, que lo soporta. Para diagnósticos locales, bajale la temperatura retórica: pedile una sola frase técnica, no tres opciones "dependiendo de qué tanta confianza tengas con él". Esa cortesía es la que lo lleva a la vaguedad.

## VII. Conclusion

Gemma4:12b-mlx es un gran programador de escritorio y un mal operador de guardia. Te escribe el `es_par` prolijo, te salva el `KeyError`, te refactoriza el envío de mails para que sea testeable y te resuelve dependencias sin recursión. Seis de siete en verde lo avalan.

Pero cuando el log te dice en la cara que tu base no está en tu máquina, te contesta con un guion de call center. No lo uses para diagnosticar; usalo para codear. Es el colega que te hace el PR perfecto y después te dice que reinicies la compu cuando no te anda el Postgres local.