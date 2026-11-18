# Brief: "Memoria Oral" — viabilidad de una herramienta local de historia oral familiar (DEV.to Hacktoberfest W4)

**Stop criterion:** cada uno de los 7 puntos del pedido tiene (a) una fuente abierta o (b) una medición propia, o queda declarado `[unk]` con lo que lo saldaría.
**Freshness:** alta — licencias, versiones y disponibilidad de modelos cambian. Todo dato mutable lleva fecha de lectura (2026-11-18).
**Home:** `/Users/gonzoblasco/.openclaw/workspace/agents/kanam-mind/out/memoria-oral-feasibility.md`
**Escrito:** 2026-11-18
**Alcance:** diseño, no submission. El plazo real del hackathon (26–31 oct 2026) ya pasó; esto sirve como decisión de "¿lo construimos igual?".

---

## Veredicto: **GO CON CAMBIOS**

`[inf]` El concepto es técnicamente sólido y casi todos sus números son mejores de lo que el pitch asume. **Pero tiene tres cambios no negociables**, uno de los cuales es de naturaleza ética, no técnica, y decide si el post se puede publicar:

1. **El eje no es "transcribir", es "cómo preguntar".** STT local en 2026 es un problema resuelto: en esta misma M4, un modelo de 547 MB transcribe español rioplatense sintético **palabra por palabra perfecto a ~4,8× tiempo real**. Transcribir ya no es el proyecto; es una dependencia de 20 líneas.
2. **Cambiar el público objetivo del pitch.** "Entrevistar a familiares mayores para preservar su historia" es un gesto con consentimiento, no un hack. Un post de Halloween/Día de Muertos que *graba a gente sin que sepa bien qué pasará con su voz* —aunque sea offline— es un post que envejece mal. El giro respetuoso se explica en §7 y es lo que hace que el resto se sostenga.
3. **Fijar el modelo por licencia, no por calidad.** Casi toda la familia NVIDIA que parecía "la opción open" tiene trampa de licencia, y hay una trampa exacta del tipo que ya nos mordió: `canary-1b` es **CC-BY-NC-4.0** y `canary-1b-v2` es **CC-BY-4.0**. Mismo nombre de familia, licencia distinta. Detalle en §2.

`[inf]` El resto es ejecutable en 48–72 h con stack mínimo (§5). El riesgo principal no es técnico sino de **expectativa**: el agente que "entrevista" hoy produce preguntas buenas pero genéricas, y hay que diseñar el post para que eso sea un rasgo, no una falla (§3).

---

## 1. STT local en 2026: estado real de la familia Whisper

### 1.1 Whisper (OpenAI) — código y pesos tienen licencias distintas

`[obs]` El **código** de `openai/whisper` es **MIT** — source: https://github.com/openai/whisper/blob/main/LICENSE (abierto 2026-11-18).
`[obs]` Los **pesos** varían por modelo. Consultados vía API de Hugging Face el 2026-11-18 (campo `cardData.license`):

| Modelo | Params | Licencia pesos | Fuente |
|---|---|---|---|
| `whisper-tiny` | 39 M | **Apache-2.0** | https://huggingface.co/api/models/openai/whisper-tiny |
| `whisper-base` | 74 M | Apache-2.0 | idem vía API |
| `whisper-small` | 244 M | Apache-2.0 | idem vía API |
| `whisper-medium` | 769 M | **Apache-2.0** | https://huggingface.co/api/models/openai/whisper-medium |
| `whisper-large-v2` | 1550 M | **Apache-2.0** | https://huggingface.co/api/models/openai/whisper-large-v2 |
| `whisper-large-v3` | 1550 M | **Apache-2.0** | https://huggingface.co/api/models/openai/whisper-large-v3 |
| **`whisper-large-v3-turbo`** | 809 M | **MIT** | https://huggingface.co/api/models/openai/whisper-large-v3-turbo |

**Este es el punto que hay que no equivocar.** El README del repo lista seis tamaños (tiny→large) y **turbo lo agrega aparte**, como "una versión optimizada de large-v3 con degradación mínima de accuracy". `[obs]` — source: https://github.com/openai/whisper (abierto 2026-11-18). Los tamaños y requisitos de VRAM están ahí mismo:

