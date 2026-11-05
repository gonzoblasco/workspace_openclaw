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

# qwen3.5:9b-mlx

## Cuando habla seguro, es cuando más hay que desconfiar

Un modelo que escribe código prolijo, explica con claridad y resuelve refactors sin transpirar puede parecer confiable. El problema aparece cuando esa misma solvencia se usa para sostener una falsedad técnica con formato de manual. Ahí no hay error de tipeo: hay inversión completa de un concepto.

## I. Lo que es, antes de lo que promete

| Campo | Valor medido |
| :--- | :--- |
| Modelo | qwen3.5:9b-mlx |
| Contexto declarado por el modelo | 262144 tokens |
| Contexto de la corrida | 262144 tokens |
| Carga inicial (p1) | 4,52 s |
| Respuesta función simple (p1) | 7,82 s, 38 tokens de salida, done: stop |
| Respuesta explicación context manager (p2) | 7,24 s, 90 tokens de salida |
| Respuesta debug KeyError (p3) | 30,73 s, 391 tokens de salida |
| Respuesta refactor con inyección (p4) | 99,03 s, 1283 tokens de salida |
| Respuesta orden topológico (p5) | 76,10 s, 1070 tokens de salida |
| Respuesta consenso (p6) | 29,06 s, 413 tokens de salida |
| Respuesta error local PostgreSQL (p7) | 4,74 s, 54 tokens de salida |
| Modo think | false en todas las corridas |
| Quant / empaquetado | mlx, 9b - dato no informado por el fabricante en la corrida |

No hay dato oculto relevante para esta corrida: el contexto declarado coincide con el usado, y el modelo no inventa hardware ni fecha de corte. Lo que sí promete -y no cumple- es la complejidad algorítmica que él mismo declara.

## II. El consenso al revés

Le preguntamos por consenso distribuido en un cluster de 3 nodos con requisito de tolerancia a un fallo. La respuesta del modelo fue categórica:

> "No deberías usar Raft porque **requiere una mayoría absoluta para tomar decisiones**, y con 3 servidores, la caída de 1 deja exactamente a la mitad del sistema fuera del quórum."

Y remata:

> "Raft **se detiene inmediatamente** para evitar inconsistencias (split-brain)"

Recomienda, en cambio, Paxos porque "es el estándar para sistemas que priorizan la disponibilidad".

Es exactamente al revés.

Con 3 nodos, la mayoría es 2. Si cae 1, quedan 2. Dos sobre tres es mayoría. Raft sigue operando. Paxos tiene la misma aritmética de quórum y, además, es notoriamente más difícil de implementar correctamente. El modelo invierte tolerancia y dificultad: presenta a Raft como el que no tolera 1 caída en 3, cuando es el caso canónico que sí tolera, y ofrece Paxos como alternativa más disponible.

No es un matiz. La severidad marcada por el evaluador es crítica, y con razón. El texto viene con subtítulos, negritas, una "matemática de Raft" con fórmula `(N/2) + 1`, y una nota técnica final que intenta cubrirse: "Si tu definición de 'no perder datos' significa solo que no haya corrupción... entonces Raft es válido". Esa nota no corrige el error central, lo embarra. El lector se queda con la idea de que con 3 nodos no puede caer ninguno si usa Raft. Si alguien diseña infraestructura con ese dato, diseña mal.

Este es el patrón que más importa: la seguridad retórica no correlaciona con la corrección factual. El modelo suena a documentación oficial mientras afirma lo contrario a lo que dice cualquier implementación de Raft en producción.

## III. La complejidad que no cierra

El segundo fallo es menos visible pero igual de instructivo.

En la prueba de orden topológico, el modelo entrega una implementación iterativa de Kahn y afirma:

> "Aquí tienes la implementación iterativa en Python que cumple con todos los requisitos: complejidad $O(N+M)$, detección de ciclos y orden topológico correcto."

Y en la explicación detalla:

> "El bucle `while queue` procesa cada nodo exactamente una vez. Dentro, iteramos sobre la lista de dependencias de ese nodo. En total, todas las aristas (dependencias) se visitan una sola vez en todo el proceso."

El código no hace eso. El bucle interno es:

```python
for pkg, deps in packages.items():
    if current_pkg in deps:
```

Eso recorre `packages.items()` completo por cada nodo extraído de la cola. No visita cada arista una vez: visita todos los paquetes por cada nodo. El costo real es `O(N² + N·M)` en el peor caso, no `O(N+M)`. El evaluador lo marca como FALSO con severidad alta, y es correcto: el modelo declara una complejidad que su propio código no cumple.

Funcionalmente el algoritmo puede devolver un orden válido en grafos chicos y detectar ciclos por tamaño de resultado, pero la promesa de eficiencia es falsa. En un grafo de dependencias grande, esa diferencia entre lineal y cuadrático es la que te deja colgado en 76,10 s de generación para después tardar en ejecución.

Son dos fallas distintas con la misma raíz: el modelo describe lo que debería hacer, no lo que efectivamente hace.

## IV. Donde funciona

La función simple es impecable. Ante `es_par`, responde con `return n % 2 == 0` en 7,82 s y 38 tokens. Sin vueltas, sin decoradores innecesarios.

