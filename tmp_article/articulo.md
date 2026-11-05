---
title: "Nova Coder: el código que sabe escribir y el razonamiento que no"
author: "Kanam · para Gonzalo Blasco"
date: "5 de noviembre de 2026"
---

# Nova Coder

## El código que sabe escribir y el razonamiento que no

**Un modelo de 15.700 millones de parámetros que se presenta como especialista en programación, evaluado en siete pruebas reales sobre una Mac mini de 24 GB.**

*Por Kanam — 5 de noviembre de 2026*

---

Hay una clase de modelo que resulta difícil de evaluar porque hace dos cosas a la vez: escribe código correcto y, cuando le preguntás algo fuera de eso, contesta con una seguridad que no tiene respaldo. Nova Coder es exactamente esa clase.

Se llama **Nova Coder**, lo publica **Moderno Tech**, y en Hugging Face se anuncia como *"inteligencia artificial especializada en programación"* con *"aproximadamente 16.000 millones de parámetros"*. Todo eso es cierto. Lo que el anuncio no dice es que por debajo corre el mismo motor que DeepSeek publicó en 2024, requantizado y con otra marca en la tapa.

Esta es su evaluación.

---

## I. Lo que es, antes de lo que promete

| Dato | Hallazgo |
|---|---|
| Repo de origen | `second-state/DeepSeek-Coder-V2-Lite-Instruct-GGUF` |
| Arquitectura | DeepSeek V2, 27 capas, 64 expertos enrutados |
| Parámetros | 15,7 mil millones totales · **2,4 mil millones activos por token** |
| Contexto declarado | 163.840 tokens |
| Licencia | MIT + DeepSeek License Agreement |
| Descargas al momento del análisis | 61 |
| Benchmarks publicados | **Ninguno** |

El dato de los parámetros merece una aclaración. El anuncio dice "16B" y lo compara con otro modelo de la misma familia diciendo que *"la cantidad de parámetros no determina por sí sola el rendimiento"*. Es una frase razonable que, en este contexto, evita decir lo importante: no son 16 mil millones de parámetros trabajando a la vez. Son **2,4 mil millones activos por token**. Un modelo denso de 16B y este comparten cifra de portada, no carga de trabajo.

El repositorio de Hugging Face expone el origen sin disimulo en su propio JSON. El nombre y el banner son nuevos; los pesos tienen dos años.

---

## II. El techo de contexto no es el que promete

La primera sorpresa no tiene que ver con la inteligencia del modelo sino con su configuración. Ollama toma el contexto del archivo GGUF y arma la memoria para 163.840 tokens. En una máquina de 24 GB de RAM eso significa que el modelo deja de entrar en la GPU y empieza a pagar el excedente en disco.

| Contexto | Respuesta a un saludo | RAM ocupada por el motor |
|---|---:|---:|
| 8.192 | 11 s | 17 GB |
| 32.768 | 18 s | 17 GB |
| 65.536 | 89 s | 30 GB |
| 131.072 | 112 s | 48 GB |
| 163.840 | **469 s** | **57 GB · swap al 92 %** |

Con el contexto por defecto, la primera prueba tardó casi ocho minutos en devolver una función de tres líneas. No es que el modelo "rinda menos": es que la máquina pasa la mayor parte del tiempo moviendo memoria.

![](fig2_contexto.png)

Un usuario que lo descargue y lo use sin ajustar nada va a concluir que el modelo es basura. No lo es. Está mal configurado de fábrica.

---

## III. Siete pruebas, un solo intento

Todas las pruebas se corrieron con el mismo ajuste —`num_ctx 32768`, temperatura 0, sin límite de tokens de salida— y sin reintentos. Un tiro por uso.

| Prueba | Qué se pidió | Tiempo | Veredicto |
|---|---|---:|---|
| Función simple | `es_par(n)` | 33,7 s | ✓ correcto |
| Explicación técnica | Context manager, en rioplatense | 6,8 s | ✓ correcto · ✗ registro |
| Debugging | Encontrar un `KeyError` | 15,5 s | ✓ diagnóstico |
| Refactor | Inyectar dependencia de tiempo | 37,7 s | ~ con errores |
| Algoritmo complejo | Orden topológico iterativo | 32,9 s | ✓✓ sobresaliente |
| Pregunta trampa | Por qué no usar Raft con 3 nodos | 53,7 s | ✗ **falso** |
| Soporte a usuario | Explicar `ECONNREFUSED` | 3,7 s | ~ respuesta errada |

![](fig1_tiempos.png)

---

## IV. Donde brilla

La quinta prueba es la mejor de la tanda. Se le pidió un ordenamiento topológico —el problema de decidir en qué orden instalar paquetes cuando cada uno depende de otros— con tres restricciones: iterativo, eficiencia lineal, y devolver vacío si hay un ciclo. Resolvió las tres.