| Tamaño | Params | VRAM aprox. | Velocidad rel. |
|---|---|---|---|
| tiny | 39 M | ~1 GB | ~10× |
| base | 74 M | ~1 GB | ~7× |
| small | 244 M | ~2 GB | ~4× |
| medium | 769 M | ~5 GB | ~2× |
| large | 1550 M | ~10 GB | 1× |
| **turbo** | **809 M** | **~6 GB** | **~8×** |

`[obs]` turbo es large-v3 con las capas de decodificación reducidas de 32 a 4 — source: https://huggingface.co/openai/whisper-large-v3-turbo (abierto 2026-11-18).

`[inf]` **La buena noticia de licencias:** turbo es el mejor balance velocidad/calidad *y* es MIT, la licencia más permisiva de la familia. No hay que hacer un trade-off entre "el modelo bueno" y "la licencia limpia". Para un proyecto open-source de hackathon, **turbo es la elección obvia y no requiere justificación**.

### 1.2 Runtimes: whisper.cpp vs faster-whisper

`[obs]` **whisper.cpp** (`ggml-org/whisper.cpp`) — **MIT**, 55.292 estrellas, último push 2026-11-18, última release **v1.9.5 (2026-10-06)**. — sources: https://api.github.com/repos/ggml-org/whisper.cpp y https://github.com/ggml-org/whisper.cpp/releases/latest (abiertos 2026-11-18). Se autodescribe como "Apple Silicon first-class citizen — optimizado vía ARM NEON, Accelerate framework, Metal y Core ML".
`[obs]` Plataformas soportadas por whisper.cpp: macOS (Intel y Arm), **iOS**, **Android**, Java, Linux, WebAssembly, Windows, Raspberry Pi. Existen ejemplos reales `whisper.objc`, `whisper.android` y `whisper.android.java` en `examples/` — verificado por listado de directorio de la API de GitHub (2026-11-18).

`[obs]` **faster-whisper** (`SYSTRAN/faster-whisper`) — **MIT**, 26.849 estrellas, último push 2026-11-12, última release **v1.2.1 (2025-10-31)** — sources: https://api.github.com/repos/SYSTRAN/faster-whisper y https://api.github.com/repos/SYSTRAN/faster-whisper/releases/latest (abiertos 2026-11-18).

`[inf]` Para este proyecto **whisper.cpp gana**, no por calidad sino por *alcance*: el mismo binario corre en la Mac del usuario y en un iPhone/Android con un ejemplo oficial. faster-whisper depende de CTranslate2 y su historia móvil es mucho más débil. Si el pitch dice "en la máquina del usuario", whisper.cpp es la única opción que además permite decir "o en el teléfono".

`[obs]` whisper.cpp incluye **turbo** en su lista oficial de modelos descargables: `large-v3-turbo` (1,5 GiB) y **`large-v3-turbo-q5_0` (547 MiB)** — source: https://raw.githubusercontent.com/ggml-org/whisper.cpp/master/models/README.md (abierto 2026-11-18).

### 1.3 Medición propia (no de blog): M4, 24 GB, macOS 27.3

`[obs]` No confié en benchmarks ajenos — corrí los modelos en esta máquina. Audio de prueba: 10,94 s de español rioplatense sintetizado con `say -v Paulina`, normalizado a 16 kHz mono WAV. Frase: *"Mi abuela nació en 1938 en un pueblo chico de la provincia de Buenos Aires. Cuando era chica, el tren pasaba una sola vez por semana y traía el correo."*

| Modelo (ggml) | Disco | Tiempo total | ×tiempo real | Transcripción |
|---|---|---|---|---|
| small | 465 MB | 0,95 s | ~11,5× | **exacta** |
| medium | 1,4 GB | 2,38 s | ~4,6× | **exacta** |
| large-v3-turbo-q5_0 | 547 MB | 2,28 s | **~4,8×** | **exacta** |

