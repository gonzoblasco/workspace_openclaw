# Review: Nova Coder (Moderno Tech) — evaluación de uso, 2026-11-05

**Modelo:** `hf.co/ModernoTech/Nova-Coder:Q4_K_M`
**Hardware:** Mac mini M4, 24 GB RAM
**Modo:** `num_ctx 32768`, `temperature 0`, sin límite de output, salida libre
**Alcance:** solo Nova. 7 usos distintos. Un intento por uso.

---

## 0. Los dos hallazgos que van antes de todo

### 0.1 No tiene thinking. Ningún nivel.

Ollama rechaza explícitamente cualquier nivel:

```
think: true   → ERROR: "does not support thinking"
think: "low"  → ERROR: "does not support thinking"
think: "medium" → ERROR: "does not support thinking"
think: "high" → ERROR: "does not support thinking"
```

Es un modelo de completion plano. **La premisa de "medir niveles de thinking" no aplica**: hay un solo nivel, que es ninguno. Lo que sigue mide eso.

### 0.2 El template de chat está roto

Con `think: false` y el prompt "Di OK" en español, respondió:

> `Apakah Anda memiliki pertanyaan atau ha...`

**Indonesia.** El template del Modelfile (`User: ... Assistant:`) es el que puso quien rebrandeó el modelo, no el nativo de DeepSeek. Está desalineado y produce idioma aleatorio en prompts cortos. En los prompts largos de la evaluación no volvió a pasar, pero el riesgo está.

### 0.3 A contexto máximo no sirve

Medido antes, en la misma sesión: a `num_ctx 163840` la primera función tardó **469 s** y el runner ocupó **57 GB** con swap al 92 %. A 32768 responde en segundos. Todo lo que sigue está medido a 32k.

---

## 1. Tabla de tiempos

| Uso | Tiempo | Salida |
|---|---:|---:|
| t1 — función simple | 33,7 s | 51 car. |
| t2 — explicación técnica | 6,8 s | 505 car. |
| t3 — debugging | 15,5 s | 1.201 car. |
| t4 — refactor con DI | 37,7 s | 2.881 car. |
| t5 — algoritmo complejo | 32,9 s | 2.566 car. |
| t6 — pregunta con trampa | 53,7 s | 2.597 car. |
| t7 — soporte a usuario | 3,7 s | 285 car. |

---

## 2. Uso por uso

### t1 — Función simple ✅

**Pedido:** `es_par(n)`.

```python
def es_par(n):
    return n % 2 == 0
```

Correcto, mínimo, sin adornos. **Pero 33,7 s para tres líneas.** El cold start se come el tiempo; no es throughput del modelo.

### t2 — Explicación técnica ✅

**Pedido:** contexto manager en rioplatense, 4 líneas.

> Un "context manager" en Python es un objeto que gestiona un contexto de ejecución, asegurando que ciertos recursos se establezcan y liberen de manera automática. Se usa comúnmente con "with" para garantizar que los recursos se liberen incluso si ocurre una excepción durante la ejecución del bloque de código.
>
> Ejemplo: Usar "with open('archivo.txt', 'r') as archivo" para leer un archivo, asegurando que se cierre automáticamente, independientemente de si el proceso termina correctamente o con errores.

Técnicamente correcto. **No es rioplatense**: es español neutro de manual, con comillas dobles angulares y un registro que no es el pedido. Ignoró la instrucción de tono.

### t3 — Debugging ✅ (con reserva)

**Pedido:** encontrar el `KeyError: 'cantidad'` y corregir.

Diagnóstico correcto (falta la clave) y fix con `.get()`. Pero **eligió el fix tolerante** (asumir 0) cuando el problema real es que un item mal formado no debería pasar silenciosamente. Es un `return total` que ahora miente: devuelve 0 en vez de fallar. Es una decisión de diseño, no un bug — y la tomó sin señalarla.

### t4 — Refactor con inyección de dependencias ⚠️

**Pedido:** hacer testeable sin cambiar el comportamiento exterior.

Bien la idea: `RecordatorioService` con `time_provider` y `email_sender` inyectados. Pero:

- **Cambió el comportamiento exterior**: antes la función abría y cerraba el SMTP; ahora la clase `EmailSender` lo hace, y el método devuelve `'enviado'` aunque `EmailSender.sendmail` ya devuelve lo mismo. Hay un valor de retorno que se pierde.
- El test que escribe **no compila**: usa `datetime.datetime(...)` sin importar `datetime` en ese bloque.
- Mockea reemplazando el método de una instancia concreta, que es la forma más frágil de hacerlo.