La explicación del context manager también cumple. En 7,24 s y 90 tokens dice: "Lo usás para asegurar que archivos se cierren solos o conexiones se liberen sin tener que escribir código extra." Es rioplatense sin forzar, es técnico sin humo, y evita la tentación de definir un LLM.

El debug del `KeyError` es el mejor tramo. Identifica que "se intenta acceder a `i['cantidad']`. Sin embargo, el diccionario pasado como argumento solo tiene la clave `'precio'` y le falta la clave `'cantidad'`." Propone `.get('cantidad', 0)` y `.get('precio', 0)`, con ejemplos que cubren `[]` y `[{'precio': 5}]`. Son 30,73 s bien usados: explica la causa, muestra el fix, no inventa.

El refactor es el pico de lucidez. En 99,03 s y 1283 tokens aplica inyección de dependencias sin romper comportamiento exterior: "pasaremos el objeto SMTP como argumento" y "Se añade un parámetro opcional `ahora`". Entrega `smtp_client: SMTPClient` y `ahora: datetime.datetime = None` con fallback a `datetime.now()`, más ejemplos con `Mock` y `assert_not_called`. Es código testeable de verdad, con tipado y separación de efectos. Ahí el marketing no hace falta: el código habla.

Incluso el manejo de error local es sobrio. Ante un fallo de conexión a PostgreSQL, no alucina logs ni tira stacktrace: "verifica si el servicio de PostgreSQL está activo y reiniciado en tu máquina." Corto, accionable, en 4,74 s.

Cuando el dominio es Python cotidiano, el modelo es un buen compañero de banco.

## V. Donde falla

Es la prueba trampa de consenso, p6. Pregunta: qué usar con 3 nodos para tolerar 1 caída sin perder datos. Respuesta del modelo: Paxos sí, Raft no, porque "con 3 servidores, la caída de 1 deja exactamente a la mitad del sistema fuera del quórum" y "Raft **se detiene inmediatamente**".

Está mal por partida doble. Primero, aritmética: 2 de 3 es mayoría, Raft no se detiene. Segundo, recomendación: Paxos no es más disponible ni más simple que Raft; es al revés en dificultad de implementación. El modelo construye una tabla comparativa implícita donde el que tolera fallos es Paxos y el que se cae es Raft. Cualquiera que haya operado etcd, Consul o cualquier log replicado con Raft sabe que el caso 3-nodos-1-caída es el caso de uso, no la excepción.

Lo grave no es solo el error, es el envoltorio. Títulos con "Consenso recomendado: **Paxos**", viñetas con "La matemática de Raft", conclusión en negrita. Esa parafernalia hace que el error viaje más lejos que un typo. Un lector apurado copia la recomendación y la repite en una review de arquitectura. El costo no es un test rojo: es una decisión de infraestructura.

El segundo fallo, p5, confirma el patrón. El modelo afirma `O(N+M)` y su loop hace `for pkg, deps in packages.items()` adentro del `while queue`. No es un detalle de notación: es prometer lineal y entregar cuadrático. Si el evaluador no lo cazara, quedaría como "implementación eficiente" en el portfolio.

En ambos casos el modelo no duda. Y cuando no duda estando equivocado, el lector necesita una regla externa para no comerse el verso.

## VI. Empaquetado, límites y configuración

qwen3.5:9b-mlx corre con contexto de 262144 tokens declarados y verificados en la corrida. Es contexto grande de verdad, no marketing de ventana. Los tiempos medidos van de 4,74 s en respuestas cortas a 99,03 s en el refactor largo, con `think: false` en todas las pruebas. No hubo truncado: todos los `done: stop`.

El empaquetado mlx sugiere uso local en ecosistema Apple, 9b parámetros. No hay dato de quantización ni de temperatura en las mediciones, así que no inventamos. Lo que sí se ve es un comportamiento consistente: a más tokens de salida, más segundos de generación, con picos en p4 y p5 que son las respuestas más largas (1283 y 1070 tokens respectivamente).

Límites observados: el modelo no verifica su propia complejidad algorítmica contra su código, y no contrasta afirmaciones de consenso contra aritmética de quórum básica. No es un problema de contexto ni de velocidad: es de auto-chequeo. Con 262144 tokens podés pegarle un paper entero de Raft en el prompt y aún así, si no lo obligás a calcular `quorum = floor(N/2)+1`, te va a repetir el verso con formato lindo.

Configuración recomendada si lo vas a usar igual: pedile que demuestre, no que declare. Que muestre el conteo de operaciones, que liste el quórum numérico para N=3, que ejecute mentalmente el loop con N=1000. Y si la respuesta viene con subtítulos perfectos y sin números, desconfiá un poco más.

## VII. Conclusion

qwen3.5:9b-mlx es sólido en lo chico y peligroso en lo grande: escribe buen Python, explica claro y refactoriza con criterio, pero patina feo cuando tiene que sostener con código lo que promete en prosa y cuando pisa territorio de sistemas distribuidos. De siete pruebas, cinco correctas y dos falsas, una de ellas crítica por invertir la tolerancia a fallos de Raft. No es un mal modelo: es un modelo que suena demasiado bien cuando se equivoca. Usalo para pulir funciones, no para decidir cuántos nodos te mantienen en pie cuando se cae uno.