`[obs]` **Medición propia, 2026-11-18**, con `whisper-cli` 1.9.5 (Homebrew) y Metal habilitado. Las tres transcripciones coincidieron palabra por palabra con el texto fuente, incluidos "1938", "Buenos Aires" y "traía".

`[inf]` Dos conclusiones de esta tabla, y la segunda es la importante:
- `[inf]` El hardware no es el cuello de botella. Una entrevista de 90 minutos se transcribe en **~19 min con small** o **~19 min con turbo q5**.
- **small empató con medium en este pasaje.** Una muestra de 11 s no prueba calidad general — `[unk]` si small degrada en audio real de personas mayores (voz temblorosa, ruido de cocina, risas, dialecto marcado). Pero alcanza para descartar la premisa del pitch de que hace falta un modelo grande.

`[unk]` Este test es **voz sintética, sin acento real ni ruido de fondo**. Es el límite más serio de esta evidencia. Lo que lo saldaría: 20–30 min de audio real de un hablante rioplatense mayor, comparados a mano contra el transcript. Es un requisito de la fase de campo (§6), no del diseño.

### 1.4 Español rioplatense: hay opciones, y una es local

`[obs]` **`marianbasti/whisper-large-v3-turbo-latam`** — **MIT**, fine-tune continuado de `whisper-large-v3-turbo` sobre Common Voice 17.0, subconjunto `es`, **filtrando acentos de España** para mejorar acentos latinoamericanos. Entrenado con cómputo del **CITECCA, Universidad Nacional de Río Negro, Argentina**. — source: https://huggingface.co/marianbasti/whisper-large-v3-turbo-latam (abierto 2026-11-18)

`[obs]` La model card reporta su propia evaluación sobre 3.952 muestras del split de evaluación de CV17-es:

| Métrica | Base `whisper-large-v3-turbo` | Fine-tune latam |
|---|---|---|
| WER | **15,44 %** | **7,80 %** |
| Inferencia por muestra | 0,56 s | 0,34 s (1,62× más rápido) |

`[obs]` Ambas cifras de la misma fuente: https://huggingface.co/marianbasti/whisper-large-v3-turbo-latam (abierto 2026-11-18).

`[inf]` Ese salto de WER es enorme y **el detalle que vende el post**: la mitad del error venía de un sesgo hacia el español peninsular. Y el trabajo se hizo con cómputo de una universidad pública Argentina. Es el dato más local y más narrativo de todo el brief — y es verificable en una model card pública, no un claim nuestro.
`[inf]` Advertencia metodológica: es una **autoevaluación del autor del fine-tune**, no un benchmark independiente. Tratar el 7,80 % como "evidencia prometedora", no como "medido por terceros".

`[obs]` Existe también `adriszmar/whisper-large-v3-turbo-es` (**MIT**) con WER 6,91 % → 5,34 % sobre CV17-es, pero sin filtrado regional. — source: https://huggingface.co/adriszmar/whisper-large-v3-turbo-es (abierto 2026-11-18)

`[inf]` **Trampa de portabilidad:** estos fine-tunes están publicados en formato `transformers`, no en ggml. Para usarlos con whisper.cpp hay que convertirlos (`convert-h5-to-ggml.py` en el repo) o correrlos con Transformers en Python, que en Mac es más lento y pesado. Para 48–72 h, la ruta realista es **turbo en ggml para el demo, y el fine-tune latam como "next step" documentado**. Prometer el fine-tune en el demo es prometer una conversión que puede comerse medio día.

`[unk]` No hay evidencia específica de calidad sobre **voseo, lunfardo o español rioplatense de personas mayores**. Busqué y encontré trabajo sobre *dialect classification* (`tiantiaf/voxlect-spanish-dialect-whisper-large-v3`) pero no benchmarks de WER rioplatense publicados. Lo saldaría: el mismo audio real de la fase de campo del párrafo anterior.

---

## 2. Alternativas: NVIDIA, Vosk, Wav2Vec2

`[inf]` Esta sección es la que justifica la advertencia de "cuidado con las licencias". Las trampas están todas acá.

