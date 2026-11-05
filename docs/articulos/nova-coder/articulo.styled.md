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

# hf.co/ModernoTech/Nova-Coder:Q4_K_M

## Escribe como un manual y se equivoca como un experto: el código anda, la teoría no.

Nova-Coder llega con la promesa implícita de todo coder-modelo de Hugging Face: liviano, rápido, listo para resolverte el backend mientras vos tomás mate. En nuestras pruebas hizo exactamente eso en lo chico y se dio vuelta en lo que importa. Cuando tuvo que explicar consenso distribuido, lo hizo con una seguridad impecable y todo al revés.

## I. Lo que es, antes de lo que promete

Nova-Coder es un modelo distribuido como `hf.co/ModernoTech/Nova-Coder:Q4_K_M`, en cuantización Q4_K_M. El fabricante declara una ventana de 163.840 tokens. La corrida se ejecutó con 32.768: esa decisión fue nuestra, no del modelo, y conviene decirlo antes de que confunda la lectura. Correr este mismo modelo con su contexto completo en una máquina de 24 GB lo empuja a swap y lo vuelve inusable, como se mide más abajo.

| Ficha | Dato medido |
|---|---|
| **Modelo** | hf.co/ModernoTech/Nova-Coder:Q4_K_M (Q4_K_M) |
| **Contexto declarado** | 163.840 tokens |
| **Contexto de corrida** | 32.768 tokens |
| **Carga inicial (p1)** | 13,91 s |
| **Latencia p1 (función simple, 105 tokens out)** | 22,94 s |
| **Latencia p5 (complejo, 817 tokens out)** | 33,46 s |
| **Latencia p6 (trampa, 573 tokens out)** | 62,29 s |
| **Think / reasoning** | 0 caracteres en todas las pruebas |

El dato que el fabricante no dice es el que más duele en el uso diario: el tiempo. Con prompts de 31 a 139 tokens de entrada, las respuestas tardaron entre 13,42 s y 62,29 s en generarse. Para un modelo que se presenta como asistente de código ágil, esa latencia lo pone más cerca del batch nocturno que del pair programming.

## II. El momento en que se da vuelta la tortilla

El hallazgo principal no está en el código. Está en la prueba p6, la trampa de consenso distribuido. Le preguntamos algo sin vueltas: con 3 servidores, ¿qué algoritmo uso para tolerar la caída de uno? Cualquier ingeniero que haya configurado un cluster sabe la respuesta de memoria: Raft y Paxos están diseñados exactamente para eso. Con 3 nodos necesitás mayoría de 2, y si se cae uno, seguís.

Nova-Coder contestó lo contrario, con una prosa ordenada, subtítulos y una conclusión que parece salida de un whitepaper:

> "Con solo 3 servidores, no podrás formar una mayoría mayoría necesaria para seguir operando si uno de ellos falla, ya que necesitarías al menos 2 para seguir funcionando."

La frase se contradice sola en la misma oración. Necesitás 2, tenés 3, se cae 1 y te quedan 2. Eso *es* la mayoría. Pero el modelo insiste:

> "con solo 3 servidores, no deberías usar Raft o Paxos directamente"

Y remata recomendando ZooKeeper como si fuera otra categoría, cuando ZooKeeper implementa Zab, que es Paxos con otro nombre y exige el mismo quórum. Para cerrar el círculo, inventa una configuración mágica:

> "podrías configurar ZooKeeper para que necesite una mayoría de 2 servidores en lugar de la mayoría típica de 2/3"

No existe "mayoría típica de 2/3" configurable a gusto. La mayoría es mayoría. Lo que el modelo vende como fine-tuning es un disparate que, si alguien lo intenta aplicar, deja el cluster sin garantías.

Este es el patrón que nos interesa: la calidad de redacción no correlaciona con la corrección. La respuesta más larga, más estructurada y más segura de toda la serie —573 tokens en 62,29 s— es la que el evaluador marcó como FALSO con severidad crítica. No duda, no matiza, no dice "no pudimos verificarlo". Afirma. Y está al revés.

## III. Cómo te habla cuando no te escucha

Antes de llegar al desastre, hay un aviso más sutil. Le pedimos explícitamente castellano rioplatense. No es un capricho estilístico: si un modelo no puede sostener un registro pedido, difícil que sostenga una especificación técnica.

En p2, la explicación del context manager es correcta en contenido:

> "Un context manager en Python es una herramienta que permite definir cómo un objeto debe ser utilizado con la sentencia "with". Permite controlar el acceso a recursos, como archivos o bases de datos, asegurando que estos se abran y cierren automáticamente"

Técnicamente, bien. Lingüísticamente, es español neutro de manual. Cero voseo, cero marca local. El evaluador lo marcó FALSO con severidad media por ignorar la instrucción de registro. Parece menor al lado del delirio de Raft, pero dice algo sobre el empaquetado: el modelo cumple con la forma genérica aunque le pidas otra. Es el mismo reflejo que después lo hace responder cualquier cosa con formato de experto.

