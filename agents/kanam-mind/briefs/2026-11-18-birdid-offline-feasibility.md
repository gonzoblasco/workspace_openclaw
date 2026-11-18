---
title: "Viabilidad: cuaderno de campo automático con ID de cantos offline"
date: 2026-11-18
author: kanam-mind
requester: CORE (webchat)
status: delivered
question: "¿Puede un MVP de 48-72 h identificar cantos de aves offline en un teléfono y armar una entrada de diario naturalista, con IA open-source no decorativa?"
verdict: GO CON CAMBIOS
---

# Brief de viabilidad — "Field Notebook" (DEV.to Hacktoberfest W1 "Touch Grass")

Contexto fijo verificado por CORE: challenge cerrado 5-11 oct 2026; hoy 18 nov 2026, así que es un ejercicio de diseño y no una submission. Requisitos: open-weight / open-source / inferencia local, proyecto nuevo, post en inglés, demo. [obs]

## Veredicto: GO CON CAMBIOS

El núcleo (canto → especie, offline, on-device) es viable con evidencia dura. El giro del cuaderno de campo solo se sostiene si el componente de visión deja de ser un identificador de plantas y pasa a ser un redactor de la entrada, o se corta del MVP. [inf]

## 1. Respuesta corta

| Pregunta | Respuesta | Confianza |
|---|---|---|
| ¿Corre BirdNET en un teléfono, offline? | Sí. BirdNET Live hace inferencia on-device con ONNX Runtime; ~84× tiempo real medido en Pixel 10 Pro | Alta (medido por terceros) |
| ¿En un fin de semana? | Solo si se forkea BirdNET Live o se usa la app tal cual. Un cliente nuevo desde cero: no | Alta |
| ¿Modelo open-source? | Sí, pero la versión importa: V3.0 (nov 2026) es Apache-2.0; V2.4 arrastra CC BY-NC-SA 4.0 | Alta |
| ¿Visión complementaria viable en 48-72 h? | No como identificador fiable. Qwen3-VL-2B entra en un teléfono, pero identificar plantas desde una foto es un problema sin resolver | Media |
| ¿El giro es diferenciador? | Sí, si el diario se genera y no se rellena a mano | Media (juicio) |

## 2. Estado real de BirdNET en noviembre de 2026

Hay dos cosas llamadas BirdNET y la distinción decide el proyecto. [obs]

BirdNET V2.4 (jun 2023) es el modelo que CORE verificó: más de 6,000 especies, 6,522 clases (incluye 11 no-especie), 0.826 GFLOPs, 50.5 MB FP32, backbone tipo EfficientNet-B0, embedding 1024. Fuente: https://birdnet-team.github.io/birdnet/models.html (leído 2026-11-18). [obs]

Pesos V2.4 en Zenodo con exportaciones TFLite: FP32 76.8 MB, FP16 53.0 MB, INT8 45.9 MB; también TF.js 75.0 MB. Fuente: https://zenodo.org/records/15050749 (intentado 2026-11-18; el gate devolvió HTTP 500 en la reverificación, ver §10). [obs]

BirdNET+ V3.0 se publicó el 13 nov 2026, o sea cinco semanas después del challenge. Existió una V3 y no es la que CORE verificó. Fuente: https://zenodo.org/records/24162518. [obs]

V3.0 cubre 11,709 especies animales (9,788 aves) más 16 clases no-animales, 11,725 clases, embedding 1280 y entrada de 32 kHz. Fuente: https://zenodo.org/records/24162518 y https://birdnet-team.github.io/birdnet/models.html (leído 2026-11-18). [obs]

Exportaciones V3.0: TorchScript, ONNX (FP32 345 MB / FP16 173 MB), TFLite (FP32 344 MB / FP16 172 MB), SavedModel, Core ML para iOS 16+/macOS 13+, y variantes pruned de ~69-72 MB para móvil y edge. Fuente: https://zenodo.org/records/24162518. [obs]