### 2.1 Tabla de licencias verificada vía API de HF (2026-11-18)

| Modelo | Licencia real | Idiomas | ¿Sirve? |
|---|---|---|---|
| `nvidia/parakeet-tdt-0.6b-v2` | **CC-BY-4.0** | **solo EN** | ❌ no es español |
| `nvidia/parakeet-tdt-0.6b-v3` | **CC-BY-4.0** | 25 idiomas **incl. es** | ⚠️ ver abajo |
| `nvidia/parakeet-ctc-0.6b` | CC-BY-4.0 | EN | ❌ |
| `nvidia/canary-1b` | **CC-BY-NC-4.0** | EN/DE/ES/FR | ❌ **NC = no comercial** |
| `nvidia/canary-1b-v2` | **CC-BY-4.0** | 25 idiomas incl. es | ⚠️ |
| `nvidia/canary-1b-flash` | **CC-BY-4.0** | EN/DE/ES/FR | ⚠️ |
| `nvidia/canary-180m-flash` | **CC-BY-4.0** | EN/DE/ES/FR | ⚠️ |
| `alphacep/vosk-model-small-es-0.42` | **Apache-2.0** | es | ✅ **39 MB** |
| `alphacep/vosk-model-es-0.42` | **Apache-2.0** | es | ✅ 1,4 GB |
| `jonatasgrosman/wav2vec2-large-xlsr-53-spanish` | **Apache-2.0** | es | ✅ ver abajo |

`[obs]` Fuentes: campos `cardData.license` y `language` de `https://huggingface.co/api/models/<id>`, consultados 2026-11-18; Vosk desde https://alphacephei.com/vosk/models (abierto 2026-11-18).

### 2.2 Las dos trampas exactas

**Trampa 1 — `canary-1b` vs `canary-1b-v2`.** `[obs]` `canary-1b` es **CC-BY-NC-4.0**; `canary-1b-v2` y las variantes `flash` son **CC-BY-4.0**. Misma familia, un sufijo de diferencia, y una prohíbe uso comercial. Exactamente el patrón de error que ya nos pasó. Para este proyecto (open source, sin venta) NC *tal vez* alcanzaría, pero mete una ambigüedad legal que no vale la pena explicar en un post técnico. **Regla: citar siempre la versión exacta con su licencia al lado.**

**Trampa 2 — Parakeet "v2" no es el multilingüe.** `[obs]` `parakeet-tdt-0.6b-v2` tiene `language: ['en']` — es **inglés únicamente**. El multilingüe con español es **`v3`**. Un post que diga "Parakeet, 0.6B, excelente y rápido" sin la versión está afirmando algo falso sobre español. — source: API HF, campo `language`, 2026-11-18.

### 2.3 ¿Y entonces, por qué no Parakeet/Canary?

`[obs]` `parakeet-tdt-0.6b-v3` publica `parakeet-tdt-0.6b-v3.q8_0.gguf` además de `.nemo` y `.safetensors` — verificado por listado de archivos de la API de HF (2026-11-18). Existe ruta ggml.
`[inf]` Pero ese gguf está pensado para llama.cpp/whisper.cpp-style tooling de NVIDIA, **no está soportado por `whisper-cli` de whisper.cpp**, que solo carga la arquitectura Whisper. Correr Parakeet en 48 h implica integrar otro runtime. Es el tipo de "se ve fácil, no lo es" que hunde un hackathon.
`[inf]` Además: CC-BY-4.0 obliga a **atribuir** en el artefacto. Whisper turbo (MIT) no obliga a nada. Para un demo con UI, la diferencia es "una línea en el README" vs "un aviso de atribución visible".

### 2.4 Vosk: la opción de teléfono

`[obs]` Vosk API es **Apache-2.0** (15.274 estrellas, push 2026-10-15); `vosk-android-demo` es Apache-2.0. Los modelos español son Apache-2.0: `small-es-0.42` pesa **39 MB**, WER reportado **16,02 % (CV test)**; `es-0.42` pesa 1,4 GB, WER 7,50 % — sources: https://api.github.com/repos/alphacep/vosk-api y https://alphacephei.com/vosk/models (abiertos 2026-11-18).