La otra señal viene de p4, el refactor para hacer testeable una función que manda mails según la hora. La idea es buena —inyectar `EmailService` y `TimeService`—, pero el código que entrega no corre:

```python
class TimeService:
    @staticmethod
    def now():
        return datetime.datetime.now()
```

Sin `import datetime` previo, eso tira `NameError` al primer test. El evaluador lo marcó INCOMPLETO, severidad media. No es que la refactorización esté mal pensada; es que el modelo te deja con un snippet que parece prolijo y te obliga a debuggearlo vos. Para un asistente que promete ahorrarte tiempo, es una ironía cara: te da la abstracción y te esconde el import.

## IV. Donde funciona

Cuando el problema es chico y autocontenido, Nova-Coder cumple. Y cumple bien.

En p1 le pedimos una función que verifica si un número es par. Respondió en 22,94 s con 105 tokens:

```python
def es_par(n):
    return n % 2 == 0
```

Veredicto: CORRECTO. Sin vueltas, sin dependencias raras. Es lo que querés de un autocompletado.

En p3, el debug con diccionarios, mostró criterio. El error era el clásico `KeyError` por acceder a `cantidad` sin chequear. Propuso:

> "cantidad = i.get('cantidad', 0)  # Usamos 0 como valor por defecto para 'cantidad'"

Y lo acompañó con tres prints que validan los bordes: lista normal, lista vacía y diccionario sin clave. Veredicto: CORRECTO. En 16,41 s y 354 tokens, resolvió lo que muchos juniors dejan pasar.

El mejor momento es p5, el problema algorítmico puro. Le dimos un grafo de dependencias de paquetes y pidió orden topológico. Devolvió Kahn completo, con `deque`, `defaultdict`, cálculo de `in_degree` y detección de ciclos:

```python
if len(result) != len(packages):
    return None
```

En 33,46 s y 817 tokens, la implementación es correcta, eficiente —O(n + m) como declara— y con ejemplo de uso que imprime `['A', 'C', 'B', 'E', 'D', 'F']`. Veredicto: CORRECTO. Acá el marketing de "Coder" se justifica. Si tu trabajo es resolver algoritmos de libro o pulir funciones puras, el modelo te lleva.

## V. Donde falla

El problema es cuando sale del corral de Python y pisa sistemas. Ya vimos p6, pero p7 confirma que no fue un tropiezo aislado.

En p7 le presentamos un error de conexión a base de datos en 127.0.0.1 rechazada. La respuesta arranca bien —chequear si el servicio está corriendo, `sudo service postgresql start`— y enseguida se diluye:

> "Esto podría deberse a varios problemas, como que el servicio de la base de datos no esté corriendo, el puerto esté incorrecto, o haya problemas de red."

Con 127.0.0.1 no hay "problemas de red". Es loopback. El paquete no sale de la máquina. La causa real es una sola: nada escucha en ese puerto local. Al meter "red" en la bolsa, el modelo te manda a revisar firewall, DNS y cableado cuando tenés que mirar `listen_addresses` o si Postgres está levantado. Veredicto: FALSO, severidad alta. Otra vez, el texto suena razonable y te hace perder tiempo en el lugar equivocado.

El patrón se repite: en p2 ignora el registro pedido, en p4 te deja código que no corre, en p6 invierte la teoría de consenso, en p7 confunde loopback con red. No son errores de tipeo. Son errores de concepto dichos con tono de documentación oficial. Ese es el riesgo. Un modelo que duda te obliga a verificar; uno que suena seguro y está equivocado te hace deployar la equivocación.

## VI. Cuánto pide, cuánto da y cómo tratarlo

Nova-Coder en Q4_K_M es liviano de bajar y pesado de esperar. La primera carga nos dio 13,91 s, las siguientes entre 0,02 s y 8,68 s según el caché, pero la generación nunca bajó de 13,42 s y se estiró a 62,29 s en la respuesta más larga. Para 105 tokens de una función par/impar, 22,94 s es mucho. Para 817 tokens de Kahn, 33,46 s es aceptable si el resultado es correcto —y lo fue—.

La brecha entre lo que declara y lo que aguanta esta máquina es real, pero la causa no es que el fabricante mienta: es que un modelo de 10 GB con un KV cache para 163.840 tokens no entra en 24 GB de RAM. La etiqueta es cierta; el hardware es el que no llega. Si planeás meterle un repo entero o logs largos, medí cuánto aguanta tu equipo antes de comprar la promesa.

Configuración: no hay thinking traces —0 caracteres en todas las pruebas—, así que lo que ves es lo que hay. No podés auditar un razonamiento intermedio porque no lo expone. Y cuando el código viene sin imports, como en p4, no hay excusa de truncado: son 455 tokens con lugar de sobra para un `import datetime`.

Si lo vas a usar, usalo encapsulado. Para generar funciones puras, tests unitarios chicos y algoritmos clásicos, rinde. Para diagnosticar infra o decidir arquitectura, no lo dejes solo. Ponelo detrás de un linter que ejecute el código y de un revisor humano que sepa de quórum. No le pidas que elija entre Raft y ZooKeeper; pedile que te escriba el `resolve_deps