La licencia de los pesos V3.0 es Apache 2.0, con un ACCEPTABLE_USE.txt aparte que debe leerse antes de usar. Fuente: https://zenodo.org/records/24162518 (descripción) y https://birdnet-team.github.io/birdnet/models.html §V3.0. [obs]

La precisión declarada de V3.0 en WABAD es AP 0.552 contra 0.272 de V2.4 sobre las ~1,000 especies que ambos predicen. Fuente: https://zenodo.org/records/24162518. No verifiqué WABAD de forma independiente. [obs]

Hallazgo que corrige el contexto de CORE: el "Apache-2.0 para los modelos" es cierto para V3.0 y para el paquete `birdnet` (MIT), pero el linaje histórico de V2.4 y BirdNET-Lite arrastra CC BY-NC-SA 4.0, anunciado por el mantenedor de BirdNET-Pi en 2021. Fuente: https://github.com/mcguirepr89/BirdNET-system/discussions/33 y https://github.com/birdnet-team/BirdNET-Lite (repo archivado). [obs]

Para un post que dice "open-source" hay que citar V3.0 y no V2.4, porque la licencia NC contradice el requisito del challenge. [inf]

No pude abrir el MODEL_LICENSE.txt ni el ACCEPTABLE_USE.txt de V3.0 (timeout), así que la afirmación Apache-2.0 se apoya en dos páginas del propio proyecto y no en el archivo de licencia. [unk]

## 3. Correr BirdNET en un teléfono: opciones reales