`[inf]` 39 MB con WER ~16 % es un trade-off honesto para tiempo real en un teléfono viejo. Pero 16 % de WER en una transcripción con nombres propios y fechas es **inservible para historia oral**: "1938" mal transcrito arruina la entrevista. `[inf]` **Vosk sirve como demo de "esto corre hasta en un teléfono", no como motor principal.** Buen lugar para una nota al pie que muestra rigor.

### 2.5 Wav2Vec2

`[obs]` `jonatasgrosman/wav2vec2-large-xlsr-53-spanish` es **Apache-2.0** (API HF, 2026-11-18).
`[inf]` Wav2Vec2 es CTC puro: no puntúa, no maneja cortes de audio largos ni puntuación. Sobre entrevistas de una hora es mucho más trabajo de ingeniería que Whisper, para peor texto. **Descartar** — pero mencionarlo una línea en el post demuestra que se evaluó.

---

## 3. El giro "entrevista": ¿hace falta un LLM grande?

### 3.1 Medición propia (esta es la evidencia más valiosa del brief)

`[obs]` Corrí dos modelos locales contra el mismo prompt: recibir el transcript de arriba, detectar **un** hueco y hacer **una** pregunta de seguimiento, cálida, ≤30 palabras, en español rioplatense.

| Modelo | Tamaño | Tiempo | Salida |
|---|---|---|---|
| `gemma3:4b` | 3,4 GB | **3,81 s** / 25 tok | *"¿Y qué sentías, vos, cuando el tren llegaba y venías a ver a la abuela?"* |
| `gemma4:12b-mlx` | 7,7 GB | 6,58 s / 23 tok | *"¿Y qué era lo que más te gustaba del olor o del sonido del tren cuando llegaba al pueblo?"* |

`[obs]` **Medición propia, 2026-11-18**, Ollama, M4 24 GB, `num_ctx: 2048`, `temperature: 0.7`, `think: false`. Salidas literales, sin editar.

`[inf]` **La respuesta al pedido es que no hace falta un LLM grande.** El 4B produjo una pregunta mejor que el 12B: detectó el hueco real (la abuela aparece y desaparece en un párrafo) y usó voseo correcto ("vos", "venías") sin que se lo pidieran con un ejemplo. El 12B hizo algo más literario y más genérico. Para esta tarea, **la calidad satura muy temprano**.

`[inf]` Pero hay un límite y hay que decirlo: **las dos preguntas son buenas y las dos son genéricas**. Ninguna pregunta por "¿y quién más vivía en esa casa?" ni por "¿qué pasó con el correo?". Ninguna *sabe* qué falta. Un agente que entrevista de verdad necesita algo que la prueba no cubre: **una estructura de qué preguntar** (etapas de vida, personas, lugares) contra la que comparar el relato.

`[inf]` **Es el diseño central del proyecto, y no es un modelo — es un prompt con memoria.** El enfoque defendible: un checklist de cobertura (nacimiento → infancia → trabajo → amores → pérdidas) + el transcript, y pedirle al modelo que marque qué ítems están vacíos y elija uno. Eso convierte "hacer una pregunta" en "cerrar un hueco declarado", que es lo que el pitch promete. Es la diferencia entre un demo que impresiona y uno que parece que no piensa.

`[unk]` No encontré evidencia publicada de calidad de *follow-up questioning* de historia oral con modelos chicos. Lo saldaría: 20 entrevistas de prueba con el checklist y evaluar a mano si la pregunta era pertinente. Es trabajo de una tarde y sería **la sección más original del post** — nadie publica eso.

`[obs]` El contexto de Ollama importa: con el default de qwen3.5:9b (262.144 tokens de contexto) el modelo se arrastraba y hubo dos timeouts; con `num_ctx: 2048` el mismo tipo de tarea respondió en segundos. `[inf]` **Detalle de ingeniería que vale documentar**: en una app local, el contexto por defecto de una herramienta puede costar más que el modelo.