Idea correcta, ejecución con dos errores concretos.

### t5 — Algoritmo complejo (topological sort) ✅✅

**Pedido:** `resolve_deps`, iterativo, O(n+m), ciclo → None.

Kahn correcto: grafo invertido, grados de entrada, cola, detección de ciclo por longitud. **La complejidad declarada es correcta.** Sin recursión.

Un solo defecto menor: si una dependencia aparece en las listas pero no como clave del dict, revienta con `KeyError` en lugar de tratarla como nodo sin dependencias. El ejemplo que trae evita el caso.

**Este es el mejor output de los siete.** Es donde un modelo de código debería brillar y brilló.

### t6 — Pregunta con trampa ❌

**Pedido:** 3 servidores, tolerar 1 caída. ¿Qué consenso? ¿Y por qué NO RAFT?

Respuesta: recomienda Paxos/Zab *porque Raft tiene "sobrecarga de comunicación" y es "demasiado complejo"* para 3 servidores.

**Es falso.** Raft tolera exactamente 1 caída con 3 nodos, y es el consenso *más simple* de los cuatro que mencionó. La respuesta invierte el argumento real. No contestó la pregunta trampa: la esquivó con una justificación inventada.

Además: dice que Zab lo desarrolló Yahoo "para su sistema de búsqueda y navegación" — Zab es de Zookeeper, no de un buscador.

**Es el output más riesgoso de la tanda**: suena autoritativo, tiene estructura impecable, y el contenido central está mal.

### t7 — Soporte a usuario ⚠️

**Pedido:** `ECONNREFUSED 127.0.0.1:5432` para un usuario no técnico, 3 líneas.

> Parece que el sistema está teniendo problemas para conectarse a la base de datos. Probablemente hay un problema en el servidor o en la configuración de la conexión. ¿Podrías revisar la conexión a la base de datos desde otro dispositivo o verificar si hay algún mantenimiento en curso?

Tono correcto, longitud correcta. **Pero no dio la respuesta obvia**: `127.0.0.1:5432` significa que la base corre *en la misma máquina* y no está levantada. Le hizo revisar "desde otro dispositivo", que en ese contexto no tiene sentido. No es un tecnicismo innecesario: es no decirle lo que tiene que hacer (arrancar Postgres).

---

## 3. Patrón

| Dimensión | Resultado |
|---|---|
| Código algorítmico | **Fuerte.** Kahn, DP, parsers: lo resuelve bien |
| Código simple | Correcto pero lento de arranque |
| Explicación técnica | Correcta y neutra; ignora el registro pedido |
| Refactor | Buena arquitectura, errores de ejecución |
| Razonamiento crítico | **Débil.** Cede a la estructura sobre la sustancia (t6) |
| Empatía / diagnóstico de usuario | Superficial (t7) |
| Español rioplatense | No lo intenta |

**Nova escribe código mejor de lo que razona.** En t5 y t3 demuestra que sabe; en t6 demuestra que puede producir una respuesta perfectamente formada y equivocada en el punto central — sin señal de duda.

---

## 4. Veredicto

**Para generar código estructurado: sirve, con supervisión.**

Es el caso de uso para el que fue hecho y donde rinde. Algoritmos, estructuras de datos, patrones: correcto y legible.

**Para razonar, explicar o atender usuarios: no.**

t6 no es un fallo aislado, es el síntoma de un modelo que aprendió a *sonar* experto. Y el template roto agrega un riesgo de idioma que no debería existir.

**No adoptar en el stack.** No por calidad (16/29 en código, el mejor de los tres locales) sino porque:
1. No tiene thinking — no compite con el resto del router en tareas de razonamiento
2. Su techo de contexto real en esta máquina es 32k, no los 163k que promete
3. Responde en indonesio con prompts cortos
4. No aporta nada que un cloud no haga mejor

**Si se usa**, que sea como generador de código cerrado, con revisión, y con `num_ctx ≤ 32768`.

---

## 5. Artefactos

- Salidas completas: `/tmp/cata_nova/out/nv_t{1..7}_False.txt`
- Métricas: `/tmp/cata_nova/out/nova_review.json`
- Script: `/tmp/cata_nova/nova_review.py`

---

*Evaluación del 2026-11-05. Solo Nova. Sin comparaciones. Tiempos medidos, no estimados.*