| Opción | Qué es | Viabilidad 48-72 h |
|---|---|---|
| BirdNET Live (Flutter + flutter_onnxruntime) | App completa: modo en vivo, point count, survey con GPS, export Raven/CSV/JSON/GPX/ZIP, offline total | Alta como base o como app a forkear (https://birdnet-team.github.io/birdnet-live-app/) |
| ONNX Runtime Mobile (Android/iOS, NNAPI/CoreML/XNNPACK EPs) | Runtime, no app | Media-alta: el runtime está; el pipeline de captura es lo caro (https://onnxruntime.ai/docs/tutorials/mobile/) |
| Core ML (V3.0 .mlpackage) | Export oficial, iOS 16+, exactamente 3 s | Media: requiere Xcode y Swift, solo iOS |
| TFLite / LiteRT | Export oficial; más preciso en segmentos de 3 s | Media: buena en Android, pero implica escribir el glue nativo |
| birdnet-stm32 | Modelo chico para STM32N6570-DK: 1,007 especies, 2.5 s, 92 ms por archivo, ~78× tiempo real | Nula para teléfono: es firmware para placa con NPU (https://birdnet-team.github.io/birdnet-stm32/) |

La arquitectura de BirdNET Live, que hay que respetar o reusar, captura del micrófono (Oboe en Android, AVAudioEngine en iOS) a PCM16 32 kHz mono y lo escribe en un RingBuffer. Fuente: https://birdnet-team.github.io/birdnet-live-app/developer/audio-pipeline/. [obs]

La inferencia pasa por un ClassifierModel (sesión ONNX) con un InferenceService encima que aplica sensibilidad, pooling temporal y top-K, con suavizado Log-Mean-Exp (α=5.0, hasta 5 ventanas). Fuente: https://birdnet-team.github.io/birdnet-live-app/developer/inference-engine/. [obs]

El geo-model es un ONNX de ~8 MB con entrada [lat, lon, semana 1-48] que filtra por lugar y estación; esto es clave para el giro porque las coordenadas son una señal y no un adorno. Fuente: https://birdnet-team.github.io/birdnet-live-app/developer/inference-engine/. [obs]

El APK pesa ~320 MB porque incluye los modelos y las imágenes de todas las especies para uso offline. Fuente: https://birdnet-team.github.io/birdnet-live-app/ (leído 2026-11-18). [obs]

Rendimiento medido: en un Pixel 10 Pro con ORT 1.28, el modelo preview 3.1 pruned FP16 corrió a ~53× tiempo real, y con dos cambios de grafo (quitar el nodo STFT, fp16 solo en convoluciones) llegó a ~84× con idéntico top-1. Fuente: https://birdnet-team.github.io/birdnet-live-app/developer/model-export-checklist/ (leído 2026-11-18). [obs]

Un grafo INT8 con esos mismos cambios llegó a 108×, pero la cuantización post-entrenamiento sólo alcanza 0.77-0.89 de acuerdo top-1, así que requiere QAT. Fuente: misma página del checklist. [obs]

El V3.0 tiene la misma arquitectura que el modelo medido, pero el 84× no fue re-medido con V3.0 en un teléfono. Fuente: misma página del checklist. [obs]

Con 3 s de audio clasificados en decenas de ms, la latencia no es el riesgo del proyecto; el riesgo es el pipeline de captura y la UI. [inf]

## 4. Alternativas open-source

| Modelo | Especies | Arquitectura / tamaño | Licencia | ¿Móvil? |
|---|---|---|---|---|
| BirdNET+ V3.0 | 9,788 aves / 11,709 animales | 69 MB pruned FP16, ONNX/TFLite/CoreML | Apache 2.0 | Sí (pensado para mobile/edge) |
| Perch 2.0 (Google) | ~15,000 clases (~10,000 aves) | EfficientNet-B3, ~12M params más 91M en la cabeza; embeddings 1536-d; segmentos de 5 s a 32 kHz | Apache 2.0 (repo) | No práctico: el model card pide TensorFlow 2.20.rc0 y GPU |
| BEANS | Benchmark, no modelo | — | MIT (repo) / CC-BY-4.0 (paper) | N/A, es para evaluar |

Fuentes de Perch: https://huggingface.co/cgeorgiaw/Perch (leído 2026-11-18), https://github.com/google-research/perch/, https://arxiv.org/abs/2508.04665. Fuentes de BEANS: https://github.com/earthspecies/beans/, https://arxiv.org/abs/2210.12300. [obs]

Perch declara SOTA en BirdSet y BEANS según su propio model card, pero no es un modelo de bolsillo y no sirve para un MVP en teléfono. [inf]

BirdNET+ V3.0 es la única opción que combina licencia limpia, tamaño móvil y exportaciones oficiales; BEANS sí es útil para el post porque permite decir "medí con un benchmark público". [inf]

## 5. Modelo de visión complementario

| Modelo | Tamaño / despliegue | Licencia | Veredicto |
|---|---|---|---|
| Qwen3-VL-2B-Instruct | GGUF Q4_K_M más mmproj Q8_0 sobre llama.cpp; Arm publicó build optimizado para CPU móvil con SME2 | Apache 2.0 | Único candidato realista on-device |
| Gemma 3 4B-it | Imágenes a 896×896 → 256 tokens | Gemma Terms of Use | Pesado para un paseo; la licencia no es OSI |
| Gemma 3 270M | Texto; la variante chica no es de visión | Gemma Terms | No aplica a fotos |
| LLaVA | No verificado en esta ronda | — | Incógnita declarada |

Qwen3-VL-2B se ofrece en GGUF con LLM en FP16/Q8_0/Q4_K_M y vision encoder mmproj en FP16/Q8_0, compatible con llama.cpp. Fuente: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct-GGUF (leído 2026-11-18). [obs]

La licencia de Qwen3-VL-2B-Instruct es `license: apache-2.0` según el README del modelo base. Fuente: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct/blob/main/README.md. [obs]

Arm publicó un build de Qwen3-VL-2B con decodificador Q4_K_M y proyector Q8_0 para CPUs móviles con SME2. Fuente: https://huggingface.co/Arm/qwen3-vl-2b-instruct-q4-k-m-ggml-llama-cpp-vivo-x300. [obs]

Gemma 3 4B-it normaliza las imágenes a 896×896 y las codifica a 256 tokens cada una. Fuente: https://huggingface.co/google/gemma-3-4b-it (leído 2026-11-18). [obs]

Gemma 3 se rige por los Gemma Terms of Use, una licencia propia que no es OSI. Fuente: https://ai.google.dev/gemma/terms (leído 2026-11-18). [obs]

El model card de Qwen3-VL dice "reconoce flora/fauna", pero eso es una afirmación de capacidad general y no una medición de precisión en identificación de plantas; no encontré ninguna evaluación de Qwen3-VL-2B contra un dataset de flora. Fuente: https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct-GGUF. [unk]

Tratar "la IA de visión identifica la planta" como cierto sería un supuesto presentado como hecho, justo lo que un post de IA debería evitar. [inf]

## 6. Stack mínimo para 48-72 h

Lenguaje y UI: Flutter (Dart), porque es el stack de BirdNET Live, el código de referencia existe y es MIT, y un solo código cubre Android e iOS. Fuente: https://birdnet-team.github.io/birdnet-live-app/. [inf]

Inferencia: flutter_onnxruntime con BirdNET+ V3.0 `_FP16_pruned.onnx` (~72 MB), que evita el preprocesamiento manual porque el ONNX trae su propio front-end. Fuente del archivo: https://zenodo.org/records/24162518. [inf]

Audio: plugin de captura de BirdNET Live o `record`/`flutter_sound` a PCM16 32 kHz mono, con ring buffer de 3 s y 50 % de solape. La ventana exacta con solape de BirdNET Live es supuesto de diseño, no verificado. [unk]

Geo-filtro: geo-model V3.0 FP16 (~8 MB) con entrada [lat, lon, semana], que convierte "un pájaro" en "el pájaro que puede estar acá en noviembre". Fuente: https://birdnet-team.github.io/birdnet-live-app/developer/inference-engine/. [inf]

Coordenadas: `geolocator` con GPS y timestamp, sin red. [inf]

Visión: Qwen3-VL-2B Q4_K_M vía llama.cpp, opcional y detrás de un flag, usada para redactar la entrada y nunca para afirmar una especie vegetal. [inf]

Almacenamiento: SQLite (o `drift`) con una tabla `entries`, audio en FLAC local y export a Markdown/JSON, sin backend. [inf]

IA no decorativa, el argumento para el post: el clasificador acústico da la especie, el geo-model restringe el espacio de hipótesis por lugar y semana, y el LLM compone la prosa a partir de la foto más el contexto acústico ya inferido; quitar cualquiera de las tres degrada el producto visiblemente. [inf]

## 7. Los tres riesgos técnicos

R1, licencia equivocada en el modelo: copiar un tutorial de BirdNET-Lite o V2.4 arrastra CC BY-NC-SA 4.0 y contradice el requisito "open-source". Mitigación: fijar V3.0 desde Zenodo, leer ACCEPTABLE_USE.txt y declarar versión y licencia exactas en el post. [inf]

R2, la visión no cumple lo que promete el giro: identificar una planta desde una foto de teléfono es difícil incluso para modelos grandes, y un 2B cuantizado no lo resuelve. Mitigación: la foto no identifica, describe el hábitat y redacta. [inf]

R3, ruido de campo y falsos positivos: un paseo tiene viento, motos y humanos, y un demo con 3 falsos positivos mata el post. Mitigación: top-3 con confianza visible, umbral configurable y grabar el demo en un lugar con cantos claros. [inf]

Riesgo secundario: el APK de ~320 MB; se mitiga no distribuyendo APK y mostrando un build de desarrollo con el modelo pruned de ~72 MB. [inf]

## 8. Evidencia de campo que haría el post convincente

El post se gana o se pierde acá y no en el README. [inf]

1. Al menos 20 grabaciones reales de un mismo paseo, cada una con top-3 y confianza, guardando los WAV/FLAC. [inf]
2. Latencia medida y no estimada: ms por ventana de 3 s en ese teléfono, porque la cifra de 84× es de un Pixel 10 Pro con un modelo preview y no fue re-medida con V3.0. [obs]
3. Una comparación honesta de aciertos y fallos; un post que admite "confundió X con Y por el ruido del río" vale más que uno que declara 95 % sin metodología. [inf]
4. El geo-model haciendo su trabajo: mostrar una detección descartada porque la especie no está en esa semana ni coordenada, lo que demuestra que la IA no es decorativa. [inf]
5. El artefacto: una entrada de diario exportada con audio, hora, coordenadas, foto y texto, abrible sin la app. [inf]
6. Reproducibilidad: comando de build, versión del modelo y hash del archivo, para que un evaluador pueda repetirlo. [inf]

Correr BEANS (MIT) sobre una porción del test set convertiría "funciona" en "medido con benchmark público". Fuente: https://github.com/earthspecies/beans/. [inf]

## 9. Recomendación: GO CON CAMBIOS

GO al núcleo: BirdNET+ V3.0, offline, on-device, con geo-filtro; la evidencia de rendimiento es buena y la licencia es limpia si se usa V3.0. [inf]

Los cambios son tres y no son cosméticos. [inf]

1. Fijar V3.0 y no V2.4, porque el contexto de CORE mezcla el tamaño de V2.4 (50.5 MB) con la licencia de V3.0; en el post va V3.0, ~72 MB pruned FP16, Apache 2.0, publicado 13 nov 2026. [inf]
2. Cambiar el rol de la visión, de identificador de plantas (no defendible) a redactor de la entrada a partir de la foto y el contexto acústico (defendible y más interesante). [inf]
3. No construir la app desde cero: forkear BirdNET Live (MIT) o correr la app y construir el cuaderno encima, porque 48-72 h alcanzan para un cuaderno de campo y no para un cliente de audio, inferencia y UI desde cero. [inf]

Lo que haría el post distinto de "otra app de identificación" es que el diario se escribe solo: el usuario camina, graba, saca una foto, y al final del paseo tiene una entrada con fecha, lugar, especie inferida, estación del año y una prosa que cruza lo que oyó con lo que vio. [inf]

NO-GO solo a la variante "identificador de plantas con Qwen3-VL", porque no hay evidencia de precisión y el presupuesto no alcanza para producirla. [inf]

## 10. Incógnitas declaradas

No abrí MODEL_LICENSE.txt ni ACCEPTABLE_USE.txt de V3.0 por timeout; la licencia Apache-2.0 se apoya en la descripción y la doc del proyecto. [unk]

El 84× corresponde al modelo preview 3.1 y no a V3.0, y se midió en un Pixel 10 Pro; no es transferible sin medir. [unk]

El link https://zenodo.org/records/24162518 respondió ok al abrirlo (200, texto extraído), pero el gate lo marcó unknown por timeout en su propio chequeo. [unk]

El link https://zenodo.org/records/15050749 devolvió HTTP 500 al reverificarlo el gate, aunque la primera lectura devolvió 200 con el listado de archivos. [unk]

No verifiqué LLaVA en esta ronda. [unk]

La ventana exacta con solape de BirdNET Live es supuesto de diseño. [unk]

No verifiqué el APK de 320 MB contando archivos; la cifra viene de la página oficial. [unk]

## Fuentes consultadas (todas leídas 2026-11-18)

- https://birdnet-team.github.io/birdnet/models.html
- https://zenodo.org/records/24162518
- https://zenodo.org/records/15050749
- https://birdnet-team.github.io/birdnet-live-app/
- https://birdnet-team.github.io/birdnet-live-app/developer/inference-engine/
- https://birdnet-team.github.io/birdnet-live-app/developer/audio-pipeline/
- https://birdnet-team.github.io/birdnet-live-app/developer/model-export-checklist/
- https://birdnet-team.github.io/birdnet-stm32/
- https://github.com/birdnet-team/BirdNET-Lite
- https://github.com/mcguirepr89/BirdNET-system/discussions/33
- https://huggingface.co/cgeorgiaw/Perch
- https://github.com/google-research/perch/
- https://arxiv.org/abs/2508.04665
- https://github.com/earthspecies/beans/
- https://arxiv.org/abs/2210.12300
- https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct-GGUF
- https://huggingface.co/Qwen/Qwen3-VL-2B-Instruct/blob/main/README.md
- https://huggingface.co/google/gemma-3-4b-it
- https://ai.google.dev/gemma/terms
- https://onnxruntime.ai/docs/tutorials/mobile/