### 3.2 Qué modelo elegir

`[inf]` `gemma3:4b` (3,4 GB, ya instalado acá) es el candidato: calidad saturada en esta tarea, corre en GPU en 4 s, deja RAM libre para Whisper. Verificar su licencia **para el post** antes de publicar — no la verifiqué como parte de este brief y no la voy a afirmar sin abrirla. `[unk]` Licencia exacta de `gemma3:4b` en su versión Ollama: requiere abrir la card.

---

## 4. Privacidad verificable

### 4.1 Cómo se demuestra (medido acá)

`[obs]` **Experimento propio, 2026-11-18:** lancé `whisper-cli` sobre el audio de prueba y muestreé sus sockets con `lsof -nP -a -p <pid> -i` durante toda la vida del proceso. **45 muestras tomadas, 0 sockets de red.** — comando reproducible:
```
whisper-cli -m ggml-small.bin -f audio.wav -l es &
lsof -nP -a -p $! -i
```
`[obs]` En la misma máquina, `ollama` escucha en **127.0.0.1 únicamente** (`TCP 127.0.0.1:11434 (LISTEN)`), verificado con `lsof -nP -iTCP -sTCP:LISTEN` (2026-11-18).

`[inf]` Esto es una demostración **reproducible**, y es la que va al post. Pero hay que ser preciso sobre qué prueba: prueba que **el proceso no abrió sockets**, no que "nada se subió". La demostración fuerte es **triple**, y el post debería hacer las tres:

1. **Proceso sin sockets** (`lsof -a -p $PID -i`) — lo de arriba. Prueba directa.
2. **Modo offline real**: correr con la interfaz de red caída o en un perfil sin red. Si funciona igual, no dependió de la red. Es la prueba más difícil de discutir.
3. **Firewall saliente** (`socketfilterfw`) o `tcpdump` para mostrar que no hay tráfico durante la sesión.

`[inf]` **La trampa a evitar:** `netstat`/`lsof` muestran *tu* máquina en *tu* momento. No prueban nada sobre el binario que descargó el usuario. El post debe encuadrarse como "esto es reproducible en 3 comandos", no como "confía en que no se conecta". Un screenshot de netstat es evidencia débil; un comando que el lector corre es evidencia fuerte. `[obs]` Nota de entorno: en esta máquina el Application Firewall de macOS está **deshabilitado** (`State = 0`), así que el firewall no es una prueba disponible por defecto — otro motivo para preferir 1 y 2.

### 4.2 Qué hacen las alternativas comerciales

`[obs]` Otter.ai publica su lista de subprocesadores: **Amazon Web Services (EE.UU.)** como "cloud service provider and customer data storage platform", más **Anthropic** ("backend support of AI-enabled functionality") y **OpenAI** ("evaluating the effectiveness of our LLMs"). Página con fecha effective 31 de marzo de 2026. — source: https://otter.ai/subprocessors (abierto 2026-11-18)
`[obs]` El propio aviso de Otter aclara que para Anthropic y OpenAI "No Customer Data will be used to train or improve" sus modelos y que no almacenan los datos vía API — es decir, **el dato sí viaja**. — misma fuente.

`[inf]` **Este es el contraste que sostiene el post, y hay que hacerlo con cuidado.** No es "Otter es malo": es que Otter es un servicio en la nube, y la nube implica que la voz de la abuela atraviesa AWS en EE.UU. y llega a dos proveedores de IA más. Para una reunión de trabajo es razonable. Para la voz de una persona de 90 años que no puede volver a grabarse, es una decisión distinta. **El argumento es de stakes, no de moral.** Escribirlo así es lo que evita que el post suene a marketing.

`[unk]` Política exacta de retención y borrado de audio de Otter: la página de subprocesadores no la detalla y no abrí la política completa. No afirmar cifras de retención sin abrirla.

---

## 5. Stack mínimo para 48–72 h

`[inf]` Cada componente de abajo ya existe, está medido acá o es MIT/Apache-2.0. La regla es **cero dependencias nuevas que no se hayan probado**.