```python
def resolve_deps(packages):
    graph = defaultdict(list)
    in_degree = {pkg: 0 for pkg in packages}
    for pkg, deps in packages.items():
        for dep in deps:
            graph[dep].append(pkg)
            in_degree[pkg] += 1
    queue = deque([p for p in packages if in_degree[p] == 0])
    result = []
    while queue:
        pkg = queue.popleft()
        result.append(pkg)
        for neighbor in graph[pkg]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    return None if len(result) != len(packages) else result
```

Eligió el algoritmo correcto (Kahn), invirtió el grafo bien, detectó el ciclo por longitud y declaró la complejidad `O(n+m)` con precisión. Es el trabajo de un modelo que efectivamente sabe de código.

El debugging siguió el mismo camino: identificó el `KeyError` y propuso una corrección. La decisión de usar `.get()` para asumir cero es discutible —enmascara datos mal formados en lugar de fallar— pero la tomó, y la explicó.

---

## V. Donde falla

La sexta prueba es la que importa.

**La pregunta:** "Tengo 3 servidores y quiero tolerar la caída de 1 sin perder datos. ¿Qué consenso uso? ¿Y por qué no debería usar Raft?"

**La respuesta:** que Raft tiene *"sobrecarga de comunicación"* y es *"demasiado complejo"* para un sistema de tres servidores, y que convendría usar Paxos o Zab, *"más ligeros y simples"*.

Es falso, y está invertido.

Raft tolera exactamente la caída de un nodo en un clúster de tres. Es, de los cuatro algoritmos que mencionó, **el más fácil de implementar y de entender** —está diseñado para eso—. Y Paxos, que recomendó como alternativa, tiene una reputación exactamente opuesta: es notoriamente más difícil de llevar a producción.

La respuesta tiene cuatro secciones, títulos en negrita, enumeraciones prolijas y una conclusión. Todo bien formado. Y el núcleo, al revés. En el mismo texto atribuye el protocolo Zab a *"Yahoo, para su sistema de búsqueda y navegación"*; Zab es el de Zookeeper.

La séptima prueba repite el patrón en pequeño. Ante un error `ECONNREFUSED 127.0.0.1:5432` —que significa "la base de datos corre en esta misma máquina y no está levantada"— respondió que "probablemente hay un problema en el servidor" y le sugirió al usuario revisar *"la conexión desde otro dispositivo"*. El tono fue correcto y el consejo, inútil.

![](fig3_perfil.png)

---

## VI. Dos defectos de fabricación

Antes de evaluar el modelo hubo que resolver dos problemas que no son de calidad sino de empaquetado.

**No tiene razonamiento.** El motor local rechaza cualquier nivel de pensamiento solicitado con un mensaje explícito: *does not support thinking*. No es un modelo al que se le pueda pedir "pensá más" o "pensá menos". Hay un solo modo.

**El formato de conversación está roto.** Ante un saludo breve en castellano, respondió en indonesio: *"Apakah Anda memiliki pertanyaan atau..."*. El formato que trae el paquete es el que puso quien lo renombró, no el nativo del modelo. Con indicaciones largas no se repitió, pero es una falla que el original no tenía.

---

## VII. Conclusión

Nova Coder **escribe código mejor de lo que razona.** Frente a un problema de programación estructurado —un algoritmo, una estructura de datos, un error con causa identificable— responde bien y rápido. Frente a una pregunta que exige criterio, produce una respuesta que suena experta y puede estar equivocada en el punto central, sin ninguna señal de duda.

Para un equipo eso es una herramienta con un uso claro y un límite claro: **sirve como generador de código cerrado, con revisión. No sirve como asesor.**

Y como pieza de infraestructura, el veredicto es más simple: no compite. No tiene razonamiento, su contexto útil en esta máquina es de 32.000 tokens y no los 163.000 que anuncia, y cuesta el triple de memoria que un modelo local más chico para un salto de calidad que no se puede demostrar.

La tapa nueva es prolija. Conviene mirar el motor antes de comprar el auto.

---

### Ficha técnica

| | |
|---|---|
| Modelo evaluado | `hf.co/ModernoTech/Nova-Coder:Q4_K_M` |
| Tamaño en disco | 10 GB |
| Hardware | Mac mini M4 · 10 núcleos · 24 GB RAM |
| Método | 7 usos, 1 intento cada uno, temperatura 0 |
| Contexto de prueba | 32.768 tokens |
| Modelos comparados | Ninguno (evaluación individual) |

*Los tiempos son medidos, no estimados. Las pruebas se corrieron localmente, sin servicios en la nube. Los artefactos completos —salidas, métricas y scripts— quedan archivados en el workspace.*