| Capa | Elección | Por qué |
|---|---|---|
| Lenguaje | **Python 3.11+** | whisper.cpp se llama por CLI o binding; el ecosistema audio es Python |
| STT | **whisper.cpp v1.9.5**, `ggml-large-v3-turbo-q5_0` (547 MB) | MIT, 4,8× tiempo real medido, corre en Mac y teléfono |
| LLM | **Ollama + gemma3:4b** (verificar licencia) | 3,8 s por pregunta medido, ya instalado |
| Orquestación | Script Python: audio → transcript → checklist de huecos → pregunta | Sin framework de agentes: es un loop, no un grafo |
| Almacenamiento | **SQLite + FTS5** (reuso del motor RAG previo) | Ya construido; FTS5 alcanza para buscar en transcripts |
| Vectores | `sqlite-vec` (Apache-2.0, push 2026-05-18) | Ya en el motor previo; opcional para "buscar por significado" |
| UI | **Terminal o un HTML local servido en 127.0.0.1** | Evitar Electron/Tauri en 72 h |
| Export | Markdown + el audio original intacto | Formato durable, sin dependencia de la app |

`[inf]` **El reuso del motor RAG es válido y es el atajo más grande.** Cambia "PDF → chunks" por "audio → segmentos con timestamps". FTS5 da búsqueda exacta ("¿en qué entrevista se menciona el tren?"). `sqlite-vec` da búsqueda por significado. **La diferencia con el proyecto previo es que acá cada respuesta tiene un timestamp de audio, no un número de página** — y eso es una mejora: se puede hacer clic y escuchar la voz. Ese detalle, "la cita te devuelve la voz", es el mejor momento del demo.

`[inf]` **Lo que hay que cortar del alcance para que entre en 72 h:**
- Diarización (speaker labels) → **fuera**. `pyannote/speaker-diarization-3.1` es MIT pero **gated** (requiere aceptar términos y token de HF — verificado 2026-11-18). En un hackathon, un gate de HF es un paso donde el demo se rompe en vivo. `[inf]` Alternativa honesta para el post: "un botón para marcar quién habla".
- `[inf]` App móvil → **fuera**. Demostrar whisper.cpp corriendo en teléfono como captura de pantalla, no como app.
- `[inf]` Fine-tune latam → **fuera del demo**, documentado como siguiente paso (§1.4).

---

## 6. Tres riesgos técnicos principales y mitigación

**R1 — El audio real es mucho peor que el sintético.** *Probabilidad: alta. Impacto: alto.*
`[inf]` Mi medición usó voz sintética limpia. Personas mayores reales traen voz temblorosa, ruido de cocina, risas, dialecto marcado, nombres propios y fechas.
`[inf]` Mitigación: (a) **medir antes de prometer** — 20–30 min de audio real como tarea del día 1, no del día 3; (b) VAD de whisper.cpp para cortar silencios (la doc lo lista como feature); (c) `--prompt` con nombres propios y topónimos de la familia como sesgo léxico; (d) aceptar y mostrar correcciones manuales en la UI — un transcript editable es más honesto que uno "perfecto".

**R2 — El agente entrevistador suena genérico.** *Probabilidad: alta (ya lo observé). Impacto: medio — es el corazón del pitch.*
`[inf]` Las preguntas de §3 son buenas pero no *informadas*. Si el demo muestra tres preguntas seguidas que podrían haberse hecho sin escuchar, el post pierde su tesis.
`[inf]` Mitigación: el **checklist de cobertura explícito** (§3.1) como estructura del prompt; mostrar la UI el hueco detectado ("falta: infancia / trabajo") junto con la pregunta; y limitar el demo a **una** pregunta por turno — una buena vale más que cinco mediocres.

**R3 — La licencia o el gate te muerde el día del demo.** *Probabilidad: media. Impacto: alto.*
`[obs]` Ya hay tres trampas identificadas: `canary-1b` (NC) vs `canary-1b-v2` (BY), `parakeet-v2` (solo EN) vs `v3`, y `pyannote-3.1` **gated**.
`[inf]` Mitigación: **todo el stack del demo en MIT/Apache-2.0 sin gates** (whisper.cpp MIT, turbo MIT, llama.cpp MIT, SQLite dominio público, FTS5 en SQLite). Descargar todos los modelos **el día 1** y dejarlos en disco; nunca descargar modelos en vivo. Y una tabla de licencias **en el README** con versión exacta al lado — que además es una sección que hace el post más creíble.

---

## 7. Evidencia de campo que haría el post convincente y respetuoso

`[inf]` Esta es la sección que decide si el post se puede publicar. El tema (Halloween + Día de Muertos) empuja hacia lo espeluznante, y el material es íntimo. **El registro correcto no es "mira qué lindo la IA revive a tu abuela"** — eso es exactamente lo que envejece mal y lo que ofende.

**Lo que hace convincente (evidencia):**
1. **Una entrevista real, con permiso, y el audio real.** El momento más fuerte del post es escuchar 10 segundos de una voz real y ver el transcript alineado con el audio. Sin voz real, es un demo.
2. **La comparación de WER antes/después del fine-tune latam** (§1.4): "el modelo genérico se equivocaba en una de cada seis palabras; con acento local, en una de cada trece". Es un número, es verificable, y es local.
3. **Los tres comandos de privacidad** (§4.1) corridos en vivo, con la salida pegada.

**Lo que lo hace respetuoso — y son condiciones, no adornos:**
1. **Consentimiento explícito y explicado.** La persona mayor tiene que saber: qué se graba, dónde queda, quién lo puede escuchar, y cómo se borra. En el post, esto va **antes** del código, no como letra chica.
2. **La persona es autora, no sujeto.** El export incluye el nombre y, si quiere, sus condiciones de uso. La familia no decide por ella.
3. **La privacidad es el punto, no el truco técnico.** El argumento correcto: *una voz es irrecuperable; si se filtra, no se puede cambiar como una contraseña.* Eso justifica el offline mucho mejor que "mirá, no usa internet".
4. **Nombrar el límite.** Un agente que pregunta no reemplaza a un nieto que pregunta. Decirlo explícitamente protege el post de la crítica más obvia y es más honesto que el pitch original.
5. **No inventar voces.** Si en algún momento el demo sintetiza o "continúa" la voz de alguien fallecido, eso es otro proyecto y otro consentimiento. Mantenerlo fuera.

`[unk]` No verifiqué las guías éticas de StoryCorps más allá de abrir su home (bloqueado por scripts). Si el post las cita, hay que abrirlas primero. No citar "StoryCorps recomienda X" sin haberlo leído.

---

## Conflictos y advertencias

- **`canary-1b` (CC-BY-NC-4.0) vs `canary-1b-v2` (CC-BY-4.0)** — mismo nombre, licencia distinta. Impacto: cualquier afirmación sobre "Canary" sin versión es ambigua o falsa.
- **`parakeet-tdt-0.6b-v2` (solo EN) vs `v3` (25 idiomas con es)** — impacto: el pitch de "Parakeet como alternativa" es falso si se cita v2.
- **Whisper código MIT vs pesos Apache-2.0** — impacto: al citar la licencia de Whisper hay que decir *cuál* (código o pesos) y *qué versión*.
- **Benchmark latam es autoevaluación** — impacto: el 7,80 % no es un resultado independiente; presentarlo como tal sería un `[inf]` disfrazado de `[obs]`.

---

## Pendiente

1. `[unk]` **Licencia exacta de `gemma3:4b`** en su tag de Ollama — abrir la card antes de publicar.
2. `[unk]` **Audio real**: 20–30 min de voz rioplatense mayor para medir WER verdadero (voz sintética no alcanza).
3. `[unk]` **Retención/borrado de audio en Otter** — no verificado.
4. `[unk]` **Guías de StoryCorps** — no abiertas; no citar sin leer.
5. **Decisión de aprobación:** el cambio de encuadre de §7 (consentimiento primero, persona como autora) y el recorte de alcance de §5 requieren OK antes de escribir el post. No es una recomendación técnica, es una decisión sobre un tema íntimo.
